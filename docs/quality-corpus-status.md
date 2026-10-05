# Motion quality corpus status

Updated 2026-10-05. This inventory distinguishes executable evidence from
candidate benchmark material. It does not claim that the release corpus,
licensing review, expected-intent labels or visual gates are complete.

## Evidence available in this checkout

| Evidence | Existing coverage | What it does not establish |
|---|---|---|
| `test/foot_lock.elisa` | Synthetic 30-frame translating foot, contact interior, blend boundary, outside range and already-still negative case. | It is a one-dimensional unit test, not a character take or toe/heel intent review. |
| `test/foot_clips.elisa` and `docs/foot-workflow.md` | End-to-end slide, sink and knee-pop comparison across the animations in `../elisa-boxing-game/build/dual-stance/black/black-boxer.glb`. The docs retain a 28-row result table and per-tool acceptance tolerances. | The GLB is external and not checked into this repository. `test/foot_clips.elisa` skips when it is missing; current fixture provenance/license and repeatable animation names/intent labels are not recorded here. It tests foot cleanup and knee transitions, not the full user workflow. |
| `test/physics_rig.elisa` | When that external boxing take exists, checks a jab's balance/momentum behavior and injects one synthetic hip flight bump to check ballistic repair. | It is not a set of independent jump/landing or unusual-rig source takes. The mixed real/synthetic result is not an animator-reviewed benchmark corpus. |
| Track/kernel tests (`test/stability.elisa`, `test/track_kernels.elisa`, `test/core_kernels.elisa`) | Fixed-point and integer synthetic spike, boundary, smoothing and seam cases. | No per-frame whole-body preservation, camera review, contact annotation or realistic noise distribution. |
| GLB/session/export tests | Generated small documents exercise malformed structure, round-trip bytes, sessions, path safety and publication failures. | Generated documents are structural safety fixtures, not quality takes. No tracked large or multi-animation capacity corpus was found. |
| Build artifacts under `build/` | Recent local GLBs and reports used by CLI parity and focused checks, all derived files. | These are disposable outputs, not immutable benchmark inputs or provenance records. Do not promote an output to source corpus without preserving the original and recording its identity. |

No `.glb` source fixture is tracked under this repository's normal source
paths. The only real-take reference found is outside the checkout. The
`scripts/check.sh` integration path conditionally runs CLI/foot regressions
when that external boxing take exists, so a successful run without it is not
evidence that the real-take cases executed.

## Corpus still required by M0

Create or license immutable inputs for the following, and keep generated
results only under `build/`:

- short and long boxing with labeled jab/cross/guard contacts;
- walk/run with planted and deliberately sliding steps;
- idle jitter, sensor spikes and a clean negative-control take;
- fast turns, pivots and toe/heel rolls that must retain timing and shape;
- jumps, landing transitions, balance changes and genuine airborne intervals;
- planted hand contact against a wall/object and an intentional release;
- unusual proportions, mirrored rigs, missing optional roles and long names;
- noisy capture plus a clean counterpart and fixed random seed metadata;
- a long high-channel-count clip and a multi-animation GLB, including one
  deliberately malformed/oversized companion.

Every take needs a source hash, acquisition/license note, rig and animation
identity, frame count/rate, unit/floor/contact annotations, expected intent,
known limitations and an immutable-file check. Negative controls must say
which motion changes are intentional. A detector's prediction is not the
ground-truth label.

## Reproducible benchmark record

For each corpus revision, keep a manifest with source SHA-256, tool/compiler
revision, exact command, hardware/OS, animation identity and evaluator notes.
Write cleaned GLBs, reports, screenshots and per-run timing/memory summaries
to a unique `build/benchmark/<run-id>/` directory; never overwrite the input.
Report worst frame, p95 and aggregate values with units for foot/hand slide,
floor penetration, knee/elbow angular jumps, endpoint drift, seam/fade
discontinuity, runtime, memory and dropped preview frames. Include raw source
and result values at every reported peak, and list excluded/unmeasurable data.

The numerical run is necessary but not sufficient: capture source/result
views around every peak and contact boundary. A named animator must review
each candidate and negative control for recognizable timing, impact and
deliberate motion before defaults or recommendations are promoted.
