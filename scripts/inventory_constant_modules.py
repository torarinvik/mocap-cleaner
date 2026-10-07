#!/usr/bin/env python3
"""List Elisa file and module scopes with multiple ungrouped constants.

This is a lexical review inventory, not a substitute for semantic API review.
Enum variants, const modules and function-local constants are excluded.
"""
import argparse
from collections import defaultdict
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parent.parent
DECLARATION = re.compile(r"^(const\s+)?(module|enum|extend)\s+([A-Za-z_]\w*(?:::[A-Za-z_]\w*)*)")
FUNCTION = re.compile(r"^(?:async\s+)?def\s+")
CONSTANT = re.compile(r"^const\s+([A-Za-z_]\w*)\s*[:=]")


def candidates(content):
    scopes = []
    constants = defaultdict(list)
    for number, line in enumerate(content.splitlines(), 1):
        text = line.lstrip()
        if not text or text.startswith("#"):
            continue
        indent = len(line) - len(text)
        while scopes and indent <= scopes[-1][0]:
            scopes.pop()
        declaration = DECLARATION.match(text)
        if declaration:
            const, kind, name = declaration.groups()
            scopes.append((indent, "module" if kind == "extend" else kind, name, bool(const), number))
            continue
        if FUNCTION.match(text):
            scopes.append((indent, "function", "", False, number))
            continue
        constant = CONSTANT.match(text)
        if not constant or any(scope[1] == "function" for scope in scopes):
            continue
        if any(scope[1] == "enum" or scope[3] for scope in scopes):
            continue
        modules = [scope for scope in scopes if scope[1] == "module"]
        owner = (("::".join(scope[2] for scope in modules), modules[-1][4])
                 if modules else ("<file>", 0))
        constants[owner].append((number, constant.group(1)))
    return list(constants.items())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="fail when any owner has multiple ungrouped constants")
    args = parser.parse_args()
    names = subprocess.check_output(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
    ).split(b"\0")
    owners = defaultdict(list)
    for encoded in sorted(set(names)):
        if not encoded:
            continue
        name = encoded.decode("utf-8", errors="surrogateescape")
        if not name.endswith(".elisa") or name.startswith("build/"):
            continue
        path = ROOT / name
        if not path.is_file():
            continue
        for (owner, line), values in candidates(path.read_text(encoding="utf-8")):
            scope_key = f"{name}:<file>" if owner == "<file>" else owner
            owners[scope_key].extend((name, number, symbol) for number, symbol in values)
    count = 0
    for owner, values in sorted(owners.items()):
        if len(values) < 2:
            continue
        declarations = ", ".join(f"{name}:{number}:{symbol}"
                                 for name, number, symbol in values)
        print(f"{owner}: {declarations}")
        count += 1
    print(f"constant inventory: {count} file/module scopes require review")
    return 1 if args.check and count else 0



if __name__ == "__main__":
    raise SystemExit(main())
