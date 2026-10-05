# Foot and hand cleanup workflow

How the studio fixes sliding and sinking feet and planted hands, what is proved,
what is only tested, and what is still open. Metrics are in micro-units (µm on
a metre-scaled rig), summed over planted frames of the boxing clips.

## Workflow in the studio

1. Open a clip. Foot cleanup is **on by default** (`feet` in the stack,
   blend 4 frames).
2. Read the sidebar readout: `slide before -> after` and
   `sink before -> after`, green when better, red when worse, grey when the
   same. The value eases to its new number over 250 ms after each edit.
3. Look for red ticks above the timeline: bins whose planted slide is still
   over 2 mm on a frame. A red triangle marks the single worst frame.
4. Press **W** to jump there: the playhead moves to the worst frame, the
   worse foot becomes the selected bone, and all three views frame that foot.
5. Select a contact on the timeline's foot rows (L green, R yellow). Clicking
   a row and frame scrubs there and selects that exact output frame; it never
   edits the contact. Use the Plant or Lift button in the timeline editor, or
   **Shift-P** / **Shift-L**, to set a one-frame override. Use Reset or
   **Shift-U** to remove this frame from authored overrides and return it to
   automatic detection; Reset is disabled when the selected frame has no
   authored override. Delete or **Shift-Delete** removes the newest authored
   interval containing the selected frame; its full 1-based range is shown
   before removal and repeated in the status line afterward. Delete is undoable.
   Reset remains frame-local. Merge appears when that interval touches an
   authored interval for the same side and state; it joins the two without
   changing contact output and can be undone. The selected side and 1-based
   frame number stay visible in the editor. To change a run's extent, drag its
   start or end handle (6 px grip). Clicking a run body or a gap only selects
   and scrubs. Every edit is
   in undo/redo (Z / Y).
6. **,** and **.** shorten or lengthen the carry blend (1..24 frames).
7. **K** toggles foot cleanup, recorded in history, so before/after is one
   key away.
8. In the 3D views (T trails), planted stretches of each foot trail are drawn
   as a bright doubled line on top of the trail.

## Hand contacts

Hand cleanup is opt-in with **J**; the session saves this toggle. The two hand
rows sit below the foot rows in the timeline (L hand blue, R hand orange) and
use the same select-first Plant/Lift/Reset, interval Delete/Merge and run-end drag
behavior. The sidebar shows the hand slide before and after the lock. **A** /
Auto runs Fix all: the boxing preset plus both foot and hand locks as one
undoable edit, with spike, balance, foot slide/sink and hand slide metrics
shown together.

## Per-clip metrics (all boxing clips, `test/foot_clips.elisa`)

Slide and sink: before → after cleanup. Knee pop (largest frame-to-frame
knee turn, µrad): the take, then the pivot and the lock on main (before the
knee limits) → now. The gate (`Knee::pop_ok`) is
`pop ≤ src + src/10 + 7000` for both ops on every clip, with slide and sink
after ≤ before + 1 mm.

