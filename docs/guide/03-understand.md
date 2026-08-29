# 変える前にコードを理解する

理解していないコードを編集すると、見えにくい回帰が出荷されます。pstack には入り口が 4 つあります。`/how` は今のコードが何をするかを説明します。`/why` は、その形になった理由を掘ります。`/teach` は両方をひとつの説明に編みます。`/recall` は、ある話題についての自分の最近の文脈を組み立て直します。

![A detective studies a machine blueprint with a magnifying glass while robots fetch case files; the evidence board behind her links clues under /how and /why.](./images/understanding.jpg)

## `/how` で振る舞いを追う

```text
/how do we dedupe notifications? is there an n+1 when we look up subscribers?
```

本当に持っている質問を聞いてください。[`/how`](https://github.com/cursor/plugins/blob/main/pstack/skills/how/SKILL.md) はコードを読み、シニアエンジニアがあなたをそのサブシステムにオンボーディングするときの水準で答えます。実行時の流れ、鍵になる型、自明でないところです。大きなサブシステムでは、先に読み取り専用の探索者を 2〜4 体に広げます。狭い質問なら、読んで説明するだけです。

`/how` は設計にも反論できます。構造そのものを疑うときは Critique モードを頼んでください:

```text
/how explain the sync service, then critique its ownership boundaries
```

説明が先に来るので、批判は実際の動きに根ざしたままです。

## `/why` で履歴を掘る

```text
/why was the retry limit set to five? does the reason still hold?
```

[`/why`](https://github.com/cursor/plugins/blob/main/pstack/skills/why/SKILL.md) は未解決事件の探偵のように動きます。ソース管理から始め、MCP が露出している証拠カテゴリ（イシュートラッカー、長文ドキュメント、チームチャット、オブザーバビリティ、エラー追跡、アナリティクスなど）を並列で問い合わせます。報告はすべて引用し、直接証拠と推論を分け、記録が薄いところは "appears to" と書きます。何も出なくても報告します。「誰も理由を書いていない」こと自体が答えだからです。

ふたつは自然に組めます。履歴が混乱の説明だと疑うなら、`do why first then how` は十分よいプロンプトです。

## `/teach` で本当に理解する

```text
/teach me how this PR changes retries. convince me it fixes the cause and not the symptom.
```

[`/teach`](https://github.com/cursor/plugins/blob/main/pstack/skills/teach/SKILL.md) は、要約では足りないとき用です。`/how` と `/why` を走らせ（小さな変更なら片方だけ）、見つけたものを図を積み上げながら平易な説明に編みます。「convince me」という枠は盗む価値があります。説明がツアーではなく、つつける議論になります。

## `/recall` で自分の文脈を組み立て直す

```text
/recall catch me up on the export work from last week
```

[`/recall`](https://github.com/cursor/plugins/blob/main/pstack/skills/recall/SKILL.md) は、自分の最近のチャットと共有記録（イシュー、以前の修正、まだ発火しているエラー）を掘り、現状と次の一手をブリーフにして返します。話題に冷えた状態で戻るときに使ってください。特定のチャットを再開したいなら、下の Session pickup プレイブックであり、`/recall` ではありません。

## Session pickup で途中の仕事を引き継ぐ

別のエージェント（または先週の自分）がブランチを途中で置いていったとき:

```text
/poteto-mode take over this branch. read the decision log, figure out what's done, and continue from there. don't redo finished work.
```

[Session pickup プレイブック](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/session-pickup.md) は、先行の軌跡を権威として扱います。ブランチの状態と判断を再構成し、再開点を名付け、ゼロから全部を再導出せずに、継承した主張を元のゴールに照らして検証します。

**落とし穴:** 「どうせエージェントがコードを読む」と、このページのスキルを飛ばさないこと。動作を追跡して得た理解（メンタルモデル）を持たずに編集を始めるエージェントは、最初のもっともらしい場所で症状を直しがちです。二度目のバグより、先に `/how` するほうが安いです。

次: [変更を設計する](./04-design.md)。
