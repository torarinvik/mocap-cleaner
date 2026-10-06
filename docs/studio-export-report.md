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

## Captured report inputs

Report generation no longer reopens the renamed-away staging path. It receives
the output fingerprint captured by loading the validated staging file before
publication. The bounded residues cover the serialized GLB bytes, not the
edited in-memory document's retained source bytes. They are non-cryptographic. Stack settings and animation
name are captured before publication rather than read again afterward.

A result-generation gate rejects changed results after modal confirmation and
before publication. Its scalar contract proves; one focused law remains
unresolved with the current prover. Full frozen report-byte recovery, exact
source-byte hashes and native failure-path qualification remain open.

The source basename is bounded independently of the destination path and
stored in a report-local buffer. Export names of different lengths therefore
cannot change source indexing, and long basenames are not truncated to a
128-byte UI text slot. Both paths are refused when they exceed the existing
4096-byte adapter boundary. Native Unicode/path-boundary qualification remains
required.

The Studio settings include `spike_threshold_fixed_channel_units` from the
exported clip and `spike_measure` describing the absolute channel second
difference and 1,000,000 scale. These are not physical acceleration units.
The unavailable marker now concerns complete detector configuration; it does
not negate individually captured thresholds in settings. Other callers may
provide fewer settings, so consumers must inspect the actual entries.

## Report text storage

Operation/band values use report-only 512-byte slots rather than the UI's
128-byte display slots. At the current 16-operation and 8-band capacities,
export uses at most 50 simultaneous formatted views in 96 slots. Source
basenames use their own local buffer. Integer formatting supports the full
signed i64 range without negating its minimum value. Report formatting is
synchronous; a future worker implementation must give each job owned storage.

The slot offset/advance policy proves 10/10. Its caller laws prove 21/22 with
one unresolved upper-bound implication; no claim of complete proof coverage
is made. Studio object compilation passes. Native report-content qualification
remains required.

## Review freshness

The export review captures the displayed result generation. If that generation
changes before confirmation, Studio resets acknowledgement and requires a new
confirmation of the updated notes. Publication additionally requires the
current stack to match the evaluated stack that produced the displayed clip;
selection-only differences are ignored by the existing stack comparison.
Failed evaluation or unavailable evaluated-stack provenance blocks export.
Reports use that evaluated stack, preventing newer failed edits from being
reported as settings for an older GLB.

Compilation of this refinement is pending because Stage1 rejected the current
external compiler source-tree mismatch. Existing generation-policy proof
results remain as documented above; native stale-review qualification is open.

Unknown export-validation codes now report unavailable status rather than
claiming successful validation. Validation results use an actual `Result`
const module; focused policy/law results remain 4/4 and 8/8. Compilation of
this refinement is pending Stage1 provenance renewal.