| clip | frames | pivot slide | pivot sink | lock slide | pop src | pivot pop main → now | lock pop main → now |
|---:|---:|---|---|---|---:|---|---|
| 0 | 121 | 51404 → 53 | 241669 → 111 | 79561 → 0 | 19200 | 19258 → 19258 | 21005 → 21005 |
| 1 | 121 | 75922 → 55 | 690354 → 101 | 110927 → 426 | 22201 | 18977 → 22227 | 22054 → 22054 |
| 2 | 113 | 39626 → 80 | 72847 → 93 | 52672 → 0 | 11500 | 11245 → 11245 | 11282 → 11282 |
| 3 | 121 | 2499 → 88 | 3365 → 100 | 2485 → 0 | 3090 | 3109 → 3109 | 3073 → 3073 |
| 4 | 61 | 20 → 15 | 90 → 99 | 0 → 0 | 3 | 14 → 14 | 3 → 3 |
| 5 | 121 | 61734 → 46 | 1484493 → 109 | 84392 → 57 | 17381 | 12959 → 12959 | 16331 → 16331 |
| 6 | 137 | 95590 → 78 | 1572803 → 128 | 156858 → 212 | 22603 | 50975 → 23285 | 24329 → 25370 |
| 7 | 361 | 1812 → 227 | 3866 → 353 | 1790 → 0 | 1217 | 1221 → 1221 | 1223 → 1223 |
| 8 | 481 | 1251 → 326 | 3852 → 468 | 1293 → 0 | 918 | 921 → 921 | 922 → 922 |
| 9 | 97 | 22519 → 61 | 72620 → 93 | 33320 → 0 | 10460 | 10613 → 10613 | 11068 → 11068 |
| 10 | 121 | 54421 → 75 | 566865 → 99 | 83185 → 0 | 23756 | 22794 → 22794 | 23174 → 23174 |
| 11 | 121 | 64144 → 68 | 482781 → 92 | 72602 → 0 | 16679 | 16343 → 16343 | 16534 → 16534 |
| 12 | 193 | 106407 → 77 | 1404944 → 137 | 106386 → 0 | 46376 | 61374 → 46723 | 46376 → 46376 |
| 13 | 169 | 51405 → 212 | 222986 → 689 | 51379 → 188 | 31341 | 36205 → 32922 | 31341 → 31341 |
| 14 | 121 | 17674 → 38 | 37073 → 79 | 17661 → 0 | 18911 | 18911 → 19224 | 18911 → 18911 |
| 15 | 121 | 18136 → 68 | 37018 → 80 | 18134 → 0 | 18549 | 18549 → 19835 | 18549 → 18614 |
| 16 | 137 | 63947 → 60 | 1308085 → 76 | 194232 → 0 | 18586 | 18247 → 18247 | 21442 → 21442 |
| 17 | 137 | 57730 → 77 | 1039900 → 85 | 141943 → 2 | 22526 | 22063 → 22063 | 26482 → 26482 |
| 18 | 129 | 96844 → 102 | 1761199 → 108 | 259176 → 32 | 28210 | 23802 → 23802 | 29941 → 29941 |
| 19 | 137 | 75335 → 97 | 1312209 → 141 | 190523 → 40 | 12161 | 41030 → 13525 | 12267 → 12267 |
| 20 | 145 | 85069 → 92 | 1892253 → 99 | 213398 → 54 | 21033 | 21311 → 21311 | 20843 → 20843 |
| 21 | 241 | 33492 → 170 | 954235 → 208 | 44792 → 0 | 3285 | 3136 → 3136 | 3552 → 3552 |
| 22 | 81 | 10133 → 45 | 36621 → 61 | 11160 → 0 | 3157 | 3066 → 3066 | 3589 → 3589 |
| 23 | 105 | 64374 → 29 | 1100467 → 60 | 182379 → 0 | 10108 | 17055 → 17055 | 16531 → 16531 |
| 24 | 137 | 89915 → 421 | 2178918 → 4378 | 180772 → 4 | 21804 | 19170 → 19170 | 17657 → 17657 |
| 25 | 137 | 48914 → 50 | 1784328 → 46 | 83543 → 0 | 26076 | 25820 → 25820 | 26530 → 26530 |
| 26 | 193 | 62950 → 1634 | 1745366 → 4751 | 138994 → 0 | 33943 | 64678 → 35946 | 33943 → 33943 |
| 27 | 177 | 56460 → 316 | 1848073 → 5366 | 117016 → 0 | 50315 | 79763 → 52324 | 60993 → 52668 |

## UX checklist

- [x] K fixes the feet (history-recorded toggle; default on)
- [x] Contact-row clicks select and scrub without changing contact data
- [x] Plant/Lift one selected frame with a button or shortcut; edits undo/redo
- [x] Reset one frame to automatic detection without changing neighboring frames
- [x] Delete the newest authored interval at the selected frame and preserve
      its prior override/detection result
- [x] Merge adjacent same-side, same-state authored intervals without changing
      the contact output
