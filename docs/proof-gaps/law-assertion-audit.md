# Law assertion audit — 2026-10-06

A Boolean law body does not establish its returned predicate unless a contract
or assertion requires that predicate. Earlier producer counts for laws that
only returned a Boolean therefore cannot establish their named behavior.

## Strengthened laws

The following files now assert `ensure result`, retaining their preconditions:

- Export validation: named status requirements plus explicit success/failure.
- Export result: forward/backward focus wrapping and adjacent order.
- Export publication: path admission, replacement consent and warning counts.
- Export report: duration arithmetic, frame/rate admission and schema fields.
- Duplicate operation: placement, index mapping and source bounds.
- Reset scope: one undo entry, enablement and isolated cleanup scopes.
- Export review: keyboard reachability and warning acknowledgement gates.
- Export path review: enabled focus choices and bounded page movement.

Current Stage1 `812c0547` compiled the report, reset, export review and path
review law files to objects without a stale override. Compilation checks source
acceptance; it does not prove their predicates. Updated producer verification
and certificate replay remain required for every strengthened law. Existing
baselines are retained and must not be weakened to accommodate new failures.

## Remaining audit

Review every Boolean law, including files that already contain some assertions.
A file-level search for missing `ensure` finds candidates but cannot establish
complete coverage. Job lifecycle, accessibility and legacy session prompt laws
still need per-function review. Workspace root laws are being reviewed by their
implementation owner. Confirm intended true/false semantics and preconditions
before adding an assertion; never assume every Boolean return is intended true.
