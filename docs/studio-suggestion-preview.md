# Suggestion preview policy

`StudioSuggestionPolicy` is the pure admission kernel for a cleanup suggestion
review. The app owns the candidate and captures both the displayed document
revision and the cleanup-stack revision when opening a preview. Apply is valid
only while both revisions still match.

Contact locks require validated contact evidence and an explicit user choice.
Candidate admission requires measured, passing results for contacts,
knee/elbow transitions, boundaries, peak velocity and impact timing. A metric
that cannot be measured is unknown and blocks the passing decision. A rejected
or cancelled preview must not create a history entry; the app owns that
transaction and must apply an accepted candidate as one grouped edit.

The Studio integration builds the boxing preset as a candidate while preserving
the current operation order, corrections, contact edits and retime bands. The
review panel switches the hosted viewports between the current and suggested
clip while timeline scrubbing and playback remain available. Optional contact
locks can only be enabled after both role tracks validate and the user opts in.

The required preservation evidence is still unavailable in the current clip
model. It stores four tracked points (hands and feet), not knee or elbow
transitions, and has no boundary comparison or semantic impact timing measure.
Those gates therefore classify as `Unknown`; Apply remains disabled. The
boxing preset is presented as a candidate recipe only. The kernel does not
make it a general recommendation or complete the M3.1 roadmap criteria.
