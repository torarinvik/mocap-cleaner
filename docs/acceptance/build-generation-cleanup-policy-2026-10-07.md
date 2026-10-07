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
mutation remains unwired until exclusive-lease and recoverable receipt paths
are implemented.
