# Studio fixed-array clone compilation cost

## Observed current-source run

The complete Studio graph was compiled at O2 using committed compiler repair
`d5a9b58a`, product `b4e9a69dadb9f830efe2dfcef5851fcf72bb66120bdaf9af4bf4ce57d0fcf243`
and runtime `a8de91a171e0620b86e9dad322a2a008f838ba6aabf66deff736bf6013814ef2`.
The first run refused a missing candidate-row error-buffer argument; `b6c260e`
restored the declaration to the existing native ABI before the second run.

The second run reached LLVM object emission and remained active beyond thirteen
minutes. A one-second process sample shows nearly all sampled time under
SelectionDAG Combine, ReplaceAllUsesWith and FoldingSet operations. The sampled
physical footprint was 29 GB on a machine with 24 GB physical memory. RSS varies
with compression/swapping and is not the same measurement.

Artifacts:

- `build/main-after-69263c2-d5a9b58a-r2.log` (compiler output).
- `build/main-after-69263c2-d5a9b58a.sample.txt` (process sample).
- `build/main-source-closure-d5a9b58a-after-69263c2.json` (initial ordered closure).

The initial closure predates the one-line candidate declaration repair. A later
hash comparison found only that file changed among its 610 sources. This is a
diagnostic run, not an accepted immutable application build.

Root intentionally sent SIGINT after identifying this hotspot and confirming the
separate void-poll publication ownership defect. Session 19436 terminated with
exit 130; OS PID 82759 was absent afterward. This is an interrupted compile,
not a compiler-reported failure, successful build or observation timeout. No
runtime or application acceptance follows from it.

## Isolated repair and remaining qualification

Compiler inspection found `emit_clone_aggregate_value` reconstructing fixed
arrays through element-wise extract/insert chains. Large generated global
`.rehome` helpers are a plausible contributor to SelectionDAG cost; the sample
alone does not identify the exact expensive generated function.

Isolated compiler commit `e6564bf9` skips that reconstruction only for recursively
known storage-free arrays and makes unmodeled storage classification fail closed.
Region-backed arrays, views, references, opaque representations and unresolved
shapes must retain conservative handling. This source change is not yet qualified.

The diagnostic product `ba3aa590` compiled a 20 KB fixed-byte-array rehome
reproducer in 6.58 seconds, producing a 516 KB object. That narrow result did
not resolve the integrated cost: an isolated copy of Studio at `f6f8a6ec`
again sampled in SelectionDAG Combine/FoldingSet with a 29.4 GiB physical
footprint. The initial 4 GiB RSS guard refused the run with exit 125; the
subsequent 10 GiB RSS limit did not constrain compressed physical footprint.
After identifying the repeated hotspot, the agent intentionally interrupted
the second run: session 76182 exited 130 and PID 86421 was absent afterward.

Retained diagnostic artifacts are
`/tmp/mocap-void-main/build/main.compile-10g.log` and
`/tmp/mocap-void-main/build/main.sample.txt`. These temporary artifacts are
diagnostic evidence, not durable release qualification. The next investigation
must identify the expensive generated function/IR rather than infer that the
fixed-array shortcut has solved the full graph or repeat O2 builds blindly.

Required evidence:

- Fresh committed compiler/runtime provenance and exact source closure.
- Current graph compilation, retained IR or generated-function evidence, and
  measured time/memory comparison against the captured diagnostic baseline.
- Byte/value preservation for fixed arrays and nested known scalar records.
- Deep-clone ownership controls for arrays containing dynamic arrays and views;
  unknown and opaque types must not silently become storage-free.
- The separate void-poll/global-publication ownership repair and actual FBX UI
  journey. Faster compilation cannot qualify a dangling result.

## Fresh complete-graph LLVM attempt

Source-matched compiler `b6e132d2`, product SHA-256
`76687087d31873332811e73508596ec5eb007e4dfa2bb963713ff4237eaa81ce`,
was invoked on the complete Studio graph with `-O2 -emit llvm` under the
generation lock. Generated runtime declarations select this exact compiler.
Pre/post input snapshots match. The 4 GiB RSS guard stopped the process at
4,237,184 KiB; compile and wrapper exit codes are both 125. No LLVM file was
produced. This is a bounded diagnostic attempt, not a current Studio build.
No process sample identifies its expensive phase yet.

Retained artifacts: `build/studio-build.AwD3UL/`.
Input manifest SHA-256:
`ceacc53586557f8c12d8685e3a507665fe1d8e862e0f80146f47666352919694`.
Compiler log SHA-256:
`bb18ed435a27ec0a775409c3d5d99fdb1c12524b07c2078bad0f99f536d34b40`.
Next isolate O0 LLVM generation from the O2 pipeline before increasing memory
or attempting object emission; retain both outcomes and keep O2 qualification
open. A lower-optimization diagnostic cannot close release acceptance.

