# Acceptance, dependencies and unresolved decisions

[Roadmap index](../../IMPLEMENTATION_PLAN.md)

These requirements apply across milestones. Implementation, pure proof,
native qualification and user acceptance are separate evidence categories.
Complete all applicable categories before removing a task from this roadmap.

## Work items and evidence

- Give each implementation slice a stable ID, priority, concrete result,
  dependencies, source/proof touchpoints, failure behavior and acceptance cases.
  Split compound checkboxes when implementation and qualification differ.
- Record evidence in small documents under `docs/acceptance/`, linked from
  the [acceptance index](../acceptance/index.md). Put generated captures,
  traces, benchmark data and fixtures under
  `build/`; record regeneration commands and input hashes so disposable
  artifacts are reproducible. Keep every maintained evidence document within
  600 lines.
- Each record identifies repository/dependency revisions, compiler/prover
  provenance, fixture version/hash, platform, hardware, command or interaction
  sequence, expected result, observed result and outstanding failures.
- Identify the party that can provide each result: implementation/proof work,
  native interaction review, animator annotation or external participant trial.
  Missing human evidence remains open; never invent participants or feedback.
- Every named proof law must assert its intended predicate through `ensure` or
  an explicit assertion. A Boolean return without such an obligation is not
  evidence for the law's name. Review preconditions against valid and invalid
  domain examples; assertion presence alone is not sufficient. Audit helper
  functions separately and retain intended false/equivalence outcomes. See the
  [law assertion coverage audit](../proof-gaps/law-assertion-audit.md).
- Accept a proof result only with its contract coverage and certificate replay.
  A proof-count improvement alone does not establish native filesystem facts,
  motion quality or usable controls. Retain original regression expectations;
  unexplained changes require investigation, not a weaker baseline.
- Qualify a fixed source/dependency snapshot. If files change during a run,
  identify affected results and rerun them before claiming snapshot acceptance.
  A failed observation does not establish that a live app/job has stopped.
- Compiler freshness exceptions must follow the actual build input set.
  Excluding Go test-only edits must still refuse renames between implementation
  and test files, implementation deletions, module changes and relevant native
  inputs. Parse paths without losing quoting or rename identities. Failed
  source-status or input-inventory commands must refuse qualification rather
  than treating an empty result as a clean source tree. Retain embedded source
  revision checks and exact linked-product provenance alongside these checks.
- Remove completed implementation from active checklists; retain outstanding
  native, quality or usability acceptance explicitly. Preserve history in Git
  and evidence records rather than rebuilding shipped policies.

## Decisions that block dependent work

| ID | Decision/result required | Dependent work and acceptance |
| --- | --- | --- |
| D01 | Canonical workspace root and writable `build/` directory independent of process working directory. | Finder launch, sessions, recovery, Storage and export resolve the same root; cancellation/read-only/unavailable roots preserve the current document. |
| D02 | Source/animation/rig identity and compatible session/recipe schemas. | Rebind, profiles, job results and reports cannot reuse stale bone indices or analysis. Duplicate animation names have distinct identities. |
| D03 | Units, frame/time conventions and metric availability. | Inspectors, fixed-point conversion, retime, contact boundaries and reports agree; unknown units or zero samples cannot produce passing quality scores. |
| D04 | Worker ownership, immutable inputs and publication protocol. | Load, analysis, rebuild and export have independent cancel/stale-result cases; retained UI state never shares mutable worker buffers. |
| D05 | Corpus annotations, preservation thresholds and reference hardware. | Recommendations and performance gates use thresholds fixed before comparing candidate output; every failed case remains visible. |
| D06 | Export/report publication and interruption recovery. | A published GLB with a failed report is explicitly partial; restart/retry cannot overwrite it or evaluate a different revision silently. |
| D07 | Distribution route and external usability participants. | Package launch/signing and the five-person trial receive real evidence; implementation can proceed while these external decisions are pending. |

Resolve shared identity and ownership interfaces early with small prototypes.
M1 shell/lifecycle and M2 identity work can proceed together; neither should
wait for completion of the other's entire milestone. Begin M5 ownership work
before wiring expensive M3 evaluation. Single-export correctness does not
depend on completion of the P1 queue UI.

## Cross-cutting acceptance cases

The remaining physics conversion boundaries and migration order are inventoried
in [physics unit migration](physics-unit-migration.md). Complete producer,
inverse and report conversions together before qualifying changed decisions.

- Maintain a single command/control definition for labels, enablement and
  dispatch; handlers also enforce admission against current state. Pointer,
  keyboard, accessibility and CLI paths cannot bypass the same safety gate.
- Maintain a global semantic-node ID registry and validate complete parent,
  child and sibling chains, unique IDs, compatible actions and focus targets.
  Exercise the node/draw budgets at maximum supported density; never silently
  drop a primary control while leaving its hit target active.
- Specify internal versus displayed frame indexing, inclusive/exclusive ends,
  fractional-time rounding and source/output time domains at every conversion.
  Verify zero/one-frame clips, first/last frames, retime boundaries and undo.
