# Current delivery queue: highest return first

[Roadmap](../../IMPLEMENTATION_PLAN.md) · [Shared acceptance](acceptance-and-dependencies.md)

Updated 2026-10-08. This is the execution order for the entire remaining M0–M8
roadmap. Priority changes do not remove requirements. Detailed milestone and
acceptance documents remain authoritative for each slice. Completed source
needs qualification, not another implementation. Historical binaries and proof
reports remain comparison evidence.

## Selection rule

Choose work that removes a demonstrated blocker, protects user data, or completes
a usable end-to-end workflow. Prefer a small integrated fix over a new feature
that cannot yet run. Rank by user impact, dependency unlocks, recurrence and
implementation/qualification cost. Reassess after an integrated build or a
completed journey; do not invent numeric ROI scores without measured inputs.

Keep one primary product blocker active. Dependency owners can repair their
existing compiler, prover and native slices alongside it. Each handoff identifies
an exact source/product tuple, failing fixture, next action and finish evidence.
Serialize heavy compiler jobs and monitor aggregate descendant memory. Avoid
unrelated style sweeps, duplicate policy implementations and new algorithms
until the first usable journey passes.

## Immediate execution contract

The next deliverable is a **current runnable Studio build**, followed by the
reported FBX/Character redraw reproduction. Work backwards from that result:

1. Use the latest frozen full-graph diagnostics to fix remaining production
   owners in descending dependency impact. Grant migrations must remove an
   observed diagnostic or complete a required access boundary; avoid unrelated
   repository-wide refactoring while the build is blocked.
2. Capture the full graph again after each coherent repair batch. Separate
   semantic permission failures from native emission failures; retain the exact
   source/product tuple and failed diagnostics so the next action is concrete.
3. Once semantic checking passes, repair the first remaining native emission
   blocker, build/package, and run the actual reported import/toggle journey.
   Do not count more policy modules or isolated smoke passes as this delivery.
4. Keep critical proof repair on its existing parallel dependency track. Gate
   the affected data-mutating operation on its required evidence; independent
   read-only import, display and diagnostic work can continue.

**Work in progress limit:** one integrated product slice plus its necessary
compiler/prover/native dependency repairs. Every new task names the user-visible
result or observed blocker it unlocks and the smallest finish check. Re-rank
when a current build passes or a native journey exposes a new failure.

**Defer expansion:** new cleanup algorithms, extra batch options, research,
broad visual polish and speculative abstractions wait until the import,
cleanup, undo and single-export journey works. Mandatory size, visibility,
effect tracking and source-preservation rules apply to every touched file.

## Next three deliveries

| Order | User outcome | Smallest next action | Stop condition |
| --- | --- | --- | --- |
| 1 | Studio launches on current dependencies | Qualify the global-checker repair, capture the full graph, then repair the local/global worker-result shadowing if still present | Current app builds/packages, then the reported FBX/toggle journey runs |
| 2 | Opening an FBX succeeds or explains how to recover | Exercise the reported asset and workspace chooser on that app; fix the first observed import/display failure | Open, cancel, retry and Character/Skeleton actions work with readable feedback and unchanged source |
| 3 | A user produces a useful reviewed result | Finish one existing finding-to-preview-to-undo-to-export journey | Export reopens with the reviewed motion and required safety evidence |

Treat each stop condition as a delivery gate, not permission to stop investigating
an observed defect. Recovery-location integration and broader storage controls
follow the usable single-take journey unless they directly block it or protect
work at risk. Proof repairs prioritize the contracts required by these deliveries.

## Deliver the smallest useful release slice

The first product checkpoint is one source-preserving FBX import, visible animated
Character/Skeleton review, one existing cleanup preview with apply/cancel and
undo, and one reviewed GLB export that reopens correctly. Complete this slice
before broadening supported tools or production options. A checkpoint is useful
progress; it does not close the remaining roadmap.

For every delivery, record:

