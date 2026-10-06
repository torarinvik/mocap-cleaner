# Recent proof and native boundary status (G83 onward)

[Proof gap index](../proof-gaps.md)

## Replay of summary dependencies (elisa-proof-mocap 19611a2, 2026-10-03)

- Replay gaps after e723e71 (cli main 30, glb_tracks 14): a certificate that
  used a callee's function summary was checked against the callee's name
  only. A same-named function in another module with a finding (or an
  unattributed line-0 finding, e.g. the control-flow-analysis budget on an
  `apply`) vetoed replay. Dependencies are now checked per declaration row
  (owner line); the budget finding is stamped at the body's first line; a
  bare call inside an included module matches its own module's summary.
  Now cli main 2779 proven / 2779 replayed / 0 gaps, rig_physics 0 gaps,
  retime 560/0, retime_laws 896/0. Regression: `examples/replay_dependency_row_probe.elisa`.
- `RigOps::run_clip` (rig_stack) has no IEEE float-parameter finding because
  it is not a masking problem: its `op.kind == RigKind...` enum comparisons
  raise contract-proposition-type findings, and the scheduler skips the body
  before the float check runs. It stays reported unverified (0 goals).
  Open: name-keyed recursion guard in replay; `--json` "functions" merges
  same-named rows.
- Full corpus vs `build/proof` reports 11 files "worse" (cli main 926 -> 1171
  unproven, etc.). The baseline predates 3244c9d/0c1a6df/e723e71; proven rose
  more in each (cli main 1488 -> 2779), i.e. G68 exposed more goals. cli main
  was already 1171 unproven before 19611a2; this commit changes no counts.

## Current key-weight certificate status (2026-10-05)

The sibling prover's JSON report for `proof/key_weight_laws.elisa` has no
findings: all 5 functions are proved, all 60 goals replay, and no replay gaps
remain.

## Local check baseline (2026-10-05)

`scripts/check.sh` records the reviewed per-file state and unproven-goal count
in `scripts/proof-baseline.tsv`. The 109-file snapshot recorded here had 69
proved, 16 unknown and 24 unsupported files. These counts describe that
snapshot, not the current corpus. The latest full run on 2026-10-05 rebuilt and
passed all 56 runtime tests and CLI checks, including the focused modal-policy
test, but the proof-baseline gate needs
review under the current semantic revision `866d1320416958d`: it reports broad
proved-to-unknown shifts, six existing unproven-count increases and ten source
or proof files without reviewed rows. The new sidebar layout source and laws
were individually proved and added as reviewed rows; the remaining shifts have
not been mass-rebaselined. Keep this check result distinct from a fully green
proof-baseline run.

The custom-overlay viewport visibility policy is now included in the reviewed
baseline: `src/studio/modal_policy.elisa` proves 2/2 obligations and
`proof/studio_modal_policy_laws.elisa` proves 18/18 with no certificate gaps.
Its focused runtime test passes. These rows record the current semantic
revision without changing any historical proof statuses.

## Issue grouping proof gap (2026-10-05)

- G83 (closed): parser annotations for `mutable name: T` are now imported into
  resource analysis, and writable capability is preserved through `for`
  captures. The fix is committed in `../elisa-proof-mocap` on
  `mocap-cleaner-proofs` as `632e4eb1`. A positive regression proves both a
  mutable local write and a captured loop accumulator; the existing negative
  control still rejects assignment to an ordinary immutable local. With this
  fix, `src/studio/issues.elisa` proves 33/33 obligations and
  `proof/studio_issue_laws.elisa` proves 45/45; both reports replay every
  certificate with zero gaps. The issue laws now state the boolean helper
  contracts explicitly. Increment examples are bounded at 10,000,000 so
  overflow cannot make adjacent values compare equal; this is a law precondition,
  not a production revision or subject-ID limit.

## Character binding coverage gap (2026-10-05)

- G84 (prover gap): `proof/studio_character_bind_laws.elisa` proves 82
  obligations and leaves one unknown. `coverage_is_monotone` needs
  `bound * 1000 / total <= (bound + 1) * 1000 / total` for `0 < total <=
  65535`, which is monotonicity of truncating division by a symbolic divisor
  after a nonlinear product; the solver returns unknown. The policy itself
  (`src/studio/character_bind_policy.elisa`) proves fully once `coverage`
  returns `FULL` explicitly for `bound == total` rather than relying on
  `total * 1000 / total == 1000`. `test/studio_character.elisa` checks the
  monotone law exhaustively for every total up to 256 pending prover support
  for division monotonicity lemmas.

## Prover artifact identity audit (2026-10-05)

