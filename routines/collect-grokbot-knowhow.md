# routine: collect-grokbot-knowhow

| 項目 | 値 |
|---|---|
| 目的 | X から Grok Bot のアップデートと活用法を集め、`docs/knowhow/` に貯める |
| 担当ボット | <専用ボット名>（メインボットには貼らない） |
| スケジュール | 1 日 1 回 |
| 出力先 | メインボットへの 1 通のダイジェスト + grok-bot-ops への追記 PR |
| 状態 | 下書き |

前提: 担当ボットに X plugin（`grokbot://app/v1/plugin/add?id=49086599`）と、このリポジトリへのアクセス。

## 書き込み先（これ以外は禁止）

この routine が開く PR が触ってよいのは次だけ。

- `docs/knowhow/`（エントリ追記、必要なら `_template.md` からのトピック新設、`.last-collect` の日付更新）
- `routines/`（収集の結果、原稿の追記が必要になったときだけ）

プロダクトコード、`skills/`、`docs/guide/`、各プロダクトリポジトリ、検証スキル本体は触らない。

## since last run

前回実行日は [`docs/knowhow/.last-collect`](../docs/knowhow/.last-collect) の 1 行。

- 値が `never` なら、公式出典付きで残せるものだけを拾う（全期間を漁らない。直近数日で足りる）
- 値が `YYYY-MM-DD` なら、その日以降を対象にする
- 実行の最後（発見が 0 件でも）に、その日の UTC 日付を `.last-collect` へ書き、同じ PR に含める。発見が無く PR を開かないなら、日付だけ更新する小さな PR を開く

## プロンプト本文（Grok Bot に貼るもの）

```text
Read https://github.com/maplefukku/grok-bot-ops/blob/main/docs/knowhow/.last-collect
for the since-last-run date (`never` or YYYY-MM-DD).

Search X since that date for:
- official Grok Bot product updates: new features, access or pricing
  changes, app releases, language support
- practical Grok Bot usage tips: routines, plugins, bot UI, automation
  patterns, cost tricks. from any author - do not limit to one person.

Classify each finding as update or tip. Keep only findings with a
concrete post link or another official http(s) URL (docs.x.ai, x.ai/news,
x.ai/bot/..., Play Store, pstack GitHub). Drop vague hype. Do not invent
links.

Send me one message: the count of posts processed, then two short lists
(updates / tips), each item one line with its link.

Launch a Cursor cloud agent on https://github.com/maplefukku/grok-bot-ops
with this task:
  Read docs/knowhow/README.md and follow its rules. Add today's
  findings: updates go to docs/knowhow/updates.md (newest on top),
  tips go to the matching topic file, or a new topic file from
  docs/knowhow/_template.md if none fits. Every entry needs a source
  http(s) URL, a date, and 確認: 未. Do not editorialize. Never write
  リンク要補完. Write only under docs/knowhow/ and, if a routine
  manuscript itself must change, routines/. No product code.
  Set docs/knowhow/.last-collect to today's UTC date (YYYY-MM-DD).
  Open one draft PR. Do not merge.
```

## 備考

- 収集専用。試して検証するのは人間か、別途立てる cloud agent の仕事。検証したらエントリの `確認` を更新する。
- [`examples/intake-x-feedback.md`](./examples/intake-x-feedback.md) は自分のプロダクトへの反応を集める routine の型見本。こちらは Grok Bot というプロダクト自体の知識を集める routine。混ぜない。
- draft PR のマージは人間。ボットは draft のまま。ルールは [`AGENTS.md`](../AGENTS.md) の「draft PR のマージ」。

### 手動 1 周チェックリスト（未実施）

この原稿を Grok Bot に貼って 1 周回した記録はまだ無い。嘘の「確認済」は書かない。

- [ ] 担当ボットを作り、https://github.com/maplefukku/grok-bot-ops への書き込み権限を付けた
- [ ] X plugin を入れた
- [ ] Cursor cloud agent をこのリポジトリで起動できる
- [ ] 実際に draft PR が開く
- [ ] マージ担当は人間（オーナー）。毎日 draft を見る。ボットはマージしない
