# Current delivery queue

[Roadmap](../../IMPLEMENTATION_PLAN.md) · [Shared acceptance](acceptance-and-dependencies.md)

This is the execution order for the remaining roadmap, not a replacement for
M0–M8. Source changes already in Git need qualification rather than another
implementation. An open acceptance item stays open until its evidence exists.
Reassess this queue after an integrated build, a discovered regression or a
completed user journey. Update outcomes from evidence, not elapsed effort.

## 1. Restore a usable, current qualification path

### Q01 — Current compiler and paired prover

**Priority:** P0; prerequisite for accepting subsequent source slices.

Compiler merge `48dc78e2` includes fetched performance changes through
`63585c5f` and preserves project-specific repairs. Its reseed completed, and the
complete Studio graph and native link succeeded. The rebuilt retained package
has a visibly discoverable Workspace / File control. Publication into the usual
bundle location was refused while the old running app held its lease; preserve
that instance and reconcile publication after release. See
[current build evidence](../acceptance/studio-workspace-build-2026-10-07.md).
This does not qualify the entire roadmap or UI interaction journey.

Remaining work:

- Compiler repair `4635427d` is held from promotion: its name-only generic
  test creates arena carriers even for scalar specialized results. Candidate
  `f9e23008` implements resolved-callee, substituted-result region demand and
  retains fail-closed unmodeled result handling. Qualify this implementation
  before pushing `codex/void-poll-region`: run a
  join/void-caller lifetime regression (prefer sanitizer coverage), compare
  carrier-function counts and benchmark Stage1 against current main with no
  slowdown. Rebase on `665f40d7` or newer, preserve borrow/reference/loop fixes,
  and run stage0 seed, `self_host_gen3_smoke`, `backend_native_smoke` and the
  fast gate. Failure lists must match main. Push only after these gates; the
  external merge train owns landing after its 60-minute quiet period. A seed
  of the broad repair remains diagnostic evidence only.
  Inspect isolated callers for scalar specialization, a scalar result borrowing
  region-backed input, and a same-named function in another module; unrelated
  allocations must not mask their carrier counts. Cover inferred, qualified and
  explicit generic calls returning owned storage. The running lifetime fixture
  must exercise optional task binding, void publication and growth of both the
  outer container and nested buffers after publication. Retain commands, hashes,
  sanitizer output and terminal exits rather than deleting the fixture artifacts.
  The first rebase onto `665f40d7` dropped project merge-resolution changes:
  the backup-to-rebased tree diff spans 69 files, including the worker arena,
  result adoption, callback ABI handling and provenance guards. Preservation
  commit `3f578e5a` restores them: root independently verified its tree hash
  equals the backup's `5d5c40f2b75e8d21c39ea57b6e9efeba7e51b082`.
  Candidate `f9e23008` differs only by a trailing blank-line removal and retains
  current-main ancestry. A clean worktree or ancestor check alone cannot
  establish preservation; the retained original branch under
  `backup/void-poll-before-main-rebase` supplies the comparison source.
  The first candidate seed failed on concrete Stage0 binding/ref diagnostics.
  Commit `331982f7` repairs those source errors; the next seed succeeded with
  product SHA-256 `f0af9891268cc6b66a8a5eb373c8d71fb114056fd1a4ef6a9c694b25370a0e27`
  and runtime SHA-256 `2c7a16bb5f87dbff7e2413e8886a31e832115f897b4a4b30df2aa56a59ace93d`.
  Root independently verified these hashes and the clean worktree. Source
  provenance and freshness checks pass; lifetime, performance and regression
  qualification remain open. Correctness builds may overlap corpus checks
  with measured memory headroom; performance measurements require a quiet,
  matched comparison window.
  Follow-up candidate `cd6c98b9` resolves qualified explicit generic result
  types and keeps touched files below 600 lines. Its exact seed and automated
  lifetime smoke pass: O0/O2 and LLVM-instrumented ASan return 42; leak
  detection is disabled, so this is not a leak qualification. Root checked
  the retained automated log and ASan executable hash `c23ca347` under
  `build/void-poll-result-region-20261007T184001Z-23185` in the compiler checkout.
  Isolated scalar controls have zero carriers; two owned-result controls have
  one each. Full before/after counts, performance and required gates remain open.
  Candidate `d355c139` fixes qualified concrete call demand; its exact seed
  and focused O0/O2/ASan smoke pass, and root's independent scalar-caller
  reducer emits successfully. The current proof build now refuses two JSON
  calls, down from nine. Their explicit `Arena&` allocator ABI suppresses the
  hidden result slot that the call guard currently requires. Validate the
  exact resolved allocator type and emitted owner argument, reject shadow
  types and ambiguous ABI mappings, and retain unmanaged-result refusals.
  This remaining client build failure must be resolved before promotion.

