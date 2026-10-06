# Mocap Studio (Phase 2)

An interactive window for cleaning one clip. It shows three engine viewports, a curve view, a timeline and the operation stack. Open a take with the toolbar's folder button, **Cmd-O**, or by dropping one GLB onto the window. Once a take is loaded, the sidebar's labelled **File** menu provides take/session open, session save and cleaned GLB export actions. Every stack edit uses the same operation pipeline that the CLI exports, so the reviewed result and exported result share cleanup semantics.

```
scripts/build_studio.sh                      # build, run studio tests, prove kernels
build/mocap_studio [clip.glb [animation]]    # default: boxing black-boxer.glb, "jab"
open build/MocapStudio.app                    # launch the current Finder bundle
```

The build also creates `build/MocapStudio.app` with a Finder bundle identifier,
display name, version and executable. Its `Contents/Resources/BUILD-INFO.txt`
records dependency revisions, worktree state, a build-input fingerprint and
SHA-256 hashes for the executable and runtime object. This is a local
development bundle; signing, notarization, an application icon and release
distribution remain open.

For compilation and packaging without running the separate Studio test suite,
use `STUDIO_SKIP_CHECKS=1 bash scripts/build_studio.sh`. Each build prepares a
fresh `build/studio-build.*` generation containing native objects, the executable
and `inputs.json`. The manifest records the transitive Elisa sources, native
sources and local headers, build recipes, compiler/runtime products and native
tool hashes, plus SDK path/version. Inputs are compared before linking and
publication; the completed manifest also binds the executable's SHA-256.
`build/mocap_studio` points to the published generation. Failed compilation or
linking preserves the previous executable.

Packaging checks the sealed manifest and the copied executable, then includes
`Contents/Resources/BUILD-INPUTS.json`. `BUILD-INFO.txt` distinguishes that record
from observations made during packaging. A direct package call without a
manifest is labelled unrecorded. Previous bundles remain in
`build/studio-package.*/previous.app`; ordinary failures and handled INT/TERM
interruptions restore the previous bundle when publication has not completed.
An unhandled process kill or machine failure can leave that backup needing
manual restoration. These generated directories are retained for recovery;
review them before removing old generations.

The input comparisons observe files at specific times; they do not detect a
file changed and restored between observations, and they do not hash the whole
SDK. A sealed build record establishes the recorded inputs and product binding,
not native interaction or motion-quality acceptance. The new staging and
restoration paths have Bash syntax checks; successful current integrated builds
and failure/interruption exercises remain qualification work.

## Layout

| Area | Contents |
|---|---|
| Toolbar | play/pause, step, speed (1x, 1/2x, 1/4x), loop, undo/redo, overlay toggles, frame, open take, export, balance overlay and Fix all. Hover a button for its label and shortcut. All icons are drawn in code. |
| Views | perspective (top), front and side (bottom). Drag orbits, right-drag pans, scroll zooms, a click picks a joint (it drives the curve view), F frames. |
| Curves | the picked bone's rotation channel (translation if it has none). Each component is shown dim for the source and bright for the cleaned clip. |
| Timeline | 1 s ruler, source spike strip, cleaned problem markers coloured by severity, left/right foot and hand contact bars, retime bands, the selected operation's scope band, and the playhead. Click or drag to scrub. Clicking a contact row selects and scrubs to that exact frame without editing; Plant/Lift buttons and Shift-P/Shift-L apply undoable one-frame overrides. Reset or Shift-U restores automatic detection at the selected frame when an authored override exists. The contact editor shows the full authored interval range before Delete or Shift-Delete removes it; the status line confirms the range, and undo restores it. Merge is enabled only when the selected authored interval touches another interval with the same side and state; it preserves the resulting contact track and can be undone. Split divides the newest interval immediately before the selected frame, which begins the right interval; both pieces keep the same state and contact output, and the action is undoable. Split is disabled at the selected interval's first frame or when the edit list is full. Drag a run endpoint to change its extent. Retime selection uses Shift-drag. |
| Sidebar | File menu; clip and cleanup metrics; history position; add buttons (Despike, Smooth, Median, Wring, Seam); and one row per operation with enable, up/down and remove. The File menu supports pointer use, Up/Down navigation, Enter/Space activation and Escape dismissal. |

