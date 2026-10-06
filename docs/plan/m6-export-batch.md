# M6: export, recipes and batch production

[Roadmap index](../../IMPLEMENTATION_PLAN.md)

## 11. M6 — Export, recipes and batch production

### 11.1 Reviewed export (P0)

Do not offer root extraction/in-place conversion or key reduction until that
semantics has its own implementation, review fields and quality validation.
- [ ] Add semantic round-trip fixtures for animation selection, evaluated
      poses, duration, contact/key timing and untouched nodes/skins/meshes on
      top of the publisher's current reload and byte-equality check. Compare
      evaluated output against the reviewed revision. Surface a clear
      distinction between file integrity and motion-quality review.
- [ ] Complete the remaining schema-v2 `.report.json` and `.report.txt`
      provenance from one immutable export snapshot: rig configuration,
      tool/dependency versions, detector thresholds and per-frame retime
      mapping. Keep explicit unavailable reasons until the publisher can
      supply those exact values. Add cryptographic source/output hashes only
      when the exact source and validated output bytes are available.

### 11.2 Studio batch and repeatability (P1)

- [ ] Wrap the existing batch/parallel/report capabilities in a queue UI:
      input list, animation selection, compatible recipe, output naming,
      collision policy, worker limit, progress, cancel and retry failures.
- [ ] Show per-take outcomes: passed, warning, failed, cancelled; aggregate
      completion must not conceal failed takes. Allow source/result review
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

