# Q01 — Current compiler and paired prover

**Priority:** P0; prerequisite for accepting subsequent source slices.

Current fetched compiler main is `7ec9def9`, including sized AST record
performance work; installed Stage0 source remains `778c8281`. Rebase the project
repairs onto this main or newer and rebuild before qualification or installation.
The latest built repair candidate is `b8256d31`, based on `7ec9def9`, with
combined alias-owner and atomic-callee repairs. Its focused regression log
reports 12 cases and one failure: the collision fixture itself declares
`Joinable` twice. Correct that fixture without weakening its collision assertion
and rerun. Nested owning-return and qualified/parent alias controls produce the
expected refusals; scalar collision controls produce none. Retain separate
reference/view, ambiguous-owner and cyclic-alias refusal controls.

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

Direct body comparison confirms generic `pool_await` returns skip deferred
actions before region unwind in current source. Port `a69638c1` on
`codex/current-generic-await-defer` restores the deferred-action check and carries
direct/generic/failed-postcondition runtime controls. Integrate after the frozen
`1371ef63` capture; rebuild and run these controls on the combined tuple before
acceptance. The port alone is unqualified. Specialized generic-result arena
demand and aggregate return snapshots also have confirmed source differences;
other historical repair groups require behavior comparison before porting.

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

Latest fetched proof main is `e27b11bc`, UI main `dc6cd397` and engine main
`2d052b44`. UI `f33e439b` already contains its fetched main. The clean compiler
checkout was fast-forwarded to `7ec9def9`; the mocap engine branch merged its
new main without conflicts at `6a6aced2`, preserving project repairs. Preserve
the dirty UI work and qualify its exact native-link snapshot. The proof checkout
is rebased onto `e27b11bc`, with owner/call repairs preserved at `9fddab1a`;
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
  Stage0. Current installed Stage0 is source `778c8281`, binary `c81b66ee`.
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
