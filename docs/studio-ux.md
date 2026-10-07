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
| 12 | Focus loss during a gesture | Modifier keys cleared; a lost pointer-up could leave a drag active | `FocusLost` clears modifiers, camera/scrub/contact/gizmo/retime drags, cancels an unfinished range or numeric entry, and restores the retime slider's starting value. The pure transition has contracts and laws in `src/studio/focus.elisa` / `focus_laws.elisa`, with `test/studio_focus.elisa`. Modifier down/up transitions are idempotent, so duplicate events cannot leave a stale Cmd/Ctrl or Shift bit; `proof/studio_shortcut_modifier_laws.elisa` and the repeated-event cases in `test/studio_shortcuts.elisa` cover this. During active numeric/text entry, open/save/export and all global plain/edit actions are suppressed. Enter commits the contact-frame draft or applies the retime speed; Backspace edits the draft; Escape cancels the contact-frame draft or retime selection. `StudioShortcuts::text_key_route` and `text_file_route` carry the contracts; `proof/studio_shortcut_text_laws.elisa` and `test/studio_shortcuts.elisa` cover every global route. `StudioTextEntryPolicy` filters both committed characters and the AppKit physical-key fallback: frame fields accept digits, while speed fields also accept decimal/suffix characters. Its focused laws and test are in `proof/studio_text_entry_policy_laws.elisa` and `test/studio_text_entry_policy.elisa`. Verify the integrated key delivery in a rebuilt running window. |
| 14 | Screen-reader orientation | Canvas exposed no semantic nodes | `src/studio/accessibility.elisa` defines stable workspace, toolbar, finding, reset and stack-action identities; the running AppKit tree exposes the workspace, five regions, all 19 toolbar controls and live status in edit mode. Toolbar button/checkbox roles, names, toggle state, Undo/Redo availability and action dispatch are verified, including an accessible Loop activation followed by restoration. The timeline publishes named Plant/Lift/Reset/Delete/Merge/Split buttons with selected side/frame and authored interval range values, plus native action routes; Reset and Delete are disabled without an authored override, Merge is disabled unless a compatible adjacent interval exists, and Split is disabled at the selected interval's first frame or when the edit list is full. Delete explains its interval-wide scope; Merge describes the same-side/state requirement and output-preserving result; Split announces its before-frame boundary and output-preserving result. The Reset menu and Duplicate action now have named groups, roles, values, disabled states and action routes. Tree identities and parent/order laws are checked, but native activation still needs exercise. The export review has proved Dialog, CheckBox, Inspect full destination path, Cancel and Export identities; the path inspector exposes each populated read-only line plus Previous, Next and Done, with disabled boundary actions. The post-export result dialog exposes Open Result, Show in Folder and Done. Disabled Export state and acknowledgement value are published with native routes. `test/studio_accessibility.elisa` checks these identities. These modal and contact trees still need native VoiceOver/UI exercise. Cleanup-stack rows, contact row/frame selection, viewport selection, focus announcements and non-edit screens remain open. |
| 15 | Finding triage | Ranked aggregate spikes with previous/next/worst navigation | Detector, subject, severity and review-status filters, reset, and an analysis-scoped Ignore/Restore action now have policy, tests and native semantic nodes. Annotations do not alter the clip and stale revisions are pruned. Session v4 tag 8 persists ignored findings and restores only exact source/animation and complete analysis-row matches. The latest failed-load window did not show the filter chips, and native activation/VoiceOver has not been checked on a valid take. |
| 16 | Contact interval keyboard editing | Contact actions existed; precise endpoint changes required pointer interaction | Shift-Left/Right moves the selected interval; Shift-Up/Down moves its last endpoint; Shift-[ / ] moves its first endpoint. Moves are bounded, undoable and described in the `?` sheet and selection status. Policy and runtime tests pass; loaded-window feedback, focus ownership and screen-reader action exposure still need review. |
| 17 | Cleanup reset scope | Individual operation removal and per-frame contact reset existed; broad reset paths were easy to confuse | The scope policy distinguishes remove one operation, clear all authored contact overrides, clear all local corrections, and restore the source result. The visible Reset popover explains the three broad scopes, disables empty actions, dismisses on Escape/click-away and records each accepted reset as one undo step. Focused tests cover the state transition and sidebar accessibility-tree order. Valid-take on-screen behavior and native VoiceOver activation remain open. |
| 18 | Duplicate operation | Exact bounded stack copy existed without a visible action | The stack heading exposes Duplicate. It inserts an exact copy after the selected operation, selects the copy, and records one undo entry; `Cmd-D` and the native accessibility action use the same route. The button shows a disabled state and explains missing selection or full capacity. Existing kernel tests cover exact field preservation, capacity and undo/redo. A final app rebuild and valid-take pointer/keyboard/VoiceOver review remain open. |
| 19 | Retimed frame readout | `src N out N` | The timeline readout labels both values as **source** and **output** frames. The values remain zero-based and use the existing source mapping and output playhead frame. During Shift-drag, the reserved right margin also shows the selected zero-based source-frame interval. |

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
there. The failed-load toolbar has since been inspected in a bundled Studio window
(2026-10-06). Valid-take rendering and native activation remain unverified.

