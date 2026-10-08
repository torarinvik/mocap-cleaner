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
