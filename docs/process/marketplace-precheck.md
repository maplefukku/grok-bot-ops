# Marketplace survey（CreateAgent precheck）

## Purpose

ふっくー HARD は CreateAgent 量産 NONE である。適用 issue は [#92](https://github.com/maplefukku/grok-bot-ops/issues/92) である。採択は [trend-log](../decisions/trend-log.md) の 2026-09-07 Official Bot Marketplace templates（約69）+ Haggle procurement である。Haggle 行は同じ日の Haggle anti-job である。引用は [parallel-fire-fleet](sand-workflow:parallel-fire-fleet)、[Cloud開発](sand-workflow:cloud)、tool-path-prefer、/poteto-mode である。

このページは WRAP だけである。Marketplace 約 69 templates の事実は [`templates.md`](../knowhow/templates.md) である。事実をここへ複製しない。export-bot-template は KEEP である。並列の自前公開経路は invent しない。CreateAgent は [`CBO`](../../bots/CBO.md) である。CreateAgent NONE である。量産しない。

テスト証拠は既存の `/workspace/fleet-scripts/quiet-test.sh -- <cmd>` である。このリポジトリの WRAP は [`scripts/quiet-test.sh`](../../scripts/quiet-test.sh) である。新しい test harness は置かない。入口は /poteto-mode である。

## 対象

CBO と、CreateAgent を依頼する PdM、編成評価である。impl CA は読まない。CreateAgent しない。

## 範囲

### 対象にする

CreateAgent 前の Marketplace survey である。KEEP と WRAP の順である。

### 対象にしない

CreateAgent の量産は対象外である。プロダクトコードは対象外である。on-demand は対象外である。Haggle 調達ボットの CreateAgent は対象外である。並列 Marketplace は REJECT である。新しい席は置かない。新しい harness は FAIL である。

## SoT

一次の Marketplace は https://x.ai/bot/marketplace である。調達記事は https://x.ai/news/grok-bot-procurement である。templates の事実は [`templates.md`](../knowhow/templates.md) である。CreateAgent 席は [`CBO`](../../bots/CBO.md) である。quiet-test の SoT は box `/workspace/fleet-scripts/quiet-test.sh` である。本体は vendor しない。

## 順

1. 公式 Marketplace を見る。入口は https://x.ai/bot/marketplace である。
2. 既存 template を KEEP するか、export-bot-template で WRAP する。
3. それでも足りないときだけ、CBO が CreateAgent する。量産は CreateAgent NONE である。

Haggle は Marketplace の調達テンプレである。spend / sign / send は explicit go なしで禁止である。Haggle 自体を CreateAgent しない。

## 禁止

| 禁止 | 破る規則 |
|---|---|
| CreateAgent 量産 | CreateAgent NONE である。席は CBO 1 体である |
| 並列 Marketplace | export-bot-template は KEEP である。自前公開経路は invent しない |
| templates 事実の複製 | 事実は knowhow である。手順だけがこのページである |
