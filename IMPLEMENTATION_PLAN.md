# Mocap Cleaner — Product and Implementation Plan

Updated 2026-10-09. This roadmap describes remaining work. Completed
implementation is recorded in Git. Milestone documents retain their original
section numbering and detailed acceptance criteria.

The product goal is a clear, safe workflow from unfamiliar capture to reviewed
export, with understandable diagnosis, recoverable cleanup and responsive
professional tools.

## Mandatory file size limit

Every maintained repository file must have **at most 600 lines**. This applies
to existing and new source, proof, test, script, configuration and documentation
files throughout every milestone. Split growing files into cohesive modules
before an edit would exceed the limit; use nested modules when appropriate,
keep helpers private and expose only the APIs callers need. Preserve includes,
behavior and proof coverage, and check file lengths before committing. Generated
`build/` artifacts and sibling repositories are outside this repository rule.

## Constants and finite choices

Whenever a module contains multiple `const` values, group them in a named
`const module`. Prefer a `const enum` when those values encode a closed set of
alternatives, and an algebraic data type when alternatives carry different data
or must exclude invalid combinations. Keep purpose-specific `const module`
groups for related numeric limits, units and configuration that are better
expressed as values. Apply this to existing code and every new change. Preserve
public/private visibility, contracts, proof coverage and the 600-line maximum.
Update all consumers and validate explicit conversions at serialization/native
boundaries; preserve required wire values. See the
[representation migration inventory](docs/plan/constant-modules.md).

## Highest-return execution focus

The retained 2026-10-08 crash report belongs to project revision `31459ca3` and
does not include a frame or playback position. The user later located the crash
around 60% of the 337-frame high-block animation (about frame 202). A fresh O0
Studio package is now at `build/MocapStudio.app`; its staged-input manifest
records the current Stage1 compiler binary and runtime hashes. It uses compiler
revision `09f15cf8`, including region-handoff fix `806772c7`, engine revision
`1e98f075` and UI revision `65f370f3`. The current converter produced a derived
GLB from the unchanged FBX, and the Studio character harness evaluated, skinned
and drew every frame without a crash. This is headless evidence: native file
opening, playback controls, Character/Skeleton switching and camera behavior
in the packaged app are still unverified. Complete that current-app journey,
then deliver one existing cleanup with preview, apply/cancel, undo and a GLB
export that reopens.

Follow the [ranked delivery queue](docs/plan/current-delivery-queue.md):

1. Finish native interaction with the fresh package on the reported FBX: test
   opening, playback near frame 202, Character/Skeleton switching,
   framing/orbit/zoom, repeated redraw, workspace setup, cancellation, retry and
   malformed-input recovery. Keep the source hash unchanged.
2. Complete one existing cleanup/export journey with preview, apply/cancel, undo,
   contracts, source correspondence and independent proof replay; reopen the GLB.
3. Refresh remaining proof/replay evidence against current sources and qualify
   interruption recovery and stale-publication handling before release. Then fix
   measured interaction bottlenecks; resume broader storage, batch and research
   work only after the first useful result passes.

## UI direction from the cleanup prototype

Use the supplied prototype as the product direction for the cleanup workflow.
Keep its information hierarchy and visual language, then deliver it in small
steps tied to the first useful result rather than attempting a broad redesign at
once:

1. Keep a visible five-stage workflow — **Import, Analyze, Auto Fix, Validate,
   Export** — with the current stage, completed stages and blocked prerequisites
   clear at a glance. Switching stages must preserve the take, selection and
   pending edits.
2. Keep the asset/scene tree on the left. Show the active take, character,
   skeleton, markers, contacts and scene elements with concise labels, useful
   counts and stable selection. Loading, missing and incompatible assets need
   actionable explanations.
3. Give the central viewport the most space. Keep perspective, front and side
   views available; make shaded/mesh and skeleton modes obvious; synchronize
   selection and frame position across views. Keep orbit, pan, zoom, framing and
   view reset discoverable and keyboard accessible.
4. Keep timeline, contacts and motion curves together below the viewport.
   Scrubbing, playback, curve selection and issue selection must identify the
   same frame range. Show the current frame, total frames and playback state.
5. Put issue review and cleanup controls in a right-side inspector. Each finding
   needs a concise name, affected body part, frame range, severity, explanation,
   confidence source and available action. Filters and sorting must not change
   the underlying issue identity or selected take.
6. Separate a batch recommendation from individual fixes. Before applying,
   show the exact selected scope, preview the before/after result, allow cancel,
   and retain undo. Make automatic review an explicit choice with visible
   progress, pause/cancel behavior and a clear completion summary.
