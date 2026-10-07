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

Repair `d355c139` subsequently emits this identical frozen reducer at O0,
exit 0, with product SHA-256
`9466ea923c6d7c26cc78fba2dd7168f5535c4b8d01b48e147f6d45c1d665c6ff`.
Root retained `d355c139-record.json` and LLVM SHA-256
`7ff4507534b2a8f48b3244377e6fec147ff4ffeddfbee81115d7e7c377c86ed2`
beside the original failed run. This independently verifies that qualified
concrete lowering is accepted; it does not prove the complete proof/Studio
graphs, runtime performance or all carrier counts. Keep those gates open.

## Fresh focused compiler regression

The source-matched `b6e132d2` product, Stage1 SHA-256
`76687087d31873332811e73508596ec5eb007e4dfa2bb963713ff4237eaa81ce`,
passes the nested void-poll/global-publication fixture at O0 and O2 (exit 42).
After the publishing frame ends, the fixture grows outer and nested buffers
and checks their retained bytes. Generated LLVM was compiled with ASan; that
executable also exits 42 without diagnostics. Leak detection is disabled,
so this does not qualify leaks.

Scalar/generic controls remain free of local carriers; owned-result controls
have call-site carriers. Explicit builtin-Arena API execution exits 0.
Generic and concrete missing-owner fixtures refuse at the frontend with
undefined `MissingOwner` (exit 1). These establish overall invalid-source
refusal, not direct coverage of the backend's unresolved-owner branch.
The new controls are committed as `bed743ad`; compiler provenance validation
still passes because they change tests, not compiler source inputs.

Retained compiler-checkout evidence:
`build/void-poll-b6e132d2-qualified-controls/evidence.log`, SHA-256
`2d30f777b98079c911ff7adeb85e2d2f3fed2700e1e140f6d15d5f92ad4e6b02`.
Wrapper exit is 0. Root independently checked the evidence hash and current
provenance. Full current-main gate comparisons, carrier counts, no-slowdown
measurements, complete Memo ownership and the actual Studio FBX journey remain
open; this focused pass does not close them.
