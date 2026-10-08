# Retained feedback and UTF-8 formatting source checks

Formatted feedback previously retained a view into StudioText's 96 rotating
128-byte slots. Rendering can reuse that slot and overwrite the status. The
snapshot source change copies formatted status into an independent fixed
128-byte buffer, guarded by an extent/readability policy. It adds no heap
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
