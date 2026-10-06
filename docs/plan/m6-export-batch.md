# M6: export, recipes and batch production

[Roadmap index](../../IMPLEMENTATION_PLAN.md)

## 11. M6 — Export, recipes and batch production

### 11.1 Reviewed export (P0)

- [ ] Define export/report publication as one revision-bound transaction with
      durable, inspectable stage outcomes. Cover crash/failure before staging,
      after GLB publication and between JSON/text report publication. A valid
      published GLB with failed reports is a partial result, not complete
      success. Offer report completion from the exact immutable snapshot;
      retries never overwrite an approved output or silently reevaluate it.
      Clean only owned unpublished staging files; preserve published artifacts
      and unknown recovery evidence. Qualify flush/close/directory durability
      failures separately from reload/byte integrity.
Do not offer root extraction/in-place conversion or key reduction until that
semantics has its own implementation, review fields and quality validation.
- [ ] Add semantic round-trip fixtures for animation selection, evaluated
      poses, duration, contact/key timing and untouched nodes/skins/meshes on
      top of the publisher's serialization byte-count check and reload/document-equivalence
      validation. Compare
      evaluated output against the reviewed revision. Surface a clear
      distinction between file integrity and motion-quality review.
- [ ] Extend the existing schema-v2 `.report.json` and `.report.txt` baseline
      (identifiers, timing estimates, settings, assumptions, metrics and
      unavailable reasons) with missing provenance from one immutable export snapshot: rig configuration,
      tool/dependency versions, detector thresholds and per-frame retime
      mapping. Keep explicit unavailable reasons until the publisher can
      supply those exact values. Add cryptographic source/output hashes only
      when the exact source and validated output bytes are available. Current
      `studio-residue-v1` identifiers are non-cryptographic. Freeze animation,
      stack/result revisions, settings and metrics before publication; reports
      must not read later live state. Bind each sidecar to that export identity
      so an old or partially replaced report cannot appear current.

### 11.2 Studio batch and repeatability (P1)

- [ ] Wrap the existing batch/parallel/report capabilities in a queue UI:
      input list, animation selection, compatible recipe, output naming,
      collision policy, worker limit, progress, cancel and retry failures. Define
      whether cancellation drains or terminates running workers; stop new
      launches, identify interrupted outputs and retain valid completed ones.
      Retry only failed/cancelled inputs with create-only publication.
- [ ] Show per-take outcomes: passed, warning, failed, cancelled; aggregate
      completion must not conceal failed takes. Mark the manifest incomplete
      when any input or required report is unfinished. Allow source/result review
      before approving warning outputs.
- [ ] Add dry-run validation of paths, rig compatibility and expected outputs.
      Do not apply one rig's absolute bone indices across unrelated inputs.
- [ ] Expose the existing report diff as a review view with thresholds,
      baseline selection and links to regressed clips/frames when available.
- [ ] Save queue/recipe configuration and deterministic manifest order.
      Retrying failed items does not rerun or overwrite approved items silently.
- [ ] Provide copyable CLI reproduction for an approved studio recipe,
      including safe path quoting and matching evaluation semantics.

**Exit:** exported poses match the reviewed revision; failures leave no
misleading partial deliverable; source files remain unchanged. Batch and
single-take output agree for identical settings.

### Report diff remaining implementation and qualification

Implemented foundations: schema-aware root/clip extraction, JSON string and
UTF-8 decoding, duplicate identity rejection, exact coefficient/exponent
parsing, common-scale comparison, sorted identity indexes, and separate HTML
presentation. Current Stage1 `f292cbe0` compiles the reader and CLI. These
foundations still need behavioral, proof and rendered qualification; compilation
does not close the review workflow. Historical proof/check evidence belongs in
`docs/acceptance/` and `docs/proof-gaps/`, rather than completed plan items.

- [ ] **Metric compatibility:** declare each supported metric's units, direction,
  numeric type and availability semantics. Compare matching provenance/schema
  versions, detector thresholds and units. Reject incompatible dimensions with
  a specific explanation; do not infer compatibility from equal key names.
- [ ] **Exact numeric qualification:** verify signed values, equivalent decimal
  spellings, positive/negative exponents, zero with large exponents, range limits,
  coefficient overflow and scale overflow. Preserve exact values in console and
  HTML. Declare the supported scale/domain and explain unavailable comparisons.
  Verify relative tolerance and absolute floor together at exact boundaries.
