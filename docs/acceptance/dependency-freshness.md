# Dependency freshness audit — 2026-10-06

Fetched `origin` in all five checkouts before comparing `HEAD...origin/main`.
All adopted dependency branches contain every fetched upstream commit.

| Dependency | Local HEAD | Fetched upstream | Ahead / behind |
| --- | --- | --- | --- |
| Compiler | `f292cbe0` | `72a75282` | 39 / 0 |
| Mocap proof assistant | `5776350b` | `151a2772` | 14 / 0 |
| Primary proof assistant | `151a2772` | `151a2772` | 0 / 0 |
| Mocap engine | `01f5aec7` | `7699ec52` | 20 / 0 |
| Elisa UI | `8ab2eb39` | `dc6cd397` | 6 / 0 |

The compiler, mocap proof assistant, engine and UI sources are clean.
Uncommitted primary proof-assistant work belongs to its active development
checkout and is preserved; it is not a published upstream revision.

## Binary provenance

The normal Stage1 compiler has been rebuilt at `f292cbe0`. The default
`../elisa-proof-mocap/build/elisa-proof` manifest identifies proof source
`5776350b`, frontend and Stage1 compiler `f292cbe0`, with both source trees
clean. The manifest records the binary hash and source tree hashes.
Build and check scripts select these default paths. Historical override builds
must remain separate from current acceptance evidence.

Freshness does not establish product correctness. The reproduced UI event
scope collision now compiles successfully; integrated Studio qualification is
separate. Export validation source proves/replays 6/6 and its laws 14/14 with
zero gaps or findings. The full gate using these default products finished with exit code 1,
recorded in `build/current-indexed-decimal-check.log`. Source changes
during a run prevent treating it as immutable snapshot acceptance.

Repeat fetch, ancestry and manifest checks before final snapshot acceptance.
Rebuild stale binaries and rerun affected verification after dependency changes.

## Latest upstream refresh

A subsequent fetch confirmed zero missing `origin/main` commits in compiler
`f292cbe0`, mocap prover `493ab83f`, engine `01f5aec7`, UI `8ab2eb39`,
and primary prover `151a2772`. The mocap prover source advanced beyond the
default binary to repair decimal append arithmetic. Its separate clean
candidate proves and independently replays the focused append obligations
3/3; expanded decimal laws still have replay gaps. Promotion remains pending
qualification. Source freshness and default binary qualification are separate.

The latest mocap prover source also repairs scoped enum ownership; additional
enum value evidence remains in development. The default remains the qualified
`5776350b` build until the replacement's certificates independently replay.
An isolated compiler candidate `faabd1f7`, based on current `f292cbe0`, admits
C-string ADT payloads. Its seed manifest matches its source commit and both the
minimal payload example and recovery store compile successfully. Runtime and
ABI qualification remain open, so the normal compiler has not been replaced.

Mocap prover source subsequently advanced to `6bced403` for exact-owner enum
value evidence, including equal-valued aliases. Focused comparisons independently
replay 5/5; broader proposition formation and caller-summary gaps remain open.
The default binary is still `5776350b`. Compiler candidate extraction IR also
loads the C-string payload with `load ptr`; emitted constructor and extraction
layouts agree, but this is compile evidence rather than runtime qualification.
