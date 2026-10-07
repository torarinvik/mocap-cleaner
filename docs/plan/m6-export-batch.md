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

The batch preflight policy now defines exact admission from captured read-only
validation facts, with typed reasons for source/animation availability, paths
outside build, source collisions, duplicate destinations, occupied GLB/report
paths and unsupported recipe/rig compatibility. Eleven laws and a fresh
diagnostic object (`build/batch-preflight-compile.IM8D19/laws.o`) cover source
compilation. Native validators, queue wiring, review UI and independent proof
replay remain required; supplied booleans alone do not verify filesystem facts.
`export_batch_preflight_copy` supplies labels and correction guidance for every
outcome and compiles to `build/batch-preflight-copy.iTT5gC/copy.o` on the fresh
diagnostic compiler. This copy still needs queue UI wiring and native review.
`export_batch_queue_copy` distinguishes processing, staged output, required
review and final publication, with drain-cancellation and recovery guidance.
Its fresh diagnostic object is `build/batch-queue-copy.dpWquy/copy.o`; native
queue wiring must establish the lifecycle facts before presenting these labels.
Compilation does not qualify publication, review binding or the UI workflow.
The bounded in-memory queue now implements draining cancellation, individual
retry and explicit resume, with item-validity and lifecycle laws. Current
evidence and remaining work are recorded in
[batch queue compilation](../acceptance/batch-queue-compile-2026-10-06.md).

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
      An empty queue has an explicit empty state with an Add inputs action;
      it must not produce a successful production manifest. Preserve approval
      of the exact staged result through publication without requiring a second
      review. After cancellation drains active workers, provide an explicit
      resume/retry action that revalidates only selected failed/cancelled inputs
      and retains completed outputs. Prove running-item counts agree with the
      worker count at every queue transition.
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

The batch review binding now has a durable per-item journal/store path and a
reopen classifier that checks source identity, snapshots, staged/final/report
bytes and recorded publication stages. Interrupted workers become Recoverable;
serialized approval and success flags do not restore terminal state. Warning
warning facts are derived independently from matching JSON and text report
snapshots, and recovered warnings require a fresh identity and attempt-bound
acknowledgement. The durable constructor is not yet wired into the Studio UI,
and native filesystem durability/race behavior remains unqualified.
Compile-only evidence and exact limits are recorded in
[batch review binding](../acceptance/batch-review-binding-2026-10-07.md).

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

### Prepared-export panel: remaining integration and qualification

The saved implementation includes shared typed sheet controls,
bounded selection/paging/focus state, owned overview snapshots, captured warning
report paging, exact-attempt acknowledgement, and publication/cancel/resume
controller routes. Report pages use stable cached line views; closing releases
payloads and invalidates approval context. Overview refresh does not copy report
payloads, and per-frame admission does not parse or copy full reports. The bound
queue independently checks durable source/journal/attempt facts under its lock.
Receipt copy distinguishes durability uncertainty, partial reports and residue.

Compile-only evidence exists for the pure panel/state/report policies and their
laws. The closed-report refusal law most recently emitted a fresh 71,904-byte O0
object with law and admission symbols retained. Independent replay still has
return-binding/call-summary gaps. Neither standalone rendering nor this evidence
qualifies the integrated application or native workflow.

- [ ] Qualify the composed `app_export_batch_ui.elisa` routes in the current
      application. Report-first keyboard/pointer dispatch and sheet-then-report
      drawing are wired, with guards for background scroll/text/file-drop/native
      toolbar actions and stale pointer gestures. Verify opening/closing, focus
      restoration and disabled-action refusal end to end. Qualify the composed
      Export queue entry for empty, populated and recovery states, including its
      availability and focus behavior after enqueue and return from review.
- [ ] Complete and qualify batch native accessibility. Report publisher widgets
      and controller event routing are now composed; report lines use individual
      nodes backed by the page cache. Sheet row/action publisher widgets and
      event routes are now composed, with retained row status views and cleanup
      on close. Qualify stable node IDs, parent/sibling metadata, focus, page
      status and announcements in the integrated app and native window.
      Native actions must use the same admission and controller routes as pointer
      and keyboard actions; stale UI observations cannot authorize writes.
      Qualify the shared UI capacity repair (`elisa-ui` commit `be0aa195`):
      semantic IDs remain bounded to 0–319, while widget actions accept only
      0–255. Exercise widget sentinel 256, semantic-only IDs 256–319, sentinel
      320 and invalid IDs; none may dispatch a widget action. Pure policy/law
      objects compiled, but native action routing remains unqualified. Check
      allocation exhaustion preserves the queue, disables unavailable native
      actions and leaves keyboard/pointer routes usable. Derive capacities from
      the shared constant module rather than duplicating numeric limits.
