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
      tool/dependency versions and detector thresholds. Qualify the captured
      per-frame retime map against the evaluated revision in both formats:
      exact integer units, frame count, endpoints, order, singleton clips and
      retimed clips. Qualify invalid-map and complete-report budget failures;
      explain the failure before GLB publication without truncating the map.
      Keep explicit unavailable reasons until the publisher can
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

Qualify the existing reader, numeric comparison, indexing and presentation
against the requirements below. Historical compiler, proof and check evidence
belongs in `docs/acceptance/` and `docs/proof-gaps/`; a compile result does not
close the review workflow. Use current dependency manifests for acceptance.

- [ ] **Metric compatibility:** qualify supported metric units, direction and
  numeric type; supply missing sample/availability semantics. Compare matching provenance/schema
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

### Remaining durable export recovery work

Existing integration freezes JSON/text bytes before GLB publication, distinguishes
individual sidecar outcomes, attempts parent-directory sync and presents partial
or uncertain results in the result dialog and accessibility text. A create-only
sidecar publisher exists and compiles; native collision/cleanup behavior and
recovery integration remain unqualified. These foundations still need recovery integration and
qualification; current evidence is in [integration observations](../acceptance/m6-integration-observations-2026-10-06.md)
and [publication proof gaps](../proof-gaps/export-publication-outcomes.md).

Retry admission now has a contracted policy and complete proof/replay (8/8
source, 22/22 laws). Integration must establish all six input facts; the policy
does not supply durable records or exact-byte verification. Evidence is in
[recovery admission](../acceptance/export-recovery-policy-2026-10-06.md).

- [ ] **Owned recovery record:** give each export an immutable transaction ID
  and keep the GLB identity, exact frozen report bytes, source/animation/stack
  revisions, final paths and stage outcomes together. Preserve multiple pending
  records without silently replacing an earlier export. Store derived recovery
  artifacts under the selected workspace's `build/`; block publication if the
  required recovery record cannot be established. Bound memory and disk usage,
  disclose capacity exhaustion and retain recoverable evidence.
- [ ] **Exact result binding:** retain a byte-for-byte output snapshot or a
  qualified cryptographic digest of the actual staged bytes. Before completing
  reports, verify the published GLB against that identity. Refuse missing,
  replaced, modified or ambiguous outputs. A non-cryptographic residue is not
  sufficient to authorize snapshot-bound recovery. Never reevaluate the live
  stack or later source take to reconstruct an old report.
- [ ] **Durable journal:** persist prepared, GLB-published, JSON-published and
  text-published stages using a versioned, bounded, validated record. Distinguish
  observed publication from file/directory durability. Recover conservative
  states after crashes between every pair of writes. A journal failure after
  publication leaves an inspectable partial result; it must not cause rollback
  messaging or deletion of published files. Reject corrupt/unknown records
  without treating them as owned cleanup candidates.
- [ ] **Missing-sidecar completion:** retry only absent current reports using
  the frozen bytes and atomic create-only publication. Never overwrite an
  existing sidecar or the GLB. When a sidecar already exists, verify exact bytes
  and binding before recognizing completion; conflicting or stale content
  requires an explicit resolution flow. Preserve successful stages after another
  failure, including failure to update the journal or Storage tracking.
- [ ] **Recovery UI:** expose pending exports, exact stage status, destination,
  unavailable reasons, retry eligibility and copyable diagnostics. Add keyboard
  and accessibility support, focus restoration and per-item retry feedback.
  Separate motion-quality review from file publication and durability. Keep
  completed GLBs usable while reports remain pending; do not lose recovery
  ownership merely because the result dialog closes or another take loads.
- [ ] **Cleanup ownership:** record private staging paths and account for failed
  unlink after successful hard-link publication. Delete only demonstrably owned
  unpublished staging/recovery files after explicit resolution. Preserve final
  outputs, current sidecars and unknown records. Show estimated reclaimed space,
  failures and remaining recovery evidence. Qualify cleanup after crash,
  cancellation, root change and partially completed recovery.
- [ ] **Native qualification:** cover failed create/write/flush/file-sync/close,
  reload mismatch, rename/link failure, destination races, parent sync failure,
  journal failure and staging unlink failure. Establish that source takes and
  approved outputs remain unchanged. Compile success and Boolean IO wrappers
  do not prove crash durability or atomic recovery semantics.
