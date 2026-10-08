# Mocap Cleaner — Product and Implementation Plan

Updated 2026-10-08. This roadmap describes remaining work. Completed
implementation is recorded in Git. Milestone documents retain their original
section numbering and detailed acceptance criteria.

The product goal is a clear, safe workflow from unfamiliar capture to reviewed
export, with understandable diagnosis, recoverable cleanup and responsive
professional tools.

## Mandatory file size limit

Every maintained repository file must have **at most 600 lines**. This applies
to existing and new source, proof, test, script, configuration and documentation
files throughout every milestone. Split growing files into cohesive modules
before an edit would exceed the limit; use nested modules when appropriate,
keep helpers private and expose only the APIs callers need. Preserve includes,
behavior and proof coverage, and check file lengths before committing. Generated
`build/` artifacts and sibling repositories are outside this repository rule.

## Constants and finite choices

Choose the representation that expresses the domain: prefer a `const enum`
for a closed set of alternatives, and an algebraic data type when alternatives
carry different data or must exclude invalid combinations. Use purpose-specific
`const module` groups for related numeric limits, units or configuration values
that are not better represented by those types. This applies to existing code
and every new change. Preserve public/private visibility, contracts, proof
coverage and the 600-line maximum. Update all consumers and validate explicit
conversions at serialization/native boundaries; preserve required wire values.
See the [representation migration inventory](docs/plan/constant-modules.md).

## Highest-return execution focus

Follow the [ranked delivery queue](docs/plan/current-delivery-queue.md):
current runnable build and redraw crash; clear FBX/workspace recovery;
safety-critical proofs; one complete cleanup journey; single export and
recoverable storage; responsiveness; repeat work and release; M8 decisions.
Finish and qualify existing production paths before adding another algorithm.
All M0–M8 requirements remain in scope; priority changes do not waive acceptance.

## Detailed roadmap

- [Current delivery queue and finish criteria](docs/plan/current-delivery-queue.md)
- [Acceptance, dependencies and unresolved decisions](docs/plan/acceptance-and-dependencies.md)
- [Pending current-toolchain policy qualification](docs/acceptance/pending-policy-qualification-2026-10-06.md)
- [Recent law source compilation; proof qualification pending](docs/acceptance/current-law-source-compile-2026-10-07.md)
- [Product goals, user journeys and baseline](docs/plan/product-and-m0.md)
- [M1: workspace, storage and recovery](docs/plan/m1-workspace.md)
- [Generated-build cleanup delivery slices](docs/plan/generated-build-cleanup.md)
- [M2–M3: diagnosis, guided cleanup and comparison](docs/plan/m2-m3-diagnosis-review.md)
- [M4: contact cleanup and precise repair](docs/plan/m4-contact-repair.md)
- [M5: responsiveness and reliability](docs/plan/m5-responsiveness.md)
- [M6: export, recipes and batch production](docs/plan/m6-export-batch.md)
- [M7: release qualification](docs/plan/m7-release.md)
- [M8 and first implementation slices](docs/plan/m8-research-and-order.md)

## Delivery requirements

- Enforce `Global.Read` for reads and `Global.Write` for writes to `global mutable`
  storage, including transitive callers and callbacks. Declare the effect rows and
  grant access at the narrow owning scope; read-modify-write needs both members.
  Preserve propagation with `can`; use `trusted` only at an explicitly reviewed
  tracking boundary. Enable the current compiler's global permission checking
  during qualification and refuse ungranted access. Migration is incomplete until
  the full application and dependency call graph pass that check.
- Use grouped family grants when a row names multiple members of the same
  family, for example `can[Memory{Allocate, Release}, Global{Read, Write}]`.
  Preserve the exact member set and unsafe tracking; qualify compiler expansion
  and member-specific refusals before treating the syntax as supported.
- Commit each small improvement.
- Extend arrays for fixed sequences of literals. The lexical
  `scripts/check_literal_push_runs.py` gate rejects consecutive integer-literal
  pushes to the same array; review other literal forms manually.
- Use the latest compiler, proof assistant, Elisa UI and engine dependencies,
  retaining required mocap fixes.
  Record fetched upstream revisions, source changes and binary manifests; rebuild
  stale products before acceptance. Build scripts must not silently permit stale
  binaries or select historical worktrees. Explicit historical comparisons remain
  separate from current-snapshot qualification. See the
  [dependency freshness audit](docs/acceptance/dependency-freshness.md).
- Preserve source takes; put derived files in `build/`.
- Land contracts and proof laws alongside proof-critical logic.
- Enforce the mandatory 600-line file limit on every change; see
  [module extraction details](docs/module-refactor.md).
- Record unresolved evidence in [proof gaps](docs/proof-gaps.md).
- Apply the shared evidence and dependency requirements before closing any
  milestone; distinguish implementation from native and user acceptance.

## Current user priority: FBX and character review

Deliver [FBX opening and Character/Skeleton review](docs/plan/fbx-character-import.md)
with source-preserving import and editable posed surfaces. This remains part of
the full roadmap and precedes further cleanup expansion.
