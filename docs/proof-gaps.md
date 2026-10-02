# elisa-proof gaps found by the mocap cleaner

Fixes are developed in the `../elisa-proof-mocap` worktree, on branch
`mocap-cleaner-proofs`.

| # | Gap | Example | Status |
|---|---|---|---|
| G1 | Division by a variable was refused (wrap guard) | `d / e >= 0` with `e >= 1` | Fixed: interval rule in the checker and the kernel replay |
| G2 | Relational division, e.g. `a * K / b <= K` when `a <= b` | `Fade::scale` needs a clamp instead | In progress |
| G3 | `a % b < b` for a symbolic `b` | `Span::wrap` | In progress |
| G4 | `A or B` goals are proved only by proving one side alone; there is no "assume not A, prove B" | `Fade::edge_distance`, `Span::contains`, `Contact::step` | In progress |
| G5 | A negated compound comparison, e.g. `not (frame <= count - 1 - frame)`, times out on budget | Fixed in our code with a proved `nearer` helper | Workaround |
| G6 | Refinement-typed parameters, `type Permille = i64 where …`, contribute no facts | Probe `ref.elisa` | In progress |
| G7 | `law` exists only inside protocols; there is no top-level reusable law | — | Investigating |
| G8 | Calls inside `ensure` are not unfolded | Earlier `Order::median3` | Workaround: branch form |
| G9 | No reasoning about float values (refused because of NaN) | All float kernels | Design choice: proof-critical logic uses integer fixed point; float math comes from engine M08 |
| G10 | No model of darray contents (backlog E-01) | Whole-track properties | Open: prove per-element kernels, test whole tracks |
| G11 | `x >= 0` does not follow from the negation of `x < 0` within budget when `x` is a local built from other locals | `Balance::ballistic_residual` | Open |
| G12 | Nonlinear products of parameters, e.g. a cross product, cannot be related | `Balance::side` degenerate cases | Open (needs case lemmas) |

## Compiler notes (Elisa stage1, not the prover)

- C1: passing a `darray[u8]` by value to a `darray[u8]&` parameter, or a `cstr`
  to an `sview` parameter, is not a type error: the backend emits invalid LLVM
  IR ("backend generated invalid LLVM IR") with no source location. Found while
  building the batch CLI; worked around with `&html` and `Out::c_text`.
- C2: `is` is reserved; `x!` optional unwrap does not parse (use flow narrowing
  after `!= null`).
- G13: callers cannot use a callee's disjunctive ensure by modus ponens
  (`k: a != b or result == b`; `k(v, v)` does not give `result == v`).
  Blocks most laws in `proof/*_laws.elisa`. Sent to the prover agent with task (b).

## Status after prover commits 4517ba1, fefdb89, 445c4be (2026-09-30)

- G4 (disjunction goals) and G13 (using disjunctive ensures): fixed (fefdb89).
- G3 (`a % b < b`) and G2 (variable-divisor division bounds): fixed for signed
  terms with `b >= 1`, `a >= 0` (445c4be). `(a / b) * b <= a` is still open.
- G6 (refinement parameters): fixed. `type T = i64 where ...` parameters become
  requires and returns become ensures (4517ba1).
- G7: `law` drops its parameters; use `lemma name(params):` with
  `assert P by: name(args)` instead.
- G14 (new, the main blocker): call results whose arguments contain arithmetic
  (`nearer(frame, last - frame)`) get no facts, and locals are inlined into
  them. Blocks Fade and, through it, Gate, Seam, Stability and most laws.
  Assigned to the prover agent as task (d).
- Fully proved now: Order, Span, Smooth, Contact.
- G14: fixed by the prover's task (d) commit: equality goals are now split into `<=` and `>=`, and
  calls are accepted inside `or` goals. Fade is fully proved; gate 10/12, seam 6/7, fade_laws 5/11.
- G15 (new): no relational facts for division by a literal (`0 <= a/2 <= a`
  given `a >= 0`). Blocks Stability. Assigned to the prover agent as task (e).
- Prover self-audit exceeds the 1.2 GB memory watchdog (1.33 GB at 445c4be),
  which predates these changes. Not raised here; it's the prover owners' call.
- G15: fixed (091d83c): division by a positive literal now has relational bounds. `soften` is proved.
- Watchdog raised to 3 GB with the user's approval (e5a565c); the self-audit
  now completes. Peak RSS for the whole run was 3.04 GiB.
- G16 (new): module-qualified constants (`Fade::MAX_FRAMES`) in contracts are not resolved. Replacing them with literals takes fade_laws from 5/11 to 9/11. Assigned to the prover agent as task (f).
- G16: fixed (76c3fab). Constants were resolved only for root-level functions, so functions inside modules missed them.
- Added `Fade::scale: distance < edge or result == FULL` and
  `Fade::weight: not looping or result == FULL`, so loop_is_full and saturates prove. fade_laws is now 10/11.
