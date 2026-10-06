# Mocap Cleaner — Product and Implementation Plan

Updated 2026-10-06. This is the remaining-work roadmap. Completed work has
been removed; its implementation history remains in Git. Existing kernels,
CLI tools, studio controls, caches and reports are the starting point for
these milestones, not tasks to rebuild.

## 1. Product outcome and boundaries

Make an animator confident taking an unfamiliar capture from import to a
reviewed, exportable result without reading source code or memorising keys.
A beginner should understand the next useful action. An expert should be
able to inspect causes, tune corrections precisely, and reproduce a result.
Cleanup must preserve the performance's intent, timing and contacts.

The product remains a desktop mocap cleanup tool. Full rig authoring,
animation from scratch, rendering, a general scene editor and a cloud service
are outside this roadmap. Additional file formats and platforms require a
separate demonstrated need; GLB and the current macOS studio are the first
release target. Rig role mapping is not a promise of general retargeting.

### Mandatory file size and module hygiene

Every maintained repository file must remain at most 600 lines, including
source, proofs, tests, scripts, configuration and documentation. This is an
ongoing acceptance requirement for every milestone and every new file.
Split growing files into cohesive modules before exceeding the limit. Use
nested modules when appropriate, keep implementation helpers private and
expose only necessary public APIs. Preserve behavior, includes, tooling and
proof coverage. Recount file lengths before committing each small change.
Generated `build/` artifacts and sibling repositories are outside this rule.
Run `python3 scripts/check_file_lengths.py` before committing; the same static
check runs before compilation in `scripts/check.sh`. It inspects tracked and
non-ignored untracked UTF-8 text files, including documentation and proofs.

### Constants and finite choice representation

Prefer a `const enum` when constants denote a closed set of alternatives.
Prefer an algebraic data type when cases carry distinct data or should exclude
invalid combinations. Otherwise group multiple related constants in actual
Elisa `const module` declarations with purpose-specific names. Apply this to
existing and new modules; preserve public/private visibility and update all
callers, contracts and proof references. Preserve required serialized/native
values through explicit, validated boundary conversions. Do not leave a weaker
integer representation solely because a constant group already exists.

### Architecture and safety requirements

- Product implementation is Elisa; UI components come from elisa-ui.
- Viewport, picking, pose evaluation, GLB preservation, animation math and
  native host facilities belong in `../elisa-engine-mocap`, branch
  `mocap-track`. Reusable widget and accessibility facilities belong in
  elisa-ui; keep cleanup policies in this repository.
- Source takes are immutable. Generated clips, reports, captures, recovery
  snapshots and other derived artifacts go under `build/`. Export and save
  dialogs must enforce this rule, including canonical-path and symlink
  checks against source takes. Do not silently overwrite another result.
- Every new kernel ships with contracts and `proof/` laws in the same small
  change. Aim for roughly as much proof code as business logic. Use integer
  fixed point for proof-critical logic: weights in permille, lengths in
  0.1 mm; document conversions at floating-point engine boundaries.
- Prover fixes go in `../elisa-proof-mocap`, branch
  `mocap-cleaner-proofs`, and are recorded in `docs/proof-gaps.md`.
- Preview, exported output and CLI evaluation share the same operation
  semantics. New UI controls expose existing capabilities before adding
  competing implementations.
- Cancellation, failed loads and failed saves preserve the last valid
  document. An action is complete only when its result has been committed
  successfully; status text must not claim an unfinished write succeeded.

### Evidence to establish before implementation

The previous roadmap includes build-only and headless-only studio checks.
Treat those as evidence of compilation or kernel behavior, not demonstrated
interaction quality. The current studio and capacity inventories are useful
code-linked references, but they do not establish on-screen usability.
Continue to validate remaining interactions in a running window before
calling them complete.

Current constraints requiring explicit decisions include the synchronous
studio rebuild, fixed operation/correction/contact-edit capacities, the
1024-command UI drawing budget, approximate heel geometry, floor-based hand
contact detection, head-pin reach limitations, and the foot-lock versus
knee-pop trade-off in `docs/foot-workflow.md`. Existing proof reports include
unknown and unsupported cases; do not describe the product as fully proved.

