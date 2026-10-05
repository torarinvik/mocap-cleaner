# Mocap Studio (Phase 2)

An interactive window for cleaning one clip. It shows three engine viewports, a curve view, a timeline and the operation stack. Open a take with the toolbar's folder button, **Cmd-O**, or by dropping one GLB onto the window. Every stack edit uses the same operation pipeline that the CLI exports, so the reviewed result and exported result share cleanup semantics.

```
scripts/build_studio.sh                      # build, run studio tests, prove kernels
build/mocap_studio [clip.glb [animation]]    # default: boxing black-boxer.glb, "jab"
```

## Layout

| Area | Contents |
|---|---|
| Toolbar | play/pause, step, speed (1x, 1/2x, 1/4x), loop, undo/redo, overlay toggles, frame, open take, export, balance overlay and Fix all. Hover a button for its label and shortcut. All icons are drawn in code. |
| Views | perspective (top), front and side (bottom). Drag orbits, right-drag pans, scroll zooms, a click picks a joint (it drives the curve view), F frames. |
| Curves | the picked bone's rotation channel (translation if it has none). Each component is shown dim for the source and bright for the cleaned clip. |
| Timeline | 1 s ruler, source spike strip, cleaned problem markers coloured by severity, left/right foot and hand contact bars, retime bands, the selected operation's scope band, and the playhead. Click or drag to scrub. Contact bars are editable; retime selection uses Shift-drag. |
| Sidebar | clip and cleanup metrics, history position, add buttons (Despike, Smooth, Median, Wring, Seam), and one row per operation with enable, up/down and remove. |

The status bar adds `* Unsaved changes` when the current cleanup stack differs from the last successfully saved session snapshot. Undoing or redoing back to that snapshot clears the marker. Export writes the cleaned animation; it does not save the editable session. The app does not yet warn before closing or replacing a take with unsaved session changes.

## Keys

The keys include Space, Left/Right, S, L, Z/Y, T C H N G X M, F, E, 1-5, D, Delete, PageUp/PageDown, Up/Down, `[` `]`, B, and I/O, plus K (foot cleanup), J (hand cleanup), W (worst foot slide), and `,` `.` (contact blend). **Cmd-Z** undoes and **Cmd-Shift-Z** redoes; plain Z/Y also work. File commands include **Cmd-O** open take, **Cmd-Shift-O** open session, **Cmd-S** save session, **Cmd-Shift-S** save as, **E** export to the current path, and **Cmd-E** export as. Press `?` for the full shortcut sheet. The timeline's foot and hand rows are editable: drag a contact's ends, click a run to lift it, and click a gap to plant. See `docs/foot-workflow.md`. Shift-F toggles the frame-time overlay; plain F frames the views.

The default export path is `build/studio_export.glb`; Cmd-E opens the native Save panel to choose another destination. The default session path is `build/studio_session.txt`. Both are derived files. Exports and session saves have not yet been qualified for atomic replacement, source-path collision handling or disk-failure recovery; see the active roadmap.

## Code

| Path | Role | Checked by |
|---|---|---|
| `src/studio/{timeline,history,stack_policy,view}.elisa` | proved integer kernels (frame/time/pixel maps, undo cursor, stack index moves, curve and severity mapping) | elisa-proof, `*_laws.elisa` |
| `src/studio/state/*` | value-level state: timeline, operation stack, history ring, clip sampling | `test/studio_state.elisa`, `test/studio_clip.elisa` |
| `src/studio/app/model.elisa`, `scene.elisa` | loaded clip plus cleaned copy; 3D draw list (grid, ghost, onion, trails or heat, contacts, skeleton) | `test/studio_capture.elisa` (offscreen PNGs `build/studio_{perspective,front,side}.png`) |
| `src/studio/state/perf_state.elisa`, `src/core/perf_cache.elisa`, `src/ops/rig_cache.elisa` | Phase 6 caches: edit window, windowed joint tracks and detectors, drag-chain preview, curve memo, rig-stack cache split at foot lock | `test/studio_perf.elisa`, `test/studio_rebuild.elisa`; `perf_cache` by `proof/perf_cache_laws.elisa` |
| `src/studio/app/{text,panels,app,main}.elisa` | 2D panels, input, window | builds only; it has not been checked visually |

## Limits

- **Skinned mesh.** M toggles the imported skinned mesh where the GLB contains supported skin data. Skeleton-only takes remain viewable without a mesh. The on-screen rendering path still needs visual qualification across supported rigs.
- **Draw budget.** elisa-ui records at most 1024 draw commands per frame. To stay under it, curves are drawn as 40 segments per series and timeline markers are grouped into 120 bins.
- **Rebuild cost.** The take is loaded once (`StudioModel::Memo`). A stack edit copies it, reruns only the ops after the first changed one (per-channel `Ops::Cache`), and re-samples the joint tracks and spike detectors only over the edited frames (see `StudioPerf::edit_window`; a window reaching a short channel's last key runs to the clip end). Contacts and balance are still recomputed in full, and the rebuild still runs on the UI thread. On the jab (unoptimised) a correction rebuild drops from about 0.5 s to about 0.23 s.
- **Native window verification.** The 2D panels and much of the interaction have headless tests. Focus loss now clears transient drags and is covered by proved policy and a headless test; delivery of the native event still needs on-screen review. Supported window sizes, accessibility exposure, and all file-panel flows also need direct on-screen review.
