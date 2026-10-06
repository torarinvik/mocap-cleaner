# Same-session prepared export retry

`src/studio/app/app_export_recovery_retry.elisa` exposes
`retry_retained_export(index)` and `recovery_retry_message(result)` for a
retained same-session record. It reads the
captured binding and bytes from memory, compares the recorded build directory
with the current canonical build path, takes the Storage transaction lock, and
rechecks the workspace, destinations, native directory type, journal, retained
files, and staging bytes before any publication decision.

The retry path never infers replacement consent. It uses create-only GLB
publication. If the final GLB already contains the exact captured bytes, the
post-publication binding reader verifies it before reports are completed. JSON
and text reports are also create-only; exact existing bytes are accepted and
conflicting files block the retry. Reports come from the retained captured
bytes, with no reevaluation of the take or cleanup stack.

Published state is retained if a later journal update, Storage tracking update,
or lock release fails. Durability uncertainty is separate from observed
publication. An incomplete report outcome is returned with `published=true`
when GLB publication already succeeded; the result includes a typed failure
and the current report outcome for the UI to explain. If a create-only link
published but staging unlink failed, the result keeps staging and explicitly
reports whether its bounded path diagnostic was retained.

The retry is restricted to the currently selected canonical build directory.
Retained entries for another workspace are rejected before recovery-file IO;
this implementation does not claim a pinned-workspace lock. The directory
ownership input uses the same-session `Prepared` create chain plus current
native directory/no-symlink facts. Inode continuity, ancestor replacement
races, crash restart authentication, and native fault injection remain
unqualified.

`StudioExportRecoveryRetryPolicy::prepared_retry_admitted` is the pure guard
kernel. Its laws prove each admission input is necessary. Compilation and proof
replay results will be added after the fresh compiler run.
