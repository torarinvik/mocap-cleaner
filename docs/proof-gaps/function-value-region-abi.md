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
darray backing storage. Studio constructs source, build-root and animation
buffers inside `start_fbx_import`; moving the Job fields alone does not establish
that those buffers survive the caller's allocation region. The standalone probe
keeps its main arena alive throughout polling and therefore cannot qualify this
part of the UI lifetime.

The repair must consume an explicitly owned capture region, or use an argument
representation whose complete storage is owned by the worker. Callback result
region forwarding alone does not meet this obligation. Qualification must let
the submitting frame end before the worker reads its request, then retain and
grow returned arrays after join releases the worker state. These are separate
checks of input and output ownership.

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

Rebuild the current compiler and runtime with source provenance, rerun the focused
FBX task probe, and exercise actual Studio import, display switching and edited
surfaces. Retain source-preservation and malformed-input controls. Compile and
proof evidence must distinguish callback ABI/ownership guarantees from the
native parser and importer correspondence. The full roadmap remains incomplete.
