# M5: responsiveness and reliability

[Roadmap index](../../IMPLEMENTATION_PLAN.md)

## 10. M5 — Responsiveness and reliability at production scale

**Touchpoints:** `app.elisa`, `model.elisa`, studio state, existing operation
and rig caches, engine host scheduling, elisa-ui rendering limits.

- [ ] Measure end-to-end input-to-preview latency with feet enabled, contact
      edits, long clips and large rigs. Profile actual screen playback and
      GPU drawing, not just headless kernel timings. Freeze named hardware,
      build and corpus before comparison: target 60 Hz playback/drag preview,
      p95 input-to-preview below 50 ms and visible job state after 100 ms.
      Record p50/p95/p99, dropped frames, sample counts and pass/fail in a
      reproducible benchmark record; developer diagnostics remain optional.
- [ ] Move expensive load/analysis/rebuild/export work out of the UI event
      path using an engine-supported worker/job boundary. Prototype safe Elisa
      ownership first; do not share mutable clip buffers unsafely. This is an
      integration gate for each load, analysis, rebuild and export path; a
      standalone job-policy proof does not establish asynchronous behavior.
- [ ] Connect the tested cancellation and supersession rules in
      `src/studio/job_policy.elisa` to each asynchronous load, analysis, rebuild
      and export commit point. Give each job a document revision and identity;
      apply results only to the matching revision and discard stale results
      after undo, take changes or new settings.
- [ ] Show progress/stage, cancellation and last valid preview. Coalesce rapid
      parameter changes; avoid spawning unbounded work per pointer event.
      Apply this boundary to session and Locate reads as well as take loading.
      An 8 MiB byte limit does not bound elapsed time: removable storage and
      special files can stall native reads. Define admitted file types, worker
      ownership, cancellation checkpoints and a user-visible waiting state;
      cancellation must preserve the document even if a native read cannot
      immediately be interrupted. Measure slow-storage behavior and refuse
      stale results after a newer chooser selection or document replacement.
- [ ] Make close, application termination and document replacement safe while
      workers own data. Retain every live affine handle until its result can be
      consumed; poll completion without blocking the UI. Record one pending
      close intent and resume the ordinary save/discard flow after draining,
      without requiring a second close gesture. Revalidate worker state at the
      final close handler, including jobs started while a prompt was open.
      Cancellation must remain available while waiting. Qualify failed jobs,
      stale results, dirty documents, repeated close requests and focus loss;
      no dropped handles, lost edits or publication into a replacement take.
- [ ] Keep playback/time mapping deterministic when results arrive; preserve
      playhead intent and pause/resume semantics during retime rebuilds.
- [ ] Extend narrow evaluation only where dependencies permit. Keep full
      contact-dependent rebuilds when required; measure before changing cache
      boundaries and compare against uncached output. Declare which fields must
      match exactly and which use a justified floating-point tolerance; cover
      operations, corrections, contacts, retime and cache boundaries.
      Hash equality must never establish cache identity alone. Qualify the
      channel and rig caches' exact source/effective-operation admission. Include collisions,
      source replacement with equal lengths, bone/loop changes, disabled edits,
      malformed retained storage and threshold changes in cache/full comparisons.
- [ ] Replace or safely extend the current fixed capacities after an ownership
      prototype. Until then display capacity before an action fails, preserve
      the draft and offer recovery; never truncate edits silently. Distinguish the 10,000,000-frame editing
      domain from the current 1,000,000-frame performance cache. Specify a
      bounded fallback above cache capacity; empty dirty windows must not
      discard edits or falsely report an evaluated preview.
- [ ] Bound cache/history/recovery memory; define eviction and invalidation.
      Set explicit budgets, retention and eviction order. Stress repeated take
      swaps, undo/redo, long sessions and batch use. Saving, undo, cancellation
      and capacity refusal preserve committed edits and the last valid preview.
      Qualify the channel cache's per-instance logical admission (4,000,000
      entries / 64 MiB estimated contents) against full evaluation, including
      disabled operations and timing/accounting during fallback.
      Qualify aggregate channel-bank and rig-cache admission, each with a
      separate 256 MiB logical estimate, including replacement accounting and
      fallback summaries. Verify budget estimates against evolving schemas.
      Establish allocator and transient memory bounds; the admission limits
      alone do not establish a process RAM bound. Measure cache pressure and
      eviction behavior so long sessions remain responsive.
- [ ] Optimize curves, issue rows and overlays for draw budget and density.
      Use explicit level of detail; selection and peak markers remain accurate.
- [ ] Record per-stage latency, memory, cache hits and stale-job rejection in
      optional developer diagnostics. Keep these details out of normal flow.

