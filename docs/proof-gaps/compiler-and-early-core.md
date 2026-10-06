# Compiler and early core gaps (G1–G20)

[Proof gap index](../proof-gaps.md)

## Mutable global enum initializer ownership

Compiler `04b384ec` declines `UiMetrics.stage_state` after recovery adds
another enum named `Stage`. Root reproduced this with two modules containing
same-named enums and different variants in `build/repro/global-enum-owner.elisa`.
The compiler returns zero despite the diagnostic and emits no object.

Global materialization looked up each declaration's table row by owner but
did not set that owner while folding its initializer. Compiler commit
`45330579` wraps materialization in the declaration's module context and
restores the previous context after the inner operation, including early
returns. The normal seed completed successfully; its provenance check matches
`45330579` (log `build/global-owner-compiler-seed.log`). The reduced reproduction
emits a fresh object without diagnostics in `build/enum-owner.WIsTrM`, and the
recovery publication adapter compiles in `build/recovery-publication.jBPo5b`.
Full Studio compilation remains pending. No executable tests were added or run
for this repair.

## Same-named ADT constructor metadata ownership

Compiler `45330579` compiles recovery completion and publication separately,
but the integrated Studio reports that completion's two-field `Published`
constructor requires publication's three fields. The reduced
`build/repro/constructor-enum-owner.elisa` declares two `Outcome` enums in
different modules with two and three fields. It fails with a wrong arity and
payload type diagnostic in `build/constructor-owner.LMtqKC`.

Semantic variant lookup selected the first bare owner/variant row, and payload
metadata had no declaration module. Compiler commit `3c72f59f` narrows bare
variant lookup through the existing lexical/unambiguous enum-module resolver
and retains payload modules for constructor type, label and count checks.
Parser-only synthetic metadata retains its separate unowned fallback. The
normal seed completed (`build/constructor-owner-compiler-seed.log`), and its
provenance check matches `3c72f59f`. The reduced reproduction emits a fresh
object without diagnostics in `build/constructor-owner.IzGtYg`. Integrated
Studio compilation remains pending.
No executable tests were added or run for this repair.

Integrated compilation then exposed a separate lookup in match patterns:
`enum_tail_variant_index` still selected the first same-named variant across
modules. The extended `build/repro/pattern-enum-owner.elisa` reproduces the
wrong two/three-field arity with `3c72f59f` in `build/pattern-owner.LaUJrv`.
Compiler `720896f4` applies the same lexical module filter to this lookup.
Its normal seed is running (`build/pattern-owner-compiler-seed.log`); source
adoption is not yet reproduction or integrated qualification.

## Current global container lowering gap

Compiler `04b384ec` declines direct mutation of a mutable global darray,
including byte-array `extend` and record-array `push`. The same record push
through a borrowed `mutable darray[Recovery]&` compiles. This is a receiver
binding gap, not evidence that recovery records need a different domain model.

Root reproduced the decline with `build/repro/recovery-retained-struct.elisa`
and a named-local variant; both return process zero but emit no object.
`build/repro/recovery-record-local-array.elisa` compiles to a fresh object.
Logs are under `build/retention-{compile,local,borrow}.*`. The recovery owner
also reduced the byte-array case in `build/repro_global_byte_extend.elisa`.
These are compile-only reproductions; no new executable test was run.

`darray_type_behind` in `codegen_type_sizes.elisa` consults only local type
bindings, and `darray_address_of` in `codegen_abi_facts.elisa` consults only
local slots. Ordinary global reads use the mutable-global table instead.
A repair must also choose an arena whose lifetime supports the global backing
storage: adding address lookup while growing in a function's temporary arena
would admit a use-after-free. Preserve local shadowing and module ownership.
The copying-to-local workaround must pass region-escape checks and have its
arena lifetime inspected before qualification. Native recovery acceptance and
the full Studio compile remain open.

Root inspected emitted LLVM for the local byte-array mutation plus global
assignment form at `build/retention-ir.Q8UHGB/repro.ll`. With compiler
`04b384ec`, the function grows in its auto region, stores the global header,
calls the generated global `rehome` helper, then frees the auto region.
The helper calls `arena_adopt`, clones the complete payload, and flips between
two global region generations. This confirms generated lifetime handling is
present; it does not qualify runtime arena semantics or repeated updates.
Logical retained byte counts do not bound physical RAM: old and new global
generations, growth storage, clones and export preparation coexist. Recovery
retention must account for these copies and avoid repeatedly rehoming the
entire payload for individual fields. Memory and native acceptance remain open.

# elisa-proof gaps found by the mocap cleaner

Historically, fixes were developed in the `../elisa-proof-mocap` worktree on
branch `mocap-cleaner-proofs`. That work was merged into the sibling
`../elisa-proof` history at `6a816257`.

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
