# Batch queue compilation — 2026-10-06

Fetched compiler origin and checked Stage1 source/product provenance at
`23a0e16a`. Every compile below used the normal wrapper without stale overrides,
exited 0 and emitted a fresh nonempty object. No executable fixture was run.

| Slice | Fresh artifact |
| --- | --- |
| Resume policy and four laws | `build/batch-resume-policy.ROUNTL/laws.o` |
| Queue model | `build/batch-queue-model.SORmke/queue.o` |
| Seven lifecycle laws | `build/batch-queue-model-laws.0C6cnt/laws.o` |
| Item validity policy and seven laws | `build/batch-item-policy.H2AkQJ/laws.o` |
| Lifecycle laws with item validity | `build/batch-item-queue.wNCTgr/laws.o` |

The model bounds queue size and workers, validates running-count correspondence,
drains running work on cancellation, revalidates individual retries and exposes
explicit resume. Warning approval survives successful publication. Item
validity rejects negative warnings, inappropriate approvals and clean output
records carrying warnings. Empty queues remain NotStarted.

The initial model used `.len()` instead of Elisa's `.count` field. Correcting
that source API error resolved its compile failure.

Proof replay remains pending. Supplied preflight, review and publication
booleans do not establish filesystem or immutable result identity. Native
workers, durable manifests, exact review binding, create-only publication and
recovery, recipe storage and Studio UI wiring remain required.
