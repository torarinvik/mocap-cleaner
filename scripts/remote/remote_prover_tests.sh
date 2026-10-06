#!/usr/bin/env bash
# Run elisa-proof-mocap's scripts/test.sh on winpc against a Linux prover from remote_prover.sh.
#
# test.sh builds the prover (scripts/build.sh) and compiles ~45 example programs with the
# Elisa compiler. winpc has no working compiler, so in the synced copy:
#   - scripts/build.sh is replaced by a stub that installs the prebuilt Linux prover and
#     replay checker plus build/profile_hooks.o and build/snapshot/;
#   - ELISA_COMPILER_BIN is a stub `elisac-stage1` that queues each compile request and waits;
#     this script serves the queue from the Mac (cross-compiling with -target-triple
#     x86_64-unknown-linux-gnu) and returns the object, output and exit status;
#   - clang/cc on PATH are wrappers that turn the Mac-only -Wl,-dead_strip into
#     --gc-sections and add -no-pie -lm.
# Nothing in elisa-proof-mocap is edited; the copy lives in ~/work/mocap-offload/ptest/<run>.
#
#   remote_prover_tests.sh                    working tree of ../elisa-proof-mocap
#   remote_prover_tests.sh --rev 0c1a6df      that commit
#   remote_prover_tests.sh --src <worktree>   another checkout
# Output: test.sh's output; exit status is test.sh's. Environment as remote_prover.sh.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECTS="$(cd "$HERE/../../.." && pwd)"
SRC="$PROJECTS/elisa-proof-mocap"; REV=""; pargs=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --src) SRC="$(cd "$2" && pwd)"; pargs+=(--src "$SRC"); shift 2 ;;
        --rev) REV="$2"; pargs+=(--rev "$2"); shift 2 ;;
        -h|--help) sed -n 2,19p "$0"; exit 0 ;;
        *) echo "unknown argument: $1" >&2; exit 2 ;;
    esac
done
CROOT="${ELISA_STAGE1_ROOT:-$PROJECTS/elisa-compiler-worktrees/local-shadow}"
CSRC="${ELISA_COMPILER_SRC:-$PROJECTS/Elisa-compiler}"
WINPC="${WINPC:-winpc}"
RBASE="${REMOTE_BASE:-work/mocap-offload}"
LOCAL="${MOCAP_OFFLOAD_CACHE:-$HOME/.cache/mocap-offload}"

PROVER="$("$HERE/remote_prover.sh" --replay ${pargs[@]+"${pargs[@]}"} | tail -1)"
PDIR="${PROVER%/elisa-proof}"
RTO="$("$HERE/remote_prover.sh" --runtime | tail -1)"
RHOME="$(ssh "$WINPC" 'echo $HOME')"

RUN="$(date +%Y%m%d-%H%M%S)-$$"
T="$RBASE/ptest/$RUN"; R="$RHOME/$T"
L="$LOCAL/ptest/$RUN"; mkdir -p "$L/tree/elisa-proof" "$L/tree/Elisa-compiler" "$L/q"
if [[ -n "$REV" ]]; then
    git -C "$SRC" archive --format=tar "$REV" | tar -x -C "$L/tree/elisa-proof"
    pinned="$(cat "$L/tree/elisa-proof/ELISA_COMPILER_REV")"
else
    rsync -a --exclude build/ --exclude .git --exclude .DS_Store "$SRC/" "$L/tree/elisa-proof/"
    pinned="$(cat "$SRC/ELISA_COMPILER_REV")"
fi
git -C "$CSRC" archive --format=tar "$(echo "$pinned" | tr -d '[:space:]')" src elisacore_std test/parity/profile_hooks.c \
    | tar -x -C "$L/tree/Elisa-compiler"
echo "$PROVER" > "$L/prover"
ssh "$WINPC" "mkdir -p $T"
rsync -az "$L/tree/" "$WINPC:$T/"