- **User outcome:** the concrete action a user can now complete.
- **Observed blocker:** retained failure and owning module/dependency, if any.
- **Next change:** the smallest source repair that advances the outcome.
- **Acceptance:** current native journey plus contracts/proofs for the affected
  transition; passing isolated controls alone do not close the delivery.
- **Deferred work:** what remains and the gate that will make it worth resuming.

Proof and compiler work serve the active delivery. Prefer a shared root-cause
repair when it removes several observed failures, but keep its regression scope
explicit. Stop repeating diagnostics when unchanged inputs yield the same result;
move to a repair or a smaller reproducer. Reassess after every delivery gate or
new user-visible failure, rather than after an arbitrary number of commits.

## Work to pause while the app cannot run

- Additional standalone policy/decoder features without a demonstrated build,
  data-preservation or first-journey dependency.
- Repository-wide effect/style/representation sweeps beyond touched production
  paths and mandatory rules.
- Batch expansion, new repair algorithms, broad visual redesign and M8 research.
- Repeated full builds with unchanged inputs, duplicate passing reducers, and
  proof census work that prevents the critical compiler repair from running.

Retain these requirements in their milestone documents. Resume them after the
relevant gate passes; do not mistake accumulated fixtures or proof counts for
user-visible delivery. Qualify already-written code before extending its surface.

## 1. Q01 + J01: produce a current build and fix the reported redraw crash

**Priority:** P0. **Return:** restores the user's ability to use the product and
unlocks every native UI acceptance check.

1. Use the qualified grouped-grant and strict Unsafe repair; retain exact-member
   refusal controls when integrating it into Studio. Finish mandatory global permission migration across Studio and included UI
   dependencies. Read-only owners use `Global.Read`; mutation propagates write
   authority. Use grouped syntax where appropriate. Preserve unsafe tracking
   with `can`; no blanket `trusted`, permissive mode or disabled checker.
2. Fetch current dependencies while preserving project repairs. Build and verify
   source/product/runtime/link correspondence. Freeze the actual input closure
   for qualification; changed inputs invalidate the attempt.
3. On that tuple, reduce and repair any remaining native emission failures,
   currently the specialized generic worker-result reads in the full app graph.
   Preserve privacy, affine ownership and caller-owned allocation lifetimes.
4. Build/package Studio, identify the exact executable, then reproduce the
   reported FBX/redraw failure. The historical `14bdc130` binary crashed after
   importing 337 frames; it cannot qualify current source. Inspect the allocation
   and ownership boundary before choosing a fix.
5. Qualify FBX open, Character/Skeleton switching, framing/orbit/zoom, playback,
   repeated redraws, edits, replacement, cancellation, close and restart on the
   reported asset and bounded controls. Preserve the original file bytes.

**Finish evidence:** current sealed build; exact crash reproduction and repair
record; actual native interaction on the repaired binary; focused lifetime
controls; source hash unchanged; no stale candidate publication. A seed, clean
single-file diagnostic, screenshot or live process is insufficient.

**Current status:** the prior matched `85eef9ff` closure passed semantic
checking and retained five specialized worker-result LLVM failures. Diagnostics
show correct generic/local/result ownership; static tracing identified a local
`slot` reference falling through to the unrelated `StudioReportText.slot`
global lookup. Validate and repair that shadowing path with a regression.

The refreshed compiler repair branch includes upstream `d05f35d4`. Its current
Studio capture (`build/studio-build.index-path-probe-d05-20261008/`) stops before
backend emission with 862 global-grant diagnostic lines. The new checker has demonstrated pattern-binder false positives and uses
name-only callee effect lookup that risks cross-module effect leakage. Qualify
its enforcement mode, binder scopes and grouped callback grants, then resolve
effect summaries by callee owner/declaration identity, including overloads and
transitive callbacks. Preserve genuine direct/transitive Global.Read/Write refusals. Genuine entry-point
and callback effect rows have been added; the revised source needs a fresh capture.
Selected engine `b8dd8add` now validates mutable mesh shapes and indices; actual
Studio redraw remains unqualified. Project-wide strict Unsafe acceptance is still
pending. No current replacement app or crash repair is accepted.
See [compiler qualification](compiler-qualification.md),
[responsiveness](m5-responsiveness.md) and [proof gaps](../proof-gaps.md).

