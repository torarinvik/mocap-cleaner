#!/usr/bin/env python3
"""Prove the mocap-cleaner corpus across the whole compute fleet, with a content cache.

  1. Builds or reuses the Linux prover (remote_prover.sh, keyed by revision, opt level and
     compiler) and keeps a copy on the Mac in build/fleet/provers/<key>/.
  2. Answers every file whose cache key is unchanged from build/fleet/cache/<key>.tsv. The key
     hashes the prover key, the invocation, and the path and bytes of the file and of everything
     its includes reach, transitively (scripts/prove.py's include rules).
  3. Rsyncs the prover and the .elisa sources (this checkout, ../elisa-engine-mocap/src,
     ../elisa-ui/src) to every host in parallel, under ~/work/mocap-fleet/.
  4. Runs the misses at once, longest first (times recorded in build/fleet/durations.json), on
     per-host slots sized from the cgroup CPU quota and gated on free memory (cgroup-aware).
  5. Prints the same TSV as remote_corpus.sh:  file  state  proven  unproven  seconds

  fleet_corpus.py                       full corpus, prover from the elisa-proof-mocap work tree
  fleet_corpus.py --quick               ~10 representative files
  fleet_corpus.py --compare BASE        exit 1 if any file is worse than BASE (TSV or build/proof dir)
  fleet_corpus.py --prover-rev 19611a2  prover built from that elisa-proof-mocap commit
  fleet_corpus.py --out FILE            also write the TSV to FILE
  fleet_corpus.py --root DIR            prove another mocap-cleaner checkout
  fleet_corpus.py --hosts v80,v32:4     hosts, optionally with a slot count (default vast)
  fleet_corpus.py --no-cache            prove everything (still refreshes the cache)
  fleet_corpus.py --clean               remove ~/work/mocap-fleet on every host and exit
  fleet_corpus.py FILE...               just these files (relative to the checkout)

Environment: FLEET_HOSTS, FILE_TIMEOUT (1800 s), MIN_FREE_GB (1.5), WINPC_MAX_JOBS (3).
"""
import argparse, glob, hashlib, json, os, re, shlex, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from prove import sources  # noqa: E402  (same include rules as the local cache)

PROJECTS = os.path.abspath(os.path.join(HERE, "../../.."))
CFG = os.path.expanduser("~/.ssh/fleet_config")
RBASE = "work/mocap-fleet"
# remote_prover.sh links the prover on this host (its WINPC), through fleet_config.
BUILD_HOST = os.environ.setdefault("WINPC", "vast")
os.environ.setdefault("SSH_CONFIG", CFG)
os.environ.setdefault("REMOTE_BASE", RBASE)
KEY_VERSION = "fleet-corpus-v1"
INVOCATION = "timeout TO nice -n 5 PROVER ABSFILE"
QUICK = ["src/core/retime.elisa", "proof/retime_laws.elisa", "src/io/glb_tracks.elisa",
         "src/physics/rig_physics.elisa", "src/cli/main.elisa", "src/core/key_weight.elisa",
         "src/core/pin.elisa", "proof/pin_laws.elisa", "src/ops/retime_apply.elisa",
         "proof/lock_laws.elisa"]
SIBLINGS = ["elisa-engine-mocap", "elisa-ui"]  # their src/ is reachable through includes
RANK = {"proved": 0, "unknown": 1, "unsupported": 2}


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def ssh(host, cmd, mux=0, **kw):
    """ssh through fleet_config's ControlMaster. sshd allows ~10 sessions per connection
    (MaxSessions), so worker slots share one master per group of 8 (`mux`)."""
    cp = [] if mux == 0 else ["-o", f"ControlPath=~/.ssh/cm/mf{mux}-%r@%h:%p"]
    return subprocess.run(["ssh", "-F", CFG, *cp, host, cmd], **kw)


# --- prover ----------------------------------------------------------------------------
def prover_key(args):
    return subprocess.run([os.path.join(HERE, "remote_prover.sh"), *args, "--key"],
                          check=True, capture_output=True, text=True).stdout.strip()


