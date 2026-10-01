#!/bin/sh
# Build and run every test, then run elisa-proof over sources and proofs.
set -u
cd "$(dirname "$0")/.."
ELISAC="${ELISAC:-../Elisa-compiler/scripts/elisac_stage1.sh}"
PROVER="${ELISA_PROOF:-../elisa-proof-mocap/build/elisa-proof}"
mkdir -p build/test
# Folder fixture for test/folder.elisa (empty files; only names matter).
rm -rf build/folder-test && mkdir -p build/folder-test/sub.glb
touch build/folder-test/a.glb build/folder-test/b.glb build/folder-test/C.GLB build/folder-test/.hidden.glb build/folder-test/c.txt
status=0
for t in test/*.elisa; do
    name=$(basename "$t" .elisa)
    if ELISA_ALLOW_STALE_STAGE1=1 "$ELISAC" -emit exe -o "build/test/$name" "$t" >"build/test/$name.log" 2>&1; then
        "build/test/$name"; rc=$?
        echo "test  $name: rc=$rc"; [ $rc -eq 0 ] || status=1
    else
        echo "test  $name: BUILD FAILED (build/test/$name.log)"; status=1
    fi
done
# CLI in the plan's form, and a folder batch with its HTML report.
boxer=../elisa-boxing-game/build/dual-stance/black/black-boxer.glb
if ELISA_ALLOW_STALE_STAGE1=1 "$ELISAC" -emit exe -o build/mocap-cleaner src/cli/main.elisa >build/test/cli.log 2>&1; then
    if [ -f "$boxer" ]; then
        rm -rf build/cli-test && mkdir -p build/cli-test/in build/cli-test/out
        cp "$boxer" build/cli-test/in/
        build/mocap-cleaner clean "$boxer" --preset boxing -o build/cli-test/out.glb --report build/cli-test/r.json >/dev/null; rc=$?
        grep -q '"ok": true' build/cli-test/r.json 2>/dev/null || rc=9
        echo "cli   clean -o --report: rc=$rc"; [ $rc -eq 0 ] || status=1
        build/mocap-cleaner batch build/cli-test/out build/cli-test/in >/dev/null; rc=$?
        grep -q "black-boxer.glb" build/cli-test/out/report.html 2>/dev/null || rc=9
        echo "cli   batch folder: rc=$rc"; [ $rc -eq 0 ] || status=1
    fi
else
    echo "cli   BUILD FAILED (build/test/cli.log)"; status=1
fi
for f in src/*/*.elisa proof/*.elisa; do
    [ -f "$f" ] || continue
    line=$("$PROVER" "$PWD/$f" | grep -E "verification state|proven:|failed:" | tr -s ' ' | tr '\n' ' ')
    echo "proof $f: $line"
    echo "$line" | grep -q "state: proved" || status=1
done
exit $status
