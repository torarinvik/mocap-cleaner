#!/usr/bin/env bash
# Build a Linux elisa-proof on winpc from an elisa-proof-mocap revision or working tree.
#
# Mac binaries do not run on winpc, and winpc can neither hold a stage1 compile of the
# prover in RAM (~4 GB peak plus agents) nor generate code with its own elisac. So the
# object is CROSS-compiled here (-target-triple x86_64-unknown-linux-gnu) and only linked
# on winpc against a Linux runtime object that is cross-compiled the same way.
#
# The result is cached on winpc under ~/work/mocap-offload/provers/<key>/ where key names
# the source revision, a hash of any uncommitted changes, the opt level and the compiler,
# so an unchanged source never rebuilds. The last stdout line is the remote prover path.
#
#   remote_prover.sh                       working tree of ../elisa-proof-mocap, O2
#   remote_prover.sh --rev 3244c9d         that commit (git archive; ignores the work tree)
#   remote_prover.sh --src <worktree>      another elisa-proof checkout
#   remote_prover.sh --replay              also build elisa-proof-replay (needed by tests)
#   remote_prover.sh --key                 print the cache key only (no build)
#   remote_prover.sh --runtime             only ensure the Linux runtime object; print its path
#
# Environment: ELISA_STAGE1_ROOT (stage1 worktree, default elisa-compiler-worktrees/
# local-shadow, the compiler the installed Mac prover uses), ELISA_COMPILER_SRC (git repo
# holding the pinned frontend revision, default ../Elisa-compiler; only read with
# git archive), WINPC (ssh host, default winpc), REMOTE_BASE (default work/mocap-offload).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECTS="$(cd "$HERE/../../.." && pwd)"
SRC="$PROJECTS/elisa-proof-mocap"
REV=""
OPT="${ELISA_OPT_LEVEL:-O2}"
REPLAY=0
KEY_ONLY=0
RUNTIME_ONLY=0
while [[ $# -gt 0 ]]; do
    case "$1" in
        --src) SRC="$(cd "$2" && pwd)"; shift 2 ;;
        --rev) REV="$2"; shift 2 ;;
        --opt) OPT="$2"; shift 2 ;;
        --replay) REPLAY=1; shift ;;
        --key) KEY_ONLY=1; shift ;;
        --runtime) RUNTIME_ONLY=1; shift ;;
        -h|--help) sed -n 2,24p "$0"; exit 0 ;;
        *) echo "unknown argument: $1" >&2; exit 2 ;;
    esac
done
CROOT="${ELISA_STAGE1_ROOT:-$PROJECTS/elisa-compiler-worktrees/local-shadow}"
CSRC="${ELISA_COMPILER_SRC:-$PROJECTS/Elisa-compiler}"
WINPC="${WINPC:-winpc}"
RBASE="${REMOTE_BASE:-work/mocap-offload}"
LOCAL="${MOCAP_OFFLOAD_CACHE:-$HOME/.cache/mocap-offload}"
PRODUCT="$CROOT/bin/elisac-stage1"
[[ -x "$PRODUCT" ]] || { echo "no stage1 product at $PRODUCT" >&2; exit 2; }

sha() { shasum -a 256 | cut -c1-"${1:-64}"; }
tree_hash() { # content hash of the given dirs under $1 (paths + bytes)
    (cd "$1" && find "${@:2}" -type f ! -name .DS_Store -print0 | LC_ALL=C sort -z \
        | xargs -0 shasum -a 256) | sha "${HASH_LEN:-16}"
}

# --- source identity ---------------------------------------------------------------
if [[ -n "$REV" ]]; then
    full="$(git -C "$SRC" rev-parse --verify "$REV^{commit}")"
    srcid="${full:0:12}"
    PINNED="$(git -C "$SRC" show "$full:ELISA_COMPILER_REV" | tr -d '[:space:]')"
else
    full="$(git -C "$SRC" rev-parse HEAD)"
    srcid="${full:0:12}"
    if [[ -n "$(git -C "$SRC" status --porcelain -- src examples ELISA_COMPILER_REV | grep -v '\.DS_Store$' || true)" ]]; then
        # Dirty: name the uncommitted content, not just HEAD.
        srcid="$srcid-d$(HASH_LEN=10 tree_hash "$SRC" src examples)"
    fi
    PINNED="$(tr -d '[:space:]' < "$SRC/ELISA_COMPILER_REV")"
fi
PINNED="$(git -C "$CSRC" rev-parse --verify "$PINNED^{commit}")"
cid="$( { shasum -a 256 "$PRODUCT" | cut -c1-64; echo "$PINNED"; } | sha 8)"
KEY="$srcid-$OPT-c$cid"
if [[ "$KEY_ONLY" == 1 ]]; then echo "$KEY"; exit 0; fi
# --- Linux runtime object (shared with remote_check.sh) ------------------------------
# The runtime must be generated for the Linux host too (else it calls sysctlbyname).
export ELISA_HOST_LINUX=1 ELISA_HOST_X86_64=1 ELISA_ALLOW_STALE_STAGE1=1
export ELISA_STAGE1_MAX_RSS_KB="${ELISA_STAGE1_MAX_RSS_KB:-8388608}"
TRIPLE=x86_64-unknown-linux-gnu
# Keyed by the product and the runtime sources.
RKEY="$( { shasum -a 256 "$PRODUCT" | cut -c1-64; tree_hash "$CROOT" elisacore_std; \
          shasum -a 256 "$CROOT/scripts/write_profiler_hook_fallbacks.sh" | cut -c1-64; } | sha 16)"
