# Track proofs (G77) — notes for the remaining 29 obligations

Follows d2cf900 (163 -> 29). **Not compiled or proved here**: no prover in
the session. Every change below is meant to be behavior-identical; where a
guard is added, the reason it never fires is stated. Please run the prover
and the corpus before merging.

## New helpers (src/tools/track.elisa)

- `foot_value`, `lock_value`, `wring_value`: local clamps replacing
  `Order::clamp(x, -FOOT_LIMIT, FOOT_LIMIT)` etc. Their ensures are written in
  the callee's own terms (`0 - Footing::LIMIT`, `Lock::LIMIT`,
  `(0 - Stability::LIMIT) / 2`), which is what `Footing::span/carry`,
  `Lock::locked` and `Stability::limit_wring` require; an `Order::clamp` to
  the Track-local constants did not discharge those requires. Same values:
  the constants are equal (FOOT_LIMIT = Footing::LIMIT, LOCK_LIMIT =
  Lock::LIMIT, WRING_HALF = Stability::LIMIT / 2 and -LIMIT/2 = (0-LIMIT)/2
  under truncating division).
- `reach_of`, `edge_of`: `Order::clamp(d, 1, Fade::MAX_FRAMES)` and
  `Order::clamp(b, 1, Fade::MAX_EDGE)` with explicit ensures, for
  `Footing::carry`'s distance and `Footing::span`'s blend.

## Changed functions

| Function | Obligation | Why it holds |
|---|---|---|
| `close_seam` | `pulled` requires (`frame >= 0`, `frame <= last`, `1 <= window <= last`) inside the loop | Loop body re-tests them; always true since `f < count = last + 1` and the early return already checked `window`. Out already holds the source, so the (dead) else is a no-op anyway. |
| `wring_guard` | overflow of `total` in the sum | Indexed `while` with invariants `|total| <= k * WRING_HALF`, `k <= n <= 1e10`, so `|total| <= 5e18`. **Only behavior caveat:** arrays over 1e10 elements (80 GB) now return 0 instead of an (overflowing) sum; no clip comes near that. Element order and clamps are unchanged. |
| `wring_one` | `Stability::limit_wring` requires on `value` and `guard` | Both pass through `wring_value`; `about` is already in that range (requires / `wring_guard` ensures), so `wring_value(about) == about`. |
| `limit_wring` | caller of `wring_guard`/`wring_one` | No edit; closes with the two above. |
| `next_plant` | `ensure result <= count` | Added `invariant next <= count` (initially `f + 1 <= count` from `f < count`; preserved since the step happens only when `next < count`). |
| `lock` | `Lock::locked` requires on value, anchor, into, left, blend | `lock_value` gives value/anchor bounds (same values as before). `into`/`left`/`blend` re-tested in the body; always true: `start <= f <= finish < count <= Fade::MAX_FRAMES` (run_end ensures, early return) and blend checked at entry. |
| `carried_side` | `Footing::span`/`carry` requires; new ensure `|result| <= Footing::LIMIT` | Inputs through `foot_value`/`reach_of`/`edge_of`; `span` ensures `blend <= width <= MAX_EDGE`, valid for `carry`. The result is wrapped in `foot_value`: `carry` is `offset`, `0`, or `Gate::apply(0, held, w)` with `w` in `[0, FULL]`, all between 0 and `held`, so the wrap never changes it. |
| `carried_at` | overflow of `first + second` | Each side now ensures `|x| <= 1e9`. No edit. |
| `carried_blends` | planted clamp; `next_plant` ensures | `foot_value` instead of `Order::clamp` (same value); `f <- next` keeps `f >= 0` from `next > f`. |
| `hold_offsets` | overflow of `anchor - v` | `anchor` is only ever 0 or a `lock_value` result, so `lock_value(anchor) == anchor`; with both operands in `±1e9` the difference fits. |

## If something stays open

- Loop-body guards in `close_seam`/`lock` assume the prover keeps facts from
  an `if` inside a captured `for` body (G75 saw facts dropped in `while`
  bodies). If they still fail, move the body into a loop-free helper taking
  the values as parameters with those facts as requires.
- `wring_guard` invariants use `k * WRING_HALF`; if nonlinear terms are not
  handled, unroll as `total <= k * 500000000` or bound per-step.
