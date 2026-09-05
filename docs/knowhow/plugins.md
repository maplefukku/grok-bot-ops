# plugins

プラグインの入手と自作。

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
