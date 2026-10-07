# Generation controller integration diagnostics

These are diagnostic observations, not current full-plan qualification.

## Background task result consumption

The full app at controller commit `0ae9584`, with provider retention capture
`5f4e2a4`, refuses the concrete generic task result reader:

```
ctx_concurrency_result_read__Result.42961@379 (index expression)
ctx_concurrency_result_read
```

The captured compile log is
`build/latest-compiler-qualification/generation-controller-main.compile.log`,
SHA256 `6f31f4978349afe4f1c8a851d48d82934383657e3519e075406135d0eaee5893`.
Compiler source is `e34f2c0656aac1232ad72da6516c7eb89f866a47`,
with selected Stage1 product SHA256
`b2e4d197df34892b4f7a43a5ff751aecd6c95c08a998783c5687548f50559ae1`.

The provider worker's reduced controller-shaped poll/join/optional snapshot
probe passes object compilation. A second simple owner named `Result`, with
its own task/join specialization, also compiles alongside the generation
consumer. That probe is `build/candidate_scan_two_results_probe.elisa`, SHA256
`8212d78fd910a2ae5c10ad2e63e84a17b25c81d2aa2b8b14e9c4b04678769e46`.

A smaller mixed graph with the actual contact and locate result types refuses
four bodies: `ctx_concurrency_ref_release@838`, `barrier_wait@1121`,
`poll_ready__Result@950` and `poll_ready`. Its source is
`build/candidate_scan_real_results_probe.elisa`, SHA256
`2b3500cd890d7fd06f9497ae64ef3b84dea4fcdbbc52f873163455e0327e058d`.
This different failure narrows diagnosis; it does not prove the same cause.
Keep the intended owning snapshot API while investigating specialization and
declaration-owner context. No executable probes ran.

## Move confirmation and result integration

The later move-controller capture reports 14 backend declines and writes no
object. Its log is
`build/latest-compiler-qualification/generation-move-controller-main.compile.log`,
SHA256 `c7d451b2596d0bda0c559efc0d468e56f63c233eb4e4b7d1eee2625421fcb440`.
The declined bodies include `classify`, `resource_clear_slot`, `state`, `reset`,
`request`, `fail`, `cancel`, `cancel_for_owner`, `retry`, `refresh`, and two
concrete result readers with their wrappers. This capture precedes the final
Storage guards in `5cda1dd` and the later result messages; it cannot qualify
those changes or establish their exact present decline set.

Result classification and nine accompanying law declarations at `021a276`
compile as an object using the selected Stage1 above. The policy requires a
bounded operation identity, certain lock release and exact quarantine/original
reconciliation before describing a move as recoverable or not moved. Unknown,
contradictory and retained-handle cases remain unresolved. These are source
compilation observations, without executable tests or authenticated proofs.
No result dismissal, repeated cleanup or restart recovery is qualified by this
policy compilation.

## Foot-quality execution evidence limitation

The retained diagnostic bundle at
`build/diagnostic-check-20261007/foot-clips/` records terminal `rc=14`.
Its run log SHA256 is
`9b8b0bbdec89d85fb987b5f15b69729db3e0b5c88404f04383eaf4639828d476`;
its retained build key is
`bada68ccda515f3ed0559668feab841b43fe4d2e52b7d8253f12c1e9ea3ac22f`.
The bundle contains the log, key, compile-cache status and terminal observation;
it contains no executable or source snapshot. A hash from today's shared
executable cannot establish the identity of that earlier execution.

Applying today's predicates to the retained metric rows yields three clip-level
OR failures (clips 4, 7, 8), no knee failures, and thus an expected `rc13`.
Today's changed source tree cannot establish the exact predicates compiled for
the captured run. The extra increment remains unexplained. Recover the matching
executable/source snapshot or capture a fresh exact run before attributing it to
compiler behavior or the correction algorithm. Preserve existing tolerances.

## Explicit retained-handle release retry

Move and Restore controls now offer **Retry Release** when their retained reply
owns a positive native handle. The entire affine reply transfers to the drain
worker; captured root, operation identity, commit status and diagnostic bytes
remain retained. The controls show Releasing during the job and return to
Recovery pending afterward. A release retry does not establish artifact location
or authorize another mutation. Busy/unknown results keep the token; no automatic
retry loop is introduced.

Admission requires all five generation jobs idle, an open Storage/review screen,
no queued close, and no storage mutation modal or running batch. It deliberately
does not require a fresh inventory row or ledger capacity: release operates on
already owned native state. Native acquire_entry permits closing an existing
registered token even when registration is inhibited by sticky release uncertainty.

