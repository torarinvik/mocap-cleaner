# Metric evidence states

`StudioMetricEvidencePolicy` distinguishes unknown, measured pass, measured
fail and inapplicable preservation evidence. An applicable metric needs
available data, positive sample count and a failure count between zero and
sample count. Zero failures pass; a positive valid failure count fails.
Missing data, empty samples and invalid counts are unknown, never zero-error
passes. Only pass and explicitly justified inapplicability admit a gate.

Callers must establish applicability and measurement availability from actual
rig/tool/data facts. A user preference cannot make a required preservation
metric inapplicable. This kernel does not choose thresholds or measure poses;
it classifies already measured outcomes. Sample exclusions and units belong
in the acceptance record and product explanation.

Policy: 39/39 proved. Laws: 55/55 proved and independently replayed with no
gaps/findings. Suggestion/comparison integration and the missing preservation
measurements remain open; this kernel alone does not complete M3. Compilation
is pending the current compiler provenance renewal.

## Typed evidence state

Evidence states now use `const enum State of i64` with typed classification
and admission APIs. Required values remain Unknown=0, Pass=1, Fail=2 and
Inapplicable=3. This is a finite-choice type, rather than an integer constant
group. No raw decode boundary is currently needed by its product callers.

The earlier 39/39 and 55/55 results qualified the integer representation.
The current older prover reports 14/39 source and 22/64 law obligations for
the typed representation. Strong reviewed baselines are retained; upgrading
the proof branch and compiler is in progress before accepting this migration's
proof gate. The migration is not claimed fully verified.
