# jenny-lite stall-adopt（box sand-workflow SoftHOLD）

## Purpose

Issue [#136](https://github.com/maplefukku/grok-bot-ops/issues/136) の A–D **encode 先**は既存 box sand-workflow 4 本にする（[fleet-stall-sweep](sand-workflow:fleet-stall-sweep) / [author-routines](sand-workflow:author-routines) / [schedules-force-agency](sand-workflow:schedules-force-agency) / [conductor-keep-moving](sand-workflow:conductor-keep-moving)）。**未 encode**。本リポジトリ差分はこの SoftHOLD process メモと参照行だけであり、4 workflow 本文はこの diff に無い。`skills/` へ本体をコピーしない（plugin HARD）。「reviewable mirror」と呼ばない。fallen tip `1a58a0d` を SoT にしない。CreateAgent / Jenny seat / credit-audit / auto-merge / webhook-fixer auto-exec / eng-only stall sweep はしない。

本 WRAP は encode 完了を主張しない。PR 本文・commit message に GitHub の issue-closing keyword を付けない。issue #136 は OPEN のまま（Testing: eval 後 1 スキル 1 PR）。encode がレビュー可能な差分になるまで閉じない。

## SoftHOLD（HARD A–D 表は置かない）

Done-when HARD の A–D 表は置かない。done-when の正本は issue #136 本文だけである。`e0301fb` が fleet.md から A–D を落とした理由（Sep06 GATE/ADV/Swift 文字撞突、PM ACK DELTA 無し、factory BROKEN / silent-miss cites invent）と、`0fbadf9` の Prefer drop（fallen tip `1a58a0d` / issue 136）を Prefer。live ADOPT B/C/D は `docs/knowhow/fleet.md` の ADV reopen / Swift flake / GATE IFF であり、jenny-lite Mode B/C/D とは別物。PM ACK より新しい文字撞突解消 DELTA が揃うまで SoftHOLD。Mode B/C/D を再 ADOPT しない。Mode A BROKEN 三条件の再定義も invent しない（named-HOLD GAP は fleet.md）。

## 引き渡し

| 項目 | 値 |
|---|---|
| 書き手 | [スキル作成](../../bots/スキル作成.md)（[author-shared-skill](sand-workflow:author-shared-skill)）。Planner / Mini / cloud CA は box 本文を書かない |
| 単位 | 既存 workflow 1 本につき eval 1 回と PR 1 本 |
| 前提 | PM ACK と文字撞突解消 DELTA。未マージの daily knowhow 行は前提にしない |
| 閉じる証拠 | box workflow 本文の差分と `evals/` の盲検評価記録。CI green とこのメモは証拠にしない |

`bots/` のスキル行は稼働中ボットの台帳である。box 側で workflow が載るまで、このメモから行を足さない。

## Flag Y

PdM Flag Y ONLY は [`pr-body.md`](./pr-body.md)。本ファイルに第二コピーを置かない。

## CreateAgent

CreateAgent NONE。agency 監査は既存 CBO 経路の審査メモだけ。「agency 行があれば CreateAgent してよい」とは読まない。

## Testing / promotion

スキル作成 eval playbook。1 スキル 1 PR after eval。Planner / Mini は plugin `skills/` に本体を置かない。

## SoftHOLD merge

merge=PM。undraft / FlagY / SoftB FIRE はしない。Mini WRAP だけで merge しない。
