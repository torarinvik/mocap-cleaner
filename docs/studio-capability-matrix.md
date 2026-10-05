# CLI and studio capability matrix

Updated 2026-10-06 from `src/cli/main.elisa`, `src/studio/app/`,
`src/studio/state/`, `src/ops/` and the existing studio UX notes. This is a
code-reading inventory, not an on-screen usability sign-off. “Available” means
there is a reachable product path in the current source; headless coverage or
an internal kernel by itself does not make a feature available to an animator.

## Take lifecycle and output

| Task | CLI | Studio | Gap that matters to the user |
|---|---|---|---|
| Open an animated GLB | `clean` accepts a path; `batch` accepts GLBs or folders. It now rejects malformed and animationless inputs before publishing output. | Open, file drop and default-path launch exist; the previous document stays protected through replacement flow. | No staged import progress, in-product animation chooser or clear setup review. Studio animation defaults to `jab`, then falls back to the first animation if that name is missing. |
| Choose animations | `clean --anim NAME` restricts work to one named animation; without it the take's usable animations are processed. Reports include clip rows. | One animation is loaded at a time; there is no visible animation list or chooser yet. | Name, duration, sample rate, channel count and empty/duplicate animation warnings are not presented as an import decision. |
| Choose a cleanup preset | `--preset boxing|raw|rokoko`. | Auto/Fix all applies the boxing preset. | No visible preset/source selector or recommendation preview. The studio's current automatic behavior is boxing-specific. |
| Export one take | Writes a GLB, can write JSON with `--report`, and supports a chosen animation name. | Export to a reviewed path under `build/`, with source-collision checks, reload/byte validation, atomic publication and JSON/text quality sidecars. | Export dialogs and failure branches still need minimum-size review. Reports currently omit full operation/rig parameters, tool versions, detector thresholds and detailed retime provenance. |
| Process a folder / compare reports | `batch` sorts inputs, supports worker jobs, outputs GLBs plus HTML; `diff` compares JSON reports and can emit HTML. | No batch queue or report comparison surface. | Studio lacks selection, queue, per-take outcome recovery and batch review. |
| Reproduce a run | `--save-ops` and `--ops` persist/restore operation records; JSON/HTML reports include quality findings and timing. | Session v4 binds editable state to source identity and saves operations, contact edits, retime bands and corrections. | No reusable named rig profile or recipe browser, recipe compatibility review, report export/side-by-side report diff or audit trail for all assumptions. |

## Cleanup and review controls

| Capability family | CLI | Studio | Current user-facing limitation |
|---|---|---|---|
| Channel filters | Six kernel types exist: despike, smooth path, median, wring limit, seam close and contact pin. The built-in presets use subsets; the CLI has no standalone flags for arbitrary curve-stack construction. | Add buttons expose five: Despike, Smooth, Median, Wring and Seam. Rows support select, enable, move, remove, strength and scope editing. | Contact pin is not in Add; parameters and frame scope have limited direct editing; no complete search, labelled inspector, role/joint scope editor, fade/boundary inspector or reset-to-default action. |
| Rig cleanup | `--op twist|pole|pelvis|lock|pivot|hands`, with pins, offsets, keyed offsets, explicit foot/hand contacts and retime flags. | Foot/hand cleanup toggles; contact interval editor; retime bands; viewport gizmo corrections. | Existing pins, twist/pole/pelvis controls, editable correction layers, advanced anchors and tool prerequisites have no complete inspector. |
| Physics analysis | Balance, ballistic and momentum checks are selectable with `--op`; batch always includes report detectors. | Aggregate spike findings have previous/next/worst navigation, detector/subject/severity/status filters, reset and analysis-scoped ignore/restore. The visible list is one row; exact peak/value/threshold are retained and stale navigation is gated. | The most recent failed-load screen did not show the filter chips, and a valid-take interaction pass is still needed. Findings remain aggregate spikes: per-bone families, source/result readings, uncertainty and detector details are open. |
| Contact editing | `--contact` and `--hand-contact` author explicit intervals. | Plant, Lift, Reset, Delete, Merge and Split action paths; first/last 1-based frame fields for authored intervals; whole-interval and endpoint keyboard nudges; history-backed edits with help and status guidance. | Timeline zoom/pan, accessible alternatives for row/range selection and numeric frame fields, anchor surface controls, source-versus-authored confidence and boundary visual review remain open. |
| Local pose repair | `--pin`, `--offset` and piecewise `--keyed` options. | Drag gizmo creates keyed local correction; undo/redo and session persistence exist. | No full key list, exact numeric transform, local/world editor, default fade control, constrained/nudge controls or complete pin inspector. |
| Retiming | `--retime` specifies source range, speed and blend; report maps frame timing. | Selection drag, speed presets/slider/typed speed, up to eight bands, history and session persistence. | Need exact source/output numeric ranges and durations, contact/key mapping review, accessible band editing and clear separation among play loop, work range, scope and retime. |
| Compare and quality | JSON report plus `diff` can compare metric names and thresholds. | Source/result curves and metric readouts; export warning acknowledgement. | No synchronized viewport comparison, persistent accessible compare switch, local issue loop, peak-to-peak navigation or preservation/regression summary per proposed step. |

