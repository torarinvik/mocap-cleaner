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
`"host": "console"`, so the build omits the SDL3/Wicked application host.
A local compiler wrapper links the engine's portable `file_path.c` adapter
and the Elisa runtime for canonical path and source identity checks. Override
paths with `ELISA_ENGINE_ROOT`, `ELISAC` and, for a separate runtime build,
`MOCAP_CLI_RUNTIME`. The studio window has its own
`scripts/build_studio.sh` (elisa-ui AppKit host).

## Checking

```
scripts/check.sh
```
It incrementally builds and runs every test, then checks elisa-proof results
for regressions against `scripts/proof-baseline.tsv`. Known `unknown` and `unsupported`
results remain visible in the report; new files and worse results need review.

## CLI

```
mocap-cleaner clean in.glb --preset boxing -o out.glb --report r.json [--op balance|ballistic|momentum|...]
mocap-cleaner batch OUTDIR [--preset P] [--op ...] [--jobs N] IN.glb|FOLDER...   # writes OUTDIR/report.html
```

`--jobs N` cleans up to N takes at once in worker processes (output order
and report are the same as `--jobs 1`; 6 boxing takes: ~10.5 s serial,
~3 s with `--jobs 4`). Reports include CPU time per stage and per op
(`"time_us"` in JSON, a table in `report.html`).

When a take cannot be loaded or has no usable animations, `clean` reports the
import problem and exits unsuccessfully without publishing an output GLB.
Run `scripts/test_cli_import.sh` for the malformed-input regression check.

### Report and worker output publication

Report, saved-operation and worker part-file writers use exclusive creation.
They reject an existing destination, including a symlink created after the
initial path check. Report success requires every byte and file close to
succeed. A failed write can leave a partial newly created artifact; it reports
failure and does not overwrite another file. These libc IO adapters remain
runtime boundaries, not fully proved publication or crash-durability code.
