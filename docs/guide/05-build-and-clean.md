# 変更を作って差分をきれいにする

ビルド用プレイブックは、ひとつの規律を共有します。観察したことを言い、証拠はプレイブックに要求させる。このページでは、よくあるビルド作業ごとにプロンプトへ何を書くか、そしてレビュー可能な差分を保つ掃除の癖を示します。

## 分かっていることを、各ビルドプレイブックに渡す

バグのプロンプトは症状を述べ、先に再現を求めます:

```text
/poteto-mode this command emits two records after a retry. repro first, then fix and verify.
```

機能のプロンプトは振る舞いと、変えてはいけないものを述べます:

```text
/poteto-mode add a --json flag. text output stays byte-identical. verify both forms.
```

リファクタのプロンプトは、構造を動かす前に振る舞いを固定します:

```text
/poteto-mode move parsing into one module, zero behavior change. record the current output first and prove it's unchanged after.
```

perf のプロンプトは雰囲気ではなく測定を述べます:

```text
/poteto-mode startup takes 1.8s on this fixture. trace it, fix the measured cause, show me before and after.
```

どれもそれぞれのプレイブック（[Bug fix](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/bug-fix.md)、[Feature](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/feature.md)、[Refactoring](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/refactoring.md)、[Perf issue](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/perf-issue.md)）に流れ、打たなかった手順をプレイブックが補います。直す前に再現する、実装前にデータ形を名付ける、構造を動かす前に振る舞いを固定する、最適化の前にプロファイルする。

ひとつの数字を持続的に上げるなら [Hillclimb プレイブック](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/hillclimb.md) があります。メトリクス、目標、試行の下限を渡すと、測定ハーネスを固定したまま仮説をひとつずつ回します。勝ちは残し、それ以外は全部戻します。

## `/tdd` で失敗するテストを先に書く

バグに安いローカルテスト経路があるなら、プロンプト全体が二語で足ります:

```text
/tdd implement
```

文脈があれば、それで十分です。[`/tdd`](https://github.com/cursor/plugins/blob/main/pstack/skills/tdd/SKILL.md) は、意図した理由で失敗する最小のテストを書き、直して、テストを再実行します。テストに広いハーネスや脆いモックが要るなら、スキルはそう言い、いちばん近い実行可能な確認に切り替えます。本物のコマンドのほうが強い証拠になる場所で、テストを強制しないでください。

## TypeScript のルールは自動で読み込まれる

[`typescript-best-practices`](https://github.com/cursor/plugins/blob/main/pstack/skills/typescript-best-practices/SKILL.md) に、ワークフロー上のスラッシュコマンドはありません。エージェントが `.ts` か `.tsx` に触ると自動で読み込まれ、型システムの原則を具体ルールにします。判別可能なユニオン、境界での `unknown`、網羅的なバリアント、スキーマ由来の型です。

## コミットする前にきれいにする

[Opening a PR プレイブック](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/opening-a-pr.md) は、各コミットの前に差分へ `/deslop` をかけ、PR 説明とコミット本文へ [`/unslop`](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md) をかけます。`/deslop` は pstack ではなく `cursor-team-kit` プラグインに入っています。無ければ、同じ結果を平易な言葉で頼んでください。物語るコメント、根拠のないガード、死んだ互換パス、無関係な編集を取り除く、と。

散文には、対象と追加ルールを `/unslop` に渡します:

```text
/unslop the readme changes, no emdashes
```

自分なりの短い言い回しは自然と育ちます。スキルは `unslop that, tighten it` のような短いプロンプトから意図を十分読みます。

## `/no-comments` でコメントを剥がす

コメントは別パスが要ります。書いたエージェント自身からではありません。作者は自分のコメントを、あなたが自分のコメントを弁護するのと同じように弁護します。だからレビュー前に、新しい目に渡します:

```text
/no-comments the diff
```

[`/no-comments`](https://github.com/cursor/plugins/blob/main/pstack/skills/no-comments/SKILL.md) は [Comment Sicko](https://github.com/cursor/plugins/blob/main/pstack/agents/comment-sicko.md) を立ち上げます。読み取り専用のレビューアで、残すリストは短いです。ライセンスヘッダ、公開 API のドキュメントコメント、コードでは言えない説明へのリンク、形を変えられない外部依存が強制する振る舞い。それ以外は消えます。自分のコードでの驚きは、その免罪符がありません。コメントはリファクタのフラグとして戻り、`/no-comments` は受け入れたフラグを根本原因で直します。コメントが制約を主張し、「消すな」と言うなら、スキルはその主張を型、テスト、lint にエンコードすることを提案します。どちらにせよ、コメントは取り除かれます。

分業ははっきりさせておいてください。`/deslop` はコードからスロップを掃除し、`/unslop` は散文から掃除し、`/no-comments` は書いていないレビューアにコメントを渡します。

**落とし穴:** 掃除は任意の磨きではありません。物語るコメントと防御的な死にコードがある差分は、レビューアには未完成に見え、次のバグはその余分なコードに潜みます。差分が膨らんでいると感じたら、レビューで指摘される前に `deslop it` と言ってください。

次: [検証して出荷する](./06-verify-and-ship.md)。
