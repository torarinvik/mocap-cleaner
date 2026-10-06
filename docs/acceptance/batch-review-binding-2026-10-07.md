# Batch review binding — 2026-10-07

The new exact identity and review-token law source compiled with the normal
current compiler wrapper. Command:

```sh
../Elisa-compiler/scripts/elisac_stage1.sh -o build/batch-review-binding-compile.yDG0DV/review-laws.o proof/studio_export_batch_review_binding_laws.elisa
../Elisa-compiler/scripts/elisac_stage1.sh -o build/batch-review-binding-compile.yDG0DV/source-laws.o proof/studio_export_batch_source_identity_laws.elisa
```

The initial proof compile exited 0 with 54,648 bytes for review laws and 10,800
bytes for source identity laws. The lifecycle source was later compiled with
the proof source included; the latest fresh outputs are
`build/batch-lifecycle-binding-compile.0PDvyN/review-laws.o` (347,392 bytes)
and `source-laws.o` (10,800 bytes), both exit 0. No executable or native test
was run. Initial compile attempts found unsupported multiline Boolean
expressions and a reserved identifier; both were corrected. This is compile
evidence only, not proof replay or native qualification.

`StudioExportBatchReviewBinding` owns the queued identity and a private-field
review token. Review issuance requires explicit review, an exact byte/scalar
match with the current identity, and an AwaitingReview item. Publication has
no caller-supplied success or destination-absence booleans. It rechecks the
source through the new no-follow identity snapshot API, reads exact staged bytes, publishes the GLB
with `commit_new_with_status`, and compares the resulting final bytes against
the reviewed bytes. It publishes JSON and text using the existing create-only
sidecar API only after the GLB verifies, then reads each sidecar back and
compares exact bytes. A public immutable receipt records each stage's native
outcome, exact-byte verification and staging disposition before the queue
transition.

The engine API was committed on `mocap-track` as `e11085c1`; it resolves a
canonical path, uses `lstat`, rejects final symlinks and non-regular files, and
returns device, inode, size and nanosecond mtime or a failure code. The source
proof laws compile, but native source was not built or tested. The bound queue
exposes item/progress snapshots, worker claims, claim-bound completion, drain
cancellation, selected retry and explicit resume. Claims bind the retained
identity and per-item attempt; stale attempts fail closed. Cancellation blocks
publication IO until resume. On retry, already-present outputs count only
after exact byte comparison, so partial reports can be completed create-only
without overwriting. Exact verified final outputs remain successful when
staging cleanup is pending; the receipt reports residue separately.

Source races between identity observation and publication, durable queue and
recovery records, destination/recipe/rig preflight verification, proof replay,
and UI review wiring remain unqualified. The separate preflight policy still
accepts facts that its caller must establish from the OS.

## Durable batch queue journal — 2026-10-07

The batch review binding now offers a durable queue constructor and routes its
enqueue, worker claim/completion, publication, retry, cancel and resume
transitions through the existing recovery store. Durable APIs accept a
caller-owned live workspace transaction descriptor per operation and retain no
descriptor in the paused or reviewable queue. The caller must release the
descriptor before returning to UI. Each transaction reopens the build root
without following its final path component and matches its canonical path,
device and inode against the queue's captured workspace root. A replaced root
or missing batch reservation fails closed. Enqueue stores exact staged GLB,
recipe and report snapshots with a versioned per-item journal under
`build/.mocap-export-recovery-*`. Claims
persist the incremented attempt and Running state before returning a worker
claim. Journal failures after work or publication keep outputs intact and
surface Recoverable in memory. Updates are accepted only along the recorded
lifecycle and atomically replaced; unknown durability is followed by a
directory sync attempt.

`reopen_durable` scans the bounded recovery inventory and rejects unreadable or
invalid record directories rather than dropping them. It checks source
identity with the no-follow source adapter, rejects symlink/non-regular
snapshot paths, reloads exact snapshot bytes, compares staged/final GLB and
report files byte-for-byte, and checks the stored publication stage facts.
Interrupted Running records are atomically rewritten to Recoverable before the
queue is returned. Serialized approval is not stored or restored. The report
warning list is independently counted from both matching report snapshots
using a strict parser for the stable Studio JSON and text suffixes. Unknown or
malformed report formats remain Recoverable. Reopened clean completed outputs
may regain Passed and warning outputs regain Warning, always unapproved. A
recovered warning requires a fresh explicit acknowledgement bound to retained
identity and attempt; it is memory-only and must be repeated after reopen.
The prepared-export queue panel and capture extension exist as separate modules,
but remain unimported and unqualified pending Studio composition and native
review. They enqueue an already reviewed single export; source selection and a
multi-take evaluation worker remain open M6 work.

