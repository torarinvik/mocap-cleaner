#!/bin/sh
# Build and run every test, then run elisa-proof over sources and proofs.
set -u
cd "$(dirname "$0")/.."
ELISAC="${ELISAC:-../Elisa-compiler/scripts/elisac_stage1.sh}"
PROVER="${ELISA_PROOF:-../elisa-proof-mocap/build/elisa-proof}"
mkdir -p build/test
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
for f in src/*/*.elisa proof/*.elisa; do
    [ -f "$f" ] || continue
    line=$("$PROVER" "$PWD/$f" | grep -E "verification state|proven:|failed:" | tr -s ' ' | tr '\n' ' ')
    echo "proof $f: $line"
    echo "$line" | grep -q "state: proved" || status=1
done
exit $status