- Committed compiler repair `d5a9b58a` is rebuilt with product `b4e9a69d`
  and runtime `a8de91a1`; source provenance passes. The focused FBX worker
  runs successfully after the submitting frame ends and after a helper returns
  its joined Result, including growth of returned arrays and Memo nodes.
  The actual void polling/global-publication case still loses returned bytes
  and crashes cleanup: it needs the caller's result allocation owner, rather
  than assuming a function return-region slot. Preserve this failing case and
  fix the compiler ownership path before accepting app publication. These
  partial probes do not close Q01 or the visible FBX journey.

- The fetched comparison baseline is now `665f40d7`, including borrow-exclusivity,
  reference-field reads and loop-value slot binding. Its clean Stage0 seed
  produced compiler SHA-256 `16a373d5f9ba605016d84fa8216c4e9e05aa73986d05bd73b1bf839dc59a09e3`
  and runtime SHA-256 `ca40ba1db8a74110936ad5cdaf808707020c5c74ebb6e491bda2198696d13b8a`.
  The frozen fast profile selected 32 checks and all 32 now have terminal
  records (24 pass, 8 fail). Its registered command list matches the profile's
  source patterns; the earlier 37-check count was incorrect and is superseded.
  `emit_annotated_list_parity_smoke` passes 354 cases, while
  `emit_ast_parity_smoke` reports 28 differing cases. The resumed baseline also
  reports header parity failure (58 divergent cases; the final refusal is
  `zeroed_relative_nested_module_reference_alias`) and interface parity failure
  (63 of 336 cases). These failures are
  terminal baseline results, not interruptions or candidate results. Remaining
  failed scripts are interpret, packed, test-runner, unsafe and slice-real,
  alongside AST, header and interface. Slice-real fails generated Stage0 inputs
  on missing arena-cache lock intrinsics, rather than a measured Stage1 parity
  difference. The exact failure lists must still match the candidate. Retain
  terminal results and
  exact failure lists before comparing the repair. Neither a baseline seed nor
  an installed upstream compiler qualifies project repairs or the Studio graph.
  Baseline `backend_native_smoke` reports 566/566 passing checks;
  `self_host_gen3_smoke` passes stages A–D, including gen3/gen4 object equality
  and identical output over 40 runs. Freshness checks pass afterward. Retained
  results, commands and logs are under the baseline compiler checkout's
  `build/baseline-665f40d7/`; candidate equivalents and timing remain open.
- Preserve the verified UI checkpoint and source closure when rebuilding after
  pending skin/session changes. Recheck fetched upstream and project repairs.
- Retain verified compiler/runtime source and linked-dependency provenance at
  every new snapshot. The current runtime input/object stamp was independently
  recomputed; source or recipe changes require another verification.
- Build the current producer/replay pair against that exact compiler and runtime.
  Qualify std paths against the selected trust root and refuse whole-unit bypasses.
- Compile current complete Studio and CLI graphs and preserve terminal evidence.
  Exercise borrow propagation, distinct owners and retained scratch capacity.
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

