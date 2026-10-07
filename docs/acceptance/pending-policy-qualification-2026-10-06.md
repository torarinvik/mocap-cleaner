# Pending current-toolchain policy qualification

These edits are implemented but remain open until current compiler/prover
products and independent certificate replay qualify the exact source snapshot.
Existing baselines must not be weakened to admit the edits.

| Slice | Authoritative source/laws | Required remaining evidence |
| --- | --- | --- |
| Recovery action availability | `export_recovery_ui_policy`, matching UI laws | Policy/law replay, full Studio object, disabled pointer/key/AX dispatch |
| Frame dialog keyboard focus | `timeline_goto_focus`, matching focus laws, `app/app_goto`, `app/panels_goto` | Current producer/replay; complete Studio compilation and native Tab/Shift-Tab/Enter/Space, visible focus, pointer field focus and accessibility interaction |
| Contact endpoint editing | `contact_frame_policy`, matching frame laws | No-op and generation refusal replay; exact history/preview preservation |
| Contact endpoint accessibility | `accessibility`, matching accessibility laws | Tree replay, full Studio compile, focus and draft/error announcements |
| Contact pose preview | `contact_preview_policy`, matching preview laws and app integration | Current replay; exact take/document/stack/frame binding; cancel and commit clear transient poses; faithful candidate rendering; measured large-clip evaluation latency and UI responsiveness |
| Numeric input capacity | `text_entry_policy`, matching entry laws | Capacity laws replay, preserved draft at refusal, correction flow |
| Retime target binding | `retime_draft_policy`, `studio_retime_draft_laws` | Current compile/replay; range/band/history changes reject mutation |
| Retime text precision | `state/retime_state` | Current existing fixture compile/run through authorized check; fourth fractional digit refused |
| Typed hand/pivot roles | `core/hand`, `core/pivot`, matching laws | Scalar/typed equivalence replay, full rig consumer compilation and runtime |
| Suggested-preview freshness | `suggestion_policy`, matching policy laws | Missing/stale preview replay, current result rendering, withheld stale evidence |
| Cache arithmetic extraction | `core/cache_budget_arithmetic`, matching laws | Current replay, inherited remaining refusals resolved without lowering baseline |
| Issue explanations | `issue_explanation`, policy and record laws | Typed category/strength and rounded-threshold replay; negative revision refusal; overflow-safe exact frame display replay; full UI compile |
| Finding navigation availability | `issue_browser_policy`, matching browser laws | Fresh/count/action/frame admission replay; stale and empty disabled appearance; pointer/key/AX refusal; invalid selection fallback; final-window bounds; no success state without exact frame jump |
| Typed finding intent | `issue_annotation`, matching annotation laws | Const enum encoding replay; existing fixture compile/run; filter, session save and accessibility integration |
| Export formatted-field capacity | `report_text_policy`, matching text laws and `app/report_text` | Byte/view boundary replay; oversized field or exhausted slots invalidate complete snapshot before GLB publication; no earlier view overwritten; normal full-stack report preserved |
| Batch dry-run admission | `export_batch_preflight_policy`, matching preflight laws | Current replay; native exact path/source/report collision checks; animation/recipe/rig fact capture; queue and UI integration |
| Batch queue lifecycle | `export_batch_queue_policy`, matching queue laws | Current replay; bounded workers and running-count consistency; cancellation drain and explicit resume/retry; exact staged-result review preserved through publication; native create-only outputs and complete manifests; queue UI integration |
| Queue records and transitions | `export_batch_queue`, item/resume policies and matching laws | Replay of validity preservation, item counts, private snapshots, retry/resume and approval retention; native facts bound to exact inputs/results |
| Typed job decisions | `job_policy`, matching job laws | Preserved enum encoding replay; existing fixture through authorized check; actual asynchronous worker commit integration |
| Proof supervisor/cache | `scripts/prove.py` | Timeout, bad exits, partial/corrupt summaries, changed source including cache-only runs, replaced/missing prover binary and parallel progress |

The full proof corpus glob includes new direct source files and all `proof/`
files. New retime-draft, issue-explanation record and cache-arithmetic files currently have no reviewed
rows in `scripts/proof-baseline.tsv`; the new batch-preflight source and laws
also need reviewed rows, as do the contact-preview and batch-queue policies and
laws. This must remain a gate failure until
reports are inspected and independently replayed. Do not substitute historical
candidate counts for current baselines.

