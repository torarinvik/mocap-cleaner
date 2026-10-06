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
- [ ] Keep playback/time mapping deterministic when results arrive; preserve
      playhead intent and pause/resume semantics during retime rebuilds.
- [ ] Extend narrow evaluation only where dependencies permit. Keep full
      contact-dependent rebuilds when required; measure before changing cache
      boundaries and compare against uncached output. Declare which fields must
      match exactly and which use a justified floating-point tolerance; cover
      operations, corrections, contacts, retime and cache boundaries.
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
- [ ] Optimize curves, issue rows and overlays for draw budget and density.
      Use explicit level of detail; selection and peak markers remain accurate.
- [ ] Record per-stage latency, memory, cache hits and stale-job rejection in
      optional developer diagnostics. Keep these details out of normal flow.

**Exit:** responsiveness targets measured on the corpus; cancellation and
stale-result scenarios pass; cached and full output agree; capacity pressure
never silently loses edits. No representation rewrite without a measured need.

