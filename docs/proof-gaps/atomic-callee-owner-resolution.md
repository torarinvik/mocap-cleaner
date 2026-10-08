# Atomic call selected a different module's parameter type

## Observed production blocker

The full Studio semantic check on source-matched compiler `5d17a2c0` reports:

```text
elisacore_runtime_concurrency.elisa:949: argument 1 to "load" expects cstr, got raw reference
```

The source calls the atomic `load` helper with a slot reference and acquire
ordering. Other modules declare `load` functions accepting filenames. The firm
argument checker queries flattened parameter rows by leaf function spelling,
and its module declaration walk does not preserve the current lexical module.
The exact failed check is retained in `build/studio-tooltip-integration/`.
This is a compiler diagnostic, not evidence that the FBX file is malformed.

## Required repair and qualification

- Resolve the actual callee declaration using lexical scope and import bindings;
  retain its declaration identity when selecting positional or named parameters.
- Preserve nested/parent/root module lookup, local callable shadowing, overload
  handling, generic parameters and genuine cstr/raw-reference refusals. An
  unresolved selector that skips this checker is not itself a safety refusal.
- Validate parallel parameter tables and chain bounds before indexing. Do not
  select a different same-spelled declaration when metadata is incomplete.
- Keep the existing indexed parameter-name chains and filter them by declaration
  identity. Scanning all program parameters for every argument reintroduces the
  documented compilation hotspot and requires correction before promotion.
- Run the minimized same-name collision control, matching mismatch positives,
  named argument reorder, local shadow and lexical/import owner controls on an
  exact-source rebuilt product. Then run the full Studio semantic check.
- Preserve the current upstream performance changes and qualify compiler gates
  and runtime performance against that main. A successful parser preflight does
  not prove the semantic repair or removal of the production blocker.

The repair is isolated in `/tmp/Elisa-compiler-atomic-load`. The source-matched
`b8256d31` seed succeeds; native Studio success remains unproved. Its focused
regression rerun reports 12 cases and one failure: the intended negative atomic
collision fixture has an unrelated duplicate `Joinable` declaration. The ancestor
mismatch fixture also emits undefined/non-function diagnostics alongside its
expected mismatch; resolve fixture validity before using it as evidence of
lexical lookup. Retain the failed log rather than relabeling it as passing:
`build/regressions-b8256d31-rerun.log` in the compiler worktree, SHA-256
`83e93b5f5b2ee3324c5ab41881e6f2206e6fb1eb5f4484c0621415a358abe67b`.

Follow-up source inspection identifies an additional real gap:
`parser_decl_module.elisa` constructs the `__using` annotation without its
lexical `module` field. Scoped import resolution therefore misses
`using Provider` inside `Outer::Inner`. Repair the annotation producer and
assert each expected diagnostic's line and message individually; unrelated
ancestor errors must not make a missing imported mismatch appear to pass.
Rebuild the changed compiler before qualification.

The shared `function_parameter_type_at_firm` accessor in
`check_firm_call_resolution.elisa` remains outside the declaration-qualified
FirmArgTypeMismatch path. Its row guard checks owner and next-link counts but
then reads `function_param_type[row]` without checking that vector's count.
Validate all indexed metadata before use and enumerate sibling consumers;
name-only shared lookup must not be described as resolved-owner qualification.
Keep the indexed lookup rather than introducing whole-table argument scans.

The `1beecf48` targeted rerun reports five fixtures and zero failed assertions:
the imported mismatch now appears at L17, the ancestor mismatch at L18, six
owning-return lines are refused, and scalar-owner collision diagnostics are absent.
This is an assertion-level result, not clean fixture qualification: the original
collision fixture still reports duplicate `Joinable`, and the ancestor fixture
still reports undefined/non-function errors. Rename test-only protocol types and
rerun with no unrelated diagnostics for the collision control. Investigate the
ancestor symbol-binding gap separately; an expected mismatch alone cannot prove
the same program is otherwise correctly resolved.

## Full Studio integration after the import-owner repair

The frozen `1beecf48` product checks the complete Studio graph with exit 1.
The previous atomic `load` diagnostic is absent. Six remaining errors at
`session_source_reference_codec.elisa:196–211` report `token_count`/`token_byte`
expecting `Token` but receiving `u32`. The same codec module checks standalone
with exit 0. Calls before the nested loops are unaffected; inspect loop-local,
optional-binding and nominal-owner inference rather than renaming application
symbols to avoid the compiler bug. The exact cause remains unconfirmed.

Input manifests before/after match byte-for-byte. Retained evidence:
`build/studio-build.atomic-compiler-semantic-1be/semantic.log`, SHA-256
`958eec829c6fb96a4780966bcf532f34fe60604f3ee366fc227b017ba758e1cd`.
This removes one integration diagnostic; it does not qualify native Studio or
the FBX redraw fix.
