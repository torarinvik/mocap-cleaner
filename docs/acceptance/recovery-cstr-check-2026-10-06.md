# Recovery compiler candidate diagnostic check

Started from project commit `ce7f242` with concurrent suggestion work present.
This run is diagnostic compatibility evidence, not immutable product acceptance.

Command: `ELISAC=../Elisa-compiler/build/recovery-cstr-candidate/scripts/elisac_stage1.sh CHECK_JOBS=2 PROOF_JOBS=2 sh scripts/check.sh`.

Candidate compiler source/binary provenance is `faabd1f7`, based on current
`f292cbe0`. The default prover remains `5776350b` with frontend `f292cbe0`.
The initial native Trash support build reports normal compiler `f292cbe0`;
inspect later unit/CLI logs before claiming candidate coverage of those builds.

Log: `build/recovery-cstr-check.log`. Tool session `19112` subsequently terminated
with exit one. All 78 executable test rows and all four CLI workflows report
rc=0. The proof baseline gate failed with missing rows, regressions and stale
rows. Concurrent source/baseline changes mean this is diagnostic evidence, not
acceptance of an immutable project revision. The initial native support build
used normal f292cbe0 as recorded above.

The candidate compiles C-string constructors/extraction and the composed recovery
adapter. That evidence does not establish new payload runtime behavior, crash
durability, filesystem race safety or complete implementation-plan acceptance.
No new executable tests were added. Native recovery failures and direct payload
runtime qualification remain separate requirements.

While this run remained live, proof wrapper commit `03376ea` changed its
dispatch summary from “proved” to “processed” and made missing results or
abnormal verifier termination fail the wrapper. Abnormal partial output cannot
enter its cache. Python syntax parsing passed; no runtime wrapper tests were
added or run. The already-running diagnostic loaded the earlier wrapper and
does not qualify this change. Its handle was polled again and remained live.
The later terminal handle poll establishes completion; historical live polls
do not supersede that result. This run does not qualify recovery native IO or
the newer report/session changes committed after its executable phase.
