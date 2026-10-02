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
- [x] Project setup: `elisa.project.json`, build script via Elisa-engine's
      `scripts/elisa_build_run.py`, README, AGENTS.md.
      Status: `scripts/build.sh` builds the CLI through `elisa_build_run.py`
      with the new engine console host (`"host": "console"`, mocap-track
      dd502f51); `scripts/check.sh` builds the CLI that way.
- [x] Data model: `Skeleton` (hierarchy, rest pose, hinge axes), `Clip`
      (per-bone tracks resampled to a fixed rate), `Pose`.
- [x] GLB import into the model, and GLB export that leaves untouched nodes,
      meshes and skins byte-identical (engine M06).
- [x] Operation stack: `Operation { kind, params, bones, range, enabled }`,
      evaluated in order and cached per operation.
      Status: `Ops::evaluate_cached` keeps chained per-op keys and results and
      reruns only ops after the first changed one (disabled-op edits change
      nothing); kernel `src/core/stack_cache.elisa` and
      `proof/stack_cache_laws.elisa` proved; `test/op_stack_cache.elisa`
      checks equal output and evaluation counts. The rig stack
      (`rig_stack.elisa`) is not cached yet: contact edits there are read by
      earlier lock/pivot ops, so its prefix is not independent.
- [x] Headless CLI: `mocap-cleaner clean in.glb --preset boxing -o out.glb --report r.json`.
- [x] Gate: the CLI reproduces the boxing leg-cleanup metrics within
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

Status (headless, `src/ops/rig_stack.elisa`, CLI `--op twist|pole|pelvis|lock|pivot`):
twist cleanup, knee/elbow pole stability, pelvis path with leg re-solve, and
foot lock are implemented on the rig view (`src/io/rig.elisa`, whole
quaternions plus hierarchy). Foot contacts are detected and hand-editable
(`--contact FOOT:FIRST:LAST:on|off`, `Contact::edited`). The plain lock holds
the ankle and keeps the foot's source rotation; `--op pivot` instead turns the
planted foot about the lower of heel and ball (`Pivot::choose`, with
hysteresis), holds that point at its plant position and settles it on the
floor (no sink or float; `test/rig_tools.elisa` on the boxing jab: pivot
slide 22.5 mm to 1.4 mm, floor error 72.6 mm to 4.3 mm summed over planted
frames). The heel is approximated by the ankle joint (the rigs have no heel
bone). The operation stack is saved and loaded as an ops file
(`src/io/ops_file.elisa`, `--save-ops FILE`, `--ops FILE`).

### Phase 2: The studio UI
Everything above works headless first; the UI puts it in front of the user.
- [x] Main window: a viewport (engine M01) with perspective, front and side
      views, a skeleton overlay (M03), and a mesh toggle with x-ray. (Three
      Metal views in `src/studio/app/app.elisa`; M toggles the skinned mesh,
      X x-ray. Headless capture of all three plus the mesh view in
      `studio_capture`. The GPU path itself is only checked by hand.)
- [x] Timeline: scrub, play at 1×, ½× and ¼×, frame step, contact bars, and
      problem markers from the detectors. (Proved `TimelineState`; markers
      binned by severity; a red strip marks balance-impossible frames.)
- [x] Curve view: per-bone rotation and position curves, with source and
      cleaned drawn together. (Dim source, bright cleaned; P switches between
      rotation and position, falling back to whichever channel the bone has,
      via proved `StudioOverlay::channel`. Position mode added here.)
- [x] Operation stack panel: add, reorder, toggle and scope operations, with
      live preview through engine pose override (M02). (Add 1-5, up/down,
      toggle, remove, range I/O, bones B, strength [ ]; each edit goes through
      history and rebuilds the cleaned clip, drawn via PoseOverride.)
- [x] Overlays (M05): foot and hand motion trails, contact markers,
      acceleration heat on bones, onion skins, before/after ghost. (Toolbar
      and T/C/H/N/G; rendered in `studio_capture`.)
- [x] Undo and redo over the operation stack. (History of whole stacks,
      corrections included; Cmd-Z / Cmd-Shift-Z through the proved
      `src/studio/shortcuts.elisa`; tests `studio_shortcuts`, `studio_capture`.)