7. Keep validation next to the preview and export action. Report measured
   results with units, explain failed checks and offer the next useful action.
   Do not show simulated quality gains, AI confidence or automation coverage as
   facts; every number must come from the current take and recorded analysis.
8. Make source preservation, workspace readiness, save state and pending exports
   visible. A failed import, cleanup, validation or export must say whether the
   take changed and provide a safe retry, recovery or cancellation path.
9. Preserve professional density without hiding controls: use consistent
   spacing, contrast, selection and severity colors; label icon-only controls;
   show focus and keyboard shortcuts; provide useful empty, loading, error and
   no-results states; and let secondary diagnostics collapse without moving the
   main workflow.

First implement only the layout and interactions that help a user open the
current FBX, understand one finding, preview and undo one repair, and export a
reopenable result. Measure viewport/playback and panel responsiveness on that
same take before expanding automation, batch controls or visual polish.

Keep one integrated product slice active, with only the compiler/prover/native
repairs necessary to unlock it. Prioritize observed failures, user data at risk
and missing workflow steps. Defer broad refactors, new algorithms and visual
expansion unless they remove a demonstrated blocker. Existing implementation
needs qualification before extension. All M0–M8 requirements remain in scope;
priority changes do not waive acceptance or the mandatory engineering rules.

## Detailed roadmap

- [Current delivery queue and finish criteria](docs/plan/current-delivery-queue.md)
- [Acceptance, dependencies and unresolved decisions](docs/plan/acceptance-and-dependencies.md)
- [Pending current-toolchain policy qualification](docs/acceptance/pending-policy-qualification-2026-10-06.md)
- [Recent law source compilation; proof qualification pending](docs/acceptance/current-law-source-compile-2026-10-07.md)
- [Product goals, user journeys and baseline](docs/plan/product-and-m0.md)
- [M1: workspace, storage and recovery](docs/plan/m1-workspace.md)
- [Generated-build cleanup delivery slices](docs/plan/generated-build-cleanup.md)
- [M2–M3: diagnosis, guided cleanup and comparison](docs/plan/m2-m3-diagnosis-review.md)
- [M4: contact cleanup and precise repair](docs/plan/m4-contact-repair.md)
- [M5: responsiveness and reliability](docs/plan/m5-responsiveness.md)
- [M6: export, recipes and batch production](docs/plan/m6-export-batch.md)
- [M7: release qualification](docs/plan/m7-release.md)
- [M8 and first implementation slices](docs/plan/m8-research-and-order.md)

## Delivery requirements

- Enforce `Global.Read` for reads and `Global.Write` for writes to `global mutable`
  storage, including transitive callers and callbacks. Declare the effect rows and
  grant access at the narrow owning scope; read-modify-write needs both members.
  Preserve propagation with `can`; use `trusted` only at an explicitly reviewed
  tracking boundary. Enable the current compiler's global permission checking
  during qualification and refuse ungranted access. Migration is incomplete until
  the full application and dependency call graph pass that check.
- Use grouped family grants when a row names multiple members of the same
  family, for example `can[Memory{Allocate, Release}, Global{Read, Write}]`.
  Preserve the exact member set and unsafe tracking; qualify compiler expansion
  and member-specific refusals before treating the syntax as supported.
- Commit each small source/proof improvement; include related documentation
  in those commits. Do not create documentation-only commits.
- Extend arrays for fixed sequences of literals. The lexical
  `scripts/check_literal_push_runs.py` gate rejects consecutive integer-literal
  pushes to the same array; review other literal forms manually.
- Use the latest compiler, proof assistant, Elisa UI and engine dependencies,
  retaining required mocap fixes.
  Record fetched upstream revisions, source changes and binary manifests; rebuild
  stale products before acceptance. Build scripts must not silently permit stale
  binaries or select historical worktrees. Explicit historical comparisons remain
  separate from current-snapshot qualification. See the
  [dependency freshness audit](docs/acceptance/dependency-freshness.md).
- Preserve source takes; put derived files in `build/`.
- Land contracts and proof laws alongside proof-critical logic.
- Enforce the mandatory 600-line file limit on every change; see
  [module extraction details](docs/module-refactor.md).
- Record unresolved evidence in [proof gaps](docs/proof-gaps.md).
- Apply the shared evidence and dependency requirements before closing any
  milestone; distinguish implementation from native and user acceptance.

## Current user priority: finish FBX review and deliver a cleaned result

Deliver [FBX opening and Character/Skeleton review](docs/plan/fbx-character-import.md)
with source-preserving import and editable posed surfaces. Earlier runtime
checks reported core import, playback and keyboard view switching on a prior
package; those checks and the retained crash trace do not qualify the current
checkout. Build and verify current sources on the reported asset, then complete
one reviewed cleanup/export before expanding the feature set.
