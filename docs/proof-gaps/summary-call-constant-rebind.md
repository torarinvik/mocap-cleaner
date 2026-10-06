# Scoped constant call summary replay

Prover commit `92700a7e` reconstructs a call summary's exact source site and
checks scoped integer constant arguments against a unique validated declaration
path. Literal parameter rebinds are tied to the callee summary's exact formal
slot. It does not infer unequal values from different enum variant names.

The qualified-constant caller repro proves and replays all 6 obligations on an
isolated candidate built with Stage1 `f292cbe0`. Prover commit `84bb8a47` then
deduplicates repeated summary rows only when they point to the same exact source
call span and argument mapping. This resolves the recovery path caller laws:
source 6/6 with full replay and laws 18/18 with full replay, zero findings.
Evidence is `build/summary-rebind-recovery-source.json` and
`build/summary-rebind-recovery6.json` in the prover checkout. The default prover
has not been replaced by this candidate.

A separate stage-policy source proof process terminated with exit 139 and
emitted an empty JSON file; this does not establish a cause or proof result. The
journal proof process had previously terminated with exit 139 as well. These
abnormal exits remain under investigation.