The status bar adds `* Unsaved changes` when the current cleanup stack differs from the last successfully saved session snapshot. Undoing or redoing back to that snapshot clears the marker. Opening another take or loading a session over unsaved changes opens a Save and Open / Discard and Open / Cancel prompt; Escape cancels, and Save keeps the prompt open if the session write fails. Closing the window and Cmd-Q use Save and Close / Discard and Close / Cancel or Save and Quit / Discard and Quit / Cancel. These native-window paths still need on-screen review. Export writes the cleaned animation; it does not save the editable session.

Session files use `mocap-studio session 4`. They bind edits to the original GLB bytes, selected animation index, source frame count and document-node count. Optional tag 7 records each retime band's source-frame range, speed in permille, blend length and enabled state. Invalid, overlapping, out-of-range or over-capacity bands are skipped as whole records. A source, animation or rig mismatch is refused with an explanation. Versions 1 through 3 have no source identity, so opening one first shows a compatibility warning. Cancel leaves the current cleanup untouched; Load is only for a session known to match the open take and rig. If the current cleanup has unsaved edits, the usual Save, Discard or Cancel prompt follows. After loading, inspect affected joints and contacts; saving the session writes the current v4 identity. Session saves use an atomic temporary-file-and-rename flow. Exports require a canonical destination below `build/`, reject source and hard-link collisions, symlink destinations and non-files, and confirm replacement before publication. Studio writes a unique sibling temporary, flushes and reloads it, checks exact bytes against the cleaned document, rechecks the destination and atomically renames the result. A review dialog names the selected animation and index, shows included/unchanged clips and output/source timing, lists each active operation with its setting, and reports that no reusable rig profile is saved, the source hierarchy is retained, no retargeting is performed, and root-motion conversion is unavailable. It also shows quality warnings; acknowledgement gates export. Select a warning row to inspect its matching before/after metric and any retained frame evidence. Previous/Next and keyboard arrows browse warning categories; Done or Escape returns to the same review and preserves its destination and acknowledgement. Frame references are zero-based output frames. Aggregate-only metrics say when they do not identify a frame. The destination has a compact preview and an **Inspect full path** control; that read-only view paginates the complete UTF-8 path into five lines, including the exact filename, with Previous/Next controls. Tab, arrows, Enter, Space and Escape work in the review, warning detail and path view. The 820 × 500 path view fits the supported 1100 × 720 minimum window. After successful commit, a result dialog shows the output and offers Open Result, Show in Folder and Done; it explains that the editable session is separate. Open Result uses the default GLB handler and Show in Folder reveals the file in Finder. Pointer, keyboard and native accessibility routes are implemented; exact warning-to-timeline issue navigation, minimum-size visual review and native VoiceOver exercise remain open.

## Keys

The keys include Space, Left/Right, S, L, Z/Y, T C H N G X M, F, E, 1-5, D, Delete, PageUp/PageDown, Up/Down, `[` `]`, B, and I/O, plus K (foot cleanup), J (hand cleanup), W (worst foot slide), **Shift-P** (plant selected contact frame), **Shift-L** (lift selected contact frame), **Shift-U** (restore automatic detection at the selected frame), **Shift-Delete** (remove the authored interval covering the selected frame), and `,` `.` (contact blend). **Cmd-Z** undoes and **Cmd-Shift-Z** redoes; plain Z/Y also work. File commands are available from the labelled File menu and as shortcuts: **Cmd-O** open take, **Cmd-Shift-O** open session, **Cmd-S** save session, **Cmd-Shift-S** save as, **E** export to the current path, and **Cmd-E** export as. Press `?` for the full shortcut sheet. Contact-row clicks select and scrub; Plant/Lift set a one-frame override, Reset removes only that frame from authored overrides, Delete removes the newest full interval covering it, Merge joins eligible adjacent intervals without changing contact output, Split divides the selected interval immediately before the selected frame, and dragging a run endpoint changes its extent. See `docs/foot-workflow.md`. Shift-F toggles the frame-time overlay; plain F frames the views.