## 2. J01: make open/import failure and workspace setup self-explanatory

**Priority:** P0. **Depends on:** a runnable current build.
**Return:** removes the confusion demonstrated in the user's screenshots.

- Open FBX directly through the ordinary Open action. If a workspace is needed,
  offer a visible chooser and explain the derived-file location; continue the
  retained request automatically when ready. Cancel preserves the current take.
- Present a persistent, readable failure summary with Details and a relevant
  Retry/Choose another file action. Expose complete text to accessibility.
- Keep filenames, status and primary controls usable at minimum window size;
  cover long paths, enlarged text, scale changes and repeated failures.
- Disclose when Character view is unavailable and how to obtain a usable mesh.
  Toggle state and the rendered view must agree through pointer, keyboard and
  accessibility actions.
- Qualify existing source changes before adding more status policies or wrappers.

**Finish evidence:** recorded first-use open/import journey, unavailable workspace
and malformed-input recovery, loaded-take refusal, focus restoration, matching
visible/accessible feedback, and unchanged document/source on failure.
See [M1](m1-workspace.md) and [shared interaction acceptance](acceptance-and-dependencies.md).

## 3. Q02: gate the active delivery with its safety-critical proofs

**Priority:** P0 for publication, ownership and data-preservation contracts.
**Return:** gives credible guarantees for the transitions most costly to get wrong.

- For each active delivery, select its blocking obligations before launching a
  broader proof census. Proof counts are evidence, not a prioritization target.
- Prioritize source identity, worker ownership, cancellation/stale publication,
  transactional history, FFI admission, export publication and storage mutation.
- Qualify the actual production handoff: native status alone must not be copied
  into several booleans and presented as independent staging evidence.
- Repair exact lexical owner/type/constant provenance and real functional theorem
  production. Resource-safety replay cannot stand in for an ensure theorem.
- Model short-circuit helper contracts under their actual branch guard. Retain
  branch-specific precondition obligations; never introduce an unguarded helper
  equality from a call that may not execute.
- Authenticate exact source/expanded import closure, then independently replay.
  Retain wrong-owner, reordered-argument, changed-source, false-assertion,
  malformed-owner and missing-precondition refusal controls.
- Rebuild matched products after relevant repairs; qualify cache reuse by each
  product's actual input identity. Report compile, declaration proof, replay and
  source correspondence separately.

**Finish evidence:** intended critical predicates authenticated and replayed on
current source, with meaningful negatives and production/native binding evidence.
Unresolved obligations remain explicit gaps. Do not weaken contracts to obtain
passing counts. Secondary convenience-law gaps follow the critical path rather
than monopolizing the first usable-build repair.

## 4. J02 + J03: finish one inspect–preview–apply–undo–export journey

**Priority:** P0. **Depends on:** current build and required safety evidence for
the affected transitions.
**Return:** demonstrates useful cleanup rather than a collection of controls.

Use one labelled noise fixture and one contact fixture. Select a finding without
editing, jump to its frame/joint, explain scope and trade-offs, preview adjacent
motion/source/result, apply once or cancel, undo/redo, save/reopen, export/reopen.

- Keep pending drafts distinct from committed history and last-valid results.
  Failure/stale work cannot change history or claim a draft was saved/exported.
- Keep units, sample domains, time/frame indexing and source/settings identity
  consistent across Studio, CLI and reports. Unknown/overflow/zero-sample metrics
  remain unavailable rather than apparently successful zeros.
