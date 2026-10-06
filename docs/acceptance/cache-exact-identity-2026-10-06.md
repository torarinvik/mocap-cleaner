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
evaluator. Compilation awaits the current constructor-owner compiler seed;
existing cached/full executable comparisons await the authorized full check.
No executable tests were added or run for this change.

Exact snapshots add one source-channel copy and one operation list per cache.
Memory budgeting, eviction and runtime measurements remain open. Rig prefix
and final caches still use modular fingerprints and need equivalent exact or
revision-bound admission; this change does not close all cache correctness.
