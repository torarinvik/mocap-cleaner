#!/usr/bin/env bash
# Prove the mocap-cleaner corpus on the compute fleet with a cross-run content cache.
# Thin wrapper over fleet_corpus.py (see its --help) that pins the current prover base:
# elisa-proof branch agent/prover-bb40-views (frontend 2678ff10), cross-compiled with the
# studio-globals stage1 and linked on vast. Override with the same env/flags as the .py:
#   PROVER_REV, ELISA_PROOF_REPO, ELISA_STAGE1_ROOT, ELISA_COMPILER_SRC, FLEET_HOSTS.
#
#   fleet_corpus.sh [--quick] [--compare BASE] [--out FILE] [--no-cache] [FILE...]
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECTS="$(cd "$HERE/../../.." && pwd)"
export ELISA_STAGE1_ROOT="${ELISA_STAGE1_ROOT:-$PROJECTS/elisa-compiler-worktrees/studio-globals}"
export ELISA_COMPILER_SRC="${ELISA_COMPILER_SRC:-$ELISA_STAGE1_ROOT}"
export SSH_CONFIG="${SSH_CONFIG:-$HOME/.ssh/fleet_config}" WINPC="${WINPC:-vast}"
export REMOTE_BASE="${REMOTE_BASE:-work/mocap-fleet}"
args=()
case " $* " in *" --prover-rev "*|*" --prover-src "*|*" --clean "*) ;;
    *) args=(--prover-src "${ELISA_PROOF_REPO:-$PROJECTS/elisa-proof}"
             --prover-rev "${PROVER_REV:-agent/prover-bb40-views}") ;; esac
exec python3 "$HERE/fleet_corpus.py" ${args[@]+"${args[@]}"} "$@"
