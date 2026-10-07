# M4: contact cleanup and precise repair

[Roadmap index](../../IMPLEMENTATION_PLAN.md)

## 9. M4 — Better contact cleanup and precise local repair

### 9.1 Contact editor

- [ ] Qualify the shipped endpoint range overlay and cancellation on screen:
      pointer movement updates the proposed interval, Escape/focus loss leaves
      saved state untouched, release creates one history entry and unchanged
      ranges create none. Validate capacity-refusal feedback, minimum-window
      handles and long takes. Qualify the contextual pose candidate against the
      exact stack that release commits, including take/document/history/frame
      changes during dragging. A pending or failed candidate must leave the
      current result visible and clearly identified. Throttling evaluation
      starts does not establish an update-latency bound: show pending work
      honestly and complete the M5 worker/supersession integration before
      accepting long-clip responsiveness. Approximate previews require explicit
      limits and comparison against release evaluation. See
      `docs/studio-contact-preview.md` for implementation/proof evidence.
- [ ] Add timeline zoom/pan, fitted range, visible row labels and draggable
      handles with usable hit targets. Visually verify the shipped 1-based
      endpoint fields and keyboard nudges on valid takes, including focus,
      invalid drafts, clip boundaries, long clips and the minimum window size.
      Qualify existing endpoint fields/buttons through native accessibility;
      implement semantic row/frame selection where still missing. Cover first,
      last, one-frame and 10,000,000-frame editing boundaries, plus refusal at
      the 32-contact-edit capacity with the draft and history preserved.
- [ ] Show automatic versus edited intervals, lock/pivot choice, anchor point,
      target surface, blend-in/out and confidence. Users can revert an interval
      without deleting other contact edits.
- [ ] Add anchor visualization and explicit anchor selection. For wall/rope
      hand contacts, support a user-defined stationary target/plane before any
      automatic inference; moving targets are a separate P2 capability.
- [ ] Warn about overlapping/incompatible pins, unreachable anchors and missing
      chains. Show the chosen compromise instead of implying an exact solve.
- [ ] Expose worst per-frame slide/penetration and transition knee/elbow jumps
      alongside totals. Jump to each metric's actual peak independently.
- [ ] Tighten foot transition quality on the known difficult boxing cases.
      Compare soft reach, adaptive release and blend policies against source
      and existing output; choose thresholds per fixture before tuning.
- [ ] Preserve deliberate toe/heel pivots, foot rolls and intentional slides.
      Separate position lock, heading stabilization and vertical settling so
      users can choose the intended constraint.

### 9.2 Existing advanced tools in the studio

- [ ] Expose existing pins through an inspector: effector, anchor, range,
      blend, enable and reach/error readout. Explain the current head-pin
      positional limitation; never label a nonzero error as exact.
- [ ] Expose existing additive/keyed offsets and correction layers with a
      visible key list, numeric transform editor, local/world-space labels,
      fades, enable/delete and timeline markers.
- [ ] Replace the hard-coded gizmo correction fade with editable defaults
      and per-correction scope. Support snap/nudge and constrained axes only
      where engine semantics are defined.
- [ ] Make preview and release evaluation agree; mark approximate previews
      clearly when full-chain constraints cannot be evaluated interactively.
      Provide Cancel and preserve selection through undo/redo.
- [ ] Expose existing pole/twist/pelvis controls with chain visualization and
      joint motion feedback. Verify roll-bone mapping before redistribution.
- [ ] Complete the existing retime inspector: selected source/output
      intervals, exact duration, blend, selected band, overlap rules and
      mapped contact/key positions. Make frame units explicit on each field.
- [ ] Expose opt-in ballistic/momentum tools with applicability warnings,
      assumptions and drift/error readouts. Keep heuristic physics separate
      from a guarantee of a physically valid motion.

### 9.3 Cleanup integrity contracts

- [ ] Add or strengthen contracts for scoped identity, deterministic output,
      finite transforms, preserved hierarchy/lengths, fade boundaries and
      contact/key mapping under retime; identify tolerance versus exactness.
- [ ] Define conflicts between corrections, pins, contacts and retime in one
      shared policy. UI warnings, CLI validation and report explanations agree.
- [ ] Add per-case quality fixtures for unreachable targets, straight-limb
      singularities, mirrored rigs, short clips, first/last-frame contacts and
      loop seams. Include reviewed output and failure expectations.

### 9.4 Tool-specific acceptance records

Populate missing records before further default tuning; reuse existing
foot-workflow corpus evidence where applicable. Numerical
thresholds must include rig scale, sampling rate and units. A mathematically
valid kernel can still fail the visual or preservation gate.

