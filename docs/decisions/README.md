# docs/decisions/

このリポジトリの Architecture Decision Records。番号は採択順。

日次の採否は [`trend-log.md`](./trend-log.md) に残す。Planner の台帳である。

読みの手順は [`docs/intent-memory/read-recipe.md`](../intent-memory/read-recipe.md)。表と制約は [`schema.sql`](../intent-memory/schema.sql)。Python の同じ述語は [`scripts/intent_memory/contract.py`](../../scripts/intent_memory/contract.py)。

| 番号 | 題 | 状態 |
|---|---|---|
| 0001 | [Intent/Memory を専用 Postgres + pgvector に置く](./0001-intent-memory-postgres-pgvector.md) | Accepted |
| 0002 | [トレンド採否を Planner の日次判断記録に置く](./0002-trend-adopt-loop.md) | Accepted |
| 0003 | [ドメイン単位で出荷量を管理する](./0003-domain-unit-throughput.md) | Accepted |