- G17 (new): budget sensitivity. With the extra disjunctive ensures,
  `last_frame_unfaded` (which proved before) now stops at the `budget` gate. Adding
  true facts should not lose a proof; case splits on disjunctive callee facts need
  pruning, e.g. drop a disjunct once a literal argument refutes it.
- G17: fixed (152ccb3). Disjuncts that literal arguments already decide are pruned before case splitting; fade_laws is now 11/11.
- 907e795: comparisons that cancel to one name times a coefficient are now decided, so limit_step proves.
- G18 (new, prover task h): literal call arguments lose their width inside callee preconditions.
  Blocks most stability and physics laws.
- G19 (new, prover task i): `-literal` bounds are not read by the arithmetic tiers.
- G20: there is no general linear-arithmetic tier, e.g. for ballistic_residual, side, accel,
  limit_wring and magnitude case splits. A design note was requested before work starts.
- Triage found no missing kernel ensures in mocap-cleaner; every remaining open law is a prover gap.
- G18/G19 fixed (81a9cf3, b147bea); qualified call widths (j), linear Fourier–Motzkin tier with
  Farkas kernel check (k), and `y + -k` replay (l, 374a404) landed. Now: contact 9/10, fade 11/11,
  gate 11/18, order 10/11, physics 6/18, seam 6/13, span 13/14, stability 5/7.
- Prover c57ebef..c91d462 (call-result generalisation, disequality refutation, width stability,
  term-equality bounds, owner-module call resolution) plus mocap contracts ef99aba/6c626ac:
  98/102 laws proved. Open: gate first_frame_is_source, last_frame_is_source, full_weight_is_fix;
  seam jump_symmetric.
