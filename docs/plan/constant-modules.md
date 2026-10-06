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
| `Knee` | 9 | `src/core/knee.elisa` |
| `Physics` | 7 | `src/physics/rig_physics.elisa` |
| `RigOps` | 9 | `src/ops/rig_hands.elisa`, `src/ops/rig_legs.elisa`, `src/ops/rig_schema.elisa` |
| `Roles` | 31 | `src/core/roles.elisa` |
| `SessionState` | 20 | `src/studio/state/session_state.elisa` |
| `StackState` | 8 | `src/studio/state/stack_state.elisa` |
| `Studio` | 11 | `src/studio/app/app_state.elisa` |
| `StudioAccessibility` | 46 | `src/studio/accessibility.elisa` |
| `StudioContactEditor` | 15 | `src/studio/contact_editor.elisa` |
| `StudioExportPathReview` | 5 | `src/studio/export_path_review.elisa` |
| `StudioExportPolicy` | 7 | `src/studio/export_policy.elisa` |
| `StudioExportReview` | 13 | `src/studio/export_review.elisa` |
| `StudioFilePolicy` | 9 | `src/studio/file_policy.elisa` |
| `StudioIssueAnnotation` | 3 | `src/studio/issue_annotation.elisa` |
| `StudioIssueBrowserPolicy` | 17 | `src/studio/issue_browser_policy.elisa` |
| `StudioLegacyPrompt` | 6 | `src/studio/legacy_session_prompt.elisa` |
| `StudioOverlay` | 7 | `src/studio/overlay_policy.elisa` |
| `StudioPanels` | 47 | `src/studio/app/panels_geometry.elisa` |
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
| `Track` | 6 | `src/tools/track_support.elisa` |

`StudioText::Buffer` now groups slots, width and capacity; its static buffer and
fixed-view generic use the qualified capacity. `StudioView::Coordinate`,
`Curve` and `Severity` separately group pixel bound, curve magnitude and
level count. Source contracts, view laws, curve-panel consumers and the
existing Studio fixture use qualified constants with unchanged values.
No proof law or baseline was removed. Normal Stage1 `bb1f4095` emitted fresh
compile-only objects for the Text and View sources, view laws and existing
Studio fixture; independent proof replay and native Studio qualification
remain open.

`StudioChrome` now models Escape layers, screens and parameter units as explicit
stable-code enums; frame, gain, session and correction bounds use separate
const modules. `Timeline` groups domain, clock and duration limits and
represents the three playback divisors as a stable-code enum. Consumers,
laws and fixtures use the new paths with unchanged numeric values.
`StudioIcons::Icon` records the generated icon codes as an enum; icon sizing,
panel layout, panel capacities and menu dimensions have purpose-specific
groups. The old `StudioDraw | 93` inventory row was misattributed: that file
declares `StudioIcons` and `StudioPanels`, while `StudioDraw` itself has no
constants. `StudioPanels` has 47 remaining ungrouped constants.
Normal Stage1 `bb1f4095` (seed 13359) produced compile-only objects for Chrome
and Timeline sources/laws and the existing session, units and capacity fixtures;
these are not proof-certificate replay or native Studio acceptance. The
full panel/app compile and native UI qualification remain open.

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

`StackCache::Capacity` holds the operation bound; `Fingerprint` holds the seed
and modulus. These numeric parameters are distinct from semantic operation
choices, which retain their typed representation. All cache/law consumers use
qualified names. Compiler `3c72f59f` accepts the existing performance fixture;
candidate prover `4da37c97` reports source 78/78 and laws 165/166, with all 165
law certificates replayed. The existing unresolved law and baseline are retained.

`PerfCache::Layout` holds the bank stride and `Capacity` holds track/frame
bounds. Source/law/runtime consumers use qualified paths. The GLB channel
consumer now uses `Slot.Unavailable` / `Slot.Available(index)` through
`select_slot`; invalid dimensions choose full evaluation. The integer `slot`
API and its sentinel remain for existing boundary consumers and established
laws. Admission has a scalar contract and three new laws. Current compiler
`720896f4` emits a fresh GLB adapter object at
`build/typed-slot-compile.KaZEXO/tracks.o`. Proof replay and cached/full runtime
qualification remain open; this compile-only result does not close them.

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

`Hinge::Angle` groups micro-radian turn constants; `Domain` holds the
numeric rotation magnitude bound. Consumers use qualified names with unchanged
values. Existing laws compile with current compiler `720896f4`; replay and
full rig adapter qualification remain open.

`Slide::Domain` groups frame, median radius and sorted-search bounds. Source,
filter adapter and laws use qualified constants with unchanged values. Compiler
`720896f4` emits `build/slide-domain.MfooxL/laws.o`. Candidate `4da/720`
reports source 51/51 and law corpus 269/272, all produced certificates
replayed without gaps. The three refusals are included `Window::middle`
obligations at the budget gate. This is comparison evidence, not full runtime
or corpus qualification; existing proof expectations remain intact.

`Retime` now separates `TimeScale`, `Rate`, `Domain` and `Defaults`. All
source, law and existing fixture consumers use qualified names; values and
visibility are preserved. Compiler `720896f4` emits the combined performance
fixture at `build/retime-domains.epX7Rj/fixture.o`. Proof replay and runtime
qualification remain open; existing baselines were not changed.

