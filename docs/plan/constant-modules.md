# Constants and finite choice migration

Audit each existing/new group for its best domain representation. Use a
`const enum` for a closed set of alternatives, an algebraic data type for
cases with distinct payloads or invalid combinations, and a `const module`
for related numeric limits, units or configuration values. A completed grouping
still requires reassessment when a stronger type fits its meaning.

Preserve visibility, source takes, contracts and proof coverage. Keep every
maintained file within 600 lines and commit each cohesive migration separately.
For serialized/native integer codes, validate explicit encode/decode functions
and preserve required wire values; unknown codes must not become success or
another valid case. Cover all variants, invalid boundary input, round-trip
conversion and public/private API scope in the contracts/proofs. Do not assume
that equal discriminant values alone prove behavior preservation.

## Verification requirements

Qualify each constant group and its source, proof and test consumers with
current compiler/prover provenance. Preserve literal values and visibility;
require independent certificate replay and retain existing proof expectations.
The current prover supports nested and lexical relative constant paths; G96
records the repair and qualification evidence.

## Remaining qualification (2026-10-07)

The inventory now includes file-level declarations as separate owners instead
of silently excluding them. It identifies one remaining group in
`src/studio/state/session_state.elisa`: the session path and temporary capacities.
Move these into a purpose-specific private const module while extracting the
FBX session codec. The Trash adapter capacities have been grouped and compiled
with the current compiler. Representation review and proof qualification remain
required after source migrations.

- [ ] Re-run `scripts/inventory_constant_modules.py --check` after subsequent changes.
      Inspect its coverage before treating zero findings as sufficient: include
      extension owners, proof/test files, file-level declarations, generated
      inputs and visibility boundaries. The inventory cannot decide whether a
      group should be an enum or algebraic data type.
- [ ] Review each public integer API that represents a finite choice. Use typed
      values internally where practical; keep explicit checked conversion at
      wire/native boundaries. Invalid inputs must retain existing refusal or
      no-op behavior. Do not turn unknown codes into a valid default.
- [ ] Verify all enum variants, numeric discriminants, capacity bounds and
      bitmask combinations against prior behavior. Include negative sentinels,
      maximum values, round trips and malformed data. Preservation of literal
      values alone does not establish behavior preservation.
- [ ] Compile all affected source, law and existing fixture graphs with current
      source-matched compiler, standard library and linked dependencies. Capture
      exact inputs before/after compilation and reject drift. Include complete
      application linking and native execution.
- [ ] Discharge current contracts with the matching proof assistant and obtain
      independent replay plus source correspondence. Nested enum declarations
      and qualified calls must bind to their actual lexical owners. Refusal or
      unauthenticated portable replay cannot close this gate.
- [ ] Run the authorized `scripts/check.sh` after compiler/prover qualification,
      preserving existing expectations. Verify persistence, CLI, preview and
      export use the same semantic values and that files still round-trip.
- [ ] Re-check every maintained repository text file is at most 600 lines.
      The latest check covers 781 files; this must remain true after each edit.

Current compile evidence and unresolved toolchain gates are tracked in
[the pending qualification record](../acceptance/pending-policy-qualification-2026-10-06.md).
New source changes must continue to follow these representation rules even
after the current migration is qualified.

The inventory now aggregates declarations from `module` and `extend` files by
qualified owner, so a single declaration in each of two extension files cannot
escape the grouping check. `scripts/check.sh` invokes its failing `--check`
mode before compilation. The corrected current inventory reports zero findings.
File-level declarations and semantic representation still require review.
