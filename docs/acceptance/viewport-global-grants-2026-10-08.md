# Viewport global access grants

`src/studio/app/app_viewport.elisa` now declares and locally grants global
access for framing, scene rendering, hosted-surface presentation and modal
visibility. Read-only queries propagate `Global.Read`; redraw and presentation
operations propagate both read and write because they update retained viewport
and hosted-surface state. Grants remain visible to callers through signatures.
No `trusted` block was introduced and no pose or rendering algorithm changed.

Full Studio diagnostics with Stage1 e791ce722fb938cda00624fc0e03b35f88edbc218a2cf3976e553d55f4ecd4ad
are retained in `build/studio-build.e791-viewport-grants/`. The semantic and LLVM
invocations both exited 1 because other modules remain unmigrated. Snapshot
checking and the 4 GiB aggregate-descendant guard completed successfully.
Viewport diagnostics fell from 30 to zero; the complete semantic log contains
5660 lines. This demonstrates partial grant migration only. It does not prove
allocation lifetime or resolve the historical mesh/redraw crash.