- [ ] **Reader qualification:** verify malformed booleans, truncated/escaped
  strings, invalid UTF-8, surrogate pairs, trailing document data, duplicate
  root/clip/metric identities, reserved `total`, empty names, non-object clip
  entries and metadata containing misleading metric keys. Verify decoding
  equality for raw versus escaped Unicode without applying undocumented Unicode
  normalization. Errors must prevent a passing qualification verdict.
- [ ] **Index qualification:** establish stable sort order, row permutation,
  adjacent duplicate detection and binary lookup equivalence. Prove all pool
  spans and index accesses valid, sort progress and search-window shrinkage.
  Qualify empty, singleton, odd-sized and reverse-ordered reports. Measure large
  reports within the 16 MiB input budget, including memory and cancellation
  behavior. Retain source row identities for diagnostics.
- [ ] **Proof closure:** close arithmetic bounds for decimal append, scale and
  floor conversion; close parser invariants and executable ADT summaries; close
  midpoint and index traversal bounds. Replay every accepted certificate and
  investigate reported disproved parser laws. Retain exact contracts and
  independently validate prover repairs; never weaken baselines for acceptance.
- [ ] **Review UI:** expose baseline selection, tolerance/floor controls, units,
  compatibility diagnostics and unavailable reasons. Link to regressed clips
  and frames only when exact identities exist. Preserve review context and offer
  a clear retry path after correcting inputs.
- [ ] **HTML review:** verify leading verdict, comparison parameters, counts,
  empty/error states, escaped names and faithful decimal formatting in a rendered
  browser. Qualify narrow-window scrolling, semantic headers, keyboard use and
  screen-reader interpretation. A failed save must produce an actionable error.
- [ ] **Snapshot acceptance:** rerun the authorized full check with clean current
  dependency manifests and a stable product snapshot. Account for every failed
  test, unknown obligation, replay gap and missing baseline. Record exact revisions
  and scope; earlier successful workflows do not qualify later source changes.

**Exit:** compatible inputs receive exact, reproducible verdicts; malformed or
unsupported inputs receive explicit unavailable/error states; the review view
and exported HTML remain usable and truthful; complete proof replay and the
full product check qualify the same snapshot.

Current metadata implementation: CLI reports declare `mocap-cleaner-report-v1`,
known comparison metric units, and the spike threshold from the actual preset
used for evaluation. The reader rejects declared schema/unit mismatches and
malformed declarations; unknown/legacy metadata is explicitly unqualified in
console and HTML. Unit metadata is capped at 128 declarations by a contracted
budget. Exact unit conversion, full detector-setting/provenance compatibility,
qualification of the strict unknown-metadata gate, metadata traversal proof replay
and native edge-case qualification remain required. The compatibility policy
has source contracts and schema/unit laws; current Stage1 compilation succeeds.

Metric dimensions now have a typed policy: supported count, frame-count and
distance metric names require matching declared dimensions; equal declarations
with a known wrong dimension are rejected. Unknown metric names remain
unqualified. Current compiler builds the reader and laws. The default prover
reports source 4/4 and laws 9/12, with three laws still unknown; independent
replay and behavior qualification remain open.

Unknown schema, unit or required detector declarations now force an unavailable
exit verdict; numeric rows remain available for inspection. The metadata
admission policy reports 3/3 and its laws 11/11 on the default prover; reader
and updated existing fixtures compile. Independent replay and behavioral
qualification remain required. These checks do not supply missing immutable
provenance or the other detector settings still listed above.

Unit-object and member lookup now use explicit `Missing`, `Invalid` and
`Present(index)` algebraic states rather than negative index sentinels. Reader
and declaration-state laws compile on the current compiler. State-law proof
checking is ongoing; token traversal bounds and malformed/duplicate declaration
behavior still require full qualification.

Lower-is-better admission now uses supported metric definitions rather than
trusting `_after` suffixes. Unsupported quality names are unavailable, and
quality values must be nonnegative; counts/frame-counts must be whole numbers.
The typed policy reports 14/14, its expanded laws 25/32. Reader and laws compile;
seven law obligations, replay and behavioral qualification remain open.

HTML tables now show expected units and Boolean status words, with metric
direction and exact decimal notation explained. Compilation succeeds. A fresh
pre-presentation-change artifact was generated successfully; local-file browser
opening was blocked by protocol security policy, so rendered layout, keyboard
and screen-reader qualification remain open (see the HTML review evidence).
