# Current delivery queue

[Roadmap](../../IMPLEMENTATION_PLAN.md) · [Shared acceptance](acceptance-and-dependencies.md)

This is the execution order for the remaining roadmap, not a replacement for
M0–M8. Source changes already in Git need qualification rather than another
implementation. An open acceptance item stays open until its evidence exists.
Reassess this queue after an integrated build, a discovered regression or a
completed user journey. Update outcomes from evidence, not elapsed effort.

## 1. Restore a usable, current qualification path

### Q01 — Current compiler and paired prover

**Priority:** P0; prerequisite for accepting every subsequent source slice.

Compiler `e34f2c0656aac1232ad72da6516c7eb89f866a47` has a fresh,
clean Stage1 product after preserving project repairs and fetching upstream.
It fixes the imported generic `view` collision that prevented Studio's nine
optional narrowing expressions from compiling. The complete app unit now
compiles. The full compile, native link, build seal/publication and app package
also completed at the captured snapshot with `STUDIO_SKIP_CHECKS=1`. The
full current check and runtime acceptance remain open. Retain the exact product and extra `scripts/platform.sh`
recipe-input hashes from [the source compile record](../acceptance/current-law-source-compile-2026-10-07.md).

The earlier prover/replay generation `953dac2d5fbf41af97a7a10f4f410dea`
was built against compiler `0fb79267` before subsequent prover commits. It is
comparison evidence. The current strict O2 pair, generation
`8a85f9729079469a980012854b4f63cd`, was built from proof HEAD
`828886b67c3c70939e9185a80668649d45163262` against compiler
`e34f2c0656aac1232ad72da6516c7eb89f866a47`. Pair integrity and
source/compiler/runtime freshness pass. The proof record gives exact source,
product and manifest hashes. Focused source correspondence remains partial,
with the portable replay trust record still reporting
`source_authenticated: false`; the full `scripts/check.sh` and runtime
acceptance remain open.

The native generation binding's arity mismatch was traced to the reserved
Elisa identifier `error`, which the extern parameter scanner omitted from its
arity count. Rename that source identifier without changing the positional C
ABI. That rename is committed and the reduced binding has no remaining arity
errors. The complete transaction adapter now compiles as an object with current
Stage1 `e34f2c`, including both evidence decoders. Integrate and qualify its
controller/native link closure; its adapter compilation does not establish UI
integration or native interaction acceptance.
Keep this separate from the resolved generic `view` collision.

Dependency freshness is still open. The selected UI has uncommitted source
changes that must be captured exactly before and after qualification. The
mocap engine now includes fetched main `55541b7b` at merge `dff5579b`,
with its provider additions preserved; a full Studio build against that merged
source passed. The bounded generation provider and its Elisa façade now compile,
and the native provider, creation scanner and bounded JSON scanner are registered
in the Studio build and source fingerprint (`b668720`). Qualify their complete
link/package closure and background controller integration. Compiler
provenance still needs `platform.sh` added to its recipe fingerprint; its exact
hash is already captured by the app input snapshot.

- Qualify borrow-region propagation through compiler/std callers, including
  explicit short-lived allocation refusal, distinct owners and retained scratch
  capacity. Do not relax lifetime validation to bootstrap the compiler.
- Qualify the proof snapshot's std paths against the validated runtime trust
  root. Keep runtime privileges restricted to individual selected std sources;
  verify whole-unit legacy bypasses refuse, including direct-product invocations.
- Before each qualification, fetch dependency upstreams and preserve project
  repairs. Rebuild changed compiler/runtime or proof sources as matched products;
  never carry a previous pair's freshness result across a source change.
- Retain immutable source/include manifests, native inputs, product hashes,
  terminal logs and pair authentication. Reject changed or mixed inputs.
- Compile the latest complete Studio and CLI graphs. Resolve frontend and
  backend failures before calling an app build usable.

**Finish evidence:** source-matched compiler provenance; authenticated current
prover/replay pair; complete graph compilation/linking; current `scripts/check.sh`
result with failures listed individually. Neither a seed nor a law object closes
this item. Keep native interaction and motion quality separately open.

### Q02 — Source authentication and critical laws

**Depends on:** Q01. Package/source correspondence work may proceed beforehand.

- Qualify exact expanded bytes, ordered imports and lexical declaration owners.
  Changed bytes, order, paths, duplicate names and unsupported scopes refuse
  authentication. Portable replay must remain labelled unauthenticated.
- Prioritize document preservation, candidate publication, history, source
  identity, export admission and storage mutation contracts before secondary
  convenience policies.
- For each law retain its exact declaration, preconditions, checked predicate,
  source identity and independent replay result. Test contradictory assertions
  as negative controls; never replace unknown results with compile counts.
- The current proof commit adds bounded struct-field projections,
  symbolic const-enum terms, source-owned immutable integer constants and
  checked guarded helper summaries. In the generation-policy graph, 89
  obligations produced 33 proven and 56 unproven. Exact-source correspondence
  checks `facts_valid` and `protection_reason`, leaves `eligible` unmatched on
  13 return ensures, and reports 19 unsupported functions. Coverage is partial
  and `source_authenticated` remains false. The creation-journal graph has 195
  obligations (53 proven, 142 unproven); its package is rejected as
  inadmissible. The proof record has exact source and product identities.
- Continue reducing connective/source admission gaps and fact growth. Extra
  enum disequality facts cannot substitute for the checked relation between a
  helper result and its inputs. Preserve fail-closed authentication and keep
  unresolved laws open; see [the exact qualification record](../proof-gaps/build-generation-policy-proof-20261007.md).

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
  Reject unknown descendants, linked entries, changed file contents, writable
  entries, replaced ancestors and mismatched artifact/build identities. Repeat
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
- Integrate the implemented native generation move/Restore/reconciliation
  adapter with the Elisa controller and review UI. Raw status/phase/location
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
  executable bytes are unchanged. Extend the durable receipt to retain these
  reviewed control digests and qualify restart reconciliation against them;
  the current v1 receipt retains product/inventory/lease evidence only.
- Integrate the bounded candidate façade with background dispatch, explicit
  overflow/refusal states and a paged accessible review list. Unknown age stays
  protected; only verified filesystem birthtime supplies retention evidence.
  A verified Published4 resolves its matching publication intent, while an
  unmatched intent stays protected. Failed/partial generations still need
  cleanup admission based on their creation evidence, without a fabricated
  product identity.
- Connect the compiled owning Restore job to the controller. Cancellation or a
  stale ticket suppresses UI publication but must drain the reply and retain any
  unclosed native handle. Restore success requires committed restore, confirmed
  lock release and exact durable reconciliation; compilation of the worker and
  task instantiation does not qualify its runtime behavior.
- Correct the native reconciliation parent comparison before runtime acceptance:
  a transaction begun at quarantine has the managed items directory as its
  source parent, while the receipt records the original parent. Compare each
  descriptor with its corresponding identity, then bind and verify the original
  parent separately. The current unconditional comparison rejects an otherwise
  valid quarantined artifact before that rebinding. Cover both original and
  quarantine recovery locations, changed parents and reused names.
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
