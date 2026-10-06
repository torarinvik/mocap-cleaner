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

Backend inspection found that `enum_decl_owner_in_file` scans the plain enum
pool before payload metadata. It therefore selects the policy's const `Event`
owner for the UI's payload-bearing hierarchy root. Const enums cannot belong
to sealed hierarchies. Compiler commit `5e3fcc65` excludes those rows from
hierarchy owner lookup. A fresh seed is running; qualification remains open.
The derived payload-bearing minimal reproduction is
`build/repro/lexical-event-payload-scope.elisa`.

Fresh compiler `5e3fcc65` compiles the payload-bearing minimal reproduction.
Full UI plus policy now declines only `StudioSuggestionPolicy.event_valid`;
nine prior UI lowering failures are gone. Its const `Event` was omitted from
plain-enum registration because the foreign UI hierarchy shares its bare name.
Compiler commit `2e1c1e51` restricts hierarchy suppression to non-const enums.
A new seed is running; combined compilation remains required. Logs for the
qualified preceding product end in `-owner.log`.

Fresh compiler `f292cbe0` now compiles the full UI plus suggestion policy
reproduction successfully. Plain enum registration (`2e1c1e51`) retains const
namesakes, and lexical const lookup (`f292cbe0`) respects local payload enums
before a foreign const fallback. The product reports current clean provenance.
Log: `build/repro/ui-policy-cross.log`. This closes the reproduced compiler
collision; integrated Studio compilation and native behavior remain separate
gates. The report diff module also compiles on this product.

## Remaining integrated failure, 2026-10-06

The historical collision above is reproduced and repaired. It must not be
treated as the confirmed cause of the remaining full Studio backend failure.
The integrated build still declines 24 function bodies and emits no Studio
object after the recovery accessibility frame conversion was corrected; see
`docs/acceptance/export-recovery-ui-2026-10-06.md`.

The exact UI Event/InputEvent hierarchy, payloads, module-qualified match arms
and `request_frame_after` compile in isolation, including the actual UI core.
This narrows the investigation to an interaction in the complete include
graph. A remaining declaration-owner or registration collision is a hypothesis,
not an established diagnosis. Temporary backend path/owner tracing is being
built into a diagnostic compiler to distinguish these possibilities. Its
results are not acceptance of a normal compiler product or application binary.
