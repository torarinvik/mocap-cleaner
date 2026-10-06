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

A smaller derived reproduction, `build/repro/lexical-event-scope.elisa`, declares
`Ui::Event`, its input/pointer/key hierarchy, exhaustive conversion functions,
and an independent `Policy::Event`. Current Stage0 compiles this object with
exit code zero. Stage0 cannot parse the full UI's newer global fixed-array
syntax, so the full UI comparison is not a usable Stage0 reference. The small
example confirms intended language behavior; repaired Stage1 and integrated
Studio compilation remain separate pending gates.

Fresh Stage1 rebuild completed at `e4acb8de` with current provenance. Both
the minimal and full UI reproductions now pass the exhaustive-return check:
the `wire_kind` fall-through diagnostic is gone. Both still report incompatible
`PointerEvent`/`KeyEvent` match arms. The candidate fixes hierarchy coverage,
but the value-wall pass still lacks the needed lexical context. Complete
compiler repair and integrated Studio qualification remain open. Logs are
`build/repro/ui-events-and-policy-repaired.log` and
`build/repro/lexical-event-scope-repaired.log`.

The remaining defect is in the branch-check declaration walker: unlike other
semantic passes, it descended into `Decl.Module` without entering/restoring
`table.current_module`. Compiler commit `88ffc005` adds that lexical context.
A fresh seed is running (session 81586); the fix remains unqualified until the
same minimal and full reproductions compile with the new product.

Fresh `88ffc005` product is current and its checkout is clean. The minimal
lexical-event reproduction now compiles successfully. Full UI plus suggestion
policy passes semantic checking, but backend lowering declines ten UI event
functions and writes no partial artifact. UI alone still compiles. Thus the
semantic scope fix is verified on both reproductions; a separate backend enum
scope defect remains. Logs: `build/repro/ui-events-and-policy-context.log`,
`lexical-event-scope-context.log`, and `ui-events-only-context.log`.
