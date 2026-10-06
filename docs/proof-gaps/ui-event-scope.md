# Compiler event scope collision

Current compiler `4c409da6` compiles an object containing only an include of
`../elisa-ui/src/core/ui_core.elisa`. Adding an include of
`src/studio/suggestion_policy.elisa` produces two errors in unchanged UI code:
`wire_kind` may fall through, and `from_record` match arms have incompatible
`PointerEvent` and `KeyEvent` types (UI event conversion line 226).

Reproduction sources and logs are derived artifacts under `build/repro/`:
`ui-events-only.elisa`, `ui-events-and-policy.elisa`, and their `.log` files.
Both were object compilations; no executable test was added or run.

The policy introduces a separate scoped `const enum Event`. A compiler scope
resolution collision is suspected; the exact resolver defect remains to be
identified. Fix the scope handling rather than accepting a renamed type as
qualification. Integrated Studio remains unqualified until the current compiler
accepts both modules and the complete app builds.

The candidate fix is committed in the compiler as `dedd2dbe`, with loop-state
threading follow-up `3e716ca8`. Enum value walls now resolve declarations in
the current lexical module before considering globally unique names. Hierarchy
coverage now filters same-named variant rows using the existing module resolver,
as flat-enum coverage already does. Product verification is pending: the seed
request was refused because another live host seed (PID 53052) owns the shared
memory-protection lock. No stale compiler override was enabled.

Compiler follow-up `e4acb8de` also constrains value-wall variant lookup to the
selected lexical declaration. Resolving a local enum as firm must not allow a
foreign same-named enum to contribute variant names. This guard also handles
an empty local enum shadowing a populated foreign enum. Fresh compiler product
verification is still pending the live host seed; the patch is not accepted
as qualification until the reproduction and integrated build succeed.
