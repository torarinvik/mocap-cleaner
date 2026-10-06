# Studio storage cleanup policy

`StudioStorageCleanupPolicy` defines which Studio-generated artifacts can be
offered in the storage cleanup review. It currently recognizes recovery
snapshots, abandoned temporary exports, and generated reports. A candidate
must be Studio-managed, resolve canonically under `build/`, be older than its
configured retention period, and not be a symlink, source take, open document,
or file referenced by a session. The candidate identity must also be freshly
verified against the inventory record; a changed identity or missing identity
verification is protected. The final Trash action also requires that the item
was selected, reviewed, and explicitly confirmed.

The policy receives filesystem facts from its caller. It does not inspect
paths, determine symlink identity, move files, or empty Trash. The engine now
provides a macOS adapter in `../elisa-engine-mocap/native/file_trash_appkit.h`
and `.m` for moving an eligible file to Trash and restoring it. Its versioned
receipt records the canonical original path, resulting Trash path, and file
identity (device, inode, size, and modification time). Move rechecks that the
candidate is a regular non-symlink under the canonical build root; restore
requires the original destination to be absent and the Trash item to match
the receipt. A field-based ABI exposes those values to Elisa without mirroring
the native struct layout; if the adapter cannot verify a post-move receipt, it
attempts to restore the file before returning failure. The adapter does not
enumerate the Studio inventory or persist receipts for the caller.

`src/studio/io/storage_manifest.elisa` now defines the version 1 storage
manifest codec. It records registered artifacts and successful Trash moves
as separate states. It bounds the record count and identity fields,
hex-encodes paths so control characters cannot split records, validates
decoded UTF-8, rejects duplicate registration or receipt identities, and leaves the caller's
output unchanged on malformed input. The scalar identity bounds live in
`src/studio/storage_receipt_policy.elisa` with 18/18 obligations proved. This
is the storage foundation: Studio has a bounded manifest reader, snapshots
canonical identity through the engine, and atomically records report sidecars
after successful export. The app displays a bounded inventory with reviewed
Move to Trash and Restore actions. Saved sessions are registered as protected
recovery artifacts. Native UI acceptance remains open. The field-based Elisa
adapter is compiled into the Studio binary.

`protection_reason` returns a stable numeric reason for the first applicable
protection rule, including unmanaged files, paths outside `build/`, symlinks,
source takes, open or session-referenced files, invalid facts, and items still
inside retention. Changed or unverified file identity has a distinct reason.
`PROTECT_NONE` means the item passes the policy. Inventory
UI can map these codes to user-facing explanations while keeping the same
eligibility decision used by the Trash action. The reason reports only the
first blocker; after that blocker is resolved, a refreshed inventory may show
the next one.

Studio integration must obtain canonical-path, file-type, source-identity,
and reference evidence from the engine/file-system boundary immediately
before showing and acting on the review. If a fact is missing or invalid, the
file is not eligible. Persist receipts safely so successful moves can be
restored after restarting Studio; tolerate Trash items that the user later
empties or changes. The review should show the item's type, location, age, and
size; successful removal can report space moved to Trash, while moving to
Trash remains recoverable. Emptying Trash stays under Finder's control.

Retention days are explicit inputs so preferences can be configured and
displayed by the UI. This kernel does not impose defaults. The focused
executable checks boundary examples; its proof file currently replays 351 of
353 obligations. The two open explanation-code and exact-sum laws are tracked
in `docs/proof-gaps.md`. No file operation is implemented by this policy.

## Complete manifest review versions (2026-10-06)

Move and Restore reviews capture the deterministic encoding of the entire
verified manifest, including every persisted field and record order. Under
the manifest lock, confirmation reloads the inventory and compares that
encoding before acting. Changes to unselected records also invalidate review.
This token represents canonical decoded content, not the original file bytes;
equivalent text encodings do not count as a content change.

Each batch step repeats this comparison. After its own successful receipt
publication, the batch advances its token to the document it published. A
failed publication followed by later receipt reconciliation leaves the old
token in place, so another step requires a fresh review. Lock failures and
version drift never queue an automatic retry.

The existing lock policy proves the admission gates. Manifest encoding,
byte comparison, native locking and app transaction wiring remain runtime
boundaries; the new version adapter is not claimed as wholly proved. The
Studio build passed with check skipping enabled; runtime concurrent-writer
and Restore scenarios remain to be verified.

## Recorded original path inspector (2026-10-06)

Choose an inventory row and use **Inspect full path**, or press Enter while
row navigation has focus. The read-only inspector snapshots the complete
recorded original path into owned storage. Previous/Next and arrow keys page
through long UTF-8 paths; Tab moves among enabled buttons, and Done or Escape
returns to the same Storage selection and review. Opening it never confirms
Move/Restore or changes cleanup selection. It is unavailable during a running
batch. Protected and identity-unverified rows remain inspectable: the label
explicitly describes a recorded location, not a newly verified filesystem fact.

The existing export path pager supplies page/focus policy and exact path lines.
Storage has a separate immutable snapshot/context; export acknowledgement and
destination are retained. Modal pointer, keyboard and accessibility dispatch
handle this inspector before the Storage actions behind it. Native screen,
minimum-window and accessibility-focus acceptance remains open.

## Inventory and displayed rows

Refresh retains a complete aligned snapshot of entries, statuses and protection
reasons separately from displayed rows. Selection reconciliation, pending batch
freshness and reviewed Move/Restore checks use that complete snapshot. The same
eligibility gate applies to inventory and displayed rows. This prepares list
filtering without allowing hidden rows to escape cleanup safety checks; the
filter controls and hidden-selection feedback are still pending. The view
projection now uses the filter policy, preserves inspection by exact identity
when still visible, and keeps entry/status/reason arrays aligned. It defaults
to All; cycling is prepared internally and refuses changes during a batch.

The inventory separation builds with `STUDIO_SKIP_CHECKS=1`; this evidence
does not qualify native filter interaction or filesystem race behavior.
Read-only review of the projection found no stale-index or hidden-row route
that bypasses identity, eligibility or manifest-version checks. Select eligible
uses displayed rows; Clear selection clears the whole selection. The future
controls must state these scopes and announce selections hidden by a filter.

## Hard links and allocation: next native boundary

Current totals are logical file sizes. A fresh native measurement must provide
verified dev/inode/size/mtime, link count and allocated blocks from one regular,
non-symlink `lstat`. Receipt measurement must locate only the exact recorded
Trash receipt. Keep dynamic link/allocation facts in inventory sidecars, not
persistent review identity: link count can change without size or mtime.
Unknown measurement must remain distinct from zero. Validate overflow when
converting `st_blocks` to bytes.

Expose link counts and allocated bytes reported, with explicit unknown states.
A single hard link is necessary but insufficient to claim physical space can
be recovered on APFS: clones and snapshots may retain shared extents. Keep
recoverable-space estimates unknown until exclusive extent/snapshot ownership
is established. Add integer classification and bounded-total contracts/laws;
native filesystem truth remains separately qualified evidence.
