# Unavailable report field counts

Reports without an exact time map emit six unavailable provenance entries;
map-bearing reports emit five. The prior scalar count of five for every report
was inconsistent with the formatter. The schema policy now records both counts
and its laws explicitly cover present and absent time maps.

Normal compiler `04b384ec` compiled the law composition without diagnostics.
Both default prover `5776350b` and clean candidate `3ac99624` proved/replayed
the policy 22/22, with zero gaps, findings or semantic errors. The source
baseline advances from 17 to 22 obligations.

The full law composition proves/replays 47/50. Its three open obligations are
the existing minute, fractional-millisecond and maximum-frame duration laws,
all refused by the wrap-guard goal gate. Their baseline remains unchanged;
this run does not qualify the full proof gate. Reports are the
`build/export-report-unavailable-count-*.json` artifacts. No executable tests
were added or run; formatter parsing/runtime qualification remains open.
