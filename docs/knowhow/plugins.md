# plugins

プラグインの入手と自作。

## Coinbase connector で limit order

- 内容: Grok と Grok Bot を Coinbase connector 経由で接続し、limit buy/sell が動いたという報告。connectors 画面: [grok.com/connectors](https://grok.com/connectors)
- 出典: [x.com/allthemoney/status/2102066509560291342](https://x.com/allthemoney/status/2102066509560291342) · [grok.com/connectors](https://grok.com/connectors)（2026-09-21）
- 確認: 未

## ワンクリック plugin share deeplink

- 内容: プラグインページで share / link アイコンから `grokbot://app/v1/plugin/add?id=…` 形式の deeplink を取得。X desktop クライアントで動作。
- 出典: [x.com/mattyp/status/2101491045553070094](https://x.com/mattyp/status/2101491045553070094)（2026-09-20）
- 確認: 未

## MCP で共有 AI memory

- 内容: MCP を使って Bot 間・ツール間で AI memory を共有する、という用法の報告。
- 出典: [x.com/connorgallic/status/2099630749380956315](https://x.com/connorgallic/status/2099630749380956315)（2026-09-15）
- 確認: 未

## Microsoft Teams

- 内容: Teams for Grok Bot プラグインでチャット・チャネルメッセージの検索・閲覧・送信ができる。
- 出典: [x.com/bot/status/2098481256417866145](https://x.com/bot/status/2098481256417866145) · [Teams plugin](https://x.ai/bot/plugin/63354504)（2026-09-11）
- 確認: 未

## GTM connectors (Salesforce / HubSpot / Gong / Clay / Granola)

- 内容: Bot を Salesforce、HubSpot、Gong、Clay、Granola など GTM ツールに接続し、アカウント把握・フォローアップ・調査ができる、という公式告知。
- 出典: [x.com/bot/status/2098183353665261979](https://x.com/bot/status/2098183353665261979)（2026-09-10）
- 確認: 未

## Dialbot + Bland で Grok Bot に電話させる

- 内容: Dialbot を入れ、Bland の voice を繋いで Bot から電話をかけるデモ。transcript / cost 確認と bot 連鎖まで。template: [x.ai/bot/NJXi2SWEuhNxjOjspMMPi](https://x.ai/bot/NJXi2SWEuhNxjOjspMMPi)
- 出典: [x.com/mattyp/status/2098155792327381294](https://x.com/mattyp/status/2098155792327381294)（2026-09-10） · [template](https://x.ai/bot/NJXi2SWEuhNxjOjspMMPi) · [reply](https://x.com/mattyp/status/2098156079620542639)
- 確認: 未

## Grok Voice（Cursor marketplace）— dictation / realtime voice / read-aloud

- 内容: Cursor marketplace の Grok Voice プラグイン。/add-dictation、/add-voice、/add-read-aloud。/debug-voice もある。コード: [github.com/cursor/plugins/tree/main/grok-voice](https://github.com/cursor/plugins/tree/main/grok-voice)
- 出典: [x.com/ericzakariasson/status/2098080093562458445](https://x.com/ericzakariasson/status/2098080093562458445)（2026-09-10） · [marketplace](https://cursor.com/marketplace/cursor/grok-voice) · [code](https://github.com/cursor/plugins/tree/main/grok-voice) · [debug](https://x.com/ericzakariasson/status/2098080105654608018)
- 確認: 未

## Microsoft Outlook / Calendar / OneDrive

- 内容: 新しいプラグインで Bot が Outlook、Calendar、OneDrive に直接アクセスする。閲覧だけではなく読み書き・操作ができる。
- 出典: [x.com/bot/status/2094543253811183943](https://x.com/bot/status/2094543253811183943)（2026-08-31）
- 確認: 未

## メール送信の前に禁止事項を書く

- 内容: Bot がメールを送れるなら、先に「送ってはいけないもの」を書いてから inbox を繋ぐ。書いていないまま接ぐと、inbox を chatbot に渡したことになる。
- 出典: [x.com/PedroKnigge/status/2094562726236541406](https://x.com/PedroKnigge/status/2094562726236541406)（2026-08-31）
- 確認: 未

## X plugin / X connector

- 内容: X plugin / X connector で投稿検索・タイムライン・トレンド・ブックマークができる。有料 Grok Bot ユーザーには開始用の無料 X API credits が付く。
- 出典: [Grok Bot now works with X](https://x.ai/news/grok-bot-and-x)（2026-08-29）
- 確認: 未

## Settings → Plugins

- 内容: コネクタはアプリ上では Plugins と表示される。Settings → Plugins で追加し、Marketplace でコネクタとパッケージ済みスキルを探す。Yours で導入済みを見る。チャットでは `/` が保存スキル、`@` が Bot・グループ・routine・コネクタ。
- 出典: [Use the computer and apps](https://docs.x.ai/grok-bot/computer-and-apps)（2026-08-29 確認）、[Settings and notifications](https://docs.x.ai/grok-bot/settings-and-notifications)
- 確認: 未

## Cursor プラグインの自作

- 内容: `.cursor-plugin/plugin.json` をマニフェストとして作る。`skills/` へのパスをマニフェストで指す。実例: [pstack の plugin.json](https://github.com/cursor/plugins/blob/main/pstack/.cursor-plugin/plugin.json)。このリポジトリ自体も同じ形式（[`.cursor-plugin/plugin.json`](../../.cursor-plugin/plugin.json)）。
- 出典: [pstack/.cursor-plugin/plugin.json](https://github.com/cursor/plugins/blob/main/pstack/.cursor-plugin/plugin.json)
- 確認: 済
