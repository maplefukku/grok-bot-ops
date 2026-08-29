# docs/knowhow/

Grok Bot 全般のノウハウ置き場です。**特定の人物に縛りません。** poteto/pstack は数ある出典のひとつで、それは [`docs/guide/`](../guide/README.md) に住んでいます。ここには X などで見つけた、誰の発信かを問わないアップデート情報と活用法を貯めます。

## 構成

| ファイル | 内容 |
|---|---|
| [`updates.md`](./updates.md) | プロダクトアップデートの時系列ログ（新機能、提供範囲、アプリ） |
| [`routines.md`](./routines.md) | routine（定期実行・webhook）の使い方とコスト |
| [`plugins.md`](./plugins.md) | プラグインとディープリンク |
| [`bot-ui.md`](./bot-ui.md) | カスタム Bot UI |
| [`templates.md`](./templates.md) | ボットテンプレートの共有、ボットを作るボット |
| [`shopping.md`](./shopping.md) | 買い物機能と決済の扱い |
| [`access.md`](./access.md) | 言語・アプリ・加入プラン |

新しいトピックは [`_template.md`](./_template.md) から作ってください。時系列の事実は `updates.md`、使い方の知恵はトピックファイル、が振り分けの基準です。

## 書き込みルール

- **出典リンク必須。** X の投稿、公式ドキュメント、リリースノートなど。リンクが無いものは書かない。
- **日付を残す。** Grok Bot は動きが速いので、いつ時点の情報かが価値の半分。
- **未検証は未検証と書く。** 各エントリに `確認: 済 / 未` を付ける。試して違ったら消すのではなく、結果を追記する。
- 誰の発信でもよいが、発信者の名前でファイルを分けない。トピックで分ける。
- ここのノウハウが自分たちの運用で 2 回以上効いたら、`lessons/` → `skills/` の昇格ルートに乗せる。

## 貯め方

[`routines/collect-grokbot-knowhow.md`](../../routines/collect-grokbot-knowhow.md) を専用ボットに貼ると、X からアップデートと活用法を定期収集し、ここへの追記 PR まで作らせられます。
