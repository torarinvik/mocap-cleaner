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

### Active blocker and exit gates

The retained crash report is from project revision `31459ca3`, with executable
SHA-256 `14bdc1305cdcb833eb2b65f44460cef69be8655a019a8f41929821c3b257705c`.
It has no recorded frame position. It predates the later launched package at
`e3698f7b`; that package is itself one commit behind the current checkout at
`69d28c69`. The crash's machine code maps to `StudioScene.build_with`, which is a
lead for reproduction, not proof of a current-source defect.

The latest available launched package is
`build/studio-package.0IFvJH/MocapStudio.app` (package generation
`studio-package.0IFvJH`, build generation `studio-build.NitjDS`, source revision
`e3698f7b`, executable SHA-256
`fd18a185a409af6cdb3cb516489ae237bf4521ed53d72712e20f7318e333bcad`). Its build
record notes a dirty compiler worktree, so it is not sufficient to qualify the
current dependency sources. A rebuild from the current mocap-cleaner checkout
stopped during semantic preflight at `build/studio-build.biCHfz/semantic.log`;
the diagnostics include same-name global-effect false positives and a UI dialog
result-region ownership error. That log contains 71 engine Global-grant
diagnostics across 12 files; classify them only after owner-aware effect matching
is qualified. The owner-aware compiler repair passed Stage0 semantic preflight,
and its focused same-leaf controls report no permissions for the unrelated key
intent and mesh-toggle callees. Its first Stage1 seed did not complete: runtime
compilation then exposed missing Global effects in numeric `Str.__cast__`
scratch-arena overloads. The two controls used a diagnostic compiler product and
a previously built reporter runtime, so they do not qualify the compiler or
Studio. Repair only the actual scratch-arena overloads and re-run Stage1 seed,
runtime build, and current Studio preflight with provenance.

1. **Build and verify the current FBX journey.** Use the current compiler,
proof assistant, UI and engine sources, and seal their exact revisions and
products. Then load the unchanged 337-frame FBX, test playback around frame 202,
Character/Skeleton switching, framing/orbit/zoom, repeated redraw, workspace
setup, cancellation, retry and malformed-input recovery. Preserve and recheck
the source digest (`50048a8a08f307d378e83d976462addcac62b5529bf60ae690da200d9d9f4485`).
2. **Deliver one useful cleaned result.** No current proof/replay pair is
qualified against current proof sources. After its source/product freshness
check passes and the FBX journey completes, inspect one finding, preview it,
apply/cancel, undo, export and reopen the GLB with source correspondence and
independent proof replay. Fix only evidence gaps that block this transition.
3. **Qualify recovery and publication safety.** Verify interruption recovery and
stale-publication refusal on the same current source/product tuple before release.

Keep proof repairs limited to obligations blocking these transitions. The prover
allocation regression warrants a root-cause repair because it blocks required
evidence; judge it against the original workload and resource limit, not a smaller
passing substitute. Recovery work becomes immediate if user work is at risk.

For each active task, record its owning module, observed failure, next source
change and exit gate. Stop or defer work that cannot name which gate it unlocks.
After a gate passes, select the next highest-impact observed failure; do not
restart completed implementation or expand the feature surface by default.

**Work in progress limit:** one integrated product slice plus its necessary
compiler/prover/native dependency repairs. Every new task names the user-visible
result or observed blocker it unlocks and the smallest finish check. Re-rank
when a current build passes or a native journey exposes a new failure.

**Defer expansion:** new cleanup algorithms, extra batch options, research,
broad visual polish and speculative abstractions wait until the import,
cleanup, undo and single-export journey works. Mandatory size, visibility,
effect tracking and source-preservation rules apply to every touched file.

## Highest ROI task selection

The following order governs task selection within the detailed queue:

| Rank | Task | Why it earns the next slot | Deliverable |
| --- | --- | --- | --- |
| 1 | Qualify the reported FBX first-use journey on current sources | Latest source is not packaged; historical crash evidence predates the last launched build | User's unchanged FBX opens, plays through the reported region, is reviewable, and gives clear cancel/retry/refusal feedback |
| 2 | Complete one cleanup through undo and export/reopen | Turns the repaired import path into a useful result | Reviewed motion exports and reopens with matching identity and proof replay |
| 3 | Close recovery and publication safety gaps | Protects work after the first result flow is real | Recovery and stale-result controls pass on the same current product |
| 4 | Measure the largest observed interaction delay | Improves everyday use after correctness | Before/after timing and memory on the same workload |

