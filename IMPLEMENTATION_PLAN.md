# Mocap Cleaner — Product and Implementation Plan

Updated 2026-10-07. This roadmap describes remaining work. Completed
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

## Detailed roadmap

- [Acceptance, dependencies and unresolved decisions](docs/plan/acceptance-and-dependencies.md)
- [Pending current-toolchain policy qualification](docs/acceptance/pending-policy-qualification-2026-10-06.md)
- [Product goals, user journeys and baseline](docs/plan/product-and-m0.md)
- [M1: workspace, storage and recovery](docs/plan/m1-workspace.md)
- [M2–M3: diagnosis, guided cleanup and comparison](docs/plan/m2-m3-diagnosis-review.md)
- [M4: contact cleanup and precise repair](docs/plan/m4-contact-repair.md)
- [M5: responsiveness and reliability](docs/plan/m5-responsiveness.md)
- [M6: export, recipes and batch production](docs/plan/m6-export-batch.md)
- [M7: release qualification](docs/plan/m7-release.md)
- [M8 and first implementation slices](docs/plan/m8-research-and-order.md)

## Delivery requirements

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
