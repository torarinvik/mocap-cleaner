# Export publication outcome qualification

`StudioExportPublicationPolicy` keeps GLB-only, JSON-only, text-only and both
sidecar write outcomes distinct. It does not claim crash durability or motion
quality approval. Reports are serialized before GLB publication; later writes
consume frozen byte arrays.

Default prover 5776350b/frontend f292cbe0 reports policy 14/20 and laws 21/38.
Unproven and unsupported obligations remain; const-enum branch summaries are
under investigation in `../elisa-proof-mocap`. No baseline was weakened and no
certificate-replay closure is claimed for these files.

Integrated compile-only Studio build succeeds with f292cbe0. Evidence:
`build/export-publication-build.log`. Runtime failures between GLB and sidecar
writes, snapshot retention, create-only retry and durable stage recovery remain
unqualified. The existing snapshot-generation policy still guards publication
against changing displayed results; this is not a proof of native IO semantics.

Directory-sync policy qualification: source 6/9, laws 10/20 on default
5776350b. Its native adapter distinguishes failed rename from a successful
rename followed by failed parent-directory sync/close. Compatibility Boolean
wrappers report observed publication only; they are not crash-durability
evidence. Integrated Studio compile passes (`build/publication-durability-ui-build.log`).
Native error injection, filesystem races and certificate replay remain open.

Recovery path bounds live in `StudioExportRecoveryPathPolicy`, separately from
the fully replayed retry admission baseline. Default 5776350b proves and replays
its source 6/6. Its laws produce 18 certificates; 14 independently replay and
four remain gaps involving scoped capacity constants and caller summaries.
Evidence: `build/export-recovery-path-source.json` and
`build/export-recovery-path-laws.json`. No reviewed baseline is weakened.

The native recovery directory adapter compiles with isolated compiler faabd1f7.
Normal f292cbe0 rejects C-string fields in ordinary payload enums. The candidate
uses the existing one-word typed pointer representation, but runtime and ABI
qualification remain required before adoption. Directory creation, ownership,
durable journals and recovery integration are not yet accepted.
