# quiet-test（fail-cap B）

## Purpose

親 SoT は [issue 42](https://github.com/maplefukku/grok-bot-ops/issues/42) である。適用 issue は [issue 45](https://github.com/maplefukku/grok-bot-ops/issues/45) である。引用は [Cloud開発](sand-workflow:cloud)、tool-path-prefer、GB、[parallel-fire-fleet](sand-workflow:parallel-fire-fleet) である。

## 対象

impl CA と 開発 bots である。

## 範囲

### 対象にする

fail-cap B の既定と呼び出し規則である。

### 対象にしない

[issue 44](https://github.com/maplefukku/grok-bot-ops/issues/44) の CI wrap と NEW-repo pointer の実装は対象外である。[issue 46](https://github.com/maplefukku/grok-bot-ops/issues/46) の PR-body show-me LOCK は対象外である。fail-cap A を既定にすることは対象外である。fail-cap C を Phase0 にすることは対象外である。

## SoT

SoT は box の `/workspace/fleet-scripts/quiet-test.sh` である。このリポジトリの薄い WRAP は [`scripts/quiet-test.sh`](../../scripts/quiet-test.sh) である。本体は vendor しない。

## fail-cap B

| 事実 | 値 |
|---|---|
| SoT | `/workspace/fleet-scripts/quiet-test.sh` |
| fail-cap | `fail-cap B` |
| 既定 fail 行数 | `QUIET_FAIL_LINES` は 500 |
| 既定 ok 行数 | `QUIET_OK_LINES` は 10 |
| log path | `--log` と `QUIET_KEEP_FAIL_LOG` |
| path の出力 | fail は full-log path を必ず印字する |
| quiet と skip | Quiet is not skip |
| lane formatter | `xcbeautify` と vitest reporters は wrapped cmd の内側で先に動く |
| wrap | quiet-test は cmd 全体を wrap する |
| CA | CA と 開発 bots の MUST wrap は `quiet-test.sh -- <cmd>` である |
| CI stdout | quiet stdout は任意である |
| CI gate | exit code と junit または artifacts は MUST である |
| WRAP | 新しい `run-quiet.sh` は置かない。第二の本体は置かない |
| REJECT A | fail log 全体の unbounded `cat` は既定ではない |
| C later | fail-cap C は、測定で B の token 消費が残ると分かったあとだけである |

CI と local の fail は `--log` または `QUIET_KEEP_FAIL_LOG` の一方を持つ。full dump は disk に残る。chat に full dump は残らない。

`QUIET_FAIL_LINES` の以前の既定は 200 である。