## Existing report coverage and implementation direction

- The shared CLI/engine stack is the source of cleanup semantics. Prefer
  exposing supported operations through studio state and inspectors rather
  than creating a second cleanup implementation.
- Studio edit history currently stores whole stack snapshots; authored state
  is session-persisted. Every visible adjustment should either be transient
  preview or one intentional, undoable history transaction.
- Current displayed metrics include spike counts, balance-impossible frames,
  foot slide/sink and hand slide. CLI report code additionally has rig and
  physics findings and per-stage/per-operation timing. Keep labels and units
  consistent when studio consumes those results.
- The current issue browser is an aggregate spike slice, not a complete issue
  system. It intentionally reports no joint subject for that detector and
  does not yet cover the CLI's rig and physics finding families.
- The UI should expose missing prerequisites inline, keep unavailable actions
  inspectable with a short reason, and preserve the source/result distinction.
  Do not imply that aggregate improvements prove every interval was improved.
- This matrix closes only the code inventory portion of M0. It does not close
  the running-window exercise, animation UX, benchmark corpus, visual review,
  or any milestone acceptance gate in `IMPLEMENTATION_PLAN.md`.

## Partial running-window review

On 2026-10-05, I opened the current build with the external
`black-boxer.glb` / `jab` take on a 2880 × 1800 display. The audit capture is
`build/studio-audit-current.png` (local build output, not a benchmark input).
The first capture showed the cleanup readout drawn over the sidebar's
ranked-findings heading, status, navigation buttons and empty-state text. A
proved sidebar layout policy now separates those sections, and the follow-up
capture at `build/studio-audit-sidebar-fixed.png` confirms the metrics, finding
controls and operation stack are legible at this display size. Redundant inline
shortcut lists were removed; the visible shortcut sheet and toolbar tooltips
remain. This is one partial window review; file panels, dialogs, small-window
behavior, keyboard-only use, VoiceOver and other journeys remain unreviewed.

The first shortcut-sheet capture showed its text dimmed beneath the native
hosted viewport surfaces. A proved modal policy now removes all three hosted
layers while the shortcut sheet or another blocking canvas dialog is active.
The 2026-10-05 help-sheet capture at `build/studio-modal-help2.png` shows the
complete sheet unobscured; after toggling it closed, the capture at
`build/studio-modal-restored2.png` confirms all three animated viewports
return. The temporary blank view regions while a modal is open are intentional.
Other modal types, window sizes and keyboard/focus flows still need individual
review.

Opening Export Review with **E** found three summary rows cut off at the former
48-byte `StudioText` slot, even though the dialog had room to show them. The
slot now allows 128 bytes, and
`build/studio-audit-export-review-fixed.png` confirms the selected animation,
source/output timing and cleanup settings are complete at 2880 × 1800. The
destination and Export button were not activated; no export was written.
`test/studio_text.elisa` protects the long-label case. Small-window wrapping
and exceptionally long animation names still need review.

The 2026-10-05 follow-up build includes issue filters and per-analysis
ignore/restore. In the failed-load window, the revised sidebar no longer
overlaps its empty-state message with navigation, but the filter chips were
not visible. The folder control also did not open the native take picker in
this attempt. No source take was opened or changed, so filter appearance,
hit-target behavior, native accessibility actions and contact nudge shortcuts
still need review on a valid take.

### 2026-10-06 valid-take supplement

Built the current `main` source at `1b25338` with
`STUDIO_SKIP_CHECKS=1 scripts/build_studio.sh`, refreshed the generated UI
smoke app, and opened the read-only `black-boxer.glb` / `jab` fixture at
2880 × 1800. The build completed with the script's warning that the optional
`studio-globals` Stage 1 compiler was unavailable. The rig, metrics, findings
panel and operation stack rendered; no session or export was saved.

The operation-stack heading visibly labels **Duplicate** and **Reset…**.
Pointer Duplicate inserted an adjacent copy, selected it, updated the visible
metrics and reported the undo affordance; one undo restored the original
three-operation stack. The Reset popover showed all three distinct scopes.
Clear contacts and Clear local corrections were visibly disabled when empty;
Restore source result was enabled, and clicking outside dismissed the menu.
The CUA `super+D` gesture toggled the selected operation, while `super+O`
changed its scope to frame 0. These gestures appear to have reached the
plain-key actions, so this run does not establish native Command-chord behavior
or text-entry ownership. Both temporary edits were undone or discarded by a
fresh launch. No file was saved, and the source stack was restored.

Pressing Escape while the Reset popover was open closed the Studio window in
this run instead of dismissing only the popover. The running-window review
therefore fails the Escape requirement and needs a back-routing fix or a
verified native event path before sign-off. Minimum-window layout, native
VoiceOver activation, filter interaction, and the broader take workflow are
still open. This supplement supersedes the earlier failed-load-only note for
Reset and Duplicate visibility; it does not close the full M0 exercise.
