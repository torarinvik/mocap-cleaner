#!/bin/sh
# Build and run every test, then run elisa-proof over sources and proofs.
set -u
cd "$(dirname "$0")/.."
python3 scripts/check_file_lengths.py || exit 1
ELISAC="${ELISAC:-../Elisa-compiler/scripts/elisac_stage1.sh}"
PROVER="${ELISA_PROOF:-../elisa-proof-mocap/build/elisa-proof}"
mkdir -p build/test
# Generated round-trip destinations must be absent for exclusive writers.
# Reset only these named test artifacts; the fixture inputs are rebuilt by
# their existing tests. This also prevents stale bytes from satisfying reads.
python3 - <<'PY'
from pathlib import Path
for name in ("rig_tools.ops", "diff-a.json", "diff-same.json", "diff-worse.json",
             "diff-lost.json", "diff-gone.json", "diff.html"):
    (Path("build/test") / name).unlink(missing_ok=True)
PY
# Folder fixture for test/folder.elisa (empty files; only names matter).
rm -rf build/folder-test && mkdir -p build/folder-test/sub.glb
touch build/folder-test/a.glb build/folder-test/b.glb build/folder-test/C.GLB build/folder-test/.hidden.glb build/folder-test/c.txt
status=0
if [ "$(uname -s)" = Darwin ]; then
    bash scripts/check_storage_io.sh || status=1
fi
# CHECK_JOBS bounds compiler and independent test concurrency.
check_jobs=${CHECK_JOBS:-4}
case $check_jobs in
    ''|*[!0-9]*) echo "CHECK_JOBS must be a positive integer" >&2; exit 2 ;;
    0) echo "CHECK_JOBS must be a positive integer" >&2; exit 2 ;;
