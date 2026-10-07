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
The accessibility law graph, independent proof replay, app composition and
native interaction acceptance remain open. These inspector failures do not
establish a compiler module-ownership collision.
