# plugins

プラグインの入手と自作。

## 有料 Grok Bot で X plugin を繋いで無料 X API credits

- 内容: X Bot を作り、その Bot に X plugin の接続を頼む。Connect カードで X にサインインする。有料 Grok Bot ユーザーは開始用の無料 X API credits を受け取れる。手順ガイドの下書き。
- 出典: [x.com/AIAcademykorea/status/2094921380253077918](https://x.com/AIAcademykorea/status/2094921380253077918)（2026-09-01）
- 確認: 未

## Supermemory プラグイン

- 内容: Grok Bot 用の Supermemory プラグイン。@bot に supermemory を追加するよう伝えると、エージェント間で共有メモリになる。
- 出典: [x.com/DhravyaShah/status/2094915837476082048](https://x.com/DhravyaShah/status/2094915837476082048)（2026-09-01）、[x.ai/bot/plugin/58578698](https://x.ai/bot/plugin/58578698)
- 確認: 未

## Outlook プラグインは 1 Microsoft アカウント

- 内容: Outlook プラグインは OAuth で 1 つの Microsoft アカウントだけを認可し、そのサインインユーザーの mailbox にだけ届く。共有 mailbox は非対応。
- 出典: [x.com/grok/status/2094915188105294255](https://x.com/grok/status/2094915188105294255)（2026-09-01）
- 確認: 未

## tinkabot で API からプラグインを足場にする

- 内容: API を指すと Grok Bot プラグイン（MCP + skills）を作り、承認提出できる。
- 出典: [x.com/GrokBotsBest/status/2094928135871467570](https://x.com/GrokBotsBest/status/2094928135871467570)（2026-09-01）
- 確認: 未

## Settings → Plugins

- 内容: コネクタはアプリ上では Plugins と表示される。Settings → Plugins で追加し、Marketplace でコネクタとパッケージ済みスキルを探す。Yours で導入済みを見る。チャットでは `/` が保存スキル、`@` が Bot・グループ・routine・コネクタ。
- 出典: [Use the computer and apps](https://docs.x.ai/grok-bot/computer-and-apps)（2026-08-29 確認）、[Settings and notifications](https://docs.x.ai/grok-bot/settings-and-notifications)
- 確認: 未

## Cursor プラグインの自作

- 内容: `.cursor-plugin/plugin.json` をマニフェストとして作る。`skills/` へのパスをマニフェストで指す。実例: [pstack の plugin.json](https://github.com/cursor/plugins/blob/main/pstack/.cursor-plugin/plugin.json)。このリポジトリ自体も同じ形式（[`.cursor-plugin/plugin.json`](../../.cursor-plugin/plugin.json)）。
- 出典: [pstack/.cursor-plugin/plugin.json](https://github.com/cursor/plugins/blob/main/pstack/.cursor-plugin/plugin.json)
- 確認: 済
