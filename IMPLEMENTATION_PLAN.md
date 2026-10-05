# Mocap Cleaner — Product and Implementation Plan

Updated 2026-10-05. This is the remaining-work roadmap. Completed work has
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
interaction quality. `docs/studio.md` also contains outdated limits and
shortcut descriptions. Audit actual code and a running window before using
those descriptions as specifications.

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
| M1 — Safe, discoverable workspace | P0 | M0 | Pointer/keyboard task paths, document lifecycle, responsive layout and accessible controls. |
| M2 — Import, rig and diagnosis | P0 | M1 | Reliable setup and a navigable explanation of capture problems. |
| M3 — Guided cleanup and review | P0 | M2 | Conservative recommendations, meaningful comparison and complete operation inspection. |
| M4 — Contact and local repair quality | P0 | M2–M3 | Precise contact editing, existing advanced tools exposed, local regression protection. |
| M5 — Responsive long-session editing | P0 | M1 state model; benchmark corpus | Safe background evaluation, scalable state and reliable recovery. Start infrastructure before M3 if measurements demand it. |
| M6 — Export and production workflow | P0 single export; P1 batch | M3–M5 | Validated export, reusable recipes, studio batch review and reproducibility. |
| M7 — Release qualification | P0 | All P0 gates | On-screen, numerical, proof, reliability and usability release evidence. |
| M8 — Advanced cleanup research | P2 | Quality corpus and measured failures | Evidence-backed extensions, separately gated before becoming defaults. |

P0 blocks a professional single-take release. P1 follows that flow and may
ship later. P2 is exploratory and must not delay a safe useful release.

## 5. M0 — Establish the actual baseline

**Touchpoints:** `src/studio/app/`, `docs/studio*.md`,
`docs/foot-workflow.md`, `docs/proof-gaps.md`, `test/`, `proof/`.

- [ ] Exercise the running studio: file panels/drop, mesh/x-ray, all views,
      selection, curves, playback, contacts, gizmos, retime, help, undo,
      sessions and export. Record pass/fail, exact build and screenshots.
- [ ] Review the legacy-session warning on screen: Cancel and Escape preserve
      a dirty document; Load leads to the separate Save/Discard/Cancel prompt;
      mouse, arrows, Enter, L and Esc have clear visible focus and outcomes.
      Check the warning at the minimum supported window size and record a
      screenshot of both it and the following dirty-document prompt.
- [ ] Reconcile documented behavior with code. Remove obsolete claims about
      absent mesh rendering, export paths and plain-only undo shortcuts.
      Label remaining headless-only and unverified behavior explicitly.
- [ ] Inventory each CLI capability against studio access, parameter editing,
      history, session persistence and metrics. Identify integration gaps
      rather than planning to reimplement existing kernels.
- [ ] Record current maximum frames, joints, animations, operations,
      corrections, contact edits, retime bands, history and draw commands.
      Show how each limit behaves at, below and above capacity.
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

**Exit:** a capability/evidence matrix, reproducible corpus and benchmarks,
and screen flows with explicit acceptance criteria. No feature is declared
visually verified solely from offscreen rendering.

## 6. M1 — A workspace that explains itself and protects work

### 6.1 Information architecture and layout

- [ ] Organize the workspace into document header, labelled primary actions,
      viewport, issue/rig browser, context inspector, timeline and status.
      Keep the currently selected clip, source and dirty state visible.
- [ ] Provide sensible initial panel sizes; add resizing, scrolling and
      collapse behavior. Prioritize the viewport and timeline at small
      sizes; avoid controls falling outside the window.
- [ ] Add single-view and multi-view layouts with a visible active-view
      indicator. Persist layout/camera preferences separately from cleanup
      parameters. Provide Reset workspace.
- [ ] Create shared spacing, type, color, focus, disabled, selected, warning
      and error tokens. Use the existing icon family consistently and retain
      readable labels for primary actions.
- [ ] Check Retina scaling, long paths, large numbers, dense rigs and resized
      windows. Budget draw commands explicitly; virtualize or clip long
      lists instead of dropping arbitrary controls.

### 6.2 Commands, focus and accessibility

- [ ] Complete visible Edit/View/Cleanup/Help command paths and context menus
      where appropriate. Centralize labels, shortcuts, enablement and dispatch
      so menus, toolbar controls, contextual actions and shortcuts stay in
      sync. Add a searchable command palette (P1) after the primary paths are
      consistent.
