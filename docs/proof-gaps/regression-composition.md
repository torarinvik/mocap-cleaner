# Report regression composition — 2026-10-06

Current prover `d3a17832` / compiler `4c409da6` proves and replays all 71 source
obligations in `src/core/regress.elisa`, including exact numeric availability.
The composed `proof/regress_laws.elisa` report remains incomplete:

- 171 obligations, 160 proved; 168 producer certificates, 160 replayed.
- Eight certificate replay gaps and three unproved source ensures.
- `exact_integer_availability_matches_domain`: `ambiguous-constant-goal` for
  equality between the availability and domain Boolean summaries.
- `growth_past_floor_regresses` and `growth_past_allowance_regresses`:
  `wrap-guard-fact` while composing allowance and regression summaries.

Derived evidence: `build/regress-current-proof.json` and
`build/regress-laws-current-proof.json`. These commands are proof checks, not
executable test runs. Replay failure must remain distinct from producer success.
The source result does not establish the composed laws or native report parser.

The prover owner has the exact findings. Preserve every law assertion, numeric
bound and regression baseline while investigating source-summary composition
and independent replay. Any repair requires rerunning these laws on its own
qualified binary; counts from another version are not current acceptance.
