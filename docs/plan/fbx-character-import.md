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

## Current slice

Commit `d51f9d6` makes the existing surface switch Character/Skeleton and uses a
contracted fallback policy. Its policy laws compile with the selected current
compiler. The FBX chooser, producer and source/cache integration remain open.

Commit `8cf0fcf` adds a worker-owned FBX job/result and publication policy laws.
Paths remain owned while conversion and GLB loading run; invalid jobs refuse, and
publication requires the current positive ticket, no cancellation, successful
conversion and a loaded memo. Worker and law objects compiled with the captured
`ac0f4423` compiler product. The worker is not yet dispatched by the UI.

A subsequent fetch found newer compiler upstream `1a7b0d96648e8007cc7160900c424c1ed7529838`
and engine upstream `a3d756eae40ee9d1228010599ae79f2233007a67`. Preserve local
repairs when integrating these before current qualification; the object compiles
above are diagnostic evidence for their captured older tuple.

Commit `4c597da` adds the original/runtime source-reference policy and 17 laws.
It binds direct GLB identity or an FBX-derived cache to separate original/runtime
paths and raw SHA-256 digests plus importer revision/options. Native file identity
and canonicalization still need to establish those inputs. Session and controller
integration remain open.

The selected compiler checkout merged fetched upstream into `bb274b14`, retaining
project-specific repairs. Reseeding first refused the shared Stage0 product's dirty
build provenance. A clean detached Stage0 checkout at `6f0988a2` was built under
`build/toolchain-stage0-current`; Go records `vcs.modified=false`. The replacement
seed is running with that explicit bootstrap binary. Current qualification waits
for its terminal result and a matching runtime rebuild.

The compiler reseed completed successfully on `bb274b14`: Stage1 SHA-256
`36389f6b18268d4266bd68aacd813c703cd788956b611b9fad9964da11a2aa32`.
The matching runtime rebuilt successfully with SHA-256
`51365ba4a06e13e0af344b5e21790795e15f1b7fbba23c0b5b94b5a52b00ccee`.
FBX worker and policy-law objects compile with this product.

Engine commit `28e6adb` extends the converter to retain one largest supported
skinned mesh and inverse bind matrices alongside the animation hierarchy. Studio
commit `7ecc7f1` registers the converter, parser objects and exact parser pins in
the build inventory/input closure. This is build integration, not yet a working
Open FBX journey. Multiple mesh/material fidelity and native pose correspondence
still need evidence. Exclusive cache staging, original/runtime source integration,
worker dispatch, session reopening and current app rebuild remain open.
