# Recovery compiler candidate diagnostic check

Started from project commit `ce7f242` with concurrent suggestion work present.
This run is diagnostic compatibility evidence, not immutable product acceptance.

Command: `ELISAC=../Elisa-compiler/build/recovery-cstr-candidate/scripts/elisac_stage1.sh CHECK_JOBS=2 PROOF_JOBS=2 sh scripts/check.sh`.

Candidate compiler source/binary provenance is `faabd1f7`, based on current
`f292cbe0`. The default prover remains `5776350b` with frontend `f292cbe0`.
The initial native Trash support build reports normal compiler `f292cbe0`;
inspect later unit/CLI logs before claiming candidate coverage of those builds.

Log: `build/recovery-cstr-check.log`. The tool session is `19112`, confirmed
running at dispatch. Results remain pending. Do not infer completion from an
unchanged log, lock file or this historical session observation; poll the handle.

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
