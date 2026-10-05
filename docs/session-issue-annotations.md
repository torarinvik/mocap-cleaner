# Session finding annotations

The session codec keeps its `mocap-studio session 4` header. Optional tag 8
stores an ignored finding as a complete detector result row:

```text
8 analysis_schema analysis_frames first_frame last_frame issue_type subject_id peak_frame severity peak_value threshold
```

Tag 6 scopes these records to the session's source fingerprint pair, selected
animation, source frame count and document-node count. Tag 8 also records
analysis schema (`2`), the output frame count after retiming, and every field
that defines the finding shown to the user. The process-local build revision
is intentionally omitted. Bump the analysis schema when finding semantics
change so older intent expires safely.

On restore, an annotation applies only to a newly computed finding whose full
result row matches. Records with invalid ranges, unsupported schemas or no
matching finding expire. A mismatched tag-6 identity rejects the session.
Older v4 sessions without tag 8 remain readable. The codec accepts at most 256
records; an over-capacity save fails before writing, and an over-capacity load
fails without replacing the caller's existing annotations.

The codec API is in `src/studio/state/session_state.elisa`:

- `encode_session_with_annotations` and `save_session_with_annotations`
- `decode_session_with_annotations` and `load_session_with_annotations`

Persisted record validation and stable result matching, including the output
frame count (which can differ from tag 6's source frame count), are in
`src/studio/state/session_issue_annotation_policy.elisa`. The running Studio
passes ignored current findings to the codec when saving. A loaded record is
held with the staged session and does not replace the current annotation store
until the user accepts that replacement. The accepted records are applied only
after the next analysis rebuild produces an exact result-row and frame-count match; all others
expire. Cancelling a replacement or failing validation leaves live intent
untouched. See `docs/studio-ux.md` for the remaining native UI review status.
