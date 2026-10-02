#!/usr/bin/env python3
"""Incremental, longest-first proof runner for scripts/check.sh.

Each file's result line is cached in build/proof/cache/<key>.txt, where the
key hashes the file, every file it includes (transitively) and the prover
binary, so an unchanged file is not re-proved. Files run longest first using
the durations recorded by earlier runs (unknown files go first), PROOF_JOBS at
a time (default: the core count). For each file the result line is written to
build/proof/<path with / as _>.txt, and a `.cached` marker sits beside it when
the line came from the cache.

Usage: prove.py PROVER FILE...
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

OUT = "build/proof"
CACHE = os.path.join(OUT, "cache")
DURATIONS = os.path.join(CACHE, "durations.json")
INCLUDE = re.compile(r'^\s*include\s+"([^"]+)"', re.M)
KEEP = re.compile(r"verification state|proven:|failed:|unproven:")


def sources(path, seen):
    """The file and everything it includes, transitively, in a stable order."""
    path = os.path.normpath(path)
    if path in seen:
        return
    seen.append(path)
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return
    for inc in INCLUDE.findall(text):
        sources(os.path.join(os.path.dirname(path), inc), seen)


def digest(path, prover_hash):
    h = hashlib.sha256(prover_hash.encode())
    files = []
    sources(path, files)
    for f in files:
        h.update(f.encode() + b"\0")
        try:
            h.update(open(f, "rb").read())
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


def summary(text):
    """Same line check.sh always printed: the kept lines, squeezed and joined."""
    lines = [re.sub(r" +", " ", l) for l in text.splitlines() if KEEP.search(l)]
    return " ".join(lines) + (" " if lines else "")


def main():
    prover, files = sys.argv[1], sys.argv[2:]
    jobs = int(os.environ.get("PROOF_JOBS") or os.cpu_count() or 4)
    os.makedirs(CACHE, exist_ok=True)
    try:
        durations = json.load(open(DURATIONS))
    except (OSError, ValueError):
        durations = {}
    prover_hash = file_hash(prover)
    todo = []
    for f in files:
        out = os.path.join(OUT, f.replace("/", "_") + ".txt")
        key = digest(f, prover_hash)
        cached = os.path.join(CACHE, key + ".txt")
        marker = out[:-4] + ".cached"
        if os.path.exists(cached):
            with open(out, "w") as o:
                o.write(open(cached).read())
            open(marker, "w").close()
        else:
            if os.path.exists(marker):
                os.remove(marker)
            todo.append((f, out, cached))
    # Longest first; files never timed go before everything else.
    todo.sort(key=lambda t: -durations.get(t[0], float("inf")))

    def prove(item):
        f, out, cached = item
        start = time.monotonic()
        run = subprocess.run([prover, os.path.abspath(f)], capture_output=True, text=True)
        took = time.monotonic() - start
        line = summary(run.stdout)
        with open(out, "w") as o:
            o.write(line)
        # Never cache an empty result (crash, missing prover output).
        if "verification state" in line:
            tmp = cached + ".tmp"
            with open(tmp, "w") as o:
                o.write(line)
            os.replace(tmp, cached)
        return f, took

    with ThreadPoolExecutor(max_workers=max(1, jobs)) as pool:
        for f, took in pool.map(prove, todo):
            durations[f] = round(took, 3)
    tmp = DURATIONS + ".tmp"
    with open(tmp, "w") as o:
        json.dump(durations, o, indent=1, sort_keys=True)
    os.replace(tmp, DURATIONS)


if __name__ == "__main__":
    main()
