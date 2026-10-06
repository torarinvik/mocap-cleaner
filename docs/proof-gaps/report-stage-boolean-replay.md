# Export report-stage Boolean branch replay

`StudioExportRecoveryReportStagePolicy::with_report` had three failed ensures
on returns below positive `json` branches. Negating the false-report contract
produced `not (current == value and not json)`, which De Morgan transforms to a
formula containing `not not json`. The producer simplified that proposition,
but the independent kernel replay did not.

Prover commit `3ac99624` adds the Boolean identity to both producer and kernel.
A clean candidate built from prover HEAD `3ac996241eaa10385e9cd78270cca5e759ff090b`,
with Stage1 `f292cbe0`, reports source 78/78 and laws 99/99, all certificates
independently replayed, zero findings. The focused branch repro replays 4/4.
The source report has two semantic normalization diagnostics and no errors.

The candidate is isolated; the default prover has not been replaced. Evidence
in the prover checkout:

- `build/summary-replay-clean-report-stage-source.json`
- `build/summary-replay-clean-report-stage-laws.json`
- `build/summary-replay-clean-false-branch.json`
- `build/elisa-proof-summary-replay-clean.manifest.json`
