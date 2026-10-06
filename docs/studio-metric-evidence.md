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