| Tool family | Improvement evidence | Preservation and failure evidence |
|---|---|---|
| De-spike/median/smooth | Fewer labelled noise events; reduced high-frequency energy on affected channels. | Deliberate impact peaks, turn direction, timing and scoped boundaries retained; no flat spots or quaternion flips. |
| Foot lock/pivot | Worst/p95/total planted displacement and floor error improve on validated intervals. | Knee transition speeds, reach error, toe rolls and adjacent airborne movement pass; impossible constraints are reported. |
| Hand lock/pin | Anchor error and planted drift improve on user-confirmed targets. | Elbow motion and reach remain acceptable; free gestures and unmarked spans are unchanged. |
| Pole/twist | Pole discontinuity and unwanted off-axis motion decrease. | Endpoint drift and bone lengths stay within declared tolerance; intentional forearm/roll-bone twist survives. |
| Pelvis cleanup | Path acceleration spikes reduce on selected spans. | Protected plants and body trajectory intent remain; joint reach/extension artifacts do not worsen unnoticed. |
| Seam | Position/orientation/velocity mismatch decreases at the chosen wrap boundary. | Interior motion and contacts remain within their gates; a non-looping action is never auto-converted into a loop. |
| Corrections/offsets | Requested pose change is reached within the declared solver tolerance. | Fade endpoints, unselected bones/frames and undo/session replay agree; unreachable goals are visible. |
| Retime | Output duration and frame mapping match the requested speed policy. | Contacts, keys, pins and issue navigation map consistently; no invalid ordering, discontinuous orientation or unexplained drift. |
| Physics heuristics | Selected path/spike measure improves with assumptions recorded. | Contact and pose distortion budgets pass; unavailable mass/environment information is disclosed. |

For each case retain the source, recipe, detector settings, expected metrics,
worst-frame references, reviewed captures, artifact paths and named reviewer.
Freeze per-case thresholds before comparison and record explicit pass/fail. Record both absolute error and
change from source; summing errors across clips must not hide a failed case.

**Exit:** contact and correction editing is discoverable and precise;
difficult fixtures satisfy declared local quality gates or show a clear
unresolved warning. Every exposed tool survives undo/session/export replay.

### Correction channel index admission

Correction application now checks unsigned channel indices against its scope
before converting them to signed frames or calling the bounded weight kernel.
Four laws cover scope endpoints and refusal beyond the scope/frame domain.
Compile-only objects from the source-matched `22cf6e5b` compiler are recorded in
`build/correction-index-qualification/evidence.json`; source hashes were observed
after compilation, so this record does not establish immutable build inputs.
Authenticate the laws and qualify oversized channel arrays, unchanged keys
outside the scope, and session/export replay before accepting this boundary.


### Endpoint no-op qualification

The typed frame dispatcher now closes an unchanged endpoint draft with
explicit feedback, without committing history or rebuilding the preview.
`StudioContactFramePolicy::changes_interval` rejects invalid plans and compares
both endpoints; two laws cover unchanged and invalid candidates. Qualify this
behavior with current compiler/prover products and native keyboard/pointer
flows: re-entering an existing endpoint must leave undo depth, dirty state and
preview revision unchanged. This implementation does not close native acceptance.

Contact endpoint drafts are also bound to `stack_generation`; a history change
rejects the draft before mutation and asks the user to reopen the field.
Invalid input now distinguishes the clip's exact frame limit from crossing the
opposite endpoint, reports that endpoint in displayed 1-based frames, and keeps
the draft editable. Qualify stale drafts after undo/redo, session application,
and take replacement, plus both inversion messages at the minimum window size.

First/Last contact endpoint fields now have native accessibility action nodes,
with edit instructions and current interval context. Both route through the
existing draft editor and are disabled without an authored interval. Tree laws
cover parentage and endpoint traversal; the existing action-order expectation
now includes the endpoint controls. Compile/replay and VoiceOver interaction
remain pending, including focus after activation and draft/error announcements.

Numeric input correction also preserves invalid retime-speed drafts on Enter,
with the valid 0.1–4 range, an example and Escape guidance. Qualify editing the
preserved draft with Backspace and resubmitting; no invalid speed may mutate
bands or history. The numeric capacity refusal likewise retains input and
reports the eight-character limit instead of silently ignoring accepted input.

Retime text parsing now rejects fractional digits beyond the three decimal
places representable by permille instead of silently discarding them. The
correction message states this precision limit. Qualify exact inputs at 0.1,
4 and three decimal places, and refusal of a fourth fractional digit (including
zero), retaining the draft and committed state. The existing parser's `sview`
loop remains outside the current symbolic proof boundary; source compilation
and native correction flow are still pending.

Retime drafts capture history generation and exact range endpoints or focused
band at entry. Enter rejects a changed target before applying speed; three laws
cover identity, history changes and target changes. Qualify selecting another
band/range while typing, undo/redo and take replacement; committed bands must
remain unchanged on refusal. Current compilation and replay remain pending.
