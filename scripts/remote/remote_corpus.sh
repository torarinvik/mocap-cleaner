#!/usr/bin/env bash
# Prove the mocap-cleaner corpus (src/*/*.elisa proof/*.elisa, 91 files) on winpc.
#
# Syncs this checkout plus the sibling sources its includes reach (../elisa-engine-mocap/src,
# ../elisa-ui/src) into ~/work/mocap-offload/trees/<run>/, starts a detached runner there
# (at most JOBS provers at once, and none started while `free -m` available < MIN_FREE_MB),
# polls until it finishes and prints a TSV:  file  state  proven  unproven  seconds
#
#   remote_corpus.sh                      full corpus, prover from remote_prover.sh (work tree)
#   remote_corpus.sh --quick              ~10 representative files
#   remote_corpus.sh --compare BASE       exit 1 if any file is worse than BASE, which is a
#                                         TSV from an earlier run or a build/proof directory
#   remote_corpus.sh --prover-rev 3244c9d prover built from that elisa-proof-mocap commit
#   remote_corpus.sh --prover PATH        an existing prover on winpc (path relative to ~)
#   remote_corpus.sh --out FILE           also write the TSV to FILE
#   remote_corpus.sh --root DIR           prove another mocap-cleaner checkout (default: this one)
#   remote_corpus.sh FILE...              just these files (relative to the checkout)
#
# Environment: JOBS (default 3, max 3), MIN_FREE_MB (1500), WINPC, REMOTE_BASE, FILE_TIMEOUT (1800s).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
PROJECTS="$(cd "$ROOT/.." && pwd)"
WINPC="${WINPC:-winpc}"
RBASE="${REMOTE_BASE:-work/mocap-offload}"
JOBS="${JOBS:-3}"; (( JOBS > 3 )) && JOBS=3
MIN_FREE_MB="${MIN_FREE_MB:-1500}"
FILE_TIMEOUT="${FILE_TIMEOUT:-1800}"
QUICK=0; COMPARE=""; PROVER=""; OUT=""; prover_args=(); files=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --quick) QUICK=1; shift ;;
        --compare) COMPARE="$2"; shift 2 ;;
        --prover) PROVER="$2"; shift 2 ;;
        --prover-rev) prover_args+=(--rev "$2"); shift 2 ;;
        --prover-src) prover_args+=(--src "$2"); shift 2 ;;
        --out) OUT="$2"; shift 2 ;;
        --root) ROOT="$(cd "$2" && pwd)"; shift 2 ;;
        -h|--help) sed -n 2,20p "$0"; exit 0 ;;
        -*) echo "unknown argument: $1" >&2; exit 2 ;;
        *) files+=("$1"); shift ;;
    esac
