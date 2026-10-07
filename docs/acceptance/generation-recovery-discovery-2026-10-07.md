# Generation recovery discovery

## Implemented source

Engine commits `397cafdc` and `c1740a1f` introduce bounded native journal
discovery. Primary commits `8b1360c` and `912a25a` add strict Elisa decoding
and native build/input registration.

Discovery holds the existing generation lock while enumerating the managed
receipt directory through retained descriptors. It bounds directory entries
to 8192 and returned operation IDs to 512. Accepted names use the exact native
`trash-` plus 32 lowercase hex format and `.json` suffix. Receipt entries must
be regular, owned, not writable by group/others, have one link, and fit the
1 MiB bound. Managed directory identities are checked again before publication.
IDs are sorted by byte order. Failure, overflow and uncertain descriptor/lock
release publish no partial IDs.

The adapter rejects unknown status codes, invalid counts, partial failure
headers, missing terminators, malformed operation IDs and duplicates. Its
returned IDs are discovery hints. It does not parse receipts, authenticate
their contents, establish quarantine location or authorize Restore. Every
selected operation still needs native reconciliation and revalidation before
mutation.

## Evidence and remaining acceptance

Strict native source compilation passes with:

```sh
clang -fsyntax-only -fobjc-arc -Wall -Wextra -Werror -O2 \
  native/studio_build_generation_recovery_discovery_appkit.m
```

Fourteen discovery law declarations compile as an object with the selected
`e34f2c0656aac1232ad72da6516c7eb89f866a47` compiler. No executable tests or
authenticated proofs were run for this slice. Native object registration has
shell syntax and diff checks; full Studio linking/package closure is pending
compiler repair. Background restart loading and recovery browsing are in
progress and are not qualified by these compile observations.

Before acceptance, capture matched-source native execution for empty/missing
trash, unavailable or malformed directories, unknown receipt files, symlinks,
hard links, concurrent writer/lock contention, changed descriptor identities,
capacity overflow and release failures. Verify no partial result is accepted.
Exercise restarting after each journal phase and reconcile discovered IDs
before enabling Restore; capture keyboard and VoiceOver journeys through
unresolved, busy, conflicting and recoverable records. Preserve all receipts
and source takes during qualification.

## Interrupted receipt metadata discovery

The receipt updater stages `.pending-<operation>-<random>` and uses
`RENAME_SWAP` before unlinking the previous receipt. A crash can retain that
pending file even when the canonical receipt is valid. Engine commits
`3d00943e`, `e1e9d1d4` and primary `8d88973` now recognize the exact staged
filename format and expose its count separately as unresolved metadata. Empty
staging files remain discoverable. Operation IDs from staged and canonical
entries are deduplicated; no pending payload is parsed, deleted or promoted.
Unknown names still refuse discovery. A complete enumeration does not imply
resolved receipt metadata. The UI must show the unresolved count and reconcile
each selected operation through its canonical receipt before enabling Restore.
Native source and law-source compilation pass; crash execution and UI acceptance
remain open. Qualify crashes before swap, after swap and before/after directory
fsync and unlink before closing restart recovery. Safe resolution of pending
files remains separate unfinished work.
