# Suggested cleanup preservation review

The suggestion dialog compares the current result with its candidate before allowing Apply. Missing role tracks or incomplete samples produce `Unknown`; they do not count as passing evidence.

## Measured gates

- Contact timing compares every detected hand and foot contact frame. Any changed frame fails this exact mask comparison.
- Knee and elbow pose compares the internal hinge angle at each frame. Angles use thousandths of a degree and allow at most 15 degrees of change per hinge sample.
- Boundary pose compares the four tracked hand and foot positions at the first and last frame. The limit is 10 mm per endpoint.
- End-effector velocity compares the three-dimensional hand and foot velocity vectors over each frame interval. The limit is 50 mm/s per sample.

The candidate is built from the same source and operation stack revision captured by the dialog. Its retime mapping is compared against the current result for each marked impact frame.

## Impact review

Studio's GLB loader currently receives no source-tagged impact annotations. In the dialog, the user can mark the playhead as an impact, explicitly confirm that the take has no impact events, or clear the review. A mark records the source frame, the current source frame count is checked, and the annotation stores the take's two-part `StudioSourceFingerprint` identity. Candidate timing passes only when each annotation maps to the same output frame in both clips. Explicitly reviewed zero-event lists are `Inapplicable`; missing or unreviewed annotations remain `Unknown`.

Impact reviews are persisted in sessions as versioned tag 9 records. Each record carries the review schema, source fingerprint pair, selected animation, source frame count, rig node count, total event count and source frame. Explicit “no events” uses one sentinel row. The session loader rejects mixed states, mismatched identities, invalid frames, duplicate frames and incomplete records. A session without tag 9 restores impact review as `Unknown`.

The two-part fingerprint is a bounded identity check, not a cryptographic digest; a matching pair does not prove byte-for-byte source identity. Contact onsets and acceleration peaks remain separate measurements and are not treated as semantic impacts.

## Verification

The measurement and session impact binding kernels carry inline contracts and focused proof files. The Studio compile is the current integration check; native-screen acceptance and executable checks remain separate qualification work.