- Finish range, anchor and parameter inspection and keyboard/accessibility
  alternatives for exposed tools before adding another cleanup algorithm.
- Use preservation thresholds fixed before candidate comparison. Intentional
  fast movement needs labels/evidence rather than being assumed to be noise.

**Finish evidence:** complete native journeys; current/candidate identity parity;
quality/preservation gates; refusal/cancellation; meaningful history; session and
export round-trip parity. See [M2–M3](m2-m3-diagnosis-review.md),
[M4](m4-contact-repair.md) and [physics migration](physics-unit-migration.md).

## 5. J04: reliable single export and recoverable cleanup

**Priority:** P0. **Return:** protects user work and makes generated storage manageable.

- Complete captured-result GLB/report staging, partial outcomes and retry.
  Preserve occupied outputs and sources; restart cannot silently publish a
  different revision. Distinguish integrity, reviewed motion and durability.
- After single export works, finish Storage review/move/receipt/restore and
  generated-build cleanup with
  exact retained identity, active-product leases, durable journals and conflict
  refresh. Quarantine moves are recoverable storage, not claimed freed space.
- Integrate typed reconciliation identity and the read-only recovery-location
  observer. Observe under descriptor locks/rechecks, return no reveal path on
  uncertainty, and reobserve exact binding before reveal. Observation alone
  never grants Restore or mutation authority.
- Cover source-path/identity substitution, stale reviews, active builds/apps,
  uncertain lock release, torn receipts, interruption and restart at every
  relevant publication/move stage. Preserve required diagnostic evidence.
- Show selected scope, destinations and consequences before mutation; provide
  understandable Restore/Retry/reveal choices and retain recoverable failures.

**Finish evidence:** one native export/reopen/recovery journey and one native
cleanup/restore/restart journey, including injected failures, exact ABI and
identity controls, proofs and source preservation. Existing pure policies or
native helper tests do not qualify the complete controller/UI.
See [generated cleanup slices](generated-build-cleanup.md) and [M6](m6-export-batch.md).

## 6. P01: qualify responsiveness and professional interaction

**Priority:** P1; regressions affecting steps 1–5 remain P0.

Measure long takes and supported dense/max-capacity layouts on fixed reference
hardware. Keep cancellation, progress, draft visibility and last-valid preview
responsive. Qualify focus, semantic IDs/actions, minimum windows, text density,
capacity refusals, process lifetime and aggregate memory. Keep the intermittent
renderer memory gate open until the original threshold passes repeatably; stable
sampled heap/GPU counters alone do not explain retained process growth.

**Finish evidence:** repeatable timing/memory records and actual pointer,
keyboard/accessibility completion at supported limits. See [M5](m5-responsiveness.md).

## 7. P02 + P03: repeat work, packaging and release

**Priority:** P1 after the single-take journey.

Finish compatible recipes, reviewed batch production, partial/cancelled outcomes
and honest availability summaries. Qualify installation/Finder/copied-bundle
launch, signing/distribution, clear first-use documentation and real user trials.
External distribution/participant decisions remain explicit dependencies.

**Finish evidence:** native repeat-work journeys, source/report identity parity,
release package and complete M7 acceptance. See [M6](m6-export-batch.md) and
[M7](m7-release.md). A single-take release is not completion of the entire plan.

## 8. R01: remaining M8 decisions

**Priority:** P2; preserve all requested research candidates.

Evaluate against labelled baselines, preservation gates and measured runtime.
Record an evidence-backed adopt/reject decision for every candidate; adopted
work receives implementation, proof, UX and qualification criteria before it
changes defaults. See [M8](m8-research-and-order.md).

## Evidence and handoff discipline

Commit small source/proof improvements; combine documentation changes with a
source commit. Keep failed attempts and unresolved acceptance visible. Every
slice needs its actual compiler/prover/native/UI evidence at the appropriate
scope. Reassess this order when a blocker is removed or evidence changes; keep
all detailed requirements until proven complete.
