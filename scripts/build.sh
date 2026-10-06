#!/bin/sh
# Build the headless CLI (elisa.project.json, host "console") through
# Elisa-engine's scripts/elisa_build_run.py.
#
#   scripts/build.sh                    build build/mocap-cleaner
#   scripts/build.sh run -- clean ...   build and run with arguments
#
# Environment: ELISA_ENGINE_ROOT (../elisa-engine-mocap), ELISAC
# (../Elisa-compiler/scripts/elisac_stage1.sh).
set -eu
ROOT=$(cd "$(dirname "$0")/.." && pwd)
ENGINE="${ELISA_ENGINE_ROOT:-$ROOT/../elisa-engine-mocap}"
ELISAC="${ELISAC:-$ROOT/../Elisa-compiler/scripts/elisac_stage1.sh}"
export MOCAP_CLI_COMPILER="$(cd "$(dirname "$ELISAC")" && pwd)/$(basename "$ELISAC")"
export ELISA_COMPILER_BIN="$ROOT/scripts/cli_compiler.py"
export ELISA_ENGINE_ROOT="$ENGINE"
action="${1:-build}"; [ $# -gt 0 ] && shift
exec python3 "$ENGINE/scripts/elisa_build_run.py" "$action" --project "$ROOT" "$@"