The older live full check predates these edits and supervisor/cache changes.
Its eventual result is comparison evidence only. Qualification requires a
coherent source snapshot, verified toolchain manifests and a fresh authorized
check after the live run reaches a terminal state. Compiler diagnostic products
with temporary instrumentation must be identified separately from adoption.

On 2026-10-07 the frame-dialog focus policy compiled with normal compiler
`bb1f4095`. The law-only object had no retained function symbols, so it is
syntax/type evidence only. The dynamic compile-only reproduction
`build/repro/goto_focus_codegen.elisa` emitted `_main` into fresh object
`build/goto-focus-codegen.kTfAr3/focus.o` (exit 0); it was not executed.
The first direct panel compile failed because standalone context omitted
elisa-ui imports; it does not qualify the dialog. Full Studio compilation,
current proof replay and native keyboard/accessibility acceptance remain open.

The frame field now uses a real retained `UiFlat::text_field`, rather than a
button action with a TextField role. Native Change events copy only bounded
digit drafts into the shared modal draft; rejected input restores the prior
retained value. A reentrancy guard separates programmatic synchronization from
foreign edits. Closed controls are hidden/disabled, and dismissal clears modal
focus before attempting to restore the previously retained focus. Focus loss
uses the same dismissal path. Native setter/readback, accessible rejection
feedback, focus announcements and fallback focus still need qualification.

`studio_timeline_goto_input_laws` covers counted extents, missing storage and
ASCII digit admission. Normal `bb1f4095` compiled the law source (syntax/type
evidence), and a dynamic compile-only reproduction emitted `_main` in
`build/goto-input-codegen.QUGNec/input.o` with exit 0. Neither artifact was
executed; current producer and independent replay remain required.

## Integrated compiler diagnosis, 2026-10-07

The source-matched candidate compiler `73319dd1` rejected the full Studio
snapshot at `app/app_pointer_input.elisa:95`: an ignored-result assignment used
a conditional suffix that the parser refused. Commit `f3a4aa0` replaced that
suffix with an explicit nested condition. The next full compile is pending;
this repair alone does not qualify the integrated application.

The uncomposed destination inspector's three backend declines were separately
traced to incorrect enum variant syntax (`Status::Empty` rather than
`Status.Empty`). Corrected policy and main law sources emitted fresh O0 objects
of 147,696 and 159,416 bytes respectively. This is compilation evidence only.
Commit `83d87aa` removed unused report/sheet accessibility imports and used the
Storage policy's existing shared tree sentinel. With verified Stage1 provenance,
the accessibility policy and law graph emitted fresh O0 objects of 256,936 and
263,240 bytes. Independent proof replay, app composition and native interaction
acceptance remain open. These inspector failures do not establish a compiler
module-ownership collision.

The integrated run on frozen app graph `f3a4aa0` reached semantic analysis and
exited 1 without an object. Its 31 diagnostics reported unresolved short
`Geometry` ownership in the sidebar, missing `nul_terminated` in the capture
extension, an expression-scoped optional binding, and a private predicate used
by the global native callback. Root checked the source/product snapshot after
the compiler process disappeared and before editing: the check exited 0. A
later agent check ran after the sidebar repair and correctly detected that edit;
it does not invalidate the earlier terminal snapshot check.

Repairs `f66f666` and `033980b` qualify the sidebar constant owner and expose only
the read-only modal predicate. `51ffbe5` supplies bounded owned native-path
storage with four laws; its fresh O0 law graph is 12,656 bytes with all four law
symbols. `b1bde51` uses that helper, refuses rejected storage before indexing,
and binds the live optional clip in an explicit statement before comparing its
animation to the captured animation ID. The new full compile must qualify these
repairs together. Standalone objects do not establish integrated success, and
the new conversion laws still require independent proof replay.

