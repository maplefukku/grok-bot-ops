# routine: collect-grokbot-knowhow

| 項目 | 値 |
|---|---|
| 目的 | X から Grok Bot のアップデートと活用法を集め、`docs/knowhow/` に貯める |
| 担当ボット | <専用ボット名>（メインボットには貼らない） |
| スケジュール | 1 日 1 回 |
| 出力先 | メインボットへの 1 通のダイジェスト + grok-bot-ops への追記 PR |
| 状態 | 下書き |

前提: 担当ボットに X plugin（`grokbot://app/v1/plugin/add?id=49086599`）と、このリポジトリへのアクセス。

## プロンプト本文（Grok Bot に貼るもの）

```text
Search X since your last run for:
- official Grok Bot product updates: new features, access or pricing
  changes, app releases, language support
- practical Grok Bot usage tips: routines, plugins, bot UI, automation
  patterns, cost tricks. from any author - do not limit to one person.

Classify each finding as update or tip. Keep only findings with a
concrete post link. Drop vague hype.

Send me one message: the count of posts processed, then two short lists
(updates / tips), each item one line with its link.

If there is at least one solid finding, also launch a Cursor cloud
agent on <grok-bot-ops repo> with this task:
  Read docs/knowhow/README.md and follow its rules. Add today's
  findings: updates go to docs/knowhow/updates.md (newest on top),
  tips go to the matching topic file, or a new topic file from
  docs/knowhow/_template.md if none fits. Every entry needs a source
  link, a date, and 確認: 未. Do not editorialize. Open one draft PR.
```

## 備考

- 収集専用。試して検証するのは人間か、別途立てる cloud agent の仕事。検証したらエントリの `確認` を更新する。
- [`examples/intake-x-feedback.md`](./examples/intake-x-feedback.md) は自分のプロダクトへの反応を集める routine の型見本。こちらは Grok Bot というプロダクト自体の知識を集める routine。混ぜない。
