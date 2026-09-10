# Intent/Memory の読み方

Linux の CLI と Python から、関連する atom を最大 N 件引く手順。iOS は対象外。GitHub の LOCK コメント URL は別ソースのまま使う。

表は [schema.sql](./schema.sql)。呼び出しの述語は [contract.py](../../scripts/intent_memory/contract.py)。なぜこの形かは [ADR 0001](../decisions/0001-intent-memory-postgres-pgvector.md)。専用 Postgres の起動は [postgres.md](./postgres.md) である。

`source` は毎回必須。`reader` も毎回必須である。人間向けに読むときは `human` を渡す。Planner / PdM / 監視は actor で再フィルタしない。`source=human`（Python は `Source.HUMAN`）を渡す。

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

標準出力は JSON の atom 配列。`--source` の既定は `human`。人間向けに読むときはこの既定のままにする。`--reader` の既定は `cli` で `human` だけ読める。bot 行を見るのは `--reader pdm` か `--reader user` である。`--tags` はスペース区切りで AND（指定した名前がすべて付いている行）。空のタグ一覧は拒否する。本番 Postgres に繋ぐクライアントはまだ無い。ローカル確認は fixture を使う。

## Planner dry-run

Planner は GitHub LOCK を自動転記しない。live ingest もしない。fixture で `by_tags` と `similar` が人間行だけを返すことを確認する。

```sh
scripts/quiet-test.sh -- python3 scripts/intent_memory/read.py --tags fleet lock --n 5 --fixture scripts/intent_memory/fixtures.json --source human --reader planner
scripts/quiet-test.sh -- python3 scripts/intent_memory/read.py --vector 1 0 0 0 --n 5 --fixture scripts/intent_memory/fixtures.json --source human --reader planner
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

human_rows = store.by_tags(("fleet",), source=Source.HUMAN, reader="planner")
near = store.similar((1.0, 0.0, 0.0, 0.0), source=Source.HUMAN, limit=5, reader="kanshi")
store.delete(human_rows[0].id, actor="pdm")
```

`scripts/` を `PYTHONPATH` に入れるか、同じ import 経路で読む。本番の行は schema.sql どおり Postgres に置く。このモジュールは CI 可能な契約であり、プロダクト DB ではない。

人間が `append` してよい kind は `intent`、`decision`、`belief`、`feeling`、`critique_human` である。`critique_bot` と `source=bot` の `append` は拒否する。

## Write ACL（Q2）

`append` が受け入れる人間の actor は Q2 の allowlist だけである。トークンは `pdm` と `user` である。GitHub の login や `PdM` ではない。

それ以外の actor は `WriteAclHold` を上げる。行は入れない。HITL PARK である。`seed_fixture` はこの検査を通らない。隔離用の `actor="bot"` 行は `seed_fixture` が入れる。

Planner / 監視の読みは `source=human` を渡す。actor で再フィルタしない。Planner は GitHub LOCK を自動転記しない。pairing の widen と live ingest は [#18](https://github.com/maplefukku/grok-bot-ops/issues/18) の ingest LOCK のままである。RecallMemory はホットパスのまま残す。

## Read ACL

`by_tags` と `similar` は毎回 `reader` を取る。`READ_ACL` の表に無い組み合わせは `ReadAclHold` を上げる。メッセージは `HITL HOLD` である。行は返さない。

| reader | 読める source |
|---|---|
| `pdm` | `human`, `bot` |
| `user` | `human`, `bot` |
| `planner` | `human` |
| `kanshi` | `human` |
| `cli` | `human` |

`planner` / `kanshi` / `cli` は `human` だけ読む。`bot` 行の読みは [#18](https://github.com/maplefukku/grok-bot-ops/issues/18) の ingest LOCK（Q3 bot↔bot critique）まで HOLD である。`pdm` / `user` は監査のため両方読める。読みの許可は書きの許可ではない。`WriteAclHold` は変わらない。SQL に reader 列も引数も無い。`p_source` のままである。ACL は Python の契約である。

## Delete ACL

`delete` は毎回 `actor` を取る。`HUMAN_DELETE_ACTORS` は Q2 の `HUMAN_WRITE_ACTORS` と同じトークンである。`pdm` と `user` だけが人間行を消せる。それ以外は `DeleteAclHold` を上げる。メッセージは `HITL PARK` である。行は残る。

`source=bot` の行は `pdm` / `user` でも消さない。`DeleteAclHold` で `HITL HOLD` である。Q3 ingest OFF のままである。

`critique_human` は消さない。`ContractError` で `critique_human must not be deleted` である。Q5 の無期限と同じ不変条件である。feeling の TTL は `expires_at` のままである。delete ではない。

見つからない id は `ContractError` である。actor が allowlist 外なら先に `DeleteAclHold` である。存在は漏らさない。

SQL に delete 関数も `p_actor` も無い。ACL は Python の契約である。`read.py` に delete は置かない。`related_ids` の cascade はしない。新しい store も置かない。pairing の widen と live ingest は [#18](https://github.com/maplefukku/grok-bot-ops/issues/18) の ingest LOCK のままである。