**Exit:** responsiveness targets measured on the corpus; cancellation and
stale-result scenarios pass; cached and full output agree; capacity pressure
never silently loses edits. No representation rewrite without a measured need.

### Verification worker supervision

The local proof runner now has a configurable per-file wall-time limit:
`PROOF_FILE_TIMEOUT` or `--file-timeout`, default 1800 seconds, matching the
remote corpus runner. Timeout is an invalid verifier run, produces an explicit
exit-124 diagnostic, discards partial evidence and cannot populate the proof
cache. Recheck timeouts are failures rather than claims of a semantic cache
mismatch. Existing already-running jobs are unaffected. Qualify timeout cleanup,
cache refusal and subsequent-file progress before relying on this supervisor;
it does not establish bounded prover search work or the proof timing target.

Runner cache format v3 also rejects prover exits outside the documented CLI
report codes 0/1, even if stdout contains a verification marker. Error reports
are discarded and not cached. Earlier cache entries are invalidated rather than
assuming they were produced under this stricter admission rule. Completed
unproven reports remain evidence of unresolved work, subject to existing proof
baselines; they are not promoted to successful verification.

Cache format v4 requires exactly one recognized verification state and complete
numeric obligation/proven/unproven totals whose sum is consistent. A `proved`
state with unresolved obligations is invalid. Reports missing totals or showing
inconsistent counters cannot be reused; discarded reports still fail the run.
Qualify malformed/partial summaries alongside timeout and abnormal-exit cases.

Cache format v5 retains obligation totals in its summary and validates the
state/counters again when reading a cache hit. Incomplete or inconsistent
entries lose their cached marker and are scheduled for fresh verification.
Counter text length is bounded before integer parsing so corrupt oversized
values cannot abort the entire run at Python's integer-string limit.

Cache format v6 rehashes each file and its transitive includes before starting
and after finishing verification. A changed queued/running source snapshot
produces an explicit invalid-run diagnostic and discards the result. This
prevents storing observed changed-source evidence under the earlier cache key.
It does not substitute for an immutable qualification checkout: changes that
are made and reverted between observations remain outside this detection.

The proof supervisor now consumes worker results in completion order and logs
each completed report or invalid run immediately with elapsed time and exit
code. A slow first task no longer hides other workers' progress. The message
says `report completed`, not `proved`; baseline and replay gates still determine
acceptance. Qualification of parallel progress and failure reporting is pending.

### Current compiler qualification gaps

- [ ] Qualify the corrected worker refusal laws against their exact final
      source. Commits `f9d0571` and `cc4d554` align the Boolean law bodies with
      their existing false-result contracts: cancelled/stale/changed identities
      and unavailable workers return the refused admission predicate itself.
      The true-result memo-restoration law still requires same source and refused
      publication. Fresh O0 objects qualify compilation only (identity 10,176
      bytes; worker policy 51,376 bytes). Independently replay these obligations
      and inspect any counterexamples before accepting their baseline. Include
      contradictory law bodies in the prover's negative qualification corpus
      when implementing the authorized verification workflow; a compiler object
      must never stand in for contract truth.

- [ ] Qualify the source-matched candidate compiler's module-constant generic
      argument resolution in the complete Studio graph. Candidate `73319dd1`
      emits the reduced `UiText::fixed_bytes_view_range[Buffer::CAPACITY]` call.
      Nonconstant and negative arguments emit no object; these reductions alone
      do not establish full application compilation.
- [ ] Reject array-extent mismatches during semantic checking, with the expected
      and supplied extents and owner-qualified constant in the diagnostic. A
      reduced wrong-owner extent currently reaches invalid LLVM argument types
      before refusing emission. Preserve refusal while improving this boundary.
- [ ] Reduce and repair the remaining full-graph optional-view/frame/camera/pick/
      gizmo backend declines. Stripped optional-return and affine-view narrowing
      reductions compile, so their success does not explain the full-graph
      failures. Retain complete graph diagnostics and exact input snapshots.
## Deferred edit completion feedback

Both contact-worker drain paths now finish queued rebuilds through one helper.
A successful new result replaces waiting feedback with a current-result message;
failed builds retain their failure guidance. Three completion obligations
compile with d2754a8e. Native worker drain, coalesced edits, failure and close
ordering still require qualification; source compilation does not close M5.

Undo and Redo now use the same typed outcome policy: ready results receive
completion feedback, queued rebuilds receive waiting feedback, and failures
keep rebuild's explanation instead of being overwritten by an Undo/Redo label.
The helper explicitly refreshes the UI even when rebuilding fails. Qualify
both history directions during a worker drain and after evaluation refusal.
