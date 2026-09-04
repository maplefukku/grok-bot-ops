# 0001. Intent/Memory を専用 Postgres + pgvector に置く

- ステータス: Accepted
- 日付: 2026-09-04
- Issue: [#18](https://github.com/maplefukku/grok-bot-ops/issues/18)

## 文脈

艦隊の Planner、監視、PdM、CLI は、人間の intent・決定・信念・感情・失敗の批判を横断して引きたい。GitHub の LOCK コメント URL は法的・仕様の正本のまま残す。このリポジトリにデータベースは無く、CI は `python3 scripts/ci.py` だけである。Postgres サービスも OpenAI キーも無い。

LOCK-COMPLETE（[Q1–Q5](https://github.com/maplefukku/grok-bot-ops/issues/18#issuecomment-5543719022)）はホストを専用 Postgres + [pgvector](https://github.com/pgvector/pgvector) に固定した。OSS AMEND の [agentcairn](https://github.com/ccf/agentcairn) は later overlay に限る（[cite](https://github.com/maplefukku/grok-bot-ops/issues/18#issuecomment-5543654126)）。

## 決定

専用 Postgres にテーブル `intent_atom` を 1 つ置く。拡張は `CREATE EXTENSION vector`。近傍は cosine 距離演算子 `<=>`（[pgvector](https://github.com/pgvector/pgvector)）。

`source` は独自列（`human` | `bot`）にする。kind から導出しない。のちに bot が belief を書いたとき、列が無いと人間クエリに混ざる。

埋め込みの既定は OpenAI `text-embedding-3-small`、1536 次元。出典は [Embeddings guide](https://developers.openai.com/api/docs/guides/embeddings)。CI は fixture ベクトルだけを使い、ネットワークも SDK も呼ばない。

feeling の TTL 既定は 90 日。LOCK は TTL を要求し、日数は言わなかった。`critique_human` は `expires_at` を持たず、期限切れしない。

Phase0 の ingest は人間だけ。`critique_bot` は schema に予約し、`append` は拒否する。隔離テスト用の bot 行は `seed_fixture` だけが入れる。

このリポジトリの CI で隔離を証明する契約は、Postgres を起動しないインメモリの `MemoryStore` である。同じ述語を [`schema.sql`](../intent-memory/schema.sql) の CHECK と任意の SQL 関数に書く。関数は Phase0 の CI では走らせない。

オーバーレイは GitHub LOCK URL を置き換えない。感情を ZuruNote / sauna / gakuse などのプロダクト DB に置かない。pstack を vendoring しない。

読み方は [`read-recipe.md`](../intent-memory/read-recipe.md)（Linux CLI。iOS は対象外）。

## 結果

- 人間の `by_tags` と `similar` は、タグやベクトルが一致しても bot 行を返さない。
- Python の読みは毎回 `source` を渡す。全ソース一括のフラグは置かない。CLI の既定は `human`。
- `by_tags` は空のタグ一覧を拒否する。忘れによる全件取得を防ぐ。
- 本番行は Postgres。このリポジトリのテストは fixture と stdlib unittest。

## 却下した案

- SQL 関数だけを契約にする。この CI に Postgres が無いので、隔離は skip になり証明にならない。
- agentcairn / DuckDB を Phase0 の正本にする。LOCK は later overlay。
- テーブルを 2 つに分ける。Issue は kind 付きの `intent_atom` 1 つ。
- `source` を kind から導出する。列と CHECK が不変条件。
- 読みの `source` を省略可能（ALL）にする。忘れが bot 行の漏洩になる。