**Finish evidence:** exact input manifests and product provenance, authenticated
current prover/replay pair, current complete graph/link closure and successful
fixed-snapshot regression evidence. A seed, object or package alone does not close
this item.

### Q02 — Source authentication and critical laws

**Depends on:** Q01. Package/source correspondence work may proceed beforehand.

The current d5 compiler request-policy run has 99 obligations, 60 proven,
39 unproven and four replay gaps; its package is source-inadmissible. See
[the exact request proof record](../acceptance/fbx-request-proof-2026-10-07.md).
This does not supersede the separate staging-policy report below.

- Qualify exact expanded bytes, ordered imports and lexical declaration owners.
  Changed bytes, order, paths, duplicate names and unsupported scopes refuse
  authentication. Portable replay must remain labelled unauthenticated.
- Prioritize document preservation, candidate publication, history, source
  identity, export admission and storage mutation contracts before secondary
  convenience policies.
- For each law retain its exact declaration, preconditions, checked predicate,
  source identity and independent replay result. Test contradictory assertions
  as negative controls; never replace unknown results with compile counts.
- Rebuild the matched pair after every proof-source repair. The earlier clean
  captured baseline was pair `655657441d704884a881f28382b46321`, built against
  compiler `48dc78e2` after committed helper-purity repair `fed9a108`.
  TakeSourceRef had 59 obligations, 34 proven and 25 unproven; staging had
  115 obligations, 21 proven and 94 unproven. Their 34 and 21 resource checks
  replayed respectively, but both packages remained source-unauthenticated
  with unsupported correspondence. Pair integrity is not source authentication.
  Retain the exact immutable pair reports; do not treat package admissibility
  as verified predicates. Subsequent proof edits require a new current pair.
- Current clean pair `1c9666c5f95e4e2d9b355e4c677100e8` follows proof commit
  `af85ea4f`, using compiler `48dc78e2`. Its immutable `staging.report.json`
  has 98 obligations, 36 proven and 62 unproven, with 36/36 replay. All thirteen
  `stage_admitted` postconditions and its resource check are proven. The owner-resolved atom rule admits
  only verified total-pure Bool helpers without preconditions, retaining exact
  call arguments. Source correspondence remains 0 checked, 38 unsupported and
  unauthenticated; neither this result nor earlier reports closes Q02.
  Exact hashes and the immutable run mapping are in
  [the staging proof record](../proof-gaps/fbx-source-staging-admission.md).
  Preserve shared reborrow, mutation exclusion and owner-qualified constraints.
  Zero-argument generic calls need checked call-site region substitutions;
  matching an ambient region by spelling cannot establish a valid binding.
- Qualify generation and creation-journal laws again with the repaired pair.
  Historical reports remain unauthenticated and cannot close Q02. Exact gaps
  are tracked in [proof gaps](../proof-gaps.md).
- Continue reducing connective/source admission gaps and fact growth. Extra
  enum disequality facts cannot substitute for the checked relation between a
  helper result and its inputs. Preserve fail-closed authentication and keep
  unresolved laws open. New repairs require fresh matched products and reports;
  the clean pair above remains the captured evidence until then. See [the exact
  qualification record](../proof-gaps/build-generation-policy-proof-20261007.md).

**Finish evidence:** authenticated intended predicates, negative controls and
unchanged regression expectations. Unresolved laws retain their gap records.

## 2. Finish one reliable import–repair–export journey

### J01 — Transactional editing and failure recovery

**Priority:** P0. **Depends on:** Q01 for qualification, existing worker protocol.

Qualify synchronous edits, queued/coalesced edits, Undo/Redo, no-op drafts,
cancellation, take replacement and close approval as one state machine:

