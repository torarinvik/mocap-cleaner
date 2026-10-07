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
