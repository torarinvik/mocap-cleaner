# Track proofs (G77): how the last 29 obligations close

`src/tools/track.elisa` now proves completely: 958 of 958 obligations, 0
findings (from 837/866 with 29 unproven at d2cf900). Six certificates do
not replay in the kernel (`fade_at` :88, `faded` :116, `median` :300; this
was 7 at d2cf900), so the state reads `unknown`, not `proved`. The prover
gaps behind the workarounds are G80-G82 in docs/proof-gaps.md.

## How this was checked

- Prover: `elisa-proof-mocap` @ `mocap-cleaner-proofs` (7571dfa), built on
  Linux with compiler d8b5d30 / stage0 0b21b7b. That build reproduces
  d2cf900's numbers exactly (837 proven, 29 unproven), so the counts are
  comparable with the macOS build.
- Tests: `track_kernels`, `track_tools`, `foot_lock` and `wide_median`
  build and pass.
- Behavior: a differential harness ran despike, smooth, median,
  close_seam, limit_wring, lock, carried, carried_blends (twice),
  hold_offsets, spike_count, contacts and pin on 1500 pseudo-random
  tracks. Tracks were 0-47 frames, with values up to +-2e12 and
  out-of-range passes, edges, blends and steps. The output checksums are
  identical to d2cf900. On in-domain inputs they are also identical to the
  pre-WIP 5975724, which aborts on out-of-domain inputs.
- Performance: lock, carried_blends, limit_wring, hold_offsets and
  close_seam on 2M-frame tracks at -O2 run at the same speed as d2cf900
  (0.88-0.98 s for both over 5 rounds; the differences are noise).

## Changes by function

| Function | Obligations closed | Why it holds / why behavior is unchanged |
|---|---|---|
| `bounded` (new) | the `Order::clamp` ones in `carried_side` | A copy of `Order::clamp` (same body and contract) under a unique name. With `Span::clamp` also in scope, the prover drops `Order::clamp`'s ensures (G81). |
| `bound_to`, `lock_value`, `foot_value`, `wring_value` (new) | the requires on `-LOCK_LIMIT`/`-FOOT_LIMIT`/`-WRING_HALF` clamps | `bound_to(v, k)` is `clamp(v, -k, k)` with `k` passed positive, because a `-K` argument is a mixed-sign constant the prover will not compare (G80). The three wrappers fix `k`, so loop bodies do not re-prove `k >= 0`. The values are the same as the clamps they replace. |
| `close_seam` | `pulled` requires (frame / window range), `blend` weight | The loop body re-tests `0 <= f <= last` and `1 <= window <= last`. That is always true: `f < count = last + 1` and the early return checked the window. |
| `wring_total` (new), `wring_guard` | both ensures, including on `return 0` | A literal `0` cannot meet `>= -WRING_HALF` (G80). The empty case returns `wring_value(n)` with `n == 0`, which is 0. The sum moved to `wring_total` and is the same sum in the same order. |
| `wring_one` | `Stability::limit_wring` requires | `about`'s requires were dropped (facts are lost in `limit_wring`'s loop). A never-taken guard in limit_wring's own terms (`-STABLE_LIMIT / 2`) covers value and about: both are within WRING_HALF = STABLE_LIMIT / 2 (wring_value, and the wring_guard ensures). |
| `limit_wring` | the summary of its callees | No edit. |
| `next_plant` | `ensure result <= count` | `invariant next <= count`: it starts at `f + 1 <= count`, and each step runs only while `next < count`. |
| `lock`, `lock_run` and `lock_frame` (new) | `Lock::locked` requires; control-flow budget; the `start >= 0` invariant | The inner loop moved to `lock_run` and the frame to `lock_frame`. Each frame is still the same `Lock::locked(clamp(v), anchor, f - start, finish - f, blend)`. `break if finish < start or finish >= count` is never taken (run_end's ensures); the prover does not tie `finish` to them. The per-frame `if` is always true: `start <= f <= finish < count <= MAX_FRAMES`, and anchor is a lock_value. |
| `carried_side`, `side_eased`, `side_held` and `carry_over` (new) | `Footing::span` / `Footing::carry` requires | The same three clamps and the same two kernel calls, one clamp per function. The prover keeps one call's ensures per body, and loses them once a later fact has a negative constant (G82). |
| `carried_at` | callee summaries | No edit. |
| `carried_blends`, `carry_gap` (new) | the `f >= 0` invariant; control-flow budget | The inner loop moved to `carry_gap` unchanged. `break if next <= f` is never taken (next_plant ensures `next > f`); the call before it drops that fact. |
| `carried` | callee summary | No edit. |
| `hold_offsets` | clamp requires | `lock_value` replaces `Order::clamp(raw, -LOCK_LIMIT, LOCK_LIMIT)`, with the same value. |

## Still open (outside track.elisa)

- `stack.elisa` `candidate`: `borrow-call-opaque` at `Track::despike`,
  `limit_wring` and `median`. `Ops` (and `Stability`) define functions
  with the same names, so the prover captures their summaries (G68
  family). The same body in a module of its own is not opaque. To close
  it, rename one side or have the prover key summaries by module.
- The 6 kernel replay gaps in `fade_at` / `faded` / `median`. Adding path
  guards did not change them; they look like a kernel-replay limit on
  call results with conditional arguments.
- `rig_stack.elisa` reports an `import-error` in this checkout (an
  include outside the repo), unrelated to Track.