- [ ] Make tab order, focus rings, button activation and list navigation
      consistent. Text entry owns typing keys; playback/cleanup shortcuts
      must not fire while entering a number or searching.
- [ ] Make every gesture available through a labelled alternative: range
      fields for drags, menu actions for contact edits, numeric transforms
      for gizmos, buttons for navigation and stack ordering.
- [ ] Specify Escape for menus, dialogs, numeric drafts, selection, contact
      drags and gizmos. Focus loss cancels transient drags safely, clears
      modifiers and leaves committed document edits unchanged.
- [ ] Provide native accessibility roles, names, values, actions and focus
      announcements through elisa-ui/host facilities. Prototype timeline and
      viewport alternatives early; document any platform blockers. Add
      semantics for operation rows, timeline/contact controls, viewport
      selection and guide screens. Represent dialogs with an announced
      heading, concise instructions, available choices and predictable focus;
      restore focus to the invoking control after dismissal. Ensure role
      actions match the actual control and never expose unrelated actions.
      Validate a keyboard-only and VoiceOver import–review–repair–compare–export
      path, including search/numeric fields that must swallow global shortcuts.
- [ ] Distinguish source/result and issue severity with labels, symbols and
      line styles as well as color. Respect reduced-motion settings for
      decorative transitions; maintain readable text contrast.
- [ ] Add concise contextual help: what a control changes, units, safe range,
      relevant shortcut and likely side effects. Avoid unexplained terms
      such as wring in primary labels; retain technical terms in advanced help.

### 6.3 Document lifecycle and recovery

- [ ] Exercise replacement, window-close and Cmd-Q prompts on screen,
      including Save/Discard/Cancel, Escape, repeated close requests and save
      failures. Confirm that unreadable, damaged and mismatched sessions are
      rejected before the dirty-document prompt; failed saves preserve the
      prompt and edits; and cancellation leaves the document usable. Keep
      unsaved-work warnings visually distinct from ordinary status feedback.
- [ ] Persist reusable rig profiles, units/floor settings and every exposed
      cleanup parameter alongside the existing v4 source/animation identity
      and local repairs. Version the next schema and define migration behavior
      that preserves the original file until the user saves the migrated copy.
- [ ] Resolve missing or changed sources with Locate source and explicit
      rebind review. Never silently apply old bone indices to a different rig.
- [ ] Add bounded autosave/recovery snapshots in `build/`, a clear Restore
      or Discard flow, retention policy and cleanup controls. Recover committed
      edits only; distinguish autosave from the user's saved session.
- [ ] Explain damaged/unsupported session fields and any dropped corrections
      in a recovery summary. Preserve the original session and refuse unsafe
      newer schemas without replacing current work.
- [ ] Add in-app recent takes/sessions with missing-file handling and Clear
      recents. Remember paths as preferences, not embedded source copies.

**Exit:** keyboard-only and pointer-only import/save/restore/export paths;
all dirty-close and failure branches exercised; no clipped controls at the
agreed minimum window size. Sources unchanged.

## 7. M2 — Import and diagnosis people can understand

### 7.1 Import and rig setup

- [ ] Extend the existing load path with staged validation and progress:
      file/container, animation list, skeleton/channels, units and rig roles.
      Keep the previous document visible until the replacement is valid.
- [ ] Add an animation chooser with names, duration, rate and channel count.
      Warn clearly about empty, duplicate-name and unsupported animations.
- [ ] Display detected scale/up axis/floor and provide explicit overrides.
      Show a floor plane and known-size reference; do not conceal uncertain
      scale behind millimetre readouts.
- [ ] Provide a rig role inspector with hierarchy search, viewport picking,
      left/right assignment, chains and roll-bone mapping. Explain required
      versus optional roles per cleanup tool.
- [ ] Visualize mapped joints, rest pose and chain lengths; flag duplicates,
      missing parents, invalid chains and unreachable geometry. Disable only
      tools requiring invalid roles, with a useful reason.
- [ ] Save reusable rig profiles with a compatibility signature and explicit
      remapping review on mismatch. Offer Reset automatic mapping.
- [ ] Expose current heel/ball approximation and configurable contact points
      where the rig lacks dedicated markers. Record assumptions in reports.
- [ ] Handle unsupported files, oversized input, malformed numbers, missing
      skin/mesh and unanimated nodes with actionable messages and safe fallback
      when skeleton-only review remains possible.

