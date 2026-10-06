# M4: contact cleanup and precise repair

[Roadmap index](../../IMPLEMENTATION_PLAN.md)

## 9. M4 — Better contact cleanup and precise local repair

### 9.1 Contact editor

- [ ] Show a contextual preview while an endpoint is dragged and make
      cancellation leave the saved contact state untouched. Preview follows
      pointer movement; Escape or focus loss preserves stack/history/output,
      and release creates exactly one commit. Validate range
      handles at the minimum supported window size and on long takes.
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

