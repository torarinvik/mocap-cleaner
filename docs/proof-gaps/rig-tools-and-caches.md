# Rig tools, physics and caches (G21–G42)

[Proof gap index](../proof-gaps.md)

## Rig tools (2026-10-01)

- G21 (new): a negative named constant (`const NONE: i64 = -1`) anywhere in a
  module makes unrelated linear goals fail with `ambiguous-constant-fact`.
  Repro: scratch `amb_neg_const.elisa` (one constant `NONE = -1`, `f` returns
  `role`, `role + 4` or `role - 4` under `role <= 5` / `role <= 9`; ensure
  `result < 26`). Workaround: `const NONE: i64 = 0 - 1`. Fixed in
  elisa-proof-mocap 41f7322 (the premise is dropped, so a goal that needs
  `NONE`'s value still wants the `0 - 1` spelling).
- G22 (new): a goal that folds to literals under an equality path fact is
  refused with `ambiguous-constant-goal`, even with no constants in scope.
  Repro: `ensure result < 0 or result >= 22`, body `return role + 14 if
  role == 8`, `return -1`. Fixed in elisa-proof-mocap ae85975;
  `Roles::hinge_roll` now carries the contract.
- C3 (compiler): an `enum Kind` in a second module (`RigOps`) is picked up by
  unqualified `Kind.X` patterns in another module's `match` (`Ops::candidate`),
  which then fails as non-exhaustive ("may fall through"). Renamed to `RigKind`.
  Fixed in Elisa-compiler 61ca4e25 (branch fix/local-shadows-global).
- `pass` is reserved in stage1.
- New kernels and laws fully proved: roles 8/8, hinge 11/11, reach 1/1, pin 17/17,
  offset 8/8; roles_laws, hinge_laws, reach_laws, pin_laws all proved.

## Phase 1 rig tools, part 2 (2026-10-01)

New kernels: `Pivot` (choose, shift, settle), `Contact::edited`,
`Offset::segment_share` / `Offset::keyed`, `Codec` (ops file digits). All
kernel files and `proof/pivot_laws`, `keyed_laws`, `edit_laws`, `codec_laws`
prove fully. Gaps found on the way (worked around, not fixed in the prover):

- G23 (new): an unqualified call to a sibling function resolves by bare name
  across modules. Adding `Offset::ramp` made `Fade::weight` / `eased_weight`
  (which call `Fade::ramp` unqualified) fail with call-requires errors.
  Workaround: renamed to `segment_share`. The compiler resolves it correctly.
- G24 (new): `wrap-guard-goal` refuses `a0 + f(...)` when the call result is
  bounded only relationally (`result <= span`, `span = a1 - a0`), although
  the facts are present. Workaround: an absolute ensure
  (`result <= 2000000000`) on the callee.
- G25 (new): the nonlinear local `(a1 - a0) * (frame - f0) / (f1 - f0)`
  inside a function drops every later goal of that function, even ones that
  only need the clamping branches. Workaround: move the product into its own
  contracted helper (`segment_share`).
- G26 (open): modular and division round trips are not proved:
  `(acc * 10 + d) % 10 == d`, `(acc * 10 + d) / 10 == acc`, and
  `in_limit(push_digit(acc, d))` for `acc <= 99999999999`. The ops-file round
  trip is covered by `test/rig_tools.elisa` instead.
- `ensure result == (A and B)` on a bool function is not usable by callers
  for `not result` goals; split into implications (`Codec::kind_ok`).

## Physics and batch (phase4-5, 2026-10-01)

No prover changes were needed; these limits were worked around in our code.

- G27: partial functions (with `requires`) cannot be called inside `ensure`
  or `requires`. Laws call them in the body instead.
- G28: a mutable accumulator in a proved function fails with
  `resource-write-readonly`, so `mass_total` is a single sum expression.
- G29: many disjunctive ensures on one callee time out its callers.
  `segment_kind` uses two linear bounds instead of one case per segment.
- G30: integer division by a constant inside a callee is not unfolded for
  callers (`(s - 3) / 2`). Workaround: explicit branches.
- G31: returning an `and` chain of comparisons fails where the same test
  written as early returns proves (`Balance::unbalanced`).
- Not provable modularly, so tested at runtime instead: winding-free
  support triangles, counter-clockwise support kept, the weightless chord
  law, and roll conservation across hinge and roll bone (G10/G12 family).
- `proof/flight_laws.elisa`: 615/0 proved. Impure files (`rig_physics`,
  `folder`, `report`, `main`) are `unsupported` like every `src/io` file was
  at baseline.

## Operation-stack cache (phase0-finish, 2026-10-01)

No prover changes were needed; worked around in `src/core/stack_cache.elisa`.

- G32: a local bound by a conditional expression (`low: i64 = a if a <= b
  else b`) loses its facts for the following `return`. Explicit branches prove.
- G33: a three-way disjunctive equality ensure (`result == a or result == b
  or result == c`) is not usable by callers that feed the result into another
  call; restated as one implication per case.
- G34: `requires i + 1 < Module::CONST` does not establish `i < CONST` at a
  call; `requires i < Module::CONST - 1` does.

## Studio caches (studio-perf, 2026-10-02)

Prover: `../elisa-proof-mocap/build/elisa-proof` at d1f61d0, unchanged. The
workarounds are in `src/core/perf_cache.elisa` and
`proof/perf_cache_laws.elisa` (34 laws, all proved).

- G35: a callee's `ensure result == e` cannot be used by a caller that passes
  the result on to another call (`lo: i64 = h(x)` followed by `d(f, lo)` is
  `unknown`). The same fact written as `result >= e` plus `result <= e`
  proves.
- G36: a `bool` callee with both `not result or P` and `result or Q` ensures
  makes callers that compose it time out (`dirty` after `take_lo/take_hi`).
  `dirty`, `memo_hit` and `on_chain` therefore return an i64 0/1 flag, and
  callers compare it with `== 1`.
- G37: once a callee has a `requires`, its ensures are often lost when its
  result feeds a second call. This holds even when the precondition plainly
  holds at the call: a one-line `h(x)` with `requires x >= 0` works without
  the requires and fails with it. So the laws that composed `margin_lo`,
  `margin_hi`, `empty_lo/empty_hi` and `memo_key` with `dirty`/`span`/
  `memo_hit` are stated over the window bounds those callees ensure. Those
  ensures are proved on the kernel itself.
- G38: comparisons against a negative constant are brittle. `ensure result <
  0` with `return -1` (or `0 - 1`) is `unknown`, while `result <= 0 - 1`
  proves. `requires hi >= NONE` (NONE = -1) was not established from `hi >=
  0` at a call. Written as `requires hi + 1 >= 0`; the empty-window laws take
  `hi < 0` as a parameter.
- G39: a law whose `requires` mentions `frames - 1` without a lower bound on
  `frames` fails the callee precondition, even though nothing overflows.
  `requires frames >= 1` and `hi < frames` prove.
- G40: slot and memo-key distinctness (`slot(t, a) != slot(t, b)` for
  `a != b`, which has constant multipliers) times out. It is stated as
  ordering (`a < b` implies `slot(t, a) < slot(t, b)`), which proves.
- G41: a law's callee precondition that follows only by implication (callee
  `requires shortest >= 0`, law has `hi >= 0` and `hi < shortest - 1`) proved
  when the law was checked alone, but went `unknown` once a sibling law over
  the same kernel (`window_end`) was in the file. Stating `requires shortest
  >= 0` (and an upper bound) directly on the law proves.
- G42: monotonicity of `window_end` (`a <= b` implies `window_end(a) <=
  window_end(b)`) times out, also when split into the two branches of the
  kernel. The law is dropped; the kernel's ensures (end is `hi` inside the
  keys, the clip's last frame otherwise) give it by hand.

