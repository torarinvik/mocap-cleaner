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
