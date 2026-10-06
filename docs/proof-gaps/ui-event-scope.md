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

The first current diagnostic seed completed with matching provenance. The
full Studio trace in `build/studio-hierarchy-match-trace.log` still records
24 declined bodies. No UI Event/PointerEvent/KeyEvent variant-path lookup is
logged for that integrated build, whereas the isolated real-UI hierarchy
reproduction enters the lookup and resolves its tags and offsets. This suggests
the integrated failure occurs before payload-enum variant lookup; it does not
establish a wrong variant owner. A second diagnostic trace now records the
match scrutinee's type classification to locate that earlier dispatch failure.
The matching second diagnostic rebuild completed. Its integrated trace in
`build/studio-hierarchy-match-trace-accepted.log` records
`HIERARCHY_SCRUTINEE owner=Studio kind=1 bits=64 arms=9` for
`Studio.event(incoming: UiCore::Event)`. The isolated real-UiCore reproduction
records kind 11 (payload enum) for the same event hierarchy. The integrated
compiler therefore classifies this event match as an i64 before payload-enum
dispatch; investigating type resolution and declaration registration is the
next step. The exact cause remains unproven. The log filename does not indicate
acceptance: this build still declines 24 bodies and explicitly writes no object.

A reduced real-UiCore event match also compiles when the scalar
`StudioSuggestionPolicy::Event` is included before UiCore. The fresh current
diagnostic compile exits 0 and emits the nonempty object
`build/event-include-order.gs9r_9wr/reverse.o` (log alongside it). Together with
the UI-first reduction, this rules out those two declarations' simple include
order as a sufficient reproduction. It does not rule out registration timing
or another collision in the complete graph. No runtime was executed.

## Recheck with refreshed upstream compiler

Fetched compiler `origin` and verified normal Stage1 provenance at `23a0e16a`.
The full Studio compile in `build/studio-upstream-current.zMhkk4/compile.log`
still refuses the same 24 function bodies, exits 2 and writes no object. The
upstream update therefore does not establish resolution of the integrated
failure. Its preceding compile exposed engine tokenizer fields declared
immutable despite mutation; engine commit `ada26e9c` fixes those declarations,
and the tokenizer alone emits a fresh object at
`build/current-glb-tokenizer.ESCx7N/tokenizer.o`.

A separate compiler worktree at `build/compiler-event-resolution-23a0`, branch
`codex/studio-event-resolution-23a0`, contains opt-in parameter/match diagnostics
at `2bba123d`. It records kind, bits, enum identity and both relevant registry
slots to distinguish missing expression types from wrong annotation resolution.
The seed build completed at `abade1bd` with matching diagnostic provenance.
This diagnostic worktree is not the selected normal
compiler and cannot qualify the application as released.

The completed trace in `build/event-current-diagnostic.k0kCxt/studio.log`
narrows the failure further. The isolated real-UI reduction registers
`UiCore::Event` (slot plus one 1), and its parameter and match both have payload
enum kind 11. Full Studio has no registered `UiCore::Event` slot (0); its
parameter and match instead have scalar kind 1, 64 bits and enum identity 2,
matching the registered `StudioSuggestionPolicy::Event` slot plus one 2.
The match already receives the wrong modeled type; this is not merely an
unmodeled-expression fallback during match lowering.

These observations establish incorrect resolution to the suggestion enum in
the complete graph. They do not establish why the UI hierarchy was omitted:
hierarchy classification, failed payload registration and metadata ownership
still need investigation. The diagnostic compile exits 2 with the same 24
refusals and no application object. No native or executable acceptance follows
from this trace. Go to frame UI integration remains pending while this blocker
is investigated.

## Reduced recovery-key collision and candidate repair

The compile-only reduction
`build/repro/hierarchy-with-recovery-key.elisa` adds the recovery dialog policy
to the previously passing real-UI/suggestion event example. With normal current
compiler `23a0e16a`, its log at
`build/event-recovery-key.YUtIK1/compile.log` records ten declined bodies,
including the event match, exits 2 and emits no object. Adding only the engine
viewport instead passes and emits
`build/event-engine-viewport.uzEDXd/repro.o`. Adding the UI gesture Contact
declaration also passes (`build/event-contact-collision.CUUMAI/repro.o`).

The recovery policy introduces a second const enum named `Key`. Inline
hierarchy registration resolves payload annotations without setting the
member's declaring module as `current_owner`. The bare enum lookup refuses
multiple foreign namesakes, so the UiCore KeyEvent payload cannot resolve
lexically in this context. This gives a reproducible registration failure,
beyond the earlier two-Event include-order hypothesis.

