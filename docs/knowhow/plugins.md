# plugins

プラグインの入手と自作。

## Settings → Plugins

- 内容: コネクタはアプリ上では Plugins と表示される。Settings → Plugins で追加し、Marketplace でコネクタとパッケージ済みスキルを探す。Yours で導入済みを見る。チャットでは `/` が保存スキル、`@` が Bot・グループ・routine・コネクタ。
- 出典: [Use the computer and apps](https://docs.x.ai/grok-bot/computer-and-apps)（2026-08-29 確認）、[Settings and notifications](https://docs.x.ai/grok-bot/settings-and-notifications)
- 確認: 未

## Cursor プラグインの自作

- 内容: `.cursor-plugin/plugin.json` をマニフェストとして作る。`skills/` へのパスをマニフェストで指す。実例: [pstack の plugin.json](https://github.com/cursor/plugins/blob/main/pstack/.cursor-plugin/plugin.json)。このリポジトリ自体も同じ形式（[`.cursor-plugin/plugin.json`](../../.cursor-plugin/plugin.json)）。
- 出典: [pstack/.cursor-plugin/plugin.json](https://github.com/cursor/plugins/blob/main/pstack/.cursor-plugin/plugin.json)
- 確認: 済
