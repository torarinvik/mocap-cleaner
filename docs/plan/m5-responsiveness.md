# M5: responsiveness and reliability

[Roadmap index](../../IMPLEMENTATION_PLAN.md)

## 10. M5 — Responsiveness and reliability at production scale

**Touchpoints:** `app.elisa`, `model.elisa`, studio state, existing operation
and rig caches, engine host scheduling, elisa-ui rendering limits.

- [ ] Measure end-to-end input-to-preview latency with feet enabled, contact
      edits, long clips and large rigs. Profile actual screen playback and
      GPU drawing, not just headless kernel timings.
- [ ] Move expensive load/analysis/rebuild/export work out of the UI event
      path using an engine-supported worker/job boundary. Prototype safe Elisa
      ownership first; do not share mutable clip buffers unsafely.
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
      boundaries and compare against uncached output.
- [ ] Replace or safely extend the current fixed capacities after an ownership
      prototype. Until then display capacity before an action fails, preserve
      the draft and offer recovery; never truncate edits silently.
- [ ] Bound cache/history/recovery memory; define eviction and invalidation.
      Stress repeated take swaps, undo/redo, long sessions and batch use.
- [ ] Optimize curves, issue rows and overlays for draw budget and density.
      Use explicit level of detail; selection and peak markers remain accurate.
- [ ] Record per-stage latency, memory, cache hits and stale-job rejection in
      optional developer diagnostics. Keep these details out of normal flow.

**Exit:** responsiveness targets measured on the corpus; cancellation and
stale-result scenarios pass; cached and full output agree; capacity pressure
never silently loses edits. No representation rewrite without a measured need.

