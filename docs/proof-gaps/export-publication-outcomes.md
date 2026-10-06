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

Recovery retention capacity now has a separate policy: at most 16 occupied
record/reservation slots and 1 GiB of logical retained plus reserved bytes.
Each request budgets two copies of its bounded GLB/report/journal payloads for
atomic staging. Unknown inventory rejects admission; held reservations remain
charged, and unremoved staging must remain in retained usage. This does not
establish filesystem free space, native scan completeness or locking semantics.
Default 5776350b independently replays source 16/16 (including six imported
budget obligations), with zero gaps/findings. Laws replay 26/40; 12 producer
certificates remain replay gaps and two obligations remain open. The source-only
baseline is reviewed; no law baseline is weakened or added. Compilation passes
with f292cbe0. Evidence: `build/export-recovery-capacity-source.json`,
`build/export-recovery-capacity-laws.json`, `build/export-recovery-capacity-build.log`.
Native inventory, reservation persistence and export integration remain required.

`Folder::entries_checked` now distinguishes failure from an empty directory,
bounds entry count and Darwin dirent fields, checks embedded NUL/separator bytes,
observes readdir errno, and requires successful close before publishing names.
It preserves caller output on failure and explicitly ties allocations to the
caller region. Other host layouts reject instead of using Darwin offsets.
Normal f292cbe0 compilation passes (`build/folder-checked-build.log`). Its scalar
policy independently replays 10/10; laws produce 24 certificates with 17 replayed
and seven caller-summary replay gaps. No law baseline is added. Native error
injection, race checks, portable dirent support and capacity inventory integration
remain open. Evidence: `build/folder-scan-source.json`, `build/folder-scan-laws.json`.

The explicit-branch stage proof batch ended with exit 1 and empty source/law
JSON files; the shell's final JSON-reader failed because no report was available.
The underlying prover failure cause is not established. This terminal run
provides no proof acceptance evidence; source contracts remain unchanged.

The recovery inventory adapter now scans the selected canonical build root and
counts every recovery-namespace directory and regular child, including unknown
journals and leftover staging. It rejects symlinks, nested/nonregular children,
unverifiable identities, incomplete scans, oversized paths and exceeded limits.
Unknown records are accounted for without acquiring cleanup authority. Typed
failure messages identify permissions, path, identity and capacity problems.
Caller must hold the workspace transaction lock; unrelated-process races remain
unqualified. The adapter and its laws compile with normal f292cbe0.

The scalar totals policy independently replays 21/21 (including 16 imported
capacity/budget obligations). Laws produce 39 certificates, with 28 replayed
and 11 gaps; no law baseline is added. Evidence:
`build/export-recovery-inventory-source.json`,
`build/export-recovery-inventory-laws.json`, `build/export-recovery-inventory-build.log`.
Native failure injection, durable reservation persistence and export/recovery
UI integration remain required before the capacity gate is operational.

The journal source/law proof batch is now terminal with exit 139 and no usable
JSON reports. Its cause is under investigation in the prover checkout; this is
not evidence that journal contracts or round-trip laws are proved. The prior
"checking is running" observation is superseded. Compilation remains separate
evidence, and no journal/stage proof baseline has been added.

`StudioExportRecoveryPrepare` now composes the accounting and storage adapters:
it requires the caller's workspace transaction lock, validates metadata/snapshot
bounds, reserves logical capacity from a complete inventory, creates a unique
directory, syncs its build parent, and stores exact output/JSON/text snapshots
plus the prepared journal. Every required write must report directory sync.
It calls the fully replayed prepared-record policy and checks that staging still
matches captured bytes before returning Prepared. Partial failures retain the
directory and return its owned path; caller metadata changes only on success.

Composition compiles with isolated faabd1f7; payload field annotations use exact
module-qualified Failure types so sibling enums cannot share an ambiguous
backend annotation. Normal compiler adoption, injected IO failures, ownership
and lock qualification, persisted reservations and Studio integration remain
open. Source/animation/stack provenance and exact report binding still require
their separate acceptance checks. Evidence:
`build/export-recovery-prepare-adapter-build.log`.

## Captured-byte recovery binding

`StudioExportRecoveryBinding::load` verifies an owned, locked same-session
record against captured immutable output/JSON/text bytes. It strictly decodes
the stored journal, checks the full export binding and exact directory spelling
against workspace plus transaction, compares each stored snapshot byte and the
published GLB byte, and only then returns the journal. Failure preserves the
caller's journal. Stored stages do not establish current sidecar integrity.

