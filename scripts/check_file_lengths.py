#!/usr/bin/env python3
"""Enforce the roadmap's 600-line limit for maintained repository text files."""
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
MAX_LINES = 600


def main():
    names = subprocess.check_output(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
    ).split(b"\0")
    checked = 0
    failures = []
    for encoded in sorted(set(names)):
        if not encoded:
            continue
        name = encoded.decode("utf-8", errors="surrogateescape")
        if name.startswith("build/"):
            continue
        path = ROOT / name
        if not path.is_file():
            continue
        try:
            raw = path.read_bytes()
            if b"\0" in raw:
                continue
            content = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        except OSError as error:
            failures.append(f"{name}: cannot inspect: {error}")
            continue
        checked += 1
        lines = len(content.splitlines())
        if lines > MAX_LINES:
            failures.append(f"{name}: {lines} lines exceeds {MAX_LINES}")
    if failures:
        for failure in failures:
            print(f"file lengths: {failure}", file=sys.stderr)
        return 1
    print(f"file lengths: {checked} maintained text files, all at most {MAX_LINES} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