- [ ] Qualify the new Queue reviewed result entry from export review, including
      native accessibility and warning admission. Add recovery inventory/reopen
      and selected failed/cancelled retry routes. Establish native preflight facts and immutable
      source/recipe/result bindings before exposing each action.
- [ ] Implement the full multi-take input/evaluation/worker pipeline, compatible
      recipe selection, progress and worker limits. Prepared captures and Resume
      queue alone do not satisfy production launch or the batch workflow.
- [ ] Move synchronous publication, cancellation, resume and acknowledgement IO
      off the UI path with owned requests, explicit busy state, cancellation/drain
      semantics and stale-result rejection. Qualify responsiveness and cleanup.
- [ ] Qualify the composed selected-item destination binding and inspector.
      The saved source includes the read-only getter, owned four-path capture,
      shared entry admission, retained controller, visible Inspect locations
      action, fourteen-control sheet navigation, modal dispatch and native
      accessibility routes. Qualify invalid queue/selection/path refusals and
      exact source, GLB, JSON and text paths end to end. Independent replay must
      establish exact-copy and stale-context laws. Keep queue identities and
      review authority private; inspect all three destinations after partial
      publication or uncertain durability. A compiled pure policy does not
      qualify the complete inspector or its native behavior.
- [ ] Qualify the retained destination inspector as the foremost modal:
      capture the selected item's four owned paths once, retain the selection,
      queue revision and attempt, and reject stale item context before showing
      another item's locations. Inspection grants no publication or approval
      authority. Route pointer, keyboard and native actions through the same
      typed controls. Escape and Done restore the invoking sheet control's focus;
      close the inspector when its sheet closes or its bound item disappears.
      Clear borrowed views before replacing or releasing their owned paths.
      Show source, GLB, JSON report and text report as named choices; distinguish
      selected location and page position visibly and through accessibility.
      Paginate complete valid UTF-8 paths without splitting scalars, dropping
      bytes or silently clipping. Qualify exact reconstruction across pages for
      maximum-length paths, multibyte boundaries and singleton pages. Preview
      ellipses must never be presented as complete paths. Qualify node IDs
      100–113 against the full native tree, text capacities and widget exhaustion;
      source-level range checks alone do not establish native usability.
- [ ] Integrate `StudioExportBatchDestinationPathLineModel` through a qualified
      UI adapter shared by drawing and accessibility. Supply complete grapheme
      units and whole-substring measurements from the active text-width provider,
      the actual row width and an explicit margin. Preserve exact original byte
      offsets and node text budgets. The uncomposed model and law graph compile;
      that evidence does not qualify adapter boundaries or native rendering.
      Preserve renderer measurement validity across the text-metric API;
      clamping NaN, negative or infinite widths into finite geometry must not
      turn unavailable measurements into an asserted fit. Distinguish a valid
      zero-width glyph range from a failed measurement. Bind retained layout
      to the active font/scale generation and rebuild when that context changes.
      Qualify combining marks, joined emoji, fallback fonts and changes in scale
      or width. A cluster larger than a text node's budget needs an explicit,
      faithful inspection fallback; do not silently split, omit or normalize
      path bytes. Bound model construction and rebuild only when the captured
      path or relevant layout metrics change. Revalidate paging and focus when
      the segment count changes. Current 32-scalar chunks are UTF-8 safe, but
      that alone does not establish grapheme or rendered-width fidelity.
- [ ] Inspect glyph widths, Unicode report paging, long paths/status messages and
      minimum window size. Make every report segment readable without silent
      clipping; preserve explicit refusal for invalid or oversized reports.
- [ ] Qualify exact warning counts/bytes, refresh invalidation, changed attempt,
      already-approved capture, lock failure/uncertain release, pause/cancel and
      partial publication using current source-matched compiler and proof tools.
      Close independent proof replay gaps without weakened contracts or baselines.
- [ ] Run current integrated build and native acceptance, including report view
      lifetime, cleanup on close, accessibility traversal and durable recovery.
      Retain fresh input/product manifests; diagnostic objects are insufficient.