- Record every distance/angle/time/weight unit and conversion, including
  fixed-point saturation/rounding. Distinguish declared units from inferred
  scale, and invalidate affected analysis when units/floor/rig settings change.
- Physics length sources now use 0.1 mm internally through explicit
  `PhysicsLengthBoundary` conversions; speed and gravity include their time
  basis, while angular acceleration and rotation drift remain microradians.
  `_um` report fields are explicitly converted at the CLI boundary, with
  accumulated overflow represented as unavailable. Source edits and updated
  proof sources are complete, but current compiler/prover qualification,
  fixed-corpus CLI/Studio decision comparison and native overlay review remain
  open. See [the physics unit migration record](physics-unit-migration.md) for
  the implementation inventory and exact remaining evidence. Preserve signed
  rounding, domain and overflow coverage while qualifying; do not treat source
  changes or compile output as proof discharge or acceptance evidence.
- For metrics distinguish measured pass, measured failure, unknown and
  inapplicable. Include sample counts, intervals and exclusion reasons. A zero
  sample count, NaN, missing contact labels or unsupported metric is not zero
  error. Automatic acceptance requires applicable measured preservation gates;
  manual review must disclose unavailable evidence without promising a pass.
- Restore focus to the invoking control after a dialog, or a documented
  fallback when that control disappeared. Cover nested modals, hidden selected
  rows, focus loss, invalid drafts and Escape without committing edits.
- Capture diagnosed native failures and retry on an identified build/fixture.
  Screenshots, an issued click and process liveness alone cannot demonstrate
  completed input routing or accessibility interaction.

## Paired measurements and aggregate reports

Apply these criteria to diagnosis, comparison, CLI output, export reports and
batch summaries. Include them in J02/J03/J04 acceptance evidence.

- A before/after comparison uses the same metric definition, physical units,
  sampling domain and captured source/settings identity. Record sample counts
  and exclusions for both sides. Different domains require an explicit aligned
  comparison; silently comparing differently filtered totals is invalid.
- Represent availability at the same granularity as the measurement. If one
  shared flag governs a pair, refusal or overflow clears both values atomically.
  Independent flags must be checked together before calculating improvement.
  An unavailable value cannot survive as an apparently measured zero or number.
- Check accumulation and report conversion bounds before arithmetic. Cover
  overflow in either member after the other already contains a positive value,
  merging an unavailable contributor, and repeated merges after refusal. Retain
  the reason and avoid percentages when the baseline is zero or unavailable.
- Batch summaries expose measured, failed, unavailable and inapplicable counts
  and the aggregation rule. A subtotal over available clips is labelled partial;
  omitted clips remain visible with reasons. An aggregate cannot certify a
  failed or unevaluated individual preservation gate.
- Render absent measurements as readable states in Studio and CLI text, and as
  explicit availability/reason fields with absent or null numbers in structured
  reports. Verify report readers preserve those states through round trips.
  Presentation placeholders cannot become numeric input to quality decisions.

**Finish evidence:** authenticated arithmetic/availability laws, matching
CLI/Studio/report outcomes for a frozen fixture, mixed-availability batch cases,
and review of the displayed reason and available recovery action.

## Interaction and recovery acceptance for every slice

Apply this checklist to each new or changed user-facing workflow, using the same
captured document identity across its pointer, keyboard and accessibility paths.

- Define entry, loading, ready, empty, unavailable, failed, cancelled and success
  states where applicable. Each state names what happened, which result remains
  usable and the next available action. Distinguish a preserved previous result
  from a newly completed result; never rely on color or a transient toast alone.
- Put the scope and consequence beside actions that change edits, publish files
  or move generated artifacts. Display the selected take, range, destination and
  affected item count before confirmation. Refresh invalidated reviews before
  allowing confirmation; repeated activation cannot duplicate the operation.
- Keep ordinary successful actions direct. Use confirmation when there is a
  concrete replacement, loss or publication consequence, with explicit action
  labels and a safe cancellation path. An error should offer a relevant recovery
  action without requiring the user to reconstruct their selection or draft.
- Preserve entered values and context after recoverable failure. Specify what
  Retry captures, whether a chooser can change the destination, and which
  identity/settings invalidate retry. Cancellation must reach a terminal state
  with an accurate account of any files or edits already committed.
- Review long labels, paths, dense lists and minimum-window layouts. Primary
  actions, error details and cancellation stay reachable; full values have an
  inspectable alternative when abbreviated. Verify focus return and announced
  state changes through the actual native window.

**Finish evidence:** a recorded state-transition walkthrough, refusal/retry cases,
pointer and keyboard completion, accessibility names/actions/focus, and unchanged
source/document evidence after cancellation or failed mutation. A screenshot or
pure admission law alone does not close this checklist.

## Scope and release decisions

P0/P1/P2 identify release order, not permission to discard requested work.
The complete roadmap still includes P1 production workflows and decisions on
every M8 research candidate. Each research item requires an evidence-backed
adopt/reject decision; adopting it creates implementation and qualification
criteria before changing defaults. A single-take release milestone is distinct
from completion of the entire implementation plan.
