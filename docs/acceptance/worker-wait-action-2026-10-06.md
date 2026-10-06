# Worker wait action representation

The three wait classifications now form `WorkerWaitPolicy::Action`, retaining
discriminants 0/1/2. The Darwin/POSIX EINTR value remains 4 under `Posix`.
The classifier's return type excludes arbitrary integer actions. Existing laws
compare typed alternatives; the native wait loop only changes its errno path.
No executable tests were added or run for this change.

Clean separate prover `4da37c97` (compiler `45330579`) reports source 9/9
producer obligations. The law text route reports 27 producer obligations with
no unproven producer goals but an unknown verification state. Authoritative
JSON (`build/worker-wait-action-laws.json`) reports 25/27 proven obligations,
37 certificates, 35 independently replayed and two replay gaps, with no
findings or semantic errors. These counts are not complete proof acceptance.
The existing 27-obligation complete baseline remains unchanged.

The unchanged pre-migration source/laws were also checked with this same
candidate (`build/worker-wait-laws-before-action.json`): 26/27 proven, 28/29
certificates replayed and one gap. Both old and new rejected certificates are
in `interrupted_wait_retries`. The typed representation adds one replay gap in
this candidate; it is recorded for prover repair rather than hidden by the
producer's complete count.

Normal compiler `3c72f59f` emits a fresh policy object without diagnostics in
`build/cache-compile.v2R4e2`. Native errno,
waitpid behavior and interruption handling still require runtime qualification
through the authorized check; pure classification does not prove those facts.
