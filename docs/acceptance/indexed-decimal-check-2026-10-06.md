# Indexed decimal reader check — 2026-10-06

Authorized command: `CHECK_JOBS=2 PROOF_JOBS=2 sh scripts/check.sh`.
Default products: Stage1 `f292cbe0`, proof assistant `5776350b`, frontend
`f292cbe0`. Log: `build/current-indexed-decimal-check.log`.

The run finished with exit code 1 in session 15179. All 78 existing tests were rebuilt and
executed: 76 returned zero; `studio_file_policy` returned 9 and
`studio_storage_accessibility_policy` returned 14. The workspace owner is
investigating these failures against the new action policies. All four CLI
workflows returned zero: clean/report, batch folder, hands/diff and retime.
The checked native Trash adapter passed. All 507 maintained files were at most
600 lines at startup.

The proof gate failed with regressions and missing reviewed baselines. Product sources changed during this run,
including parser grammar admission and index contracts, so this is diagnostic
coverage and cannot establish acceptance of an immutable current snapshot.
Do not infer decimal edge-case correctness from the existing integer report
fixtures or infer Studio accessibility behavior from policy compilation.
