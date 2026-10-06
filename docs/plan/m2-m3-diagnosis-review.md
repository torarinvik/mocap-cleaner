# M2–M3: diagnosis, guided cleanup and comparison

[Roadmap index](../../IMPLEMENTATION_PLAN.md)

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

- [ ] Expand the current aggregate spike intervals to typed findings with
      known bone/chain, interval, peak frame, severity, measured value,
      threshold units and evidence state (measured, inferred or unavailable),
      with an uncertainty reason. Numeric confidence requires calibration on
      labelled fixtures. Retain exact frames
      behind visual bins; never attach an unknown aggregate finding to an
      arbitrary joint.
- [ ] Link exact issue selection to the curves and inspector, focus a known
      subject, and optionally frame the affected region in the viewport.
- [ ] Integrate ordinary-language explanations for the currently produced
      aggregate spike findings, including exact peak frame/value, threshold
      units and unknown subject. Connect the explanation policy to the UI.
- [ ] Implement and qualify distinct producers before presenting slide,
      penetration, jitter, pole jump, seam or balance findings. Each type needs
      its own labelled positive and intentional-motion negative fixtures,
      declared false-positive budget and source/result readings. Show detector
      settings and analysis generation in advanced details.
- [ ] Distinguish confirmed user contacts from inferred contacts. Show low
      confidence and data limitations; balance and ballistic heuristics must
      not be presented as ground-truth physical validity.
- [ ] Keep visible status, row selection, filter counts and navigation
      synchronized with the displayed analysis generation. Keep durable
      source/animation/rig identity, process-local analysis generation and
      detector/configuration schema distinct. Persist annotation intent against
      durable identity, schema and finding fingerprint; never persist a build
      counter as a content revision. Qualify reopen, rebuild, retime and rig
      reassignment invalidation. Validate compact
      controls at the minimum window size and provide a discoverable way to
      inspect each available filter choice.

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
      existing corrections or silently duplicating operations. The existing pure
      admission policy still requires model and UI integration. Apply requires
      exact document and stack revisions plus measured passing results for
      every applicable preservation constraint; unavailable data blocks an
      automatic pass. Cancel/Escape leave stack and history unchanged; Apply
      followed by Undo restores their exact prior state.
- [ ] Admit preview only when the current displayed result matches its evaluated
      stack and document; failed/pending evaluation cannot be treated as the
      baseline. Candidate generation failure preserves the prior valid settings
      and candidate together, or invalidates both explicitly. Never show new
      lock settings with an old candidate pose.
- [ ] Make the Apply handler enforce the same candidate existence, freshness,
      changed-stack and evidence admission as its visual/keyboard/AX enablement.
      Cover adjustment failure, stale results during preview, failed evaluation,
      missing candidate and no-op candidate. Retain focus and explain recovery.
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


### Guided action dispatch qualification

The common suggestion action handler now checks the same action availability
predicate used by focus/accessibility before changing focus or dispatching.
This covers adjustment-page actions, lock prerequisites and impact annotation
capacity as well as the existing Apply admission checks. Qualify disabled
pointer/key/AX activation, especially inactive-page Back/Adjust and exhausted
impact capacity; no state or history changes may result from refused actions.
Current compilation and native acceptance remain open.
