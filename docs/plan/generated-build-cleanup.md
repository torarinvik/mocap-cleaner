# Generated-build cleanup: remaining delivery slices

[Roadmap](../../IMPLEMENTATION_PLAN.md) · [M1](m1-workspace.md) ·
[Delivery queue](current-delivery-queue.md)

## Product result and current boundary

An animator can identify Studio-owned builds, understand why an item is protected,
review eligible items, move them into recoverable storage and restore them without
overwriting work. Moving a directory does not imply freed disk space.

Inventory, reviewed sealed-product Move, recovery discovery/reconciliation,
Restore, release retry, exact acknowledgment, path inspection and focus traversal
are implemented. Their current native fault, motion-preservation and usability
acceptance remains open. The captured native build is recorded in
[build evidence](../acceptance/studio-native-build-2026-10-07.md).

Failed/partial rows remain protected: they lack an owning admission path based on
durable creation evidence. They must not acquire a fictitious executable seal.
Pending receipt discovery preserves staged records; it does not resolve or delete
them. These are distinct remaining implementation slices.

## G01 — Stable current dependency and interaction snapshot

**Priority:** P0. **Owner:** integration/toolchain work.

- Agree a UI source checkpoint, verify its content manifest and record the exact
  included subset. Preserve agent repairs and fetch upstream before qualification.
- Rebuild with the selected current compiler and verify runtime source/product
  provenance as well as hashes. Use a matched current producer/replay pair.
- Capture source, native/header, SDK/tool, environment and product identities
  before and after compile, link and package. Drift refuses current qualification.
- Exercise selection, Confirm Move, progress, cancellation/draining, Retry Release,
  exact Resolve Review, refresh, restart discovery and Review/Confirm Restore.
- Cover keyboard, pointer and VoiceOver, minimum window size, Unicode and escaped
  byte paths, stale selection and source/retention changes. Return focus to the
  trigger; disabled controls must not remain actionable.

**Exit:** one reproducible current snapshot completes the journey, source-take
hashes are unchanged, unresolved operations remain visible and no test/proof
category is inferred from object compilation.

## G02 — Durable incomplete-artifact evidence producer

**Priority:** P0. **Depends on:** creation journal and bounded native scanner.
**Touchpoints:** creation scanner, candidate provider, creation/move policy laws.

- Return a distinct `OwnedIncomplete` evidence variant. Keep product identity
  absent. Bind root/artifact identities, creation revision/digest, exact terminal
  failure-event digest, observed-tree digest, lease identity and failure status.
- Verify an inactive builder through the retained lock/lease protocol. Absence of
  a process name, product file or pending request is not sufficient evidence.
- Validate the complete creation chain and its namespace. Refuse missing,
  malformed, foreign, duplicate, unsupported, conflicting or oversized records.
- Match a fresh bounded descriptor-based tree scan to the failure event. Preserve
  identities, types, modes, lengths and digests; distinguish read failure from EOF.
- Refuse symlinks, hardlinks, group/other-writable contents, replaced ancestors,
  unexpected permissions and unverified descendants. Owner write permission must
  follow the recorded creation protocol; do not make ordinary failed builds
  permanently ineligible merely because their legitimate generated files are 0644.
- Keep creation journals, control records and source takes outside the movable
  artifact tree. Unknown builder/recovery state remains protected with a reason.

**Proof exit:** decoding/domain and exact-binding laws; changed event/tree/lease
refusal; active/unknown builder refusal; bounds; incomplete evidence cannot satisfy
sealed-product admission. Qualification must authenticate the native producer's
correspondence to those facts.

## G03 — Owning Move wire and retained-lock admission

**Priority:** P0. **Depends on:** G02.
**Touchpoints:** Move evidence/wire, worker, native begin/commit binding.

- Use an ADT for sealed-product versus owned-incomplete evidence. Each branch
  carries only its applicable controls; retain explicit wire values at the ABI.
- Capture immutable source, selection, age and retention evidence before review.
  Confirmation checks exact bytes and revisions, never only names or lengths.
- Add a separate incomplete begin path. Under retained global/artifact locks,
  reread the creation chain and failure event, rescan the tree and revalidate all
  root/artifact/lease identities before recording the durable trash intent.
- Refuse current artifacts, active builders, publication intents, existing recovery
  conflicts, missing journal dependencies, changed controls and capacity overflow.
- Revalidate at the commit boundary. Cancellation after dispatch drains ownership;
  it does not turn an uncertain move into a successful cancellation.

**Proof exit:** all admission conjuncts and their refusal cases, stale confirmation,
integer retention boundaries, one owning token, no source-take mutation and no
cross-variant reinterpretation. A successful source build is not this exit.

## G04 — Receipt variant, exact recovery and Restore

**Priority:** P0. **Depends on:** G03 and existing recovery state machine.

- Version durable receipts to identify the evidence variant and exact creation
  controls. Reject unsupported variants; keep legacy migration explicit.
- Restore an incomplete tree from its recorded identity without requiring or
  inventing a sealed executable. Recheck dependencies and current artifact state
  under locks; an occupied or reused original name produces a protected conflict.
- Reconciliation binds receipt, source/quarantine parents and current location.
  Journal advancement does not rename an artifact or imply certain lock release.
