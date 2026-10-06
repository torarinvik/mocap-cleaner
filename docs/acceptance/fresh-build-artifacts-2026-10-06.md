# Fresh build artifacts

Observed compiler backend declines can return process status zero while
emitting no object. Reusing an earlier object or test executable would make
that failed compile appear successful.

Studio now compiles to a unique private compile directory, requires a nonempty
new object, and moves it into the link input only after admission. Test builds
likewise compile to a new private compile directory, require nonempty executable
output, and update the executable/cache key only after admission. Failure
marks the test build failed and preserves any partial output for diagnostics; the prior
executable cannot satisfy that build attempt.

The existing test cache includes repository shell sources, so this gate change
invalidates earlier executable keys. No additional executable tests were added
or run. Both shell scripts pass syntax parsing. Their next complete authorized
check and Studio build must qualify runtime behavior; artifact presence alone
does not establish compilation semantics or product correctness.

Temporary compiler paths are unique per invocation. Only an empty private
compile directory is removed with `rmdir`; unexpected or partial contents
remain under `build/`. Final shared artifacts and generated inputs still use
the normal build paths, so this change does not qualify concurrent full Studio
builds or provide a complete generated-artifact cleanup workflow.