| Event | Required result |
| --- | --- |
| Candidate evaluation fails | Committed history, result and saved marker remain unchanged; actionable failure stays visible. |
| Several edits arrive while busy | A visible draft is distinct from the committed result; only the accepted evaluated result enters history. |
| Undo cancels a draft | Draft disappears without also undoing a committed edit unintentionally. |
| Source/history changes during work | Stale candidate is rejected; retained preview is identified accurately. |
| Save/export while draft is pending | The handler refuses or explicitly waits under the documented policy; it cannot claim the draft was saved/exported. |
| Close approval followed by a changed draft | Approval is invalidated and current work is reviewed again. |
| Counter reaches its limit | Document identities never wrap; redraw rollover invalidates all dependent caches. |

Include pointer, keyboard and accessibility dispatch. Record status, selection,
focus, dirty state and undo count after each event. Measure busy feedback and
last-valid-preview retention on a long take; a policy-only check is insufficient.

### J02 — Consistent units and honest diagnosis

**Priority:** P0. **Depends on:** [complete physics migration](physics-unit-migration.md).

- Finish producers, kernel bounds, inverse conversions, thresholds and report
  conversions together. Preserve angular units and explicit time bases.
- Reject or disclose missing feet, invalid timestamps, nonfinite positions,
  unsupported coordinates, collapsed thresholds and unavailable mass/environment
  information. An unavailable detector cannot supply a passing quality score.
- Keep CLI and Studio availability, contacts, floor and balance decisions
  consistent on the same source and settings. Revalidate after preceding fixes.
- Compare signed rounding boundaries and intended precision changes with the
  frozen corpus. Audit residual accumulation and conversion overflow.

**Finish evidence:** authenticated boundary laws; per-frame CLI/Studio parity;
before/after metrics in declared units; preservation checks; unavailable-state
text and overlay review. New refusal counters alone do not close this item.

### J03 — Diagnosis, controlled preview and precise repair

**Priority:** P0. **Depends on:** J01–J02; quality thresholds fixed before comparison.

Use one labelled noise case and one contact case as the first complete vertical
slices. Select an issue without editing; jump to its exact frame/joint; explain
the proposed scope and trade-off; preview source/result and adjacent motion;
accept once or cancel; undo; save/restore; export/reopen the same result.

Then cover every existing exposed tool with its own preservation fixture.
Complete parameter inspection, range/anchor controls and accessible alternatives
before adding another algorithm. Do not infer impact labels from improvement
metrics or call an intentional fast movement noise without evidence.

Computed boundary/velocity distances now pass finite, nonnegative and bounded
admission before integer conversion (`0d1f557`), with contracts and companion
laws. Contact, boundary, joint and velocity comparisons also require the shared
current/candidate sampling-domain check. Qualify these implemented paths with
overflow, equal-length different-time and ordinary aligned cases, preserving
the existing tolerances. Confirm that unavailable measurements retain the
candidate and explain the missing preservation evidence in the UI. Source
implementation alone does not close these runtime and proof requirements.

**Finish evidence:** complete interactions, local and aggregate quality gates,
negative controls, meaningful history entries and session/export parity.

### J04 — Reviewed publication and recoverable storage

**Priority:** P0. **Depends on:** J01 and exact captured result identity.

- Complete GLB/report staging, partial outcomes and retry from the same immutable
  snapshot. Distinguish file integrity, motion review and durable publication.
- Exercise occupied paths, source aliases, failed reports, interrupted writes,
  unavailable destinations and changed review state. Preserve prior outputs.
- Finish the Storage review/move/receipt/restore journey, including long paths,
  stale reviews, conflict refresh and unknown recovery locations. Do not claim
  freed space from a successful namespace move alone.
- Supply a recoverable generated-build cleanup flow as well as animation-output
  cleanup. Preserve current products, active generations and required receipts;
  explain what can be removed and why before mutation.
- Bind activity protection to the running artifact with a process-lifetime
  shared lease. Cleanup must acquire its exclusive lease and retain it through
  revalidation, the directory move and durable receipt publication. Unknown or
  legacy lease metadata stays protected. A failed lease acquisition must explain
  the refusal before a Studio window opens.
