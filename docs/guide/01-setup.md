# pstack をセットアップする

このページではプラグインを入れ、pstack が使うモデルを選び、最初のタスクを走らせます。セットアップはコマンド 1 つと、短い会話です。

## プラグインを入れる

Cursor のチャットで:

```text
/add-plugin pstack
```

Cursor がインストール完了を確認します。

## モデルを選ぶ

次を実行します:

```text
/setup-pstack
```

[`/setup-pstack`](https://github.com/cursor/plugins/blob/main/pstack/skills/setup-pstack/SKILL.md) は、使えるモデルを検出し、役割（コード委任、判断、レビューパネル）ごとに何を使うか尋ねます。質問に答えてください。`~/.cursor/rules/pstack-models.mdc` という小さなルールを書き、すべての pstack スキルがそれを読みます。

上書きするのは気になる役割だけで構いません。ルールに行がない役割は、スキル側のデフォルトのままです。あとからデフォルトに戻すなら、その役割の行を消すか、もう一度 `/setup-pstack` を走らせます。

Auto を使っている場合はどうなるか。役割を `inherit-parent` か `auto` にすると、pstack はサブエージェントの `model` フィールドを省略するので、親チャットのモデルを継承します。どちらも同じ意味で、どちらもモデルスラッグではありません。パネル役割の値はリストで、エントリごとにサブエージェントが 1 体走るので、リストの長さがパネル人数になります。セットアップは `swarm workers` も決めます。これは `/swarm` の各ワーカーのデフォルトで、レースが腕ごとにモデルを指名しない限り使われます。

## 検証スキルの提案を受けるか、見送るか

セットアップの最後に、`/setup-pstack` はプロジェクト内でアプリの動きを証明する手段を探します。`verify-*` スキルか、既存のハーネスです。どちらも無いと、[`/create-verification-skill`](https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/SKILL.md) で一度だけ生成を提案します。

はい、と答えると `.cursor/skills/verify-<app>/` を書きます。エージェントに、ユーザーと同じ操作でアプリを動かすことを教える、プロジェクトローカルなスキルです。引き渡す前に、一度動くことを自分で証明します。いいえ、ならセットアップは先へ進みます。`/create-verification-skill` はいつでも自分で回せます。いつ本領を発揮するかは [検証して出荷する](./06-verify-and-ship.md#プロジェクト用の検証スキルを作る) を見てください。

セットアップのあと、新しいチャットを開いてください。モデルルールは新しいセッションから効きます。

## 最初のタスクを走らせる

本物で小さいものを選び、同僚に話すつもりで書いてください:

```text
/poteto-mode add a --json flag to this command. text output stays byte-identical. verify both.
```

todo リストを見てください。先頭は必ず「Principles セクションを読む」です。残りは当たったプレイブックの手順をコピーしたもので、このプロンプトなら Feature です。`/poteto-mode` がステップを飛ばすときは、リストに残したまま `skip: <理由>` が付くので、やらなかった判断が見えます。

ここからは普通のフォローアップで大丈夫です。`/poteto-mode` はその会話に張り付きます。明示的に外すまで、その会話ではオンのままです。

次: [`/poteto-mode` に仕事を通す](./02-poteto-mode.md)。
