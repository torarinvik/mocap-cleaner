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
