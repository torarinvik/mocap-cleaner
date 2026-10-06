# Mocap Cleaner — Product and Implementation Plan

Updated 2026-10-06. This roadmap describes remaining work. Completed
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

## Constant modules

Whenever a module contains multiple constant values, group those constants
in Elisa `const module` declarations. Give groups names that describe their
purpose (such as limits, actions or statuses), preserve public/private
visibility, and update callers and proof references. Use bare constant members
inside `const module` bodies. Apply this rule to existing code and every new
change, while retaining the 600-line maximum. See the
[constant module migration inventory](docs/plan/constant-modules.md).

## Detailed roadmap

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
- Preserve source takes; put derived files in `build/`.
- Land contracts and proof laws alongside proof-critical logic.
- Enforce the mandatory 600-line file limit on every change; see
  [module extraction details](docs/module-refactor.md).
- Record unresolved evidence in [proof gaps](docs/proof-gaps.md).
