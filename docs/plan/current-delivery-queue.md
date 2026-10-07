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

Compiler `9667344c` now has matched Stage1/runtime products. Prover/replay
generation `ef1317585270400a8aa51deeb92ed517` passed pair integrity and current
dependency freshness checks. These establish the tools available for the next
qualification, not application behavior or law truth. Complete application
compilation/linking and the current full check remain open.

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
- Repair current struct/const-enum correspondence refusal and control-flow fact
  snapshot growth. The generation cleanup graph has 89 obligations, only 33
  proven and replayed, and no authenticated source obligations. Preserve its
  safety contracts and fail-closed authentication while fixing these gaps;
  see [the exact qualification record](../proof-gaps/build-generation-policy-proof-20261007.md).

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

The current suggestion adapter also needs explicit admission of computed
boundary/velocity distances before integer conversion. Finite input coordinates
alone do not establish a finite subtraction, norm or rate-scaled distance.
Reject nonfinite or out-of-domain computed values as unavailable before casting;
retain the candidate and explain the missing preservation evidence. Apply exact
current/candidate sampling-domain admission to contact, joint and velocity
comparisons as well as balance. Equal array lengths alone do not establish
matching frame times. Qualify overflow, equal-length different-time and ordinary
aligned cases without changing the preservation tolerances.

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
- Implement recoverable directory moves and receipts before exposing generation
  deletion. Existing regular-file Trash support does not qualify directory
  cleanup. Restore must refuse destination collisions and preserve recovery
  evidence when durability or lock release is uncertain.

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
