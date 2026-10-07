# Lexical owner identity in proposition typing

Status: owner repair retained in `d98afac0`; current six-package admission fails.
Nested const-enum cast repair is under review and remains unqualified.

## Reproduction and consequence

Proof source `56460af7`, compiler `2ef1fa26`, paired generation
`27a76cce72424a72ba1a75bb0e8c2f96` rejects five of the six current FBX
policy packages as source-inadmissible. Pair integrity and compiler freshness
pass. This is a proof admission gap, not evidence that the native producer
performed the required file operations.

Nested constant bindings retain only the leaf module name in
`proof/check/kernel_proposition_environment.elisa`; replay scope qualification
also reduces nested scope to that leaf. Thus
`StudioFbxImportPolicy::Limit::PATH_BYTES` (i64) and
`StudioTakeSourceRefPolicy::Limit::PATH_BYTES` (usize) collide as `Limit`.
The combined native policy report rejects typed propositions in
`request_buffers_fit`, `staging_output_valid` and source-reference `path_valid`.

Function signatures have a second identity loss: the kernel records an empty
owner and result-sort lookup rejects a second same-name signature. Duplicate
module-local `valid(x)` declarations reproduce a proposition-type refusal;
the single-declaration control forms. Selecting the first leaf-name match
would conceal ambiguity and is not an acceptable repair.

## Required repair and acceptance

- Preserve the full resolved lexical owner for nested constants and function
  signatures, including nested modules; use the resolved source callee rather
  than a global leaf-name search.
- Compare exact ordered path segments. A path hash may accelerate lookup but
  cannot establish declaration identity; detect and refuse distinct paths with
  the same hash, including sentinel remapping collisions. Apply this to lexical
  context lookup as well as qualified terms.
- Encode that identity in package terms and require independent replay to
  resolve the same declaration. Producer-only acceptance is insufficient.
- Cover equal leaf names with different scalar sorts, qualified references,
  lexical unqualified calls, shadowing and genuinely ambiguous resolution.
  Wrong-owner and wrong-sort terms must remain refused.
- Rebuild the source-matched producer/replay pair, retain frozen source closure
  and hashes, and rerun all six policy packages and correspondence checks.
  Report declaration verification, theorem replay and authenticated source
  coverage separately. Zero checked functions never establishes coverage.
- Keep the failure-policy const-enum expression refusals and four ensure
  budget timeouts as separate issues; this owner repair does not imply that
  those obligations or the entire FBX journey are qualified.

## Retained evidence

Proof checkout directory:
`build/q02-current-fbx-pair-27a76cce72424a72ba1a75bb0e8c2f96/`.
Run record SHA-256:
`1680e6bb29ef658e9bab7f9ce1a848c3119e03ea5d84faf69d6dbd481355c9f8`.
Root independently verified all 24 report/package/replay/correspondence hashes.
All six correspondence commands exit 1, check zero functions and report
coverage not-established. Failure policy alone independently replays 26/26
existing theorems; it still lacks authenticated source coverage.

## Committed repair awaiting qualification

Proof commit `d83d6f69` records full ordered module segments with declaration
identities, coalesces identical reopened paths and refuses conflicting identity
records. Producer and replay select function signatures within that exact owner.
Replay validates consistent counts, exactly one row per segment, nonempty names
and bounded indices before qualified or lexical-context lookup. New controls
cover both qualified owners, bare calls, collisions, duplicate/extra/inconsistent
rows and wrong sorts. They have not compiled or run on a fresh compiler yet.
The compiler checkout is being repaired/reseeded; stale products cannot qualify
these changes. Flat unique-only named-type lookup remains a separate conservative
coverage gap for repeated module-local user parameter/result type names.

## Current nested const-enum cast gap

The frozen `fa43d43c` application closure was checked with proof `d98afac0`,
compiler `60f5a3b2` and generation `366396b1c2b84b5e9632fad44be2a282`.
All six packages are source-inadmissible; correspondence checks zero functions.
The failure-policy report has 16 proposition-formation findings on nested
`StudioFbxImportWorker::Status` casts to `i64`, including the negative wire codes.

The pending repair traverses AST call receivers to preserve existing exact-owner
member witnesses. It proposes an `enum-underlying` environment row tied to the
const enum declaration identity and its explicit integer backing type. Replay
must require the same owner and backing width when typing a primitive cast.
Call traversal itself must not assert a numeric result from a method spelling.

Acceptance requires both source controls and adversarial package controls:

- A nested `const enum Status of i64` with `InvalidJob = -100` forms and replays.
- A claim that the same value is `-99` remains unproved.
- Another module's same-name enum cannot provide the receiver's backing type.
- A different integer backing width cannot qualify an `i64` cast by name alone.
- Arbitrary user cast hooks remain outside primitive conversion semantics.
- Duplicate identical or conflicting backing rows are refused.
- A forged backing row on a struct or non-const enum identity is refused.

Retain exact producer/replay product hashes, frozen source closure, per-control
reports and exits, then rerun all six FBX packages. A green minimal cast control
cannot close the remaining call-summary, region/borrow or CFG-budget gaps.
