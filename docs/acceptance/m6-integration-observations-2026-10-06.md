# M6 integration observations

These are successive observations from changing source snapshots. Earlier
counts and pending-build notes are historical; they do not qualify current
source. Current remaining work is maintained in the M6 plan.

Current metadata implementation: CLI reports declare `mocap-cleaner-report-v1`,
known comparison metric units, and the spike threshold from the actual preset
used for evaluation. The reader rejects declared schema/unit mismatches and
malformed declarations; unknown/legacy metadata is explicitly unqualified in
console and HTML. Unit metadata is capped at 128 declarations by a contracted
budget. Exact unit conversion, full detector-setting/provenance compatibility,
qualification of the strict unknown-metadata gate, metadata traversal proof replay
and native edge-case qualification remain required. The compatibility policy
has source contracts and schema/unit laws; current Stage1 compilation succeeds.

Metric dimensions now have a typed policy: supported count, frame-count and
distance metric names require matching declared dimensions; equal declarations
with a known wrong dimension are rejected. Unknown metric names remain
unqualified. Current compiler builds the reader and laws. The default prover
reports source 4/4 and laws 9/12, with three laws still unknown; independent
replay and behavior qualification remain open.

Unknown schema, unit or required detector declarations now force an unavailable
exit verdict; numeric rows remain available for inspection. The metadata
admission policy reports 3/3 and its laws 11/11 on the default prover; reader
and updated existing fixtures compile. Independent replay and behavioral
qualification remain required. These checks do not supply missing immutable
provenance or the other detector settings still listed above.

Unit-object and member lookup now use explicit `Missing`, `Invalid` and
`Present(index)` algebraic states rather than negative index sentinels. Reader
and declaration-state laws compile on the current compiler. State-law proof
checking remains incomplete; token traversal bounds and malformed/duplicate declaration
behavior still require full qualification.

Lower-is-better admission now uses supported metric definitions rather than
trusting `_after` suffixes. Unsupported quality names are unavailable, and
quality values must be nonnegative; counts/frame-counts must be whole numbers.
The typed policy reports 14/14, its expanded laws 25/32. Reader and laws compile;
seven law obligations, replay and behavioral qualification remain open.

HTML tables now show expected units and Boolean status words, with metric
direction and exact decimal notation explained. Compilation succeeds. A fresh
pre-presentation-change artifact was generated successfully; local-file browser
opening was blocked by protocol security policy, so rendered layout, keyboard
and screen-reader qualification remain open (see the HTML review evidence).

Studio report fields are now serialized to an owned JSON/text byte snapshot
while the validated GLB staging path and its identity still exist, before the
second confirmation and publication. Later sidecar writes consume those frozen
bytes. Compile-only integration currently stops on unrelated in-progress
suggestion mutability and workspace native-effect diagnostics; these owners
are repairing them. Publication-stage durability, snapshot-bound retry and
semantic/crash qualification remain open.

Export sidecar writes now yield typed GLB-only, GLB-plus-JSON, GLB-plus-text
or complete outcomes; status text identifies which report was not saved.
These are in-memory write outcomes, not crash-durability evidence or motion
quality approval. Policy proof is 14/20 and laws 21/38 on the current default
prover; compile-only Studio build succeeds with Stage1 f292cbe0. Durable journaling,
owned snapshot retention, create-only missing-sidecar retry and result-dialog
keyboard/accessibility integration remain required.

The integrated Studio compile subsequently succeeded after the suggestion and
workspace owners repaired their in-progress diagnostics. This qualifies
compilation of the report freeze/outcome integration; it does not qualify
publication failure recovery, source immutability or native interaction.

The export result dialog and accessibility description now consume the typed
publication outcome directly and identify the missing current sidecar, including
the possibility of stale old reports. The redundant Boolean report-success
flag was removed. Integrated Studio compilation succeeds with f292cbe0; native
visual/keyboard/accessibility and sidecar failure-path qualification remain open.

The native publisher now attempts parent-directory sync after GLB and report
renames, preserving published-with-durability-unknown as a distinct outcome
rather than treating it as rollback. The export result shows this uncertainty
visually and in accessibility text. Integrated Studio compilation succeeds with
f292cbe0. Policy proof is 6/9 and laws 10/20 on default 5776350b; replay and
injected native failure qualification remain open. These trusted native facts
do not prove crash persistence, race-free publication or Storage tracking
durability; durable journals and immutable retry ownership are still required.