- G85 (open, build/replay identity): the current `../elisa-proof-mocap`
  checkout is clean on `mocap-cleaner-proofs` at `632e4eb1`, but its built
  `elisa-proof` manifest names source head `00146e4d` and says the source was
  dirty; no matching replay manifest is present. That binary reports
  `proof/fade_laws.elisa` as `proved_with_replay_gaps / unknown / open` with
  134 of 150 certificates replayed and 16 gaps on call-dependent
  `Fade::ramp`, `weight` and `ease` summaries, with no failed or unproven
  goals. The latest cleaner check at semantic revision `866d1320416958d`
  reports 132 cached files and no rechecks, alongside broad unrelated
  `proved/0 -> unknown/0` transitions. The current prover source change
  concerns mutable local/captured loop bindings, which fade does not use.
  This points to a stale/mixed checker or replay product, not a fade kernel
  defect. Rebuild the prover and replay tool from the same source revision,
  verify their manifests, then check a tiny direct-summary fixture and the
  fade laws before considering any baseline change.

## Full check after session annotation and contact-frame slices (2026-10-05)

`scripts/check.sh` rebuilt and passed all 64 runtime tests. The four CLI
checks (clean/report, folder batch, hands/diff and retime) also passed. The
proof pass used the recorded semantic revision `866d1320416958d`: it reported
138 cached files and 8 direct proof runs, then exited at the baseline gate.
That gate still reports the G85-related broad `proved -> unknown` replay
shifts, increased open counts in existing files, and files without reviewed
baseline rows; no broad baseline update was made. The new session annotation
laws prove 59/59 with no replay gaps. The isolated contact-frame kernel and
laws have no unproven obligations (9/9 and 23/23), but remain `unknown` only
because their certificates hit the same replay gap described in G85. Review
new rows after the prover/replay products are rebuilt from matching sources.

## Contact frame limit expansion (2026-10-06)

- The contact endpoint and stored-edit caps now match the timeline's
  10,000,000-frame limit. The focused endpoint laws remain proven (23/23),
  while expanding `StudioContactEditor::MAX_FRAMES` broadens symbolic nudge
  obligations: `studio_contact_editor_laws` reports 5 unknown/timeouts and
  `studio_contact_nudge_laws` reports 9 unresolved obligations. These are
  arithmetic proof-budget gaps at the larger bound, not runtime failures. The
  focused executable tests pass through the new cap. Follow up in
  `../elisa-proof-mocap` with bounded arithmetic/case lemmas before recording
  the larger nudge domain as fully proved.

## Storage cleanup policy laws (2026-10-06)

- The manifest identity envelope is now isolated in
  `src/studio/storage_receipt_policy.elisa`; its laws prove 18/18 obligations
  with every certificate replayed. The versioned path-safe manifest codec is
  runtime-covered by `test/studio_storage_manifest.elisa`. It rejects malformed
  UTF-8 and leaves output unchanged on malformed records. The engine exposes
  canonical identity snapshots for registered files. Atomic manifest
  publication and UI integration are still open.
- G86: `proof/studio_storage_cleanup_policy_laws.elisa` proves 351 of 353
  obligations with all 351 certificates replayed. The two open laws are
  `eligible_items_have_no_protection_reason` (the verified eligibility gates
  do not yet establish the exact zero-valued explanation code through the
  reason-function summary) and `selected_bytes_never_overflow` (the verifier
  does not close the exact-sum claim from the safe subtraction bound through
  `next_total_bytes`). The eligibility, review/confirmation, and bounded-total
  kernels themselves are verified; focused executable coverage passes. Keep
  these two laws open until the proof kernel can derive those exact summaries.
- Prover commit `dc78978d` now permits calls to verified total-pure functions
  in executable postconditions, with a separate purity/totality check for
  those callees. Applying it to these two laws did not close either gap:
  routing `protection_reason` through the full `eligible` summary pushed its
  postcondition obligations over the proof budget, while the exact-sum
  postcondition still lacked a verified executable summary. The attempted
  contract edits were removed; the 351/353 baseline remains authoritative.

## Issue explanation model (2026-10-06)

- G87: the prover reports `unsupported runtime expression` for the populated
  `StudioIssueExplanation::Explanation{...}` aggregate returned by
  `StudioIssueExplanation::explain`. Removing that builder removes the
  unsupported finding. The explanation record assembly remains runtime-tested
  in `test/studio_issue_explanation.elisa`; it is not claimed as proved. The
  classification policy was split into
  `src/studio/issue_explanation_policy.elisa`, whose focused laws prove 16/16
  obligations with every certificate replayed. Keep the proof boundary there
  until Elisa Proof models aggregate record construction and field projection.

## Storage totals model (2026-10-06)

