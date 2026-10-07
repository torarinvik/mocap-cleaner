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
- Resolve the existing unit mismatch: `src/physics/balance.elisa` and
  `src/physics/rig_physics.elisa` currently feed micrometres into proof-critical
  kernels, while the project convention requires lengths in 0.1 mm. Inventory
  all such kernels and their callers before changing scale. Introduce explicit
  conversion boundaries, including signed rounding, overflow admission and
  accumulated error bounds; convert constants, thresholds, contracts and laws
  together. Keep exported `_um` metrics explicitly converted to micrometres
  and match CLI/Studio results. Prove negative coordinates, sub-unit values,
  boundary values and round-trip error bounds. Requalify correction decisions
  around thresholds and document any intended precision change before rollout.
  Split dimension-specific conversions before migrating callers: `Limb::micro`
  currently converts both limb lengths for `Reach::limb_reach` and pole angles
  for `Hinge::unwrap_step`. `RigPhysics` also uses it for heights, horizontal
  coordinates, speeds, per-frame gravity, angular acceleration and quaternion
  angle gaps. A global multiplier change would corrupt angular quantities.
  Include Studio contact heights/speeds from `GlbTracks::to_fixed` in the caller
  inventory. Assign each conversion its physical dimension and time basis;
  preserve angular units while migrating lengths and length-derived quantities.
  Qualify and integrate the isolated `LengthUnits` integer boundary added in
  `dd3e296`: nearest rounding with signed half ties away from zero, explicit
  reverse overflow admission and full-i64 source coverage. Its law graph has
  compile evidence only. Discharge its laws and bind them to exact source before
  relying on the conversion; caller migration and decision requalification
  remain required.
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

## Scope and release decisions

P0/P1/P2 identify release order, not permission to discard requested work.
The complete roadmap still includes P1 production workflows and decisions on
every M8 research candidate. Each research item requires an evidence-backed
adopt/reject decision; adopting it creates implementation and qualification
criteria before changing defaults. A single-take release milestone is distinct
from completion of the entire implementation plan.