## Storage & Recovery

Open **File → Storage & Recovery** to inspect Studio-managed generated files
and native Trash receipts. The entry is available even when no take is open.
Refresh rereads the manifest and checks current file identity; a failed scan
clears stale rows. Changed or unverifiable records stay protected. Source
paths and hard-link aliases of the active source are excluded.

The two verified byte totals distinguish files in `build/` from files in
Trash. Files in Trash still occupy disk space. These totals exclude records
whose identities could not be verified; they do not estimate reclaimed space.
The selected row shows exact bytes and completed days since modification,
using the clock captured by the latest Refresh. Future timestamps and clock
failures show an unverified age. Refresh keeps the selected artifact only when
its full identity still matches; it clears selection if that artifact changed
or disappeared.

Present files explain their cleanup protection. The current 30-day policy
retains recent files, and invalid/future ages never qualify. Reports created
in this Studio session stay protected, as do recovery points until their
recovery references can be verified. File type and symbolic-link checks run
at each Refresh. These reasons are also included in accessible row help.

Use Up/Down to choose a row and Tab to move among Refresh, Done and Restore.
Restore is available only for a valid, durably recorded, verified Trash
receipt. The first activation opens a review; **Confirm restore** performs a
fresh check and restores the file to its original location without replacing
an existing destination. Escape cancels an open review; otherwise it closes
the screen. Refresh also cancels a pending review.

If restore succeeds but the manifest save fails, the result explicitly says
the file was restored and asks for Refresh to finish recovery. An interrupted
move can be reconciled using the identity already recorded in the manifest.
Unreadable manifests are not replaced with empty inventories.

Verification: Studio builds, the identity/restore/totals/window policies have
proved scalar boundaries, and disposable native fixtures exercise checked
move rejection, restore, destination conflicts and reconciliation. The
Storage dialog's pointer, keyboard and VoiceOver acceptance is still open.
A temporary native bundle rendered the empty-start guide and exposed the File
button in its accessibility tree. AX activation left that tree unchanged;
pointer input returned `noWindowsAvailable`. Keyboard Quit closed the process.
This confirms the initial render and node publication, not File activation or
Storage interaction. The temporary bundle was removed after the process exited.
The single-file cleanup flow exposes Move to Trash review and explicit
confirmation. No row is selected on first open. Retention cycles through 7,
30 (default), 90 and 365 days and refreshes eligibility without moving files.
Changing the Restore row, refreshing, changing retention, or pressing Escape cancels an
open review. A confirmed move checks the reviewed identity and eligibility
again immediately before the native checked move. Receipt-save failure
attempts restore; fresh checks distinguish verified restoration, a retained
Trash receipt and an uncertain location. Unresolved recovery prevents another
cleanup move from replacing its receipt. Refresh can finish reconciliation.

Inventory checkboxes store selections by full artifact identity. Click a
checkbox or press Space on the inspected row to toggle an eligible file.
Select eligible covers the current verified inventory; Clear selection clears
that set. Protected rows use a disabled checkbox marker. The selected file
count and exact byte sum are visible. Refresh removes missing, changed or
newly protected selections and reports the removal.