The expanded nine admission/reconciliation law declarations compile as an object
with the isolated UI collision repair candidate. Its source base is dd0312ee,
source tree c9aa21a6692529aab8ab58faf56407bfd44c23ef56aead658ba48e48a95d182e,
product SHA256 7862a5472885a2956f012d27cf0635beff5af126c6c79d5263abe61d11a987f2.
The compiler agent reports no new frontend/affine diagnostics for integrated
controllers; the application still declines at ledger global initialization and
five generated result readers plus wrappers. The final label capture is
`build/latest-compiler-qualification/generation-main-final-label-current-candidate.compile.log`.
No executable was emitted.
The original dd wrapper refused compilation because restored source mtimes were
newer than its binary; no stale-product bypass was used for this observation.

Native retry execution, Busy/uncertain fault cases, keyboard/VoiceOver interaction,
authenticated laws and safe disposal after exact reconciliation remain open.

## Exact recovery acknowledgment

Move and Restore now expose **Resolve Review** for retained zero-handle replies.
The selected recovery observation must be current for the current workspace,
match the captured root, canonical operation, artifact ID and relative path,
have a known Acquired native status and describe Quarantined, NotMoved or
Restored. Both the old reply and reconciliation must report certain release;
active jobs, queued close, mutation modals, missing metadata, absent ledger
identity and every unresolved outcome refuse disposal.

Move comparisons use the retained wire and canonical reply operation. Restore
captures all four identity fields before dispatch (`d274c70`) and preserves them
through reply/drain ownership. Starting Restore records the selected identity in
the bounded ledger first; existing identities remain admissible at capacity.
Acknowledgment clears only the owning reply and captured controller metadata.
It retains the ledger identity and a scalar reconciliation summary. Move stays
RecoveryPending rather than publishing an earlier canceled operation as success.
Restore returns to Idle, requiring a new Review/Confirm sequence for a later
Restore. The VoiceOver Restore control uses the same admission as the visible
control, including retry and resolution cases.

The thirteen resolution law declarations compile with the fresh UI diagnostic
candidate before its next source edits. A Move-only integration reached the same
11 backend declines without frontend diagnostics. Final Move/Restore integration
compilation is pending the compiler rebuild: the candidate wrapper refused its
changed source digest and no bypass was used. These observations are source
compilation evidence only. Exact-byte native replay, repeated operations,
cancellation, uncertain release, focus/VoiceOver and authenticated proof
acceptance remain required before closing recovery.

## Recovery status priority

`02b05e3` keeps the selected operation's current reconciliation result visible
when other pending receipts exist, appending their unresolved count. An incomplete
listing also stays explicit alongside selected-operation evidence. Queued scans
show Waiting, active scans show Reconciling, and inactive stale observations
request refresh/reselection instead of claiming work is still running. Closing,
invalid metadata and overflow retain precedence. No receipt is promoted or
removed by this presentation change.

Ten status law declarations accompany the pure classifier. Their first compile
attempt was refused because the compiler candidate source digest had changed
while it was rebuilding; no stale-product bypass was used. Qualification awaits
the rebuilt product. UI/runtime and authenticated proof acceptance remain open.

## Status and path source compilation after representation fixes

`bca09c3` gives the new finite status enums explicit i64 representation, matching
repository conventions. Their eight review-status and ten recovery-message law
declarations compile as objects, as do the responsive/Unicode path laws including
the oversized-line bound from `49292cb`. The candidate wrapper accepted the
source/product identity at invocation: product SHA256
`3222e44429ef3158f2f05aa492db7755b5434c0b0d375d3e299841222710dab6`,
source base dd0312ee with captured tree
`6da30810bb9e296751161af5e5dfd04c068a3a1f628d2dfbfce9e86763bf248b`.
These are comparison source-compilation observations: the compiler agent then
committed its repairs and merged fetched upstream 218c2c22 at ac0f4423, requiring
a new matched product before current qualification.

Visible and VoiceOver path segments now share responsive geometry and explain
whole-path hexadecimal escapes for invalid/control bytes. Small panels retain a
Done exit; no off-screen path labels are published as visible segments. Settled
Restore summaries no longer mask Recovery Operations; closing, actual workers
and a live Restore confirmation take precedence. Path traversal computes escape
mode once per traversal, and oversized line requests stop at the end. No measured
latency or native/assistive-technology runtime acceptance is claimed.

The main compile started with the earlier candidate completed with exit 0 and
emitted `build/generation-current-main.o` (SHA256
`ea9bdfb96861793eefc7e6e406960330a0b7901eb52db762c36e1d0057fc96ff`).
Its terminal log at
`build/latest-compiler-qualification/generation-status-path-main.compile.log`
is empty (SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).
This remains diagnostic because compiler source changed during the invocation.
It cannot qualify the merged compiler or the whole current application; no native
link, executable, runtime or authenticated proof result follows from this object.
