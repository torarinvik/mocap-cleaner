# Export sheet row field resolution

The immutable full Studio diagnostic generation at compiler revision
`22cf6e5b193cac89fd0b3a6386ba30d6e1dcfca0` declined the field expression
in `publish_export_batch_sheet_accessibility` at line 57. It emitted no
application object. The cause remains unresolved.

On 2026-10-07, focused reductions included both `Report::Row` and
`StudioExportBatchPanelPolicy::Row`, copied an indexed queue row into its
fully qualified type, and read its label. Both include orders compiled:

- Report first: `build/sheet-owner-reduction/rows-before.o`, 134384 bytes.
- Queue policy first: `build/sheet-owner-reduction/rows-after.o`, 134200 bytes.
- Reading label and output label inside a captured loop also compiled:
  `build/sheet-owner-reduction/captured.o`, 134520 bytes.

These used the unchanged compiler wrapper in the immutable 22cf generation.
They are compile diagnostics, not proof authentication or native acceptance.
The two same-named row types and a captured loop alone do not reproduce the
failure. A module ownership collision must not be presented as established.

An initial whole-publisher reduction omitted its Studio and UI composition
and failed with missing declarations; it provides no evidence about ownership.

Next, reproduce the failure with the current matched compiler and complete
application closure, then remove dependencies while preserving the decline.
Keep both qualified row types in any reduction that implicates their names.
Fix the responsible source expression or compiler resolver only after the
failing reduction identifies the cause. Full Studio compilation and native
accessibility behavior remain required after the repair.
