# Studio export report format

`StudioExportReport` formats a version 1 JSON report and a readable text
summary from a snapshot of the values Studio has already computed. JSON keys
and their order are stable. Settings, assumptions, and warnings retain their
input order, so callers must provide them in a deterministic order.

The report contains a source label, selected animation name and index, input
and output frame counts, integer frame-rate estimates, floored duration in
milliseconds, cleanup settings, scope assumptions, quality metrics, and
categorized warnings with severity. Distance fields ending in `_um` are
micrometres. Spike fields count detected frames, changed channels count GLB
animation channels, and the balance field counts frames marked impossible by
the Studio detector. These are detector outputs, not certification thresholds.

Source and output identity values use `studio-residue-v1`, the existing pair
of bounded integer residues used to identify session inputs. They are labeled
as non-cryptographic fingerprints. They are not SHA hashes and do not prove
authenticity. The caller should pass a basename as `source_name` so a report
does not disclose a user's absolute local path. The output identity should be
computed from the validated output document by the caller.

Timing uses integer frames per second and computes `floor(frames * 1000 / fps)`.
It is an estimate in whole milliseconds; it does not encode irregular GLB key
times or per-frame retiming provenance. The maximum frame count matches the
Studio timeline limit of 10,000,000. Empty names, invalid residues, invalid
rates, negative metrics, and uncategorized warnings make the report empty
rather than emitting misleading partial JSON.

Formatting is pure. The caller chooses and atomically publishes the report
files alongside its export workflow. Tool/dependency versions, SHA-256 source
and output hashes, policy thresholds, and full retime provenance still need
to be added by the Studio integration when those values can be recorded
truthfully.
