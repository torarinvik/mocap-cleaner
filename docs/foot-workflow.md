# Foot cleanup workflow

How the studio fixes sliding and sinking feet, what is proved, what is only
tested, and what is still open. Metrics are in micro-units (µm on a
metre-scaled rig), summed over planted frames of the boxing clips.

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
5. Fix contacts on the timeline's foot rows (L green, R yellow):
   - drag a bar's start or end (6 px grip) to plant or lift the frames it
     sweeps;
   - click a bar's body to lift that whole contact;
   - click an empty part of a row to plant 8 frames centred on the click.
   The hovered row is outlined. Every edit is in undo/redo (Z / Y).
6. **,** and **.** shorten or lengthen the carry blend (1..24 frames).
7. **K** toggles foot cleanup, recorded in history, so before/after is one
   key away.
8. In the 3D views (T trails), planted stretches of each foot trail are drawn
   as a bright doubled line on top of the trail.

## Per-clip metrics (all boxing clips, `test/foot_clips.elisa`)

Before → after. The gate requires slide and sink after ≤ before on every
clip, and a knee pop of at most `max(2·src, src + 35000)`.

| clip | frames | pivot slide | pivot sink | lock slide | knee pop src / pivot / lock |
|---:|---:|---|---|---|---|
| 0 | 121 | 51404 → 53 | 241669 → 111 | 79561 → 0 | 19200 / 19258 / 21005 |
| 1 | 121 | 75922 → 55 | 690354 → 101 | 110927 → 0 | 22201 / 18977 / 22054 |
| 2 | 113 | 39626 → 80 | 72847 → 93 | 52672 → 0 | 11500 / 11245 / 11282 |
| 3 | 121 | 2499 → 88 | 3365 → 100 | 2485 → 0 | 3090 / 3109 / 3073 |
| 4 | 61 | 20 → 15 | 90 → 99 | 0 → 0 | 3 / 14 / 3 |
| 5 | 121 | 61734 → 46 | 1484493 → 109 | 84392 → 0 | 17381 / 12959 / 16331 |
| 6 | 137 | 95590 → 78 | 1572803 → 128 | 156858 → 0 | 22603 / 50975 / 24329 |
| 7 | 361 | 1812 → 227 | 3866 → 353 | 1790 → 0 | 1217 / 1221 / 1223 |
| 8 | 481 | 1251 → 326 | 3852 → 468 | 1293 → 0 | 918 / 921 / 922 |
| 9 | 97 | 22519 → 61 | 72620 → 93 | 33320 → 0 | 10460 / 10613 / 11068 |
| 10 | 121 | 54421 → 75 | 566865 → 99 | 83185 → 0 | 23756 / 22794 / 23174 |
| 11 | 121 | 64144 → 68 | 482781 → 92 | 72602 → 0 | 16679 / 16343 / 16534 |
| 12 | 193 | 106407 → 77 | 1404944 → 137 | 106386 → 0 | 46376 / 61374 / 46376 |
| 13 | 169 | 51405 → 84 | 222986 → 137 | 51379 → 0 | 31341 / 36205 / 31341 |
| 14 | 121 | 17674 → 38 | 37073 → 79 | 17661 → 0 | 18911 / 18911 / 18911 |
| 15 | 121 | 18136 → 68 | 37018 → 80 | 18134 → 0 | 18549 / 18549 / 18549 |
| 16 | 137 | 63947 → 60 | 1308085 → 76 | 194232 → 0 | 18586 / 18247 / 21442 |
| 17 | 137 | 57730 → 77 | 1039900 → 85 | 141943 → 2 | 22526 / 22063 / 26482 |
| 18 | 129 | 96844 → 102 | 1761199 → 108 | 259176 → 32 | 28210 / 23802 / 29941 |
| 19 | 137 | 75335 → 97 | 1312209 → 141 | 190523 → 40 | 12161 / 41030 / 12267 |
| 20 | 145 | 85069 → 92 | 1892253 → 99 | 213398 → 54 | 21033 / 21311 / 20843 |
| 21 | 241 | 33492 → 170 | 954235 → 208 | 44792 → 0 | 3285 / 3136 / 3552 |
| 22 | 81 | 10133 → 45 | 36621 → 61 | 11160 → 0 | 3157 / 3066 / 3589 |
| 23 | 105 | 64374 → 29 | 1100467 → 60 | 182379 → 0 | 10108 / 17055 / 16531 |
| 24 | 137 | 89915 → 61 | 2178918 → 75 | 180772 → 4 | 21804 / 19170 / 17657 |
| 25 | 137 | 48914 → 50 | 1784328 → 46 | 83543 → 0 | 26076 / 25820 / 26530 |
| 26 | 193 | 62950 → 50 | 1745366 → 71 | 138994 → 0 | 33943 / 64678 / 33943 |
| 27 | 177 | 56460 → 53 | 1848073 → 71 | 117016 → 0 | 50315 / 79763 / 60993 |

## UX checklist

- [x] K fixes the feet (history-recorded toggle; default on)
- [x] Timeline-editable contact bars: drag ends, lift run, plant span; undo/redo
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
- **Tested headless only** (`test/studio_foot.elisa`): stack fields and
  history, press/release on a 100-frame row, apply-edits replay, the model
  build with feet off and on (readout, cue, worst frame, marker count, a lift
  edit emptying the contact row).
- **Not tested at all** (needs a window): key dispatch, pointer routing to
  the contact rows, hover, drawing of markers/readout/trails, camera framing
  on W. The studio app compiles to an object file (typecheck plus codegen),
  but nothing was run on screen; no screenshots were taken.
- The per-frame worst slide can rise with feet on even when the total falls:
  the pivot moves the planted foot over the blend frames. The test gates
  the totals and the marker count, not the single worst frame.
- Baseline fix: `src/ops/stack.elisa` named `Kind` unqualified, which
  collides with an elisa-ui `Kind` once the studio includes the UI, so the
  studio app did not compile on main. It is now `Ops::Kind`.

## Open trade-off: knee pop (for the user to decide)

The pivot holds the planted foot more tightly, which some clips pay for with
faster knee motion at lift-off. The gate is tolerant,
`pop_after ≤ max(2·src, src + 35000)`. Clips where the pivot raises the pop:
6 (22603 → 50975), 12 (46376 → 61374), 13 (31341 → 36205),
19 (12161 → 41030), 23 (10108 → 17055), 26 (33943 → 64678),
27 (50315 → 79763). The lock op pops less but slides slightly on clips
17, 18, 19, 20 and 24. Options: keep the tolerant gate; tighten it and
lengthen the blend on those clips; or limit knee speed in the pivot.

## Rebuild cost with K on

Foot edits go through the studio's cached rebuild (`StudioModel::build_with`
via `App::rebuild`), so the op caches still skip unchanged ops. The frame
window cannot narrow while the foot fix is on, though: the pivot is
non-local, so `StudioPerf::edit_window` returns the whole clip when K, the
blend or a contact edit changes, and for any edit while K is on. With K off,
correction edits keep their narrow window (`test/studio_rebuild.elisa`
measures that path with K off and gates the full window with K on).
