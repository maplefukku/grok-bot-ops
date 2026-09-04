# 0002. トレンド採否を Planner の日次判断記録に置く

- ステータス: Accepted
- 日付: 2026-09-05
- Issue: [#19](https://github.com/maplefukku/grok-bot-ops/issues/19)
- LOCK: [Q1–Q7](https://github.com/maplefukku/grok-bot-ops/issues/19#issuecomment-5543826572)

## 文脈

最先端手法の投稿は Discord で止まり、リポジトリに採否が残らない。Knowhow収集の記憶は自分で ADOPT または REJECT を書いて PdM に渡す。どちらも人間がループの時計になる。判断の形が無く、監査も重複排除も [#18](https://github.com/maplefukku/grok-bot-ops/issues/18) の ingest もできない。

調査の座席は最先端手法と Knowhow収集、判断は Planner、発火は PdM と開発リーダー、日次の書き込みレーンは `ops/daily-YYYY-MM-DD` の draft PR。席は揃っている。足りないのは判断の正本と、収集ボットから決定権限を外すことである。

LOCK-COMPLETE（[Q1–Q7](https://github.com/maplefukku/grok-bot-ops/issues/19#issuecomment-5543826572)）は置き場を `docs/decisions/` と [`trend-log.md`](./trend-log.md) に固定した。周期は 1 日 1 回。終端は ADOPT と REJECT のみ。このループは #18 のマージを待たない。

## 決定

判断権限は Planner に一本化する。終端は ADOPT か REJECT の二値で、理由と route を必ず付ける。WATCH 列は置かない。保留は REJECT とし、理由に「証拠不足」と再浮上条件を書く。

判断記録は [`trend-log.md`](./trend-log.md) の「判断記録」表の 1 行である。欄は date_jst、source_bot、title、source_url、decision、理由、route、fired の順。`python3 scripts/ci.py` が decision を ADOPT または REJECT に限り、理由の非空、http(s) の source_url、正規化 source_url の一意を強制する。正規化は空白除去と末尾 `/` の削除である。先に書いた行が勝ち、後発の同じ URL はエラーである。後発の候補は既存行を Planner に知らせ、二行目は足さない。ボットは行をマージしない。

route は Planner が書く。値は skill、ADR、product-impl、ops、none。FIRE は PdM と開発リーダーのままにする。Planner は FIRE しない。実装しない。

日次の CA は当日の `ops/daily-YYYY-MM-DD` ブランチに `docs/decisions/` だけを追記する。原稿は [`routines/decide-trend-adopt.md`](../../routines/decide-trend-adopt.md)。draft PR を開き、マージしない。Phase0 では Discord へ書き戻さない。この ADR の PR は足場だけを置く。毎日の CA は回さない。

収集は最先端手法と Knowhow収集のままにする。Knowhow収集は ADOPT と REJECT を書かない。候補（title、1次 URL、fleet-actionable である理由）を Planner へ渡す。第 4 の調査ボットは立てない。CreateAgent は使わない。

[#18](https://github.com/maplefukku/grok-bot-ops/issues/18) の schema は変えない。写像表だけをこの ADR に置く。ingest は #18 の後続フェーズである。

## 結果

- ふっくーがループ内の手番を持たない。介入は draft PR のマージか拒否だけである。
- 判断は監査でき、source_url で重複排除でき、#18 が生きたら ingest できる。
- ボット判断の誤りはマージ前レビューか、再浮上後の再判断で回収する。
- `docs/decisions/` に判断台帳が増える。ADR と台帳は同じ箱に住む。

## intent_atom 写像

Phase0 の [`schema.sql`](../intent-memory/schema.sql) に URL 列は無い。判断行は次の `intent_atom` に 1 対 1 で写す。ingest コードはこの ADR では書かない。

| 判断記録 | intent_atom |
|---|---|
| （固定） | kind = `decision` |
| （固定） | source = `bot` |
| （固定） | actor = `bot:Planner` |
| （固定） | tags に `trend-adopt`、`decision:ADOPT` または `decision:REJECT`、`route:<値>`、`source_bot:<名前>` |
| 理由 | body |
| source_url | body の `source_url:` 行。列は足さない |
| date_jst | created_at |
| fired | body の `fired:` 行。related_ids は後で |
| （固定） | expires_at = null |

## 却下した案

- 判断を knowhow エントリに書く。憲章は Grok Bot のノウハウであり、一般トレンドの採否は箱違いである。
- 常設 issue にコメントで積む。監査と CI の対象にならない。
- #18 のストア稼働まで待つ。LOCK は待たないと決めた。
- WATCH 列と TTL。終端が二値でなくなり、TTL 機構が要る。
- route を PdM が書く。plan.only の範囲で Planner が書き、FIRE 権限は動かさない。
- 同じ source_url をボットがマージする。先勝ちとし、後発は既存行へリンクする。
- Phase0 で Discord へ書き戻す。community voice を保つ。
- 第 4 の調査ボット。席は既にある。
- Planner が FIRE する、または実装する。
