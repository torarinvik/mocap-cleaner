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

The keys are Space, Left/Right, S, L, Z/Y, T C H N G X M, F, E, 1-5, D, Delete, PageUp/PageDown, Up/Down, `[` `]`, B, and I/O. They are listed in the sidebar.

Export writes `build/studio_export.glb`.

## Code

| Path | Role | Checked by |
|---|---|---|
| `src/studio/{timeline,history,stack_policy,view}.elisa` | proved integer kernels (frame/time/pixel maps, undo cursor, stack index moves, curve and severity mapping) | elisa-proof, `*_laws.elisa` |
| `src/studio/state/*` | value-level state: timeline, operation stack, history ring, clip sampling | `test/studio_state.elisa`, `test/studio_clip.elisa` |
| `src/studio/app/model.elisa`, `scene.elisa` | loaded clip plus cleaned copy; 3D draw list (grid, ghost, onion, trails or heat, contacts, skeleton) | `test/studio_capture.elisa` (offscreen PNGs `build/studio_{perspective,front,side}.png`) |
| `src/studio/app/{text,panels,app,main}.elisa` | 2D panels, input, window | builds only; it has not been checked visually |

## Limits

- **Mesh toggle.** The toggle is stored but nothing is drawn. The mesh backdrop needs `ViewportScene`, which is on engine main but not on `mocap-track`.
- **Draw budget.** elisa-ui records at most 1024 draw commands per frame. To stay under it, curves are drawn as 40 segments per series and timeline markers are grouped into 120 bins.
- **Rebuild cost.** Each stack edit rebuilds the clip: two loads, a clean and resampling. This takes about 1 s unoptimised and less at -O2. The window is unresponsive during the rebuild.
- **Undo keys.** Undo and redo are plain Z and Y, with no Cmd modifier.