## 2. Success measures and working method

These are proposed release targets, to be measured on named hardware and a
versioned fixture corpus. Record deviations and revise targets with evidence,
not by weakening a gate after a regression.

| Outcome | Target and measurement |
|---|---|
| First useful result | At least 4 of 5 first-time evaluators import a supplied take, preview a suggested cleanup, compare and export within 10 minutes, without verbal coaching. |
| Discoverability | Every primary task has a visible labelled control/menu path; keyboard shortcuts are optional accelerators. |
| Trust | Every accepted fix has a scope, undo entry and change summary; source hashes stay unchanged throughout review/export/recovery. |
| Cleanup quality | Each reference case passes its declared per-frame and aggregate quality gates, plus visual review; intentional fast movement remains recognizable. |
| Responsiveness | On the agreed reference take, target 60 Hz playback and drag preview, p95 interaction processing below 50 ms; display a job state for work exceeding 100 ms. Measure p95/p99 frame times and dropped frames. |
| Work preservation | Dirty-close, cancelled file panels, failed writes, interrupted computation, source mismatch and recovery fixtures lose no committed edits. |
| Recoverable cleanup | An animator can disable/remove one correction, undo a cleanup, restore the original result, and identify generated files safe to remove; no source take is selected for deletion. |
| Precision | Frame ranges, units, bone scopes, contact anchors and export animation selection are visible and survive session round-trip. |
| Accessibility | Core import–review–correct–export flow works using keyboard alone, without color-only signals, and with supported native accessibility semantics. |

### Delivery rules

- Deliver small vertical slices: usable control, state transition, evaluation,
  feedback, undo/session handling and relevant evidence together.
- Commit each small coherent improvement. Do not accumulate unrelated UI,
  algorithm and dependency work into one large commit.
- Each task below is open. Close it only when its stated acceptance evidence
  exists. A build alone cannot close a visual or interaction task.
- Update user docs when behavior changes; move completed tasks out of this
  active plan in subsequent planning updates rather than retaining a growing
  checked-off history.
- Keep screenshot and benchmark artifacts in `build/`; record reproducible
  commands, fixture versions, hardware and conclusions in documentation.

## 3. The user journeys to design first

### A. First-time guided cleanup

Open or drop a GLB → choose its animation → confirm scale, floor and rig
roles → see a short diagnosis → preview a conservative recommendation →
compare at the affected moments → accept → export a named result and report.

The user must be able to skip recommendations and inspect the source. No
boxing-specific preset should be silently treated as appropriate for every
capture. Missing rig information must lead to an explanation and setup
controls, not a mysterious failed fix.

### B. Precise repair of one problem

Select an issue in a ranked list → jump to its frame and affected joint →
inspect source/result curves and contact context → choose a local fix →
adjust scope, fades and strength → compare adjacent motion → accept or undo.

Selecting an issue must not add an operation. Changing a parameter should
preview its effect; acceptance should produce one meaningful history entry.

### C. Contact-heavy motion

Confirm floor → inspect proposed plants → correct contact intervals → choose
lock/pivot and anchor behavior → review reach and knee/elbow warnings →
compare slide, penetration and joint motion → accept the compromise.

A reduction in summed slide is insufficient if a local transition becomes
worse. The interface must expose both improvements and remaining errors.

### D. Professional repeat work

Restore a session → resolve changed/missing source references → reuse a
rig profile and cleanup recipe → process selected takes → review failures
and regressions → export only approved results with reproducible reports.

Batch progress and individual failures must be understandable without
reading terminal output. A recipe reused on a different rig must validate
its roles, units and scopes.

## 4. Milestone order and dependency gates

