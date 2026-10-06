# Pending current-toolchain policy qualification

These edits are implemented but remain open until current compiler/prover
products and independent certificate replay qualify the exact source snapshot.
Existing baselines must not be weakened to admit the edits.

| Slice | Authoritative source/laws | Required remaining evidence |
| --- | --- | --- |
| Recovery action availability | `export_recovery_ui_policy`, matching UI laws | Policy/law replay, full Studio object, disabled pointer/key/AX dispatch |
| Contact endpoint editing | `contact_frame_policy`, matching frame laws | No-op and generation refusal replay; exact history/preview preservation |
| Contact endpoint accessibility | `accessibility`, matching accessibility laws | Tree replay, full Studio compile, focus and draft/error announcements |
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
| Proof supervisor/cache | `scripts/prove.py` | Timeout, bad exits, partial/corrupt summaries, changed source including cache-only runs, replaced/missing prover binary and parallel progress |

The full proof corpus glob includes new direct source files and all `proof/`
files. New retime-draft, issue-explanation record and cache-arithmetic files currently have no reviewed
rows in `scripts/proof-baseline.tsv`; this must remain a gate failure until
reports are inspected and independently replayed. Do not substitute historical
candidate counts for current baselines.

The older live full check predates these edits and supervisor/cache changes.
Its eventual result is comparison evidence only. Qualification requires a
coherent source snapshot, verified toolchain manifests and a fresh authorized
check after the live run reaches a terminal state. Compiler diagnostic products
with temporary instrumentation must be identified separately from adoption.
