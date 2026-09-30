#!/usr/bin/env python3
"""Per-function proof status: proved functions vs. those with open goals."""
import json, os, subprocess, sys

prover = os.environ.get("ELISA_PROOF", os.path.join(os.path.dirname(__file__), "../../elisa-proof-mocap/build/elisa-proof"))
for path in sys.argv[1:]:
    out = subprocess.run([prover, "--json", os.path.abspath(path)], capture_output=True, text=True).stdout
    try:
        goals = json.loads(out)["goals"]
    except (ValueError, KeyError):
        print(f"{path}: no report")
        continue
    status = {}
    for g in goals:
        fn = g["name"].split(".")[0]
        status[fn] = status.get(fn, True) and g["proven"]
    done = sorted(f for f, ok in status.items() if ok)
    open_ = sorted(f for f, ok in status.items() if not ok)
    print(f"{path}: {len(done)}/{len(status)} functions proved; open: {', '.join(open_) or '-'}")
