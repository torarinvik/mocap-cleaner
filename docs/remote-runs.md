# Remote runs on winpc

Heavy verification goes to `ssh winpc` (WSL2 Ubuntu, 12 cores, ~7.8 GB RAM) by default.
Rules: ~/.ssh/WINPC_FOR_AGENTS.md. Everything lives under `~/work/mocap-offload/` there.

Mac binaries do not run on winpc and winpc cannot build Elisa itself, so programs are
cross-compiled on the Mac (`-target-triple x86_64-unknown-linux-gnu`, with
`ELISA_HOST_LINUX=1 ELISA_HOST_X86_64=1`) and only linked and run on winpc
(`clang -no-pie -Wl,--gc-sections ... -lm`).

| Script | What it does |
|---|---|
| `scripts/remote/remote_prover.sh [--rev R] [--replay]` | Build/cached Linux elisa-proof from ../elisa-proof-mocap; prints its winpc path |
| `scripts/remote/remote_prover.sh --runtime` | Ensure the Linux runtime object; print its path |
| `scripts/remote/fleet_corpus.sh [--quick] [--compare BASE] [--out F]` | Prove the corpus on the fleet (default host `vast`) with a cross-run content cache; same TSV and --compare as remote_corpus.sh. **Use this one.** |
| `scripts/remote/remote_corpus.sh [--quick] [--compare BASE] [--out F]` | Prove the 91-file corpus (or 10 with --quick); TSV out; --compare exits 1 if any file is worse |
| `scripts/remote/remote_check.sh [test...]` | Unit tests (test/*.elisa) on winpc; CLI section skipped (Mac-only bridges) |
| `scripts/remote/remote_prover_tests.sh [--rev R]` | elisa-proof-mocap's scripts/test.sh on winpc; compiles are served from the Mac |

Concurrency: corpus runs use at most 3 provers (JOBS) and do not start one while
`free -m` available is below MIN_FREE_MB (1500). Never pass `--seed`.

Examples:

    scripts/remote/remote_corpus.sh --quick --compare build/proof
    scripts/remote/remote_corpus.sh --prover-rev 3244c9d --compare build/proof --out /tmp/full.tsv
    scripts/remote/remote_check.sh retime folder

Known differences: `test/folder.elisa` fails on Linux (rc 5) because src/io/folder.elisa
decodes the macOS dirent layout; remote_check.sh reports it without failing.
The Elisa compiler's own test suite is not run on winpc (needs go, llvm-21 and root).

Validation (2026-10-02, prover 3244c9d at O2, 3 jobs): the full 91-file corpus took 261 s wall
on winpc (70 proved, 2 unknown, 19 unsupported) and matched the Mac build/proof baseline
file-for-file, with the same states and the same proven/unproven counts. The quick set takes about 76 s.

## Fleet corpus runs (`fleet_corpus.sh`)

`scripts/remote/fleet_corpus.sh` pins the prover base (elisa-proof `agent/prover-bb40-views`,
frontend 2678ff10, cross-compiled with `elisa-compiler-worktrees/studio-globals`, linked on
`vast`) and runs `fleet_corpus.py`, which takes the same arguments as `remote_corpus.sh` (`--quick`,
`--compare BASE`, `--out F`, `--prover-rev R`, `--prover-src DIR`, `--root DIR`, `FILE...`)
plus `--hosts v80,v32:4,...`, `--no-cache` and `--clean`. Hosts default to `vast` (FLEET_HOSTS). It talks to the hosts through
`~/.ssh/fleet_config` and works only in `~/work/mocap-fleet/` on each box.

1. Prover: the key is `remote_prover.sh --key` (source revision or dirty-tree hash, opt level,
   stage1 product and frontend). A missing key is built by `remote_prover.sh` (WINPC=vast, SSH_CONFIG=fleet_config) and
   copied to `build/fleet/provers/<key>/elisa-proof` on the Mac, then to
   `~/work/mocap-fleet/provers/<key>/` on each host that lacks it.
2. Cache: each file's TSV row is stored in `build/fleet/cache/<key>.tsv`. The key hashes a
   version tag, the invocation, the prover key, and the path (as laid out remotely) and bytes
   of the file and of every file its includes reach, transitively, with the include rules of
   `scripts/prove.py`. That covers `../elisa-engine-mocap/src` and `../elisa-ui/src` files the
   corpus includes, so a change there re-proves exactly the files that reach it. Errors and
   timeouts are not cached. A cached row keeps the seconds of the run that produced it.
3. Sync: only when something must be proved, the `.elisa` files of the checkout and of the two
   siblings' `src/` are rsynced to `~/work/mocap-fleet/tree/<hash of checkout path>/` on all
   hosts in parallel.
4. Run: misses go out at once, longest first by `build/fleet/durations.json` (never-timed files
   first, biggest first). Slots per host come from the cgroup CPU quota, v2 or v1 (vast: 38 of 80 visible cores);
   winpc, if listed, is capped at 3 (WINPC_MAX_JOBS). Before each file a host must have MIN_FREE_GB (1.5)
   free, cgroup-aware. Provers run under `nice -n 5` and `timeout FILE_TIMEOUT`. Slots share one
   ssh ControlMaster per 8 (sshd's MaxSessions is 10).

Left on the hosts on purpose (caches): `~/work/mocap-fleet/provers/` (one binary per prover key) and `~/work/mocap-fleet/tree/` (the .elisa sources only, a few MB, so later syncs are
incremental). `fleet_corpus.py --clean` removes `~/work/mocap-fleet` on every host. Delete
`build/fleet/cache` (or pass `--no-cache`) to force re-proving on the Mac side.

Results depend on the sibling checkouts, which other sessions edit and commit while runs are
going: compare two runs only when `../elisa-engine-mocap/src` and `../elisa-ui/src` are unchanged
between them.

`remote_prover.sh` and `remote_corpus.sh` accept SSH_CONFIG (e.g. `~/.ssh/fleet_config`) so they
can target fleet aliases such as `WINPC=vast`. If vast resets and loses `~/work`, the next run
re-syncs everything it needs from the Mac (`~/.cache/fleet/vast-setup.sh` restores the box).

Validation (2026-10-03, vast, prover elisa-proof 403b436 at O2, frontend 2678ff10, 91 files):

| Run | Wall |
|---|---|
| `remote_corpus.sh` on vast, JOBS=3 (old path) | 481 s |
| `fleet_corpus.sh` cold (empty cache, fresh `~/work`) | 185 s (incl. 54 s prover cross-compile) |
| warm, no changes | 0.2 s (91 cached) |
| one-line edit to `src/core/fade.elisa` (38 files reach it) | 141 s (53 cached, 38 proved) |

Cold, warm and edit runs gave the same state/proven/unproven for every file as the
`remote_corpus.sh` TSV (that run used prover dc963fb, the branch's previous commit; the counts
are identical). The cold run is bounded by `src/cli/main.elisa` (~80 s) plus the prover build.