The isolated faabd1f7 compiler emitted `build/export-recovery-binding.o` without
diagnostics. The earlier proof wrapper reported two files processed but did not
expose the incorrect `require` spelling in two law preconditions. After fixing
them to `requires`, direct prover output establishes eight obligations proven
and independently replayed, zero findings and zero semantic diagnostics
(`build/export-recovery-binding-laws.log`). No native proof is claimed here.
No executable tests were added.
Same-session captured bytes are required: persisted sizes are not authenticated
restart identities. Ownership, lock facts, native race safeguards, sidecar
completion, Studio integration and restart recovery remain open.

## Create-only report completion adapter

`StudioExportRecoveryCompletion::complete` rechecks captured-byte binding before
each report operation. It recognizes an exact existing report, otherwise uses
atomic create-only publication. An existing conflicting or unreadable file is
never overwritten. It leaves GLB bytes untouched and records observed report
stages monotonically. Durable report stages advance only after directory-synced
publication when the journal already records GLB durability. Recognizing an
existing report alone does not advance durability.

Published outcomes retain their publication status even if the later journal
update fails; a separate typed journal status exposes that failure and unknown
directory durability. Existing-match outcomes also expose journal persistence
separately. Historical completion
stages do not authenticate other current sidecars. Caller-owned lock/IO facts
remain trusted, and Studio/restart integration and native fault qualification
are unfinished. Candidate faabd1f7 emitted the object without diagnostics
(`build/export-recovery-completion-build.log`). Report-stage laws were added;
their direct prover run is still pending in session 3607. No closure baseline
or native acceptance claim follows from compilation.

The report-stage helper is now in a separate
`StudioExportRecoveryReportStagePolicy` module, keeping its proof independent
of the broader journal transition policy. Exact per-stage result contracts were
added alongside the monotonicity and report-preservation contracts. Direct
isolated output reports 99 obligations, 82 proven and independently replayed,
zero replay gaps, 17 findings and two semantic normalization diagnostics. Three
false-JSON source branches do not establish their ensures; the remaining 14
findings concern seven calls whose executable summary therefore remains
unverified. This is not proof closure. Evidence is
`build/export-recovery-report-stage-isolated-laws.log`; the focused repro was
sent to the prover repair agent. The original broader session 3607 is still
live at the latest handle poll and is not restarted or declared terminal.

## Report preparation now blocks unsafe publication

Studio previously allowed GLB publication when staged identity or report
serialization failed. It now discards the staging file and preserves the
destination unless identity and both nonempty report snapshots are captured;
each report must also fit the existing 1 MiB recovery budget. This check occurs
before the second destination confirmation and GLB commit. This is a live
Studio guard, not durable recovery integration.

Normal f292cbe0 compiled and packaged Studio with checks skipped
(`build/export-snapshot-ready-studio-build.log`). Direct policy verification
proves/replays 4/4 with zero findings, diagnostics or gaps; its baseline was
updated from two to four reviewed obligations. Expanded laws remain open:
18 obligations, 17 proven, 15 replayed, two replay gaps and one finding in the
existing invalid-generation law. Evidence is
`build/export-snapshot-ready-source.log` and
`build/export-snapshot-ready-laws.log`. No native export behavior was exercised
and no executable tests were added.

## Sidecar path preflight

Studio now rejects destinations longer than 4,083 bytes before staging or
publication: the `.report.json` suffix occupies 12 bytes and the native path
limit is 4,096 bytes including NUL. The text suffix occupies 11 bytes. The
same admission check guards report publication. The pure path policy proves
and independently replays 2/2 with zero findings/diagnostics/gaps; its new
baseline records that source evidence. Boundary laws remain open: 12 goals,
11 proven, seven replayed, four replay gaps and one finding. Evidence:
`build/export-report-path-source.log`, `build/export-report-path-laws.log`.

The first integrated normal-compiler build stopped on undeclared
`session_impact_invalid` in concurrent session-persistence work, recorded in
`build/export-report-path-studio-build.log`. The owning agent has the diagnostic;
integration remains unverified until that work compiles. No executable tests
were added and no native long-path export was exercised.

After the session owner added the missing declaration, the same normal f292cbe0
compile/package command finished successfully in session 4190. The log now
contains both built and packaged outputs without diagnostics. This qualifies
compilation of the path guard, not native long-path behavior.

## Recovery completion diagnostics

Completion outcomes now retain the full journal persistence status rather than
collapsing written-but-unsynced and directory-synced results into one Boolean.
Typed messages distinguish unverified ownership, unavailable workspace
transactions, mismatched/unreadable captured bytes, create-only publication
failure, exact existing reports, report durability uncertainty and journal
failure/uncertainty. Published reports remain reported as published when later
journal persistence fails. Messages require keeping recovery evidence on
uncertain outcomes and do not imply every sidecar was checked.

The isolated faabd1f7 compiler emitted the completion object without diagnostics.
Messages have not been integrated into native recovery UI; native IO/UX
qualification and the existing stage-law proof gaps remain open. No executable
tests were added or run for this slice.
