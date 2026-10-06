# Fresh build artifacts

Observed compiler backend declines can return process status zero while
emitting no object. Reusing an earlier object or test executable would make
that failed compile appear successful.

Studio now compiles to a cleared pending object path, requires a nonempty
new object, and moves it into the link input only after admission. Test builds
likewise compile to a cleared pending executable, require nonempty executable
output, and update the executable/cache key only after admission. Failure
marks the test build failed and removes its pending artifact; the prior
executable cannot satisfy that build attempt.

The existing test cache includes repository shell sources, so this gate change
invalidates earlier executable keys. No additional executable tests were added
or run. Both shell scripts pass syntax parsing. Their next complete authorized
check and Studio build must qualify runtime behavior; artifact presence alone
does not establish compilation semantics or product correctness.
