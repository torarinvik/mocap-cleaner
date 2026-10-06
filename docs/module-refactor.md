# File size refactor queue

Start after the current correctness fixes. Every repository file must fit
within 600 lines. Generated build artifacts and external dependency checkouts
are outside this repository source inventory.

## Inventory (2026-10-06)

| File | Lines | Proposed responsibility boundaries |
| --- | ---: | --- |
| `src/studio/app/app.elisa` | 5370 | Application state and lifecycle; document loading; viewport; corrections; sessions; storage inventory and actions; accessibility publication; input dispatch. |
| `src/studio/app/panels.elisa` | 2039 | Shared geometry; import and export dialogs; storage screen; correction panels; timeline and viewport overlays. |
| `src/ops/rig_stack.elisa` | 1000 | Shared stack types; individual correction evaluators; validation; composition and dispatch. |
| `src/cli/main.elisa` | 886 | Argument parsing; command handlers; output formatting; entry point. |
| `IMPLEMENTATION_PLAN.md` | 779 | Keep the roadmap index and move detailed milestones into linked documents. |
| `docs/proof-gaps.md` | 720 | Keep an index and split gap records into linked topic documents, preserving identifiers. |
| `src/tools/track.elisa` | 696 | Track representation; sampling and interpolation; transforms and export helpers. |

## Refactor acceptance

- Extract cohesive responsibilities, preserving current behavior and source
  take immutability. Each small extraction gets its own commit.
- Keep public APIs small. Internal state and implementation helpers stay
  private; use nested modules where they clarify ownership.
- Preserve contracts and proof laws. Update include paths and proof discovery
  for extracted files; do not weaken a baseline to accommodate extraction.
- Update build and tool entry points, documentation links and callers.
- Recount every tracked text file after refactoring and ensure none exceeds
  600 lines. Keep new files below that limit as work continues.
- Verify builds and the authorized check suite at integration boundaries;
  native UI evidence remains necessary for UI behavior acceptance.

## Studio extraction design

Use Elisa's `extend Studio:` declarations for cohesive parts of the same
application module. This preserves callback and state ownership without
turning shared globals into a public integration API. Move global state to a
small declaration module; keep state and internal operations private. The
public boundary consists of the startup setters and the native callback
entrypoints used by `app/main.elisa` and the canvas bridge. Split state further
by responsibility if it approaches 600 lines.

Extract path ownership, character/view hosting, issue navigation, correction
editing, contact drafts, sessions/replacement, export review/publication,
storage persistence, storage inventory, storage Move/Restore, storage batch
control, accessibility publication, pointer input, keyboard input and rendering
as separately named responsibilities. Keep each extracted file below 600
lines; split accessibility by screen and input by gesture where needed. A
small `app.elisa` composition root includes these parts and hosts callbacks.

Use the same module-extension approach for `StudioPanels` where its `Box` type
and action codes must retain their namespace. Keep `StudioDraw` and
`StudioIcons` separate. Extract storage, file/export dialogs, correction
controls and timeline/curve rendering; shared geometry stays in a small module.
Private helpers stay private even when another part of the same module uses
them. Avoid a new public forwarding function for every former helper.

## Track and rig extraction design

Keep `Track` and `RigOps` public types and established entrypoints in place.
Extract track sampling/fixed-point support, filters, contact/seam/limit tools
and plant evaluation. Extract rig schema/range helpers, twist/pole evaluation,
leg/contact evaluation, hand evaluation and stack dispatch. Shared leg and
hand IK helpers need a separate internal responsibility to avoid include
cycles. Check all direct helper consumers before reducing visibility.

Flat `src/tools/track_*.elisa` and `src/ops/rig_*.elisa` paths remain visible to
the current proof-root glob. Studio's nested paths are reached through
includes; preserve that graph. New source roots need explicit proof evidence
and baseline entries, while existing contracts and law names stay stable.

## CLI and documentation extraction design

Keep CLI output safety ahead of this extraction. Move argument decoding into
`CliArguments`, output formatting into `CliOutput`, and leave dispatch and
worker coordination in the entrypoint. Parsing and escaping internals are
private; callers receive only the operations and formats they need.

Split the implementation roadmap into a short index with linked milestone
details. Split proof-gap records by topic, retaining every gap identifier and
updating local links. These are documentation moves, not completion claims.
