# Q01 — Current compiler and paired prover

## Current integrated qualification checkpoint

Compiler repair `03ae54d3` was rebuilt with clean Stage0 `35e5d07c`.
Stage1 SHA is `6909950f6974dc33440bff20986a3114b2768b8fc13fb1b5eabfa7b0503bfca4`;
linked runtime SHA is `6b5247cec30a39ac1d00e0e61a088ccb4d0901932d518d3f6be32e79b9f5412f`.
Provenance and freshness checks pass. Focused O0/O2/LLVM23 ASan callback
executions return 42, including 9 KiB arguments outliving the submitting frame.
Bare module-local `Arena&` and aliases now resolve their actual declaration;
qualified shadow, by-value shadow and scalar controls pass. Named usize
specialization controls and the application feedback executable pass.

Full Studio semantic checking passes for root `c36d1a7`, engine `378e8c33`
(integrating upstream `1a472e99`) and UI `f33e439b` with its captured dirty tree.
The 703-file manifest hash is
`bf0765bf0cec62f2ad6c261c30cfefdfbaebd805d51760cf1d04a078ac2618ac`.
The compile reads live paths under a checked manifest; it is not a copied tree.
Before/after validation passed. Exact record:
`build/studio-build.c83-03ae54d3/semantic-record.json`.
Native build, actual FBX journey, current-main gates and performance acceptance
remain open. Changes after this root capture require a fresh input manifest.
The later terminal FBX setup-refusal feedback change is outside this semantic
snapshot and still needs a fresh source qualification.

Proof pair `66309417` uses proof `797c8e1a` and compiler `c83ea675`; it is
comparison evidence after the newer compiler/root changes. Its feedback report
checks 8 functions, leaves 2 unmatched and refuses 6 unsupported functions;
32 replayed theorems do not establish complete source correspondence. Import
failure laws remain unsupported at the return-type gate; eight other selected
law packages are inadmissible. Keep those gaps open and rebuild the pair after
new checker repairs before qualifying current application laws.


**Priority:** P0; prerequisite for accepting subsequent source slices.

Current fetched compiler main is `7ec9def9`. Clean isolated Stage0 source
`778c8281` produces binary `35e5d07c`; use that selected source/product pair.
The installed `c81b66ee` binary has dirty-source fingerprint drift and cannot
qualify the current implementation.

Candidate `cdf2c329` built Stage1 `b4b2ca3d` with runtime `d3e7ffa9`;
official provenance and freshness checks pass. Its seed child numeric exit was
not captured because the zsh wrapper assigned its readonly `status` variable.
Retain that observation gap and the wrapper failure. Product provenance does
not establish runtime correctness. Focused checks found a real root-alias
resolution gap and a qualified generic indexed-result typing gap.

Combined candidate `4e54768d` adds the first-alias initialization repair and
owner-aware single-/multi-argument generic result typing. Clean Stage0 semantic
preflight passes (exit 0, peak 3,509,184 KiB); its fresh seed is running under
a parent-process 8 GiB RSS guard. Seed, provenance and freshness checks pass
(exit 0); product is `c36e5e84`, runtime `d3e7ffa9`. Aggregate worker-tree peak
was not captured, so do not claim an aggregate 8 GiB bound. Future heavy checks
must observe descendant RSS. Run exact alias/ambiguity/shadow controls,
qualified result IR/runtime assertions, defer/aggregate/ownership controls and
the full Studio closure at application `665ce9f`. Preserve the original failed
controls. The numeric-width mismatch assertions in the old qualified-payload
fixture are invalid: numeric width conversions are deliberately accepted. Retain
the oracle evidence and replace those assertions with genuine owner/type
mismatches. The local-callable optional payload error is valid and still missed;
resolve its return TypeId from the lexical function-type side table without a
global-name fallback. New direct-payload fixtures do not close that gap.

Fresh `c36e5e84` runtime control reproduces a blocking callback ABI defect:
aggregate void-poll O0 compiles then exits 139. ASan exits 134 in worker
`arena_alloc`; the generated aggregate callback expects a hidden arena pointer,
but both raw and closure indirect calls omit it. A scalar callback control
compiles and exits its expected 42. Historical repair `d5a9b58a` is absent from
the current ancestry and must be compared/ported against current source,
including worker arena transfer/adoption and indirect function metadata. Preserve
these exact artifacts under the candidate's `build/focused-c36/void-poll/`.
Do not launch or qualify the Studio FBX journey until this current runtime
control passes with its intended lifetime assertions. Scalar success does not
establish aggregate safety.