### Phase 3: Direct manipulation
- [x] Gizmos (M04): rotate and translate a bone and key it as a correction
      layer that fades in and out over a range. (R / V show the engine gizmo
      on the selected bone; releasing a drag keys `src/ops/corrections.elisa`
      at the current frame, faded over 12 frames each side by the proved
      `KeyWeight` ramp, into the stack and history. Applied on release; while
      dragging, the posed skeleton is previewed in orange (PoseOverride with
      the gizmo goal, gated by proved `StudioOverlay::preview`; the preview
      pose is tested headless, the drag wiring only by hand). Translation needs a translation channel on the
      bone. Test `studio_correction`.)
- [x] Pin tool: pin any end effector (foot, hand, head) over a range. IK
      holds it while other fixes run. (Headless: hands, feet and head via
      `--pin ROLE:FIRST:LAST[:BLEND]`, run after every other fix. The head pin
      turns the neck toward the anchor and restores the head's orientation;
      its position is exact only while the torso keeps the neck-to-anchor
      distance.)
- [x] Offset layer: an additive correction curve per bone, e.g. to push the
      knees out. (Headless: constant angle about a local axis with fade in/out,
      `--offset ROLE:AXIS:DEGREES:FIRST:LAST[:FADE]`; keyed curves, linear
      between keys, via `--keyed ROLE:AXIS:FRAME:DEGREES:FRAME:DEGREES...`.
      Keying from a gizmo waits for the studio.)

### Phase 4: Physics-aware cleanup (the Cascadeur part)
- [x] Centre of mass and support polygon overlay, flagging frames where
      balance is impossible. (Engine `BalanceOverlay` (CoM marker, plumb line,
      convex support hull; test `viewport_balance`). Per-frame states come from
      the same detector as `--op balance` (`Physics::balance_frames`, report
      rule proved as `Balance::reported`); impossible frames turn the CoM red
      and are marked on the timeline. Q toggles. The jab clip has no impossible
      frames, so the red path is checked only in the engine test.)
- [x] Ballistic check: airborne phases should follow a parabola; fix the
      pelvis path to match. (`--op ballistic`, opt-in; the boxing clips' "flights"
      are mostly contact-detection gaps.)
- [x] Momentum smoothing: cap angular momentum spikes on the torso.
      (`--op momentum`: tapered local smoothing, drift capped at 10°.)

Status: CoM and support-region flagging is headless (`--op balance`,
`src/physics/rig_physics.elisa`, reported in the CLI, JSON and HTML report),
and the studio overlay is done (Q).

### Phase 5: Batch and pipeline
- [x] Presets per source, e.g. "Mixamo boxing" or "Rokoko raw". (`boxing`, `raw`, `rokoko`.)
- [x] Batch folder processing with an HTML report. (`batch OUTDIR [--op ...] IN.glb|FOLDER...`; macOS dirent layout.)
- [x] Retarget-aware import: map several skeletons to a common rig.
      (`src/io/rig_map.elisa`: Mixamo, plain, Rokoko/Unity spellings onto `src/core/roles.elisa`.)

### Phase 6: Performance and high-ROI follow-ups
Ordered by return on effort. Every speedup is measured (before/after wall
time on the boxing jab and the full batch) and must leave outputs
byte-identical, or within the existing test tolerances.

**Proof loop (developer speed).** The full `scripts/check.sh` takes 185 s,
and almost all of that is the prover.
- [ ] Prover hot spots: `congruence_goal`, `disjunct_modus_ponens`,
      `linear_fact_parts` (in progress in `elisa-proof-mocap`); `build.sh`
      defaults to O2. Target: check.sh under 60 s.
- [ ] Incremental proofs: hash each source file plus the prover binary and
      skip re-proving unchanged files (`build/proof/<hash>.txt`).
- [ ] Longest-first scheduling in check.sh (balance, hinge, pin first), and
      `PROOF_JOBS` defaulting to the core count.
- [ ] Fix the 6 certificate-replay gaps so `key_weight` and
      `key_weight_laws` reach "proved".