- [x] Existing contact-run endpoint dragging
- [x] Live slide/sink before/after readout with green/red cues
- [x] Smooth readout transition (proved `progress`/`mix` ramp)
- [x] W jumps to the worst frame and frames the foot
- [x] Worst-slide markers on the timeline (binned for the draw budget)
- [x] Planted trail segments drawn distinctly
- [x] Blend setting (, and .), clamped and history-recorded
- [x] Hover highlight on contact rows
- [x] Shortcut hints in the sidebar
- [x] Sensible defaults: feet on, blend 4

## Gap audit

- **Proved** (`src/studio/foot_policy.elisa` + `_laws`): blend clamp and
  nudge, grab of a run end or body, drag clamps, the edit range and
  planted/lifted decision, new-span bounds, before/after cue, marker
  threshold, worst-frame scan step, transition ramp and mix.
- **Proved** (`src/studio/contact_editor.elisa` + `_laws`): valid exact-frame
  selections, explicit Plant/Lift/Reset/Delete action mapping, the half-open
  interval plan for removing one frame, stable interval compaction after
  deletion, safe merge eligibility and range bounds, and the click-versus-drag
  threshold. Accessibility laws cover all five action identities in the
  timeline tree.
- **Tested headless only** (`test/studio_foot.elisa`): stack fields and
  history, press/release on a 100-frame row, apply-edits replay, the model
  build with feet off and on (readout, cue, worst frame, marker count, a lift
  edit emptying the contact row).
- **Tested headless only** (`test/studio_contact_editor.elisa`,
  `test/studio_accessibility.elisa`): contact selection/action policy,
  resetting overlapping intervals while preserving later edit order, deleting
  the newest overlapping interval and compacting unaffected edits, merging
  forward and reverse adjacent ranges, refusing different-state/side, gapped
  or overlapping intervals, merge undo/redo, atomic reset-capacity failure,
  and stable Plant/Lift/Reset/Delete/Merge semantic
  identities. These do not exercise native pointer routing or screen-reader
  activation.
- **Not tested at all** (needs a window): key dispatch, pointer routing to
  contact-row selection and endpoint dragging, visible button enablement,
  Shift-P/Shift-L/Shift-U/Shift-Delete activation, native semantic-button
  activation, hover, drawing of markers/readout/trails, and camera framing on W.
  The studio app builds successfully, but this contact-editor revision has not
  been exercised in a window; no screenshots were taken.
- The per-frame worst slide can rise with feet on even when the total falls:
  the pivot moves the planted foot over the blend frames. The test gates
  the totals and the marker count, not the single worst frame.
- Baseline fix: `src/ops/stack.elisa` named `Kind` unqualified, which
  collides with an elisa-ui `Kind` once the studio includes the UI, so the
  studio app did not compile on main. It is now `Ops::Kind`.

## Knee limits (MotionBuilder / Cascadeur style)

The pivot and the lock both solve the leg through `src/core/knee.elisa`:

- **Soft reach.** A target past the leg's reach eases into full extension
  over the last 4 % of the leg (`Knee::soft_reach`) instead of snapping
  straight. Frames the source leg already reached are kept.
- **Knee speed limit.** The knee angle may turn no faster per frame than the
  take's own fastest knee motion (`Knee::speed_budget`). Planted frames are
  held exactly; the correction ramps in before a plant and out after it
  (`Knee::follow`, forward then backward, twice), so the extra knee motion is
  spread over the airborne frames.
- **Adaptive release.** A plant that ends on a nearly straight leg releases
  over two or three times the blend (`Knee::release_blend`).

Trade-offs, measured above: clips 24, 26 and 27 leave the planted foot up to
1.6 mm off and 5 mm high where the leg is pulled past its reach (main: under
0.2 mm). The 7 mrad allowance is for frames where the plant itself moves the
knee fast (clip 23's pivot, and clips 17 and 23 in the lock, which already
popped this much on main).

## Rebuild cost with K on

Foot edits go through the studio's cached rebuild (`StudioModel::build_with`
via `App::rebuild`), so the op caches still skip unchanged ops. The frame
window cannot narrow while the foot fix is on, though: the pivot is
non-local, so `StudioPerf::edit_window` returns the whole clip when K, the
blend or a contact edit changes, and for any edit while K is on. With K off,
correction edits keep their narrow window (`test/studio_rebuild.elisa`
measures that path with K off and gates the full window with K on).
