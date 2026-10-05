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
check_jobs=${CHECK_JOBS:-4}
case $check_jobs in
    ''|*[!0-9]*) echo "CHECK_JOBS must be a positive integer" >&2; exit 2 ;;
    0) echo "CHECK_JOBS must be a positive integer" >&2; exit 2 ;;
esac
build_test() {
    t=$1
    name=$(basename "$t" .elisa)
    if ELISA_ALLOW_STALE_STAGE1=1 "$ELISAC" -emit exe -o "build/test/$name" "$t" >"build/test/$name.log" 2>&1; then
        echo ok >"build/test/$name.status"
    else
        echo failed >"build/test/$name.status"
    fi
}
# Derived icon geometry for test/studio_icons.elisa (also made by build_studio.sh).
python3 tools/svg_icons.py build/generated/studio_icon_paths.elisa >/dev/null || status=1
# Compile in bounded parallel batches; test executables still run in file order
# because several share generated fixtures under build/.
rm -f build/test/*.status
active=0
for t in test/*.elisa; do
    build_test "$t" &
    active=$((active + 1))
    if [ "$active" -ge "$check_jobs" ]; then
        wait || true
        active=0
    fi
done
[ "$active" -eq 0 ] || wait || true
for t in test/*.elisa; do
    name=$(basename "$t" .elisa)
    if [ "$(cat "build/test/$name.status" 2>/dev/null)" = ok ]; then
        "build/test/$name"; rc=$?
        echo "test  $name: rc=$rc"; [ $rc -eq 0 ] || status=1
    else
        echo "test  $name: BUILD FAILED (build/test/$name.log)"; status=1
    fi
done
# CLI built through elisa_build_run.py (scripts/build.sh), in the plan's form, and a folder batch with its HTML report.
boxer=../elisa-boxing-game/build/dual-stance/black/black-boxer.glb
if ELISAC="$ELISAC" sh scripts/build.sh >build/test/cli.log 2>&1; then
    if [ -f "$boxer" ]; then
        rm -rf build/cli-test && mkdir -p build/cli-test/in build/cli-test/out
        cp "$boxer" build/cli-test/in/
        build/mocap-cleaner clean "$boxer" --preset boxing -o build/cli-test/out.glb --report build/cli-test/r.json >/dev/null; rc=$?
        grep -q '"ok": true' build/cli-test/r.json 2>/dev/null || rc=9
        echo "cli   clean -o --report: rc=$rc"; [ $rc -eq 0 ] || status=1
        build/mocap-cleaner batch build/cli-test/out build/cli-test/in >/dev/null; rc=$?
        grep -q "black-boxer.glb" build/cli-test/out/report.html 2>/dev/null || rc=9
        echo "cli   batch folder: rc=$rc"; [ $rc -eq 0 ] || status=1
        # --op hands finds no planted hand on the boxer: output is byte-identical.
        build/mocap-cleaner clean "$boxer" --preset boxing --op hands -o build/cli-test/hands.glb --report build/cli-test/h.json >/dev/null; rc=$?
        cmp -s build/cli-test/out.glb build/cli-test/hands.glb || rc=9
        build/mocap-cleaner diff build/cli-test/r.json build/cli-test/h.json --html build/cli-test/diff.html >/dev/null || rc=8
        echo "cli   hands + diff: rc=$rc"; [ $rc -eq 0 ] || status=1
        build/mocap-cleaner clean "$boxer" --preset raw --anim jab --retime 10:40:0.5 --save-ops build/cli-test/rt.ops -o build/cli-test/rt.glb >build/cli-test/rt.txt; rc=$?
        grep -q "^9 1 10 40 " build/cli-test/rt.ops 2>/dev/null || rc=9
        grep -q "retime frames after: 123" build/cli-test/rt.txt || rc=8
        echo "cli   clean --retime: rc=$rc"; [ $rc -eq 0 ] || status=1
    fi
else
    echo "cli   BUILD FAILED (build/test/cli.log)"; status=1
fi
# Prove files incrementally (cached by file + includes + the prover's semantic
# revision, see scripts/prove.py) and longest first, PROOF_JOBS at once
# (default: core count); report in order. PROOF_RECHECK=N re-proves N random
# cache hits and fails on any mismatch.
mkdir -p build/proof
rm -f build/proof/*.txt build/proof/*.cached
python3 scripts/prove.py ${PROOF_RECHECK:+--recheck-sample "$PROOF_RECHECK"} "$PROVER" $(ls src/*/*.elisa proof/*.elisa 2>/dev/null) || status=1
for f in src/*/*.elisa proof/*.elisa; do
    [ -f "$f" ] || continue
    base="build/proof/$(echo "$f" | tr / _)"
    line=$(cat "$base.txt" 2>/dev/null)
    tag=""; [ -f "$base.cached" ] && tag=" (cached)"
    echo "proof $f: $line$tag"
done
python3 scripts/check_proof_baseline.py src/*/*.elisa proof/*.elisa || status=1
exit $status
