# Build generation policy proof and replay (2026-10-07)

Status: the producer/replay products passed integrity and dependency freshness
checks. The policy law graph is incomplete and source correspondence is not
established. Replaying its 33 emitted theorems does not qualify the source
snapshot. This is focused evidence, not a full-corpus or application
qualification.

## Previous tool pair (comparison)

The proof repository pin was advanced in `b7f10b234f63cd19407ba3d5ce8ccdf608ace098`
to compiler commit `9667344cf0fd2e955a4e233ada1ea60033a16837`. The first all-products build completed with exit 0 and published generation
`ef1317585270400a8aa51deeb92ed517`. After the enum-fact reduction described
below, a source-matched rebuild completed with exit 0 and published current
generation `3bea4b09bd81443caa046b1c4c76941f`. The current pair checker and
`scripts/check_prover_freshness.py` both exited 0.

Current producer binary SHA-256 is
`57612fff99d5fd8a50839da92a95a102305347f657a7c19d18ce01830b7240c0`; its
manifest SHA-256 is
`3dfd99c03e0d56e6974f88b665b7b154b80016882a9eeabfb8ca7ccbab4d5d2d`.
The independent replay binary SHA-256 is
`caa9533988aab8337b8c8893dd257c4fe1bbd01de9fb67a358359f8f571df169`; its
current manifest SHA-256 is
`6540a7cfae6093bd25a715395b54a109f8011a062a67bdd0b195f43009033e92`.
Both current manifests record strict O2 builds from proof HEAD
`f4619daea5fa1909c5c790a47da8fa26ed3f730b`, compiler product SHA-256
`bed23103851823084b365d825570394243564f99e1c6e1c4dd896d633194797b`, runtime
SHA-256 `51365ba4a06e13e0af344b5e21790795e15f1b7fbba23c0b5b94b5a52b00ccee`,
and compiler source tree SHA-256
`0c654d0bb8e9c564fa3cdfa33116e96b0a442da0881a56037a75b47bf1897dcb`.

## Focused law result

The inspected source pair was:

- `src/studio/build_generation_policy.elisa`, SHA-256
  `7e4fbcccb30fbfe28264387de9fa70b074d3e5e5679c2864ee7398c154e5ccb7`.
- `proof/studio_build_generation_policy_laws.elisa`, SHA-256
  `2032823d9708a5f44ff488d476b1ec8164cf75dfebd712c490cb875b09235f2e`.

The producer's `--json` report exited 1 with status `failed` and verification
state `unsupported`: 89 obligations, 33 proven, 56 unproven, 45 findings, and
no semantic errors. The original report measured 1875 facts in
`protection_reason` and 421 in `eligible` (limit 128). Commit
`f4619daea5fa1909c5c790a47da8fa26ed3f730b` avoids root-relative enum exclusions
when the root is an exact source-resolved constructor. The current report
measures 297 and 286 facts, still above the same limit. Fact provenance shows
240 directed `Protection` constructor comparisons per function (16 variants
times 15 other variants), 18 comparisons from other enum domains, and 39/28
type-bound facts. The remaining excess is dominated by eager pairwise enum
constructor facts; branch facts are not the main contributor. Calls from
`may_cleanup` to `eligible` are unsupported and leave its executable summary
unverified; dependent ensures remain unknown. Other law ensures are unknown
under connective, non-comparison, or ambiguous-constant refusal gates.

The package contained 33 theorems. The standalone replay returned exit 0 with
status `replayed`: 33/33 replayed, zero rejected. Its trust record correctly
states `source_authenticated: false`; package replay does not establish that
the theorem statements are obligations of the source.

The producer's independent `--correspondence` check returned exit 1. It found
an exact source identity and `source_admissible: true`, but reported
`source_authenticated: false`, 0 checked obligations, 0 unmatched obligations,
and 22 unsupported functions. Initial refusals are `parameter-type` for
`facts_valid` and `eligible`, and `return-type` for `protection_reason`, which
use struct and enum types. No source authentication claim follows from this
run.

