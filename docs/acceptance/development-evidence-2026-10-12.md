# Development evidence, 2026-10-12

Development-build evidence from 2026-10-12, moved out of
`pending-policy-qualification-2026-10-06.md` to keep files within 600
lines. Nothing here qualifies a build: every check used a Stage1 that is
not current compiler main (see the compiler notes below).

## Beginner workflow band (2026-10-12)

`src/studio/workflow_policy.elisa` derives the Import, Analyze, Fix,
Validate and Export step states and one next-step hint from measured take
facts (take loaded, import running, finding count, cleaned-take change,
detector regression, export of the current stack generation).
`src/studio/app/panels_workflow.elisa` draws it under the toolbar.
`proof/studio_workflow_laws.elisa` states its laws and
`test/studio_workflow.elisa` checks all 128 fact combinations.

Evidence so far is development-only. No current Stage1 or prover could be
built on 2026-10-12, because the Elisa-core stage0 tree had uncommitted
changes and rejected current compiler sources. The test passed and the
Studio object compiled with the stale Stage1 under
`ELISA_ALLOW_STALE_STAGE1=1`. The available provers (Oct 8 and Oct 11
builds) also fail on `contact_editor.elisa`, which the baseline records as
proved, so they cannot judge the new laws. A scratch-linked development
binary showed the band on the empty Studio window. Opening the boxer take
then crashed in `Studio.clip.rehome`. The same crash happens with HEAD alone
built by the same stale Stage1, so it is a toolchain fault, not this change.
Proof replay, baseline rows and native acceptance remain open until a
current toolchain exists.

## Plain-language findings and foot-slide detection (2026-10-12)

Finding rows now read like "Sudden jerk  frames 119-124  2.6x limit  High"
instead of raw detector values. `StudioIssueExplanationPolicy::ratio_tenths`
and `strength` derive the ratio and the Low/Medium/High label from the
measured peak and threshold; the capped severity cannot, because every
listed spike is at its maximum. Planted-foot slides over
`StudioFoot::Metric::MARK_SLIDE` (2 mm per frame) are new findings
(detectors 1 and 2, left and right foot), with the foot's rig slot as the
subject. Ranking ties compare peak-to-threshold ratios, because detector
units differ. On the boxing jab the contact detector plants only 2 of 194
foot-frames: the boxer steps and stays on the balls of the feet. So the jab
yields no slide findings, and `test/studio_findings.elisa` also covers a
synthetic planted slide. Evidence is development-only, with the same
toolchain limits as the workflow band above. Proof replay of the new
explanation laws and the user-FBX journey remain open.

## GLB takes with mixed channel lengths (2026-10-12)

Studio picks keys by frame index. So a channel with fewer keys than the
longest froze at its last key, and the sample clock refused playback of such
takes outright ("Animation channels use different sample times"). The
boxing jab GLB is one of them. `src/io/shared_grid.elisa` now resamples each
multi-key channel onto the longest channel's key times when a take loads
(linear, shortest-arc slerp for rotations, STEP held). This matches what the
FBX converter does since engine `1e98f075`. The source fingerprint is still
taken from the file bytes, before alignment, and the source file is never
written. Cubic-spline takes remain refused. `test/shared_grid.elisa` checks
that the jab is misaligned before and aligned after, that the sample clock
accepts the result, and that endpoint values are kept. With the region
handoff port below, a development build played all 97 frames.

Studio test sweep with the stale Stage1: 68 of 71 pass. `studio_capture`
and `studio_correction` fail to build on missing effect grants inside engine
files. `studio_foot` exits 51, as HEAD does without this change.

## Region handoff into globals is missing from compiler main (2026-10-12)

