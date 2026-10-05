# Studio UX audit (Phase 6, "professional and easy to use")

Rules behind every decision: the user never loses work, every edit can be
undone, every action is discoverable (a label, a tooltip or the `?` sheet), and
the logic behind the chrome is a proved kernel (`src/studio/chrome.elisa` and
`chrome_laws.elisa`, plus `test/studio_session.elisa`).

Verification: the File menu, export destination and legacy-prompt policies
have laws and headless tests. The last full `scripts/check.sh` run on
2026-10-05 rebuilt and passed all 59 runtime tests and all four CLI checks.
The check exited 1 at the proof-baseline gate under semantic revision
`866d1320416958d`: it reports broad proved-to-unknown shifts, six existing
unproven-count increases, and missing reviewed rows for new proofs. Those
statuses have not been mass-rebaselined. The issue-filter policy and job
policy laws proved 57/57 and 109/109 obligations in this run. The issue
annotation, browser, accessibility and revised sidebar proofs still have
unsupported or open obligations; their limits remain visible in the reports.
The earlier sidebar layout source and laws had proved (2/2 and 6/6 obligations)
before its latest geometry adjustment. On
2026-10-05, I
inspected a loaded `black-boxer.glb` / `jab` studio window at 2880 × 1600
display pixels. That view exposed the curve bone label colliding with the
retime slider; commit `99a3d34` moved the selected-bone label into its own
row. The AppKit accessibility tree now exposes a named workspace, five region
groups, 19 toolbar controls and a live status node. Toolbar controls have
button or checkbox roles, shortcut-aware names, working action routes, toggle
values and correct disabled states for Undo/Redo. A CUA accessibility action
changed Loop from off to on and back, restoring the original state. After
rebuilding against elisa-ui commit `c9ff0b64`, a fresh native snapshot no
longer lists generic Increment/Decrement actions on semantic nodes; the
toolkit's AppKit bridge test also checks sliders allow these actions while
text fields and groups reject them. Operation rows, contact selection and
viewport selection still lack individual semantics. The timeline separately
exposes Plant, Lift, Reset, Delete, Merge and Split buttons with stable names,
selected-frame values, roles and native routes, but they have not yet been
exercised with VoiceOver. Focus announcements, guide screens, dialogs and
VoiceOver task completion remain open. File/menu flows, the legacy
warning, close prompts and minimum-size behavior remain unverified. A follow-up
2880 × 1800 capture loaded with `black-boxer.glb` / `jab` found and then
verified the fix for overlapping cleanup metrics and ranked-finding controls;
the sidebar's duplicate inline shortcut list was removed in favor of the
visible shortcut sheet. The M0 visual-exercise item remains open.

On 2026-10-06, the Reset popover and a labelled Duplicate action were added to
the operation-stack heading. Reset distinguishes clearing authored contacts,
clearing local corrections and restoring the source result; unavailable
actions are disabled, each accepted reset is one undo step, and Escape or a
click outside closes the popover. Duplicate inserts an exact copy after the
selected step, selects it, and records one undo step. The visible button,
`Cmd-D`, and a named native accessibility action share the same transition;
the button explains when no operation is selected or the stack is full. The
focused accessibility test passes. A current-source compile-only build was
opened with a valid take at 2880 × 1800. Pointer Duplicate inserted and selected
an adjacent copy, and one undo restored the original stack. Reset showed its
three scopes, disabled empty actions, and closed on click-away. The first run
exposed that Escape closed the window; commit `aaa5624` adds the Studio
workspace to the shared back-navigation stack, and a rebuilt run confirmed
Escape now closes Reset while keeping the window open. CUA modifier injection
did not verify native `Cmd-D`. VoiceOver activation, minimum-size layout and
the other Escape layers remain open.

