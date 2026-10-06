#!/usr/bin/env bash
# Prove the mocap-cleaner corpus on the compute fleet with a cross-run content cache.
# Use the current compiler checkout and committed mocap prover HEAD by default.
# Explicit historical comparisons can override PROVER_REV, ELISA_PROOF_REPO,
# ELISA_STAGE1_ROOT and ELISA_COMPILER_SRC.
#
#   fleet_corpus.sh [--quick] [--compare BASE] [--out FILE] [--no-cache] [FILE...]
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECTS="$(cd "$HERE/../../.." && pwd)"
export ELISA_STAGE1_ROOT="${ELISA_STAGE1_ROOT:-$PROJECTS/Elisa-compiler}"
export ELISA_COMPILER_SRC="${ELISA_COMPILER_SRC:-$ELISA_STAGE1_ROOT}"
export SSH_CONFIG="${SSH_CONFIG:-$HOME/.ssh/fleet_config}" WINPC="${WINPC:-vast}"
export REMOTE_BASE="${REMOTE_BASE:-work/mocap-fleet}"
args=()
case " $* " in *" --prover-rev "*|*" --prover-src "*|*" --clean "*) ;;
    *) args=(--prover-src "${ELISA_PROOF_REPO:-$PROJECTS/elisa-proof-mocap}"
             --prover-rev "${PROVER_REV:-HEAD}") ;; esac
exec python3 "$HERE/fleet_corpus.py" ${args[@]+"${args[@]}"} "$@"
