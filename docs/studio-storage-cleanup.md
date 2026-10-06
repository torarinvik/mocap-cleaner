# Studio storage cleanup policy

`StudioStorageCleanupPolicy` defines which Studio-generated artifacts can be
offered in a future cleanup review. It currently recognizes recovery
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
after successful export. The app does not yet display inventory or expose
Trash/Restore controls, so those registered reports cannot yet be managed by
the user. The field-based Elisa adapter is compiled into the Studio binary.

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
