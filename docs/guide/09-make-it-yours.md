# 自分のものにする

poteto-mode は一人の流儀です。その下にある機械（プレイブック、ルーティング、モデル役割）は、あなたの流儀を着ても同じように動きます。このページでは、個人モードの生成、セッションからの教訓の取り込み、焦点の定まったスキルの執筆、信頼する前のスキル変更の試し方を扱います。

## `/automate-me` で自分のモードを生成する

```text
/automate-me
```

流儀は自分で説明しません。[`/automate-me`](https://github.com/cursor/plugins/blob/main/pstack/skills/automate-me/SKILL.md) が履歴から読み出します。アクティブなワークスペースの最近のトランスクリプトから、返事、委任、検証、コード、散文、プロセスについての繰り返しの好みを掘り、どれが本当の自分か尋ねます。Cursor 組み込みの `create-skill` フローで `.cursor/skills/<your-name>-mode/SKILL.md` の下書きを作り、[`/unslop`](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md) を通し、ワークツリーから PR を開くので、ほかの変更と同じようにレビューできます。

習慣がずれたら、もう一度:

```text
/automate-me update my mode skill with everything since its last edit
```

更新モードは、スキルが最後に変わってからの履歴だけを掘ります。矛盾していない規則は残し、新しい証拠があるものを直し、本当に新しいパターンにだけ節を足します。

## `/reflect` でセッションの教訓を取り込む

何か教えてくれたタスクの直後に:

```text
/reflect that took way too long. capture what we learned so the next run doesn't repeat it.
```

[`/reflect`](https://github.com/cursor/plugins/blob/main/pstack/skills/reflect/SKILL.md) はトランスクリプトを 3 体の並列レビューアに送り、合成役が提案を `Accepted`、`Rejected`、`Backlog` に分け、スキルを変える前にあなたの承認を待ちます。将来の判断を変える提案だけ承認してください。奇妙なセッション 1 回は逸話であり、規則ではありません。

## 焦点の定まったスキルを書く

取り込みたいワークフローがすでに分かっているとき:

```text
/poteto-mode write a skill for verifying database migrations in this repo
```

スキルを書く仕事は [Authoring or modifying a skill プレイブック](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/authoring-a-skill.md) に当たります。Cursor 組み込みの `create-skill` を通り、フロントマターとリンクを検証し、Opening a PR プレイブックで出荷します。エージェント向けの散文は、人間向けより高い基準が求められます。役に立たない文が、将来のエージェントが従う指示になるからです。`SKILL.md` を手書きせず、その基準はプレイブックに持たせてください。

特別なケースには専用の生成器があります。アプリを操作して振る舞いを証明しなければならないスキルは検証スキルなので、[`/create-verification-skill`](https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/SKILL.md) と [`/maintain-verification-skill`](https://github.com/cursor/plugins/blob/main/pstack/skills/maintain-verification-skill/SKILL.md) を使ってください。両方は [検証して出荷する](./06-verify-and-ship.md#プロジェクト用の検証スキルを作る) で扱います。

## `/technical-writing` でドキュメントを基準に書く

出荷する散文はスキルだけではありません。ドキュメント、RFC、readme、PR 説明、コミットメッセージには:

```text
/technical-writing review the readme changes
```

[`/technical-writing`](https://github.com/cursor/plugins/blob/main/pstack/skills/technical-writing/SKILL.md) は層になった基準を適用します。目標はひとつ、疲れたエンジニアが一度読んで分かる散文です。先に文書のモード（チュートリアル、ハウツー、リファレンス、説明）を選び、文ごとに進めます。誰が何をするか、一文一思考、二通りに読めるものを残さない。自分やエージェントが書いた直後のレビューにも、ドキュメントを頼むときに最初から名指しするのにも使えます。

## スキル変更は目隠しで試す

スキル編集は将来の全セッションに効くので、実験として試してください:

```text
/poteto-mode run the eval playbook on this skill change. same task for both variants, candidates stay blind.
```

[Eval プレイブック](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/eval.md) は、ひとつの失敗モード、観察者効果の周りに組まれています。評価されていると知っているエージェントは違う動きをします。だから候補エージェントは、サニタイズしたディレクトリで自然に見える仕事を受け、「eval」も「candidate」も、互いの存在も知りません。ジャッジが中立ラベルの下ですべての出力を採点し、参照の連鎖を辿れたかどうかは、実際にどのファイルを読んだかで採点されます。主張ではなくファイルです。

評決を受け入れる前に、出力は自分ですべて読んでください。ジャッジに反対なら、自分の判断より先にルーブリックを疑ってください。

**落とし穴:** スキルがおかしいからといって、タスクの途中で編集しないこと。別 PR で直し、タスクは前へ進めてください。機能作業に絡めて出荷されたスキル編集は、レビューから見えず、評価もできません。

次: [レシピと落とし穴](./10-recipes-and-pitfalls.md)。
