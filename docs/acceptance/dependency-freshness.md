# Dependency freshness audit — 2026-10-06

## Latest observed checkout state

Fetched the four currently available origins on 2026-10-06 after the dependency
instructions changed. Earlier sections below are historical observations.

| Dependency | Local HEAD | Fetched `origin/main` | Ahead / behind |
| --- | --- | --- | --- |
| Compiler | `bb1f4095` | `23a0e16a` | 5 / 0 |
| Primary proof assistant | `01c953c6` | `2610ddb6` | 115 / 0 |
| Mocap engine | `e11085c1` | `7699ec52` | 22 / 0 |
| Elisa UI | `8ab2eb39` | `dc6cd397` | 6 / 0 |

The required `../elisa-proof-mocap` checkout was absent at this fetch. It has
subsequently been restored on `mocap-cleaner-proofs` at the primary integration
source `01c953c6`. Its history contains earlier mocap commit `6ebc2a81`, verified
by `git merge-base --is-ancestor`. The clean rebuild of prover and replay checker
completed in generation `232f491a63094a1781ce455f4143d98c`.
`scripts/check_prover_freshness.py` accepted the selected prover's binary hash,
proof source, frontend tree, compiler source/product/recipe and linked runtime.
The authorized full check is running with this explicit generation; reviewed
proof results and independent replay remain pending. This ancestry check does not establish preservation of earlier
uncommitted diagnostic patches.

The compiler manifest declares source `23a0e16a`; its normal provenance checker
passed the source-tree and product checks. Compiler
remote-gate scripts have local changes, which are preserved. No new product
acceptance is claimed from this fetch or manifest inspection.

On 2026-10-07, after fetching compiler origin again, the integrated Studio
diagnostic compile passed with both qualified backend repairs. Those repairs
and the ownership-preserving readiness API are adopted in the normal compiler
through `bb1f4095`; its replacement seed completed successfully and the normal
provenance checker passed on 2026-10-07. Product SHA-256 is
`203009661b41a4aed677487848d300b7232d0801f76fa19a65222309ffe039a7`. The preceding
`23a0e16a` compiler/prover products are comparison evidence while that source
and linked-product transition remains incomplete. Engine `e11085c1` adds the
read-only no-follow source identity adapter; Objective-C syntax qualification
passed, with linked/native behavior still open. Earlier tables below remain
historical observations.

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

## Refresh after the latest freshness request

Fetched all five origins again on 2026-10-06. Compiler `f292cbe0` remains
39 commits ahead / zero behind; mocap prover `6bced403` is 18 ahead / zero
behind; primary prover `151a2772` is current; engine `01f5aec7` is 20 ahead /
zero behind; UI `8ab2eb39` is 6 ahead / zero behind. No upstream update is
missing. Compiler, engine and UI checkouts are clean. Both prover checkouts
have active development changes, which are preserved.

The default prover manifest still records `5776350b` with compiler/frontend
`f292cbe0`. This is not the newest local prover source. Newer isolated prover
repairs have unresolved independent replay gaps and an abnormal exit in the
stage-policy diagnostic; they are not yet qualified replacements. The C-string
compiler candidate compatibility check is still running. Keep these limitations
explicit rather than describing every default binary as the latest local build.

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

## Current adoption status

Fetched all five origins again on 2026-10-06: compiler `04b384ec` is
40 commits ahead / zero behind, mocap prover `3ac99624` is 21 ahead / zero
behind, primary prover `151a2772` is equal to upstream, engine `01f5aec7`
is 20 ahead / zero behind, and UI `8ab2eb39` is 6 ahead / zero behind.

The C-string payload patch was adopted into the normal compiler source as
`04b384ec`. Its candidate compatibility run passed 78 executable tests and
four CLI workflows; direct payload runtime qualification remains open.
The normal compiler seed rebuild is running, recorded in
`build/recovery-cstr-adopted-compiler-seed.log`. Until its provenance check
passes, the installed normal binary must not be described as matching this
new source revision.

Clean isolated prover `3ac99624` independently replayed the focused recovery
report-stage obligations (78 source and 99 law obligations). Broader stage
and journal proof runs have abnormal exits under investigation. The default
prover remains `5776350b`; adopting the latest source as the default binary
is unfinished. These are current limitations, superseding the earlier
candidate-running and compiler-not-adopted entries above.

The normal compiler seed subsequently completed successfully. Its freshness
check confirms source revision `04b384ec`; the integrated time-map report
formatter emitted an object without diagnostics using this normal compiler.
Direct C-string payload runtime qualification is still open.

## Latest verified compiler and pending prover build

Fetched all five origins again on 2026-10-06. Compiler `45330579` is 41
commits ahead / zero behind; mocap prover `4da37c97` is 22 ahead / zero
behind; primary prover `151a2772` equals upstream; engine `01f5aec7` is
20 ahead / zero behind; UI `8ab2eb39` is 6 ahead / zero behind.

The normal Stage1 binary's provenance check matches `45330579`. Its global
enum-owner reproduction and recovery publication adapter emit fresh objects
without diagnostics. Integrated Studio qualification remains pending.
The newest prover source repairs recursive search depth handling; its separate
`elisa-proof-goaldepth-453` candidate is building against compiler `45330579`.
The default prover is still `5776350b`; latest-source binary adoption remains
unfinished until the candidate builds and its certificates independently replay.

