# Dependency revisions

| Dependency | Worktree | Branch | Revision | Provides |
|---|---|---|---|---|
| Elisa-engine | `../elisa-engine-mocap` | `mocap-track` | `795b3c57` | glTF token arrays renamed `json_tokens` (studio links with elisa-ui), MotionQuat `between`/`angle` (limb re-solves), M06 GLB document, M02 long clip + pose override, M07 pipeline, M01 viewport, M03 skeleton, M05 overlays, M04 gizmos |
| elisa-ui | `../elisa-ui-mocap-viewport` | `mocap-viewport` | `46e217f` | hosted engine surfaces in AppKit canvas panels |
| elisa-proof | `../elisa-proof-mocap` | `mocap-cleaner-proofs` | `36ed514` | refinement types, disjunctions (G4, G13), relational `%` and `/` |

## Blockers

- Phase 2 (studio UI): the installed stage-1 compilers are older than the
  elisa-ui sources; even elisa-ui's `examples/hello` fails to build. The
  hosting code type-checks and its policy/native tests pass (see
  `elisa-engine-mocap/docs/ui-hosted-surface.md`). The UI build waits for a
  compiler update.
- Viewport: no skinned mesh drawing and no text yet; labels come from the host UI.