def local_prover(root, key, args):
    """Mac copy of the Linux prover for `key`; built on winpc by remote_prover.sh if needed."""
    d = os.path.join(root, "build/fleet/provers", key)
    p = os.path.join(d, "elisa-proof")
    if not os.path.exists(p):
        os.makedirs(d, exist_ok=True)
        remote = subprocess.run([os.path.join(HERE, "remote_prover.sh"), *args],
                                check=True, stdout=subprocess.PIPE, text=True).stdout.strip().splitlines()[-1]
        subprocess.run(["rsync", "-az", "-e", f"ssh -F {CFG}", f"{BUILD_HOST}:{remote}", p + ".tmp"], check=True)
        os.replace(p + ".tmp", p)
    return p


# --- cache key -------------------------------------------------------------------------
def remote_rel(path, root):
    """Path as laid out in the remote tree (checkout -> mocap-cleaner/, siblings by name)."""
    path = os.path.abspath(path)
    if path == root or path.startswith(root + os.sep):
        return "mocap-cleaner/" + os.path.relpath(path, root)
    return os.path.relpath(path, PROJECTS)


def cache_key(root, f, pkey):
    h = hashlib.sha256(f"{KEY_VERSION}\0{INVOCATION}\0{pkey}\0".encode())
    files = []
    sources(os.path.join(root, f), files)
    for p in files:
        h.update(remote_rel(p, root).encode() + b"\0")
        try:
            h.update(hashlib.sha256(open(p, "rb").read()).digest())
        except OSError:
            h.update(b"<missing>")
        h.update(b"\0")
    return h.hexdigest()


# --- result parsing (same as remote_corpus.sh's runner) ---------------------------------
def parse(f, text, rc, secs):
    st = re.search(r"verification state: ([a-z_]*)", text)
    pr = re.search(r"(?:^| )proven: ([0-9]+)", text, re.M)
    un = re.search(r"unproven: ([0-9]+)", text)
    st = st.group(1) if st and st.group(1) else f"error(rc={rc})"
    if rc == 124:
        st = "timeout"
    return [f, st, pr.group(1) if pr else "-", un.group(1) if un else "-", str(secs)]


# --- hosts -----------------------------------------------------------------------------
PROBE = ("q=$(cat /sys/fs/cgroup/cpu.max 2>/dev/null); set -- $q; "
         "if [ -n \"$1\" ] && [ \"$1\" != max ]; then echo $(( $1 / $2 )); "
         "elif [ \"$(cat /sys/fs/cgroup/cpu/cpu.cfs_quota_us 2>/dev/null || echo -1)\" -gt 0 ]; then "  # cgroup v1
         "echo $(( $(cat /sys/fs/cgroup/cpu/cpu.cfs_quota_us) / $(cat /sys/fs/cgroup/cpu/cpu.cfs_period_us) )); "
         "else nproc; fi")
MEM = ("m=$(cat /sys/fs/cgroup/memory.max 2>/dev/null); c=$(cat /sys/fs/cgroup/memory.current 2>/dev/null); "
       "a=$(awk '/MemAvailable/{print $2*1024}' /proc/meminfo); "
       "if [ -n \"$m\" ] && [ \"$m\" != max ]; then f=$((m-c)); [ $f -lt $a ] && a=$f; fi; echo $a")


def host_slots(spec):
    h, _, n = spec.partition(":")
    if n:
        return h, int(n)
    try:
        r = ssh(h, PROBE, capture_output=True, text=True, timeout=20)
        n = int(r.stdout.split()[-1])
    except Exception:
        log(f"{h}: unreachable, skipped")
        return h, 0
    if h == "winpc":  # 7.7 GB RAM shared with other agents: ~/.ssh/WINPC_FOR_AGENTS.md
        n = min(n, int(os.environ.get("WINPC_MAX_JOBS", "3")))
    return h, n


def free_gb(host, mux=0):
    try:
        return int(ssh(host, MEM, mux=mux, capture_output=True, text=True, timeout=20).stdout.strip()) / 2**30
    except Exception:
        return 1e9


