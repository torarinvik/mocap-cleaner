# Export duration arithmetic bound

The duration API now guarantees its result is at most
`Timing::MAX_FRAMES * 1000` milliseconds, in addition to non-negativity and
the exact floored division equation. This exposes the existing input-derived
upper bound to callers doing further arithmetic; the implementation and law
claims remain unchanged.

Normal compiler `04b384ec` compiled the law composition without diagnostics.
Default prover `5776350b` and clean candidate `3ac99624` independently replay
the policy 23/23. Its reviewed baseline advances by one obligation.
The expanded law composition replays 48/51: the same three exact-duration
laws remain open at `wrap-guard-goal`. The reproduction was sent to the
prover repair agent; no law was weakened and no law baseline was relaxed.

Evidence is in `build/export-duration-bound-{source,laws,default}.json`
and `build/export-duration-bound-compile.log`. No executable tests were run.
