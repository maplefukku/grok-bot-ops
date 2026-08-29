# レシピと落とし穴

コピーする価値のあるプロンプト、それから一度は誰でもやる失敗です。パスと完了条件は自分のものに差し替えてください。レシピは意図してくだけています。実際に打たれる形であり、スキルは意図を十分読みます。

![She tastes a finished dish while robots cook from a recipe box, with pinned cards reading /how, /tdd, and /loop above the counter.](./images/recipes.jpg)

## 知らないサブシステムを理解する

```text
use /how first to understand how this initialization works. then use /why to figure out why it broke recently.
```

仕組みが先、履歴が後です。各スキルの報告は、どの情報源を探したかを言うので、答えが何に基づいているか分かります。

## 設計に第二の意見を取る

```text
ask /arena for a second opinion on this thread and our approach
```

今の設計が候補のひとつになり、合成は、パネルがより良い案を見つけたのか、手元の案を裏付けたのかを教えてくれます。高いコミットの前の安い保険です。

## 独立したスライスを並列で確認する

```text
/swarm check every package under packages/ against its check.sh. one worker per package. one report.
```

各ワーカーがパッケージを 1 つ所有します。親はすべてのスライスを待ち、ワーカーの生ダンプではなく、ひとつの `PASS`、`ISSUES`、`BLOCKED` 報告を返します。

## ブランチを懐疑的にレビューする

```text
/interrogate the whole branch, but skeptically. don't change anything yet. no nitpicks unless it's an actual bug or regression in behavior.
```

限定が本物の仕事をします。"don't change anything yet" は読み取り専用に保ち、あら探し禁止はノイズを先に濾すので、`Act on` の指摘が時間を割く価値があります。

## 失敗するテスト経由でバグを直す

```text
/poteto-mode repro the duplicate write first. if there's a cheap test path, /tdd it. then fix and rerun.
```

"if there's a cheap test path" が効きます。脆いモックでテストを通すより、本物のコマンドを走らせるほうが証明になり、プレイブックはそう言ってよいことになっています。

## 席を外しているあいだ、実行を正直に保つ

```text
im going to bed, keep going autonomously until every fixture passes. do not stop. keep a decision log i can audit in the morning.
```

契約の全体は [一晩のページ](./07-overnight.md) にあります。タスクと完了条件がすでに会話にあるなら、短い形で足ります。

## 逸れた実行を振り向ける

舵取りのプロンプトは 1 行です:

```text
i said the goal is to repro. i did not ask for a fix yet.
```

```text
apply prove it works. show me the real output, not the build log.
```

```text
/unslop that, no emdashes
```

言葉はほとんど要りません。要るのは正しい名前で、語彙は [原則のページ](./08-principles.md) です。

## 返事を平易な言葉にする

```text
/bro
```

プロンプトはこれだけです。[`/bro`](https://github.com/cursor/plugins/blob/main/pstack/skills/bro/SKILL.md) は直前のメッセージを、人間同士の話し方に言い直します。専門用語なし、短く。技術的には綿密な返事なのに、何と言ったか分からないときに使ってください。

## 落とし穴

- **プロンプトでスキルを列挙する。** 「use /how then /architect then /arena」は、プレイブックがすでに並べたステップを並べ替えます。ゴールと制約を述べてください。スキル名は既定を上書きするときだけ。
- **曖昧な完了条件。** 「make it better」は `/loop` に確認するものを与えません。合格か不合格かが付くコマンドか成果物を渡してください。
- **ひとつのワークツリーに並列エージェント。** 上書きし合い、差分が考古学になります。「own worktree per attempt」と言えば隔離は無料です。
- **カバレッジに `/arena` を使う。** `/arena` は同じ設計またはコードのブリーフを繰り返し、ベースを選んで良い部分を接ぎ木します。`/swarm` はスライスや宣言したレースの腕を区画し、報告を 1 つに集約します。
- **レビューコメントを全部受け入れる。** ボットも人間も、本物の指摘とノイズを同じリストに出します。`/interrogate` は指摘を act-on と dismissed に理由付きで分け、どちらも上書きできます。
- **`auto` をモデルスラッグとして扱う。** `auto` と `inherit-parent` は「model フィールドを省略し、サブエージェントが親チャットのモデルを継承する」という意味です。役割は [セットアップ](./01-setup.md) を見てください。
- **緑のビルドで成功を報告する。** ビルドはコンパイルできたことの証明です。本物のコマンド、フロー、保存された値、プロファイルを求め、返事に証拠があることを期待してください。
- **`SKILL.md` を手書きする。** [Authoring or modifying a skill プレイブック](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/authoring-a-skill.md) に通して、検証とレビューが起きるようにしてください。

ガイドはここまでです。飛ばして読んだなら、[セットアップ](./01-setup.md) に戻って本物のタスクを 1 つ走らせてください。習慣は読むことではなく使うことから身につきます。

[ガイド目次](./README.md) に戻る。
