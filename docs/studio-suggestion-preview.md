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

This policy does not select or evaluate a recipe, produce metric evidence, or
prove that existing cleanup operations preserve motion. In particular, the
existing boxing preset is only a candidate recipe. The kernel does not make it
a general recommendation or complete the M3.1 roadmap criteria.