- Prover 9e656d9 (constant facts across calls), d5ad82f (callee-requires constants),
  dd8d9df (field-place swap no longer costs split depth), 36ed514 (per-function JSON incl.
  file-level findings): all 102 laws in proof/*.elisa proved, 0 replay gaps.
  proof_status.py now reads functions[].proved so file-level findings count as open.
  Known prover-side leftovers: compiler duplicate-alias wording drift (Elisa-compiler),
  census baseline from 09-30 not re-baselined.

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

## Foot cleanup (studio-foot, 2026-10-02)

The prover (`../elisa-proof-mocap/build/elisa-proof`) was not edited; every
gap below was worked around in our code.

- G43: parameters named `to`, `from` or `new` are parse errors.
- G44: returning a negative constant (`return -1`) does not establish an
  ensure that names it; a named constant does.
- G45: a bool-equality ensure (`result == (a < b)`) reached through a
  disjunction fails; split into one helper per case
  (`StudioFoot::first_planted` / `last_planted`).
- G46: a law returning an `and` of conditions fails; one law per condition.
- G47: implication ensures over a bare bool parameter
  (`not is_first or ...`) do not prove when the result is a bool.
- G48: a law over the reflexive call `moved(v, v)` with `ensure not result`
  proves but has a certificate replay gap (state "unknown"); the i64 form is
  unproven. Replaced by `other_frame_is_moved` (`moved(v, v + 1)`).
- G49: literal bounds in clamps prove where `-LIMIT` in an ensure, or
  `Order::clamp` with negative bounds, does not.
- G50: nonlinear sign facts (`a * b >= 0`) time out; summing two carries in
  one expression times out; nested call arguments are unsupported.
- G51: `return x if a or b` fails where two separate return-ifs prove.
- G52: callers get no overflow obligations, so the `LIMIT` requires are
  ours, not the prover's.

- G53: constant and function names are global across included modules in
  goals: a kernel declaring `ease`, `nearer`, `LIMIT` or `FULL` next to
  `Fade`/`Order` breaks the other module's proofs (ambiguous-constant-goal).
  Knee renamed its helpers.
- G54: facts on a local built by subtraction (`kept: i64 = x - away`) refuse
  with wrap-guard-fact even with bounded operands; a helper whose ensures
  carry the bounds (`Knee::keep`) proves. Laws calling a kernel through a
  local hit the same gate, so laws call the kernel inline.
- G55: `start_is_gentle` (soft reach has slope one at the zone start) could
  not be stated without a product of two variables; dropped.
- G56: a law returning `bool` with `ensure result` that calls a kernel with
  literal arguments (`help_after(false, true, false)`) often fails; the same
  fact proves as an i64 law (`ensure result == N`), with the literal bound
  through `requires x == literal`, or as `ensure not result`. Kernel bool
  ensures written `result == (a and b)` fail where split `or result` /
  `or not result` clauses with explicit `true`/`false` returns prove. A
  disjunctive requires over five flags times out (`escape_never_idle`,
  replaced by one `lone_*` law per layer).
- G57: `session_clamp` cannot also ensure `value + bound >= 0 or result +
  bound == 0` (the low saturation), although the upper one proves; the law
  `small_quat_saturates` was dropped and the low side is covered by
  `result + bound >= 0` plus the session test. An idempotence law
  (`clamp_settles`, clamp of a clamp) did not prove either and was replaced
  by `zero_stays_zero`.
- G58: the Part A additions to `rig_stack.elisa` add 198 proven and 22
  unproven obligations to each driver file that includes it (main, ops_file,
  presets, rig_cache, rig_stack, rig_physics). Those files were already
  "unsupported" in the baseline and stay so; the stack and corrections
  kernels themselves improved.
- G59: laws restating `param_unit` for kinds 4 and 5 time out when the
  whole law file is proved (other kinds prove); the kernel's own ensures
  state those cases and prove, so the two laws were dropped. Laws fixing
  `wring_degrees` at literal values (200000 reads 23) do not prove through
  the division; the session/units test checks them instead.
- G60: the G56 bool-literal gap is asymmetric: `edit_applies(HAND_LEFT,
  HAND_LEFT)` proves `ensure result` but the identical RIGHT law does not;
  binding the role through `requires role == HAND_RIGHT` proves
  (`HandLaws::right_edit_reaches_right`).
- G61: from a callee's `ensure result == point - plane` the caller cannot
  conclude `result + plane == point`; the law states the subtraction form.
- G62: bounds of `size * tol / 1000` (`>= 0`, `<= BOUND` for bounded
  operands) are not derived (G2-like); `Regress::allowance` clamps the part
  explicitly so callers get its upper bound.
- G63: callers cannot use a callee's disjunctive ensure (G13 instance):
  laws over `Knee::speed_budget` failed, so `Hand::elbow_budget` restates
  the budget with case-wise `x > MIN or result == MIN` ensures.
- G64: `src/io/report_diff.elisa` (JSON scanner, file I/O) is unsupported
  like the other io modules; its verdicts go through the proved `Regress`.

- G65 (Phase 6, `slide`): callee summaries are dropped when the callee's ensures
  use `2*result`, disjunctions or parity, so state bounds directly. A
  requires `x + c < y` fails where `x < y - c` proves; `result == frame +
  reach` proves where `result - frame == reach` does not. Modulo laws over
  sums and large bounds with division time out (`Slide::flip`, and
  `SEARCH_MAX = 2001`). Finding line numbers refer to the concatenated
  include unit, not the source file.

- G66: file chords were first one two-argument kernel (`file_chord(mask, letter)`);
  its per-case laws timed out, so the chords are three one-argument kernels
  (`o_chord`, `s_chord`, `e_chord`). A disjunctive ensure such as
  `(mask != 1 and mask != 3) or ...` also failed and is split into two
  ensures (G13). `load_take` and the panel calls are app driver code (G58).


## Range retiming (retime, 2026-10-02)

The prover (`../elisa-proof-mocap/build/elisa-proof`) was not edited; every
gap below was worked around in our code.

- G67: a bool result built from `and`/`or` cannot be negated by the prover
  (`ensure not result or ...` fails); `Retime::disjoint` and
  `Retime::range_ok` use explicit `return false if` branches instead.
- G68: inside an included module, an unqualified call resolves to a
  same-named function of the including module. `Retime`'s helpers became
  `range_distance` / `range_weight`, and the engine's
  `GlbResize::push_count` became `resize_count` (it was captured by
  `StudioHistory::push_count` once the studio included it; elisa-engine-mocap
  700efa62).
- G69: contract bounds written as `frame * 1000` fail; callers pass
  pre-scaled milli-frame times (`Retime::time_of`).
- G70: ensures that reconstruct a time through division
  (`result * UNIT / span == ...`) time out; `rescale`, `forward_between` and
  `invert_between` state bounds and exact endpoints only.
- G71: a conditional early `return move out if ...` is treated as an
  unconditional move, so every later use of `out` is reported as a
  disproved use-after-move. `RetimeApply::ranges_of` / `source_times`
  return a fresh empty array from an `if` block instead.
- `src/ops/retime_apply.elisa` includes `rig_stack.elisa` and so inherits its
  state ("unsupported", the same class as `ops_file`, `rig_cache` and
  `rig_stack` on main, whose counts are unchanged). The time-map decisions it
  makes go through the proved `Retime` kernel.