**Interactive studio (user-visible latency).**
- [x] Wire `Ops::evaluate_cached` into the studio, so stack edits rerun only
      the ops after the first changed one. Do the same in the CLI's batch.
      Status: `GlbTracks::clean_animation_cached` with a per-channel bank kept
      in `StudioModel::Memo` (the take is loaded once) and shared by the CLI
      run. Jab: edit to the last op 520 of 1560 op runs, ~4 ms vs ~10 ms;
      unchanged stack ~2 ms. CLI output is byte-identical; the batch sees
      little reuse across different takes (cold runs cost about the same).
- [ ] Cache the rig stack: split it at the contact-edit boundary, so the
      lock/pivot dependency on contacts invalidates only the downstream part.
      Status: `RigCache::run_clip_cached` (`src/ops/rig_cache.elisa`) snapshots
      before the first foot lock; a contact edit reruns 2 of 5 steps
      (~13 ms vs ~23 ms), equal to `RigOps::run_clip`. Partial: library and
      tests only; the studio does not run the rig stack yet.
- [x] Range-limited re-evaluation: a correction or op scoped to frames A..B
      recomputes only A..B plus its fade margins.
      Status: `StudioPerf::edit_window` + windowed `joint_tracks`/`problems`/
      `peaks`; equal to a full build (`test/studio_rebuild.elisa`). Joint
      tracks over an 11-frame window ~0.25 ms vs ~2 ms. Op edits still clean
      whole channels (the cache handles them); contacts/balance stay full.
- [x] Gizmo drag preview at 60 fps: evaluate only the dragged bone's chain
      for the current frame, and keep the full rebuild for release.
      Status: `StudioPerf::chain_preview` over a base pose cached per frame and
      build; equal to `preview_models` (hips 52, hand 16, foot 2 bones
      moved). Not checked at 60 fps on screen (headless only).
- [x] Detectors and curves computed once per clip edit and memoised per bone
      (timeline markers, heat, curve view), not on every frame drawn.
      Status: detectors are computed per rebuild (windowed); the curve view
      reads `StudioPerf::Curves`, refilled only on a rebuild or a bone/mode
      change.
- [x] Frame-time budget overlay (F key) with per-stage times: evaluate,
      detectors, draw.
      Status: on Shift-F, since F already frames the views. Shows evaluate,
      detectors and draw µs, poses, ops rerun, drag bones moved. Builds;
      not inspected on screen.

**Foot cleanup in the studio.**
- [x] K toggles foot cleanup (on by default), recorded in history.
- [x] Timeline contact bars are editable (drag ends, lift, plant), with undo/redo.
- [x] Live slide/sink before/after readout with green/red cues and an eased transition.
- [x] W jumps to the worst slide frame and frames the foot; worst-slide markers on the timeline.
- [x] Planted trail segments drawn distinctly; hover highlight; blend keys; sidebar hints.
- [x] Proved kernels (`src/studio/foot_policy.elisa` + `_laws`), headless test `test/studio_foot.elisa`, per-clip gate `test/foot_clips.elisa`.
      Status: done 2026-10-02. Verified headless only; the app compiles but was not run on screen. Knee-pop gate is tolerant, an open trade-off in `docs/foot-workflow.md`.

**Kernels and batch (throughput).**
- [ ] Profile the CLI on the boxing clips; publish a per-op time table in
      the report.
- [ ] Running median in O(log w) per sample (two heaps or an order-statistic
      window) instead of re-sorting each window.
- [ ] Separable Gaussian with precomputed kernels; reuse buffers across
      bones instead of allocating per track.
- [ ] Batch: process files in parallel worker processes (`--jobs N`), and
      parse the GLB once per file for all ops.
- [ ] Structure-of-arrays tracks (contiguous per-channel floats) so the
      filters stream through memory.

**Product (non-performance, high ROI).**
- [ ] Hand contacts (planted hands on ropes and floor) reuse the foot
      contact pipeline.
- [ ] One-click "Fix all" in the studio: apply the preset, then show
      before/after metrics per detector.
- [ ] Report diff between two runs (regression check for preset changes).

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
