# Character state global grants

Source: `src/studio/app/app_character_views.elisa`.

Character loading and binding now propagate `Global.Read` and `Global.Write`;
read-only availability and status queries propagate `Global.Read`. Local `can`
blocks authorize the corresponding accesses without dropping unsafe tracking.
No character binding or skinning algorithm changed.

Compiler comparison product: Stage1 SHA
`e791ce722fb938cda00624fc0e03b35f88edbc218a2cf3976e553d55f4ecd4ad`,
from `/tmp/Elisa-compiler-global-local-grants`.

Full Studio semantic and LLVM diagnostics are retained in
`build/studio-build.e791-character-grants/`. Both compiler invocations exited 1;
the snapshot check and aggregate guard completed successfully. The character
module diagnostics fell from 23 to zero relative to
`build/studio-build.e791-globals/`. The remaining closure still produces 5690
log lines. This is partial grant migration evidence, not a successful build or
runtime acceptance. The reported mesh/redraw crash remains unresolved.
