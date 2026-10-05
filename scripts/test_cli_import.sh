#!/bin/sh
# Focused regression for safe CLI handling of an empty/malformed GLB.
set -eu
ROOT=$(cd "$(dirname "$0")/.." && pwd)
CLI=${1:-$ROOT/build/mocap-cleaner}
FIXTURE="$ROOT/build/cli-import-validation"
mkdir -p "$FIXTURE"
: > "$FIXTURE/empty.glb"
python3 - "$FIXTURE/no-animation.glb" <<'PY'
import json
import struct
import sys

payload = json.dumps({"asset": {"version": "2.0"}, "nodes": []},
                     separators=(",", ":")).encode()
payload += b" " * (-len(payload) % 4)
total = 12 + 8 + len(payload)
with open(sys.argv[1], "wb") as stream:
    stream.write(struct.pack("<III", 0x46546C67, 2, total))
    stream.write(struct.pack("<II", len(payload), 0x4E4F534A))
    stream.write(payload)
PY
for name in empty no-animation; do
    rm -f "$FIXTURE/out.glb"
    set +e
    output=$("$CLI" clean "$FIXTURE/$name.glb" -o "$FIXTURE/out.glb" --preset raw 2>&1)
    status=$?
    set -e
    [ "$status" -eq 1 ] || { printf '%s: expected exit 1, got %s\n%s\n' "$name" "$status" "$output" >&2; exit 1; }
    printf '%s\n' "$output" | grep -q 'input could not be loaded or has no usable animations' || { printf '%s: missing diagnostic\n%s\n' "$name" "$output" >&2; exit 1; }
    [ ! -e "$FIXTURE/out.glb" ] || { echo "$name input produced an output file" >&2; exit 1; }
done
printf 'cli import validation: malformed and animationless inputs rejected without output\n'
