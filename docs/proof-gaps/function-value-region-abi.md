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

Conservative rejection of unsupported callbacks may be an interim compiler
safety measure; it does not deliver required background FBX import. Do not replace
the asynchronous product path with a blocking call to obtain a passing probe.

## Acceptance still required

Rebuild the current compiler and runtime with source provenance, rerun the focused
FBX task probe, and exercise actual Studio import, display switching and edited
surfaces. Retain source-preservation and malformed-input controls. Compile and
proof evidence must distinguish callback ABI/ownership guarantees from the
native parser and importer correspondence. The full roadmap remains incomplete.
