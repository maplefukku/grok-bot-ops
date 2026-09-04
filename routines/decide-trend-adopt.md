# routine: decide-trend-adopt

| 項目 | 値 |
|---|---|
| 目的 | 候補を 1 日 1 回 ADOPT または REJECT し `docs/decisions/trend-log.md` に残す。実装と FIRE はしない |
| 担当ボット | Planner |
| スケジュール | 1 日 1 回 |
| 出力先 | PdM への 1 通のダイジェスト + ops/daily 上の `docs/decisions/` 追記 |
| 状態 | 下書き |

前提: 担当ボットにこのリポジトリへのアクセス。最先端手法と Knowhow収集から候補を受け取れること。

## 書き込み先（これ以外は禁止）

この routine が開く PR が触ってよいのは次だけ。

- `docs/decisions/`（通常は [`trend-log.md`](../docs/decisions/trend-log.md) の追記。ADR 自体を直すときだけ [`0002-trend-adopt-loop.md`](../docs/decisions/0002-trend-adopt-loop.md)）

`docs/knowhow/`、`bots/`、プロダクトコード、`docs/intent-memory/`、`scripts/intent_memory/` は触らない。

## プロンプト本文（Grok Bot に貼るもの）

```text
Receive 候補 from 最先端手法 and Knowhow収集. Each 候補 has a
title, a 1° http(s) URL, and why it is fleet-actionable.

Every item must be ADOPT or REJECT, with a non-empty 理由 and a
route of skill, ADR, product-impl, ops, or none. There is no WATCH.
If you would hold, write REJECT. That 理由 must contain 証拠不足
and the condition that lets the trend surface again.

Dedup by source_url. Normalize by stripping whitespace and trailing
/. If docs/decisions/trend-log.md already has that URL, do not add
a second row. Report the existing row (date_jst, decision, 理由)
and move on. Do not merge rows.

Never FIRE. Never implement. No Discord writeback.

Launch a Cursor cloud agent on https://github.com/maplefukku/grok-bot-ops
with this task:
  Read docs/decisions/trend-log.md and
  docs/decisions/0002-trend-adopt-loop.md. Append today's
  decision rows under ## 判断記録. Write only under
  docs/decisions/. Touch 0002 only if the ADR itself must
  change. No docs/knowhow/. No bots/. No product code.
  No docs/intent-memory/. Work on branch
  ops/daily-YYYY-MM-DD for today's date. Open or update
  that day's draft PR. Do not merge. Dedup by normalized
  source_url. If a row exists, do not add another.
  Never FIRE. Never implement. No Discord writeback.

Send PdM one message: the counts of ADOPT, REJECT, and skipped
duplicates, then one line per new row (title, decision, route,
source_url).
```

## 備考

- Q2 は 1 日 1 回のダイジェスト。投稿ごとの 4 回や週次にはしない。
- Q7 は Phase0 では Discord へ書き戻さない。
- [#18](https://github.com/maplefukku/grok-bot-ops/issues/18) の ingest は後続。この原稿は写像表のある ADR まで。
- `bots/` の台帳行は次の `ops/daily` に乗せる。この PR では触らない。
- draft PR のマージは人間。ボットは draft のまま。ルールは [`AGENTS.md`](../AGENTS.md) の「draft PR のマージ」。
- LOCK は [#19 のコメント](https://github.com/maplefukku/grok-bot-ops/issues/19#issuecomment-5543826572)。正本は [`0002-trend-adopt-loop.md`](../docs/decisions/0002-trend-adopt-loop.md)。

### 手動 1 周チェックリスト（未実施）

この原稿を Grok Bot に貼って 1 周回した記録はまだ無い。嘘の「確認済」は書かない。

- [ ] Planner ボットがある
- [ ] 最先端手法から候補を受け取った
- [ ] Knowhow収集から候補を受け取った
- [ ] 判断行が `docs/decisions/trend-log.md` に書かれた
- [ ] PdM が ADOPT を 1 件 FIRE した
- [ ] fired に URL を埋め戻した
- [ ] 人間が draft をマージする。ボットはマージしない
- [ ] Planner は FIRE しない。実装しない
- [ ] Discord へ書き戻さない
