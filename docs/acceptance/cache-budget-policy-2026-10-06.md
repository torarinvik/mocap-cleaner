# Cache budget admission policy

The new `CacheBudgetPolicy` defines a **per-cache logical** cap of 4,000,000
entries and 67,108,864 estimated bytes (64 MiB). `channel_request` accounts
operation results, one source snapshot, keys, and operation records. It counts
each stored `i64` value as 8 bytes and each logical operation record as 64
bytes. Product and sum operations check their cap before multiplication or
addition; any known positive capacity overrun maps to `FALLBACK_CAPACITY`.
The generic decision function maps negative accounting to `FALLBACK_INVALID`;
the channel request function requires nonnegative dimensions.

Both fallback decisions map to `EVALUATE_FULL`, which preserves the full
uncached computation path. This policy does not bound aggregate cache banks,
allocator metadata/spare capacity, transient evaluation memory, or physical
RAM peak. The channel cache now checks this admission before allocating its
result arrays and exact identity snapshots. Refusal clears retained logical
contents and evaluates enabled operations in order, preserving operation timing
and evaluation counts. Rig cache admission is still outstanding. Clearing
contents does not prove release of allocator capacity or a physical RAM bound.
Current compiler `720896f4` emits a fresh channel adapter object at
`build/cache-fallback-compile.FeyCI8/stack.o`. Runtime cache/full comparison
and proof replay remain open; this compile-only evidence does not close them.
The exact channel layout and checked arithmetic laws are in
`proof/cache_budget_laws.elisa`.
