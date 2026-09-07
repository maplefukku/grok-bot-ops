# CI 梯子（LIGHT→FULL）

## Purpose

PdM が 2026-09-08 に確認した bake である。CBO LEDGER NOTE 2026-09-08 である。席一行の bake は draft [PR 58](https://github.com/maplefukku/grok-bot-ops/pull/58) である。引用は [job-brief](sand-workflow:job-brief)、[Cloud開発](sand-workflow:cloud)、[parallel-fire-fleet](sand-workflow:parallel-fire-fleet)、[#32 LOCK A](https://github.com/maplefukku/grok-bot-ops/issues/32)、[#16](https://github.com/maplefukku/grok-bot-ops/issues/16)、[ADR 0003](../decisions/0003-domain-unit-throughput.md) である。

このページは WRAP だけである。太い lander の正本は [`README.md`](./README.md) の出荷単位である。worktree の掃除は [`worktree-prune.md`](../mini-ops/worktree-prune.md) である。PR 本文の 4 見出しは [`pr-body.md`](./pr-body.md) である。テスト証拠は既存の `/workspace/fleet-scripts/quiet-test.sh -- <cmd>` である。このリポジトリの WRAP は [`scripts/quiet-test.sh`](../../scripts/quiet-test.sh) である。新しい test harness は置かない。梯子の中身は invent しない。

SPEED NORM は並列 local worktree と BDD/scenario の太い domain lander である。点滴 micro-PR は禁止である。

## 対象

開発リーダー、product 開発*、impl CA、PR確認、PdM の merge sweep である。

## 範囲

### 対象にする

PdM が確認した bake と、CBO の席一行である。

### 対象にしない

CTO extras は post-RATIFY まで HOLD である。中身は書かない。プロダクトリポジトリの workflow 定義は書かない。品質Drive の [HOLD LOCK 2026-09-06](../../bots/品質Drive.md) は再開しない。CreateAgent と新しい席は置かない。新しい harness は FAIL である。

## SoT

席一行の bake は [PR 58](https://github.com/maplefukku/grok-bot-ops/pull/58) である。出荷単位は [`README.md`](./README.md) である。PR 本文は [`pr-body.md`](./pr-body.md) である。recipe SoT は box `/workspace/fleet-scripts/pr-show-me-template.md` である。quiet-test の SoT は box `/workspace/fleet-scripts/quiet-test.sh` である。本体は vendor しない。

## bake

| 事実 | 値 |
|---|---|
| SPEED NORM | 並列 local worktree。BDD/scenario の太い domain lander。点滴 micro-PR は禁止 |
| CI 梯子 | LIGHT-WT → same-BC combine → FULL path-first → post-merge E2E |
| merge-batch | same-BC |
| Flag | FULL tip だけ |
| E2E | FULL tip だけ |
| HOLD | CTO extras は post-RATIFY まで |
| 席一行 | 並列local worktree / BDDシナリオの太いPRで点滴micro-PR禁止 / merge-batch+CI梯子LIGHT→FULL |

required CI の green は same-BC を畳んだ FULL tip である。LIGHT-WT の green は merge-ok ではない。

post-merge E2E は段である。品質Drive の HOLD を上書きしない。

段の中身は invent しない。jobs と `paths` と runner はプロダクトリポジトリの workflow である。