The current direct native-path report uses proof pair
`8147b64172c74ca5b5f92ba3eb065033`, law SHA-256
`5504f3c05112ac76bbc9c14b42eb590179bf1cf2eeba583fded70bd100c5a134`
and policy SHA-256
`ff5d53ceebb59d6666d13bda7fee72a078475a11316835f24ff6dd9abcf34f2a`.
Both hashes match the inspected source. It reports 45 obligations, 24 proved
and 21 unproven, with 20 unsupported/unknown findings and no counterexample.
Contract calls and function summaries remain unverified; return/termination
ensures and index bounds remain unresolved. An imported `equal` goal also has
one kernel replay gap. This direct report does not qualify the conversion or
its source correspondence. Preserve the full contracts and investigate the
summary/replay boundaries before changing acceptance baselines.

The same proof pair's corrected job-law reports are separate from
`worker_wait_laws`. `studio_job_identity_laws` SHA-256
`0f748c5b0d613cd921fd8b4d3e3edcd72a154fedb7831f8bb8f2d80b1fcaee5a`
reports 36 obligations, 14 proved and 22 findings: 11 unknown ensures, nine
unverified summaries, one unsupported expression and one unsupported contract
call. Its 14 certificates replay internally without gaps.
`studio_job_policy_laws` SHA-256
`01b4e2163fd38e37322579f36756400e0b5106e6f2408c8a9f1c980f92a901e2`
reports 145 obligations, 131 proved and 14 findings: 11 unknown ensures and
three unsupported expressions. Its 131 certificates replay internally without
gaps. The inspected reports are `/tmp/studio_job_identity_laws-8147.json` and
`/tmp/studio_job_policy_laws-8147.json`; source hashes match the current laws.
No counterexample was reported, but neither graph has complete proof or source
acceptance. Internal theorem replay does not discharge unsupported source goals.

The subsequent full Studio run reached the backend and exited 2 without an
object, declining 18 initializers/functions across queue projections, panel
geometry, accessibility and scene operations. App sources changed during this
run, so it supplies diagnostic comparison evidence only. The composed inspector
graph must receive a new stable snapshot and current compiler run after targeted
backend reductions and repairs; this diagnostic result does not qualify it.

## Empty dynamic-array initializer repair

The compiler candidate now records source revision
`4afdce0862bc87cd26566b6016f5553aaf670427`, source-tree SHA-256
`aaef4fd64dbddfb1b2f708d69f08ef98f805fffaf1daf3491b706fdfaf698492`,
build-recipe SHA-256
`eaa161adf4e56aea3a0dd5662b7743f959ed430e701d28226fbd0f5daca7eb46`
and product SHA-256
`61fd208871173f6fea1f0d54848df463f38405def89e2f010536723054f3b7f1`.
The root independently inspected `bin/elisac-stage1.provenance.json`, ran
`python3 scripts/stage1_provenance.py check . bin/elisac-stage1` successfully
in the candidate checkout and recomputed the matching product hash.

The compiler worker reports a subsequent no-bypass seed completed successfully
after the freshness-checker repair, followed by an empty-array reduction with
a 544-byte O0 object and LLVM global `{ ptr, i64, i64 } zeroinitializer`.
It reports nonempty dynamic-array global initialization still refuses with no
object. These reduction observations remain worker-reported until their exact
artifacts are inspected. Compiler-product provenance alone does not establish
linked runtime provenance or qualify the composed Studio graph. Remaining
private-field ownership and call/binary backend declines require separate
reductions and an eventual fixed-snapshot integrated build.

The root subsequently reran both reductions with the verified candidate
product above. `global_empty.elisa` SHA-256
`a55c2efe466b9ef1c7e77b04bf3921a922713b89a2ccb9104866a1816c1da1a5`
compiled at O0 with exit zero to `global_empty-current.o` (544 bytes), with
`_Batch.snapshots` and `_Batch.count_snapshots` symbols.
`global_nonempty.elisa` SHA-256
`8148c0c1dfc2f76e82a5799709588c2dbe1b70016dc7e89bf3d319cd249495a2`
exited 2 with `global initializer snapshots`; the requested
`global_nonempty-current.o` does not exist. Inputs and output paths are under
`build/m5-runtime-origin-candidate/reductions-current/`. These observations
independently establish the narrow compile/refusal behavior; the worker's LLVM
representation observation and integrated application acceptance stay separate.

## Manifest path law compilation

