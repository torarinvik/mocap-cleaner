# M1: workspace, storage and recovery

[Roadmap index](../../IMPLEMENTATION_PLAN.md)

## 6. M1 — A workspace that explains itself and protects work

### 6.1 Information architecture and layout

- [ ] Organize the workspace into document header, labelled primary actions,
      viewport, issue/rig browser, context inspector, timeline and status.
      Keep the currently selected clip, source and dirty state visible.
- [ ] Provide sensible initial panel sizes; add resizing, scrolling and
      collapse behavior. Prioritize the viewport and timeline at small
      sizes; avoid controls falling outside the window.
- [ ] Add single-view and multi-view layouts with a visible active-view
      indicator. Persist layout/camera preferences separately from cleanup
      parameters. Provide Reset workspace.
- [ ] Create shared spacing, type, color, focus, disabled, selected, warning
      and error tokens. Use the existing icon family consistently and retain
      readable labels for primary actions.
- [ ] Check Retina scaling, long paths, large numbers, dense rigs and resized
      windows. Budget draw commands explicitly; virtualize or clip long
      lists instead of dropping arbitrary controls.

### 6.2 Commands, focus and accessibility

- [ ] Complete visible Edit/View/Cleanup/Help command paths and context menus
      where appropriate. Centralize labels, shortcuts, enablement and dispatch
      so menus, toolbar controls, contextual actions and shortcuts stay in
      sync. Add a searchable command palette (P1) after the primary paths are
      consistent.
- [ ] Make tab order, focus rings, button activation and list navigation
      consistent. Verify numeric drafts and future search fields through the
      running-window keyboard path, including focus announcements and field
      dismissal.
- [ ] Make every gesture available through a labelled alternative: range
      fields for drags, menu actions for contact edits, numeric transforms
      for gizmos, buttons for navigation and stack ordering.
- [ ] Specify Escape for menus, dialogs, numeric drafts, selection, contact
      drags and gizmos. Focus loss cancels transient drags safely, clears
      modifiers and leaves committed document edits unchanged.
- [ ] Provide native accessibility roles, names, values, actions and focus
      announcements through elisa-ui/host facilities. Prototype timeline and
      viewport alternatives early; document any platform blockers. Add
      semantics for operation rows, timeline/contact controls, viewport
      selection and guide screens. Represent dialogs with an announced
      heading, concise instructions, available choices and predictable focus;
      restore focus to the invoking control after dismissal. Ensure role
      actions match the actual control and never expose unrelated actions.
      Validate a keyboard-only and VoiceOver import–review–repair–compare–export
      path, including search/numeric fields that must swallow global shortcuts.
- [ ] Distinguish source/result and issue severity with labels, symbols and
      line styles as well as color. Respect reduced-motion settings for
      decorative transitions; maintain readable text contrast.
- [ ] Add concise contextual help: what a control changes, units, safe range,
      relevant shortcut and likely side effects. Avoid unexplained terms
      such as wring in primary labels; retain technical terms in advanced help.

### 6.3 Document lifecycle and recovery

- [ ] Make workspace root changes transactional: stage and validate every
      derived path before replacing active buffers or persisting preferences.
      Public path builders must read the active root, never rejected staging
      state. Cancellation and failure retain the current document and root.
      On success, invalidate old Storage inventory, selection and cleanup
      previews, then reload the new root's manifest and preferences. Captured
      jobs and export review destinations must remain bound to their snapshot
      or be explicitly invalidated; a root switch must not silently redirect
      publication. Qualify rejected-root, long-path, active-job and repeat-switch
      cases through the native UI and path-policy proofs.

- [ ] Establish an explicit canonical workspace root with a writable `build/`
      directory. Persist its location separately from source/session contents;
      show it and offer Locate workspace when unavailable. Finder launch,
      changed working directories, read-only/removable volumes and cancelled
      setup must preserve the document and resolve artifacts consistently.
      Never fall back silently to `/build` or the source-take directory.
- [ ] Exercise replacement, window-close and Cmd-Q prompts on screen,
      including Save/Discard/Cancel, Escape, repeated close requests and save
      failures. Confirm that unreadable, damaged and mismatched sessions are
      rejected before the dirty-document prompt; failed saves preserve the
      prompt and edits; and cancellation leaves the document usable. Keep
      unsaved-work warnings visually distinct from ordinary status feedback.
