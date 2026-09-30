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
