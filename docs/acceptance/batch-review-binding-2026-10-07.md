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
transitions through the existing recovery store while the workspace lock is
held. Enqueue stores exact staged GLB, recipe and report snapshots with a
versioned per-item journal under `build/.mocap-export-recovery-*`. Claims
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
warning list does not yet have an independent parser, so reopened items remain
Recoverable even when final bytes match; they never regain Passed/Warning from
the journal's state or warning count. Empty durable queues and the batch UI
entry point are not yet wired into Studio.

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
