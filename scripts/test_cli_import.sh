#!/bin/sh
# Focused regression for safe CLI handling of an empty/malformed GLB.
set -eu
ROOT=$(cd "$(dirname "$0")/.." && pwd)
CLI=${1:-$ROOT/build/mocap-cleaner}
FIXTURE="$ROOT/build/cli-import-validation"
mkdir -p "$FIXTURE"
: > "$FIXTURE/empty.glb"
rm -f "$FIXTURE/out.glb"
set +e
output=$("$CLI" clean "$FIXTURE/empty.glb" -o "$FIXTURE/out.glb" --preset raw 2>&1)
status=$?
set -e
[ "$status" -eq 1 ] || { printf 'expected exit 1, got %s\n%s\n' "$status" "$output" >&2; exit 1; }
printf '%s\n' "$output" | grep -q 'input could not be loaded or has no usable animations'
[ ! -e "$FIXTURE/out.glb" ] || { echo 'invalid input produced an output file' >&2; exit 1; }
printf 'cli import validation: malformed input rejected without output\n'
