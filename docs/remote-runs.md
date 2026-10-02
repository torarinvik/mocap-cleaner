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
