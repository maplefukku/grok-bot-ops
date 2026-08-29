# routine: intake-slack-bugs

| 項目 | 値 |
|---|---|
| 目的 | Slack のバグ報告チャンネルを耕し、工場に投げられる形に仕分ける |
| 担当ボット | <専用ボット名>（メインボットには貼らない） |
| スケジュール | 1 時間ごと |
| 出力先 | メインボットへの 1 通の要約報告 |
| 状態 | 下書き |

## プロンプト本文（Grok Bot に貼るもの）

```text
Check <#channel> for new top-level reports since your last run.

For each new report:
- classify it: bug / performance / feature request / question / noise
- for a bug or performance report, extract: symptom in one line, repro
  steps if stated, affected product (match against my products list),
  and a link to the thread
- do not reply in the channel. do not attempt any fix.

Send me exactly one message: a table of new items with classification
and product, the count of items processed, and a short "ready for the
factory" list of bugs that have a symptom and a product identified.
If there are no new reports, say so in one line.
```

## 備考

- 仕分けの先、つまりスレッドへの返信・チケット化・再現・修正までやらせたくなったら、それは routine ではなく **プロダクトリポジトリに benny を入れる** 話。[pstack/automations/benny](https://github.com/cursor/plugins/tree/main/pstack/automations/benny) を対象リポジトリの `.cursor/automations/benny/` にマージする。
- 「ready for the factory」に挙がったものを、人間かメインボットが cloud agent（`/poteto-mode`）へ投げる。