## Enum-demand repair pair (comparison only)

Proof commit `10916b8cd1586756fe2396136f59fb11a1c1c8e9` replaced eager
pairwise enum facts with source-validated constructor comparisons requested by
source expressions and expanded goal expressions. The paired build completed
with exit 0 as generation `0729897f0fdc46ab8c0172974f1e42d3`; pair resolution,
pair `check-current`, and `scripts/check_prover_freshness.py` each exited 0
against the captured compiler product. Both manifests record proof HEAD
`10916b8cd1586756fe2396136f59fb11a1c1c8e9`, clean proof source tree
`4d446c5418858afeac105a4406aac5d6d2cabf7472048039517b593342cdcd96`,
compiler product SHA-256
`bed23103851823084b365d825570394243564f99e1c6e1c4dd896d633194797b`, compiler
source tree SHA-256
`0c654d0bb8e9c564fa3cdfa33116e96b0a442da0881a56037a75b47bf1897dcb`, and
runtime SHA-256
`51365ba4a06e13e0af344b5e21790795e15f1b7fbba23c0b5b94b5a52b00ccee`.
Producer binary SHA-256 is
`14af900081bd3fb92a3e019cb3cf9d4da1e32e744b4ffcee4a3557151451c6c7` and its
manifest SHA-256 is
`63948ca3da328d652681b7744b04c7278764031942170e80d73fe3f524ee6170`;
replay binary SHA-256 is
`1da727382340c35a55330190ad76949c00cfa27944d1642af578e1455475824a` and its
manifest SHA-256 is
`6b487c984c5e31e622ae050a97b06cbb5ee8519734b9d981381d6e08149a0345`.

The law source hashes remained unchanged:
`src/studio/build_generation_policy.elisa` is
`7e4fbcccb30fbfe28264387de9fa70b074d3e5e5679c2864ee7398c154e5ccb7`, and
`proof/studio_build_generation_policy_laws.elisa` is
`2032823d9708a5f44ff488d476b1ec8164cf75dfebd712c490cb875b09235f2e`.
The producer report still exited 1: 89 obligations, 33 proven, 56 unproven,
56 findings, and no semantic errors. Its 603 boundary facts contain only
type-bound and branch-condition facts for `protection_reason` (39) and
`eligible` (30); it emitted zero requested enum-value comparison facts. Thus
the repair avoids the prior 297/286 fact overflows but does not establish the
missing comparison premises or improve the proof counts. Findings include 25
unsupported and 31 unknown obligations; unknown refusal gates are connective
(18), non-comparison-goal (12), and ambiguous-constant-goal (1).
The report's first `eligible` ensure failure is goal 3 at law line 91:
`not (protection_reason(item) == Protection.None) or facts_valid(item)`. This
shows the remaining connective refusal depends on a verified summary for the
conditional enum-returning `protection_reason` helper (and the bool-returning
`facts_valid` helper). The enum-demand scan alone supplies no such summary; the
report's corresponding helper call is still unverified. Do not treat adding a
constructor disequality fact as a repair for this missing return relation.

The package independently replayed 33/33 theorems with zero rejected. Replay
reports `source_authenticated: false`. Source correspondence remains open:
checked 0, unmatched 0, unsupported 22, coverage `not-established`; unsupported
declarations include struct/enum signatures and dependent local types. This
is a producer/replay result, not a source proof. The retained JSON is in
`build/focused-qualification-10916-enum-demand/` (`report.json`,
`package.json`, `replay.json`, and `correspondence.json`).

This generation is comparison evidence only. After it was built, the compiler
checkout was fetched and found behind the newly fetched `origin/main`. The
compiler owner has since integrated upstream as
`cc6570385d30090d0faa4e64a8f130f446764cec` and is rebuilding the selected
product/runtime. Generation `0729897f0fdc46ab8c0172974f1e42d3` must not qualify
that newer compiler. Re-run producer, replay, and correspondence with a matched
pair from the integrated compiler before any current acceptance claim.

