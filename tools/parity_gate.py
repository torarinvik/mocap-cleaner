#!/usr/bin/env python3
"""Phase 0 boxing parity gate.

Compares three versions of each boxing dual-stance GLB:

  raw      the merge step's output before leg cleanup. The boxing repo's
           build/dual-stance GLBs are cleaned in place, so the raw version is
           regenerated here by running elisa-boxing-game/tools/merge_dual_stance_glb.py
           with its output directory redirected to build/parity/raw/. The merge
           is plain Python (no Blender). The regenerated file's sha256 is checked
           against the boxing merge manifest.
  boxing   elisa-boxing-game/build/dual-stance/<c>/<c>-boxer.glb (cleaned by
           tools/clean_leg_motion.py in Blender). Read only.
  mocap    build/mocap-cleaner clean <raw> <out> --preset boxing.

Metric, per clip and per version: leg bones (UpLeg, Leg, Foot, ToeBase, both
sides) have their rotation tracks sampled on a uniform RATE grid (LINEAR
sampler interpolation, quaternion nlerp). Angular velocity is the rotation
angle between consecutive frames times RATE; angular acceleration is its
first difference times RATE. A spike is a frame where |acceleration| exceeds
SPIKE_THRESHOLD; the peak is the largest |acceleration| in the clip. The same
threshold applies to all three versions.

Gate: for every clip, mocap_spikes <= boxing_spikes * TOLERANCE, where
TOLERANCE = 1.25 lets mocap-cleaner leave up to 25% more spikes than the
Blender cleanup. When boxing has 0 spikes, mocap must also have 0.

Writes only under build/parity/. Exits 0 when every clip passes, 1 otherwise.
"""
import hashlib
import json
import math
import struct
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
BOXING = ROOT.parent / "elisa-boxing-game"
OUT = ROOT / "build/parity"
CLI = ROOT / "build/mocap-cleaner"
CHARACTERS = ("black", "white")
PREFIX = "mixamorig:"
LEG_BONES = [PREFIX + s + b for s in ("Left", "Right") for b in ("UpLeg", "Leg", "Foot", "ToeBase")]
RATE = 120.0                        # Hz sampling grid (the rate clean_leg_motion.py writes)
SPIKE_THRESHOLD = 2000.0            # deg/s^2 angular-acceleration magnitude counted as a spike
TOLERANCE = 1.25                    # mocap spikes may be at most boxing spikes * TOLERANCE


def load(path):
    raw = path.read_bytes()
    length, kind = struct.unpack_from("<II", raw, 12)
    assert kind == 0x4E4F534A
    doc = json.loads(raw[20:20 + length])
    off = 20 + length
    blen, bkind = struct.unpack_from("<II", raw, off)
    assert bkind == 0x004E4942
    return doc, raw[off + 8:off + 8 + blen]


COMPONENTS = {"SCALAR": 1, "VEC3": 3, "VEC4": 4}
DTYPES = {5126: np.float32, 5122: np.int16, 5123: np.uint16, 5120: np.int8, 5121: np.uint8}


def accessor(doc, blob, index):
    acc = doc["accessors"][index]
    view = doc["bufferViews"][acc["bufferView"]]
    n = COMPONENTS[acc["type"]]
    dtype = DTYPES[acc["componentType"]]
    start = view.get("byteOffset", 0) + acc.get("byteOffset", 0)
    stride = view.get("byteStride", 0) or n * np.dtype(dtype).itemsize
    data = np.ndarray((acc["count"], n), dtype=dtype, buffer=blob, offset=start, strides=(stride, np.dtype(dtype).itemsize))
    data = data.astype(np.float64)
    if acc.get("normalized") or dtype is not np.float32:
        data /= {np.int16: 32767.0, np.uint16: 65535.0, np.int8: 127.0, np.uint8: 255.0}[dtype]
    return data


def sample_quats(times, quats, grid, step):
    if step:
        idx = np.clip(np.searchsorted(times, grid, side="right") - 1, 0, len(times) - 1)
        return quats[idx]
    idx = np.clip(np.searchsorted(times, grid, side="right") - 1, 0, len(times) - 2) if len(times) > 1 else None
    if idx is None:
        return np.repeat(quats[:1], len(grid), axis=0)
    t0, t1 = times[idx], times[idx + 1]
    u = np.clip((grid - t0) / np.maximum(t1 - t0, 1e-9), 0.0, 1.0)[:, None]
    a, b = quats[idx], quats[idx + 1]
    b = np.where((np.sum(a * b, axis=1) < 0)[:, None], -b, b)
    q = a * (1 - u) + b * u
    return q / np.linalg.norm(q, axis=1, keepdims=True)