def sync(host, root, tree, pkey, prover):
    """Prover (once per key) and .elisa sources into ~/work/mocap-fleet on `host`."""
    e = f"ssh -F {CFG}"
    ssh(host, f"mkdir -p {RBASE}/provers/{pkey} {tree}/mocap-cleaner " +
        " ".join(f"{tree}/{s}" for s in SIBLINGS), check=True)
    if ssh(host, f"test -x {RBASE}/provers/{pkey}/elisa-proof").returncode:
        subprocess.run(["rsync", "-az", "-e", e, prover, f"{host}:{RBASE}/provers/{pkey}/elisa-proof.tmp"], check=True)
        ssh(host, f"cd {RBASE}/provers/{pkey} && chmod +x elisa-proof.tmp && mv -f elisa-proof.tmp elisa-proof", check=True)
    only = ["--include=*/", "--include=*.elisa", "--exclude=*", "--prune-empty-dirs"]
    rs = ["rsync", "-az", "--delete", "--exclude=build/", "--exclude=.git", *only, "-e", e]
    subprocess.run(rs + [root + "/", f"{host}:{tree}/mocap-cleaner/"], check=True)
    for s in SIBLINGS:
        subprocess.run(rs + [os.path.join(PROJECTS, s, "src"), f"{host}:{tree}/{s}/"], check=True)


def clean(hosts):
    def one(h):
        r = ssh(h, f"rm -rf {RBASE}", capture_output=True, text=True, timeout=60)
        log(f"{h}: removed ~/{RBASE}" if r.returncode == 0 else f"{h}: {r.stderr.strip()}")
    with ThreadPoolExecutor(len(hosts)) as ex:
        list(ex.map(one, hosts))


# --- compare (same rules as remote_corpus.sh) -------------------------------------------
def load(src):
    rows = {}
    if os.path.isdir(src):
        for n in os.listdir(src):
            if not n.endswith(".elisa.txt"):
                continue
            t = open(os.path.join(src, n)).read()
            st = re.search(r"verification state: (\S+)", t); pr = re.search(r"(?<!un)proven: (\d+)", t)
            un = re.search(r"unproven: (\d+)", t)
            f = n[:-4]; d = f.split("_", 1) if f.startswith("proof_") else f.split("_", 2)
            f = "proof/" + d[1] if d[0] == "proof" else "/".join(d)
            rows[f] = (st.group(1) if st else "?", pr.group(1) if pr else "-", un.group(1) if un else "-")
    else:
        for l in open(src):
            p = l.rstrip("\n").split("\t")
            if len(p) >= 4 and p[0] != "file":
                rows[p[0]] = tuple(p[1:4])
    return rows


