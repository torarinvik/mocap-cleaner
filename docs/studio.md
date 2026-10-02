# Mocap Studio (Phase 2)

An interactive window for cleaning one clip. It shows three engine viewports, a curve view, a timeline and the operation stack. Every stack edit re-runs the same `GlbTracks::clean_animation` that the CLI exports with, so what the window shows is what gets exported.

```
scripts/build_studio.sh                      # build, run studio tests, prove kernels
build/mocap_studio [clip.glb [animation]]    # default: boxing black-boxer.glb, "jab"
```

## Layout

| Area | Contents |
|---|---|
| Toolbar | play/pause, step, speed (1x, 1/2x, 1/4x), loop, undo/redo, overlay toggles, frame, export. All icons are drawn in code (no icon downloads). |
| Views | perspective (top), front and side (bottom). Drag orbits, right-drag pans, scroll zooms, a click picks a joint (it drives the curve view), F frames. |
| Curves | the picked bone's rotation channel (translation if it has none). Each component is shown dim for the source and bright for the cleaned clip. |
| Timeline | 1 s ruler, source spike strip, cleaned problem markers coloured by severity, left/right foot contact bars, the selected operation's scope band, and the playhead. Click or drag to scrub. |
| Sidebar | clip stats, history position, add buttons (Despike, Smooth, Median, Wring, Seam), and one row per operation with enable, up/down and remove. |

## Keys

The keys are Space, Left/Right, S, L, Z/Y, T C H N G X M, F, E, 1-5, D, Delete, PageUp/PageDown, Up/Down, `[` `]`, B, and I/O, plus the foot keys K (fix feet on/off), W (jump to the worst slide), and `,` `.` (carry blend). They are listed in the sidebar. The timeline's foot rows are editable: drag a contact's ends, click it to lift it, click a gap to plant. See `docs/foot-workflow.md`. Shift-F toggles the frame-time overlay (evaluate, detectors and draw times in µs, poses evaluated, ops rerun, bones moved by a drag); plain F still frames the views.

Export writes `build/studio_export.glb`.

## Code

| Path | Role | Checked by |
|---|---|---|
| `src/studio/{timeline,history,stack_policy,view}.elisa` | proved integer kernels (frame/time/pixel maps, undo cursor, stack index moves, curve and severity mapping) | elisa-proof, `*_laws.elisa` |
| `src/studio/state/*` | value-level state: timeline, operation stack, history ring, clip sampling | `test/studio_state.elisa`, `test/studio_clip.elisa` |
| `src/studio/app/model.elisa`, `scene.elisa` | loaded clip plus cleaned copy; 3D draw list (grid, ghost, onion, trails or heat, contacts, skeleton) | `test/studio_capture.elisa` (offscreen PNGs `build/studio_{perspective,front,side}.png`) |
| `src/studio/state/perf_state.elisa`, `src/core/perf_cache.elisa`, `src/ops/rig_cache.elisa` | Phase 6 caches: edit window, windowed joint tracks and detectors, drag-chain preview, curve memo, rig-stack cache split at foot lock | `test/studio_perf.elisa`, `test/studio_rebuild.elisa`; `perf_cache` by `proof/perf_cache_laws.elisa` |
| `src/studio/app/{text,panels,app,main}.elisa` | 2D panels, input, window | builds only; it has not been checked visually |

## Limits

- **Mesh toggle.** The toggle is stored but nothing is drawn. The mesh backdrop needs `ViewportScene`, which is on engine main but not on `mocap-track`.
- **Draw budget.** elisa-ui records at most 1024 draw commands per frame. To stay under it, curves are drawn as 40 segments per series and timeline markers are grouped into 120 bins.
- **Rebuild cost.** The take is loaded once (`StudioModel::Memo`). A stack edit copies it, reruns only the ops after the first changed one (per-channel `Ops::Cache`), and re-samples the joint tracks and spike detectors only over the edited frames (see `StudioPerf::edit_window`; a window reaching a short channel's last key runs to the clip end). Contacts and balance are still recomputed in full, and the rebuild still runs on the UI thread. On the jab (unoptimised) a correction rebuild drops from about 0.5 s to about 0.23 s.
- **Undo keys.** Undo and redo are plain Z and Y, with no Cmd modifier.