- G88 (resolved by removing unused aggregate adapter): Studio now calls the
  proved scalar totals kernel directly. The unused `Totals`/`DisplayAmount`
  wrapper was removed after a repository reference audit found only its test
  used it. No aggregate mutation or construction is needed for this feature.
  Scalar source and law proofs establish exact accumulation and display unit
  bounds; runtime tests pin limits to the manifest schema and exercise full
  capacity and invalid sizes. UI byte totals remain exact.

## Storage retention age arithmetic (2026-10-06)

- `src/studio/storage_age_policy.elisa` bounds signed filesystem timestamps and
  nonnegative clock facts before age calculation. It avoids signed timestamp
  subtraction unless the age is below the cleanup saturation cutoff, counts
  completed days, and clamps old receipts at the existing 365000-day cleanup
  limit. Its source proves 20/20 obligations and its focused laws prove 46/46,
  with every certificate replayed. Runtime boundary coverage is in
  `test/studio_storage_age_policy.elisa`.
- The age proof exposed a report-accounting invariant that incorrectly required
  branch-specific proof attempts to be no greater than source obligations.
  A return-heavy function can produce multiple independently replayed attempts
  for one source obligation. The prover's report invariant was corrected and a
  regression fixture verifies the source-level totals, per-attempt certificates,
  and fully proved status together. The previously unknown age report is now
  fully proved; no timestamp bound or requirement was weakened.

## Deterministic call replay across stable conditionals (2026-10-06)

- G89: independent replay previously rejected deterministic helper-call witnesses
  inside an `if` arm or after an early-return guard. The source-site walker now
  searches each arm with a cloned binding state, and crosses a join only when
  both arms preserve outer bindings. Arm-local declarations are supported;
  assignments to outer locals and unsupported control flow still fail closed.
  The regression covers a helper call in a conditional return, after an early
  return, after a branch-local declaration, and after a declaration-only join;
  all 17 obligations and certificates replay. This restores `fade` (103/103),
  `key_weight` (36/36), `offset` (205/205), and their `key_weight` laws
  (60/60). G89 also included qualified scalar-call resolution by module path
  and source-validated constant arguments, so same-named functions in other
  modules no longer block replay. Gate and gate laws now fully replay (167/167
  and 235/235). Retime improved to 548/560, retime laws to 862/896, and footing
  to 322/342 (footing laws 411/437); those remaining gaps are still under
  investigation. No established baseline was downgraded.
- A follow-up matcher compares nested binary and unary call arguments
  structurally while requiring source-validated constant facts at literal
  substitutions. The regression with a helper call inside a binary argument
  proves and replays 30/30 certificates. This further improves footing to
  326/342 replayed certificates; 16 replay gaps remain. Retime remains at
  548/560 replayed certificates (12 gaps), so the larger caller-summary issue
  is still open. The attempted constant-aware summary comparison did not
  change either report and was discarded.
- The shared 12-certificate gap is localized to `range_step`: retime reports
  the failed owner at line 314, and session-band laws report it at line 318.
  Both traces are calls to `range_weight`; all seven recorded callee
  precondition goals replay. The unresolved evidence is therefore in the
  call-summary/call-witness path, not those precondition proofs. Further
  diagnostics are pending a build against the current compiler source.

## Issue browser and accessibility policies (2026-10-06)

- The nested conditional in `node_parent`'s result contract was unsupported.
  `node_parent` now states equality with the executable `parent_for_id` mapping,
  whose per-ID guarantees cover the issue group, all six filter controls, the
  navigation controls, and both visible finding rows. The two filter-control
  laws are expanded into six exact cases; this preserves the original finite
  predicate domain without relying on the prover to unfold a symbolic predicate
  through the parent call.
- G90: `navigation_target` calling `previous_target` or `next_target` from a
  conditional return did not transfer the callees' result bounds into the
  caller, leaving four obligations open and four replay gaps. The caller now
  spells out the same scalar wrap cases directly. The helper kernels retain
  their independent contracts and proofs; this caller workaround is documented
  until branch-return call-summary propagation is proved end to end.
- `StudioAccessibility::next_sibling` exceeded the control-flow step budget by
  one step. Its existing relationships are split across toolbar, contact,
  sidebar, and workspace helpers. Current source and law reports are fully
  proved: issue browser 255/255, issue laws 311/311, accessibility 290/290, and
  accessibility laws 334/334; all certificates replay.

## Storage preference file reader (2026-10-06)

- `src/studio/io/storage_preferences_codec.elisa` is a pure, exact-length
  codec for `mocap-storage-preferences-v1\nretention-preset=<0..3>\n`.
  Its source report proves 128/128 obligations with all certificates replayed.
  The focused codec laws prove 130/130 obligations; they pin the exact record
  length and its fit within the reader limit. The strict reader accepts at most
  128 bytes and changes its output only after a successful close and decode.