- Qualify direct launches, symlink launches, Finder launches, copied/renamed
  bundles and simultaneous launch/cleanup. Distributed bundles must acquire
  their own artifact-local lease without accessing the developer checkout.
  Precreate lease files during build/package creation; launching an installed
  bundle must not modify its signed contents.
- Qualify the implemented explicit build/package contents inventories against
  native cleanup validation. Evidence and schema are recorded in
  [the inventory acceptance record](../acceptance/build-generation-cleanup-policy-2026-10-07.md).
  Reject unknown descendants, linked entries, changed file contents, group/other-
  writable entries or modes inconsistent with the evidence, replaced ancestors
  and mismatched artifact/build identities. Repeat
  enumeration on retained descriptors must start at the beginning and distinguish
  read errors from end of directory. Revalidate immediately before mutation.
- Cover failed and partial generations with an independent durable creation
  journal and declared ownership; do not invent a sealed executable identity
  for a build that never linked. Refuse an active builder, preserve diagnostic
  evidence required by recovery, and reconcile crashes at every creation stage.
- Present managed quarantine as recoverable storage. Report moved bytes
  separately from freed disk space; retain external inventory and transaction
  records until their recovery dependencies are resolved. Provide restore from
  the journal identity even after the original generation name is reused.
- Qualify the connected native generation move/Restore/reconciliation
  adapter, Elisa controller and review UI. Raw status/phase/location
  decoders must reject unsupported values; native integer flags accept only
  exact 0/1. Never publish a recoverable success from a parsed receipt alone:
  verify identity, location, locks and durable journal/parent synchronization.
- Before persisting a move intent, match the complete reviewed identity under
  retained global and artifact locks: artifact/path/device/inode plus product,
  manifest, contents-inventory and lease-record digests. The native
  `validate_reviewed` operation and Elisa adapter now compare those controls
  under the begin transaction's retained locks, with repeat validation before
  intent and mutation. Wire the controller to require that admission, rather
  than treating a successful begin as complete review validation. Build manifest
  evidence hashes exact `inputs.json` bytes; packages hash exact
  `PACKAGE-GENERATION.json` and separately `BUILD-INPUTS.json` bytes. The contents
  inventory excludes these controls. Refuse changed controls even when the
  executable bytes are unchanged. Engine `0d6fa26c` adds v2 durable receipts
  retaining these reviewed control digests and revalidating them during Restore
  and reconciliation. Qualify restart and changed-control refusal against exact
  saved digests. V1 receipts remain legacy product/inventory/lease evidence;
  expose that weaker scope explicitly before enabling UI recovery. Strict native
  compilation and companion law object compilation do not establish runtime
  durability, native/source correspondence or authenticated proofs.
- Integrate the bounded candidate façade with background dispatch, explicit
  overflow/refusal states and a paged accessible review list. Unknown age stays
  protected; only verified filesystem birthtime supplies retention evidence.
  A verified Published4 resolves its matching publication intent, while an
  unmatched intent stays protected. Failed/partial generations still need
  cleanup admission based on their creation evidence, without a fabricated
  product identity. Execute G02–G06 in the [targeted cleanup slices](generated-build-cleanup.md);
  producer verification, retained-lock admission and variant-aware receipts must
  land together before incomplete rows become movable.
  The owning scan worker and controller are now implemented (`ddf349a`,
  `0ae9584`): refresh queues a scan, frame polling drains it without waiting,
  and publication checks ticket, cancellation, workspace path and captured
  retention. Progress/refusal/overflow text is connected to Storage's status
  bar. The concrete consuming graph now compiles and links at the captured
  snapshot. Qualify its native publication and failure paths. The generation
  inspection screen has 16 rows per page, protection explanations, pointer/
  keyboard selection and paging/refresh/back controls; runtime acceptance remains
  open despite successful source and paging-law compilation.
  Native accessibility and explicit source-bound move confirmation are wired
  (`863be07`, `692360c`, `5e1b130`, `5cda1dd`). The controller rechecks the
  scan, selection, retention and workspace at confirmation and retains the owning
  reply even after cancellation. Complete native compile/link/package evidence
  now exists for the captured snapshot; later UI drift requires rebuilding before
  current runtime acceptance.
  Qualify result/recovery presentation and connected Restore flow, including
  implemented Unicode path inspection and eight-target focus traversal. See the
  [integration diagnostics](../acceptance/generation-controller-diagnostics-2026-10-07.md).
