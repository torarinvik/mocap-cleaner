# Contact endpoint drag preview

Dragging a detected contact endpoint shows a purple proposed inclusive range
and a 1-based frame-range status. A transient contextual pose candidate is
requested while playback is paused. The existing result stays visible while
that candidate is pending, unavailable or stale; release commits through the
normal edit path. Runtime responsiveness and native acceptance remain open.

Release adds one contact edit through the existing stack/history path. A
clamped range identical to the original is a no-op with an explicit status.
A refused release reports invalid interval or exhausted edit capacity instead
of retaining the transient release instruction. Escape or loss of focus
clears the transient preview. Other stack commits and undo/redo also clear
it, preventing a later pointer release from applying an obsolete interval.
Keyboard commands are ignored during the active pointer press except Escape.

The preview policy accepts the 10,000,000-frame editing domain, clamps the
first endpoint between zero and the last endpoint, and clamps the last
endpoint between the first endpoint and the final frame. Invalid grab parts
preserve the original interval. The original policy and laws were proved
49/49 and 65/65, with direct certificate replay reporting no gaps.

## Contextual pose candidate

Dragging an endpoint now requests a transient pose candidate built from a copy
of the current stack using the same `FootState::release` operation that release
uses. `StudioModel::build_with` evaluates that candidate over the full clip;
the candidate is displayed in the hosted pose views only. The committed result,
timeline metrics, stack, history and export input remain the current result.
The proposed range and status identify whether a fresh candidate is visible.

Candidate display requires an exact match on proposed endpoints, take serial,
document build generation, stack generation and playhead frame. A changed take,
history or document cancels the drag; a changed playhead drops the candidate and
requests a fresh one. Candidate build failure leaves the current result visible,
and release still follows the normal interval and capacity checks. Cancel or
release discards the candidate without adding history.

The `StudioContactPreviewPolicy` and its laws compile to a fresh object with
current compiler `23a0e16a` at `build/contact-current-policy.umIKtZ/laws.o`;
the laws include cadence, generation wrap, stale identity and maximal-clock
checks. This is compile evidence, with proof replay still pending.
A 250 ms minimum interval bounds candidate evaluation
start frequency. Candidate construction still runs synchronously through the
full clip evaluator, so this does not bound evaluation duration or guarantee a
responsive drag on long takes. M5 background evaluation and runtime profiling
remain required. Playback suspends pose evaluation, including requests from
pointer movement. Candidate metrics and curve views also continue to describe
the committed result while the three pose views show a fresh candidate.

Integrated Studio compilation, certificate replay for the new policy, and
native pointer/cancel/undo/long-take acceptance remain open. The current full
Studio trace reaches an independent backend diagnostic in event handling, so
the source-level integration is not yet qualified by that trace.
