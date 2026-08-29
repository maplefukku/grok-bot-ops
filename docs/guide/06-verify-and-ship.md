# 結果を検証して PR を開く

「コンパイルできた」は証拠ではありません。[Prove It Works 原則](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-prove-it-works/SKILL.md) は、成功を報告する前に本物の成果物を確認させます。あなたの仕事は、「本物の成果物」を確認可能にすることです。このページでは、完了条件の書き方、アプリ用の検証スキルの生成、PR を開くこと、マージ可能な状態まで運ぶことを扱います。

![A prototype plane flies a real test course while she times it with a stopwatch and robots film and checklist the run; the terminal reads verify: pass, evidence: captured.](./images/verification.jpg)

## 完了条件を最初に書く

終わった意味を、最初のプロンプトに、合う言葉で入れてください:

```text
/poteto-mode add json output to this command. text output stays byte-identical, the json parses, both run against the sample project. show me the evidence.
```

これでエージェントは満たすべき気分ではなく、実行できる確認を 3 つ持ちます。返事には、使ったコマンドと出力そのものが載るべきです。確認が走れなかったなら、良い返事は "inconclusive" と言います。証拠無しの自信ある返事は赤旗として扱ってください。

確認は変更に合わせてください:

- CLI の変更は本物のコマンドを走らせる。
- UI の変更は、動いているアプリで変わったフローを歩く。
- パーサやマイグレーションは保存した入力を再生する。
- perf の変更は前後のプロファイルを比べる。
- ストレージの変更は書いた値を読み戻す。

小さくて完全には信じていない差分には、[`/blast-radius`](https://github.com/cursor/plugins/blob/main/pstack/skills/blast-radius/SKILL.md) がほかで壊れうるものを探します。その変更が安全である根拠になっている事実をひとつ選び、エッセイではなくコードを走らせて証明します。

## プロジェクト用の検証スキルを作る

上の UI の箇条書きは、本物の要件を隠しています。エージェントには、アプリを動かすスクリプトされた手段が要ります。プロジェクトにそれがあるなら十分です。無ければ:

```text
/create-verification-skill
```

[`/create-verification-skill`](https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/SKILL.md) がインタビューするのはあなたではなくリポジトリです。ユーザーが触るもの、ローカルでの起動方法、動かせる手段（既存ハーネスが先、無ければブラウザと CDP、PTY、素の HTTP）、振る舞いを証明する証拠、2 インスタンスを並べて走らせられるか、を組み立てます。コードが答えられないことだけ、あなたに聞きます。

書く先は `.cursor/skills/verify-<app>/` です。エージェント向けの手順で、Launch、Doctor、Drive、Evidence、Cleanup の各節を正確に備え、加えて `features/` の下にフィーチャーマップがあります。アプリが何をするか、各機能が動いたと証明する結果は何か、の索引です。スキルには [完成したフィーチャーマップの例](https://github.com/cursor/plugins/tree/main/pstack/skills/create-verification-skill/references/feature-map-example/) が付きます。README の索引と、必須の H2 が 4 つある機能ごとのファイルです。引き渡す前に、生成器はスキルを一度エンドツーエンドで証明します。起動、doctor 確認、機能をひとつ操作、証拠を取る、掃除。その証明が失敗したら、出力を使わないでください。

以降、「アプリで検証して」は、セットアップの会話無しで、このリポジトリのどのエージェントでも実行できるステップになります。

検証スキルが動くようになったら、[`/swarm`](https://github.com/cursor/plugins/blob/main/pstack/skills/swarm/SKILL.md) がフィーチャーマップの項目単位で全体の検証パス（一巡）を分割し、結果を集約できます。

## 検証スキルを正直に保つ

アプリは変わり、フィーチャーマップは腐ります。ずれたら:

```text
/maintain-verification-skill
```

[`/maintain-verification-skill`](https://github.com/cursor/plugins/blob/main/pstack/skills/maintain-verification-skill/SKILL.md) は生成したスキルを監査します。機能ごとに読み取り専用のソースリーダーを並列で 1 体、そのあとマップされた全機能を操作するライブパスです。結末は必ず次の 3 つのいずれかひとつです。`clean` はカバレッジが足りて出荷するものが無い。`changed` は、検証スキル自身のディレクトリに閉じた、証明済み修正の PR が 1 本。`blocked` はブロッカーを名指します。プロダクトコードは編集しません。ライブパスがプロダクトの回帰を捕まえたら、ドキュメントで上塗りせず、回帰として報告します。

## PR を開く

```text
/poteto-mode open the pr. small ordered commits, evidence in the description.
```

[Opening a PR プレイブック](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/opening-a-pr.md) はワークツリーから動き、作業を小さく順序の付いたコミットにリベースし、差分を掃除し、散文のスロップを取り、PR リンクを返します。太い 1 本より狭い 5 本、膨らむブランチよりスタックしたフォローアップです。

## Babysit で PR をマージ可能な状態まで運ぶ

開いた PR は、すぐブロッカーを集め始めます。チェック失敗、レビューコメント、トランクの前進。その消耗は [Babysit プレイブック](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/babysit.md) に渡してください:

```text
/poteto-mode babysit this pr. get it green.
```

Babysit は付属のウォッチャーで PR を見守り、ブロッカーを順に取ります。コンフリクト、レビュースレッド、CI。既知の修正は 1 回の push にまとめ、チェックが修正のたびに再起動しないようにします。コメントの仕分けは懐疑的です。人間もボットも、本物の指摘とノイズを同じリストに出すからです。本物は直し、ノイズは反証をスレッドに書いて却下します。状態だけ欲しいときは小さく聞き、Babysit はループを始めずに答えます:

```text
/poteto-mode check on pr 123. anything outstanding?
```

Babysit はマージ可能な状態で止まります。全部緑でもマージしません。マージは別の判断だからです。

## Shipping でスタックを着陸させる

緑は安全と同じではありません。着陸する準備ができたら、そう言ってください:

```text
/poteto-mode land the stack.
```

[Shipping プレイブック](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/shipping.md) は、マージを仕掛ける前に各 PR を独立に検証します。PR ごとに新しいエージェントがライブで振る舞いを証明し、変更を書いたエージェントはそれを判定しません。そのあと Shipping は、底から連続した検証済みの区間だけを、Graphite の merge-when-ready で着陸させ、鎖を切った最初の PR を報告します。未検証の上に載っている検証済み PR は待ちます。マージすると隙間を下に引き込むからです。

次: [寝ているあいだに回す](./07-overnight.md)。
