# Compiled export build-input identity

Studio builds now generate `build/generated/studio_build_identity.elisa` as a
constant module before compilation. The generator first checks Stage1 product
provenance. It records full Git revisions and dirty-worktree flags for Studio,
engine, UI and compiler, plus SHA-256 hashes of the actual compiler product and
linked runtime object. The generated file and generator participate in bundle
input fingerprinting.

Export snapshots extend their settings with these compiled constants before
GLB publication. They never query later Git state. JSON and text unavailable
provenance descriptions now distinguish partial build-input evidence from a
complete application/dependency manifest. Report assumptions explicitly state
that a dirty revision is not an exact source identity.

The first compile/package run passed on normal f292cbe0 in session 61851. A
subsequent run after adding the pre-generation provenance check terminated
with exit two in session 12782: the backend declined
`save_session_to_current_path@37` in concurrent session-save work and did not
write an object. The session owner has the diagnostic. The current
`build/export-build-identity-studio-build.log` records both provenance checks
and that failure, rather than the earlier successful compile/package output.
Generated values identify compiler f292cbe0, engine 01f5aec7 and UI 8ab2eb39,
all clean at capture, with the project dirty. The compiler hash is
`5a6c3f32668295ca8786ca0892c1fab56db44457f6b6d2e9b8e4236156a431c6`;
runtime hash is
`b51e6114f0576681e432e1162a3dbdcdac46c140d3b7e7256c0069be0bd11897`.

Existing report formatting laws remain open: 41 obligations, 38 proven,
35 independently replayed, three replay gaps, three findings and zero semantic
diagnostics (`build/export-build-identity-report-laws.log`). No baseline was
weakened and no executable tests were added. Generated fields have not been
observed in a native exported report yet.

This metadata does not establish immutable source provenance when files change
during compilation. Revisions/dirty flags cannot replace exact source tree
hashes, dependency closure manifests or source/output byte authentication.
Native export observation, deterministic report behavior and complete M6
provenance qualification remain unfinished.