The nine new path-admission and entry-key laws in
`proof/studio_storage_manifest_laws.elisa` compile at O0 into
`build/manifest-path-qualification/laws.o` (224,056 bytes). The command was
`../Elisa-compiler/bin/elisac-stage1 -emit obj -O0 -o build/manifest-path-qualification/laws.o proof/studio_storage_manifest_laws.elisa`.
It exited zero; `nm` contains every new law symbol. The law source SHA-256 is
`0d0d5df938f5510acf4d8b8c43e4d1272dbeb50a44b6067c692cf951ba4ca22d`.
The compiler provenance check passed for source
`bb1f4095e350aa8dcb232a0e56b53c684b44ce2f`, product SHA-256
`203009661b41a4aed677487848d300b7232d0801f76fa19a65222309ffe039a7`.
This compile-only record does not discharge the laws, qualify filesystem
behavior or establish authenticated source correspondence. The final current
proof pair must report those outcomes separately.

## Report model initialization privacy

The compiler worker isolated the `current_status` decline to Studio's external
`global mutable prepared_report_model: StudioExportBatchReportView::Model = zeroed`.
The inspected application declaration is in
`src/studio/app/app_export_batch_warning_review.elisa`; the report model's
status and owned buffers are private in its defining module. A reduction using
the owning module's constructor and accessor succeeds, while an external
zeroed global reproduces the private-field refusal. This distinguishes the
initialization violation from the earlier suspected accessor-owner collision.
The report module's isolated object also does not qualify its external caller.

Repair the application storage through the owning constructor, with explicit
absence/lifetime admission or narrow owner-managed storage APIs. Retain private
fields and the report's bounded ownership and stale-review checks. A complete
integrated compile and native report open/page/close qualification remain open;
making the status public would bypass the diagnosed boundary.

Commit `19e07c7` repairs the application storage to `Model? = null`. Opening
constructs, loads and validates a local model through the owning module, then
moves it into storage; closing releases it to null. Owner-side optional status
and page-count APIs return Empty/0 for absence. Paging, draw, accessibility and
acknowledgement callers use those APIs or a guarded borrow. Previous is disabled
for absent or stale page state. The private cache reads the validated immutable
model without revalidating up to 1 MiB on every page change.

The worker's focused O0 products are `build/report-model-optional/report-view.o`
(57,640 bytes) and `report-laws.o` (77,360 bytes). The root inspected those
sizes and confirmed both absence-law symbols in the law object. This records
source implementation and focused compilation, not complete application or
proof qualification. The cached-valid flag's relationship to the model's
immutable open/close lifetime still needs contract/source-correspondence
evidence, alongside native report open/page/close and acknowledgement checks.

The integrated run for `9bd6700` recorded 528 inputs in
`build/report-model-optional/full-studio-9bd6700/inputs-before.json`. The root
initially rehashed every input successfully, then detected an external change
to `elisa-ui/src/core/ui_paint.elisa` while compiler PID 49071 was still active.
The application sources remained unchanged. This run may supply terminal
diagnostics, but cannot qualify its original snapshot, even if the UI change
is later reverted. Preserve that mismatch and inspect the post-run manifest
before repairs. Prepare the next compilation from a verified immutable copy
of the complete source/include graph and linked inputs; shared-checkout edits
must not silently change the compiled generation or its provenance.

## Path measurement callback ownership boundary

The adapter worker reported that an explicit `WidthMeasure` callback with
`Unsafe.PointerCast` invalidates the region facts needed by later path/model
accesses. The adapter's `UiText::unsafe_sview_bounded_bytes` introduces the same
boundary. A generic caller region and output parameter did not resolve the
refusal. This is a reported diagnostic observation; the adapter is uncomposed
and no successful adapter compilation or native qualification is recorded.

Investigate a safe owned or fixed-buffer text-view API and preserve the current
effect checks. Any required UI/compiler repair must establish exact retained
bytes and buffer lifetimes, alongside the separate checked-width validity gate.
Do not make unsafe callbacks appear safe by dropping their declared effects.

## Isolated integer length conversion

Commit `dd3e296` adds `LengthUnits` and ten laws without composing the module
into existing callers. Micrometres convert to 0.1 mm with nearest rounding,
half ties away from zero, using division/remainder before adjustment. Reverse
conversion admits exactly the i64-safe multiplication range. Laws cover both
i64 extrema, signed ties, exact units, reverse refusal and the 50 micrometre
round-trip error bound. Angular and current physical callers are unchanged.