# Stubs on winpc.
ssh "$WINPC" "bash -s" <<EOF
set -e
cd $R; mkdir -p shim fakec/scripts fakec/build/runtime q
cp ~/$RTO fakec/build/runtime/elisacore_runtime.o
cat > elisa-proof/scripts/build.sh <<'B'
#!/usr/bin/env bash
# remote_prover_tests.sh stub: install the prebuilt Linux products instead of compiling.
set -e
ROOT="\$(cd "\$(dirname "\$0")/.." && pwd)"; mkdir -p "\$ROOT/build/snapshot"
cp -f ~/$PDIR/elisa-proof ~/$PDIR/elisa-proof-replay ~/$PDIR/profile_hooks.o "\$ROOT/build/"
[ -n "\${ELISA_PROOF_OUTPUT:-}" ] && cp -f ~/$PDIR/\$(basename "\$ELISA_PROOF_OUTPUT") "\$ELISA_PROOF_OUTPUT"
rm -rf "\$ROOT/build/snapshot/elisa-proof"; mkdir -p "\$ROOT/build/snapshot/elisa-proof"
cp -R "\$ROOT/src" "\$ROOT/examples" "\$ROOT/build/snapshot/elisa-proof/"
rm -rf "\$ROOT/build/snapshot/Elisa-compiler"; cp -R "\$ROOT/../Elisa-compiler" "\$ROOT/build/snapshot/"
mkdir -p "\$ROOT/build/runtime"; cp -f $R/fakec/build/runtime/elisacore_runtime.o "\$ROOT/build/runtime/"
B
for c in clang cc; do cat > shim/\$c <<'S'
#!/usr/bin/env bash
a=(); link=1
for x in "\$@"; do case "\$x" in -Wl,-dead_strip) a+=(-Wl,--gc-sections) ;; -c|-S|-E|-r) link=0; a+=("\$x") ;; *) a+=("\$x") ;; esac; done
if [ \$link = 1 ]; then exec /usr/bin/clang-19 -no-pie "\${a[@]}" -lm; else exec /usr/bin/clang-19 "\${a[@]}"; fi
S
chmod +x shim/\$c; done
cat > fakec/elisac-stage1 <<'F'
#!/usr/bin/env bash
# driver: $R/fakec/scripts/elisac_stage1.sh
# Queue the compile for the Mac (remote_prover_tests.sh) and wait for its answer.
Q=$R/q; id="\$(date +%s%N)-\$\$"; mkdir -p "\$Q/\$id.files"
out=""; prev=""; args=()
for x in "\$@"; do
    [ "\$prev" = -o ] && out="\$x"
    if [ -f "\$x" ] && [ "\$prev" != -o ]; then mkdir -p "\$Q/\$id.files\$(dirname "\$x")"; cp "\$x" "\$Q/\$id.files\$x"; fi
    args+=("\$x"); prev="\$x"
done
printf '%s\0' "\${args[@]}" > "\$Q/\$id.args.tmp"; mv "\$Q/\$id.args.tmp" "\$Q/\$id.args"
while [ ! -f "\$Q/\$id.done" ]; do sleep 0.5; done
[ -n "\$out" ] && [ -f "\$Q/\$id.o" ] && cp "\$Q/\$id.o" "\$out"
cat "\$Q/\$id.out"; cat "\$Q/\$id.err" >&2
exit "\$(cat "\$Q/\$id.done")"
F
chmod +x fakec/elisac-stage1
cp fakec/elisac-stage1 fakec/scripts/elisac_stage1.sh
cd elisa-proof
PATH=$R/shim:\$PATH ELISA_COMPILER_BIN=$R/fakec/elisac-stage1 CLANG=$R/shim/clang \
    nohup bash -c 'bash scripts/test.sh; echo \$? > ../test.rc' > ../test.log 2>&1 < /dev/null &
EOF
echo "running test.sh in winpc:$R with $PROVER" >&2

# Compile server: answer queued requests until test.sh finishes.
export ELISA_HOST_LINUX=1 ELISA_HOST_X86_64=1
served=0
while :; do
    reqs="$(ssh "$WINPC" "cd $R/q && ls *.args 2>/dev/null | sed 's/\.args\$//' | while read i; do [ -f \$i.done ] || echo \$i; done")"
    for id in $reqs; do
        rsync -az "$WINPC:$R/q/$id.args" "$WINPC:$R/q/$id.files" "$L/q/" 2>/dev/null || true
        args=(); prev=""; have_o=0
        while IFS= read -r -d '' x; do
            if [[ "$prev" == -o ]]; then x="$L/q/$id.o"; have_o=1
            elif [[ "$x" == "$R/elisa-proof/build/snapshot/"* ]]; then x="$L/tree/${x#"$R/elisa-proof/build/snapshot/"}"
            elif [[ "$x" == "$R/"* ]]; then x="$L/tree/${x#"$R/"}"
            elif [[ -f "$L/q/$id.files$x" ]]; then x="$L/q/$id.files$x"; fi
            args+=("$x"); prev="$x"
        done < "$L/q/$id.args"
        rc=0
        nice -n 5 "$CROOT/scripts/elisac_stage1.sh" -target-triple x86_64-unknown-linux-gnu "${args[@]}" \
            > "$L/q/$id.out" 2> "$L/q/$id.err" || rc=$?
        for f in out err; do sed -i '' "s|$L/tree/|$R/|g; s|$L/q/$id.files||g" "$L/q/$id.$f"; done
        echo "$rc" > "$L/q/$id.done"
        up=("$L/q/$id.out" "$L/q/$id.err"); [[ -f "$L/q/$id.o" ]] && up+=("$L/q/$id.o")
        rsync -az "${up[@]}" "$WINPC:$R/q/" && rsync -az "$L/q/$id.done" "$WINPC:$R/q/"
        served=$((served + 1))
    done
    if ssh "$WINPC" "test -f $R/test.rc"; then break; fi
    [[ -z "$reqs" ]] && sleep 3
done
ssh "$WINPC" "cat $R/test.log"
rc="$(ssh "$WINPC" "cat $R/test.rc")"
echo "remote_prover_tests: test.sh exit $rc ($served compiles served; log winpc:$R/test.log)" >&2
exit "$rc"
