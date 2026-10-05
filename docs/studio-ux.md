# Studio UX audit (Phase 6, "professional and easy to use")

Rules behind every decision: the user never loses work, every edit can be
undone, every action is discoverable (a label, a tooltip or the `?` sheet), and
the logic behind the chrome is a proved kernel (`src/studio/chrome.elisa` and
`chrome_laws.elisa`, plus `test/studio_session.elisa`).

Verification: the File menu policy and laws prove with zero open obligations;
`test/studio_file_policy.elisa` passes; the studio compiles with
`STUDIO_SKIP_CHECKS=1 scripts/build_studio.sh`; and
`ELISA_PROOF=../elisa-proof-worktrees/integration-20261004/build/elisa-proof scripts/check.sh`
passes all 39 runtime tests, CLI checks and the 97-file proof baseline. The
window was not inspected on screen. Layout, colours and tooltip placement
still need a visual check.

| # | Audit item | Before | Decision / outcome |
|---|---|---|---|
| 1 | First-run state | Blank grey views | `chrome_screen`: if no take is loaded, the views show "Open a take to start", the command line to use, and "press A / ?". If loading fails, a separate failed screen appears (red). |
| 2 | File Open / Save / Export | Take path only from argv; export to `build/studio_export.glb` | Native panels and AppKit file drops handle the operations. The engine's `FilePanel` (`elisa-engine-mocap` `native/file_panel_appkit.m`, `src/ui/file_panel.elisa`, mocap-track 8e998bc6) wraps NSOpenPanel and NSSavePanel. A labelled sidebar **File** menu now exposes Open Take, Open Session, Save Session, Save Session As, Export Cleaned GLB and Export As; it supports pointer selection, Up/Down, Enter/Space and Escape. These rows share the native actions used by shortcuts, and availability/action mapping is proved in `StudioFilePolicy` with a headless test. **Cmd-O** or dropping one local file opens a take (.glb): the file is read first, and a file with no animation leaves the current take untouched. Otherwise every per-take cache, the playhead, the gizmo and the undo history start fresh, so undo never reaches into another take. **Cmd-S** saves the session in place and **Cmd-Shift-S** saves it as (.txt). **Cmd-Shift-O** opens a session. **E** exports in place and **Cmd-E** exports as (.glb). The status line names the file. Every opened, saved or exported file is registered with macOS recent documents. The chords are proved (`StudioShortcuts::o_chord`, `s_chord`, `e_chord` and seven laws). The AppKit drop hook validates the active window and copies its borrowed path into app-owned storage. An in-app recents menu is still deferred. Panels, menu interactions and drops still need on-screen exercise. |
| 13 | Dirty document replacement and close | Dirty marker, but replacing a take or closing the window could discard edits | **Cmd-O**, toolbar Open, file drop and Open Session stage the selected path and show Save and Open / Discard and Open / Cancel when the session is dirty. Native window close uses Save and Close / Discard and Close / Cancel; **Cmd-Q** reaches AppKit's termination decision and uses Save and Quit / Discard and Quit / Cancel. A failed save keeps the prompt and edits in place. Escape and keyboard focus navigation are supported; prompt choice/navigation rules have contracts, laws and `test/studio_replacement.elisa`. These modal paths still need on-screen review. |
| 3 | Labelled toolbar, tooltips with shortcuts | Icons only | Hovering any toolbar button shows its name and shortcut (`StudioPanels::tip_of`). The A / Auto action is labelled as Fix all with the boxing preset; the toolbar shows a "? shortcuts" hint. |
| 4 | Shortcut sheet | None | `?` (Slash) toggles a grouped sheet: Playback, Editing, File, View, plus the Escape rule. While the sheet is open, other keys are ignored. `help_after` is proved. |
| 5 | Readable op names, slider units | Op names and strengths shown as before | Done. Each stack row shows its parameter with a unit: passes (×), frames with ms, or a ±° wring limit. The sidebar shows before/after spikes, balance-impossible frames, foot slide and sink, and hand slide; distances are in mm. It also shows the foot/hand toggles and blend in frames. While dragging, the status bar shows the rotation in ° and the move in mm; nudges echo the new value. Unit choice is proved in `chrome.elisa` (`param_unit`, `wring_degrees`); readout maths was previously tested in `test/studio_units.elisa`. |
| 6 | Visual hierarchy | Status text crammed into the toolbar | Toolbar is for actions, the views and curves for content, the timeline for time, the sidebar for the stack, and the status bar for state and messages. Messages use the accent colour and headings are bold. |
| 7 | Status bar | None | Bottom bar shows: frame N / count (1-based), time `s.mmm`, fps, the selected operation, the last clean gain, and the last message. |
| 8 | Non-blocking feedback, safe defaults, full undo | Status line; default stack is the boxing preset | All feedback goes to the status bar, with no modal dialogs, except the system open and save panels, which open only when asked for (row 2). Defaults are unchanged (boxing preset, feet on, hands off). Fix all and loading a session are history commits, so Cmd-Z undoes them. |
| 9 | Escape always cancels | Escape only cancelled a gizmo drag | `escape_layer` peels exactly one layer per press: help sheet, gizmo drag, contact press, gizmo mode, then the selection. The order is proved, and the test checks that 4 layers are peeled. |
| 10 | Save/load session | None | `src/studio/state/session_state.elisa`: a text format (`mocap-studio session 4`) that saves feet and hand toggles, blend, operations, contact edits and gizmo corrections (tag 4: quaternion in millionths, translation in micrometres). Tag 6 records a two-residue fingerprint of the original GLB bytes, selected animation index, source frame count and document-node count. V4 restore rejects missing, duplicate or mismatched identity metadata. Versions 1 through 3 can still be parsed by the migration API, but the studio refuses to restore them until the user explicitly approves a legacy migration; that UI path remains open. On load, scopes are clamped, quaternion and offset values are clamped (`StudioChrome::session_clamp`) and the quaternion is re-normalised, corrections on missing nodes are dropped, unknown or damaged lines are skipped, and unsupported headers are refused. Saves write a unique same-directory temporary, check fwrite/flush/fsync/close, then atomically rename; failures remove the temporary and preserve the existing session. The status line distinguishes unreadable files, legacy files without source identity, and source/animation/rig mismatches. |
| 11 | One-click "Fix all" + metrics | Preset existed only as the initial stack | The A key or the Auto button applies the boxing preset with foot and hand locks as one undoable edit. The sidebar shows before/after spike count, balance-impossible frames, foot slide/sink and hand slide; the status bar retains the last slide and spike gain. |
| 12 | Focus loss during a gesture | Modifier keys cleared; a lost pointer-up could leave a drag active | `FocusLost` clears modifiers, camera/scrub/contact/gizmo/retime drags, cancels an unfinished range or numeric entry, and restores the retime slider's starting value. The pure transition has contracts and laws in `src/studio/focus.elisa` / `focus_laws.elisa`, with `test/studio_focus.elisa`. Native event delivery still needs an on-screen check. |

## Icons

The user approved Lucide (ISC). `lucide-static` 1.49.0 came from the npm
tarball. Only the 26 SVGs the studio uses, plus `LICENSE`, are vendored in
`assets/icons/lucide/`, and `SOURCE.txt` records where they came from.

`assets/icons/custom/` holds six hand-authored icons in the same 24 px,
2 px-stroke style: foot fix, contacts, pivot, spike, retime and trails.

elisa-ui draws strokes, not SVG or bitmaps. `tools/svg_icons.py` therefore
flattens every path, arc, circle and rect into line segments and writes
`build/generated/studio_icon_paths.elisa`; `scripts/build_studio.sh` runs it
before compiling. Each icon is held to 20 segments or fewer by
Douglas-Peucker simplification, so 18 toolbar icons cost about 360 of the
1024 draw commands elisa-ui allows per frame.

`test/studio_icons.elisa` checks headless that every icon code draws, stays
inside its box and meets the budget. Tooltips keep the text labels and
shortcuts.

Verified headless only: the geometry was rasterised offline from the
generated segments into `build/generated/icon_preview.png` and inspected
there. The on-screen toolbar has not been inspected (no desktop
screenshots).