Isolated compiler candidate `dcbab5cf` sets the owner while registering each
hierarchy member and restores it on every continuing path. It is not adopted:
the diagnostic seed rebuild is waiting for another live host-wide self-host
build. Qualification must rebuild with matching provenance, compile the
reduction in both include orders and the complete Studio graph, and examine
remaining refusals. This source inspection and failing reduction do not yet
prove that the candidate repairs the full application.

## Separate module-global array index failure (2026-10-07)

The existing full Studio refusal in `append_retained_range` also reproduces
without UI or engine dependencies. The compile-only source
`build/repro/retained-range-cursor.elisa` indexes a module-global `darray[u8]`
while appending to a borrowed output. Normal compiler `23a0e16a` exits 2,
declines that index expression and writes no object; its log is
`build/retained-range-cursor.CqHsEZ/compile.log`. An explicitly typed local
cursor does not resolve it (`build/retained-range-position.iLKkGm/compile.log`).

The dynamic-array address helper only consults lexical slots for an identifier.
Candidate `b49c0d77` adds an owned mutable-global lookup when no lexical binding
exists, checks the global is a dynamic array, and preserves local shadowing.
This candidate remains isolated and unqualified pending fresh positive and
shadowing reductions and full Studio compilation.

The default and `-O1` diagnostic seeds both terminated at the 6 GB memory guard;
neither produced a qualified replacement compiler. A bounded `-O1` seed with
a 10 GB guard is running after observing 24 GB physical RAM and 81% reported
free memory. The earlier validation sessions have disappeared without terminal
full-check evidence; their partial logs cannot establish completion.

The 10 GB diagnostic seed completed with matching provenance at `b49c0d77`.
In `build/event-owner-candidate.XPB4Ma`, the original event reduction and
both recovery-Key include orders all exit 0 and emit nonempty objects. This
qualifies the reduced hierarchy repair only. The global-array reduction still
declines: the index reader's mutable-global branch returns before the general
address fallback. Follow-up candidate `925bcbb2` adds the dynamic-array read
to that branch, using the ordinary bounds and reference-element handling.
Its reseed is queued behind a verified live host build; it remains unqualified.

The follow-up seed completed at `925bcbb2`. All five reductions in
`build/studio-owner-global-candidate.9j1L9G` now exit 0 and emit nonempty
objects: the original hierarchy, both recovery-Key include orders and both
global-array cursor variants. Full Studio compilation next encountered two
new Go to frame syntax errors before reaching backend qualification. Root
commit `c020573` corrects those conditional expressions and a separately
observed accessibility text-buffer reset. A fresh complete Studio diagnostic
compile is running in `build/studio-goto-current-candidate.5bdqyL`.
The normal compiler has not adopted these candidates; reduced objects do not
establish native Studio or current normal-product acceptance.

Additional compile-only owner/shadowing qualification at `925bcbb2` lives in
`build/global-array-shadow-qualification.QIHnh4`. Same-named globals in two
modules with different element widths and a borrowed local array shadow all
compile to a nonempty positive object (exit 0). A scalar parameter shadowing
the array name is rejected (exit 1, no nonempty object), rather than silently
indexing the global. These checks strengthen type/owner evidence; no compiled
program was executed and they do not replace native behavior acceptance.

The complete Studio compile in `build/studio-goto-current-candidate.5bdqyL`
completed successfully: exit 0 and a fresh 1,602,528-byte object. Its trace
classifies the Studio event parameter and match as payload enum kind 11,
with registered `UiCore::Event` slot plus one 1. No declined bodies are
reported. This resolves the reproduced integrated compiler refusal for this
source graph; it does not establish linked or native UI behavior.

After fetching compiler origin again (no missing upstream commits), the
qualified repairs were adopted into the normal compiler as `bbb3feb9`,
`cc7b1e4a` and `5f89731a`. The ownership-preserving readiness API was also
adopted as `709ec863`; its native memory behavior remains unqualified. The
normal product rebuild is running. Fresh normal-product Studio compilation,
native linking and matching prover/replay rebuild remain required. The
ongoing full check selected the preceding `23a0e16a` product and is now
comparison evidence, not acceptance of these newly adopted sources.

The first normal seed failed at the readiness API's atomic completion store:
Stage0 correctly requires a mutable heap reference for that write. Normal
compiler follow-up `bb1f4095` marks the worker's state reference mutable; the
worker still release-publishes completion only after writing the result.
Its replacement seed is running with the same bounded 10 GB guard. No normal
compiler product acceptance is claimed until that seed and provenance checks
complete.
