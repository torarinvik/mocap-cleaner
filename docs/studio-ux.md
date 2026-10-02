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

## Icons (proposed, NOT downloaded)

These are open-licence sets that cover the toolbar (play, step, loop, undo/redo,
trails, contacts, heat, onion, ghost, x-ray, mesh, frame, export, balance,
auto-clean):

- **Lucide**, ISC licence: a consistent 24 px stroke style and the largest coverage.
- **Tabler Icons**, MIT licence: about 5k icons, including bone, footprint and wand.
- **Phosphor**, MIT licence: six weights, which helps with toggle on/off states.
- **Material Symbols**, Apache 2.0 licence: a variable font with fill and weight axes.

For the domain-specific icons (contact bar, onion skin, foot plant), custom
AI-generated glyphs in the same stroke style were suggested. Nothing is fetched
until the user picks a set.
