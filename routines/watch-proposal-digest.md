# routine: watch-proposal-digest

| 項目 | 値 |
|---|---|
| 目的 | 週次で Intent/Memory の human 読みと stall 状況から proposal digest を 1 通出す。実装も PR も Guardian の実行もしない |
| 担当ボット | 監視 |
| スケジュール | Mon 10:00 JST: `0 10 * * 1`. 15 分間隔は禁止 |
| 出力先 | PdM への proposal digest 1 通 |
| 状態 | LIVE |

前提: 担当ボットにこのリポジトリへの読み取り。書き込み PR は開かない。

## 書き込み先（これ以外は禁止）

この routine は PR を開かない。ファイルも直さない。出すものは PdM への 1 通だけである。

## プロンプト本文（Grok Bot に貼るもの）

```text
Weekly proposal digest only. Do not open a PR. Do not merge.
Do not implement. Do not CreateAgent. Do not execute Guardian
actions. Guardian stays proposal-only.

Read docs/intent-memory/read-recipe.md. Keep Grok Bot
RecallMemory as the local hot path. Do not replace it.

If you need to query atoms, dry-run the fixture CLI from
the recipe (by_tags / similar, --source human). Never append
critique_bot. Never ingest trend-log rows.

Send PdM one message: item count, then a short proposal
list (stalls, human intent atoms worth a human look, and
no-action items). Each item is a proposal. No auto-PR.
No FIRE. No code change.
```

## 備考

- 正本の読みは [`docs/intent-memory/read-recipe.md`](../docs/intent-memory/read-recipe.md) である。
- 週次 digest は既存の監視 routine `guardian-phase0-propose` の Mon `0 10 * * 1` に折り込む。スロットは 1 つ。ボットも routine も増やさない。
- 平日 06-22 の 2 時間おき stall sweep は変えない。これは週次の提案だけを厚くする。
- [#18](https://github.com/maplefukku/grok-bot-ops/issues/18) の overlay である。Neo4j / Mem0 / Graphiti / LightRAG / agentcairn UI は対象外。
- draft PR のマージ規則は関係しない。この原稿は PR を作らない。
