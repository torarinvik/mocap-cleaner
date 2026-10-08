# Current delivery queue: highest return first

[Roadmap](../../IMPLEMENTATION_PLAN.md) · [Shared acceptance](acceptance-and-dependencies.md)

Updated 2026-10-08. This is the execution order for the entire remaining M0–M8
roadmap. Priority changes do not remove requirements. Detailed milestone and
acceptance documents remain authoritative for each slice. Completed source
needs qualification, not another implementation. Historical binaries and proof
reports remain comparison evidence.

## Selection rule

Choose work that removes a demonstrated blocker, protects user data, or completes
a usable end-to-end workflow. Prefer a small integrated fix over a new feature
that cannot yet run. Rank by user impact, dependency unlocks, recurrence and
implementation/qualification cost. Reassess after an integrated build or a
completed journey; do not invent numeric ROI scores without measured inputs.

Keep one primary product blocker active. Dependency owners can repair their
existing compiler, prover and native slices alongside it. Each handoff identifies
an exact source/product tuple, failing fixture, next action and finish evidence.
Serialize heavy compiler jobs and monitor aggregate descendant memory. Avoid
unrelated style sweeps, duplicate policy implementations and new algorithms
until the first usable journey passes.

## 1. Q01 + J01: produce a current build and fix the reported redraw crash

**Priority:** P0. **Return:** restores the user's ability to use the product and
unlocks every native UI acceptance check.

1. Repair grouped family grants in the compiler. Preserve exact members in
   declaration validation, direct global access, unsafe checks and transitive
   calls. Require positive grouped/expanded equivalence and partial-member
   refusal controls; a family name must not accidentally grant every member.
2. Finish mandatory global permission migration across Studio and included UI
   dependencies. Read-only owners use `Global.Read`; mutation propagates write
   authority. Use grouped syntax where appropriate. Preserve unsafe tracking
   with `can`; no blanket `trusted`, permissive mode or disabled checker.
3. Fetch current dependencies while preserving project repairs. Build and verify
   source/product/runtime/link correspondence. Freeze the actual input closure
   for qualification; changed inputs invalidate the attempt.
4. On that tuple, reduce and repair any remaining native emission failures,
   including private-ledger initialization and generic worker-result reads.
   Preserve privacy, affine ownership and caller-owned allocation lifetimes.
5. Build/package Studio, identify the exact executable, then reproduce the
   reported FBX/redraw failure. The historical `14bdc130` binary crashed after
   importing 337 frames; it cannot qualify current source. Inspect the allocation
   and ownership boundary before choosing a fix.
6. Qualify FBX open, Character/Skeleton switching, framing/orbit/zoom, playback,
   repeated redraws, edits, replacement, cancellation, close and restart on the
   reported asset and bounded controls. Preserve the original file bytes.

**Finish evidence:** current sealed build; exact crash reproduction and repair
record; actual native interaction on the repaired binary; focused lifetime
controls; source hash unchanged; no stale candidate publication. A seed, clean
single-file diagnostic, screenshot or live process is insufficient.

**Current status:** individual global-owner migrations have reduced diagnostics,
but the complete closure still fails. Grouped syntax is prepared in source but
compiler repair/qualification is pending. The user-visible crash remains open.
See [compiler qualification](compiler-qualification.md),
[responsiveness](m5-responsiveness.md) and [proof gaps](../proof-gaps.md).

## 2. J01: make open/import failure and workspace setup self-explanatory

**Priority:** P0. **Depends on:** a runnable current build.
**Return:** removes the confusion demonstrated in the user's screenshots.

- Open FBX directly through the ordinary Open action. If a workspace is needed,
  offer a visible chooser and explain the derived-file location; continue the
  retained request automatically when ready. Cancel preserves the current take.
- Present a persistent, readable failure summary with Details and a relevant
  Retry/Choose another file action. Expose complete text to accessibility.
- Keep filenames, status and primary controls usable at minimum window size;
  cover long paths, enlarged text, scale changes and repeated failures.
- Disclose when Character view is unavailable and how to obtain a usable mesh.
  Toggle state and the rendered view must agree through pointer, keyboard and
  accessibility actions.
- Qualify existing source changes before adding more status policies or wrappers.

**Finish evidence:** recorded first-use open/import journey, unavailable workspace
and malformed-input recovery, loaded-take refusal, focus restoration, matching
visible/accessible feedback, and unchanged document/source on failure.
See [M1](m1-workspace.md) and [shared interaction acceptance](acceptance-and-dependencies.md).

## 3. Q02: close safety-critical proof gaps alongside the production paths

**Priority:** P0 for publication, ownership and data-preservation contracts.
**Return:** gives credible guarantees for the transitions most costly to get wrong.

- Prioritize source identity, worker ownership, cancellation/stale publication,
  transactional history, FFI admission, export publication and storage mutation.
- Qualify the actual production handoff: native status alone must not be copied
  into several booleans and presented as independent staging evidence.
- Repair exact lexical owner/type/constant provenance and real functional theorem
  production. Resource-safety replay cannot stand in for an ensure theorem.
- Model short-circuit helper contracts under their actual branch guard. Retain
  branch-specific precondition obligations; never introduce an unguarded helper
  equality from a call that may not execute.