Safety-critical proofs, FFI checks and negative controls travel with each task;
they are part of its finish gate. Avoid an independent evidence backlog that
leaves the shipped transition unverified. Broader storage cleanup, batch,
algorithms and polish retain their detailed requirements but wait for their
activation gates.

**Decision checkpoint:** after each delivery, record what a user can now do,
which observed failure remains, and the smallest next change. Prefer fixing a
shared cause over adding another policy layer. If investigation is repeating
unchanged evidence, change the hypothesis or integrate the existing repair.
Do not spend the next slot on a roadmap rewrite, an unrelated abstraction or a
new tool while a higher-ranked user journey remains blocked.

## Next three deliveries

| Order | User outcome | Smallest next action | Stop condition |
| --- | --- | --- | --- |
| 1 | The reported FBX journey is fully reviewable on current sources | Qualify a freshly built package, then test playback near frame 202, framing/orbit/zoom, repeated redraw, workspace setup, malformed-input details, cancel and retry | Character/Skeleton and playback work; failure/cancel paths are clear; source bytes stay unchanged |
| 2 | A user produces a useful reviewed result | Complete one existing finding-to-preview-to-undo-to-export journey | Export reopens with the reviewed motion and required safety evidence |
| 3 | Work survives interruption and publication races | Exercise recovery and stale-result refusal against the same sealed product | Recovery restores the intended result and stale candidates cannot replace it |

Treat each stop condition as a delivery gate, not permission to stop investigating
an observed defect. Recovery-location integration and broader storage controls
follow the usable single-take journey unless they directly block it or protect
work at risk. Proof repairs prioritize the contracts required by these deliveries.

## Allocation and activation gates

Use these gates to keep effort directed at usable results:

| Work | Do now when | Resume broader work when |
| --- | --- | --- |
| Compiler and dependency repair | It prevents the current Studio build or required proof execution | The integrated current tuple passes and exposes the next actual failure |
| Proof repair | It blocks ownership, source preservation, history or publication in the active journey | Those critical obligations authenticate and replay under the original workload limits |
| UI and ease of use | It prevents opening, understanding a failure, viewing, cancelling or completing the first cleanup | The first native journey works; then address measured usability problems |
| Storage and recovery | Existing user work or required build evidence is at risk | Single export/reopen works; then complete cleanup/restore/restart |
| Performance | The active journey crashes, stalls or exceeds its existing resource gate | The original gate passes repeatably; then measure supported large takes |
| New algorithms, batch and research | An existing tool cannot deliver the first useful result and evidence identifies the missing capability | Single-take acceptance passes and a measured need justifies expansion |

Prefer one shared root-cause fix to several compensating wrappers. Run the
smallest control that distinguishes the suspected cause, then integrate when
inputs change. Do not repeat passing reducers or unchanged full builds. Keep
completed implementation in Git and pending qualification in its acceptance
record; avoid rebuilding a feature merely because native evidence is missing.

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

## Work to defer until the first useful result passes

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

## 1. Q01 + J01: finish native FBX review and recovery

**Priority:** P0. **Return:** restores the user's ability to use the product and
unlocks every native UI acceptance check.

The shared-sample-clock engine repair is committed as `1e98f075`. An earlier
bounded bridge test preserved the user's FBX digest, and earlier runtime checks
reported import, playback and `M` view switching on a prior package. The latest
retained crash report instead belongs to `31459ca3`; the later launched package
is `e3698f7b`, and current source is `69d28c69`. Current-source build qualification
is the active blocker. Do not infer that a later build fixes the reported playback
failure until that exact package is tested through frame ~202.

**Remaining finish evidence:** build from qualified current dependencies; test
frame ~202 and the complete import/recovery journey; keep source digest unchanged;
record visible and accessible recovery feedback. After this gate, complete one
cleanup through preview, apply/cancel, undo and export/reopen. Safety proofs and
FFI negative controls remain part of each affected transition.
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