Move to Trash reviews the complete selected set and exact byte total. A
changed set or retention policy cancels confirmation. Cleanup processes at
most one file per frame and rechecks every remaining reviewed identity before
each move. Cancel or Escape stops between files; completed receipts are kept.
Controls that change the set are disabled while running. The result shows
recorded, failed/restored and untouched counts, plus per-file outcomes.
Unknown locations and receipt recovery stop the batch. Refresh can reconcile
an uncertain item and update its result without automatically resuming moves.
Retry requires a new review and excludes files already recorded in Trash.

Retention presets are saved atomically in
`build/studio_storage_preferences.txt` and re-read on inventory refresh.
First use defaults to 30 days. Existing unreadable, malformed, unsupported or
unsafe settings block cleanup and show an alert; they are never silently
replaced. Repair the named settings file and Refresh to resume review.
A failed save preserves the previous setting. The settings file and its
filesystem aliases are protected from cleanup. Changing retention only
changes eligibility; every move still requires review and confirmation.

The overview separates Eligible, Protected, Recovery and In Trash counts
and exact logical bytes. Changed or unverified identities have unknown current
sizes and stay outside these totals. Recovery files use their own category
and remain protected. Logical bytes are not a disk-space-reclamation estimate:
hard links and files retained in Trash can keep disk space allocated.
A verified inventory with no eligible files explains the next safe action:
review protection reasons and retention, then Refresh after changes.

Grouping/filtering, stale-exemption management, dedicated review scrolling and
running-window/fault-injection acceptance remain open.
A single native filesystem operation still runs on the UI thread; the batch
returns to the event loop between files.

A native smoke on 2026-10-06 against the rebuilt overview binary confirmed
that the empty guide no longer displays the stale findings sidebar. The
published File accessibility button remained present, but its AX press and
Cmd-O did not change the tree. Pointer fallback failed with CUA
`noWindowsAvailable` while the process was still running. This does not
verify File or Storage activation; their running-window acceptance remains
open. Cmd-Q closed the temporary app, its exit was checked, and its generated
bundle was removed. The Storage overview layout itself is build-checked,
not yet verified through native input.

During Move review, Up/Down and pointer inspection preserve the frozen
cleanup selection and confirmation state. Checkbox/Space selection changes
still cancel review, as do Refresh, retention changes and Escape. Restore
review still cancels when its inspected receipt changes. Inspection uses a
bounded total navigation policy; exact next/previous helper contracts and
wrapper bounds are proved, with the independent composed step replay gap
recorded as G92. Native review interaction acceptance remains open.

Saved exemptions in `build/studio_storage_exemptions.txt` now load on every
inventory refresh. They use a distinct versioned header and registered
non-recovery records. Matching uses the complete reviewed identity and
canonical path; a stale exemption cannot silently match a replacement file.
A matched file is protected and excluded from selection. Source, recovery,
active-output and metadata protections continue independently. Unreadable,
unsupported or unsafe exemption files block cleanup and produce an alert.
Atomic exemption publication reloads the saved file before accepting its
state. The inspected verified row offers Keep this file or Remove exemption
through pointer, keyboard and accessibility actions. Activation refreshes
identity evidence before saving; changing protection never moves files and
removal still requires a fresh cleanup review. The policy and laws prove
112/112 and 140/140 obligations with replay. Studio builds and the existing
accessibility semantic test passes; native interaction acceptance remains
open. Missing or changed saved entries still need a dedicated management view.

The overview and accessible inventory summary include the last scan value
or an explicit unavailable state, including empty inventories. Visible and accessible copy share a formatter for an explicit UTC date and
time; unsupported timestamps use the unavailable message. The scalar clock-field policy proves 18/18 obligations and its laws prove
32/32, all certificates replayed. Calendar boundaries remain covered by
runtime tests; calendar-date arithmetic has no complete formal contract. This records scan time, not artifact creation or Trash
move time.

Artifact registration now reuses the canonical export-path admission guard
before capturing or inserting identity metadata. This rejects source aliases,
unsafe paths and nonregular files even when a creation caller requests
registration. Fresh native snapshot checks remain required. Successfully saved sessions are now registered as protected recovery
material after fresh admission and identity checks. Registration failure
is reported separately from successful save. Creation/dependency metadata,
crash durability and a distinct completed-output kind remain pending; completed
GLB outputs must not be mislabeled as temporary exports.

