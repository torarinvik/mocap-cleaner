# FBX feedback and implicit-void source correspondence

Status: source-checker changes are committed in the proof checkout but are not
qualified by a fresh producer/replay pair. The latest pair attempt was refused
by the compiler freshness guard; no stale override was used.

## Captured baseline

The retained comparison pair is proof HEAD `797c8e1a4804c9efbcaf650f76b2e2e576416f89`,
compiler source `c83ea67518bbc6ff9866fe25cff4cf93411fe73b`, Stage1 product
`e9abce9d0eaeeb08bd55d59b832b59897ab2de5523c6ea148691a38fa45c475e`, and
runtime `6b5247cec30a39ac1d00e0e61a088ccb4d0901932d518d3f6be32e79b9f5412f`.
Its reports are in
`../elisa-proof-mocap-current-20261007/build/qualification-c83-797c8e1a/law-reports-current/`.
The pair replayed its packages, but the source reports were not authenticated.

For `studio_fbx_import_failure_policy_laws.elisa`, the package replayed 35/35
theorems and the source was admissible, while all 10 functions were unsupported
as `return-type`. Eight law functions have assert-only bodies with no declared
return type; `classify` returns a const enum and `message` returns `sview`.
The sequential checker already records `assert` obligations, but rejected the
first group before walking those bodies. Enum and string-view return semantics
remain unsupported and must stay refused until owner-aware source types and
return expressions are implemented.

For `studio_fbx_failure_feedback_policy_laws.elisa`, the package replayed 32/32
theorems and the source was admissible. Eight functions were checked, two were
unmatched and six were unsupported. `show_failure` had one unmatched
`return-ensure`; dependent laws correctly refused it as `callee-unchecked`.
The body expands the checked `may_replace_feedback` result inside a Boolean
conjunction. The proof checker now canonicalizes only conjunction association,
preserving operand order, so an expanded helper result can match the same
source proposition shape. This repair is still unqualified; a changed-helper
and wrong-owner control must continue to refuse.

## Repairs awaiting qualification

Proof commits `f5854683` and `07af1987` respectively canonicalize ordered
Boolean conjunctions after checked helper expansion and admit assert-only
implicit-void functions in the sequential subset. Value-returning implicit
functions, loops and matches remain refused by the void inference scan, and a
value return in an active void function is rejected. Focused positive and
refusal harnesses were added in the proof checkout.

The first fresh build attempt for these commits exited 2 before compilation.
The Stage1 wrapper found
`/tmp/Elisa-compiler-callback-arena-repair/src/backend/codegen_const_globals.elisa`
newer than product `6909950f6974dc33440bff20986a3114b2768b8fc13fb1b5eabfa7b0503bfca4`.
The refusal is retained at
`../elisa-proof-mocap-current-20261007/build/qualification-03ae-07af1987/build.log`.
The compiler owner is producing a new source-matched tuple. The new proof
changes and all current FBX policy bytes must be captured together before
reporting checked obligations or source authentication.

## Remaining limits

The import-failure `classify` const-enum result and `message` string-view result
are still unsupported. The boolean normalization and implicit-void support do
not establish enum numeric values, string-view semantics, helper purity, or
native correspondence. Qualification must report package authentication,
independent replay, source admissibility, and checked function coverage
separately.