- Authenticate exact source/expanded import closure, then independently replay.
  Retain wrong-owner, reordered-argument, changed-source, false-assertion,
  malformed-owner and missing-precondition refusal controls.
- Rebuild matched products after relevant repairs; qualify cache reuse by each
  product's actual input identity. Report compile, declaration proof, replay and
  source correspondence separately.

**Finish evidence:** intended critical predicates authenticated and replayed on
current source, with meaningful negatives and production/native binding evidence.
Unresolved obligations remain explicit gaps. Do not weaken contracts to obtain
passing counts. Secondary convenience-law gaps follow the critical path rather
than monopolizing the first usable-build repair.

## 4. J02 + J03: finish one inspect–preview–apply–undo–export journey

**Priority:** P0. **Depends on:** steps 1–3 for affected paths.
**Return:** demonstrates useful cleanup rather than a collection of controls.

Use one labelled noise fixture and one contact fixture. Select a finding without
editing, jump to its frame/joint, explain scope and trade-offs, preview adjacent
motion/source/result, apply once or cancel, undo/redo, save/reopen, export/reopen.

- Keep pending drafts distinct from committed history and last-valid results.
  Failure/stale work cannot change history or claim a draft was saved/exported.
- Keep units, sample domains, time/frame indexing and source/settings identity
  consistent across Studio, CLI and reports. Unknown/overflow/zero-sample metrics
  remain unavailable rather than apparently successful zeros.
- Finish range, anchor and parameter inspection and keyboard/accessibility
  alternatives for exposed tools before adding another cleanup algorithm.
- Use preservation thresholds fixed before candidate comparison. Intentional
  fast movement needs labels/evidence rather than being assumed to be noise.

**Finish evidence:** complete native journeys; current/candidate identity parity;
quality/preservation gates; refusal/cancellation; meaningful history; session and
export round-trip parity. See [M2–M3](m2-m3-diagnosis-review.md),
[M4](m4-contact-repair.md) and [physics migration](physics-unit-migration.md).

## 5. J04: reliable single export and recoverable cleanup

**Priority:** P0. **Return:** protects user work and makes generated storage manageable.

- Complete captured-result GLB/report staging, partial outcomes and retry.
  Preserve occupied outputs and sources; restart cannot silently publish a
  different revision. Distinguish integrity, reviewed motion and durability.
- Finish Storage review/move/receipt/restore and generated-build cleanup with
  exact retained identity, active-product leases, durable journals and conflict
  refresh. Quarantine moves are recoverable storage, not claimed freed space.
- Integrate typed reconciliation identity and the read-only recovery-location
  observer. Observe under descriptor locks/rechecks, return no reveal path on
  uncertainty, and reobserve exact binding before reveal. Observation alone
  never grants Restore or mutation authority.
- Cover source-path/identity substitution, stale reviews, active builds/apps,
  uncertain lock release, torn receipts, interruption and restart at every
  relevant publication/move stage. Preserve required diagnostic evidence.
- Show selected scope, destinations and consequences before mutation; provide
  understandable Restore/Retry/reveal choices and retain recoverable failures.

**Finish evidence:** one native export/reopen/recovery journey and one native
cleanup/restore/restart journey, including injected failures, exact ABI and
identity controls, proofs and source preservation. Existing pure policies or
native helper tests do not qualify the complete controller/UI.
See [generated cleanup slices](generated-build-cleanup.md) and [M6](m6-export-batch.md).

## 6. P01: qualify responsiveness and professional interaction

**Priority:** P1; regressions affecting steps 1–5 remain P0.

Measure long takes and supported dense/max-capacity layouts on fixed reference
hardware. Keep cancellation, progress, draft visibility and last-valid preview
responsive. Qualify focus, semantic IDs/actions, minimum windows, text density,
capacity refusals, process lifetime and aggregate memory. Keep the intermittent
renderer memory gate open until the original threshold passes repeatably; stable
sampled heap/GPU counters alone do not explain retained process growth.

**Finish evidence:** repeatable timing/memory records and actual pointer,
keyboard/accessibility completion at supported limits. See [M5](m5-responsiveness.md).

## 7. P02 + P03: repeat work, packaging and release

**Priority:** P1 after the single-take journey.

Finish compatible recipes, reviewed batch production, partial/cancelled outcomes
and honest availability summaries. Qualify installation/Finder/copied-bundle
launch, signing/distribution, clear first-use documentation and real user trials.
External distribution/participant decisions remain explicit dependencies.

**Finish evidence:** native repeat-work journeys, source/report identity parity,
release package and complete M7 acceptance. See [M6](m6-export-batch.md) and
[M7](m7-release.md). A single-take release is not completion of the entire plan.

## 8. R01: remaining M8 decisions

**Priority:** P2; preserve all requested research candidates.

Evaluate against labelled baselines, preservation gates and measured runtime.
Record an evidence-backed adopt/reject decision for every candidate; adopted
work receives implementation, proof, UX and qualification criteria before it
changes defaults. See [M8](m8-research-and-order.md).

## Evidence and handoff discipline

Commit small source/proof improvements; combine documentation changes with a
source commit. Keep failed attempts and unresolved acceptance visible. Every
slice needs its actual compiler/prover/native/UI evidence at the appropriate
scope. Reassess this order when a blocker is removed or evidence changes; keep
all detailed requirements until proven complete.