- [ ] Persist reusable rig profiles, units/floor settings and every exposed
      cleanup parameter alongside the existing v4 source/animation identity
      and local repairs. Version the next schema and define migration behavior
      that preserves the original file until the user saves the migrated copy.
- [ ] Resolve missing or changed sources with Locate source and explicit
      rebind review. Never silently apply old bone indices to a different rig.
      For v4, load the selected file and compare its computed fingerprints,
      animation identity, frame count and node count. Two rolling residues do
      not establish exact byte equality. Require an explicit Restore session
      review for matching metadata, with Cancel and Open as new take available;
      identify the legacy binding limitation without claiming proof of source
      identity. A matching saved identity alone is not evidence about a newly
      selected file. When metadata differs, offer Open as new take without
      session repairs or Cancel; explain
      that existing work remains available until replacement is confirmed.
      Implement changed-rig rebind in the next schema using stable semantic
      bone identities, an inspectable old-to-new mapping, ambiguity refusal and
      a summary of unmapped repairs. Never infer that equal node counts make
      stored indices safe. Retain the original session during migration.
- [ ] Strengthen the next schema's source binding: record versioned content
      digest, byte count, animation selection and semantic rig identities.
      Specify the digest's collision-resistance assumption explicitly; only
      direct comparison of retained original bytes establishes exact byte
      equality. Validate correction node ownership against the semantic rig
      before applying stored indices. Cover duplicate/renamed bones, reordered
      nodes, equal-count different rigs, digest mismatch, truncated data and
      unsupported digest versions. Missing legacy binding evidence requires
      review or refusal rather than silent promotion during migration.
- [ ] Qualify session and Locate reads at zero bytes, exactly the 8 MiB limit,
      one byte over the limit, read failure and close failure. The bounded
      reader preserves its output on failure; the UI must also preserve the
      active document, pending edits and recoverable candidate state. Explain
      oversized, unreadable and unsupported files with actionable messages.
      Keep Cancel available for every invalid candidate, skip disabled choices
      during keyboard navigation and restore focus after dismissal. Exercise
      chooser cancellation, repeated activation and replacement-save failure.
- [ ] Add bounded autosave/recovery snapshots in `build/`, a clear Restore
      or Discard flow, retention policy and cleanup controls. Recover committed
      edits only; distinguish autosave from the user's saved session.
- [ ] Explain damaged/unsupported session fields and any dropped corrections
      in a recovery summary. Preserve the original session and refuse unsafe
      newer schemas without replacing current work.
- [ ] Add in-app recent takes/sessions with missing-file handling and Clear
      recents. Remember paths as preferences, not embedded source copies.

#### Storage cleanup and Restore experience

The remaining work below builds on the current inventory, identity-backed
selection, retention presets, reviewed batch move, receipt reconciliation and
Restore implementation. Current implementation and evidence are recorded in
`docs/studio-ux.md`; running-window and failure-path acceptance remains open.

- [ ] Add inspectable hard-link/allocation accounting to the overview and
      qualify timestamp presentation through native inputs. Label logical
      bytes, allocated bytes reported and unknown measurements separately.
      A verified link count of one does not establish reclaimable space on
      APFS: clones and snapshots can retain extents. Keep recoverable space
      unknown unless exclusive extent/snapshot ownership is established.
      Moving to Trash must never claim space has been freed. Verify totals
      and no-eligible explanation at all supported inventory sizes.
- [ ] Extend artifact metadata to saved recovery sessions and register
      interrupted/temporary exports at their actual creation sites. Record
      creation time, session/recovery dependencies and build-relative location
      alongside the canonical identity. Migrate older manifests explicitly;
      missing dependency/time evidence stays unknown and protected. Do not
      infer ownership from names or sweep arbitrary files in `build/`.
- [ ] Replace blanket recovery protection with verified dependency tracking:
      retain the snapshots needed by open documents, saved sessions, recovery
      generations and pending jobs. Preserve source/alias, manifest and active
      output protection. Exercise fresh eligibility with changed sources,
      symlink replacement, future timestamps and unavailable clock/filesystem
      facts; unknown evidence must never permit a move.