esac
build_test() {
    t=$1
    name=$(basename "$t" .elisa)
    if [ -x "build/test/$name" ] && [ "$(cat "build/test/$name.build-key" 2>/dev/null)" = "$test_build_key" ]; then
        echo cached >"build/test/$name.status"
    elif ELISA_ALLOW_STALE_STAGE1=1 "$ELISAC" -emit exe -o "build/test/$name" "$t" >"build/test/$name.log" 2>&1; then
        echo "$test_build_key" >"build/test/$name.build-key.tmp"
        mv "build/test/$name.build-key.tmp" "build/test/$name.build-key"
        echo ok >"build/test/$name.status"
    else
        echo failed >"build/test/$name.status"
    fi
}
# Derived icon geometry for test/studio_icons.elisa (also made by build_studio.sh).
python3 tools/svg_icons.py build/generated/studio_icon_paths.elisa >/dev/null || status=1
test_build_key=$(python3 scripts/test_build_key.py "$ELISAC") || exit 2
# Compile in bounded parallel batches.
rm -f build/test/*.status
active=0
pids=
for t in test/*.elisa; do
    build_test "$t" &
    pids="$pids $!"
    active=$((active + 1))
    if [ "$active" -ge "$check_jobs" ]; then
        for pid in $pids; do wait "$pid" || true; done
        pids=
        active=0
    fi
done
for pid in $pids; do wait "$pid" || true; done
cached_tests=0
built_tests=0
for t in test/*.elisa; do
    name=$(basename "$t" .elisa)
    if [ "$(cat "build/test/$name.status")" = cached ]; then
        cached_tests=$((cached_tests + 1))
    else
        built_tests=$((built_tests + 1))
    fi
done
echo "test builds: $cached_tests cached, $built_tests rebuilt"
# The CLI build is independent of the test executables and overlaps their run.
ELISAC="$ELISAC" sh scripts/build.sh >build/test/cli.log 2>&1 &
cli_build_pid=$!
python3 scripts/run_tests.py "$check_jobs" test/*.elisa || status=1
# CLI built through elisa_build_run.py (scripts/build.sh), in the plan's form, and a folder batch with its HTML report.
boxer=../elisa-boxing-game/build/dual-stance/black/black-boxer.glb
if wait "$cli_build_pid"; then
    if [ -f "$boxer" ]; then
        rm -rf build/cli-test && mkdir -p build/cli-test/in build/cli-test/out
        cp "$boxer" build/cli-test/in/
        cli_clean() {
            build/mocap-cleaner clean "$boxer" --preset boxing -o build/cli-test/out.glb --report build/cli-test/r.json >/dev/null
            rc=$?
            grep -q '"ok": true' build/cli-test/r.json 2>/dev/null || rc=9
            echo "$rc" >build/cli-test/clean.status
        }
        cli_batch() {
            build/mocap-cleaner batch build/cli-test/out build/cli-test/in >/dev/null
            rc=$?
            grep -q "black-boxer.glb" build/cli-test/out/report.html 2>/dev/null || rc=9
            echo "$rc" >build/cli-test/batch.status
        }
        cli_retime() {
            build/mocap-cleaner clean "$boxer" --preset raw --anim jab --retime 10:40:0.5 --save-ops build/cli-test/rt.ops -o build/cli-test/rt.glb >build/cli-test/rt.txt
            rc=$?
            grep -q "^9 1 10 40 " build/cli-test/rt.ops 2>/dev/null || rc=9
            grep -q "retime frames after: 123" build/cli-test/rt.txt || rc=8
            echo "$rc" >build/cli-test/retime.status
        }
        cli_hands() {
            # --op hands finds no planted hand on the boxer: output is byte-identical.
            build/mocap-cleaner clean "$boxer" --preset boxing --op hands -o build/cli-test/hands.glb --report build/cli-test/h.json >/dev/null
            rc=$?
            echo "$rc" >build/cli-test/hands-clean.status
        }
        cli_clean & clean_pid=$!
        cli_batch & batch_pid=$!
        cli_retime & retime_pid=$!
        cli_hands & hands_pid=$!
        wait "$clean_pid" || true
        wait "$batch_pid" || true
        wait "$retime_pid" || true
        wait "$hands_pid" || true
        rc=$(cat build/cli-test/hands-clean.status)
        if [ "$rc" -eq 0 ]; then
            cmp -s build/cli-test/out.glb build/cli-test/hands.glb || rc=9
            build/mocap-cleaner diff build/cli-test/r.json build/cli-test/h.json --html build/cli-test/diff.html >/dev/null || rc=8
        fi
        echo "$rc" >build/cli-test/hands.status
        rc=$(cat build/cli-test/clean.status); echo "cli   clean -o --report: rc=$rc"; [ "$rc" -eq 0 ] || status=1
        rc=$(cat build/cli-test/batch.status); echo "cli   batch folder: rc=$rc"; [ "$rc" -eq 0 ] || status=1
        rc=$(cat build/cli-test/hands.status); echo "cli   hands + diff: rc=$rc"; [ "$rc" -eq 0 ] || status=1
        rc=$(cat build/cli-test/retime.status); echo "cli   clean --retime: rc=$rc"; [ "$rc" -eq 0 ] || status=1
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
# The pure preferences codec lives beside its IO adapter, but participates
# in the same reviewed proof corpus as the Studio kernels.
set -- src/*/*.elisa src/studio/io/*_policy.elisa src/studio/io/storage_preferences_codec.elisa proof/*.elisa
python3 scripts/prove.py ${PROOF_RECHECK:+--recheck-sample "$PROOF_RECHECK"} "$PROVER" "$@" || status=1
for f in "$@"; do
    [ -f "$f" ] || continue
    base="build/proof/$(echo "$f" | tr / _)"
    line=$(cat "$base.txt" 2>/dev/null)
    tag=""; [ -f "$base.cached" ] && tag=" (cached)"
    echo "proof $f: $line$tag"
done
python3 scripts/check_proof_baseline.py "$@" || status=1
exit $status
