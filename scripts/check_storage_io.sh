#!/usr/bin/env bash
# Native Storage adapter checks use only disposable generated files in build/.
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
ENGINE="${ELISA_ENGINE_ROOT:-$ROOT/../elisa-engine-mocap}"
STAGE1="${ELISA_STAGE1:-$ROOT/../Elisa-compiler}"
[[ "$(uname -s)" == Darwin ]] || { echo 'Storage native checks require macOS' >&2; exit 2; }
mkdir -p "$ROOT/build/test"
TASK_FIXTURE="$(mktemp -d "$ROOT/build/test/storage-io.XXXXXX")"
trap 'rm -rf -- "$TASK_FIXTURE"' EXIT
printf 'generated storage fixture\n' > "$TASK_FIXTURE/report.txt"
bash "$STAGE1/scripts/elisac_stage1.sh" -O2 -o "$TASK_FIXTURE/adapter.o" "$ROOT/test/native/studio_file_trash.elisa"
clang -fobjc-arc -Wall -Wextra -Werror -O2 -c "$ENGINE/native/file_trash_appkit.m" -o "$TASK_FIXTURE/trash.o"
clang -std=c11 -Wall -Wextra -Werror -O2 -c "$ENGINE/native/file_path.c" -o "$TASK_FIXTURE/path.o"
clang "$TASK_FIXTURE/adapter.o" "$TASK_FIXTURE/trash.o" "$TASK_FIXTURE/path.o" "$STAGE1/build/runtime/elisacore_runtime.o" -framework Foundation -o "$TASK_FIXTURE/check"
"$TASK_FIXTURE/check" "$ROOT/build" "$TASK_FIXTURE/report.txt"