The next live check found hosted 3D viewport layers covering the shortcut
sheet. The proved `StudioModalPolicy` now removes those layers beneath blocking
canvas dialogs. The complete help sheet is legible, and all three viewports
return after the `?` toggle closes it. Captures are recorded in
`docs/studio-capability-matrix.md`; replacement, legacy-session and export
dialogs remain to be reviewed on screen. The dedicated test passed, and both
the policy and laws proved (2/2 and 18/18 obligations).

Opening the export review then exposed summary rows silently truncated at 48
bytes. The fixed 128-byte text slots display the complete animation, timing and
cleanup details in the live capture; `test/studio_text.elisa` verifies the
entire long label survives formatting. The dialog was cancelled without
writing an export. This finding and capture are in
`docs/studio-capability-matrix.md`. The latest full check rebuilt and passed
all 59 runtime tests and all four CLI checks. It exited 1 because the
proof-baseline gate still reports the previously documented semantic shifts
and missing reviewed rows. A failed-load window review of the new finding
controls confirmed that navigation no longer overlaps the empty-state label,
but the filter chips were not visible and the take picker did not open; repeat
the interaction review on a valid loaded take before treating those controls
as verified.

| # | Audit item | Before | Decision / outcome |
|---|---|---|---|
| 1 | First-run state | Blank grey views | `chrome_screen`: if no take is loaded, the views show "Open a take to start", the command line to use, and "press A / ?". If loading fails, a separate failed screen appears (red). |
| 2 | File Open / Save / Export | Take path only from argv; export to `build/studio_export.glb` | Native panels and AppKit file drops handle the operations. The engine `FilePanel` wraps NSOpenPanel/NSSavePanel and exposes canonical-parent resolution, symlink/file facts, inode identity and a Cancel-default quick-export replacement alert (`elisa-engine-mocap` commits `c4c43e3d`, `ef1b0159`, `72a672cf`). A labelled sidebar **File** menu exposes Open Take, Open Session, Save Session, Save Session As, Export Cleaned GLB and Export As; it supports pointer selection, Up/Down, Enter/Space and Escape. These rows share the native actions used by shortcuts, and availability/action mapping is proved in `StudioFilePolicy`. **Cmd-O** or dropping one local GLB opens a take: the file is read first, and a file with no animation leaves the current take untouched. **Cmd-S** saves the session; **Cmd-Shift-S** saves as; **Cmd-Shift-O** opens a session. **E** exports to the current path and confirms before replacing it; **Cmd-E** uses the native Save panel. Destinations must resolve below `build/`; source/hard-link collisions, symlinks and non-files are rejected. Export is written to a unique sibling temporary, flushed, reloaded, byte-compared with the cleaned document, safety-checked again and atomically renamed. Only a validated committed export updates the recent-file list. `test/studio_export_policy.elisa` and `test/studio_export_publisher.elisa` cover the policy and round trip. Semantic review/report, Show in Folder/Open Result and native Save-panel/confirmation exercise remain open. |
| 13 | Dirty document replacement and close | Dirty marker, but replacing a take or closing the window could discard edits | **Cmd-O**, toolbar Open, file drop and Open Session stage the selected path and show Save and Open / Discard and Open / Cancel when the session is dirty. Native window close uses Save and Close / Discard and Close / Cancel; **Cmd-Q** reaches AppKit's termination decision and uses Save and Quit / Discard and Quit / Cancel. A failed save keeps the prompt and edits in place. Escape and keyboard focus navigation are supported; prompt choice/navigation rules have contracts, laws and `test/studio_replacement.elisa`. These modal paths still need on-screen review. |
| 3 | Labelled toolbar, tooltips with shortcuts | Icons only | Hovering any toolbar button shows its name and shortcut (`StudioPanels::tip_of`). The A / Auto action is labelled as Fix all with the boxing preset; the toolbar shows a "? shortcuts" hint. |
| 4 | Shortcut sheet | None | `?` (Slash) toggles a grouped sheet: Playback, Editing, File, View, plus the Escape rule. While the sheet is open, other keys are ignored. `help_after` is proved. |
| 5 | Readable op names, slider units | Op names and strengths shown as before | Done. Each stack row shows its parameter with a unit: passes (×), frames with ms, or a ±° wring limit. The sidebar shows before/after spikes, balance-impossible frames, foot slide and sink, and hand slide; distances are in mm. It also shows the foot/hand toggles and blend in frames. While dragging, the status bar shows the rotation in ° and the move in mm; nudges echo the new value. Unit choice is proved in `chrome.elisa` (`param_unit`, `wring_degrees`); readout maths was previously tested in `test/studio_units.elisa`. |
| 6 | Visual hierarchy | Status text crammed into the toolbar | Toolbar is for actions, the views and curves for content, the timeline for time, the sidebar for the stack, and the status bar for state and messages. Messages use the accent colour and headings are bold. |
| 7 | Status bar | None | Bottom bar shows: frame N / count (1-based), time `s.mmm`, fps, the selected operation, the last clean gain, and the last message. |
| 8 | Non-blocking feedback, safe defaults, full undo | Status line; default stack is the boxing preset | Routine feedback goes to the status bar. System file panels open only when asked for (row 2); an explicit compatibility warning appears before loading a legacy session without source identity. Defaults are unchanged (boxing preset, feet on, hands off). Fix all and loading a session are history commits, so Cmd-Z undoes them. |
| 9 | Escape always cancels | Escape only cancelled a gizmo drag | `escape_layer` peels exactly one layer per press: help sheet, gizmo drag, contact press, gizmo mode, then the selection. The order is proved, and the test checks that 4 layers are peeled. |
| 10 | Save/load session | None | `src/studio/state/session_state.elisa`: a text format (`mocap-studio session 4`) that saves feet and hand toggles, blend, operations, contact edits, retime bands and gizmo corrections (tag 4: quaternion in millionths, translation in micrometres; optional tag 7: band range, speed in permille, blend and enabled flag). Band records reject malformed fields, overlap, out-of-range frames and capacity overflow without clamping authored timing. `SessionBandPolicy::band_record_valid` has contracts and proof laws; runtime round-trip and malformed-record cases are in `test/studio_session.elisa`. Tag 6 records a two-residue fingerprint of the original GLB bytes, selected animation index, source frame count and document-node count. Optional tag 8 persists up to 256 ignored finding rows, keyed by tag 6 identity, analysis schema, output frame count after retiming and the full result row; changed findings expire, and over-capacity input fails without replacing existing state. Codec and app reconciliation contracts and round-trip tests are in `src/studio/state/session_issue_annotation_policy.elisa`, `proof/session_issue_annotation_laws.elisa` and `test/studio_session_annotations.elisa`. Loading stages annotations with the stack and changes live intent only after replacement is accepted; post-build reconciliation restores exact result matches and expires the rest. V4 restore rejects missing, duplicate or mismatched identity metadata. Versions 1 through 3 can be parsed only through an explicit legacy path. The studio shows the warning before asking about unsaved edits; Cancel preserves the current cleanup, while Load is followed by the normal dirty-document prompt. After confirmation, the decoded stack is held until replacement is accepted, so parse failures cannot discard current edits. On load, scopes are clamped, quaternion and offset values are clamped (`StudioChrome::session_clamp`) and the quaternion is re-normalised, corrections on missing nodes are dropped, unknown or damaged lines are skipped, and unsupported headers are refused. Saves write a unique same-directory temporary, check fwrite/flush/fsync/close, then atomically rename; failures remove the temporary and preserve the existing session. On-screen confirmation and small-window review remain open. |
| 11 | One-click "Fix all" + metrics | Preset existed only as the initial stack | The A key or the Auto button applies the boxing preset with foot and hand locks as one undoable edit. The sidebar shows before/after spike count, balance-impossible frames, foot slide/sink and hand slide; the status bar retains the last slide and spike gain. |
| 12 | Focus loss during a gesture | Modifier keys cleared; a lost pointer-up could leave a drag active | `FocusLost` clears modifiers, camera/scrub/contact/gizmo/retime drags, cancels an unfinished range or numeric entry, and restores the retime slider's starting value. The pure transition has contracts and laws in `src/studio/focus.elisa` / `focus_laws.elisa`, with `test/studio_focus.elisa`. Native event delivery still needs an on-screen check. |
| 14 | Screen-reader orientation | Canvas exposed no semantic nodes | `src/studio/accessibility.elisa` defines stable workspace, toolbar, finding, reset and stack-action identities; the running AppKit tree exposes the workspace, five regions, all 19 toolbar controls and live status in edit mode. Toolbar button/checkbox roles, names, toggle state, Undo/Redo availability and action dispatch are verified, including an accessible Loop activation followed by restoration. The timeline publishes named Plant/Lift/Reset/Delete/Merge/Split buttons with selected side/frame and authored interval range values, plus native action routes; Reset and Delete are disabled without an authored override, Merge is disabled unless a compatible adjacent interval exists, and Split is disabled at the selected interval's first frame or when the edit list is full. Delete explains its interval-wide scope; Merge describes the same-side/state requirement and output-preserving result; Split announces its before-frame boundary and output-preserving result. The Reset menu and Duplicate action now have named groups, roles, values, disabled states and action routes. Tree identities and parent/order laws are checked, but native activation still needs exercise. The export review has proved Dialog, CheckBox, Inspect full destination path, Cancel and Export identities; the path inspector exposes each populated read-only line plus Previous, Next and Done, with disabled boundary actions. The post-export result dialog exposes Open Result, Show in Folder and Done. Disabled Export state and acknowledgement value are published with native routes. `test/studio_accessibility.elisa` checks these identities. These modal and contact trees still need native VoiceOver/UI exercise. Cleanup-stack rows, contact row/frame selection, viewport selection, focus announcements and non-edit screens remain open. |
| 15 | Finding triage | Ranked aggregate spikes with previous/next/worst navigation | Detector, subject, severity and review-status filters, reset, and an analysis-scoped Ignore/Restore action now have policy, tests and native semantic nodes. Annotations do not alter the clip and stale revisions are pruned. Session v4 tag 8 persists ignored findings and restores only exact source/animation and complete analysis-row matches. The latest failed-load window did not show the filter chips, and native activation/VoiceOver has not been checked on a valid take. |
| 16 | Contact interval keyboard editing | Contact actions existed; precise endpoint changes required pointer interaction | Shift-Left/Right moves the selected interval; Shift-Up/Down moves its last endpoint; Shift-[ / ] moves its first endpoint. Moves are bounded, undoable and described in the `?` sheet and selection status. Policy and runtime tests pass; loaded-window feedback, focus ownership and screen-reader action exposure still need review. |
| 17 | Cleanup reset scope | Individual operation removal and per-frame contact reset existed; broad reset paths were easy to confuse | The scope policy distinguishes remove one operation, clear all authored contact overrides, clear all local corrections, and restore the source result. The visible Reset popover explains the three broad scopes, disables empty actions, dismisses on Escape/click-away and records each accepted reset as one undo step. Focused tests cover the state transition and sidebar accessibility-tree order. Valid-take on-screen behavior and native VoiceOver activation remain open. |
| 18 | Duplicate operation | Exact bounded stack copy existed without a visible action | The stack heading exposes Duplicate. It inserts an exact copy after the selected operation, selects the copy, and records one undo entry; `Cmd-D` and the native accessibility action use the same route. The button shows a disabled state and explains missing selection or full capacity. Existing kernel tests cover exact field preservation, capacity and undo/redo. A final app rebuild and valid-take pointer/keyboard/VoiceOver review remain open. |

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