- [ ] Add grouping, sorting and search. Qualify the implemented type/eligibility
      filters with native inputs and retained hidden selections. Show each
      row's kind, modified age, exact size and build-relative location. Qualify
      the implemented recorded-original-path inspector at the minimum window
      size with native pointer, keyboard and accessibility inputs. Support bounded
      rendering and scrolling through large inventories and review sets.
- [ ] Add an explicit scanning state and keep the screen responsive during
      slow scans and filesystem operations. Distinguish first use, empty,
      no eligible files, stale analysis and partial failure. Exercise existing
      read/save errors with permission failures and malformed manifests; offer
      Refresh, retry, containing-folder access and inspectable details.
- [ ] Put the protection reason beside every protected candidate, with a
      detailed explanation on demand. Outside-root records need a safe
      explanation rather than silently disappearing; source takes must never
      become cleanup rows. Verify that pointer, keyboard and accessibility
      activation cannot select a protected file. Use text/symbols as well as
      color, and never suggest bypassing a protection rule.
- [ ] Add safe group selection with an explicit scope after filtering. Show
      eligible/protected counts separately from selected count/bytes. Verify
      that selection survives sorting/filtering by exact identity, drops stale
      or newly protected files with an announcement, and remains empty on
      first use. Check Select eligible and Clear selection at all capacities.
- [ ] Complete the multi-file review: every selected name, original location,
      destination and exact size must be inspectable without cancelling the
      review. Add dedicated review scrolling and full-path details. Exercise
      changed set/size/retention immediately before confirmation and between
      moves: stop, update the review and require explicit confirmation again.
      Keep Restore and Finder's permanent-deletion role clear beside the action.
- [ ] Qualify receipt durability and crash boundaries with generated fixtures:
      interrupt before/after native move and atomic receipt publication;
      inject write, rollback and recovery-lookup failures; restart and reconcile
      the exact identity. Verify retained receipts, known original restoration
      and unknown locations are reported accurately, with a manual Finder
      recovery path. Never overwrite malformed manifests or claim freed space.
- [ ] Exercise the implemented manifest lock and complete-content review
      version protocol with two Studio instances and a retry during an external
      manifest update. Verify other receipts survive, stale reviews are rejected
      and successful moves stay out of subsequent retries. Validate cancellation at
      every item boundary, terminal unknown/recovery stops, duplicate activation,
      maximum batch size and refreshed per-item accounting.
- [ ] Qualify ancestor-directory replacement, root relocation/remount and
      source aliases between validation and mutation. Prefer descriptor-bound
      native operations where supported; document remaining race boundaries
      and refuse uncertain mutations. Distinguish atomic namespace publication
      from crash durability, including directory synchronization failures.
- [ ] Add a dedicated **Recently moved to Trash** view with original location,
      recorded move date and Restore. Extend/migrate the receipt schema for
      move timestamps; do not substitute file modification time for move date.
      Explain unknown dates on older receipts. Distinguish missing, changed,
      expired and conflicting items, offer Refresh after conflict resolution,
      and remove expired metadata without deleting unrelated files.
- [ ] Add management of saved exemptions for missing or changed files, and
      show a preview of what each saved retention preset makes eligible. Explain the minimum age.
      Preserve required recovery snapshots even under the shortest setting.
      Changing preferences or exemptions must only change the candidate set;
      movement still requires review and confirmation. Keep Studio retention
      separate from Finder Trash retention.
- [ ] Finish focus restoration and keyboard sorting/filtering/review scrolling.
      Exercise pointer-only, keyboard-only and VoiceOver flows through entry,
      selection, review, cancellation, progress, result and Restore. Verify
      roles, names, values, protection reasons, totals and announcements using
      large inventories, long paths, stale receipts, unavailable Trash, partial
      errors and interrupted writes. Record screen/tree evidence and source-take
      hashes from generated fixtures under `build/`.

**Storage cleanup exit:** an animator can identify what Studio owns, select
only eligible generated files, understand the consequences before acting,
restore a moved item without overwriting work, and explain every protected or
failed item. Source-take hashes remain unchanged in all fixtures.

**Exit:** keyboard-only and pointer-only import/save/restore/export paths;
all dirty-close and failure branches exercised; no clipped controls at the
agreed minimum window size. Sources unchanged.
