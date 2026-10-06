# M8 and first implementation slices

[Roadmap index](../../IMPLEMENTATION_PLAN.md)

## 13. M8 — Evidence-led advanced cleanup (P2)

These are research candidates, not promised defaults. Promote one only after
an observed corpus failure, a clear user workflow and a measurable benefit.

- [ ] Investigate adaptive filter windows and confidence-aware recommendations
      that preserve impacts and deliberate turns better than fixed presets.
- [ ] Investigate contact-aware pelvis/whole-body adjustments for unreachable
      plants, comparing foot error, knee motion and body-path distortion.
- [ ] Evaluate richer contact geometry, multiple support surfaces and moving
      hand targets with explicit target motion input; do not infer hidden
      environment motion from pose data alone.
- [ ] Evaluate improved head/body pin solving only where current neck reach
      limits block a real repair workflow.
- [ ] Investigate surface penetration checks when validated mesh/collision
      geometry is available, distinct from joint/floor proxies.
- [ ] Evaluate key reduction and additional import/export formats only against
      a named downstream pipeline with round-trip quality fixtures.

For each experiment: record baseline, hypothesis, prototype, contracts,
comparison metrics, visual review, runtime cost and adopt/reject decision.
Do not change default recipes until preservation and failure behavior are
qualified on the expanded corpus.

## 14. Remaining implementation and qualification slices

Use this as priority order, with the shared dependency decisions governing
parallel progress. Existing implementation needs its remaining qualification,
not reimplementation. Each row should become small reviewable commits; a
blocked native or participant gate does not stop independent implementation.

| Slice | Concrete result | Evidence needed before closing |
|---|---|---|
| 1 | M0 studio audit, corrected current-behavior docs and interaction specifications | Running-window captures, gap matrix, measured limits and reviewed first-use flows. |
| 2 | Finish command discovery, focus rules and accessible alternatives | Pointer and keyboard journeys; native tree gives every primary control a clear name, role-appropriate actions, correct value and useful focus; dialogs and status are announced; VoiceOver and keyboard users finish the core tasks; text fields cannot trigger global cleanup; focus survives dialogs and panels. |
| 3 | Missing/changed source locate flow, rig-profile persistence and safe rebind review | Locate succeeds for renamed files; mismatched animation/rig cannot receive stale edits; rebind review shows exactly which stored settings remain valid. |
| 4 | Animation/rig/floor setup with actionable validation | Valid, ambiguous and incompatible rig fixtures; users can resolve warnings without source edits. |
| 5 | Selectable issue list linked to timeline, joint and metrics | Exact frame selection, understandable issue summary and stale-analysis handling. |
| 6 | Suggested-cleanup preview and complete inspector for one existing tool | Apply/cancel/undo parity; local preservation metrics; user can explain the effect before accepting. |
| 7 | Select-first contact editor with interval/anchor controls | One-frame precision, keyboard equivalent, transition quality and visible compromises. |
| 8 | Revision-safe background rebuild and bounded recovery | Rapid edits, undo and take swap reject stale results; cancellation preserves the last valid preview. |
| 9 | Complete existing tool exposure and reviewed export | Session/CLI/preview/export semantic parity; output reopens and matches the reviewed revision. |
| 10 | Corpus expansion, user trials and release qualification | All P0 gates; unresolved limits documented; first-time users finish the core journey without coaching. |

Keep the plan driven by the user's full task: understand the capture, make a
controlled repair, see whether it helped, retain the work, and deliver an
animation that matches what was reviewed.
