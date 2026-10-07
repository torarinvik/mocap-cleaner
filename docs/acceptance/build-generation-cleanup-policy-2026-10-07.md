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

Initial producer registration is now implemented in `6926f46` and wired into
Studio builds in `6eb048e`, before snapshot and native/Elisa product writes.
The external `build/.studio-generation-creations/<artifact-id>.json` record
uses schema `mocap-studio-generation-creation-v1`, phase `created`, revision 1,
a random operation ID, original relative path, build/artifact/lease identities
and explicitly declared entries (including control records). Registration
requires the global exclusive lock, a private empty lease under an exclusive
artifact lock, and an initial tree containing only declared directories and
that lease. Unknown preexisting outputs refuse registration.

The producer uses exclusive record publication, file/parent/build directory
synchronization and repeated descriptor/path checks. It preserves uncertain
published records and replaced temporary entries for inspection. The helper
itself is a captured build input. Bash syntax and Python AST parsing passed;
no helper execution or crash/race acceptance is claimed. Package registration
is now wired before copying any product files (`c3ec81d`), with its complete
control/file/directory plan captured. The producer also verifies exact published
record bytes and stable bindings before and after parent synchronization
(`739248b`). Later phase updates, native record consumption and failed-generation
cleanup remain open. A Created record never establishes failed/abandoned eligibility.

## Immutable start and failure events

`a2f4ad2` / `211723d` append `<id>.revision-2.json` before any build or
package product writes. It retains the initial ownership record, links its exact
bytes with `previous_sha256`, and records Building at revision 2. The bounded
reader refuses duplicate JSON keys, unsupported fields, noncanonical declared
plans, changed prior records, replaced ancestors and mismatched lease identity.

`74bb2f2` / `acd76f3` add `<id>.revision-3.json` for owned unsealed build
failures. It links the exact Building event, retains exit status and observed
file/directory entries with file sizes and digests. Recording requires retained
global/artifact exclusive locks, the original private empty lease, matching
build/artifact identities and a stable tree containing only declared paths.
Unknown descendants or a nonempty/replaced lease preserve unresolved state.
The build EXIT handler attempts this only before successful product sealing;
later publication, packaging or check failures cannot mark a sealed build failed.
Package failure events, Sealed/Published events and restart consumption remain
open. SIGINT/SIGTERM exit statuses are retained; abrupt process death still
requires inactive-builder reconciliation, not an invented failure event.

Creation-journal contracts now include explicit verified-unsealed evidence and
refuse contradictory sealed/unsealed flags. There are 24 public laws and two
private fixture helpers. The earlier 23-law version compiled on `0fb79267`;
the final 24-law source still needs current compilation and authenticated proof.
Bash syntax, Python AST and repository line-length checks passed for the new
failure path. No runtime, crash, cancellation or filesystem race acceptance is
claimed from those source checks.

### Sealing and executable publication records

The build now appends a Sealed revision 3 only after checking the complete
contents inventory, executable digest, input record and sealed lease against
the original creation identity and Started revision 2. Failure and Sealed are
mutually exclusive revision 3 records. A sealed product is not a failed build
when a later publication or packaging step fails.

Publication retains the global exclusive lock and the original artifact's
exclusive lease across the current executable symlink rename, both directory
syncs, and Published revision 4 publication. The event links the exact Sealed
record bytes. Revalidation checks the prior records, original filesystem
identities, full product seal and current pointer. A failure after rename
reports an uncertain publication and preserves the current generation for
reconciliation; it does not claim a rollback or a durable Published event.
Both helpers are captured in build and package input identity records.

Evidence is limited to source review, Python AST parsing, shell syntax checks
and clean diff checks. These helpers have not yet been exercised by a successful
current full Studio build. Restart reconciliation, package terminal events and
native consumption of creation records remain open; the records alone do not
establish cleanup eligibility. The existing journal transition policy and laws
cover the intended Sealed/Published admission rules, but current authenticated
proof qualification remains pending.

Publication retries now refuse before pointer mutation when revision 4 already
exists, or when the current pointer already names this generation without that
record. The latter is an interrupted-publication reconciliation case, not
permission to redo the rename. Two additional source laws reject Published to
Published and Published to Building. The journal law count is now 26; their
current compiler and authenticated proof qualification remain pending.

The pure journal kernel now separates `may_begin_publication` from
`may_advance(Sealed, Published)`. Preflight requires verified absence of a
Published record and a current pointer that differs, along with the sealed
product, original identities and both exclusive locks. It does not require or
produce publication durability. Five additional laws cover that distinction,
existing-event refusal, already-current refusal, terminal-phase refusal and
exclusive-lease admission. There are now 31 public journal laws. These are
source contracts awaiting current compiler and authenticated proof evidence.

### Unsealed package failure recording