Coherent source candidate `2469d5ed` ports that callback ABI/worker ownership
repair, integrates lexical local-callback return typing and validates Fn-pool
rows/spans before access. Its first semantic preflight failed because the port
omitted a generic callback specialization helper. Follow-up `4218e314` restores
that helper; full-driver semantic checking passes (exit 0, peak aggregate
5,063,024 KiB under the 8 GiB guard). Preserve the first failed attempt.
Rebuilt-product provenance and O0/O2/ASan execution remain pending. Qualify raw
aggregate callbacks and scalar capturing closures separately; hidden-arena
aggregate lambda construction remains unsupported and must refuse explicitly.
Corrected fixture source is frozen at `07f9e3cb` for the next seed. Both fixture
AST parses and shell syntax pass. Clean Stage0 semantic checking reports the
same generic task callback hidden-region mismatch and optional-binding/escape
diagnostics against old and repaired runtime sources. Preserve this oracle
limitation separately; it neither accepts nor disproves the target Stage1 ABI
repair. Stage1 compilation, exact raw/closure IR shape and actual runtime/lifetime
controls remain the acceptance gate.
The previous publisher IR uses the permanent static-region fallback and has no
arena free or global rehome call. That absence alone does not prove a post-join
use-after-free; it leaves bounded cleanup and allocation cost unqualified.

The historical `5d17a2c0` full Studio semantic check reports only the atomic
`load` selection error. The frozen `1beecf48` full Studio check removes that
diagnostic but exits 1 with six codec `Token`/`u32` mismatches inside nested loops.
The codec passes standalone; minimize and repair the context-dependent inference
before full-graph acceptance. See the [retained diagnostic evidence](../proof-gaps/atomic-callee-owner-resolution.md).
Named constant value specialization,
prior project-repair integration, production ownership IR, all compiler/prover
gates and native Studio acceptance remain open. Earlier callback cache-content
and sanitizer results are retained comparison evidence in the ownership gap
record. Recheck them on the final source/product/runtime closure. Measure
cache-hit rehome allocation cost; unresolved-call static lifetime fallback does
not qualify cleanup.

Candidate `cdf2c329` integrates successful generic-await defer execution,
aggregate contract/defer snapshots and specialized generic-result arena demand.
The combined candidate preserves these repairs. Run their actual O0/O2 controls
on the freshly built product, including error propagation, reverse defer order,
large contract-bearing returns and qualified indexed results. Clean Stage0
reference execution is comparison evidence; it does not qualify Stage1 or Studio.
Named constant specialization, current-main gate comparisons, carrier counts
and quiet-window runtime benchmarks remain required before promotion.

The `1482a808` historical baseline is terminal: the 32-check fast profile has
24 passes and eight failures; the five separately run oracle lanes have one
pass and four failures. All 37 checks are accounted for. Retain its manifest
and logs under `/tmp/elisa-compiler-baseline-current-1482/build/current-main-1482-baseline/`.
It cannot qualify promotion against newer main, and overlapping work invalidates
performance comparisons from its durations. Preserve the upstream
counted-fill geometric-growth and NaN-diagnostic ownership fixes when integrating
project repairs. Rebuild the paired prover on the final compiler tuple; its
nested constant-owner source correspondence repair is still undergoing controls.
See [retained FBX evidence](../acceptance/fbx-request-proof-2026-10-07.md).

Latest fetched proof main is `d8716191`, UI main `dc6cd397` and engine main
`5bfcaa64`. UI `f33e439b` already contains its fetched main. The clean compiler
checkout was fast-forwarded to `7ec9def9`; the mocap engine branch is at `6a6aced2`, preserving project repairs. The
new engine delta to `5bfcaa64` contains documentation changes only; reconcile
it with the next legitimate source integration rather than creating a
documentation-only merge commit. Preserve
the dirty UI work and qualify its exact native-link snapshot. The proof checkout
is rebased onto `d8716191`, with owner/call repairs preserved at `bf05d339`
and checked helper conditions added at `34bd86b3`;
its matching producer/replay rebuild remains open. Captured
earlier source/product pairs remain comparison evidence; rebuild against the
final closure before qualification.

Remaining work:

- Finish replacing multi-source owner selectors with a source-qualified result descriptor
  or a supported lifetime-preserving representation. Preserve distinct FnTable,
  StructTable, GenericTable and AST owners. Do not unify unrelated input regions,
  erase lifetime tracking, or introduce copy allocations without measuring their
  cost. Distinguish a valid top-level empty owner from absence explicitly.
- Rebuild from a clean source snapshot using an explicitly selected source-matched
  Stage0. Select clean isolated Stage0 source `778c8281`, binary `35e5d07c`.
  Record its actual toolchain, preserved dirty test files and hash; verify that
  source changes do not invalidate the selected product before each seed.
