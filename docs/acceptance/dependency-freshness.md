# Dependency freshness audit — 2026-10-06

Fetched `origin` in all five checkouts before comparing `HEAD...origin/main`.
All adopted dependency branches contain every fetched upstream commit.

| Dependency | Local HEAD | Fetched upstream | Ahead / behind |
| --- | --- | --- | --- |
| Compiler | `88ffc005` | `72a75282` | 36 / 0 |
| Mocap proof assistant | `994f95be` | `151a2772` | 13 / 0 |
| Primary proof assistant | `151a2772` | `151a2772` | 0 / 0 |
| Mocap engine | `01f5aec7` | `7699ec52` | 20 / 0 |
| Elisa UI | `8ab2eb39` | `dc6cd397` | 6 / 0 |

The compiler, mocap proof assistant, engine and UI sources are clean.
Uncommitted primary proof-assistant work belongs to its active development
checkout and is preserved; it is not a published upstream revision.

## Binary provenance

The normal Stage1 compiler has been rebuilt at `88ffc005`. The default
`../elisa-proof-mocap/build/elisa-proof` manifest identifies proof source
`994f95be`, frontend and Stage1 compiler `88ffc005`, with both source trees
clean. Its binary SHA-256 is
`8c00afea0b6ebcd4da02966ff6e62a358c7d561c95a54dc69da1795852fbc2b6`.
Build and check scripts select these default paths. Historical override builds
must remain separate from current acceptance evidence.

Freshness does not establish product correctness. Current compiler semantic
scope repairs are qualified by focused compilation, while a UI payload-enum
backend failure remains recorded in `docs/proof-gaps/ui-event-scope.md`.
Focused export validation laws replay 11/14 certificates with zero replay gaps;
three goals remain unproven. Earlier full-check runs used earlier binaries and
do not qualify this snapshot.

Repeat fetch, ancestry and manifest checks before final snapshot acceptance.
Rebuild stale binaries and rerun affected verification after dependency changes.