| Milestone | Priority | Depends on | Deliverable |
|---|---|---|---|
| M0 — Evidence and interaction specification | P0 | Existing studio | Honest baseline, fixture corpus, agreed screen flows and quality thresholds. |
| M1 — Safe, discoverable workspace | P0 | M0; shared identity schemas with M2 | Pointer/keyboard task paths, document lifecycle, responsive layout and accessible controls. |
| M2 — Import, rig and diagnosis | P0 | M0; co-develop identity with M1 shell | Reliable setup and a navigable explanation of capture problems. |
| M3 — Guided cleanup and review | P0 | M2 | Conservative recommendations, meaningful comparison and complete operation inspection. |
| M4 — Contact and local repair quality | P0 | M2–M3 | Precise contact editing, existing advanced tools exposed, local regression protection. |
| M5 — Responsive long-session editing | P0 | M1 state model; benchmark corpus | Safe background evaluation, scalable state and reliable recovery. Prototype ownership before expensive M3 integration. |
| M6 — Export and production workflow | P0 single export; P1 batch | M3–M5 | Validated export, reusable recipes, studio batch review and reproducibility. |
| M7 — Release qualification | P0 | All P0 gates | On-screen, numerical, proof, reliability and usability release evidence. |
| M8 — Advanced cleanup research | P2 | Quality corpus and measured failures | Evidence-backed extensions, separately gated before becoming defaults. |

P0 blocks a professional single-take release. P1 follows that flow and may
ship later. P2 is exploratory and must not delay a safe useful release.

## 5. M0 — Establish the actual baseline

**Touchpoints:** `src/studio/app/`, `docs/studio*.md`,
`docs/foot-workflow.md`, `docs/proof-gaps.md`, `test/`, `proof/`.

- [ ] Complete a valid-take running-window exercise of file panels/drop,
      mesh/x-ray, every view, selection, curves, playback, contacts, gizmos,
      retime, undo, sessions and export. Record the exact build, outcomes and
      screenshots in `docs/studio-capability-matrix.md`. Review contact
      nudges and finding filters on screen, including focus, hit targets,
      issue-row selection, ignore/restore and undo using fixtures that contain
      real findings. Verify Escape on every layer and review replacement,
      legacy-session and export dialogs for readability, focus and dismissal
      at the minimum window size. Verify Duplicate edge-state feedback (no
      selection and full stack), native `Cmd-D`/`Cmd-O` routing, text-entry
      ownership and VoiceOver activation through the app's native input path.
- [ ] Review the legacy-session warning on screen: Cancel and Escape preserve
      a dirty document; Load leads to the separate Save/Discard/Cancel prompt;
      mouse, arrows, Enter, L and Esc have clear visible focus and outcomes.
      Check the warning at the minimum supported window size and record a
      screenshot of both it and the following dirty-document prompt.
- [ ] Complete running-window review of capacity behavior. Record limit
      feedback, atomicity, memory and accessibility/draw overflow; close the
      still-unverified capacity cases in `docs/studio-capacities.md`. Visually
      check contact fields and keyboard nudges at the supported frame boundary
      and retain the existing larger-domain proof evidence; resolve any newly
      observed gaps without weakening reviewed baselines.
- [ ] Establish benchmark takes: short boxing, walking/running, idle jitter,
      turns, jumps/landings, planted hands, unusual proportions, noisy input,
      long clips and multi-animation GLBs. Use licensed or synthetic fixtures;
      keep originals immutable and document expected motion intent.
- [ ] Include negative controls: deliberate punches, rapid turns, intentional
      foot slides, toe rolls and fast elbow motion that should remain.
- [ ] Baseline worst-frame, percentile and aggregate slide, floor error,
      knee/elbow angular jumps, endpoint drift, boundary discontinuity,
      runtime and memory. State units and how contacts were labelled.
- [ ] Specify low-fidelity layouts and interaction sequences for all four
      journeys, including empty, loading, error, selection and busy states.
      Review terminology with an animator before polishing visuals.

The CLI-to-studio source inventory is recorded in
`docs/studio-capability-matrix.md`; that inventory identifies existing
capabilities and UI integration gaps without duplicating kernels.
Existing motion-quality evidence and missing corpus categories are inventoried
in `docs/quality-corpus-status.md`; that inventory is not a release benchmark.

**Exit:** a capability/evidence matrix, reproducible corpus and benchmarks,
and screen flows with explicit acceptance criteria. No feature is declared
visually verified solely from offscreen rendering.