`Hand::Domain` holds its geometry bound and `Defaults` its minimum run.
`Role.Left` / `Role.Right` are a closed const enum with preserved integer
values 9 / 13; existing integer role boundaries use explicit `.i64()`
conversions. All source, law and fixture consumers were migrated. Current
compiler and proof qualification remain pending.
Compile-only qualification with current compiler `1f136742` emitted
`build/hand-role-compile.NGRICE/hands.o` from the existing hands fixture.
The fixture was not executed; proof replay and rig integration remain open.

`Pivot::Point` represents Heel/Ball with preserved codes 0/1; `Domain`
holds the numeric magnitude bound. The rig uses typed retained choices and
`choose_point`, which has an equivalence contract with the existing integer
kernel. Existing scalar laws retain that kernel and explicit enum conversions;
a new law covers typed equivalence. Compile qualification is pending because
the compiler source changed and its provenance guard rejected the prior binary.
No stale-product override was used; proof expectations remain unchanged.

`StudioContactFramePolicy::Endpoint` replaces loose First/Last codes with
closed alternatives, preserving codes 0/1 through explicit integer boundary
conversions. `Domain` holds the frame limit. Source, proof and fixture consumers
retain existing invalid-target rejection and atomic invalid-draft behavior.
Current compile/replay qualification awaits the compiler rebuild.

`StudioTextEntryPolicy::Character` groups ASCII encoding facts; `Capacity`
holds the numeric draft limit. The rejection sentinel remains a single integer
boundary value. Capacity admission has a contract and three laws; a refused
append preserves the draft and displays correction/cancellation guidance.
Compiler/replay and native input qualification await current products.

Issue explanation `Category` and `Level` are now closed const enums, and the
explanation record carries these types. Existing discriminant values remain
0/1 and 0/1/2. The external detector code remains a separate encoding fact;
unknown detector codes still produce the generic category. Matching laws and
fixture consumers were migrated, with mild/strong threshold laws added.
Current compiler/replay qualification remains pending.

Finding intent now uses `StudioIssueAnnotation::Disposition` with Unresolved
and Ignored alternatives. The filter's integer interface receives an explicit
conversion; discriminants remain 0/1, covered by two encoding laws. `Capacity`
owns the annotation bound. Existing fixture consumers were migrated without
execution. Current compile, replay and session/filter qualification remain open.

`StudioIssueBrowserPolicy` now separates navigation `Action` as a const enum,
`Capacity` limits and `Accessibility` node identifiers. Previous/Next/Worst
retain codes 0/1/2 at existing integer routing boundaries, with an encoding law.
Source, laws and existing fixtures use the scoped facts; current compile and
replay qualification remain open.

Finding-filter `Disposition` now represents Unresolved/Ignored/Any as a const
enum with preserved codes 0/1/2. The raw filter-validation interface retains
integer status so malformed stored values can be refused explicitly. Consumers
convert the named alternatives at that boundary. The encoding law and existing
fixture emitted fresh diagnostic objects in `build/filter-disposition-compile.QbizwZ`
and `build/filter-disposition-compile.RQTe4c`. Replay, fixture execution and full
application qualification remain pending.

`SessionIssueAnnotationPolicy::Capacity` groups the annotation record bound,
and `Domain` groups severity/frame validation bounds. The independently
versioned analysis schema remains one public constant. Literal values and wire
schema are unchanged. Normal `bb1f4095` compiled the policy and law sources
(syntax/type evidence) and emitted a fresh nonempty object for the existing
`studio_session_annotations` fixture under `build/annotation-bound-compile.*`.
The fixture was not executed; current proof/replay and full Studio acceptance
remain required.

`StackPolicy::Limit` groups the editable operation/frame domain bounds. All
source, law and existing fixture references use the qualified paths; values
remain 16 operations and 10,000,000 frames. Normal `bb1f4095` emitted a fresh
object for the existing `studio_duplicate_operation` fixture in
`build/stack-limit-compile.*`; source/law compilation also completed. These
objects were not executed. Current proof/replay and full Studio qualification
remain open.

`StudioCharacterBind::Mode` now represents Direct, Inherited and Rest as a
closed const enum throughout the binding arrays, consumer and existing fixture.
`Coverage` groups the permille scale and minimum drawing coverage. Existing
binding laws return the typed enum and compile at O0 to a fresh 37,152-byte
object. The inherited pose consumer validates the ancestor index before
indexing the public binding arrays. The existing fixture was updated for the
API and was not executed. Current proof replay and integrated/native character
qualification remain open. Four unused StudioModel track constants were removed;
its remaining numeric values now live in purpose-specific `Support`, `Correction`
and `Wring` const modules, preserving their public visibility and values. Existing
capture/correction fixture consumers use the qualified names; they were not run.

The character consumer emitted a fresh 2,572,928-byte O0 object before the model
constant grouping. The two explicit negative/end ancestor boundary laws also
compile with retained symbols in a fresh 39,320-byte law object. These are
compile-only evidence, not proof replay or native character acceptance.

After grouping, `StudioModel` emitted a fresh 2,385,776-byte O0 object with
`balance_of`, `correction_for` and `nudge` retained. The selected normal compiler
passed its source/binary/runtime provenance check. All four dependency origins
were fetched again; local compiler, prover, UI and engine repairs were preserved.
This does not close current proof replay, existing fixture execution or the full
native application gate.