done
cd "$ROOT"
if [[ ${#files[@]} -eq 0 ]]; then
    if [[ "$QUICK" == 1 ]]; then
        files=(src/core/retime.elisa proof/retime_laws.elisa src/io/glb_tracks.elisa
               src/physics/rig_physics.elisa src/cli/main.elisa src/core/key_weight.elisa
               src/core/pin.elisa proof/pin_laws.elisa src/ops/retime_apply.elisa
               proof/lock_laws.elisa)
    else
        files=(src/*/*.elisa proof/*.elisa)
    fi
fi
[[ -n "$PROVER" ]] || PROVER="$("$HERE/remote_prover.sh" ${prover_args[@]+"${prover_args[@]}"} | tail -1)"
ssh "$WINPC" "test -x ~/$PROVER" || { echo "no prover at winpc:~/$PROVER" >&2; exit 2; }

RUN="$(date +%Y%m%d-%H%M%S)-$$"
T="$RBASE/trees/$RUN"
ssh "$WINPC" "mkdir -p $T/elisa-engine-mocap $T/elisa-ui"
RS=(rsync -az --delete --exclude build/ --exclude .git --exclude .DS_Store)
"${RS[@]}" --exclude '*.glb' --exclude '*.fbx' "$ROOT/" "$WINPC:$T/mocap-cleaner/"
"${RS[@]}" "$PROJECTS/elisa-engine-mocap/src" "$WINPC:$T/elisa-engine-mocap/"
"${RS[@]}" "$PROJECTS/elisa-ui/src" "$WINPC:$T/elisa-ui/"
printf '%s\n' "${files[@]}" > "${TMPDIR:-/tmp}/corpus-$RUN.list"
rsync -az "${TMPDIR:-/tmp}/corpus-$RUN.list" "$WINPC:$T/files.list"
rm -f "${TMPDIR:-/tmp}/corpus-$RUN.list"

# Runner: largest files first (they take longest), memory-gated, detached from ssh.
ssh "$WINPC" "cat > $T/run.sh" <<'EOF'
#!/usr/bin/env bash
cd "$(dirname "$0")/mocap-cleaner"; P="$1"; JOBS="$2"; MIN="$3"; TO="$4"
mkdir -p ../out
one() {
    local f="$1" o="../out/$(echo "$1" | tr / _).txt" t0=$(date +%s)
    timeout "$TO" nice -n 5 "$P" "$PWD/$f" > "$o.raw" 2>&1; local rc=$?
    local st pr un
    st=$(grep -m1 -o 'verification state: [a-z_]*' "$o.raw" | awk '{print $3}')
    pr=$(grep -m1 -oE '(^| )proven: [0-9]+' "$o.raw" | grep -oE '[0-9]+')
    un=$(grep -m1 -oE 'unproven: [0-9]+' "$o.raw" | grep -oE '[0-9]+')
    [[ -z "$st" ]] && st="error(rc=$rc)"; [[ $rc == 124 ]] && st=timeout
    printf '%s\t%s\t%s\t%s\t%s\n' "$f" "$st" "${pr:--}" "${un:--}" "$(( $(date +%s) - t0 ))" > "$o"
}
t0=$(date +%s)
for f in $(xargs ls -S < ../files.list); do
    while (( $(jobs -rp | wc -l) >= JOBS )) || (( $(free -m | awk '/^Mem:/{print $7}') < MIN )); do sleep 2; done
    one "$f" & sleep 1
done
wait
cat ../out/*.txt | sort > ../result.tsv
echo "wall $(( $(date +%s) - t0 ))s" > ../done
EOF
ssh "$WINPC" "cd $T && nohup bash run.sh ~/$PROVER $JOBS $MIN_FREE_MB $FILE_TIMEOUT > run.log 2>&1 < /dev/null &"
echo "run winpc:~/$T with $PROVER (${#files[@]} files, $JOBS jobs)" >&2

n=${#files[@]}
while ! ssh "$WINPC" "test -f $T/done"; do
    sleep 20
    echo "  $(ssh "$WINPC" "ls $T/out 2>/dev/null | grep -c 'txt\$'; free -m | awk '/^Mem:/{print \"avail \" \$7 \"MB\"}'" | tr '\n' ' ')of $n" >&2
done
res="$(ssh "$WINPC" "cat $T/result.tsv; cat $T/done >&2")"
[[ -n "$OUT" ]] && printf '%s\n' "$res" > "$OUT"
printf 'file\tstate\tproven\tunproven\tseconds\n%s\n' "$res"
ssh "$WINPC" "rm -rf $T/mocap-cleaner $T/elisa-engine-mocap $T/elisa-ui"  # keep out/ and result.tsv

[[ -z "$COMPARE" ]] && exit 0
python3 - "$COMPARE" <<PY
import os, re, sys
RANK = {"proved": 0, "unknown": 1, "unsupported": 2}
def load(src):
    rows = {}
    if os.path.isdir(src):  # build/proof directory from check.sh / prove.py
        for n in os.listdir(src):
            if not n.endswith(".elisa.txt"): continue
            t = open(os.path.join(src, n)).read()
            st = re.search(r"verification state: (\S+)", t); pr = re.search(r"(?<!un)proven: (\d+)", t)
            un = re.search(r"unproven: (\d+)", t)
            f = n[:-4]; d = f.split("_", 1) if f.startswith("proof_") else f.split("_", 2)
            f = "proof/" + d[1] if d[0] == "proof" else "/".join(d)
            rows[f] = (st.group(1) if st else "?", pr.group(1) if pr else "-", un.group(1) if un else "-")
    else:
        for l in open(src):
            p = l.rstrip("\n").split("\t")
            if len(p) >= 4 and p[0] != "file": rows[p[0]] = tuple(p[1:4])
    return rows
base = load(sys.argv[1]); new = {}
for l in """$res""".splitlines():
    p = l.split("\t"); new[p[0]] = tuple(p[1:4])
num = lambda s: int(s) if s.isdigit() else None
bad = 0
for f, (st, pr, un) in sorted(new.items()):
    if f not in base: print(f"new      {f}: {st} {pr}/{un}"); continue
    bs, bp, bu = base[f]; why = []
    if RANK.get(st, 9) > RANK.get(bs, 9): why.append(f"state {bs} -> {st}")
    if num(pr) is not None and num(bp) is not None and num(pr) < num(bp): why.append(f"proven {bp} -> {pr}")
    if num(un) is not None and num(bu) is not None and num(un) > num(bu): why.append(f"unproven {bu} -> {un}")
    if why: bad += 1; print(f"WORSE    {f}: " + ", ".join(why))
    elif (st, pr, un) != (bs, bp, bu): print(f"better   {f}: {bs} {bp}/{bu} -> {st} {pr}/{un}")
print(f"compare: {len(new)} files, {bad} worse than {sys.argv[1]}")
sys.exit(1 if bad else 0)
PY
