# routines

Grok Bot の routine（定期実行・イベント・webhook）の公式の使い方。

## 担当ボットに付ける

- 内容: routine は「その定期作業を持つ Bot」に作る。スケジュールとタイムゾーン、入力、期待結果、承認境界、ソース欠損時の振る舞いを確認する。1 Bot は最大 50 routine。直近 20 回の実行記録が残る。バックグラウンド routine はノート PC を閉じても動く。
- 出典: [Skills and routines](https://docs.x.ai/grok-bot/skills-routines-and-automations)（2026-08-29 確認）
- 確認: 未

## イベント起点は狭くする

- 内容: Cursor アカウント連携で、Slack メッセージや GitHub 通知などから routine を起こせる。プラグインの Slack / GitHub とは別接続のことがある。「すべての新着」のような広いリスナーはノイズになり、usage を食う。
- 出典: [Skills and routines](https://docs.x.ai/grok-bot/skills-routines-and-automations)（2026-08-29 確認）
- 確認: 未

## webhook routine

- 内容: pstack の `/make-bot-ui` は `trigger: { "type": "webhook" }` の routine を作り、外部 UI のサーバから JSON を POST してボットを起こす手順を書く。sender key はサーバに置き、ブラウザやチャットに出さない。
- 出典: [pstack `/make-bot-ui`](https://github.com/cursor/plugins/blob/main/pstack/skills/make-bot-ui/SKILL.md)
- 確認: 未

## webhook の URL / sender key は desktop だけ

- 内容: webhook routine の POST URL・sender key・Authorization ヘッダは desktop アプリの trigger カードにだけ出る。iOS アプリは Active / trigger 名 / 指示 / 実行履歴だけで URL・key は見えない。
- 出典: [x.com/MartyEarthy/status/2094203371817513281](https://x.com/MartyEarthy/status/2094203371817513281)（2026-08-30）、[x.com/MartyEarthy/status/2094203369992999400](https://x.com/MartyEarthy/status/2094203369992999400)
- 確認: 未

## iPhone Shortcuts から webhook routine に位置を POST

- 内容: iOS Shortcuts で現在地を取り、webhook routine の POST URL へ JSON（lat/lon/accuracy_m）を送る手順の実例。Authorization: Bearer と X-Automation-Key の両方に同じ sender key。通知やクリップボードに key/URL を出さない。
- 出典: [x.com/MartyEarthy/status/2094203369992999400](https://x.com/MartyEarthy/status/2094203369992999400)（2026-08-30）、[x.com/MartyEarthy/status/2094203371817513281](https://x.com/MartyEarthy/status/2094203371817513281)
- 確認: 未

## GitHub PR 監視 routine でレビュー Bot

- 内容: 専用 GitHub アカウントを Bot に渡し、新着/変更 PR を routine で監視 → カスタム prompt/skills でレビュー → GitHub review と Slack 通知、という運用例。
- 出典: [x.com/dqlopez/status/2094137708432273474](https://x.com/dqlopez/status/2094137708432273474)（2026-08-30）
- 確認: 未

## 運用の型（このリポジトリの採用ルール）

- 内容: routine 1 本につき専用ボット 1 体。原稿は [`routines/`](../../routines/README.md) を正本にし、貼り付け先を実体とする。出力には毎回処理件数を含めさせ、コスト異常に気づけるようにする。
- 出典: 上項（担当ボットに付ける）を、この司令室の規約にしたもの。[Skills and routines](https://docs.x.ai/grok-bot/skills-routines-and-automations)
- 確認: 済（このリポジトリの規約）
