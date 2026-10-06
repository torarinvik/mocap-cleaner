# Current cache diagnostic check

The authorized `scripts/check.sh` run uses normal compiler `3c72f59f` and the
clean isolated prover `4da37c97` built with compiler/frontend `45330579`.
`CHECK_JOBS=2` and `PROOF_JOBS=2` bound concurrency. The starting repository
revision is recorded in `build/current-cache-check-revision.txt`; output is
`build/current-cache-check.log`. Recovery UI/retry source edits continued during
the run, so it is diagnostic evidence rather than immutable snapshot acceptance.

The checked Trash adapter passed. All 78 executable test rows completed: 77
passed and `studio_export_report` returned 19. Its generated JSON contains the
current explicit partial-provenance reason, while the fixture expected the older
absence wording. Commit `bbbb6ef` updates that existing expectation; it has not
been rerun yet. Cache/performance fixtures passed in this run. All four CLI
workflows (clean/report, batch, hands/diff and retime) returned zero.

The proof phase is still running. No final gate result or proof closure is
claimed. A later compiler repair (`720896f4`) is being rebuilt separately; this
run does not qualify that compiler or the evolving recovery UI.