The source SHA-256 is
`d61b44c18d73c6af5eabf97343e98ef0fe46d7ff69619f49db80dae2c92d3e8e`;
the law SHA-256 is
`1448ee5b4fad32951519d5af930773937a42ad2892e6a69d8248eb5ffe659c2a`.
The current normal compiler provenance check passed; an O0 compile of the law
graph exited zero and emitted `build/length-units-qualification/laws.o`,
18,608 bytes, SHA-256
`b4d2cadf71576366b4578daa70e922fb04e72ad6b18016c162c24ac0e88fb3b3`.
`nm` lists all three kernel and ten law definitions. This establishes compiled
source only: authenticated proof, overflow qualification, caller migration,
threshold behavior and exported-metric compatibility remain open.

Commit `820a963` strengthens the converter's own contracts with sign
preservation and the signed 50 micrometre reconstruction error bound; the law
graph now has twelve laws. Current source/law SHA-256 values are respectively
`088b16fc58a7796eff6777a8dce956e50cb90d8c4da0dc3fdf5334fcd411d9b1`
and `ef51d53dc586bcee7918b0b801070394280f65accb679e3e90845d31812d2240`.
Its O0 compile exited zero, producing `laws-contracted.o` (26,352 bytes),
SHA-256 `7cb461382834dc192cb8826220766aac1a4375299fb36ccc9508b10628632864`
in the same build directory. The preceding generation remains comparison
evidence; proof qualification must use these current source hashes.

## Immutable integrated input staging

The compiler worker staged `build/report-model-optional/immutable-20261007`
with project/UI/engine sibling layout and the exact candidate compiler source,
binary, standard library and runtime inputs. The root independently compared
original before/after inventories (equal), rehashed all 529 staged manifest
entries (zero mismatches), and mapped staged paths back to original sibling
roots (all 529 hashes match). The graph includes `ui_paint_diagnostic.elisa`.
This establishes staging consistency only. Preserve explicit standard-library
root selection and verify the staged manifest after compilation before treating
the eventual product as qualification evidence.

The original comparison run (worker session 40404, PID 49071) terminated with
exit 2 and no object. The worker reported 23 backend declines spanning export
batch/report/destination calls, destination accessibility, a sheet field
expression and camera/navigation binary expressions. The empty-global and
external report-zeroed declines were absent from this diagnostic set, but that
does not qualify their integrated repairs. The post-run check refused publication;
the worker's detailed comparison records identify changed `ui_paint.elisa` and
added `ui_paint_diagnostic.elisa` as the input drift. Keep this generation as
comparison evidence. The staged generation has begun a separate compilation
with its standard-library root explicitly set inside the immutable copy.

The staged compilation (worker session 11768, PID 31225) terminated with exit
2, no object and the same 23 backend declines. Its post-run snapshot check
exited zero. The root independently rehashed all 529 entries in the staged
`mocap-cleaner/build/studio-immutable/inputs-before.json` after termination:
zero mismatches. This is a source-matched diagnostic failure, not a successful
application qualification. Preserve the staged generation while repairing the
compiler using minimal reductions. The final app compilation requires a new
immutable generation containing the later constant migrations and checked text
measurement API; this older snapshot cannot qualify those changes.

## Current migrated law graphs and compiler freshness

The normal compiler at `bb1f4095` subsequently acquired external backend WIP;
its product provenance now refuses a source-tree mismatch. Preserve that WIP
and do not use the old product to qualify the current normal checkout. Earlier
normal-compiler object records are generation-specific comparison evidence.

The root fetched the candidate compiler's origin successfully and checked
source/product provenance before and after a fresh compile-only batch using
candidate `4afdce08` (product SHA-256
`61fd208871173f6fea1f0d54848df463f38405def89e2f010536723054f3b7f1`).
All fifteen current law graphs compiled O0 with nonempty objects. The batch
captured 173 inputs, including resolved literal includes, candidate standard
library, binary, runtime object and provenance file; before/after hashes had
zero drift. Results and exact leaf-source hashes are retained in
`build/constant-qualification-current-candidate/compile-report.json` with input
inventories alongside. The standard-library root was explicitly selected from
the candidate checkout. This is compile evidence, not authenticated proof,
native execution or complete linked application qualification.