The failure event writer now accepts both original studio-build and
studio-package creation records. For packages it opens the nested Resources
lease through directory descriptors and rechecks that ancestor's identity,
the original lease identity, the prior journal records and the observed
subtree. Unknown descendants, a sealed/nonempty lease or replaced ancestors
refuse the event. The package script installs its failure handler immediately
after Started and disables it after product sealing. SIGINT/SIGTERM preserve
nonzero status; SIGKILL still requires inactivity/reconciliation evidence.

Python source and embedded package Python blocks parse successfully, shell
syntax and diff checks pass. Runtime failure injection and authenticated proof
qualification remain pending. This adds failure records, not native cleanup
consumption or package Sealed/Published terminal events.

### Current package seal events

Current protocol-1 packages now append Sealed revision 3 after verifying the
PACKAGE-GENERATION record, copied BUILD-INPUTS product/generation identity,
complete contents inventory, readonly lease and actual copied executable.
Resources and MacOS are opened and rebound through directory descriptors.
The event retains the original creation root/lease identity, links Started
revision 2 bytes and records the package, input and lease control digests.
Both locks remain held through durable journal publication.

Unrecorded protocol-0 legacy packaging does not produce a Sealed creation
event and remains outside current cleanup qualification. The new helper is
wired into current packaging and captured in build/package input snapshots;
compiler `scripts/platform.sh` is also captured. AST, embedded-Python parsing,
shell syntax and diff checks passed. A fresh full build exercising this new
package event is pending. Package Published events and interrupted bundle
publication reconciliation remain open.

### Current package Published events

The current package path now holds the new package lease exclusively before
publication and retains it through parent syncs and Published revision 4.
An existing current bundle is opened by directory descriptor and its readonly
lease is also locked exclusively before moving it to `previous.app`. Both
moves use Darwin `renameatx_np(RENAME_EXCL)`; a replacement destination refuses
atomically, without a check-then-overwrite fallback. Unsupported exclusive
rename support refuses publication.

Published links the exact Sealed event, records the current relative path and,
when present, the previous root identity and backup path. The new seal and
journal chain are rechecked after the move and through event publication.
Failures after either move preserve both generations and report uncertainty;
restart reconciliation and a user-facing recovery action remain required.
This replaces the automatic shell rollback only for current protocol-1 builds.
Unrecorded legacy packaging stays outside current cleanup qualification.

Source AST/embedded Python, shell syntax and diff checks passed. A fresh full
build exercising package Published is in progress. The preceding successful
`studio-build.r2TDoB` build includes the redo-draft fix, but its package reached
Sealed revision 3 only and cannot qualify this newly wired helper.

### Pre-move package publication intent

The package helper now durably creates a separate publication-intent record
before moving either bundle. It links exact Sealed revision 3 bytes and binds
the proposed current path, previous root identity and previous lease identity.
Published revision 4 additionally binds the intent digest. An existing intent
refuses retry and requires reconciliation; its presence never establishes that
the moves or Published event succeeded. Prior bytes, previous Resources/lease
bindings and held lease descriptors are rechecked through record publication.

The journal admission contract now requires verified intent absence. A new law
refuses admission when an intent already exists, bringing the total to 32.
The exact law source compiles with the clean e34f2c compiler; object SHA256 is
`ccf25564a1a70cb4bbfdbc6526413882bae2d68fff014c91265f0cef4cb99390`.
This is compilation evidence, not authenticated proof or interruption testing.
The preceding successful package `studio-package.xqxehP` has Sealed3 and
Published4, but predates the pre-move intent implementation. Its
`previous_sha256` links Sealed3; it is not a digest of the previous bundle.
Fresh intent-aware build qualification and restart recovery remain open.

### Reconcile an exactly current package

`scripts/reconcile_studio_package.sh studio-package.GENERATION_ID` acquires
the verified global lock and finishes only the layout where the intended new
package is already current. The bounded reader checks Created/Started/Sealed,
exact publication-intent fields and digests, original new root/lease identities,
the current product seal, and any old backup's complete recorded seal and
lease identity. Both artifact leases must be available exclusively. It syncs
the observed publication directories before creating a missing Published event.
An existing byte-exact Published event is revalidated and synced without
replacement. No bundle is moved or removed.

Pending-before-move, old-backup/current-absent, conflicting, busy and unknown
layouts refuse. They remain protected for additional recovery actions. This
command does not establish automatic restart recovery or a user-facing UI
flow. Source AST, wrapper shell syntax and diff checks pass; the reconciliation
command has not yet been exercised or fault-injected, and authenticated native
I/O correspondence remains open.

### Bounded generation JSON decoding

Contents inventory and creation/control readers now share duplicate-field
refusal and a pre-decode structural nesting limit of 32. The scan distinguishes
JSON strings and escaped quotes/backslashes, so brackets inside string values
do not consume structural depth. Existing byte limits, descriptor ownership,
no-follow reads and before/after identity/version checks remain required.
Malformed or over-deep JSON refuses instead of reaching unbounded parser
recursion. Python AST and diff checks passed; malformed/fault-case runtime
qualification remains open. A successful normal build alone cannot establish
those refusal cases.