- Repair named constant-value fixed-array specialization without duplicating
  literal limits or weakening view lifetimes. Literal `[2]` works where
  `[Limit::BYTES]` with value 2 declines; see
  [specialization gap](../proof-gaps/named-constant-array-specialization.md).
  Qualify exact owner/type resolution and ambiguous/wrong-type refusals.
- Preserve the resolved-callee/substituted-result carrier rule and fail-closed
  unmanaged-result checks. Cover inferred, qualified and explicit generic calls,
  concrete calls, scalar/borrowed results, shadow allocators, ambiguous mappings
  and explicit builtin Arena references. Reject by-value/shadow allocator owners.
- Rerun the nested owned-result regression through optional polling, void global
  publication and one-shot join/adoption. Grow both outer and nested buffers
  after all producing frames end. Retain O0/O2 and LLVM-instrumented ASan evidence;
  disabled leak detection cannot qualify leaks. The production path remains
  nonblocking. See [lifetime evidence](../proof-gaps/fbx-join-buffer-lifetime.md).
- Compare the required seed, self-host, native and registered fast gates
  against fetched main `b26659e2` or newer. Preserve semantic indexing, the
  view-origin fixpoint optimization, runtime AST lookup inlining and the newer
  global darray/module hierarchy resolution changes.
  Preserve those changes alongside the project repairs. Match exact failing fixture lists,
  preserving original expectations. The current fast profile registers 37 checks:
  32 profile scripts plus five standing checks. Match all 37 names and their
  failing fixtures, not only the profile-script subset. The historical
  `665f40d7` subset has 24 passing/8 failing profile scripts, native 566/566 and
  self-host A–D passing. Logs are retained under
  `/tmp/elisa-compiler-baseline-665f40d7/build/baseline-665f40d7/`.
  Rebuild and rerun current main before using it as the promotion baseline;
  historical gate outcomes cannot qualify the current compiler changes.
- Qualify the newly working Stage1 value-threading feature separately with
  `test/parity/value_threading_smoke.sh` and
  `test/parity/value_threading_codegen_smoke.sh` on current main and candidate;
  the earlier 37-check profile does not establish their coverage. Preserve
  owned field, loop capture/value and builtin container cases, plus dropped
  result, borrowed field, moved-use and wrong tuple-target refusals. Read the
  current STYLE_GUIDE before adoption. Use value forms for eligible owned data
  only after compiler and source-proof qualification; keep reference forms for
  borrowed data and FFI buffers. Verify that canonicalization preserves resolved
  callee identity, region ownership and the scalar-result carrier rule.
- Keep the preserved void-ensure behavior delta explicit: the old candidate native
  expectation yields 565/566; revised success/failure checks yield 567/567 and
  verify the exact guard/panic. This Stage0-built backend harness is not direct
  Stage1 CLI or unchanged-main parity. See
  [void contract evidence](../proof-gaps/void-return-postconditions.md).
- Measure per-function local carrier changes separately from hidden Arena ABI
  slots on a common frozen graph. Three small controls are byte-identical with
  local counts 0/0/4; candidate `2ef1fa26` refused the full common compiler graph
  with 67 lifetime diagnostics. Those controls establish neither a full-graph
  count nor a speed result. Requalify after the helper repair.
- Benchmark Stage1 runtime against current main on the same substantive inputs
  in a quiet measurement window. Require equivalent successful outputs and no
  slowdown; a refused workload supplies no timing ratio. Preserve raw commands,
  samples, resource measurements and product/input hashes.
- Push `codex/void-poll-region` only after all promotion requirements are met.
  The external merge train owns landing after 60 minutes quiet. Preserve project
  repairs and fetched borrow/reference/loop fixes; an ancestry check alone is
  insufficient. Backup-to-restoration tree equality is recorded in Git and the
  retained compiler evidence, rather than remaining an implementation task.
- Preserve the verified UI checkpoint and source closure when rebuilding after
  pending skin/session changes. Recheck fetched upstream and project repairs.
- Retain verified compiler/runtime source and linked-dependency provenance at
  every new snapshot. The current runtime input/object stamp was independently
  recomputed; source or recipe changes require another verification.
- Build the current producer/replay pair against that exact compiler and runtime.
  Qualify std paths against the selected trust root and refuse whole-unit bypasses.
