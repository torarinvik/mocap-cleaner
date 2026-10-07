# Balance/report availability: current source compilation

Status: formatter and three law graphs compile; proof replay and integrated
application/native acceptance remain open.

Primary snapshot: `ffa3962e4df984daf9801d95a945d6498a761bf6`.
The only unrelated worktree change at observation was `.gitignore`. Imported
primary sources are from this commit; this record covers the small graphs below,
not the complete application or sibling UI/engine graphs.

Compiler: clean `5b3546508e36c35fcff94ae4b7631874e651e62c`, selected
through `scripts/elisac_stage1.sh` in its worktree. Product SHA-256:
`89d1b2ea78f8fbfe675386d0d2b84767077bb1572e23dece46f30d9749d59ce4`.

## Commands and observed results

From the primary root, run the compiler wrapper with each input and output:

```sh
../Elisa-compiler-m5-numeric-call-lowering/scripts/elisac_stage1.sh \
  INPUT -emit obj -o OUTPUT
```

Outputs and logs are under `build/report-availability-qualification/`.

| Input | Output | Log | Exit |
| --- | --- | --- | --- |
| `src/studio/export_report.elisa` | `report.o` | `report-fixed.log` | 0 |
| `proof/studio_export_report_laws.elisa` | `report-laws.o` | `report-laws.log` | 0 |
| `proof/studio_export_policy_laws.elisa` | `export-laws.o` | `export-laws.log` | 0 |
| `proof/studio_balance_status_policy_laws.elisa` | `balance-laws.o` | `balance-laws.log` | 0 |

Before `ffa3962`, the formatter compile refused 22 calls passing `&out` from
helpers whose `out` parameter was already a mutable reference. Diagnostic log
`report.log` retains that failure. Passing the existing references directly
resolved it; no admission or preservation contract was weakened.

## SHA-256

| Input | Source hash | Object hash |
| --- | --- | --- |
| Formatter | `f49c0a4cf0c1cd46255d98225ccc7380bc1778f00c5dc6f68a42b322d17dcc7e` | `113ee10af0f6da7fa3407a359f5250ac6e44d0555f80b3cedadb2c903ee50e47` |
| Report laws | `8d12a7beb954d3a997c6d02420bed602e2a29a7664be63704d8218171b411d70` | `ee47b3f734c29e8b31fe9b1b5f1d931f470c935473ff24caa966bd23ada1c7c3` |
| Export laws | `e24ea53acfdea3e90bef889af02fae07805132d1314f55c52bf00ff0b5f9e6e1` | `e2cbd63036afe59d715d417570f91a9619f58eb01379bc3068400cf1f83e5c47` |
| Balance laws | `aca41c3264334e02c0d76bc9a771430ca77424456ccab368fd8af1632e544cfa` | `359bfa80c3b4352be235e02c018690a6846fe49c6c1ea6ce994052f7e7cfd4de` |

## Remaining evidence

No executable or test suite ran. Object generation does not discharge laws or
establish JSON contents. Authenticate/replay obligations, compile/link complete
Studio and CLI graphs, exercise schema-v3 null/reason output and actual warning
admission, and compare source/result sampling domains on frozen fixtures. Verify
unavailable values cannot appear as measured zero in panels or quality decisions.
