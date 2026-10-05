# CLI and studio capability matrix

Updated 2026-10-05 from `src/cli/main.elisa`, `src/studio/app/`,
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
| Export one take | Writes a GLB, can write JSON with `--report`, and supports a chosen animation name. | Export to a reviewed path under `build/`, with source-collision checks, reload/byte validation and atomic publication. | Existing session and export flows need minimum-size, native file panel and failure branch review; full quality report integration is in progress. |
| Process a folder / compare reports | `batch` sorts inputs, supports worker jobs, outputs GLBs plus HTML; `diff` compares JSON reports and can emit HTML. | No batch queue or report comparison surface. | Studio lacks selection, queue, per-take outcome recovery and batch review. |
| Reproduce a run | `--save-ops` and `--ops` persist/restore operation records; JSON/HTML reports include quality findings and timing. | Session v4 binds editable state to source identity and saves operations, contact edits, retime bands and corrections. | No reusable named rig profile or recipe browser, recipe compatibility review, report export/side-by-side report diff or audit trail for all assumptions. |

## Cleanup and review controls

| Capability family | CLI | Studio | Current user-facing limitation |
|---|---|---|---|
| Channel filters | Six kernel types exist: despike, smooth path, median, wring limit, seam close and contact pin. The built-in presets use subsets; the CLI has no standalone flags for arbitrary curve-stack construction. | Add buttons expose five: Despike, Smooth, Median, Wring and Seam. Rows support select, enable, move, remove, strength and scope editing. | Contact pin is not in Add; parameters and frame scope have limited direct editing; no complete search, labelled inspector, role/joint scope editor, fade/boundary inspector or reset-to-default action. |
| Rig cleanup | `--op twist|pole|pelvis|lock|pivot|hands`, with pins, offsets, keyed offsets, explicit foot/hand contacts and retime flags. | Foot/hand cleanup toggles; contact interval editor; retime bands; viewport gizmo corrections. | Existing pins, twist/pole/pelvis controls, editable correction layers, advanced anchors and tool prerequisites have no complete inspector. |
| Physics analysis | Balance, ballistic and momentum checks are selectable with `--op`; batch always includes report detectors. | Balance and motion metrics are displayed as aggregate/readout overlays. A two-row ranked browser navigates aggregate spike intervals to exact peak frames and shows each peak value and threshold; stale rows are disabled. | The browser covers aggregate spikes only: no detector filters, per-bone findings, source/result readings, uncertainty, intentional-motion acknowledgement or analyzer details. |
| Contact editing | `--contact` and `--hand-contact` author explicit intervals. | Plant, Lift, Reset, Delete, Merge and Split action paths; contact states and selected frame; history-backed edits. | Timeline zoom/pan, exact numeric interval entry, accessible alternatives for row/range selection, anchor surface controls, source-versus-authored confidence and boundary visual review remain open. |
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
The character, three viewport panes, curves and timeline are visible, but the
sidebar's ranked-findings card is not usable: the cleanup readout is drawn over
its heading, status, navigation buttons and empty-state text. The same sidebar
also repeats most shortcuts inline even though the toolbar already offers a
shortcut sheet. Fix the findings/readout layout and remove redundant inline
shortcut clutter before marking this interaction reviewed. This is one partial
window review; file panels, dialogs, small-window behavior, keyboard-only use,
VoiceOver and other journeys remain unreviewed.