The matched prover build using the stale normal checkout refused publication
at its provenance gate. Its replacement uses the verified candidate product
and co-located runtime; acceptance still requires the resulting generation's
exact source/product identities and successful replay/correspondence reports.

## Stack, contact and session constant domains

Commits `83ccdfb`, `eefd8c6` and `951d0ef` separate stack/contact capacities
and limits into const modules, and contact sides, editing actions, nudge
targets and session save/load outcomes into const enums. Session wire tags
remain an extensible const module: unknown tags are still permitted by the
existing reader policy. Integer boundaries preserve all previous values.
Existing fixture references were updated; fixtures were not executed.

The verified candidate compiler compiled the current domain law graphs O0:

| Law graph | Object bytes |
| --- | ---: |
| studio_stack_constant_domain_laws | 1,393,040 |
| studio_contact_editor_domain_laws | 47,120 |
| studio_contact_editor_laws | 65,088 |
| studio_contact_nudge_laws | 50,352 |
| studio_session_constant_domain_laws | 2,111,640 |

Objects are in `build/constant-qualification-current-candidate/`. These
additional compiles are outside the earlier fifteen-graph input manifest.
They establish compilation only; authenticated discharge, full application
integration and runtime persistence behavior remain required. The maintained
text length check now covers 780 files, all at most 600 lines.

## Final grouping inventory and context-specific compilation

Commits `0098790`, `cf085bf`, `322fea7` and `6140bca` migrate role indices,
private application constants, accessibility IDs/ranges and panel action codes.
The lexical inventory now reports zero ordinary module scopes requiring review.
The maintained text length check covers 781 files, all at most 600 lines.
These results do not establish complete representation or behavior acceptance.

Current candidate O0 compilation produced role laws (62,560 bytes), rig
selection laws (919,968 bytes) and panel constant-domain laws (4,232,040 bytes).
The panel proof graph requires explicit UiCore/UiText imports; its initial
missing-import attempt failed and supplied no acceptance evidence.

The focused accessibility graph compiled. The wider export batch-sheet graph
refused 25 bodies with field-expression diagnostics involving accessibility
constants and emitted no object. Renaming the ID const module to SemanticId
did not resolve the failure. The compiler worker has this context-specific
failure for reduction; module ownership is not yet established as its cause.
Current full application and authenticated proof qualification remain open.

The accessibility sheet failure was reproduced at root `182f7ef` against
candidate `4afdce08` with the candidate standard library explicitly selected.
The full Studio input snapshot check before/after compilation passed with no
drift. Compilation exited 2, declined the same 25 bodies and emitted no object.
Exact input inventory, failure log and result metadata are retained under
`build/accessibility-domain-qualification/`. This is source-matched diagnostic
evidence; it does not qualify the application or establish the failure's cause.

## Accessibility dependency repair

Commit `1183b87` resolves the preceding 25 field-expression declines by
declaring accessibility.elisa's direct UiCore dependency. Its NO_NODE constant
uses UiCore::MAX_ACCESSIBILITY_NODES. The focused law graph supplied UiCore
explicitly, whereas the wider sheet graph did not; this was a missing source
dependency, not an established compiler ownership collision.

A fresh candidate O0 batch after the repair produced sheet laws (638,048
bytes), report laws (544,656 bytes) and workspace accessibility laws (434,248
bytes), all exit 0. Full input snapshot comparison passed with no drift.
Repaired inventories, logs and results are retained in
`build/accessibility-domain-qualification/`. Independent source-authenticated
proof replay and native accessibility behavior remain required.

## Current full-check entry gate

At root `664d738`, the authorized `bash scripts/check.sh` invocation passed
file lengths (782 files), owner-aggregated constant inventory (zero findings)
and consecutive literal-push checks (zero findings). It exited 2 at the prover
freshness gate: the selected prover is stale relative to current proof source.
The test suite did not execute. Re-run the full check only with the resulting
source-matched proof-tool generation and compiler dependencies; this refusal
is not a passing test result or a reason to bypass provenance.
