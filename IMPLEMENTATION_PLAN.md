# Mocap Cleaner — Implementation Plan

A desktop tool that does one thing: turn raw or retargeted motion capture into
clean, shippable animation. It is inspired by Cascadeur, but the scope is
**cleanup only**. There is no keyframe authoring from scratch, no rendering
pipeline and no rigging.

- **UI:** elisa-ui, with elisa-ui-designer for layouts.
- **3D viewport, pose evaluation and debug drawing:** Elisa-engine. See
  `elisa-engine/docs/plans/mocap-engine-track.md`, milestones M01–M08.
- **App logic:** Elisa (`src/`), with tests in `test/` and machine-checked
  properties in `proof/` (elisa-proof).

## Principles

1. **Non-destructive.** A clip is a source plus an ordered stack of cleanup
   operations. Every operation has parameters, can be toggled and scoped to a
   frame range and a set of bones, and can be undone. The source file is
   never modified.
2. **Show the problem before fixing it.** Every tool pairs a *detector*
   (curves, heat colouring, markers on the timeline) with a *fixer*. Users jump
   to the worst frame, not scrub for it.
3. **Measured, not eyeballed.** Each operation reports what it changed, such as
   the maximum rotation change, foot slide before and after, and seam jumps.
   The same metrics run headless in CI.
4. **Contacts are sacred.** Planted feet (and, later, hands) never slide or
   sink as a side effect of any other fix.
5. **Clip boundaries are exact.** Fixes fade to the source at clip edges, and
   loops wrap, so blends in a game still meet.

## Proven reference

`elisa-boxing-game/tools/clean_leg_motion.py` and its companions already solve
the first problems on real Mixamo-derived boxing clips at 120 Hz. They are the
algorithmic spec for phase 1:

- Running-median de-spike followed by a Gaussian. The median removes
  out-and-back twitches shorter than about 170 ms and keeps deliberate turns.
- Ground detection from heel and ball height. The planted foot's rotation is
  de-spiked about whichever of heel and ball is lower, with a vertical fix so
  it neither sinks nor floats.
- Foot heading de-spike, in the air as well.
- Knee pole de-spike, then a knee turn about the hip–ankle line. The turn is
  just enough to keep the ankle's off-hinge "wring" under a soft limit of
  about 16° from the clip's guard pose.
- Pelvis path smoothing, so a landing does not snap the knees.
- Two-bone IK re-solve that uses the smoothed source hinge axes, so no twist
  noise is inherited.
- Edge fade and loop wrap.

## Phases

### Phase 0: Skeleton of the app (headless first)
- [ ] Project setup: `elisa.project.json`, build script via Elisa-engine's
      `scripts/elisa_build_run.py`, README, AGENTS.md.
- [ ] Data model: `Skeleton` (hierarchy, rest pose, hinge axes), `Clip`
      (per-bone tracks resampled to a fixed rate), `Pose`.
- [ ] GLB import into the model, and GLB export that leaves untouched nodes,
      meshes and skins byte-identical (engine M06).
- [ ] Operation stack: `Operation { kind, params, bones, range, enabled }`,
      evaluated in order and cached per operation.
- [ ] Headless CLI: `mocap-cleaner clean in.glb --preset boxing -o out.glb --report r.json`.
- [ ] Gate: the CLI reproduces the boxing leg-cleanup metrics within
      tolerance on the boxing GLBs.

### Phase 1: The immediately useful tools
Each tool comes with its detector.

| Tool | Detector | Fix |
|---|---|---|
| **De-spike** (any bone or channel) | Angular acceleration per bone, highlighted on the timeline | Running median plus Gaussian, with window and strength settings |
| **Smooth** | Jitter (high-pass magnitude) | Gaussian or Butterworth, low-pass per channel group |
| **Foot contacts** | Contact bars on the timeline from heel and ball height and speed, editable by hand | Pin planted foot position and heading, pivot about heel or ball, with no sink or float |
| **Foot slide** | Planted-foot speed | Lock to the contact position, blend in and out |
| **Knee and elbow stability** | Pole swing and off-hinge ankle or wrist wring | Pole de-spike plus the wring limit (hip-roll correction) |
| **Pelvis path** | Vertical and horizontal acceleration spikes | Path smoothing, legs re-solved to the contacts |
| **Twist cleanup** | Off-axis twist on hinge joints (knee, elbow) | Rebuild from the hinge plane, move twist to the roll bones |
| **Loop seam** | Position and velocity jump from last frame to first | Cross-fade the seam over N frames |

Status (headless, `src/ops/rig_stack.elisa`, CLI `--op twist|pole|pelvis|lock`):
twist cleanup, knee/elbow pole stability, pelvis path with leg re-solve, and
foot lock are implemented on the rig view (`src/io/rig.elisa`, whole
quaternions plus hierarchy). Foot contacts are detected, not yet hand-editable;
the lock holds the ankle position and keeps the foot's source rotation (no
heel/ball pivot yet).

