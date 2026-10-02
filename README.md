# Mocap Cleaner

A Cascadeur-style tool that does one thing: clean motion capture. See
[IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md).

- `src/core`: fixed-point kernels, namely fade, order statistics, spans, gating and the loop seam.
- `src/detect`: detectors for contacts and spikes.
- `src/physics`: centre of mass, support region, ballistic and momentum checks.
- `proof/`: elisa-proof obligations. Kernels in `src/` also carry their contracts inline.
- `test/`: runtime tests, where each `main` returns 0 on pass.
- `docs/proof-gaps.md`: prover limits found by this project, and their fixes.

## Building

```
scripts/build.sh                                  # -> build/mocap-cleaner
scripts/build.sh run -- clean in.glb --preset boxing -o build/out.glb
```
The CLI builds through Elisa-engine's `scripts/elisa_build_run.py` (from
`../elisa-engine-mocap`, branch `mocap-track`). `elisa.project.json` sets
`"host": "console"`, so the engine compiles `main()` straight to an executable
without the SDL3/Wicked application host. Override paths with
`ELISA_ENGINE_ROOT` and `ELISAC`. The studio window has its own
`scripts/build_studio.sh` (elisa-ui AppKit host).

## Checking

```
scripts/check.sh
```
It builds and runs every test, then runs elisa-proof on every source and proof file.

## CLI

```
mocap-cleaner clean in.glb --preset boxing -o out.glb --report r.json [--op balance|ballistic|momentum|...]
mocap-cleaner batch OUTDIR [--preset P] [--op ...] [--jobs N] IN.glb|FOLDER...   # writes OUTDIR/report.html
```

`--jobs N` cleans up to N takes at once in worker processes (output order
and report are the same as `--jobs 1`; 6 boxing takes: ~10.5 s serial,
~3 s with `--jobs 4`). Reports include CPU time per stage and per op
(`"time_us"` in JSON, a table in `report.html`).