## O0 complete-graph LLVM isolation

The same source-matched compiler product subsequently completed
`-O0 -emit llvm` under the generation lock and 4 GiB RSS cap. Compile and
wrapper exit codes are both 0; the post-run input snapshot check passed.
`build/studio-build.6x886Z/studio.ll` contains 49,019,150 bytes and 5,886
function definitions. Its SHA-256 is
`f4242c512991a7822c07db8e72e2e5036d32e70333de60d32c6415b97e162e17`.
The input manifest SHA-256 is
`bf2a2de3090a0fc60cf6b630b65827d76b32a3441836bf6cce65c2df1fb07fd5`.

The retained `largest-functions.txt` ranks emitted functions by IR lines.
`StudioIconPaths.draw` leads with 12,225 lines, followed by
`SessionState.decode_session_with_source_reference` with 5,698 lines.
This size ranking does not identify an optimization hotspot. The compiler
prints LLVM after its optimization pipeline, so the O0 success and O2 guard
refusal narrow the next investigation to that pipeline; a sampled pass or
isolated reproduction is still required to identify the cause.
The O2 path also calls `inline_aos_store_record` before LLVM's default O2
passes; the O0 path skips it. Both this transformation and the LLVM passes
remain candidates, so running standalone `opt` on the O0 file would not
reproduce the complete O2 pipeline by itself.

No object, linked application, FBX import or user journey was qualified by
this diagnostic. Subsequent compiler source repairs require a fresh product
before current implementation qualification.

## Isolated SROA expansion

Standalone LLVM 23.1.2 `opt -passes=default<O2>` on that retained O0 IR
was intentionally stopped by a 1,536 MiB RSS watchdog. The observed peak was
2,319,872 KiB after 5.58 seconds; process exit is -15 (SIGTERM), not an
optimizer-reported failure. The polling cap can overshoot between samples.
`build/studio-opt-isolation-20261007/result.json` retains command and outcome.

The pass trace identifies a concrete expansion: SROA processes
`StudioSessionSaveSourceWorker.capture` at 1,157 instructions after SimplifyCFG;
the following EarlyCSE pass sees 281,111 instructions. This precedes module
inlining. Extracting that function from the O0 file and running only SROA
also succeeds, expanding the 1,782-line extracted module to 281,736 lines.
The extraction/SROA shell exits 0. Exact commands and artifact hashes are in
`build/studio-opt-isolation-20261007/capture-run-record.json`.
Extracted IR SHA-256:
`5b162de996b372b5ce8b4d6857cb7f8b98850445b1e279c89e364db8cb168ecb`.
SROA output SHA-256:
`1cd24034250f2ab9e9b72c6c5f17578a02b7f82f8961ce0b569d8e447c40951f`.

The worker returns a 20,024-byte record. Remaining first-class aggregate
loads cross contract-check blocks before their final sret stores. Existing
copy lowering rewrites nearby copies to memmove but conservatively leaves
these cross-block loads/stores intact. The repair must preserve the returned
snapshot while retaining contract evaluation and correct ownership. Moving a
load past a possible source mutation would change semantics. Qualify any
repair with snapshot-mutation, contract success/failure and aggregate ownership
controls, then recompile the complete current graph. This reducer supplies a
specific optimization lead; it does not establish the only full-build hotspot.

## Frozen-snapshot representation diagnostic

A hand-transformed copy of the extracted LLVM replaces twelve large SSA
load/store pairs with dedicated stack snapshots. Each snapshot memmove occurs
at the original load point; its final memmove occurs at the original sret
store point. Contract checks, deferred actions and intervening control flow
retain their positions. This avoids rereading the original source after those
actions and does not reuse the contract's `result` slot as immutable storage.

Running SROA and LLVM verification on this diagnostic exits 0. The transformed
output has 1,826 lines and 118,524 bytes, compared with the original SROA output's
281,736 lines and 36,736,320 bytes. Exact substitutions, command and hashes are
retained in `build/studio-opt-isolation-20261007/capture-frozen-snapshots-record.json`.
Transformed input SHA-256:
`28d6b86fb5d7d77818e8669d75eacdad00190178d15c451a327b9fcf1d5ef2b2`.
This is an LLVM representation experiment, not a compiler implementation or
runtime-equivalence proof. The compiler repair must still cover all return
paths, ownership, snapshot mutations and contract failures, then qualify the
complete current application graph without this hand transformation.