### 7.2 Issue browser and explainable detectors

- [ ] Turn binned markers into selectable issue records: type, bone/chain,
      interval, peak frame, severity, measured value, threshold and confidence
      or uncertainty reason. Retain exact frames behind visual bins.
- [ ] Group adjacent samples into useful intervals; avoid a list entry per
      frame. Filter by issue type, limb, severity and unresolved status.
- [ ] Add next/previous issue and worst issue actions. Selection aligns
      playhead, joint, curves, inspector and optional camera framing.
- [ ] Explain each issue in ordinary language with source/result readings:
      slide, penetration, jitter, spike, pole jump, seam or balance warning.
      Show detector settings and analysis revision in advanced details.
- [ ] Let users mark intentional motion/ignore a finding without modifying
      animation. Persist annotations separately from cleanup operations and
      revalidate their scope after retiming.
- [ ] Distinguish confirmed user contacts from inferred contacts. Show low
      confidence and data limitations; balance and ballistic heuristics must
      not be presented as ground-truth physical validity.
- [ ] Keep diagnosis tied to the displayed revision; show Updating while
      results are stale and prevent stale results from guiding a new fix.

**Exit:** an unfamiliar rig can be configured without source edits; selecting
any issue reaches its exact relevant frame; unsupported capabilities explain
which setup is missing. Intentional-motion fixtures are reviewed for false
positives before enabling recommendations.

## 8. M3 — Guided cleanup, transparent inspection and comparison

### 8.1 Replace the generic Fix all experience

- [ ] Rework the existing automatic action into Preview suggested cleanup.
      Choose a source/motion recipe explicitly or use a conservative neutral
      suggestion. Explain the current boxing-specific behavior during migration.
- [ ] Present recommended steps, affected limbs/ranges, assumptions and
      expected benefit. Show why a step is unavailable or risky.
- [ ] Make contact locking conditional on validated contacts and user intent.
      Do not enable hand locks simply because the user chose automatic cleanup.
- [ ] Separate preview state from committed stack. Offer Apply, Adjust and
      Cancel; Apply adds one grouped undo entry without erasing unrelated
      existing corrections or silently duplicating operations.
- [ ] Evaluate candidate improvement against preservation constraints:
      contacts, knee/elbow transitions, boundaries, peak velocity and intended
      impact timing. Flag or withhold candidates that worsen protected metrics.
- [ ] Report remaining problems and trade-offs after applying. Avoid a single
      reassuring score that hides a newly introduced local failure.

### 8.2 Full operation inspector and reusable recipes

- [ ] Build a searchable Add cleanup menu covering existing supported tools,
      with purpose, prerequisites, relevant issue types and safe initial values.
- [ ] Give each operation a labelled inspector: enable, name, strength/window,
      passes, axes/channel group, bone/role scope, frame/time range, fades,
      boundary mode and tool-specific parameters. Expose actual kernel
      capabilities; mark unsupported combinations rather than inventing them.
- [ ] Support typed values, sliders, reset parameter, reset operation and
      constrained input. Display frames plus milliseconds at the actual rate;
      distinguish playback speed from retiming speed.
- [ ] Explain ordering and fixed pipeline stages, including contact-dependent
      stages, final pins and retime. Reject or explain invalid moves; never
      suggest that a displayed order differs from evaluation order.
- [ ] Add duplicate, rename, bypass-all and before-this-step review (P1).
      Drag ordering must have equivalent move buttons and keyboard actions.
- [ ] Coalesce a slider or numeric edit into one undo transaction. Invalid
      numeric drafts and cancelled drags leave no history entry.
- [ ] Add saved recipes with named/versioned settings, rig requirements,
      relative or absolute scope semantics, and preview before replacement.
      Separate factory presets from user recipes; preserve edited recipes.

### 8.3 Trustworthy comparison

- [ ] Add clearly labelled Source/Result switching, synchronized side-by-side
      and ghost comparison. Match frame, camera, root-motion mode and selection.
- [ ] Offer press-and-hold comparison that restores the prior mode on release
      and focus loss, plus a persistent accessible toggle.
- [ ] Show before/after worst, p95 and total metrics with units, contact sample
      counts and comparable intervals. Display improvement and regression
      separately; expose excluded/unmeasurable data.
- [ ] Add jump-to-largest-change and result-only artifact review. Highlight
      how much each selected operation changed the pose/path, not just detector
      improvement.
