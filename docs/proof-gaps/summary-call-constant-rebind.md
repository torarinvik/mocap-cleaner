# Scoped constant call summary replay

Prover commit `92700a7e` reconstructs a call summary's exact source site and
checks scoped integer constant arguments against a unique validated declaration
path. Literal parameter rebinds are tied to the callee summary's exact formal
slot. The independent checks reject ambiguous owners and do not infer unequal
values from different enum variant names.

A focused qualified-constant call repro proves and replays all 6 obligations
on an isolated candidate built with Stage1 `f292cbe0`. This candidate has not
replaced the default prover.

`StudioExportRecoveryPathPolicy` laws remain 14/18 replayed on that candidate.
The four open caller laws now pass source-call lookup but fail formal argument
matching. No baseline was weakened. The candidate's direct stage-policy proof
process also terminated with exit 139 and emitted an empty JSON file; this does
not establish a cause or usable proof result. The journal proof process had
previously terminated with exit 139 as well. These crashes remain under
investigation.
