# Allocation regions across task callback calls

## Observed failure

The focused FBX worker called directly succeeds; the same Job dispatched through
`task`, readiness polling and join crashes during worker allocation before a
Result is returned. Exact evidence and limitations are in
`build/fbx-worker-async-crash-evidence-2026-10-07.json`, using compiler revision
`48dc78e2`. Studio's visible import refusal remains separate runtime evidence;
the standalone probe omitted AppKit initialization.

## Compiler and runtime boundary

Read-only inspection found that direct calls append hidden allocation-region
arguments recorded by `FnTable.arena_counts`, whereas function-value calls emit
only explicit arguments plus applicable error/environment parameters. Generic
`fn(A) -> R` metadata does not retain the callback's required allocation slots.
The task worker's raw C entry cannot receive an extra hidden argument implicitly.

The proposed repair is being developed in isolated checkout
`../Elisa-compiler-fn-region-call-abi`. No repaired compiler product is qualified.
The selected compiler remains unchanged until a coherent source/product build
and runtime evidence exist.

## Required ownership obligations

- Callback metadata preserves required regions and their exact ABI order.
- Worker entry obtains a valid, explicitly owned allocation region before calls.
- Captured Job storage remains live while the worker reads it.
- Returned arrays and Memo backing remain live after worker exit and join,
  including publication into a retained Studio document.
- Adoption or ownership transfer happens only after worker completion; concurrent
  allocations must not mutate an unsynchronized caller allocator.
- Polling retains the worker and its region; cancellation still drains ownership.
- Join, rejected results and close each release or transfer ownership exactly
  once. A stack-local worker arena cannot back a retained result.
- Raw callbacks and allocation-free callbacks retain valid, explicit ABI behavior.

### Captured request buffers

The selected runtime's `ctx_concurrency_box_new` allocates the outer argument
box and shallowly assigns its value. That does not transfer ownership of nested
darray backing storage. Studio previously constructed source, build-root and animation
buffers inside `start_fbx_import`; moving those Job fields alone did not establish
that those buffers survive the caller's allocation region. The standalone probe
keeps its main arena alive throughout polling and therefore cannot qualify this
part of the UI lifetime.

The repair must consume an explicitly owned capture region, or use an argument
representation whose complete storage is owned by the worker. Callback result
region forwarding alone does not meet this obligation. Qualification must let
the submitting frame end before the worker reads its request, then retain and
grow returned arrays after join releases the worker state. These are separate
checks of input and output ownership.

Commit `15dd271` changes the FBX argument to a composed `RequestBuffers` value
with inline source/build-root arrays of 4096 bytes and an animation array of
1024 bytes. Bounded admission contracts precede copying; the worker allocates
its dynamic arrays after receiving those bytes. Worker and companion law sources
compile with selected clean compiler `48dc78e2` (product `461d377b`), with logs
`build/fbx_inline_request_worker.log` and `build/fbx_inline_request_laws.log`.
This is source compilation evidence only. The revised asynchronous probe and
actual Studio import remain unqualified; the generic nested-reference capture
problem and worker result-region repair remain open.

Conservative rejection of unsupported callbacks may be an interim compiler
safety measure; it does not deliver required background FBX import. Do not replace
the asynchronous product path with a blocking call to obtain a passing probe.

## Product callback scope

A source audit found ten named Studio task sites, all returning aggregate
Result types. The affected compatibility review must include:

| Callback | Product path |
| --- | --- |
| `load_fbx_import_job` | FBX import |
| `evaluate_contact_preview_job` | Contact repair preview |
| `load_session_locate_job` | Session source relocation |
| `move_build_generation_job` | Generated-build cleanup |
| `restore_build_generation_job` | Cleanup restoration |
| `generation_move_handle_drain_job` | Cleanup participant drain |
| `generation_restore_handle_drain_job` | Restore participant drain |
| `scan_build_generation_candidate_scan_job` | Cleanup candidate inspection |
| `generation_recovery_scan_job` | Recovery record inspection |
| `generation_recovery_discovery_job` | Recovery discovery |

Several declarations omit an explicit `Memory.Allocate` capability or declare
only `Blocking.IO`. Aggregate return shape alone does not establish that every
callback has the same allocation ABI. Compare inferred callback metadata to
the actual callee slots and preserve allocation-free paths. This audit identifies
qualification scope; it does not establish that all ten paths fail at runtime.

## Acceptance still required

Cleanup restoration, recovery reconciliation and recovery discovery now capture
`StudioWorkerPathCapture::Path` values instead of submitting dynamic path arrays.
Each value contains its bytes and count inline; reconstruction occurs inside the
worker. The existing capture/restore contracts and fifteen companion laws cover
bounded counts and refusal, but do not prove task ABI correctness or result-region
publication. Current compiler qualification for these three callback integrations
remains open, alongside the previously converted candidate scan.

Seed19's current-source diagnostic product `0e1698e53d8e60b9761e366c4a670db4b958ef69aee1208e14453303136c7d7c`
uses runtime `37637ffa62447f4a16008ed834fbb5bc9ef3ade0f32d9669d84d3860d6ab9449`
and dirty source tree `9ee5163beebab821207fecca7da9e05b51568e18d60bd59a8bd0febbfcc73d7f`
at merged HEAD `3714380c`. Its provenance check passes. The three worker source
objects and both capture/copy law objects compile at O2, with matching runtime
source closure guards. These object-only units need not emit their otherwise
unreachable functions; this is source compilation evidence, not execution or
proof discharge. The clean-archive prover build correctly refuses this dirty
compiler snapshot, so a committed repair and rebuilt pair remain required.

This compiler caught storage dependency invalidation when callers appended NULs
to both reconstructed paths. `restore_terminated` now constructs a complete
terminated path inside its own helper before returning it; callers do not mutate
those buffers before native calls. Recovery scan and Restore then compile.
The complete app still declines three task-result extraction sites for missing
concrete hidden caller slots; standalone worker compilation does not close them.

Termination contracts now also require exactly one trailing NUL, no interior NUL,
and exact preservation of the captured path bytes. Count-only contracts were too
weak to express the native path identity obligation. These strengthened contracts
and their five additional laws require compilation and authenticated proof with
the committed repair product; the preceding Seed19 evidence predates them.

Contact preview submits an affine Memo containing nested dynamic buffers.
`StudioModel::build_with` copies the pristine document, rig order and markers for
the displayed Clip, but previously assigned the nested source reference directly.
`StudioTakeSourceRefCopy` now copies all six byte arrays into the caller-selected
region before Clip construction, with byte/count preservation contracts and seven
companion laws. Compilation, authenticated proof and post-frame lifetime evidence
for this change remain open. This removes one source-level alias; it does not
establish that the submitted Memo's allocation owner survives the task, or that
joined output can safely outlive the publication frame. Those require an explicit
ownership path and current compiler/runtime evidence.

Rebuild the current compiler and runtime with source provenance, rerun the focused
FBX task probe, and exercise actual Studio import, display switching and edited
surfaces. Retain source-preservation and malformed-input controls. Compile and
proof evidence must distinguish callback ABI/ownership guarantees from the
native parser and importer correspondence. The full roadmap remains incomplete.
