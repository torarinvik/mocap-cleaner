# Constants and finite choice migration

Audit each existing/new group for its best domain representation. Use a
`const enum` for a closed set of alternatives, an algebraic data type for
cases with distinct payloads or invalid combinations, and a `const module`
for related numeric limits, units or configuration values. A completed grouping
still requires reassessment when a stronger type fits its meaning.

Preserve visibility, source takes, contracts and proof coverage. Keep every
maintained file within 600 lines and commit each cohesive migration separately.
For serialized/native integer codes, validate explicit encode/decode functions
and preserve required wire values; unknown codes must not become success or
another valid case. Cover all variants, invalid boundary input, round-trip
conversion and public/private API scope in the contracts/proofs. Do not assume
that equal discriminant values alone prove behavior preservation.

## Verification requirements

Qualify each constant group and its source, proof and test consumers with
current compiler/prover provenance. Preserve literal values and visibility;
require independent certificate replay and retain existing proof expectations.
The current prover supports nested and lexical relative constant paths; G96
records the repair and qualification evidence.

## Remaining groups (2026-10-06)

The extra proof/test groups have been migrated: `KneeLaws::Domain` holds
its public geometry aliases, and the shortcut fixture uses `KeyEvent` for
its six event codes. Other audited proof/test owners have one constant each.
No Elisa fixture files were found under `scripts/`.

Counts describe ungrouped module-scope declarations; extension files are
counted under their owning module. Single-constant modules need not be
extracted solely for this rule. Group public and private constants separately
when their visibility differs. Split values by purpose rather than collecting
unrelated limits, actions and filesystem facts in one bag.

The remaining source groups are listed below; historical totals are omitted
because incremental migrations change the inventory.
File-level export publisher limits, outside this module-owner inventory, now
use private `StudioExportPublisher::Capacity` (path and staging buffer sizes).
Numeric capacities remain a const module; typed validation outcomes use an enum.

| Module | Ungrouped constants | Declaration files |
| --- | ---: | --- |
| `Balance` | 13 | `src/physics/balance.elisa` |
| `Cli` | 6 | `src/cli/arguments.elisa` |
| `CliOutputGuard` | 6 | `src/cli/output_guard.elisa` |
| `CliOutputGuardPolicy` | 8 | `src/cli/output_guard_policy.elisa` |
| `CliOutputPublisher` | 3 | `src/cli/output_publisher.elisa` |
| `GlbTracks` | 4 | `src/io/glb_tracks.elisa` |
| `Hand` | 4 | `src/core/hand.elisa` |
| `Hinge` | 3 | `src/core/hinge.elisa` |
| `Knee` | 9 | `src/core/knee.elisa` |
| `PerfCache` | 4 | `src/core/perf_cache.elisa` |
| `Physics` | 7 | `src/physics/rig_physics.elisa` |
| `Pivot` | 3 | `src/core/pivot.elisa` |
| `Retime` | 8 | `src/core/retime.elisa` |
| `RigOps` | 9 | `src/ops/rig_hands.elisa`, `src/ops/rig_legs.elisa`, `src/ops/rig_schema.elisa` |
| `Roles` | 31 | `src/core/roles.elisa` |
| `SessionIssueAnnotationPolicy` | 4 | `src/studio/state/session_issue_annotation_policy.elisa` |
| `SessionState` | 20 | `src/studio/state/session_state.elisa` |
| `Slide` | 3 | `src/core/slide.elisa` |
| `StackCache` | 3 | `src/core/stack_cache.elisa` |
| `StackPolicy` | 2 | `src/studio/stack_policy.elisa` |
| `StackState` | 8 | `src/studio/state/stack_state.elisa` |
| `Studio` | 11 | `src/studio/app/app_state.elisa` |
| `StudioAccessibility` | 46 | `src/studio/accessibility.elisa` |
| `StudioCharacterBind` | 5 | `src/studio/character_bind_policy.elisa` |
| `StudioChrome` | 24 | `src/studio/chrome.elisa` |
| `StudioContactEditor` | 15 | `src/studio/contact_editor.elisa` |
| `StudioContactFramePolicy` | 3 | `src/studio/contact_frame_policy.elisa` |
| `StudioDraw` | 93 | `src/studio/app/panels_geometry.elisa` |
| `StudioExportPathReview` | 5 | `src/studio/export_path_review.elisa` |
| `StudioExportPolicy` | 7 | `src/studio/export_policy.elisa` |
| `StudioExportReview` | 13 | `src/studio/export_review.elisa` |
| `StudioFilePolicy` | 9 | `src/studio/file_policy.elisa` |
| `StudioIssueAnnotation` | 3 | `src/studio/issue_annotation.elisa` |
| `StudioIssueBrowserPolicy` | 17 | `src/studio/issue_browser_policy.elisa` |
| `StudioLegacyPrompt` | 6 | `src/studio/legacy_session_prompt.elisa` |
| `StudioModel` | 9 | `src/studio/app/model.elisa` |
| `StudioOverlay` | 7 | `src/studio/overlay_policy.elisa` |
| `StudioReplacement` | 8 | `src/studio/replacement.elisa` |
| `StudioResetScope` | 4 | `src/studio/reset_scope.elisa` |
| `StudioRetime` | 5 | `src/studio/app/retime_panel.elisa` |
| `StudioScene` | 13 | `src/studio/app/scene.elisa` |
| `StudioShortcuts` | 13 | `src/studio/shortcuts.elisa` |
| `StudioSidebarLayout` | 28 | `src/studio/sidebar_layout.elisa` |
| `StudioStorageAccessibilityCopy` | 7 | `src/studio/app/storage_accessibility_copy.elisa` |
| `StudioStorageArtifactDestination` | 4 | `src/studio/io/storage_artifact_destination.elisa` |
| `StudioStorageBatchPolicy` | 18 | `src/studio/storage_batch_policy.elisa` |
| `StudioStorageCleanupPolicy` | 22 | `src/studio/storage_cleanup_policy.elisa` |
| `StudioStorageExemptionPolicy` | 4 | `src/studio/storage_exemption_policy.elisa` |
| `StudioStorageExemptionsCodec` | 14 | `src/studio/io/storage_exemptions_file.elisa` |
| `StudioStorageExemptionsWirePolicy` | 2 | `src/studio/io/storage_exemptions_wire_policy.elisa` |
| `StudioStorageManifest` | 8 | `src/studio/io/storage_manifest.elisa` |
| `StudioStorageManifestLockFile` | 4 | `src/studio/io/storage_manifest_lock_file.elisa` |
| `StudioStorageManifestLockPolicy` | 5 | `src/studio/storage_manifest_lock_policy.elisa` |
| `StudioStorageMovePolicy` | 24 | `src/studio/storage_move_policy.elisa` |
| `StudioStoragePreferencesCodec` | 2 | `src/studio/io/storage_preferences_codec.elisa` |
| `StudioStoragePreferencesFile` | 6 | `src/studio/io/storage_preferences_file.elisa` |
| `StudioStoragePreferencesPolicy` | 4 | `src/studio/storage_preferences_policy.elisa` |
| `StudioStorageReceiptPolicy` | 7 | `src/studio/storage_receipt_policy.elisa` |
| `StudioStorageRegistrationPolicy` | 7 | `src/studio/storage_registration_policy.elisa` |
| `StudioStorageReservedNamespace` | 3 | `src/studio/io/storage_reserved_namespace.elisa` |
| `StudioStorageSelectionPolicy` | 9 | `src/studio/storage_selection_policy.elisa` |
| `StudioText` | 3 | `src/studio/app/text.elisa` |
| `StudioTextEntryPolicy` | 7 | `src/studio/text_entry_policy.elisa` |
| `StudioTimelineGotoPolicy` | 5 | `src/studio/app/timeline_goto_input.elisa` |
| `StudioView` | 3 | `src/studio/view.elisa` |
| `Timeline` | 9 | `src/studio/timeline.elisa` |
| `Track` | 6 | `src/tools/track_support.elisa` |

