# Intent/Memory の読み方

Linux の CLI と Python から、関連する atom を最大 N 件引く手順。iOS は対象外。GitHub の LOCK コメント URL は別ソースのまま使う。

表は [schema.sql](./schema.sql)。呼び出しの述語は [contract.py](../../scripts/intent_memory/contract.py)。なぜこの形かは [ADR 0001](../decisions/0001-intent-memory-postgres-pgvector.md)。専用 Postgres の起動は [postgres.md](./postgres.md) である。

`source` は毎回必須。人間向けに読むときは `human` を渡す。Planner / PdM / 監視は actor で再フィルタしない。`source=human`（Python は `Source.HUMAN`）を渡す。

Grok Bot 本体の RecallMemory はホットパスのまま残す。このストアは overlay である。置き換えない。

Planner、監視、PdM は下の dry-run を指す。ボットローカル記憶を消さない。

## 辺（related_ids と URL）

`related_ids` は表の列である。`source_url` と任意の `github_url`（LOCK コメント）と `gb_url`（GB / ボード）は列にしない。[ADR 0002](../decisions/0002-trend-adopt-loop.md) どおり body の行に書く。

```text
source_url: https://example.com/primary
github_url: https://github.com/maplefukku/grok-bot-ops/issues/18#issuecomment-5543719022
gb_url: https://github.com/maplefukku/grok-bot-ops/issues/18
```

Python の `AtomDraft` に同名の任意フィールドを渡してよい。`append` が body へ畳む。

## CLI（fixture ファイル）

リポジトリルートで、関連する atom を最大 N 件引く:

```sh
python3 scripts/intent_memory/read.py --vector 1 0 0 0 --n 5 --fixture scripts/intent_memory/fixtures.json
```

タグだけの絞り込み:

```sh
python3 scripts/intent_memory/read.py --tags fleet lock --n 5 --fixture scripts/intent_memory/fixtures.json
```

標準出力は JSON の atom 配列。`--source` の既定は `human`。人間向けに読むときはこの既定のままにする。`--tags` はスペース区切りで AND（指定した名前がすべて付いている行）。空のタグ一覧は拒否する。本番 Postgres に繋ぐクライアントはまだ無い。ローカル確認は fixture を使う。

## Planner dry-run

Planner は GitHub LOCK を自動転記しない。live ingest もしない。fixture で `by_tags` と `similar` が人間行だけを返すことを確認する。

```sh
scripts/quiet-test.sh -- python3 scripts/intent_memory/read.py --tags fleet lock --n 5 --fixture scripts/intent_memory/fixtures.json --source human
scripts/quiet-test.sh -- python3 scripts/intent_memory/read.py --vector 1 0 0 0 --n 5 --fixture scripts/intent_memory/fixtures.json --source human
```

返る行の `source` は `human` だけである。`critique_bot` は返らない。RecallMemory は触らない。読み側は actor で再フィルタしない。`source=human` を渡す。

trend-log の写像は dry-run だけである。`append` しない。

```sh
scripts/quiet-test.sh -- python3 scripts/intent_memory/trend_log.py --dry-run --path docs/decisions/trend-log.md
```

pairing の widen と live ingest は [#18](https://github.com/maplefukku/grok-bot-ops/issues/18) の ingest LOCK のあとである。

## Python

```python
from intent_memory import Kind, Source, AtomDraft, MemoryStore

store = MemoryStore()

store.append(AtomDraft(
    kind=Kind.INTENT,
    tags=("fleet", "lock"),
    body="GitHub LOCK comment URLs stay legal SoT.",
    actor="pdm",
    embedding=(1.0, 0.0, 0.0, 0.0),
    source_url="https://github.com/maplefukku/grok-bot-ops/issues/18",
    github_url="https://github.com/maplefukku/grok-bot-ops/issues/18#issuecomment-5543719022",
))

human_rows = store.by_tags(("fleet",), source=Source.HUMAN)
near = store.similar((1.0, 0.0, 0.0, 0.0), source=Source.HUMAN, limit=5)
```

`scripts/` を `PYTHONPATH` に入れるか、同じ import 経路で読む。本番の行は schema.sql どおり Postgres に置く。このモジュールは CI 可能な契約であり、プロダクト DB ではない。

人間が `append` してよい kind は `intent`、`decision`、`belief`、`feeling`、`critique_human` である。`critique_bot` と `source=bot` の `append` は拒否する。

## Write ACL（Q2）

`append` が受け入れる人間の actor は Q2 の allowlist だけである。トークンは `pdm` と `user` である。GitHub の login や `PdM` ではない。

それ以外の actor は `WriteAclHold` を上げる。行は入れない。HITL PARK である。`seed_fixture` はこの検査を通らない。隔離用の `actor="bot"` 行は `seed_fixture` が入れる。

Planner / 監視の読みは `source=human` を渡す。actor で再フィルタしない。Planner は GitHub LOCK を自動転記しない。pairing の widen と live ingest は [#18](https://github.com/maplefukku/grok-bot-ops/issues/18) の ingest LOCK のままである。RecallMemory はホットパスのまま残す。