The normal compiler subsequently advanced to `3c72f59f` for lexical ownership
of ADT constructor metadata. Its seed completed successfully and its provenance
check matches that exact source revision. The reduced two-module constructor
example emits a fresh object, as do channel/rig caches, the window source,
worker-wait policy and existing Studio performance fixture. Integrated Studio
and full current-snapshot checks remain pending. Prover `4da37c97`'s separate
candidate was built cleanly against compiler `45330579`; broad journal search
and independent replay gaps remain under investigation, so it has not replaced
the older default prover.

Compiler `720896f4` subsequently closes the separate lexical match-pattern
payload-arity lookup. Its normal seed and provenance check match this revision.
The reduced constructor/match reproduction and current existing performance
fixture emit fresh objects. Recovery UI integration and a stable full check
still require qualification; the prover default has not been promoted.

Checked Studio builds and `scripts/check.sh` now run
`scripts/check_prover_freshness.py` before qualification. It checks the selected
binary hash against its manifest, current prover HEAD/source contents, current
Stage1 provenance, linked frontend/compiler revisions and runtime hash. The
older default prover is rejected explicitly rather than silently qualifying a
current source snapshot with an old tool. A missing/malformed manifest fails.

Historical diagnostic or candidate comparisons require explicit
`MOCAP_PROOF_COMPARISON=1` alongside the selected `ELISA_PROOF` path. This mode
still verifies the manifest's binary hash and prints that the run is a
comparison, not current snapshot qualification. The active earlier diagnostic
run started before this preflight existed and remains comparison evidence.
`STUDIO_SKIP_CHECKS=1` remains the explicit compile-only route; it does not
establish proof acceptance. No executable tests were added or run for this gate.

## Subsequent upstream refresh

A new fetch confirms compiler `720896f4` is 43 ahead / zero behind origin,
mocap prover `4da37c97` is 22 ahead / zero behind, engine `01f5aec7` is 20
ahead / zero behind and UI `8ab2eb39` is 6 ahead / zero behind. The primary
prover is now `0491e6ad`, two local commits ahead / zero behind: file splitting
and `ProofReport` state regrouping. These are independent local development,
not missing published upstream changes. Their worktree is preserved. Carrying
that broad refactor into the mocap prover requires compatibility qualification
and preservation of its mocap-specific repairs. No default prover promotion
is claimed by this source refresh.

## Latest fetched source snapshot (2026-10-06)

All five `git fetch origin` operations completed successfully. Comparisons
against each fetched `origin/HEAD` show zero missing upstream commits:

| Checkout | Local HEAD | Fetched upstream | Ahead / behind |
| --- | --- | --- | --- |
| Compiler | `1f136742` | `72a75282` | 44 / 0 |
| Mocap prover | `6ebc2a81` | `151a2772` | 24 / 0 |
| Primary prover | `0491e6ad` | `151a2772` | 2 / 0 |
| Mocap engine | `01f5aec7` | `7699ec52` | 20 / 0 |
| Elisa UI | `8ab2eb39` | `dc6cd397` | 6 / 0 |

Compiler/prover source edits remain unqualified WIP beyond these HEADs. The
default compiler product is stale, and its diagnostic reseed is waiting on a
live isolated host build. The prover fuel patch likewise awaits a matching
compiler. These fetch results establish published-source ancestry only;
they do not establish binary freshness or complete Studio/proof acceptance.
No checkout was repointed and no stale-product override was used.

A fresh fetch of all four origins on 2026-10-07 found no missing published
`origin/main` commits at the selected compiler/prover/UI/engine heads above.
The prover build started with the preceding compiler product terminated at its
input revalidation barrier (exit 2), refusing to cache or publish mixed compiler,
source, recipe or link inputs. It published no current product pair. A new
paired build against verified compiler `bb1f4095` is required; the refused
build does not establish proof correctness or replay qualification.

## Runtime selection refusal and terminal comparison check (2026-10-07)

The subsequent pair at prover source `4b71c24a` and compiler `bb1f4095`
produced generation `f74f69896e2d47e19011c166a93a46df`. Its internal pair
consistency checks passed, but `scripts/check_prover_freshness.py` refused it:
the linked global `~/.elisac/elisacore_runtime.o` differed from the selected
compiler's `build/runtime/elisacore_runtime.o`. This generation is not current
qualification. Rebuilding with an explicit selected runtime is in progress;
acceptance requires the stricter freshness gate as well as producer and
independent replay results.

The earlier authorized `scripts/check.sh` run has now terminated with exit 1.
Its log is `build/check-current-2026-10-07.log`; the proof baseline gate reports
regressions, unsupported/unknown obligations, missing reports and entries
needing review. Sources and selected products changed during that long run,
so it remains comparison evidence. No baseline was relaxed to make it pass.
A stable current snapshot needs a new complete check after compiler and prover
qualification; this terminal failure does not establish current acceptance.

Another fetch of all four selected origins completed on 2026-10-07 before the
next qualification cycle. Their source ancestry is:

| Checkout | Selected HEAD | Fetched `origin/main` | Ahead / behind |
| --- | --- | --- | --- |
| Compiler | `bb1f4095` | `23a0e16a` | 5 / 0 |
| Mocap prover | `4b71c24a` | `2610ddb6` | 116 / 0 |
| Mocap engine | `e11085c1` | `7699ec52` | 22 / 0 |
| Elisa UI | `8ab2eb39` | `dc6cd397` | 6 / 0 |

These successful fetches establish no missing published upstream commits at
that observation. They do not qualify the isolated compiler repair, the pending
runtime-matched prover pair, or the newly integrated navigation handlers.
