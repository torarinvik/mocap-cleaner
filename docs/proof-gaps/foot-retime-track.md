# Foot cleanup, retiming and tracks (G43–G82)

[Proof gap index](../proof-gaps.md)

## Foot cleanup (studio-foot, 2026-10-02)

G67-G71 and G73 were worked around in our code. G72 was fixed in our code
and G74 in the prover (`../elisa-proof-mocap`, branch `mocap-cleaner-proofs`,
3244c9d). Both `src/core/retime.elisa` and `proof/retime_laws.elisa`
now prove completely with every certificate replayed.

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

G67-G71 and G73 were worked around in our code. G72 was fixed in our code
and G74 in the prover (`../elisa-proof-mocap`, branch `mocap-cleaner-proofs`,
3244c9d). Both `src/core/retime.elisa` and `proof/retime_laws.elisa`
now prove completely with every certificate replayed.

- G67: a bool result built from `and`/`or` cannot be negated by the prover
  (`ensure not result or ...` fails); `Retime::disjoint` and
  `Retime::range_ok` use explicit `return false if` branches instead.
- G68: inside an included module, an unqualified call resolves to a
  same-named function of the including module. `Retime`'s helpers became
  `range_distance` / `range_weight`, and the engine's
  `GlbResize::push_count` became `resize_count` (it was captured by
  `StudioHistory::push_count` once the studio included it; elisa-engine-mocap
  700efa62).
  Constants are captured the same way: in `retime_apply` (which also
  includes `rig_stack` and `knee`), `Retime`'s `MAX_SPEED` resolved to
  `RigStack::MAX_SPEED: f64` (its contracts were rejected), and `MIN_SPEED` was exposed to the same
  capture by `Knee::MIN_SPEED = 2000`. `Retime`'s bounds are now
  `MIN_RATE` / `MAX_RATE`; writing `Retime::MAX_SPEED` inside the module
  did not help.
  Constant half resolved in elisa-proof-mocap 0c1a6df: module constants are
  owned by their module, bare names resolve to the function's own module, and
  `Q::NAME` (including nested modules) to `Q`. The capture caused wrongful
  rejection, never a false proof; no corpus file relied on it. Function half
  resolved in elisa-proof-mocap e723e71: a bare call inside an included module
  resolves to that module's own function, then to globals, never to the
  including module's same-named function; `Mod::f` resolves only within `Mod`.
  The scheduler now matches findings per owning module, so a same-named
  function elsewhere can no longer mask or taint a callee's summary. No corpus
  file relied on the wrong resolution; callers of unverified `Ops::apply`,
  `range_weight` and similar now report it honestly.
- G69: contract bounds written as `frame * 1000` fail; callers pass
  pre-scaled milli-frame times (`Retime::time_of`).
- G70: ensures that reconstruct a time through division
  (`result * UNIT / span == ...`) time out; `rescale`, `forward_between` and
  `invert_between` state bounds and exact endpoints only.
- G71: a conditional early `return move out if ...` is treated as an
  unconditional move, so every later use of `out` is reported as a
  disproved use-after-move. `RetimeApply::ranges_of` / `source_times`
  return a fresh empty array from an `if` block instead.
- G72 (fixed): `range_step` (eight ensures over `range_weight` and `step`)
  left one obligation open, and it took about 7 minutes to fail, on the Mac
  as well as on winpc (the earlier note that it proved on the Mac was
  wrong). Adding the early returns `return speed if blend == 0`, `return
  UNIT if time == start` and `return UNIT if time == stop` (the output is
  unchanged) made it prove in about 20 s, so its callers in `retime_laws`
  keep its summary.
- G73: a product of two variables divided by a third (`done * span /
  whole`) leaves the bounds of the local unknown even when clamped.
  `rescale` goes through `rescale_fraction` (constant multiplier, like
  `invert_between`) and `rescale_offset` (bounded parameter, like
  `forward_between`), with an exact `return time if reached == stop` so 1x
  stays byte-identical.
- G74 (fixed): the laws `apart_accepted` (`ensure result` of `disjoint`
  on `other + 1`), `clamped_speed_ok` (`speed_ok` of a `clamp_speed`
  result) and `advance_land_forward` (`land(advance(...))`) are restored
  with their original statements and prove. `disjoint` gained
  `ensure result or a_last >= b_first` and `ensure result or b_last >=
  a_first`, `speed_ok` gained `ensure result or speed < MIN_RATE or speed >
  MAX_RATE`, and `land` gained `ensure result == time or result == end`.
  Two prover changes were needed. First, a premise that has the goal as one
  of its alternatives is now split first, instead of the bounded split
  depth going to unrelated disjunctions such as `clamp_speed`'s. Second, a
  call rewritten by a callee summary (`advance(t, d)` to `t + d`) keeps its
  original form when only that form appears in the facts.