- Qualify the connected owning Restore job and recovery browser (`51c3cbc`,
  `1157dab`, `d1e4d35`). Cancellation or a
  stale ticket suppresses UI publication but must drain the reply and retain any
  unclosed native handle. Restore success requires committed restore, confirmed
  lock release and exact durable reconciliation; compilation of the worker and
  task instantiation does not qualify its runtime behavior.
- Qualify progress/result UI for the connected owning reviewed move job
  (`8492253`, `aa19a87`, `5cda1dd`). It captures inline native buffers,
  independently admits age against the captured retention, matches reviewed
  controls under retained locks, requires durable v2 intent evidence, closes
  ownership and reconciles before recoverable success. Worker, law and concrete
  result-consumer objects compile; no native execution or authenticated proof
  qualification is established. A stale/cancelled reply must retain any new
  operation identity and recovery evidence before it is discarded, as well as
  draining any remaining native handle. An uncertain move can become recoverable
  only after exact durable quarantine reconciliation and confirmed lock release.
  An unresolved retained reply blocks subsequent moves until exact recovery
  acknowledgment. Outcome-specific copy and
  bounded in-memory identity retention are implemented (`5882dbe`, `021a276`,
  `80eb81c`, `5e2af2e`, `d644106`, `13f1245`). Recording uses owned root and
  operation bytes, detects exact duplicates and refuses capacity overflow;
  completion retains its reply if recording fails. Ledger browsing, earlier
  operation selection and background reconciliation are now connected.
  Qualify exact root/operation binding, stale replies, cancellation, capacity
  overflow and repeated moves. Qualify implemented exact resolution of retained
  replies; uncertain release continues to refuse acknowledgment. Exact Move/Restore Resolve Review source is connected to current
  reconciliation and retained ledger identity; qualify it before accepting
  repeated cleanup. Restore captures artifact/path before dispatch (`d274c70`)
  and requires a new review/confirmation after acknowledgment. Explicit
  remaining-handle Retry Release controls are implemented
  (`f06a8b7`), with whole-reply ownership transfer and admission laws. Qualify
  Busy/stale/uncertain native results, retained metadata, retry progress and
  cancellation; establish exact reconciliation before disposing of the reply or
  permitting another mutation. Generation job starts now serialize
  inventory, discovery, reconciliation, move and Restore (`330e1c8`); qualify
  deferred requests and responsiveness under every overlapping user action.
  Keep ledger internals private; current compiler constructor/result repairs
  preserve that API and require current regression qualification. Restart receipt discovery is implemented as candidate
  enumeration with explicit unresolved pending metadata; qualify its native
  crash/lock/descriptor matrix and UI loading before closing restart recovery.
  See [discovery evidence and open acceptance](../acceptance/generation-recovery-discovery-2026-10-07.md).
- Qualify the corrected native reconciliation parent comparison before runtime acceptance:
  a transaction begun at quarantine has the managed items directory as its
  source parent, while the receipt records the original parent. Compare each
  descriptor with its corresponding identity, then bind and verify the original
  parent separately. Engine `453eda39` removes the unconditional comparison
  that rejected valid quarantine recovery and verifies its source parent against
  the retained items descriptor. Strict native compilation passes; the companion
  Elisa policy and five law declarations compile as an object. Native execution
  and proof authentication remain open. Cover both original and quarantine
  recovery locations, changed parents and reused names.