Session writes now check canonical destination admission before serialization
and publication. Outside-build paths, source identities/aliases, symlinks and
unverified or nonregular destinations stop the save with a specific message.
Replacement workflows retain the current document when this guard fails.
This reuses the export admission kernel; native session-save path acceptance
and filesystem race/fault qualification remain open.

The registration policy now proves 14/14 source obligations and 33/33 law
obligations, with zero certificate replay gaps. Its exact receipt-kind mapping
is checked against the persisted schema. Native registration and durability
acceptance remain open.

Artifact registration rereads the manifest before extending it, preserving
records published since the last inventory read. An unreadable or malformed
latest manifest stops registration. This fixes stale-cache publication; it
does not yet serialize overlapping reads/writes by two processes. The lock
transaction must encompass that fresh read, native actions and publication.

The 2026-10-06 integration check rebuilt 78 executable tests and all 78
returned zero, including the Storage semantic tests and UTC calendar
boundaries. This covers the compiled test binaries, not native input flows
or the complete roadmap. Its native Storage check stopped at stale compiler
provenance. All four CLI scenarios returned zero. The complete command
finished with exit 1 because native verification and the proof baseline gate
were not clean; the latter reported established regressions and missing
reviewed entries. Concurrent registration proof edits require a final
focused recheck before a clean proof baseline can be claimed.

## Manifest transaction integration (2026-10-06)

Studio now holds a persistent-file nonblocking lock across fresh manifest
reads, registration, reconciliation, Restore, and each batch item's full
remaining-selection validation, native move and receipt publication. Nested
refresh calls reuse the outer descriptor; wrappers release after all inner
return paths. Retention and exemption changes share the same transaction
scope. Publication requires a held scope. The lock file is protected metadata
and is never unlinked by this protocol.

Lock acquisition failure disables cleanup using unverified manifest state.
Release uncertainty latches a block on later moves until restart and stops a
running batch. Completed receipts and counters remain available for inspection.
The pure lock/alert kernels are proved; this does not prove native syscall
behavior or whole-app lifetime/control flow. Two-instance, crash, path-replace,
release-failure and keyboard/VoiceOver acceptance remain open. External
programs that ignore the advisory lock are outside its serialization guarantee.

## Reserved output destinations

Session saves, GLB review/publication and report sidecars reject Storage's
manifest, preferences, exemptions and persistent lock paths. Native namespace
comparison canonicalizes parents and applies Unicode normalization/case
folding, conservatively rejecting case-only variants on case-sensitive volumes
too. Unknown resolution or invalid UTF-8 blocks the write. Existing targets
and controls additionally require verified native snapshots; matching device
and inode identities reject hard-link aliases. These checks supplement the
source-take and build-root admission rules.

The pure artifact admission gate proves 2/2 obligations and its laws prove
6/6. The separate ASCII reference policy proves scalar folding and count
bounds (13/13 source, 19/19 laws); it does not formally verify native Unicode
comparison. Native syntax checks pass. Runtime Unicode/volume alias fixtures
and filesystem race acceptance remain open.

### Storage reflow and filename source changes (2026-10-07)

The footer now derives columns/rows from an integer layout policy. Below the
header breakpoint, Inspect path and exemption actions use a separate row;
selection actions use another. File-list capacity reserves those extra rows.
Drawing, hit testing and accessibility continue to share `storage_button_box`
and `storage_row_box`. These are source changes, not running-window evidence.

Filename commands carry a clip limited to the name column, preventing them
from drawing over type/status labels. Names exceeding the 128-byte display
slot reserve three bytes for `...` and stop at a complete UTF-8 scalar boundary.
Copies stop at the slot bound. The full retained path remains available through
inspection and semantic row names. The top-level Storage panel currently owns
its temporary clip state; nested clipping would need preserved/intersected
caller clip state before this renderer is reused inside another clipped panel.

Eight layout laws and four truncation laws accompany these changes. Their
current compilation and authenticated proof qualification are pending. Also
pending: native resize/keyboard/VoiceOver checks, font and scale validation,
long introduction/overview/footer text, tiny-window minimum-size behavior,
and an overflow marker when a name fits the byte slot but exceeds its pixel
column. Source clipping alone does not close those presentation requirements.
