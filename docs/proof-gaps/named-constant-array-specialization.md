# Named constant specialization of fixed-array view helpers

## Reproduction

On source-matched installed compiler `b26659e2` (product `94f11e30`), a module
with `const module Limit` and `BYTES: usize = 2` can declare
`bytes: u8[Limit::BYTES] = [195, 169]`. Calling
`UiText::fixed_bytes_view_range[Limit::BYTES](bytes, 0, 2)` passes semantic
checking but native O2 emission declines the call and exits 2 without an object.
Changing only the call argument to `[2]` compiles and runs with exit 0. The
fixed-array declaration still uses the named constant in this passing control.

Sources and terminal logs are retained under
`build/dialog-result-reduction/{named-array-view,literal-array-view}.*`.
The first malformed relative-include attempt was corrected before the controlled
comparison; it is not evidence about specialization behavior.

The same failure blocks existing StudioText's named `Buffer::CAPACITY` helper
and the new retained-status snapshot helper. Three actual UTF-8 helper
obligations using literal lengths 2 and 4 compile/run successfully, but do not
qualify the named-constant path. Preserve constants and the UI borrowed-view API;
using repeated literal sizes would leave the compiler defect unresolved.

## Repair and acceptance

Resolve a constant-value generic argument through its exact lexical/module
owner and declared type before specialization. Preserve the array extent and
borrowed-result lifetime; the result is a view, so scalar/borrowed calls must not
gain unrelated allocation carriers. Reject unknown, ambiguous, mutable,
wrong-type and contradictory constant bindings. Cover nested qualified owners,
same-leaf constants in different modules, direct literals and named values.

Require source-matched seed/provenance, positive native execution, negative
refusal controls and generated ABI agreement. Then run both
`test/studio_status_text_lifetime.elisa` and `test/studio_text_utf8_slot.elisa`
on the integrated compiler containing the prior project repairs. Formal
source/replay qualification and full Studio runtime acceptance remain open.