### Phase 2: The studio UI
Everything above works headless first; the UI puts it in front of the user.
- [ ] Main window: a viewport (engine M01) with perspective, front and side
      views, a skeleton overlay (M03), and a mesh toggle with x-ray.
- [ ] Timeline: scrub, play at 1×, ½× and ¼×, frame step, contact bars, and
      problem markers from the detectors.
- [ ] Curve view: per-bone rotation and position curves, with source and
      cleaned drawn together.
- [ ] Operation stack panel: add, reorder, toggle and scope operations, with
      live preview through engine pose override (M02).
- [ ] Overlays (M05): foot and hand motion trails, contact markers,
      acceleration heat on bones, onion skins, before/after ghost.
- [x] Undo and redo over the operation stack. (History of whole stacks,
      corrections included; Cmd-Z / Cmd-Shift-Z through the proved
      `src/studio/shortcuts.elisa`; tests `studio_shortcuts`, `studio_capture`.)

### Phase 3: Direct manipulation
- [x] Gizmos (M04): rotate and translate a bone and key it as a correction
      layer that fades in and out over a range. (R / V show the engine gizmo
      on the selected bone; releasing a drag keys `src/ops/corrections.elisa`
      at the current frame, faded over 12 frames each side by the proved
      `KeyWeight` ramp, into the stack and history. Applied on release, no
      live drag preview yet. Translation needs a translation channel on the
      bone. Test `studio_correction`.)
- [x] Pin tool: pin any end effector (foot, hand, head) over a range. IK
      holds it while other fixes run. (Headless: hands and feet via
      `--pin ROLE:FIRST:LAST[:BLEND]`, run after every other fix; head not yet.)
- [x] Offset layer: an additive correction curve per bone, e.g. to push the
      knees out. (Headless: constant angle about a local axis with fade in/out,
      `--offset ROLE:AXIS:DEGREES:FIRST:LAST[:FADE]`; keyed curves wait for the studio.)

### Phase 4: Physics-aware cleanup (the Cascadeur part)
- [ ] Centre of mass and support polygon overlay, flagging frames where
      balance is impossible.
- [ ] Ballistic check: airborne phases should follow a parabola; fix the
      pelvis path to match.
- [ ] Momentum smoothing: cap angular momentum spikes on the torso.

### Phase 5: Batch and pipeline
- [x] Presets per source, e.g. "Mixamo boxing" or "Rokoko raw". (`boxing`, `raw`, `rokoko`.)
- [ ] Batch folder processing with an HTML report.
- [x] Retarget-aware import: map several skeletons to a common rig.
      (`src/io/rig_map.elisa`: Mixamo, plain, Rokoko/Unity spellings onto `src/core/roles.elisa`.)

## Proofs (elisa-proof)

**Target: roughly as much proof code as business logic.** Every kernel and
operation lands in the same change as its proofs, and proofs are part of the
phase gates. Write them in `proof/`. Each numeric kernel gets proofs of its
contract, not just tests. Candidates, in rough order:

- **Median de-spike:** output length equals input; a constant signal is
  unchanged; a monotone signal stays monotone; output lies within the input's
  min and max for each window.
- **Gaussian smooth:** kernel weights sum to 1; constant in gives constant out;
  wrap mode stays periodic.
- **Edge fade:** fade(0) = fade(n−1) = 0 and fade is 1 in the interior, so the
  clip boundaries equal the source exactly.
- **Two-bone IK:** reachable targets are hit exactly (within ε); bone lengths
  are preserved; the knee lies in the plane of the pole.
- **Quaternion helpers:** normalise yields unit length; hemisphere alignment
  keeps the dot product with the previous frame ≥ 0; the swing/twist split
  recomposes to the input.
- **Contact pinning:** a planted foot's lowest point stays at floor height.
- **Operation stack:** disabled operations are the identity; a range-scoped
  operation leaves frames outside its range unchanged.
- **GLB round-trip:** export after import with no operations is
  byte-identical.

When elisa-proof lacks something these need, or has bugs, fix it in a
dedicated worktree of `elisa-proof` on its own branch and record each item in
`docs/proof-gaps.md`.

## Engine dependencies

| Need | Engine milestone | Blocks |
|---|---|---|
| Animation math: quaternions, IK, filters | M08 | Phase 0 and 1 |
| Pose override from app-supplied transforms | M02 | Phase 2 preview |
| GLB round-trip | M06 | Phase 0 export |
| Headless mode and offscreen PNG | M07 | CI gates |
| Viewport inside elisa-ui | M01 | Phase 2 |
| Skeleton draw and pick | M03 | Phase 2 and 3 |
| Overlays: trails, heat, ghosts | M05 | Phase 2 |
| Gizmos | M04 | Phase 3 |

Suggested first slice (agreed with the engine session): **M08 plus M02**, and
in this repo Phase 0 plus the de-spike and foot-contact tools, all headless.
M01 is waiting on one decision: whether elisa-ui hosts a shared Metal texture
or an SDL child window.
