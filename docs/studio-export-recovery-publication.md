# Prepared recovery GLB publication

`StudioExportRecoveryPublication::commit` accepts the recovery directory,
staging and final destination paths, the expected journal record, captured GLB,
JSON and text bytes, and caller-established ownership and lock facts. The
journal is strictly decoded from disk and compared with the expected record's
binding and `Prepared` stages.

Before rename it requires both expected stages to be `Prepared`, strictly
reloads the journal and checks the same binding and recovery directory through
`RecoveryBinding::load_prepared`, checks captured sidecar and output-snapshot
bytes, compares staging bytes again with the captured GLB, and requires the
final destination spelling to equal the journal destination byte for byte. It
does not read the destination before publication, since it may not exist or may
contain an older export. The ordinary `RecoveryBinding::load` remains the
post-publication check that also compares final destination bytes. Neither path
infers directory ownership or lock state.

The result distinguishes preflight rejection, native `NotPublished`, and
`Published(status, journal_status)`. Once the publisher reports a successful
rename, a later journal update failure cannot turn that into a rejection. The
observed stage advances to `GlbPublished`; the durable stage advances only
when the native publisher reports `PublishedDirectorySynced`.

Scalar admission and outcome facts are contracted in
`export_recovery_publication_policy.elisa` and covered by the focused law file.
Native path reads, exact byte comparisons and rename remain trusted IO
boundaries; this policy does not prove race freedom against an external process.
