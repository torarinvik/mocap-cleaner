# Edit transaction source record

Source inspected at primary `b8803f0`. This records implementation structure;
it does not establish successful current application compilation, proof truth
or native behavior. The [remaining qualification](../plan/m5-responsiveness.md)
must complete before acceptance.

## Source structure

- `app_edit_transactions.elisa` owns pending stacks, typed Record/Undo/Redo
  intents, base tickets, candidate evaluation and publication. Helpers remain
  private within Studio. `app_corrections.elisa` retains correction controls.
- Synchronous edits evaluate before history recording; synchronous Undo/Redo
  evaluate a read-only target before moving the cursor. Base tickets are checked
  again before publication. Evaluation temporarily owns and restores Memo.
- Worker-active edits compose into a retained draft. Drain validates the base,
  evaluates and publishes the accepted intent. Undo first cancels an existing
  draft; an unchanged draft creates no history entry.
- Publication installs clip, built stack, rig/result revision, readouts, timeline
  and findings. Stack/result increments use admitted generation boundaries.
- Pending drafts block session saving and export; dirty/replacement flows account
  for them. Session candidates remain retained on refusal. Close approval also
  compares the captured pending draft, so changed draft state requires review.
- Callers consume commit refusal and use admitted completion feedback. Waiting
  and failure feedback are retained while the result is not ready.

## Evidence and limits

The immutable `build/studio-qualification-9a952f8/` graph has 552 hashed inputs,
with byte-identical before/after input inventories. Its full O0 compile failed
with five frontend diagnostics and produced no object. The post-run snapshot
check passed with its recorded native-tool PATH. Later initializer and callback
repairs and the transaction integration require a new complete snapshot/run.

Selected policy/history O0 graphs compiled with the source-matched d2754a8e
compiler before the subsequent repair batch made that product stale. Those
objects establish source compatibility only. Later pending-draft identity and
ownership transfers remain uncompiled with a rebuilt current product.

The retained proof CLI build failed with 33 borrowed-return diagnostics and
15 concurrency refusals. Five proof-owned return ties are repaired in source;
compiler/std repairs and paired rebuilt tools remain pending. No authenticated
transaction replay, executable transaction tests or native interaction result
is recorded here. Neither M5 nor any release gate is closed.