- [ ] Provide local looping around an issue, adjustable handles and neighboring
      context. Compare seams and correction fade boundaries explicitly.
- [ ] Improve curve readability: component labels, units, legend, source/result
      styles, zoom/pan, selected range, hover values, fit selection and reset.
      Downsampling must preserve visible extrema and signal its resolution.

### 8.4 Timeline and viewport precision

- [ ] Add typed Go to frame/time, first/last frame, selection start/end,
      previous/next contact boundary and previous/next correction key.
      Display the indexing convention consistently; clamp invalid input with
      an explanation rather than jumping to an unrelated frame.
- [ ] Separate work range, playback loop, operation scope and retime band
      visually and in their labels. Changing a playback loop must not change
      exported duration or operation scope.
- [ ] Support loop-selection playback, adjustable preview speed and stable
      frame stepping while paused. Show actual versus requested playback
      rate when performance cannot sustain real-time review.
- [ ] Add pan/zoom controls, fit clip and fit selection to the timeline.
      Keep the frame under the pointer stable during zoom; distinguish a
      timeline drag from moving a contact edge or retime band.
- [ ] Add a searchable skeleton tree synchronized with viewport selection,
      visibility filters and isolated-chain review. Picking overlapping
      joints must offer an unambiguous alternative through the tree.
- [ ] Provide visible camera orientation, perspective/orthographic labels,
      frame selection, frame whole character and reset camera actions.
      Evaluate track-character and root-relative review modes without
      changing the underlying animation.
- [ ] Keep overlay settings purposeful: presets for Contacts, Jitter and
      Comparison; adjustable trail/onion density; a clear way to return to
      an uncluttered view. Overlay changes do not dirty cleanup sessions
      unless explicitly saved as review preferences.

**Exit:** novice and expert can explain what changed and why; cancelling a
suggestion preserves the stack; applying and undoing restores exact prior
state. No recommendation passes solely on aggregate improvement.

## 9. M4 — Better contact cleanup and precise local repair

### 9.1 Contact editor

- [ ] Replace surprising click-to-lift behavior with select-first interaction.
      Provide explicit Plant, Lift, Split, Merge, Delete and Reset detection
      actions. Keep a contextual hint and preview during a drag.
- [ ] Add timeline zoom/pan, fitted range, visible row labels, draggable handles
      with usable hit targets, numeric interval fields and keyboard nudging.
      Exact one-frame edits must work on long clips.
- [ ] Show automatic versus edited intervals, lock/pivot choice, anchor point,
      target surface, blend-in/out and confidence. Users can revert an interval
      without deleting other contact edits.
- [ ] Add anchor visualization and explicit anchor selection. For wall/rope
      hand contacts, support a user-defined stationary target/plane before any
      automatic inference; moving targets are a separate P2 capability.
- [ ] Warn about overlapping/incompatible pins, unreachable anchors and missing
      chains. Show the chosen compromise instead of implying an exact solve.
- [ ] Expose worst per-frame slide/penetration and transition knee/elbow jumps
      alongside totals. Jump to each metric's actual peak independently.
- [ ] Tighten foot transition quality on the known difficult boxing cases.
      Compare soft reach, adaptive release and blend policies against source
      and existing output; choose thresholds per fixture before tuning.
- [ ] Preserve deliberate toe/heel pivots, foot rolls and intentional slides.
      Separate position lock, heading stabilization and vertical settling so
      users can choose the intended constraint.

### 9.2 Existing advanced tools in the studio

- [ ] Expose existing pins through an inspector: effector, anchor, range,
      blend, enable and reach/error readout. Explain the current head-pin
      positional limitation; never label a nonzero error as exact.
- [ ] Expose existing additive/keyed offsets and correction layers with a
      visible key list, numeric transform editor, local/world-space labels,
      fades, enable/delete and timeline markers.
- [ ] Replace the hard-coded gizmo correction fade with editable defaults
      and per-correction scope. Support snap/nudge and constrained axes only
      where engine semantics are defined.
- [ ] Make preview and release evaluation agree; mark approximate previews
      clearly when full-chain constraints cannot be evaluated interactively.
      Provide Cancel and preserve selection through undo/redo.
- [ ] Expose existing pole/twist/pelvis controls with chain visualization and
      joint motion feedback. Verify roll-bone mapping before redistribution.
- [ ] Complete the existing retime inspector: source/output interval, exact
      duration, blend, selected band, overlap rules and mapped contact/key
      positions. Clarify whether every frame field uses source or output time.
