# Create-only GLB publication

New exports now have a native create-only commit API. It atomically links the
validated staging file to the final destination; an existing destination makes
the operation fail without replacing it. This closes the destination-creation
race left by preflight followed by unconditional rename. Explicit replacement
consent selects the existing rename path; identity races during authorized
replacement still require separate native qualification.

The exclusive result separates publication/durability status from staging
unlink success. A linked output remains published when unlink fails. Recovery
publication takes an explicit replacement-consent flag and carries
`staging_removed` alongside native and journal statuses. The integration must
retain the owned staging path and show pending cleanup in that case.

The cleanup classifier and laws independently replay 8/8 obligations using
clean prover candidate `3ac99624`. This Boolean evidence does not qualify native
link, unlink, parent synchronization, path identity, source preservation or
crash behavior. The normal compiler rebuild for `45330579` is still running;
this source integration has not yet compiled with that rebuilt product.
Evidence is `build/export-staging-cleanup-laws.json`. No executable tests were
added or run. Full Studio integration and native fault qualification remain open.
