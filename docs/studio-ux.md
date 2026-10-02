# Studio UX audit (Phase 6, "professional and easy to use")

Rules behind every decision: the user never loses work, every edit can be
undone, every action is discoverable (a label, a tooltip or the `?` sheet), and
the logic behind the chrome is a proved kernel (`src/studio/chrome.elisa` and
`chrome_laws.elisa`, plus `test/studio_session.elisa`).

Verification: everything below is built and tested headless (prover, the
`test/studio_*` suite, and `scripts/build_studio.sh`). The window was not
inspected on screen. Layout, colours and tooltip placement still need a visual check.

| # | Audit item | Before | Decision / outcome |
|---|---|---|---|
| 1 | First-run state | Blank grey views | `chrome_screen`: if no take is loaded, the views show "Open a take to start", the command line to use, and "press A / ?". If loading fails, a separate failed screen appears (red). |
| 2 | File Open / Save / Export | Take path only from argv; export to `build/studio_export.glb` | **Save**: Cmd-S writes the session (see 10). **Export**: E, unchanged, is shown in the tooltip and the sheet. **Open**: Cmd-O reopens the saved session. A native file-open dialog is **deferred**. It needs an NSOpenPanel bridge, which belongs in the engine (`elisa-engine-mocap`, `mocap-track`) or elisa-ui, and neither was changed here. Takes still open from the command line. |
| 3 | Labelled toolbar, tooltips with shortcuts | Icons only | Hovering any toolbar button shows its name and shortcut (`StudioPanels::tip_of`). A labelled "Auto" button (clean with preset) was added, and the toolbar shows a "? shortcuts" hint. |
| 4 | Shortcut sheet | None | `?` (Slash) toggles a grouped sheet: Playback, Editing, File, View, plus the Escape rule. While the sheet is open, other keys are ignored. `help_after` is proved. |
| 5 | Readable op names, slider units | Op names and strengths shown as before | Not changed in this pass. The sidebar already names operations. The status bar now gives the time in seconds and the rate in fps. Units on the strength/edge controls are a follow-up. |
| 6 | Visual hierarchy | Status text crammed into the toolbar | Toolbar is for actions, the views and curves for content, the timeline for time, the sidebar for the stack, and the status bar for state and messages. Messages use the accent colour and headings are bold. |
| 7 | Status bar | None | Bottom bar shows: frame N / count (1-based), time `s.mmm`, fps, the selected operation, the last clean gain, and the last message. |
| 8 | Non-blocking feedback, safe defaults, full undo | Status line; default stack is the boxing preset | All feedback goes to the status bar, with no modal dialogs. Defaults are unchanged (boxing preset, feet on). The one-click clean and loading a session are history commits, so Cmd-Z undoes them. |
| 9 | Escape always cancels | Escape only cancelled a gizmo drag | `escape_layer` peels exactly one layer per press: help sheet, gizmo drag, contact press, gizmo mode, then the selection. The order is proved, and the test checks that 4 layers are peeled. |
| 10 | Save/load session | None | `src/studio/state/session_state.elisa`: a text format (`mocap-studio session 1`) that saves feet, blend, operations and contact edits. On load, scopes are clamped to the take, unknown or damaged lines are skipped, and a file without the header is refused. Gizmo corrections are not saved yet. |
| 11 | One-click "Clean with preset" + metrics | Preset existed only as the initial stack | The A key or the Auto button applies `StudioModel::initial_stack()` (boxing, feet on) as an undoable edit. The status bar then shows the slide and spike reduction (`clean_gain`, permille clamped to 0..1000). |

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
