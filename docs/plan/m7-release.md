# M7: release qualification

[Roadmap index](../../IMPLEMENTATION_PLAN.md)

## 12. M7 — Professional release qualification

### Evidence and automation

- [ ] Extend focused state tests for command enablement, focus/text input,
      transactional drafts, dirty state, migration, capacities and job revisions.
- [ ] Add numerical regressions for the expanded motion corpus, including
      negative controls and per-frame contact/joint limits. Keep tolerances
      tied to documented units and fixture intent.
- [ ] Audit actual proof coverage per critical contract. Reduce unknown or
      unsupported cases by priority, record remaining limits honestly, and
      retain the existing proof-regression baseline gate.
- [ ] Add reproducible UI interaction checks for file lifecycle, stack editing,
      contacts, retime, gizmo cancellation, comparison and export. Supplement
      captures with real native-window checks for input routing and GPU paths.
      Exercise export-warning acknowledgement, disabled Export, result-dialog
      focus, Open Result, Show in Folder, missing/failed outputs and Done/Escape.
      Confirm the editable session remains separate from the published GLB;
      complete the review/result journeys with keyboard and VoiceOver.
- [ ] Capture and review visual states at supported window sizes/scales:
      first run, malformed input, busy/cancelled job, missing rig roles, dense
      timeline, long paths, export warnings/result, help and restored session.
- [ ] Exercise disk full/permission failure, interrupted write, malformed GLB,
      damaged session, changed source, rapid edits and focus loss. Verify
      source hashes and last valid committed state after each scenario.
- [ ] Run clean-build and warm developer-loop checks separately; report
      timings with hardware and contention. Performance gates must identify
      which path they measure rather than implying cached timing is cold.

### Usability and release readiness

- [ ] Run the four journeys with at least five intended users, including
      first-time and experienced animators. Record completion, time, wrong
      actions, recovery and moments of uncertainty without coaching.
- [ ] Prioritize observed failures: lost-work risks first, blocked tasks next,
      misleading cleanup next, then friction and visual polish. Repeat failed
      journeys after changes.
- [ ] Publish a quick-start based on visible controls, a contact repair guide,
      parameter explanations, supported input/rig limits and troubleshooting.
      Update `docs/studio.md`, `docs/studio-ux.md` and `docs/foot-workflow.md`
      to describe verified behavior.
- [ ] Prepare a runnable app package with icon/name/version, dependency
      provenance, licenses and reproducible build instructions. Verify launch
      from Finder and file opening outside a development shell; assess signing
      and distribution requirements for the chosen release route.
- [ ] Maintain a release checklist: P0 acceptance evidence, no critical
      data-loss bugs, documented quality limits, visual review, numerical/proof
      gates, session compatibility, export parity and usability target.

**Exit:** all P0 gates have recorded evidence. Unresolved lower-priority gaps
are explicit release notes; no build-only check closes a user journey.

