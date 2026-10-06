# Exact Studio export time map

`StudioExportTimeMapReport` serializes an already computed mapping from each
zero-based output frame to its exact source time. Its input is the integer
milli-source-frame array produced by `RetimeApply::source_times`; one source
frame is exactly 1000 units. The formatter does not call the nearest-frame
helpers, round values to whole frames, or recalculate retime behavior.

The JSON output is a compact object with a declared time unit and a `frames`
array of `[output_frame, source_time_milli_frames]` pairs. The text output uses
the same pair order in CSV rows. Both preserve every supplied integer and are
deterministic for identical inputs.

Before formatting, the adapter requires a source count in `1..10,000,000`, an
output count in `1..100,000,000`, and an array whose count exactly equals the
output count. It checks that the map starts at zero, ends at the final source
frame, contains only in-range values and is strictly increasing. A mismatch or
invalid map returns an empty byte array. Each report is independently limited
to the existing 1 MiB report budget. Every byte append is admitted against the
remaining budget before it is stored. Output remains private until the
complete report is returned, so budget failure cannot expose a partial result.

The callable entry points are:

- `StudioExportTimeMapReport::valid_map(times, source_frames, output_frames)`
- `StudioExportTimeMapReport::json(times, source_frames, output_frames)`
- `StudioExportTimeMapReport::text(times, source_frames, output_frames)`

The serializer and scalar policy are pure Elisa modules. The policy contracts
prove count, source-time domain and byte-admission predicates; the law file
covers the source-time ceiling, per-entry ordering and global time bound. The
report serializer is an adapter over a dynamic array; current proof tooling
does not discharge its indexed-loop validation and serialization obligations.
Those adapter obligations remain open and are covered by the existing report
integration's validation and atomic output bounds, plus focused adapter checks.
The report integration exposes additive exact-map JSON and summary entry
points; existing report callers keep their unavailable-map behavior.