- G91: a separate law connecting `header_matches` to the same exact byte
  predicate did not replay its final goal (132/133 goals replayed); the
  duplicated-predicate version was removed. The source contract itself still
  directly proves the header implementation 128/128, but the independent law
  connection is not claimed until proof replay can establish it.
- The libc-backed `src/studio/io/storage_preferences_file.elisa` remains a
  runtime adapter. Its direct proof report has 129/133 obligations and four
  unsupported findings: the prover cannot form propositions for the nullable
  `FILE*` branch and `ferror` call in the IO effect region, and cannot encode a
  resource summary through the final adapter call. It is not claimed as
  proved. The runtime path distinguishes open, read (`ferror`), size, close,
  and format failures through `load_status`; the bool `load` entrypoint reports
  success only after all checks pass.

## Storage exemption file adapter (2026-10-06)

- `src/studio/io/storage_exemptions_wire_policy.elisa` isolates the exact
  28-byte `mocap-storage-exemptions-v1\n` prefix. Its source proves 58/58
  obligations and focused size laws prove 60/60, with every certificate
  replayed. The file adapter delegates record parsing, duplicate rejection,
  paths, and manifest bounds to `StudioStorageManifest::decode` and applies
  exemption-only state and identity checks before changing caller output.
- The adapter's direct report includes the manifest parser and libc IO graph:
  the latest report has 640 obligations, 572 proven, and 73 findings, with
  unresolved loop/index proofs in manifest parsing, unsupported native IO
  effect propositions, and an opaque output resource summary. The adapter is
  not claimed as proved. Its runtime load status keeps open, read, capacity,
  close, and format failures distinct; atomic publication remains the caller's
  responsibility through the existing publisher.

## G92: composed inspection step replay (2026-10-06)

Storage inspection has verified exact next/previous helpers and a total
wrapper that rejects invalid counts and proves its output stays in bounds.
Source proves 37/37 and the bounds/helper laws prove 55/55 with full replay.
Independent forward/backward step laws through `inspection_target` still
leave two goals unknown, despite the helpers' exact contracts. The current
proof boundary verifies the helpers and wrapper bounds separately; composed
step replay remains open. Earlier direct implication contracts on the
unbounded wrapper also left forward-return goals unknown.

## G93: CLI destination and publication boundaries (2026-10-06)

`CliOutputGuardPolicy` source proves 61/61 obligations, with all 61
certificates replayed. Its admission contracts reject unresolved/outside paths,
source aliases, existing outputs and reserved metadata. Its laws report 73/79
proven with six unresolved ensure obligations, no semantic diagnostics and
73/73 certificates replayed. The array-construction/path-composition laws are
not claimed as fully proved. The sibling-prefix law now excludes a leading
slash, which would otherwise construct a legitimate descendant.

The authorized integration check recorded these runtime adapter scopes:

| Module | Proven | Unproven | State |
| --- | ---: | ---: | --- |
| CLI output guard | 62 | 14 | unsupported |
| CLI GLB publisher | 248 | 265 | unsupported |
| CLI private worker directory | 1 | 4 | unsupported |

Native realpath/lstat/identity/Unicode facts and filesystem IO are trusted
runtime boundaries. Preflight checks cannot pin directories against later
changes. GLB bytes are written through the original mkstemp descriptor,
flushed/synced, reloaded and compared before create-only hard-link publication.
Final destinations cannot be replaced by that link operation. A temporary-name
replacement between validation and linking remains possible; directory sync,
crash durability and orphan-temporary cleanup are not established. Non-macOS
namespace comparison currently has only ASCII case-fold coverage.

Report, saved-operation and worker-part writers use exclusive creation and
check completion. `OutputCompletionPolicy` proves 4/4 source and 10/10 law
obligations with full replay; it proves the boolean completion gate, not libc
write/close behavior. Failed writes may leave partial new artifacts.

The integration check rebuilt 78 executables: 77 passed and `rig_tools` exited
43 because its previous generated ops destination existed. The named fixture
reset was corrected and its focused rerun passed. All four CLI scenarios
passed. Strict native Storage verification still stopped at stale stage1
provenance, and the proof gate retained existing regressions and missing
reviewed baselines. No green full-check claim is made at this head.

## G94: module extraction proof comparison (2026-10-06)

Track was extracted into support, filter, contact and plant modules, preserving
function bodies and contracts while making implementation helpers private.
The composition root and the original file were both checked with the same
current prover: each reports unsupported, 926 proven and 17 unproven.
This matches the pre-extraction result but still exceeds the stored 15-open
baseline. The old baseline remains unchanged; extraction is not a proof fix.
The CLI build and the existing track-tools test pass. New module baselines
record their reviewed current results, including existing unresolved goals.