- Qualify generation recovery through this outcome matrix before exposing it:

  | Observed state | Required UI and action |
  | --- | --- |
  | Original present, quarantine absent | Report not moved only after exact identity checks; allow fresh review. |
  | Original absent, exact quarantine present | Show recoverable moved state after durable reconciliation; offer Restore. |
  | Original name reused | Keep recorded item identifiable; refuse overwriting the new occupant. |
  | Both locations present, neither present or identity changed | Show unresolved/conflict with inspectable locations; protect both. |
  | Intent exists after restart | Reconcile descriptors and journal before enabling retry or Restore. |
  | Move succeeded but journal/parent flush failed | Show uncertain recovery; retain evidence and stop the batch. |
  | Lease/global lock release uncertain | Refuse further mutation until admission is safely recovered. |

- Complete a keyboard and VoiceOver journey through generation selection,
  review, confirmation, progress, partial result, restart reconciliation and
  Restore. Return focus to the triggering control or retained row. Disable
  repeated activation while a transaction is active, announce updated totals,
  and provide containing-folder access for unresolved recovery. Existing
  regular-file Trash acceptance does not qualify directory cleanup.

**Finish evidence:** source hashes unchanged, output reopens as reviewed, reports
bind to that output, interrupted states reconcile, and restore cannot overwrite
work. Follow the detailed M1/M6 durability and native failure criteria.

## 3. Qualify scale, professional repeat work and release

### P01 — Density, responsiveness and capacity

**Depends on:** usable current app and the reference hardware/corpus decision.

Measure cold and warm paths separately: input handling, evaluation, drawing,
publication, memory and cancellation. Report p95/p99 and worst cases; averages
cannot hide stalls. Exercise maximum stack/contact/history sizes, dense issues,
long paths and large semantic trees at supported window sizes/scales.
Capacity refusal must precede mutation and explain recovery. Keep the 600-line,
constant-representation and literal-push gates running throughout implementation.

### P02 — Recipes and reviewed batch production

**Priority:** P1; remains part of full-plan completion. **Depends on:** J04.

Wire captured preflight facts to native validators and the queue UI. Qualify
compatible rig/recipe reuse, duplicate destinations, individual failure,
draining cancellation, resume/retry and approval of the exact staged result.
Empty or partially failed queues cannot publish a complete production manifest.
Preserve valid completed outputs and approvals across other item failures.

### P03 — Packaging, documentation and user trials

**Depends on:** all applicable P0 evidence. Implementation may proceed earlier.

Verify Finder launch and file opening outside a developer shell, package identity,
licenses and provenance. Choose the distribution route explicitly. Update guides
from observed controls and failure paths. Run all four journeys with at least
five real intended users without coaching, recording uncertainty and recovery.
Fix lost-work and blocked-task failures first, then misleading results and friction.
Do not invent participants or count internal scripts as usability trials.

### R01 — Remaining M8 decisions

Retain every research candidate in M8. For each, name an observed corpus failure,
hypothesis, baseline, experiment cost and adopt/reject criterion before prototyping.
An adoption adds implementation, proofs and quality acceptance; a rejection needs
recorded evidence. A P0 release does not complete P1 workflows or these decisions.

## Work coordination and handoff

Keep source ownership explicit while agents work in shared checkouts. Parallelize
independent compiler, prover, product and evidence work; serialize edits to shared
interfaces. Commit small coherent changes and announce source freezes before
immutable generations are copied. Record active process handles and terminal
results; a stale lock or previous status is not evidence of a running build.
After a failed integrated run, prioritize its concrete diagnostic before opening
another unrelated source batch. External reviewer gates do not prevent independent
implementation, but remain visible until the required person supplies evidence.

For each active qualification record the owning task, source generation, command,
PID or session, log location and last observed state. Replace a running state with
its terminal exit and diagnostic when it ends. A compiler failure identifies the
failed declaration or lowering step and a reproducible input; an external blocker
identifies the missing decision and dependent work. Keep these distinct from
unqualified implementation. Resume independent work while a build runs, and state
the next concrete action after failure instead of reporting a generic stall.
