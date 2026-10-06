# Current Studio export integration build

Normal compiler f292cbe0 built and packaged the current Studio in sessions
82165 and 3957, both terminal exit zero. Command:
`STUDIO_SKIP_CHECKS=1 sh scripts/build_studio.sh`.
Log: `build/current-export-integration-build.log`.

This composition includes bounded report/path preflight, create-only sidecar
publication, compiled build-input identity, POSIX source labels, contact edits,
correction scopes and exact binary32 correction offset formatting. The session
owner's restore repair also compiles in this composition. Earlier backend
declines remain documented as historical observations; they no longer describe
the latest integrated build.

Bundle metadata at inspection identifies project revision `8d0fd6c` with
dirty=true, engine `01f5aec7`, UI `8ab2eb39` and compiler `f292cbe0`; all three
dependency worktrees are clean. Build-input SHA-256:
`3e7039fd00d79569ffe9467d3ff10b54992aabe9402a23b6b803875252e2b668`.
Executable SHA-256:
`6fb16838570d9616b0541220d20390b63a7d091a097156313e7ab83d13562145`.
Runtime object SHA-256:
`b51e6114f0576681e432e1162a3dbdcdac46c140d3b7e7256c0069be0bd11897`.

The shared worktree changed during development. This is compile/package
integration evidence, not acceptance of an immutable source snapshot. Checks
were explicitly skipped; no executable tests were added or run by this command.
Earlier 78 executable/four CLI passes in the compiler candidate diagnostic do
not exercise these newer changes. Native export observation, binary32 runtime
round trips, source-file preservation, failure injection and complete proof
closure remain required. Exact retime-map report serialization is in progress;
durable recovery adapters are not integrated into this Studio yet.
