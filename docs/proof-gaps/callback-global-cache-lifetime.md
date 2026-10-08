# Callback scratch ownership and global cache publication

## Demonstrated failure

Studio imported the reported high-block FBX, displayed 337 frames, then crashed
while reading the first cached skinned vertex. The retained sealed app's fault
address was unmapped although the descriptor count admitted the read. The
controlled e24 diagnostic IR shows a callback-owned arena threaded through
`sync_view`, `render_clip` and pose refresh. Refresh publishes a global descriptor;
the callback frees its arena without rehoming that transitive global write.
Three UI source files differ from the sealed crash closure, so diagnostic IR is
controlled reproduction evidence, not an identical sealed-source rebuild.

Existing source-level geometry contracts and passing engine-only cache controls
do not establish the generated allocation lifetime. Logical bounds cannot prove
that an admitted array descriptor still owns mapped backing storage after a
callback returns. Do not erase tracking with `trusted` to admit publication.

## Current repair evidence

The callback-shaped content/growth control fails at O0/O2 on compiler e24 and at
O2 on fetched main `b26659e2`. Candidate `a6d52dc2`, based on that main, propagates
resolved direct-callee global-write effects through caller-owned arena slots.
Its exact Stage0-seeded product `5d31572a` compiles and runs the unchanged fixture
with exit 0 at O0/O2. Source, product and runtime pre/post hashes are retained in
`/tmp/Elisa-compiler-global-rehome/build/global-rehome-transitive-check-b266/`.
This is focused runtime evidence, not a formal theorem about the full backend.

## Required closure

- Inspect production generated ownership IR: rehome the affected cache before
  its producing callback arena is freed, including nested owning payloads.
- Preserve resolved module identity, overload/shadow refusal, recursive-call
  handling and scalar-result allocation behavior. Unknown effects must not be
  treated as proven safe. Static indefinite storage is not cleanup acceptance.
- Run sanitizer controls and retain terminal logs. Arena mapping/reuse can evade
  sanitizer poisoning; no report cannot override a failed content assertion.
- Measure cache-hit redraw allocations and peak retained memory. Syntactic write
  propagation may clone a cache even when the refresh returns without writing.
- Integrate earlier project repairs and qualify the original source-file import,
  Character/Skeleton switching, playback, frame changes and repeated redraws on
  a matched current app. Keep the original take unchanged.

Full evidence and acceptance boundaries:
[FBX request record](../acceptance/fbx-request-proof-2026-10-07.md).


## Production scalar-type owner collision

The candidate full Studio compile does not yet reach production IR because
`UiDialog::result` receives a global-storage return diagnostic. Root isolated
this on the exact candidate product: a fixed global array of `UiDialog::Result`
(a scalar const enum) returns one element successfully. Including the actual
UI dialog source also emits LLVM successfully. Adding an unrelated
`Other::Result` struct containing `darray[u8]` makes the unchanged scalar return
fail with the same diagnostic. Sources, logs and terminal statuses are retained
in `build/dialog-result-reduction/{scalar-enum,actual-ui,other-owner}.*`.

The global-storage return checker currently compares a bare return type name
against collected owning-struct names without preserving module owner identity.
A repair must distinguish the scalar enum from the unrelated owning struct,
while continuing to refuse genuine owning global-storage copies. Qualify exact
qualified/unqualified owner resolution, nested owners and ambiguous/shadow
refusal; changing the UI result API or dropping tracking would hide the defect.
The concurrent atomic-loader diagnostic remains a separate unresolved reduction.
