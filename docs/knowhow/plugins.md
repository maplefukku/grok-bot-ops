# plugins

プラグインの入手・共有・自作。

## ディープリンクで直接入れる

- 内容: `grokbot://app/v1/plugin/add?id=<id>` で Grok Bot にプラグインを直接インストールできる。既知の id: pstack `9717366`、X plugin `49086599`。
- 出典: X の投稿（リンク要補完）（2026）
- 確認: 未

## プラグイン・設定の共有リンク

- 内容: プラグインのタイトルにホバーするとリンクをコピーできる。設定も共有可能（例: 言語設定 `grokbot://app/v1/settings?id=language`）。
- 出典: X の投稿（リンク要補完）（2026）
- 確認: 未

## Cursor プラグインの自作

- 内容: `.cursor-plugin/plugin.json` をマニフェストとして作る。`skills/` `agents/` へのパスをマニフェストで指す。実例: [pstack の plugin.json](https://github.com/cursor/plugins/blob/main/pstack/.cursor-plugin/plugin.json)。このリポジトリ自体も同じ形式（[`.cursor-plugin/plugin.json`](../../.cursor-plugin/plugin.json)）。
- 出典: pstack リポジトリの実物
- 確認: 済
