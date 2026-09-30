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
