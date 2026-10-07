# FBX joined-result buffer lifetime

The corrected isolated void-poll probe passed valid paths into native staging
and conversion. Immediately before callback return, source/destination lengths
were 70/101 and both started with `/`; source/runtime digests had length 64
and first bytes 53/51. After readiness and join, all four lengths and payload
addresses were unchanged, but all four first bytes were zero.

Memo node growth from 94 to 4,190 succeeded. That does not establish ownership
of the whole Memo: after pending-to-document global publication, nested byte
array reads in `document_memo.rehome` faulted with EXC_BAD_ACCESS. Explicit
caller-region annotations in a separate probe did not remove either failure.

Root inspected and retained three diagnostic logs under
`build/void-join-boundary-diagnostic/`; `record.json` binds their hashes. The
probe source and executable were overwritten between runs, so this capture
does not claim an immutable product/source closure or release qualification.

The earlier suspected native `open` stall was an LLDB breakpoint before the
call executed. It is not evidence of native blocking. The next repair must
track actual payload allocation owners, join's target region, worker-arena
transfer and release ordering. Intact headers, scalar success status and one
surviving dynamic field cannot prove that every returned allocation survives.

Preserve exact bytes through join, poll return, global publication, nested
growth and cleanup before rebuilding the user package. Requalify with committed
compiler/runtime provenance and an immutable probe closure; keep the actual
FBX Character/Skeleton journey and source preservation checks open.

## Identified lowering defect

Subsequent LLDB inspection placed all four payload addresses inside
`ConcurrencyWorkStart1.worker_arena`. The worker's first release saw two
references; the joined release saw one and `arena_transferred=false`, then
freed that arena. The generated LLVM call from the void poll passed a null
hidden result-region argument to `join__Result`. Root independently found
that null argument in the retained diagnostic LLVM module
`/tmp/mocap-void-probe/build/fbx_worker_void_global_probe.ll`.

The callback's allocation owner is therefore present, but join cannot adopt
it into a live caller owner. Repair general aggregate call lowering to supply
the call site's allocation region even when the enclosing function returns
void. Do not weaken intrinsic authentication or infer storage-free results
from an unknown type. Rebuild and qualify the whole returned graph before
promoting the compiler; explicit worker annotations alone did not fix this.

## Regression scope

Positive carrier controls must use scalar or void callers with an owned generic
temporary result. A function already returning an array has a hidden return
arena and cannot establish that a local carrier is created when that slot is
absent. Likewise, an unrelated array literal or typed growable local can hide a
failed call-demand scan. Cover inferred, explicit and qualified specialization.

Negative controls must keep scalar-specialized calls, scalar results borrowing
region-backed input, and same-named functions in different modules free of newly
introduced local carriers. Inspect their generated function bodies separately
from the allocating fixture entry point. Retain full compiler before/after
carrier counts and matched Stage1 timings; passing byte reads alone does not
establish the required absence of a runtime slowdown.

An independent reducer exposes another call-demand gap in candidate `cd6c98b9`:
a scalar `inspect()` returns `Owned::bytes()[0].i64()`, where a non-generic
module function returns `darray[u8]`. Current-main compiler `665f40d7` emits
LLVM (exit 0); the candidate refuses `inspect` with "region-backed call has no
live allocation arena" (exit 2). The frozen source, exact commands, compiler
hashes and logs are retained in `build/qualified-owned-call-dy7nj95a/record.json`.
This is compile/lowering evidence, not a runtime correctness result for main.
Resolve qualified concrete calls as well as generic specialization; retain the
fail-closed guard. A scalar caller with no other allocations must acquire the
needed carrier only when its resolved result owns storage.
