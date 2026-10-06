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
- Job lifecycle: cancellation, stale revision/generation and prior value retention.
- Legacy session prompt: Cancel default, focus movement and closed-prompt refusal.
- Accessibility: node bounds, parent/sibling relationships and control mapping.
- Contact editor: plant/lift semantics and reset/delete/split action admission.
- Finding browser: filter controls, visible row ordering and final sibling sentinel.

Current Stage1 `812c0547` compiled the report, reset, export review and path
review law files to objects without a stale override. Compilation checks source
acceptance; it does not prove their predicates. Updated producer verification
and certificate replay remain required for every strengthened law. Existing
baselines are retained and must not be weakened to accommodate new failures.

## Remaining audit

Review every Boolean law, including files that already contain some assertions.
A file-level search for missing `ensure` finds candidates but cannot establish
complete coverage. The accessibility unknown-identity law now excludes contact editor and issue
nodes as well as other recognized workspace categories. Its previous domain
included valid attached nodes, contradicting its name and intended predicate.
The existing contact and sidebar laws retain positive coverage for those nodes. Workspace root laws are being reviewed by their
implementation owner. Confirm intended true/false semantics and preconditions
before adding an assertion; never assume every Boolean return is intended true.

Job and legacy session law compilation was attempted after the compiler advanced
to `4c409da6`. The provenance gate rejected the preceding product as stale; no
override was used. Their compilation and replay remain pending a current build.

Accessibility law compilation/replay remains pending the current compiler and
proof assistant builds. No assertion has been claimed verified from old counts.

A per-function scan also found missing assertions in suggestion and workspace
root laws; their implementation owners are correcting them. This scan is only
an audit aid: assertions must cover the intended behavior, not merely exist in
a body. Finding and contact laws still require current-toolchain compilation
and replay. The existing assertions with false/equivalence outcomes were kept.

## Compilation follow-up on current Stage1

Stage1 `4c409da6` compiled job, legacy session and regression laws, plus the
full Studio entry point. Standalone accessibility law compilation initially
failed because `StudioAccessibility::NO_NODE` references UiCore's node capacity
without the law file including UiCore. The law now explicitly includes the
same UI core as its existing executable fixture; object compilation succeeds.
This expands the dependency closure and must be reflected in proof qualification
rather than hiding missing definitions or weakening assertions. Updated replay
and native interaction checks remain open.
