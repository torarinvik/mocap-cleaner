# Studio storage cleanup policy

`StudioStorageCleanupPolicy` defines which Studio-generated artifacts can be
offered in a future cleanup review. It currently recognizes recovery
snapshots, abandoned temporary exports, and generated reports. A candidate
must be Studio-managed, resolve canonically under `build/`, be older than its
configured retention period, and not be a symlink, source take, open document,
or file referenced by a session. The final Trash action also requires that the
item was selected, reviewed, and explicitly confirmed.

The policy receives filesystem facts from its caller. It does not inspect
paths, determine symlink identity, move files, or empty Trash. The engine now
provides a macOS adapter in `../elisa-engine-mocap/native/file_trash_appkit.h`
and `.m` for moving an eligible file to Trash and restoring it. Its versioned
receipt records the canonical original path, resulting Trash path, and file
identity (device, inode, size, and modification time). Move rechecks that the
candidate is a regular non-symlink under the canonical build root; restore
requires the original destination to be absent and the Trash item to match
the receipt. The adapter does not enumerate the Studio inventory or persist
receipts for the caller.

Studio integration must obtain canonical-path, file-type, source-identity,
and reference evidence from the engine/file-system boundary immediately
before showing and acting on the review. If a fact is missing or invalid, the
file is not eligible. Persist receipts safely so successful moves can be
restored after restarting Studio; tolerate Trash items that the user later
empties or changes. The review should show the item's type, location, age, and
size; successful removal can report space moved to Trash, while moving to
Trash remains recoverable. Emptying Trash stays under Finder's control.

Retention days are explicit inputs so preferences can be configured and
displayed by the UI. This kernel does not impose defaults. `proof/` covers the
exclusion and confirmation rules; `test/studio_storage_cleanup_policy.elisa`
covers boundary examples. No file operation is implemented by this policy.
