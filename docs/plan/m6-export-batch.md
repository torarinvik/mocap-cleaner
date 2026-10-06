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

### Report diff input qualification still required

The CLI now errors when no baseline quality metric/status is comparable or a
compared integer metric exceeds the supported regression domain. It does not
silently accept those inputs through magnitude clamping. The domain kernel has
contracts and composed laws; current compilation and replay remain pending.

- [ ] Replace the legacy flat scanner with schema-aware JSON parsing. Reject
  malformed booleans, truncated strings, invalid escapes, duplicate identities
  and unsupported numeric representations. Preserve fractions/exponents using
  declared units and rounding rather than dropping their suffixes.
- [ ] Validate metric types and availability on both sides; Boolean values
  cannot stand in for numeric errors. Compare only compatible provenance and
  units, and report unavailable dimensions with explicit reasons.
- [ ] Qualify missing clips/metrics, unsupported magnitudes, empty baselines,
  decimal/exponent values and malformed documents before closing diff review.

Report diff now checks engine JSON tokenization and an object root before metric
extraction; failed structure/empty input produces an input error. The module
compiled with current Stage1 `4c409da6`, without a stale override. This is only
a structure admission step: legacy extraction still needs the schema, numeric,
string decoding and duplicate-identity work listed above. Engine tokenization
alone does not establish every required report validation rule.

The diff comparison now rejects Boolean values for numeric quality metrics
and mismatched baseline/candidate types, including numeric values used instead
of a Boolean `ok` status. This does not replace schema validation or availability
checks. Current object compilation is recorded separately from executable and
proof acceptance.

Report extraction now rejects duplicate clip/key pairs instead of letting the
first match hide a later value. Reusing the parser clears its output buffers;
failed duplicate admission clears extracted metrics. The module compiled on
current Stage1 `4c409da6`. This check uses the legacy extracted byte identity;
Unicode/escape-normalized identities and schema-aware nesting still need the
reader replacement above. Its pairwise scan also needs an explicit input budget
or indexed implementation before large batch-report qualification.
