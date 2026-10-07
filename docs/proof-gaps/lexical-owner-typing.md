# Lexical owner identity in proposition typing

Status: reproduced; source repair committed as `d83d6f69`, qualification open.

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
