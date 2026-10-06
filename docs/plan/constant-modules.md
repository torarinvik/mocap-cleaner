# Constant module migration

Every module with multiple constants must use actual Elisa `const module`
declarations. Bare members live inside purpose-specific groups; callers use
the group-qualified names. Preserve literal values, visibility, source takes,
contracts and proof coverage. Keep each maintained repository file at most
600 lines and commit each cohesive group separately.

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

Remaining source inventory: **83 owners, 751 ungrouped constants**.

| Module | Ungrouped constants | Declaration files |
| --- | ---: | --- |
| `Balance` | 13 | `src/physics/balance.elisa` |
| `Cli` | 6 | `src/cli/arguments.elisa` |
| `CliOutputGuard` | 6 | `src/cli/output_guard.elisa` |
| `CliOutputGuardPolicy` | 8 | `src/cli/output_guard_policy.elisa` |
| `CliOutputPublisher` | 3 | `src/cli/output_publisher.elisa` |
| `Codec` | 2 | `src/core/codec.elisa` |
| `Fade` | 3 | `src/core/fade.elisa` |
| `Folder` | 3 | `src/io/folder.elisa` |
| `GlbTracks` | 4 | `src/io/glb_tracks.elisa` |
| `Hand` | 4 | `src/core/hand.elisa` |
| `Hinge` | 3 | `src/core/hinge.elisa` |
| `KeyWeight` | 2 | `src/core/key_weight.elisa` |
| `Knee` | 9 | `src/core/knee.elisa` |
| `PerfCache` | 4 | `src/core/perf_cache.elisa` |
| `Physics` | 7 | `src/physics/rig_physics.elisa` |
| `Pivot` | 3 | `src/core/pivot.elisa` |
| `Regress` | 2 | `src/core/regress.elisa` |
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
| `StudioExportReport` | 6 | `src/studio/export_report.elisa` |
| `StudioExportReportPolicy` | 8 | `src/studio/export_report_policy.elisa` |
| `StudioExportResult` | 4 | `src/studio/export_result.elisa` |
| `StudioExportReview` | 13 | `src/studio/export_review.elisa` |
| `StudioExportValidation` | 4 | `src/studio/export_validation.elisa` |
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
| `StudioSourceFingerprint` | 2 | `src/studio/source_fingerprint.elisa` |
| `StudioStorageAccessibilityCopy` | 7 | `src/studio/app/storage_accessibility_copy.elisa` |
| `StudioStorageAgePolicy` | 7 | `src/studio/storage_age_policy.elisa` |
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
| `StudioStorageOverviewPolicy` | 7 | `src/studio/storage_overview_policy.elisa` |
| `StudioStoragePreferencesCodec` | 2 | `src/studio/io/storage_preferences_codec.elisa` |
| `StudioStoragePreferencesFile` | 6 | `src/studio/io/storage_preferences_file.elisa` |
| `StudioStoragePreferencesPolicy` | 4 | `src/studio/storage_preferences_policy.elisa` |
| `StudioStorageReceiptPolicy` | 7 | `src/studio/storage_receipt_policy.elisa` |
| `StudioStorageRegistrationPolicy` | 7 | `src/studio/storage_registration_policy.elisa` |
| `StudioStorageReservedNamespace` | 3 | `src/studio/io/storage_reserved_namespace.elisa` |
| `StudioStorageScanTimePolicy` | 2 | `src/studio/storage_scan_time_policy.elisa` |
| `StudioStorageSelectionPolicy` | 9 | `src/studio/storage_selection_policy.elisa` |
| `StudioStorageTotalsKernel` | 8 | `src/studio/storage_totals_kernel.elisa` |
| `StudioText` | 3 | `src/studio/app/text.elisa` |
| `StudioTextEntryPolicy` | 7 | `src/studio/text_entry_policy.elisa` |
| `StudioTimelineGotoPolicy` | 5 | `src/studio/app/timeline_goto_input.elisa` |
| `StudioView` | 3 | `src/studio/view.elisa` |
| `Timeline` | 9 | `src/studio/timeline.elisa` |
| `Track` | 6 | `src/tools/track_support.elisa` |
| `Window` | 2 | `src/core/window.elisa` |
| `WorkerWaitPolicy` | 4 | `src/io/worker_wait_policy.elisa` |
