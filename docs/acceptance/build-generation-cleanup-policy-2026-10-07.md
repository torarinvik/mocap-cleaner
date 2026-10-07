# Generated Studio build cleanup prerequisite

The build input record now carries a generation schema, artifact kind and ID
derived from the unique `studio-build.*` directory. Packaging verifies that ID
against the input record's directory and executable digest. Each app bundle also
records its own `studio-package.*` ID, the source build ID, and executable
SHA-256 in `Contents/Resources/PACKAGE-GENERATION.json`. The sealed build input
record remains byte-for-byte intact in `BUILD-INPUTS.json`.

`StudioBuildGenerationPolicy` is a pure fail-closed prerequisite for a future
review flow. Cleanup eligibility requires a verified manifest/product and
filesystem identity, verified current/active/recovery protection facts, an
old unprotected generation beyond its retention period, and explicit
selection, review and confirmation. A caller may report `Identity.Matches`
only after binding the manifest ID to the directory basename and checking the
no-follow directory identity and sealed product digest. Missing activity or
protection inventory must remain unverified.

An earlier nine-law compile used compiler `5b354650` and source commit
`c45541f`; it is historical comparison evidence only. The current policy has
17 laws. Its latest focused producer run compiled the law source with compiler
`9667344`, but source authentication remains unsupported: the producer
reported 89 obligations, 33 proven and 56 unproven, with 22 unsupported
functions. Replay of those emitted theorems does not authenticate the current
source. See the [current law source compile record](current-law-source-compile-2026-10-07.md)
and the [generation policy proof status](../proof-gaps/build-generation-policy-proof-20261007.md)
for hashes and the exact producer/replay limits.

The build and package scripts now share an OS advisory lock at
`build/.studio-generation.lock`. Each script verifies the inherited descriptor,
exclusive lock state, owner, inode, and no-follow path identity before work;
standalone packaging acquires the lock and packaging called by a build reuses
the same open-file description. Future cooperating cleanup clients must use
this lock for their complete inventory/review/mutation transaction.

The global build lock covers cooperating build/package clients only. By itself
it does not establish whether a Studio process is using an artifact, and it
does not provide a recoverable directory Trash receipt. No cleanup mutation is
wired. Current products, active generations and package `previous.app`
recovery backups therefore remain protected by leaving their directories in
place. J04 and M7 cleanup acceptance remain open.

The source now adds artifact-local shared leases. A build generation receives a
sealed `.studio-generation.lease` beside its executable and input record; a
package receives one in `Contents/Resources`, bound to its package ID and the
copied executable digest. Startup resolves the actual executable, checks its
generation/package records and lease file, then retains a shared `flock` until
the UI exits. A failed or missing check presents Retry/Cancel and refuses to
start the window. This supports direct build-symlink launch and bundles renamed
to `previous.app` or moved independently of the developer build directory.

The five lease admission laws compiled at O0 to a 5,328-byte object, and a
small Elisa API context compiled to a 2,688-byte object. Both used the
provenance-checked Stage1 source `9667344cf0fd2e955a4e233ada1ea60033a16837`
and product SHA-256
`bed23103851823084b365d825570394243564f99e1c6e1c4dd896d633194797b`. The
focused AppKit adapter compile with `-fobjc-arc -Wall -Wextra -Werror -O2`
emitted a 21,944-byte object. These are source/native compile checks only;
current full Studio linkage, Finder launch, lease contention/replacement
behavior and cleanup-side exclusive acquisition remain unqualified. Legacy
artifacts with no protocol record remain unknown and protected. Cleanup
mutation remains unwired pending controller integration and qualification of
the native exclusive-lease and recoverable receipt paths.

## Explicit contents ownership inventory

Commits `c23caed`, `c077c13` and `4fc9529` implement the inventory producer
and bind it into Studio build and package sealing. Builders explicitly declare
all produced noncontrol files and directories. Complete traversal rejects
unknown descendants, symlinks, hard links, foreign owners and unstable reads.
Limits are 4,096 entries, 32 path components, 4,095 UTF-8 path bytes, 1 MiB JSON
and 10^15 total regular-file bytes. File entries contain `size_bytes` and
`sha256`; directory entries contain only `path` and `kind`.

Records use `mocap-studio-generation-inventory-v1` and live outside the artifact
at `build/.studio-generation-inventory/<artifact-id>.json`. `root_device` and
`root_inode` identify the artifact directory; `build_root_device` and
`build_root_inode` identify its owning build directory. Creation is exclusive,
requires the inherited global build lock, and syncs the external record before
sealing. `contents_inventory_sha256` binds it into generation metadata and the
lease. Package directory identity survives publication and backup renames.

Build controls `inputs.json` and `.studio-generation.lease`, and package controls
`Contents/Resources/{PACKAGE-GENERATION.json,BUILD-INPUTS.json,.studio-generation.lease}`,
are excluded to avoid a digest cycle. Cleanup must verify those controls
independently. External inventory records remain recovery dependencies after
quarantine. Unregistered copies and incomplete generations remain protected;
failed-generation ownership requires its separate creation journal.

Shell syntax, Python AST parsing and diff whitespace checks passed. No build,
package execution, crash recovery, inventory tampering or cleanup mutation
qualification is claimed for this integration yet. Native validation and
current end-to-end qualification remain open.

## Native adapter and creation-journal source progress

Engine commit `c52023cea002f8295f72d0b304ed1f5743cc10e5` supplies the
native move, Restore and reconciliation adapter. Primary commit `aadafd13`
adds its native build/link inputs and bounded Elisa extern declarations. The
adapter source includes descriptor-relative validation, retained locks,
exclusive operation IDs, intent records and parent synchronization. This is
implementation progress; controller integration, full linkage and native
failure/restart acceptance are still open. The compile records for compiler
`9667344c` above are now historical comparisons against current `cc657038`.

Primary `ca94635` adds creation-journal transition contracts and seventeen
laws. A Created journal can enter Building; a Building journal can become
Failed or become Sealed with verified product evidence. Publication requires
a verified seal and durable namespace publication. Only verified inactive
builders can become Abandoned. Failed, Abandoned and Published records cannot
restart or be reclassified through this policy. Contradictory active-owner and
inactive-builder evidence refuses admission.

Every advance requires matching positive revisions below the signed i64 limit,
retained global/artifact exclusive locks, verified root/artifact/journal
identities and a durable prior record. The next revision cannot wrap. Only
confirmed durable phases map into the incomplete-generation cleanup policy;
uncertain writes remain Unknown until native reconciliation. The functions
authorize preparing an update; they do not prove a filesystem write succeeded.
Initial journal creation, producer registration, durable persistence, startup
reconciliation and cleanup integration remain to implement. These new laws
have not yet compiled or received authenticated proof qualification.
