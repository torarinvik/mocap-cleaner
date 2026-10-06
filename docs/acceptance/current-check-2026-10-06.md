# Current full check — 2026-10-06

Command: `CHECK_JOBS=2 PROOF_JOBS=2 sh scripts/check.sh`.
Log: derived `build/current-full-check.log`.

## Snapshot and completed evidence

- Compiler: current Stage1 `4c409da6`, normal provenance gate.
- Prover: clean strict build `d3a17832`, frontend `4c409da6`.
- Engine: `01f5aec7` on `mocap-track`, includes fetched upstream.
- UI: `8ab2eb39`, includes fetched upstream.
- Native checked-Trash adapter: passed.
- All 78 test executables rebuilt and completed with return code zero.
- CLI application built successfully with the current compiler.

Concurrent suggestion and workspace integration is present in the shared tree.
Affected results require rerunning after those sources change; this evidence
cannot qualify a later whole-tree snapshot. Repository documentation changes
alone do not invalidate executable behavior, but source/dependency changes do.

## Scope limitations and pending results

CLI scenarios and proof gates are still running. No overall green result is
claimed. The existing report-diff fixture covers tolerance, regression, missing
clips, lost status, unreadable files and HTML generation. It does not establish
new malformed/duplicate/type/precision admission cases. Native UI interaction,
workspace adoption and motion preservation acceptance remain open. Prover
nested-enum source witnesses are under repair; stronger law failures remain
visible and proof baselines have not been weakened.
