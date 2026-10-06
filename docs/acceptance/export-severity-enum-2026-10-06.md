# Typed export report severity

Export severity is now a const enum with the existing wire values info 0,
warning 1 and error 2. Report warnings carry the typed severity, and formatting
matches all three variants explicitly. The policy retains an integer admission
predicate for wire validation; invalid wire values remain rejected.

Normal compiler `04b384ec` compiled the existing report test's composition
without diagnostics into `build/export-report-severity.o`; it was not executed.
Enum members use dot access. The initial colon-style member access produced
backend declines even though the compiler process returned zero; the final log
and emitted object establish successful compilation after correcting access.

Clean candidate prover `3ac99624` independently replays policy 23/23 and law
composition 48/51. The same three duration wrap-guard laws remain open; no
baseline was weakened. Evidence is in `build/export-report-severity-*.json`.
Studio caller integration is owned by the recovery integration agent and its
combined build remains to be qualified. Native warning presentation and full
report runtime qualification remain open.
