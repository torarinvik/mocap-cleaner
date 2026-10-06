#!/usr/bin/env python3
"""Incremental, longest-first proof runner for scripts/check.sh.

Each file's result line is cached in build/proof/cache/<key>.txt. The key hashes
  * the file and every file it includes, transitively (include directives are
    found with the prover's own rules, see `include_target`),
  * the prover invocation shape and cache format version, and
  * the prover's *semantic revision* (see `semantic_revision`): what decides the
    verdicts, not the binary bytes. A prover rebuild that changes only scripts,
    docs, tests, examples or the optimization level keeps every cached result;
    a change to the prover sources, the linked compiler frontend, the runtime,
    the compile mode or the target invalidates every result.
When the binary has no build manifest, or the manifest does not describe that
exact binary, the binary hash itself is the revision (every rebuild re-proves).

Files run longest first using the durations recorded by earlier runs (unknown
files go first), PROOF_JOBS at a time (default: the core count). For each file
the result line is written to build/proof/<path with / as _>.txt, and a
`.cached` marker sits beside it when the line came from the cache.

`--recheck-sample N` re-proves N randomly chosen cache hits as well and exits 3
with a loud report if any fresh result differs from the cached one (those cache
entries are replaced by the fresh results; the fresh line is what is reported).

Each fresh file has a positive wall-time limit (default 1800 seconds), set by
`--file-timeout` or PROOF_FILE_TIMEOUT. A timed-out report is invalid and is
never cached. This supervisor limit is independent of producer search fuel.

Usage: prove.py [--recheck-sample N] [--file-timeout SECONDS] PROVER FILE...
"""
import argparse
import hashlib
import json
import math
import os
import random
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

OUT = "build/proof"
CACHE = os.path.join(OUT, "cache")
DURATIONS = os.path.join(CACHE, "durations.json")
KEEP = re.compile(r"verification state|proven:|failed:|unproven:")
# Bump when the key layout or the cached line format changes.
KEY_VERSION = b"prove-cache-v2"
# The prover is run as `PROVER <absolute file>`; part of the key so a change
# here cannot reuse results produced by another invocation.
INVOCATION = b"argv:PROVER,ABSFILE"
SPACE = b" \t\n\v\f\r"


def include_target(line):
    """The include path on one line, as the prover's proof_include_path reads it
    (src/proof/import.elisa): `{$include P}` / `{$I P}` (case-insensitive keyword,
    P quoted with ' or " or a bare word) and `[#]include "P"`. None otherwise."""
    s = line.strip(SPACE)
    if len(s) >= 3 and s[:2] == b"{$" and s[-1:] == b"}":
        body = s[2:-1].strip(SPACE)
        k = 0
        while k < len(body) and body[k] not in SPACE:
            k += 1
        word = body[:k].lower()
        if word not in (b"i", b"include") or k == len(body):
            return None
        arg = body[k:].strip(SPACE)
        if not arg:
            return None
        if len(arg) >= 2 and arg[:1] == arg[-1:] and arg[:1] in (b'"', b"'"):
            return arg[1:-1]
        if not any(c in SPACE for c in arg):
            return arg
        return None
    c = s[1:] if s[:1] == b"#" else s
    c = c.lstrip(SPACE)
    if not c.startswith(b"include "):
        return None
    c = c[len(b"include "):].lstrip(SPACE)
    if len(c) >= 2 and c[:1] == b'"' and c[-1:] == b'"':
        return c[1:-1]
    return None


def sources(path, seen):
    """The file and everything it includes, transitively, in a stable order.
    Lines split on LF only, like the prover. A missing file is still listed
    (hashed as missing), so creating it later changes the key."""
    path = os.path.normpath(path)
    if path in seen:
        return
    seen.append(path)
    try:
        data = open(path, "rb").read()
    except OSError:
        return
    for line in data.split(b"\n"):
        inc = include_target(line)
        if inc is None:
            continue
        inc = os.fsdecode(inc)
        sources(inc if os.path.isabs(inc) else os.path.join(os.path.dirname(path), inc), seen)


def digest(path, revision):
    h = hashlib.sha256(KEY_VERSION + b"\0" + INVOCATION + b"\0" + revision.encode() + b"\0")
    files = []
    sources(path, files)
    for f in files:
        h.update(os.path.abspath(f).encode() + b"\0")
        try:
            h.update(hashlib.sha256(open(f, "rb").read()).digest())
        except OSError:
            h.update(b"<missing>")
        h.update(b"\0")
    return h.hexdigest()


def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def semantic_revision(prover):
    """(revision, how). The fields of the prover's build manifest
    (scripts/build_manifest.py, written beside the binary) that decide what the
    binary computes: the hash of the compiled prover src/ tree (scripts, docs,
    tests and examples are outside it), the compiler frontend revision and tree
    linked into it, the runtime object, compile mode, compiler stage and target.
    Left out on purpose: optimization level and compiler flags (O0..O3 give the
    same reports; a codegen bug is what --recheck-sample is for), the binary and
    compiler-wrapper bytes, paths, the prover git HEAD and dirty flag, and the
    profiler hook object (built from the pinned frontend tree)."""
    binary = file_hash(prover)
    fallback = ("binary:" + binary, "binary hash (no usable manifest)")
    try:
        m = json.load(open(prover + ".manifest.json"))
        if m.get("schema") != "elisa-proof-build-manifest-v1":
            return fallback
        if m["binary"]["sha256"] != binary:
            return fallback[0], "binary hash (manifest describes another binary)"
        fields = {
            "source_tree_sha256": m["proof"]["source_tree_sha256"],
            "frontend_revision": m["frontend"]["revision"],
            "frontend_tree": m["frontend"]["tree"],
            "runtime_sha256": m["runtime"]["sha256"],
            "compile_mode": m["compile_mode"],
            "compiler_stage": m["compiler"]["stage"],
            "target": m["target"],
        }
    except (OSError, ValueError, KeyError, TypeError):
        return fallback
    if any(not v for v in fields.values()):
        return fallback
    blob = json.dumps(fields, sort_keys=True).encode()
    return "semantic:" + hashlib.sha256(blob).hexdigest(), "manifest semantic revision"


