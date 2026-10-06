# Dependency freshness audit — 2026-10-06

Fetched `origin` in each checkout before comparing `HEAD...origin/main`.
Counts describe committed ancestry, not working-tree or binary qualification.

| Dependency | Local HEAD | Fetched upstream | Ahead / behind | Status |
| --- | --- | --- | --- | --- |
| Compiler | `812c0547` | `72a75282` | 31 / 0 | Clean source; normal Stage1 wrapper reports current `812c0547`. |
| Primary proof assistant | `151a2772` | `151a2772` | 0 / 0 | Active uncommitted work preserved; not adopted as committed upstream. |
| Mocap engine | `bc98339e` | `7699ec52` | 18 / 138 | Merge required on `mocap-track`; workspace host files preserved. |
| Elisa UI | `8ab2eb39` | `dc6cd397` | 6 / 0 | Clean source, includes all fetched upstream commits. |

The mocap proof assistant is merging committed primary `151a2772`, retaining
its cleaner fixes and aligning its frontend pin with current compiler `812c0547`.
Its new build and proof replay are not yet qualified. Engine integration is
assigned to the workspace host implementation owner to avoid conflicting edits.

Repeat the fetch/ancestry audit before final snapshot acceptance. Rebuild and
rerun affected verification after dependency changes. A clean working tree,
zero behind count or successful object compilation alone does not establish
native behavior, source compatibility across the whole product or proof replay.
Keep historical comparison builds explicitly separate from acceptance evidence.

## Follow-up

The compiler advanced to `4c409da6`; its rebuilt Stage1 reports current provenance
and compiled Studio, report diff and focused law objects. The engine merge
completed as `01f5aec7` on `mocap-track` (20 ahead / 0 behind fetched upstream),
retaining the workspace host and adopting the upstream lifetime-safe PNG API.
These builds do not yet qualify the linked Studio or engine regression suite.
The proof assistant rebuild remains in progress.