- [ ] Expose opt-in ballistic/momentum tools with applicability warnings,
      assumptions and drift/error readouts. Keep heuristic physics separate
      from a guarantee of a physically valid motion.

### 9.3 Cleanup integrity contracts

- [ ] Add or strengthen contracts for scoped identity, deterministic output,
      finite transforms, preserved hierarchy/lengths, fade boundaries and
      contact/key mapping under retime; identify tolerance versus exactness.
- [ ] Define conflicts between corrections, pins, contacts and retime in one
      shared policy. UI warnings, CLI validation and report explanations agree.
- [ ] Add per-case quality fixtures for unreachable targets, straight-limb
      singularities, mirrored rigs, short clips, first/last-frame contacts and
      loop seams. Include reviewed output and failure expectations.

### 9.4 Tool-specific acceptance records

Populate the following records during M0 before tuning defaults. Numerical
thresholds must include rig scale, sampling rate and units. A mathematically
valid kernel can still fail the visual or preservation gate.

| Tool family | Improvement evidence | Preservation and failure evidence |
|---|---|---|
| De-spike/median/smooth | Fewer labelled noise events; reduced high-frequency energy on affected channels. | Deliberate impact peaks, turn direction, timing and scoped boundaries retained; no flat spots or quaternion flips. |
| Foot lock/pivot | Worst/p95/total planted displacement and floor error improve on validated intervals. | Knee transition speeds, reach error, toe rolls and adjacent airborne movement pass; impossible constraints are reported. |
| Hand lock/pin | Anchor error and planted drift improve on user-confirmed targets. | Elbow motion and reach remain acceptable; free gestures and unmarked spans are unchanged. |
| Pole/twist | Pole discontinuity and unwanted off-axis motion decrease. | Endpoint drift and bone lengths stay within declared tolerance; intentional forearm/roll-bone twist survives. |
| Pelvis cleanup | Path acceleration spikes reduce on selected spans. | Protected plants and body trajectory intent remain; joint reach/extension artifacts do not worsen unnoticed. |
| Seam | Position/orientation/velocity mismatch decreases at the chosen wrap boundary. | Interior motion and contacts remain within their gates; a non-looping action is never auto-converted into a loop. |
| Corrections/offsets | Requested pose change is reached within the declared solver tolerance. | Fade endpoints, unselected bones/frames and undo/session replay agree; unreachable goals are visible. |
| Retime | Output duration and frame mapping match the requested speed policy. | Contacts, keys, pins and issue navigation map consistently; no invalid ordering, discontinuous orientation or unexplained drift. |
| Physics heuristics | Selected path/spike measure improves with assumptions recorded. | Contact and pose distortion budgets pass; unavailable mass/environment information is disclosed. |

For each case retain the source, recipe, detector settings, expected metrics,
worst-frame references and reviewed captures. Record both absolute error and
change from source; summing errors across clips must not hide a failed case.

**Exit:** contact and correction editing is discoverable and precise;
difficult fixtures satisfy declared local quality gates or show a clear
unresolved warning. Every exposed tool survives undo/session/export replay.

## 10. M5 — Responsiveness and reliability at production scale

**Touchpoints:** `app.elisa`, `model.elisa`, studio state, existing operation
and rig caches, engine host scheduling, elisa-ui rendering limits.

- [ ] Measure end-to-end input-to-preview latency with feet enabled, contact
      edits, long clips and large rigs. Profile actual screen playback and
      GPU drawing, not just headless kernel timings.
- [ ] Move expensive load/analysis/rebuild/export work out of the UI event
      path using an engine-supported worker/job boundary. Prototype safe Elisa
      ownership first; do not share mutable clip buffers unsafely.
- [ ] Introduce document revision and job identity. Apply results only to the
      matching document/revision; supersede queued edits and discard stale
      results after undo, take changes or new settings.
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

## 11. M6 — Export, recipes and batch production

### 11.1 Reviewed export (P0)

- [ ] Add export review with selected animations, destination under `build/`,
      filename, duration/rate, rig profile, root-motion policy, active operations
      and unresolved warnings. Require explicit acknowledgement for material
      warnings, with a route back to the relevant issue.
- [ ] Provide intentional export controls only for supported semantics.
      Root extraction/in-place conversion or key reduction requires a separate
      implemented and validated policy before offering a checkbox.
