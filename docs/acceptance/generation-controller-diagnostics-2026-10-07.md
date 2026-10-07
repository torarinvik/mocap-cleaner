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
five generated result readers plus wrappers. No executable was emitted.
The original dd wrapper refused compilation because restored source mtimes were
newer than its binary; no stale-product bypass was used for this observation.

Native retry execution, Busy/uncertain fault cases, keyboard/VoiceOver interaction,
authenticated laws and safe disposal after exact reconciliation remain open.
