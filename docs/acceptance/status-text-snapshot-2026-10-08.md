# Retained feedback and UTF-8 formatting source checks

Formatted feedback previously retained a view into StudioText's 96 rotating
128-byte slots. Rendering can reuse that slot and overwrite the status. The
snapshot source change copies formatted status into an independent fixed
128-byte buffer, guarded by a count/non-null policy. The borrowed view supplies the input
storage lifetime; the policy does not prove a foreign pointer span. It adds no heap
allocation. Literal messages remain literal-backed; the snapshot stays readable
until another explicit captured message replaces it.

`test/studio_status_text_lifetime.elisa` specifies 300 scratch-slot rotations
without changing captured feedback. The test and three extent laws pass semantic
checking on installed source-matched compiler `b26659e2` (product `94f11e30`).
Native test emission exits 2: the backend declines fixed-array generic view
helper calls used by both existing StudioText and new capture. No lifetime
runtime pass is claimed. Retained records are in `build/dialog-result-reduction/`.
The source-changed repair checkout was refused by its provenance wrapper;
no stale override was used.

StudioText now returns only the complete UTF-8 scalar prefix of its raw slot.
Viewing partial text leaves raw bytes intact so a subsequent continuation can
complete the scalar. The new slot test covers 127 ASCII bytes followed by a
partial two-byte scalar, an exact 128-byte fit, a partial four-byte scalar, and
viewing then completing a scalar. Companion proof obligations call the actual UI
prefix helper on fixed literal arrays; they are not assumptions about its result.
Both test and proof files pass semantic checking. Runtime and source/replay
qualification remain open. These obligations do not establish grapheme-safe
line wrapping, full-message persistence or readability of clipped explanations.

The filename scanner also now checks its 4096-byte scan budget before reading
the next byte. Full UI review, a discoverable persistent details view, complete
paths/messages and accessible retry controls remain roadmap requirements.


The three UTF-8 helper obligations additionally execute with O2 compile/run
exit 0 on the source-matched installed `b26659e2` product, using a retained
standalone driver. The helper calls specialize literal fixed-array lengths
2 and 4; this does not close the formatter's named-constant specialization
decline or the 300-redraw snapshot test. Exact source/executable hashes and
terminal logs are retained in
`build/dialog-result-reduction/text-utf8-helper-driver.record.json`.
Formal source correspondence and proof replay remain open.


The status accessibility node now exposes the retained instruction as its help
text, separately from the compact display-slot value that appends a filename.
This avoids forcing a long literal recovery instruction through the 128-byte
display formatter merely to read it with VoiceOver. Native accessibility review,
complete filename/path inspection and the discoverable full-details view remain
open; this source binding alone does not qualify the full recovery workflow.


The three pure extent laws now execute through a focused O2 driver over counts
-2 through 130, both data-presence states, and maximum i64 refusal; compile/run
exit 0 on source-matched installed `b26659e2`. The maintained regression is
`test/studio_status_text_extent.elisa`. This closes the pure admission runtime
check only. The separate snapshot, formatter and formal source/replay acceptance
items remain open.

## Current Studio integration check

After the complete guide clip, measured tooltip layout and unavailable-character
tooltip changes (through root commit `d4e1d82`), the full Studio semantic check
on clean compiler `5d17a2c0` exits 1 with only the known atomic `load` resolution
diagnostic at runtime concurrency line 949. No additional guide or tooltip
diagnostics are reported. The selected product SHA is
`b60c2b081425874cb730b09de9e0a524fcd5f3beab6fe595353fc7bc4f8a0006`;
the runtime remains `956c9f44e4024087b63954d5abbe6620a4a2c5c78c5a4cee044e3da2bde5ce96`.
The normal identity generator selected this compiler's runtime declarations,
and the compile used its canonical wrapper with a 2 GiB memory cap.

Evidence: `build/studio-tooltip-integration/semantic.log` SHA
`34f4b3ec63e559d75a668605af885e8ce0181d5eb74f8ae48dbefc90faa4cc31`,
with `semantic.exit` and `identity.env` in the same directory. This is a failed
whole-app check with a narrowed blocker, not a native build, visual result or
proof replay. The nested owning-return regression checks are separate and still
pending on this compiler tuple.
