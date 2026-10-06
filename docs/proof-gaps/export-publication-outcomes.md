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

The adapter now exposes closed record names for JSON, text, journal and output
snapshot paths. Bounded length admission rejects invalid names before copying;
allocated strings have explicit release ownership. No recovery directory is
created by the compile-only qualification. Candidate LLVM IR represents the
created variant as `{ i32, [1 x i64] }` and stores its C-string with `store ptr`;
this confirms emitted layout only, not native runtime or ownership correctness.
Evidence: `build/recovery-creation-payload.ll` and
`build/export-recovery-store-build.log`. Integration awaits candidate adoption
and durable record establishment before GLB publication.

`StudioExportRecoveryPreparePolicy` requires owned storage, reserved capacity,
synced GLB/JSON/text snapshots, synced prepared journal and directory sync before
publication admission. Default 5776350b independently replays source 9/9 and
laws 25/25, with zero gaps or findings. All seven missing-fact cases reject
publication regardless of the other facts. Native code must establish these
facts; the policy is not yet connected to the export operation. Evidence:
`build/export-recovery-prepare-source.json`,
`build/export-recovery-prepare-laws.json` and compile-only
`build/export-recovery-prepare-build.log` (normal compiler f292cbe0).

The bounded native reader preserves exact staged bytes and rejects reads beyond
the caller's limit, IO errors and close failures. Limits are 64 MiB for one GLB,
1 MiB per report and 64 KiB for a journal. The arithmetic budget policy and laws
independently replay 6/6 and 20/20 on default 5776350b, with no findings or gaps;
both the reader and laws compile with normal f292cbe0. Evidence:
`build/export-recovery-budget-source.json`,
`build/export-recovery-budget-laws.json`, `build/export-recovery-bytes-build.log`.
Total retained disk capacity and concurrent file mutation remain unqualified.

Recovery storage now writes each closed record type with the atomic create-only
publisher and enforces its byte limit. Output snapshot storage consumes exact
nonempty bytes from the private staging file, rather than GLB reserialization.
These APIs compile with isolated faabd1f7 (`build/export-recovery-store-build.log`).
The caller must supply an owned directory from creation and retain evidence on
partial failure. This does not establish durable prepared journals, total disk
reservation, exact final-output verification or integration with export; those
remain required before admitting publication through the prepared-record gate.

The bounded byte adapter also compares a loaded file against expected bytes,
requiring equal lengths and equality at every byte. Failed or oversize reads
return false; residue fingerprints are not involved. It compiles with f292cbe0.
Quantified byte-comparison proof, native race qualification and retry integration
remain open; this observation alone does not authorize publication or cleanup.

`StudioExportRecoveryStagePolicy` defines prepared, GLB, GLB+JSON, GLB+text and
complete stages as a const enum with explicit wire values. Its boundary rejects
report-only and unknown values; transitions preserve observed sidecars and do
not regress. Current source and laws compile with f292cbe0. Proof qualification
is pending: the first formula produced budget refusals and caller replay gaps,
and an equivalent explicit-branch formulation is being checked. Do not use
superseded `build/export-recovery-stage-*.json` reports as acceptance evidence
until the current runs finish and their certificates are reviewed. No baseline
is added for the stage policy, and journal qualification/integration remain open.

The version-1 journal codec now stores a strict header, transaction basename,
workspace and three final paths, capture generation/animation, frozen byte sizes,
and separate observed/durable stages. Paths are UTF-8-validated hex fields;
transaction names are restricted to the private mkdtemp namespace. It rejects
extra/missing fields, aliased final paths, noncanonical or out-of-range numbers,
unknown stages and durability claims inconsistent with observed publication.
Decode and encode publish caller outputs only after complete validation.
Source contracts and companion laws compile with normal f292cbe0; proof checking
is running, so no certificate closure or reviewed baseline is claimed.

The native store creates `journal.txt` without replacing an existing record.
Updates require a strictly decoded prior journal, unchanged immutable binding,
and monotonic observed/durable stages, then use the atomic synced publisher.
These adapters compile with isolated faabd1f7. Native ownership/race checks,
semantic source/stack provenance qualification, round-trip proof and injected
journal failures remain open. Format validity alone never authorizes retry or
cleanup. Evidence: `build/export-recovery-journal-laws-build.log` and
`build/export-recovery-store-build.log`.
