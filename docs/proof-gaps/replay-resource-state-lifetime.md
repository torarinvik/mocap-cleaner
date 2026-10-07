# Replay resource-state lifetime validation

Status: Stage0 refusal retained; current Stage1 concrete report control passes.
Matched producer/replay and escaping-negative qualification remain open.

## Evidence and scope

The full resource replay module closure, exact reporter bodies and concrete
`proof_kernel_replay_resource_report_with_workspace` entry reproduce two
lifetime refusals at `reporters.elisa:141` and `:185` with clean Stage0 source
`6f0988a2`, binary `7b190f5a`, using `-emit obj -O0`.
The diagnostics say that a call may store inferred local state into a
longer-lived region through argument 1. No executable was produced.

Retained record in `../elisa-proof-mocap-current-20261007/`:
`build/q02-reporter-lifetime-reducer-20261007/concrete-resource-report-obj.*`.
Status is exit 1; stderr SHA-256 is
`12c7b7c575a2ab467c4ffbd155cf74702bef2fb807b30df43400b277c96f4b2a`.
This is source-harness evidence, not a qualified producer/replay pair.

The earlier `-emit lowered` probes passed but did not exercise the failing
validation stage. Object-emission controls distinguish the patterns:
an independent local-copy probe passes; a probe tying a stack-local state to
the node arena refuses; a recursive multi-field probe refuses a direct push
of a node-backed name into state. Those controls do not establish that the
full reporter refusal is a compiler defect.

## Dataflow and required repair

Resource header decoding returns names borrowed from `nodes[].name`. Reporters
extend those names into `ProofKernelReplayResourceState.formal_names` before
calling event walkers. Event transitions also store node-backed names in
`active_regions`, `external_regions`, `binding_names` and `binding_region`.
The lifetime of the state container and the lifetime of its borrowed elements
must both be represented correctly.

- Reduce the concrete object-emission failure while retaining the actual
  resource helper bodies, state fields and caller relationships.
- Establish whether the refusal reflects a real escape, a missing supported
  lifetime representation or an overly conservative compiler check.
- Preserve borrowed-name tracking. Do not use `trusted`, remove safety helpers,
  or allocate the entire state in the node arena solely to silence diagnostics.
- If stable node indices replace names, validate every index against the same
  node snapshot and preserve transition and replay behavior.
- Run positive and escaping negative controls through object emission, then
  rebuild the current producer/replay pair with exact source provenance.

Changing only state region annotations or placing temporary formal names in
the node arena did not remove the two full-source refusals in scratch probes.
No such workaround has been accepted into source.

## Bounded Stage1 path controls

The reporter-extended path-control harness at source SHA-256
`ec2d127c440ff4bf26c73af3b8012217ad47dca593eaf3e7d1365d4ad45e167e`
compiles and runs with exit 0 on frozen diagnostic compiler `b35b5bc3`.
Compiler provenance validation exits 0; the observed compilation process-group
RSS peak is 187,648 KiB under a 2 GiB watchdog, with no watchdog termination.
The harness exercises field identity, index matching and node-budget refusal.
It includes the actual reporters, but its main calls only path controls;
it does not execute the concrete report entry from the original reproduction.
The original reporter gap therefore remains open pending that matching check
and current producer/replay qualification.

Retained record in the dedicated proof checkout:
`build/q02-reporter-lifetime-reducer-20261007/resource-place-controls-ec2d-b35b5bc3.json`.
Record SHA-256:
`7ea49be39f309065c5c4a9010b4c16f7e8e1999763cd373d0c66db4417b8584b`.
Log SHA-256:
`f4a7b24df270c2033fb9a1b004e8f3dcde135befc3146f5002c1326793441619`.
This compiler product is diagnostic while its separate malformed-metadata
repair is pending; these controls do not qualify that repair or promotion.

## Concrete current Stage1 report control

A strengthened harness at source SHA-256
`0bab770f089ea819c78656f883b8e619bd760131d9dae00b85b11ac97f95a009`
executes `resource_report_with_workspace` on a caller summary containing a
real resource call to a callee with a formal resource-bind event. This invokes
both top-level event replay and nested callee event replay, covering the calls
at reporter lines 185 and 141. The control requires successful report replay;
compilation, execution and product provenance checks all exit 0. Compilation
peaks at 267,408 KiB under a 2 GiB watchdog, with no watchdog termination.

Compiler production source is `60f5a3b2`, product SHA-256
`04487c330fbbac27ce93660e15e6775686e32a9e1bfc29dd335788e1b750674d`.
The clean working HEAD `edb319ed` includes subsequent test-only commits;
the record distinguishes that HEAD/tree from the product's source revision.
Record in the dedicated proof checkout:
`build/q02-reporter-lifetime-reducer-20261007/resource-report-entry-controls-0bab770f-edb319ed.json`.
Record SHA-256:
`55f4e58309701e1ae1e6695f4399a84788b981b83ebd6f4d637a206247528dfe`.
Log SHA-256:
`92819e0277ab5c8e1c78bbd8bc13ab18664d87c9da4cc9b2dd1e8d4cfd8b5bea`.

This resolves the focused current Stage1 reproduction, not full source
authentication or proof-pair qualification. Retain the original Stage0
refusal and qualify an actually escaping borrowed-name negative control.
