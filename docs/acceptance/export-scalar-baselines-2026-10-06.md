# Reviewed export scalar baselines

Root independently reran four files using the default prover with clean proof
source `5776350b` and compiler/frontend `f292cbe0`. Its binary SHA-256 matches
the manifest: `e14a233fa4bff39936d784e679c867dc666c614c0a9d61aca71267312b19c327`.
This historical compiler input is explicit; the normal development compiler
has since advanced to `04b384ec`, and newer prover source is under repair.

| File | Proven and independently replayed |
| --- | --- |
| `src/studio/export_time_map_policy.elisa` | 14/14 |
| `proof/studio_export_time_map_laws.elisa` | 20/20 |
| `src/studio/export_recovery_publication_policy.elisa` | 6/6 |
| `proof/studio_export_recovery_publication_laws.elisa` | 12/12 |

All four runs returned zero, with zero replay gaps, findings or semantic
errors. Reports are `build/<repository path with underscores>.review.json`.
The reviewed baseline adds only these scalar files. It does not claim closure
for dynamic arrays, report assembly, journal IO, native locks, path ownership,
publication races, crash durability or the complete recovery workflow.
