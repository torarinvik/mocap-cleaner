# Contact endpoint drag preview

Dragging a detected contact endpoint shows a purple proposed inclusive range
and a 1-based frame-range status. The overlay previews the interval; it does
not evaluate a new cleaned pose while the pointer moves. The existing result
stays visible until release commits and rebuilds it.

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
preserve the original interval. Current policy and law results are 49/49 and
65/65 proved, with the agent's direct certificate replay reporting no gaps.
Root reproduced both complete proof summaries after integration.

Studio compilation passed. Running-window pointer geometry, minimum-window
readability, focus-loss cancellation, one-entry undo and native announcement
qualification remain open in M0/M4. The overlay does not establish interactive
pose-preview quality or eliminate the contact-edit capacity limit.

The later release-feedback refinement passed diff checks, but its Studio
compilation attempt was refused by Stage1 provenance after an external
compiler source edit. The earlier successful build qualifies the original
preview slice; compilation of the feedback refinement remains pending.
