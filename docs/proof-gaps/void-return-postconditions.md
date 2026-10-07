# Void-return postcondition lowering

Status: reproducible compiler backend gap; repair and current qualification open.

Compiler repair commits `74bd774` and `f0d8e4e` now emit void postconditions
without a synthetic result binding. The source covers explicit bare returns,
void call returns and implicit fallthrough, before deferred actions and region
cleanup, retaining the error success ABI. Source review found the initially
missing fallthrough path and the follow-up added its guard. These commits have
not yet been qualified by a rebuilt current product or runtime observations;
the failing product evidence below remains the last observed compilation.

The current compiler at `5b3546508e36c35fcff94ae4b7631874e651e62c`
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

No reduction executable or tests ran. The compiler's
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