- `src/ops/retime_apply.elisa` includes `rig_stack.elisa` and so inherits its
  state ("unsupported", the same class as `ops_file`, `rig_cache` and
  `rig_stack` on main, whose counts are unchanged). The time-map decisions it
  makes go through the proved `Retime` kernel.
- G75: `RetimeApply::source_times` called `range_step` with requires it could
  not see. It now goes through `well_formed`, `step_at`, `range_delta`,
  `entered` and `rescale_tail`, which carry the guards themselves. The
  guards are no-ops for `ranges_of` output (ordered, non-empty, in-clip
  ranges), so the output is unchanged; the range_step requires close.
  Remaining: index and budget findings at `source_times` :167-171. Tried
  (gaps2): moving the stop handling into a loop-free helper indexed by a
  plain `usize` removes the index and budget findings, but the prover then
  drops path facts in the `while t < end` body: even an explicit
  `if t >= 0 and t <= MAX_TIME` immediately before `range_delta(t)` /
  `finish(t)` leaves those requires unproven, and the two `t` invariants
  stop being preserved (net +3). Reverted; this looks like a prover gap
  in while-loop fact tracking rather than missing app guards.
- G76: `Track::despike`/`smooth` called `Gate::apply` per frame with
  requires on the fade and the values. They now end in `faded`, which uses
  `fade_at` (no requires, ensures `[0, FULL]`, calls the `Fade` kernel in
  its domain and repeats its body otherwise) and `blend` (calls
  `Gate::apply` within `±LIMIT`, the identical formula otherwise). The
  `fixed.count` and frame-range guards never fire: the passes only assign
  existing slots. All Gate::apply findings in Track close.
- G77: `Ops::apply` in `stack.elisa` builds its per-frame weight through
  `frame_fade` (fully proven; `else: return FULL` on every branch, direct
  `return Fade::ramp`) and `gated`, and checks the bone index before
  `Gate::bone_selected`. `src/tools/track.elisa` now proves completely
  (958/958 obligations, 0 findings; 6 certificates in `fade_at`/`faded`/
  `median` do not replay, as before, so its state reads `unknown`); the
  workarounds are G80-G82 and docs/track-proofs-notes.md. `stack.elisa`
  goes from 65 to 34 unproven, all in `stack.elisa` itself. `candidate`
  still sees `borrow-call-opaque` at `Track::despike`, `Track::limit_wring`
  and `Track::median`: a G68-style capture, since `Ops` (and `Stability`)
  define functions with those names. An identical `limit_wring` body in a
  module of its own is not opaque to its caller. Closing it needs either
  distinct names on one side or the prover keying summaries by module.
- G78 (closed): `push_number` in `Report` and `OpsFile` walks the 19
  powers of ten from 10^18 down in a fixed `for` loop, skipping leading
  zeros (same bytes; the units digit is always written). No `place`
  invariant remains. Report goes from 31 to 8 unproven; what is left there
  is G79 (`push_cstr` / `save`) and its callers.
- G79 (prover gap): `contract-proposition-type` on `file != null`
  (`Report::save`, `OpsFile::read_bytes`) and on cstr `s[i] != 0`
  (`push_cstr`). Optional-pointer comparison is not a proposition the
  kernel accepts; it cannot be closed in app code without changing the
  null check. Left for the prover.
- G80 (prover gap): a closed comparison between constants of different
  sign is never decided. `return 3` does not establish `ensure result >=
  -5`, `Order::clamp(0, -H, H)` does not establish `result >= -H`, and a
  `-K` argument fails `requires lo <= hi`. `proof_closed_safe_constant_
  comparison` and `proof_closed_signed_i64_comparison`
  (`src/proof/linear/congruence_goals.elisa`) both bail out on
  `proof_has_ambiguous_integer_constant`, which accepts only 0..127
  (`fixed_width_arithmetic.elisa:5-35, 84-87`). Two negative constants
  compare fine through linear reasoning. App workaround: clamp through a
  helper that takes the bound positive (`Track::bound_to(v, k)`, ensures
  `result >= -k`), and never return a literal under a negative bound.
- G81 (prover gap): two `clamp`s in scope (`Order::clamp` and
  `Span::clamp`, both included by Track) make the prover drop
  `Order::clamp`'s ensures at the call; a uniquely named copy
  (`Track::bounded`) keeps them. Same family as G68.
- G82 (prover gap): within one body, the ensures of a call result are lost
  once a later call's facts mention a negative constant, and facts about a
  `let x = f(...)` binding are not tied to `f`'s ensures after a call that
  takes a `mutable` borrow. Track keeps one clamp per function
  (`carried_side` -> `side_eased` -> `side_held` -> `carry_over`), moves
  inner loops into their own functions (`lock_run`, `carry_gap`, which
  also clears the control-flow fact budget), and restates the callee's
  ensures as never-taken `break if` guards where a loop invariant needs
  them.

