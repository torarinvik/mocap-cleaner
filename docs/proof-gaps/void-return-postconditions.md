# Void-return postcondition lowering

Status: focused native success/failure enforcement observed; broader return-path,
authenticated proof and integrated qualification remain open.

Compiler repair commits `74bd774` and `f0d8e4e` now emit void postconditions
without a synthetic result binding. The source covers explicit bare returns,
void call returns and implicit fallthrough, before deferred actions and region
cleanup, retaining the error success ABI. Source review found the initially
missing fallthrough path and the follow-up added its guard. These commits have
now compile through the rebuilt, source-matched compiler at
`9667344cf0fd2e955a4e233ada1ea60033a16837`. No runtime observation has
yet qualified their contract behavior.

## Repaired-product compilation

Selected wrapper: `../Elisa-compiler-m5-numeric-call-lowering/scripts/elisac_stage1.sh`.
Both commands used `INPUT -emit obj -o OUTPUT` and exited 0:

- Reduction input `build/physics-residual-qualification/void-ensure.elisa`,
  output `void-ensure.o`, log `void-ensure-966.log` in the same directory.
  Object SHA-256:
  `2f54dce7c10a160be7f77bb545459dc23078b04e564ce823592e23734aab5618`.
- `proof/physics_residual_report_laws.elisa`, output
  `build/physics-residual-qualification/laws.o`, log `compile-966.log`.
  Law source SHA-256:
  `5cdad7019fdb637898aaed58bcf592bf5c0ab9823ca2cb46f682a2e883e964e4`;
  object SHA-256:
  `e361032a6126e5023b64b26508fb0d6774316890d73e49b4cf6305fc1884f81f`.

Compiler product SHA-256:
`bed23103851823084b365d825570394243564f99e1c6e1c4dd896d633194797b`.
Matched runtime SHA-256:
`51365ba4a06e13e0af344b5e21790795e15f1b7fbba23c0b5b94b5a52b00ccee`.
These object results qualify source lowering only, not execution of successful
or failing postconditions. No executable or test suite ran.

## Original failure retained for comparison

The previous compiler at `5b3546508e36c35fcff94ae4b7631874e651e62c`
(product SHA-256 `89d1b2ea78f8fbfe675386d0d2b84767077bb1572e23dece46f30d9749d59ce4`)
refuses `proof/physics_residual_report_laws.elisa` object compilation, exit 2.
It declines bare returns in `balance_frames`, `accumulate_residual` and
`merge_residual`. No partial object is emitted. Retained diagnostic:
`build/physics-residual-qualification/compile.log`.

Explicit `-> void` annotations produced the same refusal and were reverted.
A compile-only reduction isolates the cause:

```elisa
module VoidEnsureReduction:
    public:
        def early(flag: bool) -> void:
            ensure flag == flag
            return if flag
            return
```

Compile with the selected compiler wrapper, `-emit obj -o OUTPUT`:

- `build/physics-residual-qualification/void-ensure.elisa` refuses, exit 2;
  source SHA-256 `0745e953e3a23f9fa270f14dd80660d7311e67d7b19d4be7ffb7747a3e86b159`.
- The otherwise identical procedure without `ensure`, in `void-return.elisa`,
  compiles, exit 0; source SHA-256
  `8fcd5608342549ce72414fb6321af40bea964ed530bf745f125a134ec1b50221`.

No reduction executable or tests ran. The previous compiler's
`src/backend/codegen_stmt_return_vardecl.elisa` explicitly declines bare void
returns when `pending_ensures` is nonempty, instead of dropping an unenforced
contract. This is a useful refusal but prevents the required procedures from
landing in an integrated object.

Repair must evaluate void postconditions without inventing a `result` value,
then retain deferred actions, region unwind and ordinary/error return ABI.
Do not remove contracts or accept partial objects. Qualify explicit early return,
fallthrough, mutation observed by the postcondition, contract failure and error
returns with the repaired source-matched compiler. Recompile the complete
residual law graph and Studio/CLI before claiming integration; authenticated
proof replay remains separate from compiler contract enforcement.

## Current native backend observation

Candidate compiler source `2ef1fa26` preserves these repairs via `3f578e5a`.
The original native gate returns 565/566 because its old void-ensure case
expects refusal; current main returns 566/566 under that expectation. The
revised gate runs the supported successful predicate and a failing predicate,
and completes 567/567 with terminal exit 0. This is an explicit preserved
behavior difference, not identical results under an unchanged baseline.

Root inspected the failure LLVM: it loads parameter n, compares n > 0,
branches to the panic/abort path on false, and returns void on true. The
retained runtime diagnostic is `panic at elisa_stage1:2:14: postcondition failed`,
with a touch backtrace. In `/tmp/Elisa-compiler-void-poll/build/`:

- `abort_contract_ensure_void_false.ll` SHA-256:
  `1c8d452485a5602c2f2237ebf4804d2de87b900bd227ea2e5c2cf28c386b6ad4`.
- `abort_contract_ensure_void_false.run.log` SHA-256:
  `6f1c84bea2f8fcb36b29618890e9b0f915a523b36b6ecb5140e6a7c0737ff2ff`.
- Gate result: `backend-native-2ef1fa26-r3.log`; strengthened IR and runtime
  diagnostic assertions also pass in r4, 567/567, terminal exit 0.

The harness is built by the explicit clean Stage0 and exercises the candidate
backend source. It does not establish direct Stage1 CLI enforcement, all void
return forms, authenticated proof, or Studio integration. Those scopes remain
open; historical source compilation above remains comparison evidence.