Retained current JSON is in the proof checkout at
`build/focused-qualification-9667344-enumfix/` (`report.json`, `package.json`,
`replay.json`, and `correspondence.json`). The full
`scripts/check.sh` run remains pending the parent task's source freeze.

## Current correspondence repair pair (2026-10-07)

The proof checkout committed bounded source-owned struct projections, symbolic
const-enum terms, immutable integer constant lookup, guarded pure helper
summaries and scoped-call evaluation in proof commit
`828886b67c3c70939e9185a80668649d45163262`. This also fixes an immutable tuple
assignment that had silently left helper return types empty. Scoped helper
calls are refused when their short name is ambiguous. The source-authentication
claim remains false unless every reported source obligation is matched to a
replayed theorem.

The exact producer/replay generation is
`8a85f9729079469a980012854b4f63cd`. Both strict O2 product manifests record
proof HEAD `828886b67c3c70939e9185a80668649d45163262`, proof source tree
`736b0ce4350a9c405ecaa808ef25b7dc71a0fa95c225f06c0e845259f37f7ed9`, compiler
revision `e34f2c0656aac1232ad72da6516c7eb89f866a47`, compiler product SHA-256
`b2e4d197df34892b4f7a43a5ff751aecd6c95c08a998783c5687548f50559ae1`, compiler
source tree SHA-256
`220301ca3a395c676f8bb655d9f095278e970218a61517e747909bfcfae192fe`, build
recipe SHA-256 `a666bf810cb3950297866e5ee41b53677778c2157c6c77929dda451532064139`,
Stage1 provenance SHA-256
`2757edaf410fb718c9b7148f7d0d8a009624d9397fff1cc7688337025db2c62a`, and
runtime SHA-256
`51365ba4a06e13e0af344b5e21790795e15f1b7fbba23c0b5b94b5a52b00ccee`. The
producer SHA-256 is
`b491033be1f3063cc3fb0c3e4552a969de5dbd2a30c69bf776f27a244d2259eb`, with
manifest SHA-256
`942b681acd9c195c7db65dd9d2d0f575dca6f43de015d497c8f289264dda53fa`. The
independent replay SHA-256 is
`53681640da2fc604f383dca1a44c95b6dc3412f0c0ef456f7cc0d4d21c2e6662`, with
manifest SHA-256
`f0744db5478ffd25fae10bde9e0df7f9e399bcdf5fd96ba78d4745d59834c30e`. Pair
integrity and current source/compiler/runtime freshness both pass.

For the generation policy, the captured source hashes are unchanged:
`src/studio/build_generation_policy.elisa` is
`7e4fbcccb30fbfe28264387de9fa70b074d3e5e5679c2864ee7398c154e5ccb7`, and
`proof/studio_build_generation_policy_laws.elisa` is
`2032823d9708a5f44ff488d476b1ec8164cf75dfebd712c490cb875b09235f2e`. The
report has 89 obligations, 33 proven and 56 unproven, with no semantic errors.
The package replays 33/33 theorems. Exact-source correspondence checks two
zero-obligation helpers (`facts_valid`, `protection_reason`), leaves one
function unmatched on its 13 return ensures (`eligible`), and reports 19
unsupported functions. Coverage is partial and `source_authenticated` remains
false. The package/replay result therefore does not authenticate the complete
source.

The creation-journal capture also preserves exact source hashes:
`src/studio/build_generation_creation_journal_policy.elisa` is
`f3115ea879f977f9743f034aeca94b5e3aeb3b8b2848fb9440d69aba24c42722`,
`src/studio/build_generation_creation_policy.elisa` is
`42b50c648d0d3982554b6134c00e92c87167a06396305a8c15a75742feebfdc5`, the
shared generation policy is
`7e4fbcccb30fbfe28264387de9fa70b074d3e5e5679c2864ee7398c154e5ccb7`, and
`proof/studio_build_generation_creation_journal_policy_laws.elisa` is
`48e9a172db9b891bafa819475c90fb56e8ff086f8a4539c10aadfc5342173fc7`. Its
report has 195 obligations, 53 proven and 142 unproven. Package creation and
correspondence reject the source as `source-inadmissible`; no source function
is authenticated. Captures are retained under
`elisa-proof-mocap/build/focused-qualification-pair-8a85f972-generation-policy/`
and `...-creation-journal/`.

