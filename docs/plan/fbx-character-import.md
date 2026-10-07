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

## Ownership, typestate and foreign boundary requirements

- Represent validated request, owned staging, verified conversion and publishable
  animation as distinct states. Use the current compiler's checked state-family
  features, with private construction/transition authority and affine consumption.
  A status flag or state name alone cannot establish resource ownership, digest
  verification or successful native effects. Derive value states only from checked
  predicates and admit protocol transitions only after the corresponding effect.
- Inspect current Stage1 support before selecting syntax: compiler documentation
  contains both delivered slices and unfinished parity work. Require a positive
  compile and the intended semantic rejection for illegal construction, premature
  publication and use after consuming a transition. Backend decline is not proof
  that an invalid program was rejected by the safety checker.
- Keep raw extern declarations private to a bounded adapter. Use operation-specific
  `can` grants for raw calls and pointer conversion, retaining propagated tracking.
  Reserve `trusted` for an explicitly justified boundary where tracking is
  intentionally stopped. Do not grant general Unsafe to controllers or treat
  annotations as proof of the native implementation.
- Record each native declaration's target ABI, buffer extent, termination,
  initialization, mutation, pointer retention, blocking effects and error behavior.
  Express supported extern contracts and lifetime annotations accurately. The
  current converter/stager return integer statuses, not borrowed pointers, so
  borrowed-return annotations cannot establish their input lifetime.
- Validate native output before constructing a verified state: bounded nonempty
  paths, strict digests, managed destination ownership, preserved original identity,
  readable selected animation and completed worker ownership transfer. Failed
  output must remain an error and must not acquire publication authority.
- For asynchronous transfer, qualify the indirect aggregate ABI, inline capture
  copy, owned result arena, completion synchronization and one-shot join/adoption.
  Test capture after the submitting frame ends and returned-array growth after
  worker release. Cancellation, refusal and shutdown must drain each owner once.
- Land kernel contracts and companion laws with these changes. Keep native ABI,
  source correspondence, compiler rejection and actual UI evidence distinct;
  unknown proof results cannot authorize unsafe access or remove runtime checks.

## Current implementation and remaining work

The Open FBX controller now dispatches the import worker, retains the original
source identity, admits only a current successful result, and supports the
Character/Skeleton switch with a skeleton fallback when no surface is available.
Exclusive private staging, source/runtime digests, importer/options identity and
memo source references are integrated. The bounded `source-ref-v1` codec,
source-aware session save, format-aware Locate worker and publication admission
are implemented. Their current runtime, asynchronous ownership and authenticated
proof qualification remain open.

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
The old Python conversion driver used the wrong sampling-rate ABI; corrected
checks and their limits are documented in the captured native evidence.
Independent eight-influence Blender evidence is under
`build/fbx-user-highblock-influence8` and `build/fbx-bladed-influence8`.
UI switching remains unverified.
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

- Qualify the current void-poll result-owner repair before accepting background
  import. Earlier function-value ABI repairs made focused joins work, but the
  actual void caller still passed a null result arena: worker payload headers
  survived while their bytes were freed, and nested Memo cleanup faulted.
  Preserve worker arena/adoption and callback repairs through the rebase, then
  run the retained lifetime and performance controls and the actual Studio
  journey. See [joined-result lifetime evidence](../proof-gaps/fbx-join-buffer-lifetime.md)
  and [compiler promotion gates](current-delivery-queue.md). A standalone probe
  omits AppKit and cannot establish the complete user journey.

- Complete cancellation/restart and repeat authorized runtime checks against the
  final current application tuple.
- Inspect actual Open FBX, character deformation, pose edits and Character/Skeleton
  switching in the current application.
- Qualify the implemented session-reference codec and source-aware Locate
  integration. `load_at_index` is now the legacy GLB path only; referenced GLB
  verifies digests, while FBX validates saved processing identity and original
  bytes before cache reuse or regeneration. Exercise save/reopen and relocation,
  missing cache/source, changed source, changed importer/options, interrupted
  regeneration and legacy compatibility. Require the regenerated runtime digest
  and selected animation to match before applying edits. Compile and authenticate
  the existing codec, resolution, admission and decode-ownership laws; source
  compilation does not establish returned-buffer lifetime or native file identity.
- Repair shared-field reborrow replay and zero-argument generic-region proof
  handoff gaps, then obtain current source correspondence evidence. Native staging
  correspondence remains a separate requirement.

## Remaining character fidelity acceptance

The independent fixture comparison identified a real 9.243 mm vertex error from
dropping a fifth skin influence. See
[skin comparison evidence](../acceptance/fbx-topology-and-skin-pose-2026-10-07.md).
Engine commit `1cbed086` implements eight-slot conversion/loading/evaluation,
paired attributes, legacy four-slot compatibility, bounded joint/weight validation
and refusal above eight positive influences. It raises the converter joint limit
to 256 so the user's 89-joint Unreal character is accepted. Full-source Blender
pose comparisons and a focused engine viewport run now cover that fixture.

Build the final Studio tuple containing these changes and the corrected native
`double` sampling-rate declaration. Complete the actual import, playback,
pose-edit and display-switch journey before closing this requirement. Cover
multiple stacks, unsupported input and edited pose cache invalidation; retain
absolute maximum errors alongside percentile measurements. Largest-mesh-only
conversion and material fidelity remain explicit limitations requiring product
handling rather than a broad FBX compatibility claim.