- [x] Guard publication destinations under canonical `build/`; reject source
      paths and hard-link aliases, symlink leaves, non-regular targets and
      unconfirmed replacement. Quick Export asks before replacing; Cancel keeps
      the current destination. See `StudioExportPolicy` and the FilePanel path
      identity adapter.
- [x] Stage GLB bytes in a unique same-directory temporary, flush and reload
      them, compare the exact bytes with the reviewed cleaned document, recheck
      destination safety, then publish with one atomic rename. Failed writes or
      validation leave the selected destination intact.
- [ ] Reload the derived GLB and compare animation channels/poses, contacts,
      duration and untouched nodes/skins/meshes against expected output.
      Compare evaluated output against the reviewed revision, and report write
      success separately from semantic review.
- [ ] Export a human-readable summary and machine-readable report containing
      source/output hashes, animation identities, tool/dependency versions,
      recipe/rig settings, metrics, thresholds and warnings.
- [ ] Offer Show in folder and Open result for review. Keep the editable
      session separate from the exported animation and explain both.

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
- [ ] Capture and review visual states at supported window sizes/scales:
      first run, malformed input, busy/cancelled job, missing rig roles, dense
      timeline, long paths, warnings, help and restored session.
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

## 13. M8 — Evidence-led advanced cleanup (P2)

These are research candidates, not promised defaults. Promote one only after
an observed corpus failure, a clear user workflow and a measurable benefit.

- [ ] Investigate adaptive filter windows and confidence-aware recommendations
      that preserve impacts and deliberate turns better than fixed presets.
- [ ] Investigate contact-aware pelvis/whole-body adjustments for unreachable
      plants, comparing foot error, knee motion and body-path distortion.
- [ ] Evaluate richer contact geometry, multiple support surfaces and moving
      hand targets with explicit target motion input; do not infer hidden
      environment motion from pose data alone.
- [ ] Evaluate improved head/body pin solving only where current neck reach
      limits block a real repair workflow.
- [ ] Investigate surface penetration checks when validated mesh/collision
      geometry is available, distinct from joint/floor proxies.
- [ ] Evaluate key reduction and additional import/export formats only against
      a named downstream pipeline with round-trip quality fixtures.

For each experiment: record baseline, hypothesis, prototype, contracts,
comparison metrics, visual review, runtime cost and adopt/reject decision.
Do not change default recipes until preservation and failure behavior are
qualified on the expanded corpus.

## 14. First implementation slices

Start in this order; each row should become several small reviewable commits.

| Slice | Concrete result | Evidence needed before moving on |
|---|---|---|
| 1 | M0 studio audit, corrected current-behavior docs and interaction specifications | Running-window captures, gap matrix, measured limits and reviewed first-use flows. |
| 2 | Finish command discovery, focus rules and accessible alternatives | Pointer and keyboard journeys; native tree gives every primary control a clear name, role-appropriate actions, correct value and useful focus; dialogs and status are announced; VoiceOver and keyboard users finish the core tasks; text fields cannot trigger global cleanup; focus survives dialogs and panels. |
| 3 | Missing/changed source locate flow, rig-profile persistence and safe rebind review | Locate succeeds for renamed files; mismatched animation/rig cannot receive stale edits; rebind review shows exactly which stored settings remain valid. |
| 4 | Animation/rig/floor setup with actionable validation | Valid, ambiguous and incompatible rig fixtures; users can resolve warnings without source edits. |
| 5 | Selectable issue list linked to timeline, joint and metrics | Exact frame selection, understandable issue summary and stale-analysis handling. |
| 6 | Suggested-cleanup preview and complete inspector for one existing tool | Apply/cancel/undo parity; local preservation metrics; user can explain the effect before accepting. |
| 7 | Select-first contact editor with interval/anchor controls | One-frame precision, keyboard equivalent, transition quality and visible compromises. |
| 8 | Revision-safe background rebuild and bounded recovery | Rapid edits, undo and take swap reject stale results; cancellation preserves the last valid preview. |
| 9 | Complete existing tool exposure and reviewed export | Session/CLI/preview/export semantic parity; output reopens and matches the reviewed revision. |
| 10 | Corpus expansion, user trials and release qualification | All P0 gates; unresolved limits documented; first-time users finish the core journey without coaching. |

Keep the plan driven by the user's full task: understand the capture, make a
controlled repair, see whether it helped, retain the work, and deliver an
animation that matches what was reviewed.
