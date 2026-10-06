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
and evaluation counts. Rig cache admission is described below. Clearing
contents does not prove release of allocator capacity or a physical RAM bound.
Current compiler `720896f4` emits a fresh channel adapter object at
`build/cache-fallback-compile.FeyCI8/stack.o`. A direct proof run on the
committed policy reports 30/39 obligations proven and 4 replay gaps; the law
file reports 47/81 obligations proven and 7 replay gaps. Both runs also report
unverified callee summaries, so the arithmetic and fallback proof slice is not
qualified yet. Runtime cache/full comparison and rig-cache qualification remain
open; compile-only evidence does not close them.
The exact channel layout and checked arithmetic laws are in
`proof/cache_budget_laws.elisa`.

## Aggregate channel bank admission

`CacheBankBudgetPolicy` caps estimated logical contents at 268,435,456 bytes
(256 MiB). The GLB adapter totals actual retained result/source/key/operation
counts once, then replaces each slot's contribution during evaluation. A bank
already beyond the limit discards cached contents before processing; an
inadmissible replacement discards that slot and evaluates the complete stack
with profiling. No output edit or operation is discarded by this decision.
Checked sums/products refuse invalid counts before arithmetic overflow.

Current compiler `720896f4` emits the combined performance fixture object at
`build/cache-bank-integrated.YrIMRg/fixture.o`. Runtime equivalence and proof
replay remain open. This estimate excludes bank headers, spare allocator
capacity, transient evaluation/output copies and the rig cache. Clearing
logical contents does not prove physical capacity release. Eviction order and
performance under pressure still require measured qualification.

## Rig cache admission

The rig adapter now checks a separate 256 MiB logical contents budget before
constructing its schedule or copying the input clip. It accounts three clip
snapshots and operation/schedule records. Per-element estimates are 192 bytes
for joints, 32 for quaternions, 24 for vectors, 8 for indices/times, 1 for flags
and 80 for operation records. These reflect the current field schemas and
require reassessment if those schemas change; they are not allocator metrics.
Refusal invalidates all retained snapshots and runs `RigOps::run_clip` on the
complete input, preserving its returned summary and applied-operation count.

Current compiler `720896f4` emits the combined fixture object at
`build/rig-cache-budget.vjUN9z/fixture.o`. The scalar policy has contracts and
five laws. Runtime comparison, independent proof replay, physical memory
release and transient peak qualification remain open. The channel and rig
limits are separate; their combination is not a whole-process memory limit.

## Focused proof comparison on compiler 720

The clean `4da/720` candidate reports the following for current budget files,
including imported helper obligations. Every report remains unqualified:

| File | Produced / obligations | Replayed / produced | Replay gaps |
| --- | ---: | ---: | ---: |
| Aggregate bank policy | 44 / 56 | 40 / 44 | 4 |
| Aggregate bank laws | 52 / 81 | 48 / 52 | 4 |
| Rig budget policy | 37 / 46 | 33 / 37 | 4 |
| Rig budget laws | 42 / 61 | 38 / 42 | 4 |

Reports are `build/cache-budget-focus-{0,1,2,3}-720.json` respectively.
Inherited findings include checked-product wrap guards, typed execution
contracts and unverified helper summaries. Aggregate contents and rig laws
also report ambiguous constant goals; lexical owner resolution requires
investigation. No contract or existing baseline was weakened in response.

Checked arithmetic is subsequently extracted into `CacheBudgetArithmetic`,
with its six original laws moved intact into a dedicated proof module. Bank
and rig policies now import only arithmetic and layout estimates, avoiding
unrelated channel execution obligations. The combined fixture compiles at
`build/cache-arithmetic-extract.eSIb2g/fixture.o` with compiler `720896f4`.
The same `4da/720` comparison reports arithmetic laws 20/30 certificates,
all 20 replayed, and rig laws 19/34, all 19 replayed. Neither report is fully
proved: checked-product wrap guards, helper summaries and ambiguous goals
remain. The changed obligation totals reflect the include graph, not weakened
assertions. These reports are `build/cache-arithmetic-laws-720.json` and
`build/rig-budget-extracted-laws-720.json`.