Batch IDs are reserved by `mkstemp` using a create-only marker inside the
selected build directory. The six-character ID is read from the created marker;
the marker and parent directory are synced before the ID is returned. The
bounded allocator refuses new IDs after 256 retained reservation markers, and
the queue store checks that the marker remains a regular non-symlink file under
the live transaction. Reservation cleanup and native collision/race behavior
remain unqualified.

The native build-root adapter captures canonical path and device/inode from an
opened `O_DIRECTORY|O_NOFOLLOW` descriptor. Path/device/inode rechecks alone do
not close the replacement race; operations must remain relative to that opened
directory. The current adapter now does this for durable queue snapshots,
journals and final output/report publication. Recovery inventory enumeration,
batch-ID markers and source identity/output preflight checks remain path based.
Those checks retain a TOCTOU and are not described as secure same-object
operations.

The latest native slice adds a registry mutex and a release check that verifies
the caller descriptor still refers to the registered file and open-file
description before closing its integer descriptor. The mutex remains held
through descriptor-relative IO so release cannot unlock the workspace during a
native operation. Durable journal updates now read the prior journal with
`openat(O_NOFOLLOW)` and replace it with a synced temporary plus `renameat` in
the opened recovery directory. Initial recovery-directory creation, snapshots
and the initial journal also use the verified root with `mkdirat` and
`openat(O_EXCL|O_NOFOLLOW)`; files and directories are synced before success.
Reopen reads of snapshots and journals now use the same relative adapter. Final
GLB and report publication traverses each target parent with
`openat(O_DIRECTORY|O_NOFOLLOW)` and creates only absent regular files with
`O_EXCL|O_NOFOLLOW`, preserving unrelated outputs. A partial write is reported
as a partial artifact; a later report failure leaves earlier outputs intact and
the queue's receipt records each artifact separately. Recovery inventory
enumeration, reservation markers and source identity/output preflight checks
remain path based and retain the replacement TOCTOU. Fresh O0 compile-only
qualification on the provenance-checked Stage1 product produced nonempty queue
store (728,104 bytes), review binding (949,472 bytes), publication module
(124,480 bytes), and publication laws (129,056 bytes) objects. Strict C11
syntax checking of `storage_manifest_lock.c` and Objective-C syntax checking of
`file_trash_appkit.m` exited 0. No native runtime, concurrent lock, fd reuse or
filesystem replacement behavior was exercised.

Compile-only qualification used the provenance-checked normal Stage1 product
(`bb1f4095`) with `-emit obj -O0`; O2 dead-stripped these proof/module-only
fixtures to 336-byte symbol-only objects, so those outputs are not counted as
evidence. O0 outputs were nonempty: review-binding laws 850,816 bytes, journal
laws 301,104 bytes, queue model laws 153,424 bytes, recovery-policy laws
186,384 bytes, queue-store source 677,776 bytes and recovery-store source
483,048 bytes. The compiler exited 0 for each. No law replay, executable,
native adapter behavior, crash, race, flush/close failure, filesystem
durability or Studio UI qualification was run. The native recovery store still
needs qualification for directory enumeration, symlink races, atomic journal
replacement and sync failures.

Root subsequently ran `clang -fsyntax-only -fobjc-arc` on the current engine
`native/file_trash_appkit.m`; it exited 0 without diagnostics. This establishes
native source syntax only, not a linked adapter, file identity behavior or race
qualification. No native executable was run.

Warning recovery and acknowledgement changes were separately compile-qualified
with the same provenance-checked compiler at O0: report warning parser 13,328
bytes, parser laws 18,024 bytes, queue store 686,376 bytes, review binding
848,984 bytes, review-binding laws 874,640 bytes, and recovery-policy laws
186,384 bytes. These objects establish compiler acceptance only. No executable
report samples or native acknowledgement flow were run; report syntax support
is limited to the current Studio serializer format.
