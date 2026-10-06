# Workspace-bound artifact destination protection

`StudioStorageArtifactDestination::allowed` now receives the selected canonical
build root. Both destination identity snapshots and reserved-control identity
snapshots use it rather than the process-relative literal `build`. Studio passes
`workspace_build_directory()` through its artifact guard. This makes reserved
metadata identity checks follow workspace selection and retains fail-closed
handling of unresolved or ambiguous facts. The private finite native fact
values are now a const enum with distinct safe/path/identity/unknown cases.

Normal f292cbe0 emitted `build/workspace-artifact-destination.o` without
diagnostics (`build/workspace-artifact-destination-build.log`). The existing
admission-policy laws prove and independently replay 6/6, zero findings,
diagnostics or replay gaps, with clean candidate 3ac99624
(`build/workspace-artifact-destination-laws.log`). These Boolean proofs do not
qualify native filesystem resolution, root identity or races.

Full Studio build session 31992 overlapped session-policy refactoring and failed
on undefined `record_valid`/`records_complete` declarations. Its log is
`build/workspace-artifact-destination-studio-build.log`; that build does not
qualify combined integration. Root is waiting for the session owner's completed
composition before retrying. No executable tests were added or run. Native
workspace-switch export, hard-link aliases and protected metadata behavior
remain qualification requirements.
