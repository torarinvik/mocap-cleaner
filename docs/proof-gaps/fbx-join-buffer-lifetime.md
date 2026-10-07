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
