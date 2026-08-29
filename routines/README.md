# routines/

Grok Bot の routine（外側ループ）の**原稿置き場**です。稼働する実体は Grok Bot 本体に貼った routine で、ここはその正本です。変更はまずここを直し、それから貼り直します。

## 運用ルール（Lauren の実運用から）

- **routine 1 本につき専用ボット 1 体。** メインボットはチーフ・オブ・スタッフとして残し、定期作業を背負わせない。長い本チャットで routine を回すと、毎回そのコンテキスト分のトークンを食う。
- **高頻度スケジュールを避ける。** 15 分間隔は 1 日ほぼ 100 回走る。時間単位か 1 日数回で足りることがほとんど。
- **外側ループは収集と仕分けまで。** 修正や実装はやらせない。工場（プロダクトリポジトリの cloud agent）へ投げる素材を耕すのが仕事。
- **外部から起こすなら webhook routine。** 自作 UI やアプリからボットを起動できる。
- 費用の異常に気づけるよう、routine の出力には毎回、処理件数を含めさせる。

## いまある原稿

| ファイル | 目的 | 頻度の目安 |
|---|---|---|
| [`intake-slack-bugs.md`](./intake-slack-bugs.md) | Slack のバグ報告を収集・仕分け | 1 時間ごと |
| [`intake-x-feedback.md`](./intake-x-feedback.md) | X の苦情・要望・アイデアを収集 | 1 日 2〜3 回 |
| [`maintain-verification.md`](./maintain-verification.md) | 各プロダクトの feature map を毎日更新 | 1 日 1 回 |

新しい routine は [`_template.md`](./_template.md) から作ってください。
