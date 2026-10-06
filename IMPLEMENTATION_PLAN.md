# Mocap Cleaner — Product and Implementation Plan

Updated 2026-10-06. This roadmap describes remaining work. Completed
implementation is recorded in Git. Milestone documents retain their original
section numbering and detailed acceptance criteria.

The product goal is a clear, safe workflow from unfamiliar capture to reviewed
export, with understandable diagnosis, recoverable cleanup and responsive
professional tools.

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
- Keep public APIs narrow and every repository source/document file at most
  600 lines; see [module extraction plan](docs/module-refactor.md).
- Record unresolved evidence in [proof gaps](docs/proof-gaps.md).
