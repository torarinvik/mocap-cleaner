# Exact channel-cache identity

The operation channel cache previously admitted reuse from a chained modular
hash alone. Equal hashes do not establish equal source samples or operations.
It now retains the source samples, bone, loop mode and operation snapshot and
compares them before admitting a cached prefix. Two disabled operations remain
equivalent regardless of their inert parameters. Cached result storage must
cover the retained operation/frame shape before indexed reuse. Hashes remain
an additional rejection filter, preserving the existing prefix scan.

`CacheIdentityPolicy` requires hash, exact input, exact operation and valid
storage together. Clean candidate prover `4da37c97` built with compiler
`45330579` proves and independently replays its laws 12/12, with zero gaps,
findings or semantic errors (`build/cache-identity-laws.json`). This scalar
evidence does not prove array comparison, snapshot ownership or the integrated
evaluator. Compiler `3c72f59f` emits a fresh channel-cache object without
diagnostics in `build/cache-compile.teUM8X`. The initial local-array assignment
was rejected for escaping its inferred region; snapshot copying now extends
the cache's existing array storage. Existing cached/full executable comparisons
await the authorized full check.
No executable tests were added or run for this change.

Exact snapshots add one source-channel copy and one operation list per cache.
Memory budgeting, eviction and runtime measurements remain open. Rig prefix
and final caches now also require retained input and effective-operation
identity alongside hashes. Their additional ownership and memory requirements
still need qualification; this change does not close all cache correctness.

## Rig prefix and final admission

Rig cache admission retains the full pre-operation clip, exact source token,
threshold, operation list and scheduled step order. Prefix reuse compares the
effective scheduled operations before the contact boundary. Final reuse compares
the full effective operation list, including contact edits. Both require exact
input clip equality, including hierarchy, roles, times, TRS, animation slot facts
and dirty masks. Floating values are compared bytewise to distinguish signed
zero and preserve actual representations. Hash collisions or a threshold change
alone cannot authorize reuse.

Compiler `3c72f59f` emits a fresh object without diagnostics in
`build/cache-compile.nyxmdr`. This does not qualify the pointer-cast float byte
comparison, snapshot lifetime, cache/full equivalence or added memory pressure.
The shared admission policy/laws remain the proved scalar kernel; integrated
proof and runtime qualification are separate and unfinished.

## Integrated compile and proof observations

The existing `test/studio_perf.elisa` fixture compiles to a fresh object with
compiler `3c72f59f` in `build/cache-fixture-compile.jkAG46`; it was not executed.
The broad evaluator proof route with candidate `4da37c97` processes channel
stack 1,094/1,146 producer obligations and rig cache 2,162/3,032, both in
unsupported state. Logs are `build/exact-cache-integration-proof.log` and
`build/proof/src_ops_{stack,rig_cache}.elisa.txt`. These partial counts neither
close integrated correctness nor replace the existing reviewed baselines.

The later shared schema extraction, bulk snapshot copies and performance-cache
constant grouping compile together in the existing Studio performance fixture
with current compiler `720896f4` (`build/cache-schema.p5f224`). This is fresh
object evidence, not a runtime rerun after those edits. The earlier diagnostic
full check passed its cache/performance tests on the earlier source snapshot.
