# quiet-test（fail-cap B）

## Purpose

このページは quiet-test の fail-cap B LOCK である。親 SoT は [issue 42](https://github.com/maplefukku/grok-bot-ops/issues/42) である。適用 issue は [issue 45](https://github.com/maplefukku/grok-bot-ops/issues/45) である。引用は [Cloud開発](sand-workflow:cloud)、tool-path-prefer、GB、[parallel-fire-fleet](sand-workflow:parallel-fire-fleet) である。

## 対象

impl CA と 開発 bots である。

## 範囲

### 対象にする

fail-cap B LOCK の文書化である。box SoT の WRAP である。

### 対象にしない

[issue 44](https://github.com/maplefukku/grok-bot-ops/issues/44) の CI wrap と NEW-repo pointer は対象外である。[issue 46](https://github.com/maplefukku/grok-bot-ops/issues/46) の PR-body show-me LOCK は対象外である。fail-cap A を既定にすることは対象外である。fail-cap C を Phase0 にすることは対象外である。wrapper 本体を新しく書くことは対象外である。

## SoT

SoT は box の `/workspace/fleet-scripts/quiet-test.sh` である。このリポジトリは script を vendor しない。WRAP のみである。NEW-repo の scaffold は box path を指す。本体をコピーしない。

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

fail は full-log path を必ず印字する。CI と local の fail は `--log` または `QUIET_KEEP_FAIL_LOG` の一方を持つ。full dump は disk に残る。chat に full dump は残らない。

## 呼び出し

| 面 | 規則 |
|---|---|
| CA と 開発 bots | MUST wrap は `/workspace/fleet-scripts/quiet-test.sh -- <cmd>` である |
| CI stdout | quiet stdout は任意である |
| CI gate | exit code と junit または artifacts は MUST である |
| lane formatter | `xcbeautify` と vitest reporters は wrapped cmd の内側で先に動く |
| wrap | quiet-test は cmd 全体を wrap する |
| skip | Quiet is not skip |

## 既定値

| 名前 | 既定 |
|---|---|
| `QUIET_OK_LINES` | 10 |
| `QUIET_FAIL_LINES` | 500 |
| `--log` | fail は full-log path を印字する |
| `QUIET_KEEP_FAIL_LOG` | fail の full dump を disk へ残す |

`QUIET_FAIL_LINES` の以前の既定は 200 である。

## 出典

| 名前 | 参照 |
|---|---|
| parent SoT | https://github.com/maplefukku/grok-bot-ops/issues/42 |
| this issue | https://github.com/maplefukku/grok-bot-ops/issues/45 |
| Cloud開発 | sand-workflow:cloud |
| tool-path-prefer | tool-path-prefer |
| GB | Grok Bot |
| parallel-fire-fleet | sand-workflow:parallel-fire-fleet |
