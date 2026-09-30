# Mocap Cleaner

A Cascadeur-style tool that does one thing: clean motion capture. See
[IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md).

- `src/core`: fixed-point kernels, namely fade, order statistics, spans, gating and the loop seam.
- `src/detect`: detectors for contacts and spikes.
- `proof/`: elisa-proof obligations. Kernels in `src/` also carry their contracts inline.
- `test/`: runtime tests, where each `main` returns 0 on pass.
- `docs/proof-gaps.md`: prover limits found by this project, and their fixes.

## Checking

```
scripts/check.sh
```
It builds and runs every test, then runs elisa-proof on every source and proof file.