The default export path is `build/studio_export.glb`; Cmd-E opens the native Save panel to choose another destination. The default session path is `build/studio_session.txt`. Both are derived files. Before publication, Studio reloads the temporary GLB and compares its complete document bytes with the reviewed cleaned document. If preparation fails, the status distinguishes a write failure, a reload failure and a reloaded document mismatch. This confirms file round-trip integrity; it does not measure motion quality. After the validated GLB is committed, Studio also writes `<export>.report.json` and `<export>.report.txt` sidecars atomically. If a sidecar fails, the GLB remains published and the status reports the report failure separately. The version 1 report contains available detector metrics, cleanup toggles, warnings and non-cryptographic source/output residues; it does not yet include tool versions, policy thresholds, full operation parameters or detailed retime provenance. See `docs/studio-export-report.md` for the format and limits. Atomic publication and path-collision policy have focused tests; result navigation and broader disk-failure qualification remain open.

## Code

| Path | Role | Checked by |
|---|---|---|
| `src/studio/{timeline,history,stack_policy,view,file_policy}.elisa` | proved integer kernels (frame/time/pixel maps, undo cursor, stack index moves, curve and severity mapping, File menu action availability) | elisa-proof, `*_laws.elisa` |
| `src/studio/export_policy.elisa` | proved canonical build containment and fail-closed destination decisions | `proof/studio_export_policy_laws.elisa`, `test/studio_export_policy.elisa` |
| `src/studio/app/export_publisher.elisa` | sibling-temp write, fsync, GLB reload and exact-byte validation before atomic rename | `test/studio_export_publisher.elisa`; full `scripts/check.sh` |
| `src/studio/state/*` | value-level state: timeline, operation stack, history ring, clip sampling | `test/studio_state.elisa`, `test/studio_clip.elisa` |
| `src/studio/app/model.elisa`, `scene.elisa` | loaded clip plus cleaned copy; 3D draw list (grid, ghost, onion, trails or heat, contacts, skeleton) | `test/studio_capture.elisa` (offscreen PNGs `build/studio_{perspective,front,side}.png`) |
| `src/studio/character_bind_policy.elisa`, `src/studio/app/character.elisa` | separate GLB skinned model binding by bare joint name, then rig role; unmatched joints inherit from the nearest bound skin ancestor or stay at rest; draws only at ≥500‰ direct coverage | `proof/studio_character_bind_laws.elisa`, `test/studio_character.elisa`; coverage monotonicity remains an acknowledged prover gap (G84) |
| `src/studio/state/perf_state.elisa`, `src/core/perf_cache.elisa`, `src/ops/rig_cache.elisa` | Phase 6 caches: edit window, windowed joint tracks and detectors, drag-chain preview, curve memo, rig-stack cache split at foot lock | `test/studio_perf.elisa`, `test/studio_rebuild.elisa`; `perf_cache` by `proof/perf_cache_laws.elisa` |
| `src/studio/app/{text,panels,app,main}.elisa` | 2D panels, input, window | loaded-window visual review at 2880 × 1600; headless tests; running AppKit accessibility tree |
| `src/studio/accessibility.elisa` | proved workspace/toolbar identities, tree relationships and toolbar action mapping | `proof/studio_accessibility_laws.elisa`, `test/studio_accessibility.elisa`, native AppKit tree and action review |

## Limits

- **Skinned mesh.** M toggles the imported skinned mesh where the GLB contains supported skin data. Skeleton-only takes remain viewable without a mesh. The on-screen rendering path still needs visual qualification across supported rigs.
- **Draw budget.** elisa-ui records at most 1024 draw commands per frame. To stay under it, curves are drawn as 40 segments per series and timeline markers are grouped into 120 bins.
- **Rebuild cost.** The take is loaded once (`StudioModel::Memo`). A stack edit copies it, reruns only the ops after the first changed one (per-channel `Ops::Cache`), and re-samples the joint tracks and spike detectors only over the edited frames (see `StudioPerf::edit_window`; a window reaching a short channel's last key runs to the clip end). Contacts and balance are still recomputed in full, and the rebuild still runs on the UI thread. On the jab (unoptimised) a correction rebuild drops from about 0.5 s to about 0.23 s.
- **Native window verification.** The loaded workspace was visually reviewed at 2880 × 1600, and a curve-label overlap was corrected. The AppKit tree exposes workspace landmarks, toolbar controls and live status; an accessible Loop action was verified and restored. Other interactive controls, irrelevant native actions on non-adjustable nodes, modal semantics, supported window sizes, native focus-loss delivery and all file-panel flows still need direct review.
