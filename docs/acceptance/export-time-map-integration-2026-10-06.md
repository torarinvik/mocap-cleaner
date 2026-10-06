# Export source-time map integration

Studio freezes the evaluated clip's exact integer `times` array into both
report sidecars before GLB publication. JSON records a `source_time_map`
object with explicit milli-source-frame units and output-frame indices;
text includes the same values as CSV. No nearest-frame rounding is applied.

The map serializer requires matching frame counts, valid source-time bounds,
zero first time, exact final source frame, and strictly increasing entries.
A one-frame clip has the single entry zero. These requirements match
`RetimeApply::source_times`, which supplies `StudioModel::Clip.times`.

The additive report APIs preserve existing callers and reject empty map
serialization or a complete report larger than 1 MiB. Studio's existing
snapshot check rejects empty sidecars before publishing the GLB. Raw map
assembly helpers are private; callers cannot inject arbitrary JSON bytes.
The unavailable retime-map marker is omitted only in the map-bearing APIs.

## Evidence and remaining work

Normal compiler provenance identifies `04b384ec`. The formatter emitted
`build/export-report-time-map.o`; its log has no diagnostic beyond the
successful provenance check. Both modified source files remain under 600 lines.
This is compilation evidence, not JSON parsing, native publication, or
semantic GLB round-trip qualification. The focused source proof run finished with exit 1 and unsupported state:
87 of 274 obligations proved/replayed, 187 unproven, 189 findings, and
zero semantic errors, recorded in `build/export-report-time-map-proof.json`.
This expanded count includes imported serializer obligations; it is not a
closed proof or a reviewed baseline improvement. No executable tests were added.

Full Studio compilation and proof baseline review remain open. Durable
recovery integration and its fault qualification are separate requirements.
