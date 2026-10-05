# Mocap Studio (Phase 2)

An interactive window for cleaning one clip. It shows three engine viewports, a curve view, a timeline and the operation stack. Open a take with the toolbar's folder button, **Cmd-O**, or by dropping one GLB onto the window. Once a take is loaded, the sidebar's labelled **File** menu provides take/session open, session save and cleaned GLB export actions. Every stack edit uses the same operation pipeline that the CLI exports, so the reviewed result and exported result share cleanup semantics.

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
| Sidebar | File menu; clip and cleanup metrics; history position; add buttons (Despike, Smooth, Median, Wring, Seam); and one row per operation with enable, up/down and remove. The File menu supports pointer use, Up/Down navigation, Enter/Space activation and Escape dismissal. |

The status bar adds `* Unsaved changes` when the current cleanup stack differs from the last successfully saved session snapshot. Undoing or redoing back to that snapshot clears the marker. Opening another take or loading a session over unsaved changes opens a Save and Open / Discard and Open / Cancel prompt; Escape cancels, and Save keeps the prompt open if the session write fails. Closing the window and Cmd-Q use Save and Close / Discard and Close / Cancel or Save and Quit / Discard and Quit / Cancel. These native-window paths still need on-screen review. Export writes the cleaned animation; it does not save the editable session.

Session files use `mocap-studio session 4`. They bind edits to the original GLB bytes, selected animation index, source frame count and document-node count. A source, animation or rig mismatch is refused with an explanation. Versions 1 through 3 have no source identity, so opening one first shows a compatibility warning. Cancel leaves the current cleanup untouched; Load is only for a session known to match the open take and rig. If the current cleanup has unsaved edits, the usual Save, Discard or Cancel prompt follows. After loading, inspect affected joints and contacts; saving the session writes the current v4 identity. Session saves use an atomic temporary-file-and-rename flow. Exports require a canonical destination below `build/`, reject source and hard-link collisions, symlink destinations and non-files, and confirm replacement before publication. Studio writes a unique sibling temporary, flushes and reloads it, checks exact bytes against the cleaned document, rechecks the destination and atomically renames the result. A review dialog names the selected animation and index, shows included/unchanged clips and output/source timing, lists each active operation with its setting, and reports the source hierarchy, root-motion policy and quality warnings. Warning acknowledgement gates export. After successful commit, a result dialog shows the output and offers Open Result, Show in Folder and Done; it explains that the editable session is separate. Open Result uses the default GLB handler and Show in Folder reveals the file in Finder. Pointer, keyboard and native accessibility routes are implemented; full path inspection, rig/profile identity, warning-to-issue navigation, minimum-size layout and native VoiceOver exercise remain open.

## Keys

The keys include Space, Left/Right, S, L, Z/Y, T C H N G X M, F, E, 1-5, D, Delete, PageUp/PageDown, Up/Down, `[` `]`, B, and I/O, plus K (foot cleanup), J (hand cleanup), W (worst foot slide), and `,` `.` (contact blend). **Cmd-Z** undoes and **Cmd-Shift-Z** redoes; plain Z/Y also work. File commands are available from the labelled File menu and as shortcuts: **Cmd-O** open take, **Cmd-Shift-O** open session, **Cmd-S** save session, **Cmd-Shift-S** save as, **E** export to the current path, and **Cmd-E** export as. Press `?` for the full shortcut sheet. The timeline's foot and hand rows are editable: drag a contact's ends, click a run to lift it, and click a gap to plant. See `docs/foot-workflow.md`. Shift-F toggles the frame-time overlay; plain F frames the views.

The default export path is `build/studio_export.glb`; Cmd-E opens the native Save panel to choose another destination. The default session path is `build/studio_session.txt`. Both are derived files. Atomic publication and path-collision policy have focused tests; the active roadmap tracks export review, reports, result navigation and broader disk-failure qualification.

## Code

| Path | Role | Checked by |
|---|---|---|
| `src/studio/{timeline,history,stack_policy,view,file_policy}.elisa` | proved integer kernels (frame/time/pixel maps, undo cursor, stack index moves, curve and severity mapping, File menu action availability) | elisa-proof, `*_laws.elisa` |
| `src/studio/export_policy.elisa` | proved canonical build containment and fail-closed destination decisions | `proof/studio_export_policy_laws.elisa`, `test/studio_export_policy.elisa` |
| `src/studio/app/export_publisher.elisa` | sibling-temp write, fsync, GLB reload and exact-byte validation before atomic rename | `test/studio_export_publisher.elisa`; full `scripts/check.sh` |
| `src/studio/state/*` | value-level state: timeline, operation stack, history ring, clip sampling | `test/studio_state.elisa`, `test/studio_clip.elisa` |
| `src/studio/app/model.elisa`, `scene.elisa` | loaded clip plus cleaned copy; 3D draw list (grid, ghost, onion, trails or heat, contacts, skeleton) | `test/studio_capture.elisa` (offscreen PNGs `build/studio_{perspective,front,side}.png`) |
| `src/studio/state/perf_state.elisa`, `src/core/perf_cache.elisa`, `src/ops/rig_cache.elisa` | Phase 6 caches: edit window, windowed joint tracks and detectors, drag-chain preview, curve memo, rig-stack cache split at foot lock | `test/studio_perf.elisa`, `test/studio_rebuild.elisa`; `perf_cache` by `proof/perf_cache_laws.elisa` |
| `src/studio/app/{text,panels,app,main}.elisa` | 2D panels, input, window | loaded-window visual review at 2880 × 1600; headless tests; running AppKit accessibility tree |
| `src/studio/accessibility.elisa` | proved workspace/toolbar identities, tree relationships and toolbar action mapping | `proof/studio_accessibility_laws.elisa`, `test/studio_accessibility.elisa`, native AppKit tree and action review |

## Limits

- **Skinned mesh.** M toggles the imported skinned mesh where the GLB contains supported skin data. Skeleton-only takes remain viewable without a mesh. The on-screen rendering path still needs visual qualification across supported rigs.
- **Draw budget.** elisa-ui records at most 1024 draw commands per frame. To stay under it, curves are drawn as 40 segments per series and timeline markers are grouped into 120 bins.
- **Rebuild cost.** The take is loaded once (`StudioModel::Memo`). A stack edit copies it, reruns only the ops after the first changed one (per-channel `Ops::Cache`), and re-samples the joint tracks and spike detectors only over the edited frames (see `StudioPerf::edit_window`; a window reaching a short channel's last key runs to the clip end). Contacts and balance are still recomputed in full, and the rebuild still runs on the UI thread. On the jab (unoptimised) a correction rebuild drops from about 0.5 s to about 0.23 s.
- **Native window verification.** The loaded workspace was visually reviewed at 2880 × 1600, and a curve-label overlap was corrected. The AppKit tree exposes workspace landmarks, toolbar controls and live status; an accessible Loop action was verified and restored. Other interactive controls, irrelevant native actions on non-adjustable nodes, modal semantics, supported window sizes, native focus-loss delivery and all file-panel flows still need direct review.
