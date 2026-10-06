# Studio export report format

`StudioExportReport` formats a version 2 JSON report and a readable text
summary from a snapshot of the values Studio has already computed. JSON keys
and their order are stable. Settings, assumptions, and warnings retain their
input order, so callers must provide them in a deterministic order.

The report contains a source label, selected animation name and index, input
and output frame counts, integer frame-rate estimates, floored duration in
milliseconds, active cleanup settings, ordered operation parameters, retime
bands, scope assumptions, quality metrics, and categorized warnings with
severity. Distance fields ending in `_um` are
micrometres. Spike fields count detected frames, changed channels count GLB
animation channels, and the balance field counts frames marked impossible by
the Studio detector. These are detector outputs, not certification thresholds.

The JSON `unavailable` array names provenance fields that this export snapshot
does not provide and gives a reason for each omission: application/tool
versions, dependency versions, detector thresholds, detailed rig configuration,
and the per-frame retime map. The text summary has a matching
unavailable-provenance section. Consumers should treat these fields as
unavailable, not infer defaults from their absence. The schema version was
bumped to 2 when these explicit markers were added.

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
truthfully. SHA-256 values are not emitted as unavailable entries because no
SHA-256 calculation is implemented by this formatter; the existing residues
remain explicitly labeled non-cryptographic.

Studio writes `<export>.report.json` and `<export>.report.txt` as atomic
same-directory sidecars after the validated GLB rename succeeds. The source
label is the loaded take's basename. The report includes the available
detector metrics, foot/hand cleanup toggles, cleanup blend, each active stack
operation's kind, enabled state, frame span, bone mask, strength, and edge
blend, plus active retime bands and whether retiming was applied. It does not
serialize rig configuration or the per-frame source-time map. Output identity
is calculated from the validated temporary GLB before it is renamed. A
sidecar failure does not roll back the GLB; Studio reports that the GLB
succeeded while report sidecars failed, with the destination path available
for retry.

## Partial publication feedback

The result dialog and its native accessibility announcement distinguish a
validated GLB from incomplete report publication. If either report write
fails, one sidecar may already exist and the other may be missing or stale.
The dialog therefore does not recommend retrying the whole export, which
would require replacing the published GLB. A report-only completion workflow
from an immutable export snapshot remains planned in M6.

Status also distinguishes report failure from Storage tracking failure,
including simultaneous failure. Tracking failure cannot imply that reports
were saved. These are presentation corrections; publication ordering and
retry behavior are unchanged. Running-window failure-path qualification is
still required.