RT="$LOCAL/runtime/$RKEY"
if [[ ! -s "$RT/rt.o" ]]; then
    mkdir -p "$RT"
    ELISA_STAGE1_RUNTIME_STD=1 "$PRODUCT" -emit obj -O0 -target-triple "$TRIPLE" \
        -o "$RT/rt.o.tmp" "$CROOT/elisacore_std/native_runtime_support.elisa"
    bash "$CROOT/scripts/write_profiler_hook_fallbacks.sh" --host-callbacks > "$RT/hooks.c"
    mv -f "$RT/rt.o.tmp" "$RT/rt.o"
fi

ssh "$WINPC" "mkdir -p $RBASE/runtime/$RKEY"
if ! ssh "$WINPC" "test -s $RBASE/runtime/$RKEY/elisacore_runtime.o"; then
    rsync -az "$RT/rt.o" "$RT/hooks.c" "$WINPC:$RBASE/runtime/$RKEY/"
    ssh "$WINPC" "set -e; cd $RBASE/runtime/$RKEY; clang -fno-builtin -c -o hooks.o hooks.c
        clang -r -o elisacore_runtime.o.tmp rt.o hooks.o; mv -f elisacore_runtime.o.tmp elisacore_runtime.o"
fi
if [[ "$RUNTIME_ONLY" == 1 ]]; then echo "$RBASE/runtime/$RKEY/elisacore_runtime.o"; exit 0; fi

RDIR="$RBASE/provers/$KEY"
want="elisa-proof"; [[ "$REPLAY" == 1 ]] && want="elisa-proof-replay"
if ssh "$WINPC" "test -x $RDIR/elisa-proof && test -x $RDIR/$want"; then
    echo "cached: $KEY" >&2
    echo "$RDIR/elisa-proof"; exit 0
fi

# --- snapshot and cross-compile -----------------------------------------------------
W="$LOCAL/build/$KEY"
mkdir -p "$W"
LOCK="$W/.lock"
until mkdir "$LOCK" 2>/dev/null; do
    echo "waiting for another build of $KEY ($(cat "$LOCK/pid" 2>/dev/null))" >&2; sleep 20
done
echo $$ > "$LOCK/pid"
trap 'rm -rf "$LOCK"' EXIT
SNAP="$W/snap"
if [[ "$(cat "$SNAP/Elisa-compiler/.rev" 2>/dev/null)" != "$PINNED" ]]; then
    rm -rf "$SNAP/Elisa-compiler"; mkdir -p "$SNAP/Elisa-compiler"
    git -C "$CSRC" archive --format=tar "$PINNED" src elisacore_std test/parity/profile_hooks.c \
        | tar -x -C "$SNAP/Elisa-compiler"
    echo "$PINNED" > "$SNAP/Elisa-compiler/.rev"
fi
rm -rf "$SNAP/elisa-proof"; mkdir -p "$SNAP/elisa-proof"
if [[ -n "$REV" ]]; then
    git -C "$SRC" archive --format=tar "$full" src examples | tar -x -C "$SNAP/elisa-proof"
else
    cp -R "$SRC/src" "$SRC/examples" "$SNAP/elisa-proof/"
fi
mains=(main)
[[ "$REPLAY" == 1 ]] && mains+=(replay_main)
for m in "${mains[@]}"; do
    if [[ ! -s "$W/$m.o" ]]; then
        t0=$(date +%s)
        "$CROOT/scripts/elisac_stage1.sh" -emit obj "-$OPT" -target-triple "$TRIPLE" \
            -o "$W/$m.o.tmp" "$SNAP/elisa-proof/src/$m.elisa"
        mv -f "$W/$m.o.tmp" "$W/$m.o"
        echo "cross-compiled $m.elisa at $OPT in $(( $(date +%s) - t0 ))s" >&2
    fi
done

# --- link on winpc --------------------------------------------------------------------
ssh "$WINPC" "mkdir -p $RDIR.tmp"
objs=("$SNAP/Elisa-compiler/test/parity/profile_hooks.c" "$SNAP/elisa-proof/examples/verified.elisa")
for m in "${mains[@]}"; do objs+=("$W/$m.o"); done
rsync -az "${objs[@]}" "$WINPC:$RDIR.tmp/"
{
    echo "key: $KEY"; echo "source: $SRC"; echo "revision: $full"; echo "source_id: $srcid"
    echo "opt: $OPT"; echo "stage1: $CROOT ($(git -C "$CROOT" rev-parse --short HEAD 2>/dev/null))"
    echo "frontend: $PINNED"; echo "runtime: $RKEY"; echo "built: $(date -u +%FT%TZ)"
} > "$W/BUILD_INFO"
rsync -az "$W/BUILD_INFO" "$WINPC:$RDIR.tmp/"
ssh "$WINPC" "set -e; cd $RDIR.tmp; clang -c -O2 -o profile_hooks.o profile_hooks.c
    for m in ${mains[*]}; do
        out=elisa-proof; [ \$m = replay_main ] && out=elisa-proof-replay
        clang -no-pie -Wl,--gc-sections -o \$out \$m.o profile_hooks.o ~/$RBASE/runtime/$RKEY/elisacore_runtime.o -lm
    done
    rm -f main.o replay_main.o
    ./elisa-proof \$PWD/verified.elisa > smoke.txt 2>&1 || true
    grep -q 'verification state: proved' smoke.txt || { cat smoke.txt; echo 'smoke run failed' >&2; exit 1; }
    cd ..; rm -rf $KEY; mv $KEY.tmp $KEY"
echo "built: $KEY" >&2
echo "$RDIR/elisa-proof"
