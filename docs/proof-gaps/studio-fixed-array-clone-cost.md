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
