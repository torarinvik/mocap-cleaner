# Finding explanations

The finding browser currently receives aggregate motion-spike intervals.
Selecting a row navigates to its exact peak frame. An aggregate finding does
not identify a joint, so selection preserves the existing joint selection.

Rows use `StudioIssueExplanation::explain` to retain the exact peak frame,
value and threshold. Native accessibility help describes the detector and its
limitations. The visible selection status reminds users to review intent.
Invalid finding records receive an explicit rebuild message.

The spike measure is the absolute second difference of rounded channel
components scaled by 1,000,000. Translation, quaternion and scale components
can contribute; these aggregate values are not physical acceleration or a
single common physical unit. Cubic-spline and morph-weight channels are
excluded by the current collector. The peak and threshold are detector
readings, not calibrated confidence or a recommendation to change the take.
Deliberate fast motion may trigger a finding.

The explanation policy and laws already exist. This change connects them to
row presentation; it adds no detector or automatic repair. Running-window
readability, VoiceOver announcement and intentional-motion qualification
remain open in M0/M2. Distinct slide, penetration, jitter, pole, seam and
balance producers remain future work.