Compiler commit `806772c7` ("Fix region handoff into global stores") exists
only on `backup/fbx-worker-region-latest-pre-62eb`. Without it, development
builds crash in `Studio.clip.rehome` on every take load; HEAD without any of
today's changes crashes the same way. Ported onto `f7b6c4a2`, it made a
development Studio open, draw and play the boxer take. A main-based port is
on Elisa-compiler branch `mocap/region-handoff-port` (`a83b2d745`). It is
unbuilt, because no bootstrap on this host accepts current main's sources.
The Studio runtime bridge `build/generated/studio_runtime.elisa` includes
`/private/tmp/Elisa-compiler-fbx-latest`, another session's scratch
checkout. Its runtime currently fails to compile together with
`gltf_track_sample.elisa`, which is why `SharedGrid` uses `MotionQuat`.

## One frame numbering for beginners (2026-10-12)

The timeline label read "frame 96 / 96" on the last frame, while the status
bar, Go to Frame and the accessibility labels said "Frame 97 / 97". The
timeline now uses the same 1-based numbering. Export reports keep their
documented zero-based output frames. Development build only (region-fix
Stage1); not qualified.

## Sidebar header no longer overlaps (2026-10-12)

The Pending exports button was drawn over the Balance badge, and the
Workspace / File button covered the frame/bone and spike lines. Pending
exports now sits at the right end of the toolbar. Frames and bones are
shown beside the File button, and the duplicate spike line was dropped,
since "spikes before -> after" is still listed below. Checked by screenshot
of a development build with the boxer take open; not qualified.

## Export publishes again (2026-10-12)

In a development build, every export ended with "Prepared recovery no
longer matches the captured export" and nothing was published. The
recovery journal decoder handed its caller path arrays that were freed
when it returned (compiler gap G85 in `docs/proof-gaps.md`), so the
pre-publication reread never matched. With the decoders bound to the
caller's region, the boxer jab exported. Studio reported "written, reopened
and validated" with both reports. The exported GLB then opened in a fresh
Studio at 97 frames and 54 bones. Distinct publication rejections
(ownership, busy workspace, staging or destination changed) now have their
own plain-language messages. Development build only; not qualified.

## Two-frame bursts and remaining findings (2026-10-12)

Practice take: `build/practice/noisy-jab.glb`, derived from the boxer GLB
with quaternion spikes on frames 20-21, 55 and 80 of the jab's arm and leg
rotations. The default stack cut 172 spikes to 4, but a High "Sudden jerk"
on frame 20 survived. Despike was median-of-3 only, and two equal
outliers are a majority of three. Despike's first pass is still
median-of-3; later passes now use median-of-5 (`Order::median5`, built
from the proved `low`/`high`/`median3`), which removes bursts up to two
frames wide. With the default two passes, the same take now goes from
172 spikes to 2, and only a Low 1.1x finding remains. `track_kernels`
checks the new passes against a reference and checks that a two-frame
burst is removed.

Beginner journey on that take:
- The band no longer says "export" while findings remain. A new
  `RemainingFindings` hint says "Problems remain: press W to jump to each
  one...".
- W now steps through findings (worst first) and Shift-W steps back; with
  no findings, W keeps its old jump to the worst foot slide.
- A with nothing left to add now points to the findings list.
- Adding a step and Cmd-Z restored history 1/2 with the same results.

Related tests pass on the region-fix Stage1: track_kernels, track_tools,
op_stack, glb_clean, studio_workflow, studio_shortcuts, studio_state,
studio_issues, studio_issue_browser, studio_duplicate_operation,
studio_reset_scope and studio_session. Development build only; not qualified.

## Selecting a stack row works again (2026-10-12)

Up/Down never moved the stack selection. So `[` / `]`, B, I, O, D,
PgUp/PgDn and Delete always acted on the first row, and so did clicking
another row. `select_row` sent the selection through `commit`, which drops a
stack that `StackState::same` calls unchanged, and `same` ignores the
selection. Selection now changes the current history snapshot in place
(`HistoryState::reselect`): no undo step, and the take is not marked unsaved.
While a pending edit is staged, it still goes through `commit`.
`studio_state` covers it. In a development build on the practice take, Down
twice selected Despike and `]` raised it to 3x passes as one history step.
Development build only; not qualified.

## FBX journey opens; default cleanup follows the frame rate (2026-10-12)