- Finish the native producer and consuming UI for the implemented owned location
  snapshot (`StudioBuildGenerationRecoveryLocations`). The current adapter and
  laws compile but are unregistered: no native producer supplies its facts yet.
  Return each side's exact/absent/occupied/unsafe/unknown state with descriptor
  evidence binding canonical path bytes to entry and parent identities. Refuse
  partial output; never derive a quarantine path from an operation ID.
- Publish location observations only for the exact current ticket, selected row,
  root and operation. Workspace changes, reselection, Refresh and queued mutation
  invalidate reveal actions until a new observation arrives. Keep location
  inspection separate from Restore admission and recheck native facts at reveal
  dispatch; a previously verified path can be replaced before the user clicks.
- Show original and quarantine states separately. For an exact artifact, reveal
  its verified containing location; for a different occupant, reveal only the
  verified parent folder and explain the name conflict. Absent, unsafe, unknown,
  unavailable and refused outputs cannot produce a guessed reveal target.
  Include keyboard/VoiceOver names and disabled-action reasons, and return focus
  to the same retained operation after inspection.
- Preserve operation/root/artifact/path metadata through stale replies, cancellation
  and release retry. Acknowledge only exact current terminal evidence with zero
  owned handles, certain release and retained operation identity.
- Stage/torn receipts stay visible as unresolved candidates. Design their resolution
  separately; do not promote an unparsed pending payload or unlink it on scan.

**Exit:** native interruption/restart cases establish where the tree is and which
metadata remains required. Unknown, conflict and durability failures remain
protected; another Restore always requires a new review/confirmation.

## G05 — Review, explanations and repeated cleanup

**Priority:** P0. **Depends on:** G02–G04 admission, not merely row visibility.

- Show artifact kind, creation state, verified age, selected retention, exact path,
  owned bytes and the actionable protection/refusal reason.
- Explain incomplete-build cleanup in ordinary language. Keep developer digests
  in inspectable details rather than making them a prerequisite for review.
- Preview consequences before confirmation; distinguish recoverable movement,
  metadata retention and actual space reclamation. Do not promise freed space.
- Keep selected reconciliation results visible alongside unresolved-receipt warnings.
  Distinguish waiting, active work, stale evidence, partial results and protected
  errors. Offer Refresh/reselection when it can change the result.
- Define bounded ledger capacity behavior and later metadata retirement. Remove
  records only after proving no active/recovery dependency remains; never evict
  an unresolved operation to make a new mutation fit.

**Exit:** an unfamiliar animator can explain the candidate, protection reason,
consequence and recovery action using pointer, keyboard or VoiceOver.

## G06 — Native failure matrix and actual usability evidence

**Priority:** P0. **Depends on:** stable G01 snapshot plus G02–G05.

Retain disposable fixtures and terminal evidence under `build/`. Bind every result
to the exact source/product tuple and preserve original expectations.

| Case family | Required observation |
| --- | --- |
| Creation | Failure at creation, first write, intermediate object, link and seal; exact event/tree evidence or protected refusal. |
| Identity | Equal-length different roots/operations/paths, root relocation, replaced parent, inode reuse and stale retention refuse. |
| Contents | Empty and ordinary failed trees, read error, hidden descendant, symlink, hardlink, oversized/deep inventory and mode/content changes. |
| Ownership | Two Studio instances, active builder, busy token, duplicate activation and release uncertainty retain ownership/evidence. |
| Durability | Intent, rename and every journal/directory sync boundary; restart finds exact protected state without overwriting either location. |
| Recovery | Pending-only, malformed, truncated, duplicate and legacy receipts; reused original name; cancelled and late replies; exact acknowledgment. |
| Interaction | Minimum/resized window, longest path, Unicode/control bytes, maximum rows, disabled focus targets and restored trigger focus. |

Use real participant evidence for the release usability trial. Agent inspection
and automated checks can diagnose defects but cannot stand in for animator trials
or annotated motion-quality evidence. Keep each evidence category open until its
own required result exists.

## Producer checkpoint: failed-tree facts

Engine mocap commit `a29c9b2b` exposes the exact failed-tree verification result,
positive terminal failure status and builder-inactive observation made while the
artifact lease is exclusively locked. The tree digest is SHA-256 over the domain
`studio-failed-tree-native-v1\n` followed by Foundation sorted-key JSON for the
verified, path-sorted observed entries. This is a versioned native encoding,
not the Python creation-journal serialization. The latest-record digest binds the
exact failure event only for the verified revision-3 failed chain.

Non-failed final phases clear incomplete facts. A scanner observation does not
retain mutation ownership; begin/commit must reacquire and revalidate under locks.
Engine mocap commit `a0ec5e05` adds
`elisa_studio_build_candidates_incomplete` for the same immutable snapshot
token/index. It returns unavailable or verified evidence, positive failure status,
lease identities and inactive/tree verification flags. Verified requires the
revision-3 failed chain, no publication intent and representable scalar facts;
stale tokens and invalid indices refuse. Existing row access supplies the digests.

Elisa commit `3362f05` adds an owning incomplete-evidence ADT with exact journal
binding and refusal laws. Its initial adapter still decodes unavailable evidence.
The additive native API does not enable mutation: retained-lock admission and
variant-aware receipts/Restore remain open. Strict native syntax compilation
passed; fault/runtime acceptance and source-authenticated correspondence proofs
remain required.
