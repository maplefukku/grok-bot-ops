# routines

Grok Bot の routine（定期実行・イベント・webhook）の公式の使い方。

## ChatGPT → Grok Bot の bridge（Bridge Bot + webhook routine + skill）

- 内容: Grok Bot に "Bridge Bot" を新設し、webhook trigger の routine を作り、ChatGPT 側にその webhook へコマンドを送る skill を作る。ChatGPT から Grok Bot へ routine の設定、状態確認、作業の委譲を送れる、という報告。
- 出典: [x.com/moritzkremb/status/2097621535955833166](https://x.com/moritzkremb/status/2097621535955833166)（2026-09-09）
- 確認: 未

## webhook + iOS ショートカットでスマホの入力を Bot へ

- 内容: Grok Bot の webhook で外部からの入力を受けてワークフローに繋ぎ、iOS ショートカットと組み合わせてスマホから Grok Bot へ入力しやすくする、という用法。
- 出典: [x.com/0xlangeai/status/2097505793079931247](https://x.com/0xlangeai/status/2097505793079931247)（2026-09-09）
- 確認: 未

## 例外監視 webhook → GitHub issue と fixer

- 内容: 例外監視サービスから webhook を受け、GitHub issue を作りつつ Bot の webhook に投げて fixer を起こす運用例。incoming webhook が使える前提。
- 出典: [x.com/claytonlz/status/2097381463847297443](https://x.com/claytonlz/status/2097381463847297443) · [raises.dev](https://raises.dev/)（2026-09-08）
- 確認: 未

## Teach a task（デモから skill）

- 内容: Teach a task が使えるとき、ブラウザ作業を最大10分デモ録画して skill 下書きを作れる。マイク音声は録らない。秘密はデモ中に出さず secure handoff を使う。できた skill は draft。見えない場合は文章指示から skill を作らせる。
- 出典: [Skills and routines](https://docs.x.ai/grok-bot/skills-routines-and-automations)（2026-09-07 確認）
- 確認: 未

## 監視 webhook → Cloud Agent で PR

- 内容: Laravel Nightwatch（web + telemetry）と Sentry（iOS + Android）から webhook を受け、Laravel Cloud のヘルスは API の定期チェック。エラーが出たら Cloud Agent を起こして PR を作る運用例。
- 出典: [x.com/teslascope/status/2094570345902845980](https://x.com/teslascope/status/2094570345902845980)（2026-08-31）
- 確認: 未

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

## 運用の型（このリポジトリの採用ルール）

- 内容: routine 1 本につき専用ボット 1 体。原稿は [`routines/`](../../routines/README.md) を正本にし、貼り付け先を実体とする。出力には毎回処理件数を含めさせ、コスト異常に気づけるようにする。
- 出典: 上項（担当ボットに付ける）を、この司令室の規約にしたもの。[Skills and routines](https://docs.x.ai/grok-bot/skills-routines-and-automations)
- 確認: 済（このリポジトリの規約）
