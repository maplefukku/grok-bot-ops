# routines/

Grok Bot の routine（外側ループ）の**原稿置き場**です。稼働する実体は Grok Bot 本体に貼った routine で、ここはその正本です。変更はまずここを直し、それから貼り直します。

## 運用ルール（Lauren の実運用から）

- **routine 1 本につき専用ボット 1 体。** メインボットはチーフ・オブ・スタッフとして残し、定期作業を背負わせない。長い本チャットで routine を回すと、毎回そのコンテキスト分のトークンを食う。
- **高頻度スケジュールを避ける。** 15 分間隔は 1 日ほぼ 100 回走る。時間単位か 1 日数回で足りることがほとんど。
- **外側ループは収集と仕分けまで。** 修正や実装はやらせない。工場（プロダクトリポジトリの cloud agent）へ投げる素材を耕すのが仕事。
- **外部から起こすなら webhook routine。** 自作 UI やアプリからボットを起動できる。
- 費用の異常に気づけるよう、routine の出力には毎回、処理件数を含めさせる。

## routine は使いながら増やす

このディレクトリは最初から埋めません。Grok Bot を触る中で「定期化する価値がある」と分かった仕事だけを、[`_template.md`](./_template.md) から原稿に起こして足します。

## いまある原稿

| ファイル | 目的 | 頻度の目安 |
|---|---|---|
| [`collect-grokbot-knowhow.md`](./collect-grokbot-knowhow.md) | Grok Bot のアップデート・活用法を X から収集し `docs/knowhow/` へ | 1 日 1 回 |
| [`decide-trend-adopt.md`](./decide-trend-adopt.md) | 候補を ADOPT または REJECT し `docs/decisions/trend-log.md` へ残す | 1 日 1 回 |
| [`maintain-verification.md`](./maintain-verification.md) | 各プロダクトの feature map を毎日更新（プロダクト登録後に有効） | 1 日 1 回 |

## 例（[`examples/`](./examples/)）

プロダクトを持って外側ループを組むときの型見本です。そのままは動かしません。使うときは対象チャンネルやキーワードを埋め、トップレベルにコピーして「下書き → 稼働中」に上げてください。

| ファイル | 目的 |
|---|---|
| [`examples/intake-slack-bugs.md`](./examples/intake-slack-bugs.md) | Slack のバグ報告チャンネルを収集・仕分け |
| [`examples/intake-x-feedback.md`](./examples/intake-x-feedback.md) | 自分のプロダクトへの X の反応を収集 |