def clip_metrics(doc, blob):
    names = {n.get("name"): i for i, n in enumerate(doc["nodes"])}
    legs = {names[b] for b in LEG_BONES if b in names}
    result = {}
    for anim in doc["animations"]:
        tracks = []
        end = 0.0
        for ch in anim["channels"]:
            if ch["target"].get("node") in legs and ch["target"]["path"] == "rotation":
                s = anim["samplers"][ch["sampler"]]
                t = accessor(doc, blob, s["input"])[:, 0]
                if s.get("interpolation") == "CUBICSPLINE":
                    q = accessor(doc, blob, s["output"])[1::3]
                else:
                    q = accessor(doc, blob, s["output"])
                tracks.append((t, q, s.get("interpolation") == "STEP"))
                end = max(end, float(t[-1]))
        if not tracks:
            continue
        grid = np.arange(0.0, end + 1e-9, 1.0 / RATE)
        acc_all = []
        for t, q, step in tracks:
            g = sample_quats(t, q, grid, step)
            dot = np.clip(np.abs(np.sum(g[1:] * g[:-1], axis=1)), 0.0, 1.0)
            vel = np.degrees(2.0 * np.arccos(dot)) * RATE
            acc_all.append(np.abs(np.diff(vel)) * RATE)
        acc = np.concatenate(acc_all) if acc_all else np.zeros(0)
        result[anim["name"]] = {"spikes": int(np.sum(acc > SPIKE_THRESHOLD)),
                                "peak": float(acc.max()) if acc.size else 0.0}
    return result


def regenerate_raw():
    """Run the boxing merge with OUT redirected; sources stay read-only."""
    raw_dir = OUT / "raw"
    script = (BOXING / "tools/merge_dual_stance_glb.py").read_text()
    needle = 'OUT = ROOT / "build/dual-stance"'
    assert needle in script, "merge script layout changed"
    script = script.replace(needle, f"OUT = Path({str(raw_dir)!r})")
    script = script.replace('str(output.relative_to(ROOT))', 'str(output)')
    code = ("import sys; sys.path.insert(0, %r); __file__ = %r\n" % (str(BOXING / "tools"), str(BOXING / "tools/merge_dual_stance_glb.py"))) + script
    subprocess.run([sys.executable, "-c", code], check=True)
    manifest = json.loads((BOXING / "build/dual-stance/manifest.json").read_text())
    for rec in manifest["records"]:
        path = raw_dir / rec["character"] / f"{rec['character']}-boxer.glb"
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != rec["sha256"]:
            sys.exit(f"regenerated raw {path} sha256 {digest} != boxing manifest {rec['sha256']}")
    return raw_dir


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    raw_dir = regenerate_raw()
    rows, ok = [], True
    report = {"threshold_deg_s2": SPIKE_THRESHOLD, "rate_hz": RATE, "tolerance": TOLERANCE, "clips": []}
    for c in CHARACTERS:
        raw_path = raw_dir / c / f"{c}-boxer.glb"
        boxing_path = BOXING / f"build/dual-stance/{c}/{c}-boxer.glb"
        mocap_path = OUT / "mocap" / f"{c}-boxer.glb"
        mocap_path.parent.mkdir(parents=True, exist_ok=True)
        cli = subprocess.run([str(CLI), "clean", str(raw_path), str(mocap_path), "--preset", "boxing"],
                             capture_output=True, text=True)
        (OUT / f"cli-{c}.log").write_text(cli.stdout + cli.stderr)
        if cli.returncode != 0:
            sys.exit(f"mocap-cleaner failed on {c}: see {OUT / f'cli-{c}.log'}")
        m = [clip_metrics(*load(p)) for p in (raw_path, boxing_path, mocap_path)]
        for clip in m[0]:
            r, b, x = m[0][clip], m[1].get(clip), m[2].get(clip)
            limit = b["spikes"] * TOLERANCE
            passed = x["spikes"] <= limit
            ok &= passed
            rows.append((c, clip, r, b, x, passed))
            report["clips"].append({"character": c, "clip": clip, "raw": r, "boxing": b, "mocap": x, "pass": passed})
    print(f"leg angular-acceleration spikes > {SPIKE_THRESHOLD:.0f} deg/s^2 at {RATE:.0f} Hz; "
          f"gate: mocap <= boxing * {TOLERANCE}")
    print(f"{'char':5} {'clip':22} {'raw':>6} {'boxing':>6} {'mocap':>6}   {'peak raw':>9} {'boxing':>9} {'mocap':>9}  gate")
    for c, clip, r, b, x, passed in rows:
        print(f"{c:5} {clip:22} {r['spikes']:6d} {b['spikes']:6d} {x['spikes']:6d}   "
              f"{r['peak']:9.0f} {b['peak']:9.0f} {x['peak']:9.0f}  {'PASS' if passed else 'FAIL'}")
    tot = [sum(row[i]["spikes"] for row in rows) for i in (2, 3, 4)]
    npass = sum(row[5] for row in rows)
    print(f"total spikes raw {tot[0]}, boxing {tot[1]}, mocap {tot[2]}; {npass}/{len(rows)} clips pass")
    (OUT / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
