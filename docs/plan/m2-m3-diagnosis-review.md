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

The frame dialog is implemented: Cmd-G, digit-only input, 1-based labels,
last-frame clamping with an explanation, Apply/Cancel, input modality,
focus-loss cancellation, accessibility routing and exact captured target
checks. Its parser statuses are typed alternatives. Tab/Shift-Tab traverse
the input and both actions; Enter/Space activate focused buttons, and the
focused control has a visible outline. Focus traversal uses a closed enum
with accompanying laws; native focus behavior remains to be qualified. Integrated compilation,
native keyboard/accessibility acceptance and current proof replay remain
open. Time input and the boundary-navigation controls below remain to be
implemented; this does not close the combined timeline milestone.

The exact boundary-selection policy now admits only in-range frames strictly
before/after the playhead, retains the nearest eligible boundary, and refuses
invalid candidates without losing the prior choice. It also validates inclusive
selection endpoints. Its accompanying laws compile with retained function
symbols at O0; current producer/replay and UI integration remain open. Contact
and correction-key producers must feed exact frames, never visual bins, and
the UI must explain when no boundary is available. Keyboard integration now
uses Home/End for clip endpoints, Shift-Home/End for selection endpoints,
Cmd-Up/Down for contact-state transitions, and Cmd-PageUp/PageDown for enabled
correction keys. Contact transitions select the first frame with the new state;
they do not fabricate a clip-end transition. Incomplete contact tracks, an
unevaluated current stack, and active pointer drags refuse navigation. Empty
directional searches explain why the playhead stayed unchanged. Full integrated
compilation, current replay, pointer/AX controls, native shortcut delivery and
selection/contact/key journey acceptance remain open.

Unsigned seconds entry now has a separate counted-text adapter and integer
millisecond kernels. It accepts whole seconds or up to three decimal places,
including `.5`; malformed prefixes, repeated dots, excess digits and incomplete
decimal drafts are refused. Conversion uses the evaluated clip rate and floors
to the containing output frame; valid times past the clip clamp to its last
frame. The scalar kernels and ten laws compile at O0 with retained symbols,
as does the parser. No executable parser fixtures were run. Text parsing is
outside the current symbolic boundary; current producer/replay, UI wiring,
native text input and the actual-rate playback/time-display consistency audit
remain open. A parser implementation alone does not close Go to time.

The frame/time dialog is now wired to Cmd-G / Cmd-Shift-G, shared Apply/Cancel
validation, decimal keyboard drafts, retained text-field changes and mode-specific
visual/accessibility labels. It captures the clip rate as well as the existing
take/document/stack/frame-count target, refusing a changed rate. Integrated
qualification remains open. The committed-text callback now validates the whole
insertion's characters and combined capacity before changing the draft, accepts
decimal seconds, and refuses unsupported content without dropping characters.
Endpoint/boundary navigation explicitly pauses playback without changing the
stack/history; active contact presses also refuse navigation. Qualify native
committed-text/paste routing, exact refused-draft preservation and playing-state
transitions in the integrated window.

- [ ] Qualify time conversion against the timeline clock and evaluated sample
      times. Loaded Studio playback now uses captured output timestamps; the
      displayed average key rate remains an estimate.
      Use one validated time basis for playback, time entry, stepping, display,
      curves and reports; describe any rounding. Detect nonuniform key spacing
      and distinguish authored keys from evaluated review samples. Never present
      an estimated average key rate as exact timing. Cover supported rates,
      retimed results, degenerate channels and nonuniform input without moving
      or exporting a different pose than the time label indicates.
      Include fractional rates such as 30000/1001 and 60000/1001; an integer
      rounded fps label must not become the authoritative sample clock.

An integer-rate clock policy now provides ceiling-rounded frame starts, an
exclusive clip end, floor conversion and modulo looping that preserves phase
across several short loops in one tick. Its ten laws compile at O0 with retained
symbols. It is not yet integrated into playback and does not represent
fractional rates or validate authored key spacing. Current producer/replay,
rational-rate timing, evaluated-grid admission and clock integration remain
required before the clock-consistency item can be closed.

The clock arithmetic now also represents bounded rational rates, including
30000/1001 and 60000/1001. Quotient/remainder splitting avoids overflowing a
direct maximum-time × numerator product. The integer-rate entry points delegate
to that same arithmetic. Nine rational-clock laws compile at O0 with retained
symbols, including fractional-frame boundaries and maximum-duration cases.
The rational policy remains a separate arithmetic foundation. Loaded Studio now
uses captured sample timestamps; current proof/runtime qualification and consistent
curve/report timing remain required.

Each evaluated Clip now captures an owned, privately represented sample clock
from its actual cleaned GLB input timestamps. Times round to the nearest
microsecond, become clip-relative, and must strictly increase. Every nonconstant
channel must match the same per-frame times and input/output key counts;
single-key channels remain constant, with finite valid times. Cubic interpolation,
empty/oversized grids and mismatched channel grids return typed unavailable
states rather than a guessed exact clock. Nonuniform increasing grids are
supported. The capture module and updated model compile at O0 to retained
objects; scalar timestamp policy now has fourteen accompanying laws. Playback,
stepping and seconds entry use this clock, and the status bar shows the actual
sample timestamp with six decimal places. Unsupported clocks explain refusal.
Current proof/replay, integrated app compilation and native playback acceptance
remain open; export reports and curve timing still need consistent integration.

- [ ] Extend seconds entry to captured microsecond precision so displayed sample
      timestamps can be entered without truncation. Keep one capacity policy for
      typed input, committed text, accessibility replacement and parser; add the
      matching contracts/laws and qualify boundary/clamp behavior.
- [ ] Make pointer and accessibility Play enablement share the captured-clock
      readiness/count predicate used by the playback handler. Preserve Stop when
      playback is already active; explain unavailable timing consistently.

- [ ] Add typed Go to frame/time, first/last frame, selection start/end,
      previous/next contact boundary and previous/next correction key.
      Display the indexing convention consistently. Keep empty, malformed or
      overflowing drafts editable and disable Apply without moving the playhead.
      Clamp a valid numeric value outside the clip with a visible explanation.
      Bind every action to the current document, result and stack revisions;
      replacement or a changed frame count invalidates an open draft.
      Expose identical validation and enablement through pointer, keyboard and
      accessibility actions. Cancel and focus loss preserve the selected frame.
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

Stale candidate viewing is now refused by a pure preview-admission contract,
with missing/stale candidate laws. The viewport falls back to current result;
the panel highlights the actually visible result and labels the stale suggested
control. Qualify a document/stack change during candidate viewing: no stale pose
may remain presented as current, and suggested-view activation stays disabled.
Candidate metric freshness and native rendering/replay evidence remain open.

Stale suggested comparisons now withhold their before/after numeric rows and
show rebuild guidance. Contact, joint, boundary, velocity and impact evidence
all return unavailable when the captured revision is stale, preventing a passing
label from describing measurements against an older candidate. Qualify stale
review screens and accessibility announcements; current compilation/replay and
native evidence are pending.

Initial suggestion generation now explains an unevaluated baseline or failed
candidate evaluation instead of silently returning. Impact-review preparation
is deferred until a valid candidate is admitted for opening; blocked or failed
entry does not reset annotation intent. Qualify injected candidate failure and
rejected entry against exact stack/history, visible result and impact-review
snapshots. Successful entry may invalidate annotations for a changed durable
source identity; failure messages do not claim source changes or proof closure.