def compare(base_src, rows):
    base = load(base_src)
    num = lambda s: int(s) if s.isdigit() else None
    bad = 0
    for f, st, pr, un, _ in rows:
        if f not in base:
            print(f"new      {f}: {st} {pr}/{un}"); continue
        bs, bp, bu = base[f]; why = []
        if RANK.get(st, 9) > RANK.get(bs, 9): why.append(f"state {bs} -> {st}")
        if num(pr) is not None and num(bp) is not None and num(pr) < num(bp): why.append(f"proven {bp} -> {pr}")
        if num(un) is not None and num(bu) is not None and num(un) > num(bu): why.append(f"unproven {bu} -> {un}")
        if why:
            bad += 1; print(f"WORSE    {f}: " + ", ".join(why))
        elif (st, pr, un) != (bs, bp, bu):
            print(f"better   {f}: {bs} {bp}/{bu} -> {st} {pr}/{un}")
    print(f"compare: {len(rows)} files, {bad} worse than {base_src}")
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*")
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--compare")
    ap.add_argument("--prover-rev")
    ap.add_argument("--prover-src")
    ap.add_argument("--out")
    ap.add_argument("--root", default=os.path.abspath(os.path.join(HERE, "../..")))
    ap.add_argument("--hosts", default=os.environ.get("FLEET_HOSTS", "vast"))
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--clean", action="store_true")
    a = ap.parse_args()
    hosts = a.hosts.split(",")
    if a.clean:
        clean([h.partition(":")[0] for h in hosts]); return 0
    t_start = time.time()
    root = os.path.abspath(a.root)
    os.chdir(root)
    files = a.files or (QUICK if a.quick else sorted(glob.glob("src/*/*.elisa") + glob.glob("proof/*.elisa")))
    pargs = (["--rev", a.prover_rev] if a.prover_rev else []) + (["--src", a.prover_src] if a.prover_src else [])
    timeout = int(os.environ.get("FILE_TIMEOUT", "1800"))
    min_free = float(os.environ.get("MIN_FREE_GB", "1.5"))

    pkey = prover_key(pargs)
    fleet = os.path.join(root, "build/fleet")
    cache = os.path.join(fleet, "cache")
    os.makedirs(cache, exist_ok=True)
    dur_path = os.path.join(fleet, "durations.json")
    try:
        durations = json.load(open(dur_path))
    except (OSError, ValueError):
        durations = {}

    rows, todo = {}, []
    for f in files:
        k = cache_key(root, f, pkey)
        c = os.path.join(cache, k + ".tsv")
        if os.path.exists(c) and not a.no_cache:
            rows[f] = open(c).read().rstrip("\n").split("\t")
        else:
            todo.append((f, k))
    log(f"prover {pkey}: {len(files)} files, {len(rows)} cached, {len(todo)} to prove")

    if todo:
        # Longest first; files never timed go first, biggest first (they are the slow ones).
        todo.sort(key=lambda t: (t[0] in durations, -durations.get(t[0], 0), -os.path.getsize(t[0])))
        prover = local_prover(root, pkey, pargs)
        with ThreadPoolExecutor(len(hosts)) as ex:
            slots = dict(ex.map(host_slots, hosts))
        live = [h for h, n in slots.items() if n > 0]
        if not live:
            log("no reachable host"); return 2
        tree = f"{RBASE}/tree/{hashlib.sha256(root.encode()).hexdigest()[:12]}"
        t0 = time.time()
        with ThreadPoolExecutor(len(live)) as ex:
            list(ex.map(lambda h: sync(h, root, tree, pkey, prover), live))
        log(f"synced {', '.join(f'{h}:{slots[h]}' for h in live)} in {time.time() - t0:.1f}s")

        lock = threading.Lock()
        queue = list(todo)
        state = {"done": 0}

        def worker(slot):
            host, mux = slot
            while True:
                with lock:
                    if not queue:
                        return
                    f, k = queue.pop(0)
                for _ in range(120):
                    if free_gb(host, mux) >= min_free:
                        break
                    time.sleep(5)
                cmd = (f"cd {tree}/mocap-cleaner && timeout {timeout} nice -n 5 "
                       f"~/{RBASE}/provers/{pkey}/elisa-proof \"$PWD\"/{shlex.quote(f)}")
                for _ in range(3):  # 255 is ssh failing, not the prover
                    t1 = time.time()
                    p = ssh(host, cmd, mux=mux, capture_output=True, text=True, errors="replace")
                    if p.returncode != 255:
                        break
                    time.sleep(2)
                secs = round(time.time() - t1)
                row = parse(f, p.stdout + p.stderr, p.returncode, secs)
                with lock:
                    rows[f] = row
                    durations[f] = time.time() - t1
                    state["done"] += 1
                    log(f"  [{state['done']}/{len(todo)}] {host} {secs}s {f}: {row[1]} {row[2]}/{row[3]}")
                if not row[1].startswith("error") and row[1] != "timeout":
                    with open(os.path.join(cache, k + ".tsv.tmp"), "w") as fh:
                        fh.write("\t".join(row) + "\n")
                    os.replace(os.path.join(cache, k + ".tsv.tmp"), os.path.join(cache, k + ".tsv"))

        n_slots = min(sum(slots[h] for h in live), len(todo))
        # Never more slots than files; when trimming, the fast boxes keep theirs and winpc goes.
        order = sorted(live, key=lambda h: h == "winpc")
        assigned = []
        for h in order:
            for i in range(slots[h]):
                if len(assigned) < n_slots:
                    assigned.append((h, 1 + i // 8))
        with ThreadPoolExecutor(len(assigned)) as ex:
            list(ex.map(worker, assigned))
        with open(dur_path + ".tmp", "w") as fh:
            json.dump(durations, fh, indent=0, sort_keys=True)
        os.replace(dur_path + ".tmp", dur_path)

    out = [rows[f] for f in sorted(rows)]
    text = "".join("\t".join(r) + "\n" for r in out)
    if a.out:
        open(a.out, "w").write(text)
    sys.stdout.write("file\tstate\tproven\tunproven\tseconds\n" + text)
    sys.stdout.flush()
    log(f"wall {time.time() - t_start:.1f}s ({len(rows) - len(todo)} cached, {len(todo)} proved)")
    return compare(a.compare, out) if a.compare else 0


if __name__ == "__main__":
    sys.exit(main())
