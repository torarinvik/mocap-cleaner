# Report reader follow-up check

The authorized command is:

```sh
ELISA_PROOF=../elisa-proof-mocap/build/elisa-proof-enum-committed \
CHECK_JOBS=2 PROOF_JOBS=2 sh scripts/check.sh
```

Output: `build/report-reader-current-check.log`, session 70887.

Observed results:

- File-length gate passed for 497 maintained text files.
- Checked native Trash adapter passed.
- 39 existing test executables rebuilt; 39 reused cached builds.
- All 78 existing tests executed with exit code zero.
- CLI cleanup/report, folder batch, hands plus report diff, and retime passed.
- Proof gate remains running; the complete check is not qualified as passing.

Compiler product was `4c409da6`; the explicitly selected prover product was
clean `3de825c7`. Engine and UI revisions were `01f5aec7` and `8ab2eb39`.
These results cover the existing fixtures. No executable tests were added.
New Unicode edge cases, rendered HTML accessibility, fractional numbers,
indexed comparison, and decoder proof completion remain unqualified.

Shared source changed during this run, including surrogate arithmetic and
agent-owned app integration. Treat this as diagnostic evidence, not acceptance
of one immutable complete source snapshot. Compiler scope repair `3e716ca8`
postdates the executable compiler used here and requires a fresh rebuild and
qualification. Another host seed is currently holding the global seed lock;
do not accept its manifest as evidence of this repair without checking which
source snapshot it compiled.

## Terminal proof gate

Session 70887 is terminal with exit code 1. All 78 existing executable tests
and the four CLI workflows returned zero earlier in this run, but the proof
gate failed with regressions and missing reviewed baselines. This run selected
prover `3de825c7` and began with compiler `4c409da6`; source edits and compiler
rebuilds occurred during the run. It is diagnostic evidence and cannot qualify
the current snapshot. Keep the proof contracts and baseline review requirements;
do not convert these failures into acceptance by weakening the baseline.
Full output: `build/report-reader-current-check.log`.
