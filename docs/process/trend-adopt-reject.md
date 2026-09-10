# trend-adopt REJECT（判断の終端 WRAP）

## Purpose

[issue 117](https://github.com/maplefukku/grok-bot-ops/issues/117) の WRAP である。正本は [ADR 0002](../decisions/0002-trend-adopt-loop.md) と [issue 19 LOCK Q1–Q7](https://github.com/maplefukku/grok-bot-ops/issues/19#issuecomment-5543826572) である。日常の原稿は [`routines/decide-trend-adopt.md`](../../routines/decide-trend-adopt.md) である。台帳は [`trend-log.md`](../decisions/trend-log.md) である。引用は [parallel-fire-fleet](sand-workflow:parallel-fire-fleet)、[Cloud開発](sand-workflow:cloud)、tool-path-prefer、[poteto-mode](../guide/02-poteto-mode.md) である。

このページは WRAP だけである。判断の walker は [`scripts/intent_memory/trend_log.py`](../../scripts/intent_memory/trend_log.py) である。新しい contract/ 箱は置かない。第 4 の調査ボットは CreateAgent しない。WATCH 列は invent しない。第二のチェックリストは置かない。

## 対象

Planner（判断のみ）、最先端手法、Knowhow収集（候補のみ）、PdM（ADOPT の FIRE のみ）、開発リーダー（ADOPT の FIRE のみ）である。REJECT 行に FIRE は無い。impl CA は読まない。

## 範囲

### 対象にする

終端が ADOPT または REJECT の二値であること。保留は REJECT とし、理由に「証拠不足」と再浮上条件を書くこと。`source_url` の正規化と先勝ち dedup である。Planner が route を書くこと（REJECT では多くが `none`）。日次 CA が `docs/decisions/` だけを `ops/daily-YYYY-MM-DD` に追記すること。

### 対象にしない

WATCH 列と TTL 機械。ボットによる行のマージ。Planner の FIRE と実装。Discord Phase0 書き戻し。第 4 調査ボットの CreateAgent。新しい trend-adopt harness。プロダクトコード。on-demand。

## SoT

判断記録の形は [`0002-trend-adopt-loop.md`](../decisions/0002-trend-adopt-loop.md) である。日常追記の原稿は [`decide-trend-adopt.md`](../../routines/decide-trend-adopt.md) である。行の CI は `scripts/ci.py` の `trend-log-decisions` である。dedup の純関数は [`scripts/trend_adopt_idempotency.py`](../../scripts/trend_adopt_idempotency.py) である。intent 写像の dry-run は [`trend_log.py`](../../scripts/intent_memory/trend_log.py) である。ingest は #18 の後続である。

## REJECT 終端

| 項目 | 規則 |
|---|---|
| decision | `ADOPT` または `REJECT` のみ。これ以外は CI が落とす |
| 保留 | WATCH にしない。REJECT と書く |
| 理由 | 空禁止。保留なら「証拠不足」と再浮上条件を含む |
| route | `skill`、`ADR`、`product-impl`、`ops`、`none`。REJECT で FIRE しないときは `none` が多い |
| fired | REJECT 行は空でよい。ADOPT のみ PdM が JOB/issue/PR を埋める |
| dedup | `source_url` を正規化（空白除去、末尾 `/` 削除）して一意。先勝ち。後発は行を足さない |
| merge | ボットは行をマージしない。人間が draft をマージする |

```text
保留にしたい候補
  → decision = REJECT
  → 理由 = 証拠不足: …。再浮上: …
  → route = none（多く）
  → fired = 空
  → FIRE しない。skill/ADR/product-impl は作らない
```

## 再浮上

REJECT 行の「再浮上」は期限付き WATCH ではない。条件が満たされたとき、同じ `source_url` で新しい行は足さない。Planner は既存行を知らせ、同 URL の二行目は書かない。人間がマージ前に見て、必要なら別 URL または ADR 改定で再開する。

## Planner 禁止

| 禁止 | 破る規則 |
|---|---|
| FIRE | FIRE は PdM と開発リーダー。Planner は Never FIRE |
| 実装 | Planner は Never implement |
| 行のマージ | 先勝ち dedup。後発候補は skipped |
| CreateAgent | 第 4 調査ボットは REJECT 済み。CreateAgent NONE |
| WATCH 列 | 終端は二値。WATCH は invent しない |
| knowhow へ ADOPT/REJECT | 収集ボットは候補だけ。判断は Planner |
| Discord 書き戻し | Phase0 は none |

## Domain WRAP

LOCK は GitHub Actions に依存しない。ページと [`scripts/test_trend_adopt_reject_lock.py`](../../scripts/test_trend_adopt_reject_lock.py) が持つ。証拠は `scripts/quiet-test.sh -- python3 scripts/ci.py` である。Quiet is not skip。新しい harness は置かない。入口は /poteto-mode である。

## 関連

出荷単位は [`README.md`](./README.md) である。PR 本文の 4 見出しは [`pr-body.md`](./pr-body.md) である。CI 梯子は [`ci-ladder.md`](./ci-ladder.md) である。quiet-test は [`quiet-test.md`](./quiet-test.md) である。intent 写像は [ADR 0002](../decisions/0002-trend-adopt-loop.md) である。
