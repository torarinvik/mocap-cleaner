# FBX opening and character review

## Required result

Open an FBX take through Open Take or file drop. Review its animation on its
character surface when available, and switch between Character and Skeleton
using an understandable toolbar control and M. Loading another character remains
available for skeleton-only takes. Preserve original source bytes.

## Import and source identity

- Extend chooser and file-drop routing to FBX with case-insensitive extension
  handling. Validate actual content at the bounded engine parser boundary.
- Use the current pinned ufbx integration. Existing animation-only FBX-to-GLB
  conversion is insufficient for an FBX that contains a character surface.
- Produce editable animation and skin/mesh data with consistent node indices,
  transforms, units, inverse bind matrices and joint weights. Preserve animation
  stack selection. Avoid silently choosing helper geometry over the character.
- Place derived data in exclusively created Studio-owned directories under
  `build/`. Never overwrite an existing cache or original source file.
- Retain original source identity independently from the derived GLB identity.
  Session reopen/Locate, recent files and export review must describe the FBX
  source; edited export must not overwrite it. Bind caches to source bytes,
  importer revision/options and derived-content digests.
- Failed or cancelled import preserves the current take. Report unsupported
  surfaces/materials and skeleton-only fallback plainly. Import work must not
  block viewport input; retain ownership until worker completion or drain.

## Viewport behavior

- Character mode draws the posed surface; Skeleton mode draws editable bones.
  A missing or failed surface draws the skeleton rather than an empty viewport.
- Imported mesh must follow the edited pose, frame selection and playback, not
  merely display its rest pose. Invalidate skin caches after take/rig/stack changes.
- Keep comparison overlays independently selectable. Provide clear unavailable
  state and a discoverable Load Character action for animation-only sources.
- Keyboard, pointer and accessibility use the same display state. Frame Character
  includes the visible body bounds. Do not advertise texture fidelity until the
  renderer preserves the imported material/texture data.

## Evidence required

Matched current-source builds, animation and skin correspondence, source hash
preservation, malformed/oversized/truncated input refusal, cancellation/restart,
multiple animation stacks, missing surface fallback, pose edits and real viewport
inspection. Source compilation does not establish these runtime results.

## Current implementation and remaining work

The Open FBX controller now dispatches the import worker, retains the original
source identity, admits only a current successful result, and supports the
Character/Skeleton switch with a skeleton fallback when no surface is available.
Exclusive private staging, source/runtime digests, importer/options identity and
memo source references are integrated. Session reopen and Locate still need FBX
source-reference integration.

A full native Studio build completed on compiler `bb274b14` with the project
repairs retained. Its Stage1 SHA-256 is
`36389f6b18268d4266bd68aacd813c703cd788956b611b9fad9964da11a2aa32`;
matching runtime SHA-256 is
`51365ba4a06e13e0af344b5e21790795e15f1b7fbba23c0b5b94b5a52b00ccee`.
The executable SHA-256 is
`97ea9a61994205f488848d198df163c631fd9d24e562648455eacd74a0486585`.
Build evidence is retained in `build/latest-compiler-qualification/` and generation
`build/studio-build.yOXPzH`.

The first authorized native FBX check produced a GLB containing a mesh, skin and
animation, refused an existing destination without changing it, and preserved the
original FBX digest. Results are in `build/fbx-runtime-8t_omy1p/results.json`.
Further deterministic, malformed/truncated and bounded FIFO refusal checks are
recorded in [captured native evidence](../acceptance/fbx-native-checks-2026-10-07.md).
Independent Blender pose evidence is under `build/fbx-pose-check-bb274`; the
mesh outlier remains under investigation. UI switching remains unverified.
The converter currently retains one largest supported skinned mesh; multiple
mesh/material fidelity remains open.

Compiler upstream performance changes `fb9747ee` and `63585c5f` are integrated in
selected checkout merge `48dc78e2`. The compiler reseed and Studio compilation/linking succeeded; current build and
visible workspace control evidence are in
[workspace build record](../acceptance/studio-workspace-build-2026-10-07.md).
Package publication remains blocked by the old running bundle lease; the retained
new bundle is open. Complete full runtime and proof acceptance before treating
the journey as qualified. Earlier
build and runtime results remain evidence for their captured source tuple.

Next acceptance work:

- Complete cancellation/restart and repeat authorized runtime checks against the
  final current application tuple.
- Inspect actual Open FBX, character deformation, pose edits and Character/Skeleton
  switching in the current application.
- Implement persisted original/runtime references for session reopen and Locate,
  including changed-source refusal and cache recovery. Persist format, original
  digest, runtime digest, importer/options identity and animation selection using
  a versioned bounded codec. Legacy GLB sessions must remain readable.
  `session_locate_worker.elisa` currently calls `Model::load_at_index` on the
  original path; replace this direct GLB assumption with format-aware loading.
  A relocated FBX must match its saved original digest before applying edits.
  Reuse cache only when its runtime digest and importer/options match; otherwise
  regenerate from a verified source under the chosen workspace. Handle missing
  cache, missing source, changed source and interrupted regeneration explicitly.
  Add refusal and round-trip laws alongside the codec and admission logic.
- Repair shared-field reborrow replay and zero-argument generic-region proof
  handoff gaps, then obtain current source correspondence evidence. Native staging
  correspondence remains a separate requirement.

## Character fidelity follow-up

The independent fixture comparison identified a real 9.243 mm vertex error from
dropping a fifth skin influence. See
[skin comparison evidence](../acceptance/fbx-topology-and-skin-pose-2026-10-07.md).
Preserve up to eight influences using paired JOINTS_1/WEIGHTS_1 attributes and
an eight-slot loader/evaluator; refuse source vertices above the supported bound
rather than silently losing weights. Keep four-influence GLBs compatible through
zero-filled additional slots. Validate paired attributes, accessor ranges, joint
bounds, finite nonnegative weights and positive combined totals. Repeat independent
pose comparisons against the full source weights after implementation. Do not
close character fidelity on percentile measurements that hide an outlier.
