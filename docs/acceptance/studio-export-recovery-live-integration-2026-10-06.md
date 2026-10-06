# Live export recovery integration

`src/studio/app/app_export_recovery.elisa` routes Studio GLB publication through
the prepared recovery adapter. The caller validates the GLB, JSON, and text
destinations before locking, then takes the Storage transaction lock, repeats
destination admission, captures the staging bytes, and prepares a durable
recovery package before the GLB rename. JSON and text completion use those
captured bytes. Dialog/status copy runs after the helper releases the lock.

The helper keeps at most 16 same-session recovery entries and 100,000,000
logical payload bytes across the output snapshot, reports, journal, and paths.
The payload is retained after the export result closes or a take is replaced.
`retained_export_recovery_count()` and `retained_export_recovery_at(...)`
provide the entry access API for the retry UI, which remains to be integrated.
Partial prepare failures retain up to 16 bounded path-only diagnostics; they do
not authorize retry or cleanup. The diagnostic paths are exposed through
`retained_export_recovery_path_count()` and
`retained_export_recovery_path_at(...)` for a later review surface. If the list
is full or a path cannot be represented, the result carries an explicit
diagnostic-unavailable flag and the UI must keep the staging path visible.
The retained `Record` is the immutable captured binding from preparation; its
stage fields are not a live view after publication. Any retry surface must
reread the journal under the matching workspace transaction lock and verify
the binding and exact retained bytes before using its observed/durable stages.

The byte cap is a logical retained-payload limit, not a physical RAM ceiling.
Appending the next payload uses a local copy followed by one global assignment.
The compiler's arena rehome may temporarily keep old/new global generations,
the local growth buffer, and staging/prepare buffers alive together. Peak
allocator high-water and native `arena_adopt` behavior have not been measured
or qualified, so this integration does not claim a 100 MB peak-RAM bound.

The `Prepared(directory)` result comes from the store's same-session create
chain. Before using it, the caller checks native path facts and rejects missing,
non-directory, or symlink paths. The binding adapter then rereads and matches
the journal plus every retained byte, and publication rechecks staging bytes
before rename. This is not inode continuity or a complete defense against
ancestor replacement races; native ownership authentication and fault-injected
crash recovery remain unqualified. The caller passes only the observed
same-session creation chain and current native path facts as the ownership
input.

The result preserves observed GLB publication if a later journal update,
sidecar write, Storage manifest update, or lock release fails. It records
unknown durability when either the GLB/report publication or its journal
update reports uncertain directory durability. Failures before GLB publication
keep recovery evidence and report actionable next steps. No retry controls are
present yet, so retained records are available through the API but not yet
selectable by the user.

Compilation and focused proof results are recorded after qualification; this
document does not assert runtime fault-injection or VoiceOver results.

## Recovery action availability (2026-10-06)

The panel and native accessibility controls now use the same
`StudioExportRecoveryUiPolicy::action_enabled` decision. Previous and Next
require at least two records. Retry and folder actions require a retained
record and their existing verification conditions; NoHit is always disabled.
Close and Refresh remain available for an empty inventory.

The common action dispatcher applies this decision before side effects, so
mouse and keyboard activation obey the same disabled state as accessibility.
Retry still performs its transaction and fresh validation before writing.
New navigation, empty-inventory and NoHit laws accompany the policy. The
conflict law's contradictory postcondition was corrected to assert its actual
claim that conflicts disable retry. These edits await current compiler and
certificate-replay qualification; no native interaction result is claimed.