The authorized full `scripts/check.sh` run is pending. The proof-authentication
work remains incomplete even if that repository-wide regression check passes.

## Owner-aware lookup qualification (2026-10-07)

A fresh matched producer/replay generation was built in the isolated proof
worktree after adding lexical source type lookup and aligning the proof recipe
with Stage1's `scripts/platform.sh` input. Generation
`9a1ba34caa3b4040a967433478e8d91b` passed pair integrity and current-source
checks. Both product manifests pin proof HEAD
`67d6ac746b472c0a58fe180f439e579f91c3199e`, proof source tree SHA-256
`5d39f4dfa4cacad4dd4ebe47bf0f39957a40120c414c3e1099e40011e0c357dc`, compiler
revision `dd0312ee4ae2aef7506d3155d2c17cf0a0771cdf`, compiler product SHA-256
`4bc25a80830bafd04066607a00a1623b3d6e446b7cb02cd449ad4938ccb164a7`, compiler
source tree SHA-256
`c4daec9675a5a4a00bb1e9a331b6c6b8dc901a8ff3ac77cb6295730d7abc3bfb`, recipe
SHA-256 `105bd840e8e6ce839d87eb77f5155a4600e33b44d102db614d9402e15d433073`, and
runtime SHA-256
`51365ba4a06e13e0af344b5a21790795e15f1b7fbba23c0b5b94b5a52b00ccee`. Producer
SHA-256 is
`7b0880590418ec208d4ce2bcdb30fbb8376dadf4af553aadd1f295c4c7d1c975` and replay
SHA-256 is
`b5833031e3cd4f3c70b6feb5cf7a5319c644bfe1fd824deb9af85b4d9df30079`.

For the generation policy, the law graph remains 89 obligations (33 proven,
56 unproven; zero semantic errors). The package replays 33/33 theorems. Source
correspondence checks two zero-obligation helpers, leaves `eligible` unmatched
on 13 return ensures, and reports 19 unsupported functions. Coverage is
partial and `source_authenticated` is false. The package and replay therefore
do not authenticate the full source.

The creation-journal laws graph in this pair reports 186 obligations (56
proven, 130 unproven). Package construction rejects the source as
`source-inadmissible`; correspondence checks no functions and authentication is
false. The report files are retained under
`elisa-proof-mocap-owner-aware/build/focused-qualification-pair-9a1ba34c-generation-policy/`.

Three exact contract-proposition formation failures remain in this capture:

- `StudioBuildGenerationPolicy::may_cleanup`, source line 94, calls
  `eligible(item)` in an ensure, and line 98 calls it in a body guard.
- `StudioBuildGenerationCreationPolicy::may_prepare_move`, source line 78, calls
  `eligible(facts)` in an ensure.

All three fail as `contract-proposition-type` with the typed kernel's
`term-sort-or-operator-rejected` fallback. The declaration projection stores
function signatures by bare name, while these modules both declare an
`eligible` and the source-neutral call representation supplies only the leaf
name to function lookup. The next repair must carry exact lexical owner
resolution through function signatures and call formation. It must retain
qualified exact-path matching, reject ambiguous same-scope matches, and keep
unsupported or indirect calls refused. Adding an uninterpreted helper result
or a summary axiom would not authenticate these source contracts.

The proof-side source lookup repair and recipe pin are committed as
`ac9df91b` and `67d6ac74` in the isolated proof worktree. The producer/replay
capture does not qualify the full application or authenticate source
correspondence.