`high block_Unreal5.6.fbx` (SHA `50048a8a…`, unchanged afterwards) imports
and opens in a development Studio built with
`/private/tmp/Elisa-compiler-fbx-latest` (branch
`codex/fbx-worker-region-latest`, Stage1 from `06e945842`). It shows 337
frames, 94 bones, ~30 fps, and 123 spikes cut to 41. That branch has
`0b2df353b` ("fix task callback region ABI ownership"), which gives worker
tasks their own arena (G86), and the region handoff fix. Neither is on
compiler main. This is labelled comparison evidence from another session's
unmerged compiler, not qualification.

The take exposed a cleaning fault: the default stack is the 120 Hz boxing
preset in frames, so at 30 fps its leg median spanned 666 ms instead of
166 ms. `Presets::operations_at` now retunes the preset to the take's
rate: median radius scales with the rate, binomial passes with its square
(the kernel's variance grows linearly with passes), and Despike stays
per-frame. Studio swaps the retuned stack in as the fresh history base
right after a take loads. At 30 fps the stack reads "radius 5 fr (166 ms)"
and "2x passes". `test/preset_rate.elisa` covers 120, 60, 30, 1 and
invalid rates. `proof/preset_rate_laws.elisa` compiles but is unproven;
there is no working prover on this host.

## Hold the first real pose (2026-10-12)

On the FBX take, the worst finding (a High sudden jerk, 55x the limit) is
frame 1's T-pose jumping into the motion. Studio could not fix it:
nothing trims frames, and every operation fades out over 8 frames at the
clip edges. New operation **Hold start** (`Ops::hold_start`, add button
"Hold start" or key 6) gives the first N frames (strength, default 1) the
pose of frame N. It spans the whole clip without an edge fade, so later
frames and the frame count stay unchanged. Sessions store it as kind code
6, export reports and the CLI name it `hold_start`, and the row shows
"first N fr". When a motion-spike finding peaks within the first two
frames, W's status line and the finding's help name the likely T-pose and
key 6.

In a development build (fbx-latest Stage1) on `high block_Unreal5.6.fbx`,
W jumped to frame 2 and the status read "This jump is at the very start:
likely a T-pose before the motion. Press 6...". Pressing 6 added Hold start
(first 1 fr, 33 ms) as one history step. Spikes after cleanup fell from 41
to 26, and the worst remaining finding became a 5.8x jerk at frame 316.
`test/hold_start.elisa` covers held frames, untouched later frames, an
over-long hold and the session kind code. op_stack, studio_session,
studio_state, glb_clean, studio_shortcuts, track_kernels, studio_capacity
and studio_issues pass.

## FBX take exported and reopened (2026-10-12)

Rank-1 journey in a development build (fbx-latest Stage1; labelled
comparison evidence, not qualification):
- Open `high block_Unreal5.6.fbx` (source SHA `50048a8a…`, unchanged
  after every step).
- Review the export; acknowledge the one balance note.
- Export: "The GLB was written, reopened and validated", with both reports
  beside it in `build/`.
- Reopen `high block_Unreal5.6_clean.glb` in a fresh Studio: 337 frames,
  94 bones, ~30 fps, spikes 41 -> 39 on the already-cleaned result.

Fixes found on the way:
- **Export name.** Every take exported to `studio_export.glb`, so a second
  take's export would replace the first take's. The default destination is
  now `<build>/<take stem>_clean.glb`.
- **Animation label.** The export review labelled the animation with the
  requested name (default "jab") even when the take had none by that name.
  It now uses the loaded animation's own name ("Unreal Take").
- **Report animation name.** Both reports wrote an empty animation name,
  including the earlier boxer report: a `cstr` global converted to `sview`
  gave an empty view. The name is now passed as an explicit byte view;
  the report reads `"name": "Unreal Take"`.
- **Balance note.** "Comparison unavailable: The first balance measurement
  is unavailable." now reads "Balance could not be measured on the original
  take, so it cannot be compared. Check the feet by eye." (the JSON
  comparison reason too; `studio_export_report` updated and passing).
  Why balance cannot be measured on this 94-bone Unreal rig is still open.
