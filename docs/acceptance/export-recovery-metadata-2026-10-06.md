# Recovery metadata capture

`StudioExportRecoveryMetadata::draft` captures native build and destination
paths into arrays owned by the caller's explicit lifetime. It constructs both
sidecar paths from the same captured destination and admits only bounded,
valid paths and journal metadata. Failure preserves the previous output.

The placeholder transaction is replaced by recovery preparation after actual
directory creation. A draft proves neither ownership nor durable publication;
it must not be accepted as a retained journal or offered for retry.

Contracts and companion laws bind the captured generation, animation and
byte counts to the supplied values and reject a negative generation. Normal
compiler `04b384ec` emitted the law composition object without diagnostics
in `build/export-recovery-metadata-laws-compile.log`.

Proof replay is unfinished: imported journal verification currently has a
long-running abnormal-exit investigation. No closed proof baseline is claimed,
and no executable tests were added or run. Live Studio integration, native
path qualification and failure-state behavior remain open.
