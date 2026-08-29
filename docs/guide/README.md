# pstack ガイド

> 日本語訳: [pstack 公式ガイド](https://github.com/cursor/plugins/tree/main/pstack/docs/guide)（[MIT License](./NOTICE.md), © 2026 Lauren Tan）
> スキル本体へのリンクは原文リポジトリを指します。

pstack は、エージェントを細かく管理するのをやめたときにいちばん効きます。欲しいものと、終わったと判断できる条件を自分の言葉で渡す。`/poteto-mode` がプレイブックを選び、必要なスキルをステップに応じて呼び、証拠を見せます。このガイドは、その習慣を現実的なプロンプトで身につけるためのものです。

ここで学ぶこと:

1. [pstack をセットアップする](./01-setup.md)。プラグインを入れ、モデルを選ぶ。
2. [`/poteto-mode` に仕事を通す](./02-poteto-mode.md)。ゴールを渡し、プレイブックが選ばれるのを見る。
3. [コードを理解する](./03-understand.md)。何か書く前に `/how`、`/why`、`/teach`、`/recall`。
4. [変更を設計する](./04-design.md)。形が固まる前に `/architect`、`/arena`、`/swarm`、`/interrogate`。
5. [作って差分をきれいにする](./05-build-and-clean.md)。ビルド用プレイブック、`/tdd`、`/unslop`、`/no-comments`。
6. [検証して出荷する](./06-verify-and-ship.md)。本物のアプリで動きを証明し、焦点の絞られた PR を開き、マージまで運ぶ。
7. [寝ているあいだに回す](./07-overnight.md)。一晩の契約、朝に監査できる判断ログ、エージェント 1 体の枠を超えてスケールするプレイブック。
8. [原則の名前で舵を切る](./08-principles.md)。作業の途中でエージェントを振り向ける 21 の名前。
9. [自分のものにする](./09-make-it-yours.md)。自分用のモードと、スキル変更の試し方。
10. [レシピと落とし穴](./10-recipes-and-pitfalls.md)。コピーできるプロンプトと、避けたい失敗。

最初は順に読んでください。二度目からは各ページが独立しています。

## ひとつだけ覚えるなら

ゴールと、合否が分かる確認方法を、自分の言葉で渡すこと:

```text
/poteto-mode the export writes duplicate rows when a retry lands mid-run. repro first, then fix and verify.
```

プレイブック名もスキル一覧も要りません。「repro first」と確認できる結果があれば、`/poteto-mode` がルーティングできます。Bug fix プレイブックに当たり、手順を todo にコピーし、各ステップで必要なスキルを呼びます。

次: [pstack をセットアップする](./01-setup.md)。
