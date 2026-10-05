#!/usr/bin/env python3
"""Fail when a source or proof file regresses from its reviewed corpus status."""
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BASELINE = Path(__file__).with_name("proof-baseline.tsv")
RANK = {"proved": 0, "unknown": 1, "unsupported": 2}
REPORT = re.compile(
    r"verification state: (\w+).*?proven: (\d+).*?unproven: (\d+)"
)


def read_baseline():
    rows = {}
    for number, line in enumerate(BASELINE.read_text().splitlines(), 1):
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) != 4:
            raise ValueError(f"{BASELINE}:{number}: expected four tab-separated fields")
        path, state, proven, unproven = fields
        if path in rows:
            raise ValueError(f"{BASELINE}:{number}: duplicate path {path}")
        rows[path] = (state, int(proven), int(unproven))
    return rows


def read_report(path):
    report = ROOT / "build" / "proof" / (path.replace("/", "_") + ".txt")
    match = REPORT.search(report.read_text())
    if match is None:
        raise ValueError(f"{path}: missing or unrecognized proof report at {report}")
    state, proven, unproven = match.groups()
    return state, int(proven), int(unproven)


def main(paths):
    baseline = read_baseline()
    current_paths = set(paths)
    errors = []
    improved = 0
    for path in sorted(current_paths):
        expected = baseline.get(path)
        if expected is None:
            errors.append(f"{path}: no reviewed proof baseline")
            continue
        try:
            actual = read_report(path)
        except (OSError, ValueError) as error:
            errors.append(str(error))
            continue
        old_state, _, old_open = expected
        state, _, open_goals = actual
        if state not in RANK or old_state not in RANK:
            errors.append(f"{path}: unknown status {old_state!r} -> {state!r}")
        elif RANK[state] > RANK[old_state] or open_goals > old_open:
            errors.append(
                f"{path}: proof regression {old_state}/{old_open} -> {state}/{open_goals}"
            )
        elif RANK[state] < RANK[old_state] or open_goals < old_open:
            improved += 1
    for path in sorted(set(baseline) - current_paths):
        errors.append(f"{path}: stale proof baseline entry")
    if errors:
        print("proof baseline: regression or review needed")
        for error in errors:
            print(f"  {error}")
        return 1
    print(f"proof baseline: {len(current_paths)} files checked, {improved} improved, no regressions")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except (OSError, ValueError) as error:
        print(f"proof baseline: {error}", file=sys.stderr)
        sys.exit(2)
