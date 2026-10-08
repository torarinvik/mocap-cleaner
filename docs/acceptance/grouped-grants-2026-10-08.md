# Grouped family grants and state migration

Compiler source `090c41214a7e9a8893093d8baf7d5520f95c239a`, Stage1
`fbc0ac467484e53ee2bb6a857a7b42f3a231505ea5ff9bbe8dc79f9a24bf7a6f`, runtime
`6b5247cec30a39ac1d00e0e61a088ccb4d0901932d518d3f6be32e79b9f5412f`.
Official seed, provenance and freshness checks passed. Grouped Global, Memory
and Unsafe positives compile/run; a partial Global grant refuses under `# globals`.
Native partial-Unsafe enforcement remains a separate compiler gap: object emission
accepts it silently while interpretation warns. Broader parity harness failures
are retained, not reported as passes.

Source normalizes repeated family members to brace groups without changing their
member sets or introducing trusted boundaries. Pending keyboard, session-save,
session-locate, accessibility-toolbar, gizmo and correction owner migrations
were included in the full Studio capture in
`build/studio-build.fbc-grouped-migration/`.
Semantic and LLVM each exited 1; the aggregate guard and unchanged-input snapshot
check completed successfully. The semantic log has 2445 lines, none in those six
modules, with no unknown-permission or pointer-cast diagnostics. Other modules
still fail. This is syntax/access migration evidence, not an integrated build,
proof authentication or runtime crash acceptance. Native unsafe enforcement,
current dependency qualification and the reported redraw crash remain open.
