#!/usr/bin/env bash
# Run scripts/check.sh's unit tests (test/*.elisa) on winpc.
#
# Each test is cross-compiled here to a Linux object (cached by content of the test and
# everything under src/ plus the sibling sources, so unchanged tests are not recompiled),
# then linked against the Linux runtime and run on winpc from a synced copy of the
# checkout, as check.sh runs them (cwd = checkout root, rc 0 = pass).
#
# The CLI section of check.sh (scripts/build.sh through elisa_build_run.py) is not run:
# it links native bridges that are only built for the Mac. The proof section is
# remote_corpus.sh. test/folder.elisa fails on Linux (rc 5) because src/io/folder.elisa
# decodes the macOS dirent layout; it is reported but not counted as a failure.
#
#   remote_check.sh                 all tests
#   remote_check.sh retime hands    just these tests
#
# Environment: ELISA_STAGE1_ROOT, WINPC, REMOTE_BASE, MOCAP_OFFLOAD_CACHE (see remote_prover.sh).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
PROJECTS="$(cd "$ROOT/.." && pwd)"
CROOT="${ELISA_STAGE1_ROOT:-$PROJECTS/elisa-compiler-worktrees/local-shadow}"
WINPC="${WINPC:-winpc}"
RBASE="${REMOTE_BASE:-work/mocap-offload}"
LOCAL="${MOCAP_OFFLOAD_CACHE:-$HOME/.cache/mocap-offload}"
cd "$ROOT"
names=("$@")
[[ ${#names[@]} -gt 0 ]] || names=($(cd test && ls *.elisa | sed 's/\.elisa$//'))

RTO="$("$HERE/remote_prover.sh" --runtime | tail -1)"

# Same derived input check.sh makes before the tests.
python3 tools/svg_icons.py build/generated/studio_icon_paths.elisa >/dev/null

# Cache key: product + all sources tests can include.
srckey="$( { shasum -a 256 "$CROOT/bin/elisac-stage1" | cut -c1-64
            find src build/generated "$PROJECTS/elisa-engine-mocap/src" "$PROJECTS/elisa-ui/src" \
                -name '*.elisa' -type f -print0 | LC_ALL=C sort -z | xargs -0 shasum -a 256; } \
          | shasum -a 256 | cut -c1-16)"
OBJ="$LOCAL/tests"; mkdir -p "$OBJ"
export ELISA_HOST_LINUX=1 ELISA_HOST_X86_64=1
built=(); status=0
for n in "${names[@]}"; do
    k="$n-$(cat "test/$n.elisa" | shasum -a 256 | cut -c1-10)-$srckey"
    if [[ ! -s "$OBJ/$k.o" ]]; then
        if nice -n 5 "$CROOT/scripts/elisac_stage1.sh" -emit obj -target-triple x86_64-unknown-linux-gnu \
                -o "$OBJ/$k.o.tmp" "test/$n.elisa" > "$OBJ/$n.log" 2>&1; then
            mv -f "$OBJ/$k.o.tmp" "$OBJ/$k.o"
        else
            echo "test  $n: BUILD FAILED ($OBJ/$n.log)"; status=1; continue
        fi
    fi
    mkdir -p "$OBJ/up"; ln -f "$OBJ/$k.o" "$OBJ/up/$n.o"; built+=("$n")
done
[[ ${#built[@]} -gt 0 ]] || exit 1

T="$RBASE/check"
ssh "$WINPC" "mkdir -p $T/obj $T/elisa-boxing-game/build/dual-stance/black"
RS=(rsync -az --delete --exclude .git --exclude .DS_Store)
"${RS[@]}" --exclude build/ "$ROOT/" "$WINPC:$T/mocap-cleaner/"
"${RS[@]}" "$PROJECTS/elisa-engine-mocap/src" "$WINPC:$T/elisa-engine-mocap/"
"${RS[@]}" "$PROJECTS/elisa-ui/src" "$WINPC:$T/elisa-ui/"
boxer="$PROJECTS/elisa-boxing-game/build/dual-stance/black/black-boxer.glb"
[[ -f "$boxer" ]] && rsync -az "$boxer" "$WINPC:$T/elisa-boxing-game/build/dual-stance/black/"
rsync -az --delete "$OBJ/up/" "$WINPC:$T/obj/"
rm -rf "$OBJ/up"

ssh "$WINPC" "bash -s" <<EOF | tee "$LOCAL/check-last.txt" || status=1
set -u
cd ~/$T/mocap-cleaner
mkdir -p build/test build/generated
rm -rf build/folder-test && mkdir -p build/folder-test/sub.glb
touch build/folder-test/a.glb build/folder-test/b.glb build/folder-test/C.GLB build/folder-test/.hidden.glb build/folder-test/c.txt
st=0
for n in ${built[*]}; do
    if clang -no-pie -Wl,--gc-sections -o build/test/\$n ../obj/\$n.o ~/$RTO -lm > build/test/\$n.link 2>&1; then
        timeout 1800 nice -n 5 build/test/\$n; rc=\$?
        if [ \$n = folder ] && [ \$rc -ne 0 ]; then
            echo "test  \$n: rc=\$rc (expected on Linux: src/io/folder.elisa reads the macOS dirent layout)"; continue
        fi
        echo "test  \$n: rc=\$rc"; [ \$rc -eq 0 ] || st=1
    else
        echo "test  \$n: LINK FAILED"; head -5 build/test/\$n.link; st=1
    fi
done
exit \$st
EOF
exit $status
