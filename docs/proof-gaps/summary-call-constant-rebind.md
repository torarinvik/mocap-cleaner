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

Clean immutable candidate `build/elisa-proof-summary-rebind-clean` has manifest
proof revision `84bb8a47`, source_dirty=false, compiler/frontend `f292cbe0`.
Its SHA-256 is
`77c360104b38cdcdffffa3a26b2a95300fb7dfc2b47bf80a6ef76040616f47e4`,
verified against the actual binary. Root independently reran current product
files and inspected the full output: source 6/6 and laws 18/18 independently
replayed, zero findings, zero semantic diagnostics and zero replay gaps.
Product logs are `build/recovery-path-clean-0.log` and
`build/recovery-path-clean-1.log`. Reviewed source/law baseline rows now require
those results; the older default cannot close the law row. This qualifies the
focused policy, not default promotion or native path ownership/races.

A separate stage-policy source proof process terminated with exit 139 and
emitted an empty JSON file; this does not establish a cause or proof result. The
journal proof process had previously terminated with exit 139 as well. These
abnormal exits remain under investigation.