- Compile current complete Studio and CLI graphs and preserve terminal evidence.
  The test entry point now refreshes generated runtime declarations through the
  canonical build-identity generator before deriving cache keys (`ebb9888`).
  Verify this path in the integrated run; reject mismatched compiler roots and
  preserve sealed historical input snapshots.
  Exercise borrow propagation, distinct owners and retained scratch capacity.
  Diagnose the captured contract-return SROA expansion while preserving snapshot
  semantics and ownership. O0 complete-graph LLVM generation succeeds for the
  earlier source-matched tuple; O2 remains unqualified. See
  [the isolated optimization evidence](../proof-gaps/studio-fixed-array-clone-cost.md).
  The return-snapshot repair seeded successfully at `a9b22071`; earlier
  `756315f2`, `fa0aeb0e`, `84574b1e` and `972ac576` seed attempts failed
  type/parser checks and supply no qualifying product. Capture large values at
  their original evaluation point, keep contract `result` storage distinct,
  and copy the captured bytes after cleanup. Qualify deferred mutation and
  failing contracts at O0/O2 before full Studio optimization. The implementation
  currently excludes error-function success out-parameters; audit that path
  explicitly and preserve its return-value timing rather than inferring coverage
  from non-error sret controls.
  Its strengthened 32,776-byte ensure/defer fixture returns the original first
  field and both padding endpoints at O0/O2 (exit 42). A false ensure compiles
  and aborts at runtime (134). Root inspected the retained evidence log under
  `build/large-return-snapshot-a9b22071-final/` in the compiler checkout.
  Product `7778893b…f1132` is captured comparison evidence after the new upstream
  fetch; repeat these controls and complete Studio optimization on the rebased
  source-matched product before acceptance.
- Finish the authorized diagnostic check without restarting on observation or
  per-file timeouts. Its drifting inputs cannot qualify current source; retain
  individual failures and obtain a fixed-snapshot current regression result.
- Keep native interaction, motion quality and real user acceptance separately open.
- Keep FFI capability propagation visible through `can` grants. Close strict
  native extent/contracts using bounded bridges; use `trusted` only at a deliberate
  documented stopping point. Audit all task captures separately from returned-data
  ownership, including source-aware Session Locate's nested request buffers.
  See [the foreign adapter audit](../proof-gaps/fbx-foreign-adapter.md).
- Bounded adapter strict compilation and the real high-block staging/conversion,
  digest, cache and source-preservation probe pass for the captured `50b16e68`
  tuple. This is a qualified native adapter slice, not current application or
  asynchronous ownership acceptance. Requalify the full graph after the repair
  build; do not mix its std/runtime sources with an installed upstream binary.
- Restore, recovery scan and recovery discovery now submit bounded inline paths,
  matching candidate scan. Qualify all four callbacks and publication after the
  polling frame ends; input capture alone cannot establish returned-data lifetime.

**Latest Git refresh (2026-10-08):** compiler upstream remains `7ec9def9`,
Stage0 remains `778c8281`, and prover upstream remains `e27b11bc` after fetch.
Engine upstream advanced to `2d052b44`; merged into the mocap client at
`6a6aced2`, preserving project repairs. These four engine commits update retained
validation and quantifier-repair documentation; they do not establish a Studio fix.
The combined GSR and atomic callee-resolution compiler candidate `b8256d31`
passes its frozen full-driver Stage0 semantic preflight. Build its Stage1 product
with the current Stage0, retain source/product/runtime correspondence, then qualify
the regressions and full Studio graph. No current Stage1 runtime acceptance is
claimed from that semantic preflight. The candidate seed subsequently completed
with exit 0 and matching provenance: Stage1 product
`ff62235c816679909a3f251939eb4ef1405cd393ad620e663e70b4454ad661d5`,
runtime object
`d3e7ffa90eff6a89966f9d3318a2262b2b52d0c38ec9148cc50cf6ce4a4ad7c8`.
The retained seed log is `/tmp/Elisa-compiler-atomic-load/build/seed-b8256d31.log`.
Focused GSR/atomic regression execution and the fixed-snapshot Studio semantic
check remain pending. The seed alone does not qualify installation or FBX redraw.
The focused run also exposed dropped lexical ownership on parser `__using`
annotations. Repair `1beecf48` restores the current module and passes Stage0
semantic checking; its exact-source reseed is in progress. Preserve the failed
`b8256d31` regression log and require individual line/message assertions in the
rerun. The next Studio snapshot includes the source-path admission law and
validated FBX request comprehension from root `3e0ac6a`.

**Finish evidence:** exact input manifests and product provenance, authenticated
current prover/replay pair, current complete graph/link closure and successful
fixed-snapshot regression evidence. A seed, object or package alone does not close
this item.

Return to the [delivery queue](current-delivery-queue.md#q01--current-compiler-and-paired-prover).
