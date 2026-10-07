#!/usr/bin/env python3
"""Reject consecutive integer-literal pushes into the same Elisa array.

This lexical check covers maintained Elisa files. It does not classify loops,
computed values or non-integer expressions as fixed byte sequences.
"""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent
PUSH = re.compile(r"^(\s*)([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)\.push\((?:0x[0-9a-fA-F]+|[+-]?[0-9]+)\)\s*$")


def runs(content):
    previous = None
    first = 0
    count = 0
    for number, line in enumerate(content.splitlines() + [""], 1):
        match = PUSH.match(line)
        key = (match[1], match[2]) if match else None
        if key != previous:
            if count > 1:
                yield first, count, previous[1]
            first = number
            count = 0
            previous = key
        if match:
            count += 1


def main():
    names = subprocess.check_output(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
    ).split(b"\0")
    failures = 0
    for encoded in sorted(set(names)):
        if not encoded:
            continue
        name = encoded.decode("utf-8", errors="surrogateescape")
        if not name.endswith(".elisa") or name.startswith("build/"):
            continue
        path = ROOT / name
        if not path.is_file():
            continue
        for line, count, target in runs(path.read_text(encoding="utf-8")):
            print(f"{name}:{line}: extend {target} with these {count} literals")
            failures += 1
    print(f"literal push runs: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