Export-result actions migrated to `StudioExportResult::Action`; policy/laws
retain 7/7 and 16/16 proved results. Existing test compilation is pending a
provenance-valid Stage1 product after the external compiler source edit.

`Window::Domain` groups frame, radius and reflection-magnitude bounds. These
are numeric domain limits rather than alternatives. Source contracts, laws,
track consumers and the existing fixture use qualified constants with unchanged
values. Current compiler `3c72f59f` emits a fresh source object;
focused proof evidence is recorded separately without lowering the baseline.
`StudioSourceFingerprint::Residue` already groups both residue moduli and has
been removed from the remaining inventory.

`WorkerWaitPolicy::Action` represents Retry, Reaped and Failed as a closed enum;
`Posix::EINTR` keeps the platform errno fact separate. Values and wait behavior
are unchanged. Current independent replay has two unresolved law gaps; retain
the existing complete law baseline until they are resolved. Normal compiler
`3c72f59f` emits a fresh policy object; native adapter qualification remains open.

`Codec::Domain` holds decimal field magnitude and serialized operation-kind
count. These numeric format bounds are not choices; operation variants remain
the responsibility of the operation schema. Their values are unchanged.
Compilation and proof replay await current toolchain products.

`Regress::Domain` groups the bounded metric magnitude and maximum permille
tolerance. All law consumers use the qualified names; numeric values and
regression behavior are unchanged. Current compilation/replay remain pending.

`Folder::DarwinDirent` privately groups native directory-record layout limits.
These ABI offsets are platform-specific numeric facts, not alternatives for an
enum. The current folder reader remains Darwin-specific; cross-platform batch
work must use a qualified host directory service rather than assuming this ABI.

`KeyWeight::Domain` groups the full permille weight and bounded frame domain.
Correction and law consumers use qualified values; numeric behavior is unchanged.
These numeric limits remain a const module rather than an enum.
Current compiler `4c409da6` accepts the weight source. Prover `d3a17832` proves
and replays source 36/36 and laws 60/60, with zero gaps. Correction executable
qualification must be rerun after this consumer change.

Codec follow-up with current prover `d3a17832`: source 50/50 obligations and
certificates replayed, zero gaps; laws 71/74 replayed with three gaps and no
producer findings. Law replay remains open; source success is not a substitute.

`Fade::Domain` groups full permille weight, frame bound and edge-window bound.
All source/law consumers use the qualified values. Current prover `d3a17832`
replays source 103/103; laws replay 147/150 with three gaps and no producer
findings. The prior 150-obligation law baseline is retained, not weakened.
