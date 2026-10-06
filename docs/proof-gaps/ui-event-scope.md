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
