# routine: intake-x-feedback

| 項目 | 値 |
|---|---|
| 目的 | X 上の苦情・要望・アイデアを集め、次の開発テーマの材料にする |
| 担当ボット | <専用ボット名>（メインボットには貼らない） |
| スケジュール | 1 日 2〜3 回 |
| 出力先 | メインボットへの 1 通の要約報告 |
| 状態 | 下書き |

前提: 担当ボットに X plugin を入れておく（`grokbot://app/v1/plugin/add?id=49086599`）。

## プロンプト本文（Grok Bot に貼るもの）

```text
Search X for recent posts mentioning <product names / handles / keywords>
since your last run.

Classify each relevant post: complaint / feature idea / praise / question.
For complaints and ideas, extract the underlying need in one line and
note which product it maps to.

Send me exactly one message: the count of posts processed, top 3
complaints by frequency, top 3 feature ideas worth considering, each
with links. Skip praise unless something is notably resonating.
Do not reply to any post.
```

## 備考

- 収集専用。ポストへの返信はさせない。
- ここで挙がったテーマを工場に投げるかどうかは、メインボットとの会話（チーフ・オブ・スタッフ）で決める。