def summary(text):
    """Same line check.sh always printed: the kept lines, squeezed and joined."""
    lines = [re.sub(r" +", " ", l) for l in text.splitlines() if KEEP.search(l)]
    return " ".join(lines) + (" " if lines else "")


def main():
    ap = argparse.ArgumentParser(usage=__doc__.rsplit("Usage: ", 1)[1].strip())
    ap.add_argument("--recheck-sample", type=int, default=0, metavar="N")
    ap.add_argument("--file-timeout", type=float,
                    default=os.environ.get("PROOF_FILE_TIMEOUT", "1800"), metavar="SECONDS")
    ap.add_argument("prover")
    ap.add_argument("files", nargs="*")
    args = ap.parse_args()
    if not math.isfinite(args.file_timeout) or args.file_timeout <= 0:
        ap.error("--file-timeout must be a positive finite number of seconds")
    prover, files = args.prover, args.files
    jobs = int(os.environ.get("PROOF_JOBS") or os.cpu_count() or 4)
    os.makedirs(CACHE, exist_ok=True)
    try:
        durations = json.load(open(DURATIONS))
    except (OSError, ValueError):
        durations = {}
    revision, how = semantic_revision(prover)
    todo, hits = [], []
    for f in files:
        out = os.path.join(OUT, f.replace("/", "_") + ".txt")
        key = digest(f, revision)
        cached = os.path.join(CACHE, key + ".txt")
        marker = out[:-4] + ".cached"
        if os.path.exists(cached):
            line = open(cached).read()
            with open(out, "w") as o:
                o.write(line)
            open(marker, "w").close()
            hits.append((f, out, cached, line))
        else:
            if os.path.exists(marker):
                os.remove(marker)
            todo.append((f, out, cached, None))
    sample = random.SystemRandom().sample(hits, min(max(0, args.recheck_sample), len(hits)))
    # Longest first; files never timed go before everything else.
    work = sorted(todo + sample, key=lambda t: -durations.get(t[0], float("inf")))

    def prove(item):
        f, out, cached, old = item
        start = time.monotonic()
        timed_out = False
        try:
            run = subprocess.run([prover, os.path.abspath(f)], capture_output=True,
                                 text=True, timeout=args.file_timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            run = subprocess.CompletedProcess([prover, os.path.abspath(f)], 124,
                stdout="", stderr=f"proof file exceeded {args.file_timeout:g}s wall-time limit; partial output discarded")
        took = time.monotonic() - start
        line = summary(run.stdout)
        if old is not None and line != old:
            # The cache was wrong: report the fresh line, drop the stale one.
            marker = out[:-4] + ".cached"
            if os.path.exists(marker):
                os.remove(marker)
            if os.path.exists(cached):
                os.remove(cached)
        with open(out, "w") as o:
            o.write(line)
        # Never cache an empty result (crash, missing prover output).
        if "verification state" in line and run.returncode >= 0:
            tmp = cached + ".tmp"
            with open(tmp, "w") as o:
                o.write(line)
            os.replace(tmp, cached)
        invalid = timed_out or "verification state" not in line or run.returncode < 0
        if invalid and os.path.exists(cached):
            os.remove(cached)
        diagnostic = (run.stderr or run.stdout).strip() if invalid else ""
        return f, took, old, line, invalid, run.returncode, diagnostic

    mismatches = []
    invalid_runs = []
    with ThreadPoolExecutor(max_workers=max(1, jobs)) as pool:
        for f, took, old, line, invalid, returncode, diagnostic in pool.map(prove, work):
            durations[f] = round(took, 3)
            if invalid:
                invalid_runs.append((f, returncode, diagnostic))
            if old is not None and not invalid and line != old:
                mismatches.append((f, old, line))
    tmp = DURATIONS + ".tmp"
    with open(tmp, "w") as o:
        json.dump(durations, o, indent=1, sort_keys=True)
    os.replace(tmp, DURATIONS)
    print(f"prove: {len(hits)} cached, {len(todo)} processed, {len(sample)} rechecked; "
          f"key: {how} {revision[:24]}", file=sys.stderr)
    if mismatches:
        print("prove: CACHE MISMATCH - cached results differ from a fresh run:", file=sys.stderr)
        for f, old, line in mismatches:
            print(f"  {f}\n    cached: {old}\n    fresh:  {line}", file=sys.stderr)
        sys.exit(3)
    if invalid_runs:
        print("prove: invalid verifier runs (no result or abnormal termination):", file=sys.stderr)
        for f, returncode, diagnostic in invalid_runs:
            print(f"  {f}: exit {returncode}\n    {diagnostic[:2000]}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