The follow-up source repair is committed as `2cd4e96b`. It projects each
function signature with its module owner and builds a per-proposition function
environment using the nearest exact owner-path prefix, respecting lexical
shadowing and refusing duplicate declarations at that owner. Repeated-leaf
qualified calls are also refused while the kernel arena erases their owner.
This source change has not yet compiled: the pinned compiler wrapper currently
rejects its own selected product as stale against a restored source-file
freshness check. No pair or proof result is claimed for `2cd4e96b`.

## Owner-aware call formation qualification (2026-10-07)

The isolated proof worktree `elisa-proof-mocap-owner-aware` now contains the
owner-aware function lookup repair and builds a fresh matched producer/replay
pair. Generation `d321c0515e654899a3769707457298ca` passed `verify_product_pair.py
resolve` and `check-current`. Both manifests pin proof HEAD
`9432ac91184298227ece607c7f5e2fdb621032e0`, with source tree SHA-256
`846a3bf794327f488f3085a0be55b0348574b851ac759385d444c33fe373f4d8`. The
producer SHA-256 is
`749ccd82dedd0eacb8b299b00759d213bfec1e2886688c3d6850c8e6eef9c6be`; replay is
`fb59c8c3e6b26c8b461acea2e98fc5f849910a025cd6697c4381b94a29cc72b2`.

The compiler manifests pin commit
`ac0f4423189e7f554388a903888347400d74acee`, Stage1 SHA-256
`e5ca2db0d650bd6bc28550f396dff9d390da6f7d6097f29e4c3cb6ef9a9e00fe`, compiler
source tree SHA-256
`1b34af95cfb8dc232f19df3db79377af92f071209650537b7eef85405f8e2f56`, recipe
SHA-256 `105bd840e8e6ce839d87eb77f5155a4600e33b44d102db614d9402e15d433073`, and
runtime SHA-256
`51365ba4a06e13e0af344b5a21790795e15f1b7fbba23c0b5b94b5a52b00ccee`. Stage1
provenance validation passed.

The focused capture is retained at
`elisa-proof-mocap-owner-aware/build/focused-qualification-pair-d321c0515e654899a3769707457298ca-generation-policy/`.
Its exact primary source hashes are:

- `src/studio/build_generation_policy.elisa`:
  `7e4fbcccb30fbfe28264387de9fa70b074d3e5e5679c2864ee7398c154e5ccb7`
- `src/studio/build_generation_creation_policy.elisa`:
  `42b50c648d0d3982554b6134c00e92c87167a06396305a8c15a75742feebfdc5`
- `src/studio/build_generation_creation_journal_policy.elisa`:
  `f3115ea879f977f9743f034aeca94b5e3aeb3b8b2848fb9440d69aba24c42722`
- `proof/studio_build_generation_policy_laws.elisa`:
  `2032823d9708a5f44ff488d476b1ec8164cf75dfebd712c490cb875b09235f2e`
- `proof/studio_build_generation_creation_journal_policy_laws.elisa`:
  `48e9a172db9b891bafa819475c90fb56e8ff086f8a4539c10aadfc5342173fc7`

The generation-policy law graph still has 89 obligations (33 proven, 56
unproven, zero semantic errors). The source package replays 15/15 theorems.
Correspondence checks `facts_valid` and `protection_reason`, leaves `eligible`
unmatched on 13 unproved return ensures, and marks `may_cleanup` unsupported
because its helper is unchecked. The creation-journal law graph has 204
obligations (67 proven, 137 unproven, zero semantic errors). Its source package
replays 32/32 theorems; correspondence checks no functions, with 4 unmatched
and 8 unsupported. Both reports keep `source_authenticated: false`.

The three earlier `contract-proposition-type` formation failures no longer
appear in the focused law reports. This confirms the typed source lookup repair
for the captured inputs; it does not close the helper-summary, parameter-type,
or unproved-obligation gaps. The pair therefore does not authenticate either
policy source, and Q02 remains open.
