# Strict positive quotient bound replay

`ReportIndexKernel::midpoint` computes `first + (stop - first) / 2` for a half-open interval.
The proof assistant already bounded a nonnegative quotient by its dividend, but that only gave
`(stop - first) / 2 <= stop - first`; the midpoint contract needs a strict upper bound.

The signed division rule now adds `dividend / divisor < dividend` only after independently
proving `dividend > 0` and `divisor >= 2`. The replay kernel mirrors those side-condition proofs
and the same strict fact. Existing quotient facts and unrelated division cases are unchanged.

Focused reports from a separate candidate binary built from prover commit `1d33024c` and compiler
revision `f292cbe0766f2d5086f174c984b0f2cd0a64d85c` prove and replay the ReportIndexKernel source
13/13 obligations and laws 24/24, with zero replay gaps or findings. The candidate manifest has
clean prover and compiler source snapshots. The default executable was held unchanged during the
concurrent full check; it still needs a clean rebuild after that check terminates.
