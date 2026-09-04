# Intent/Memory の読み方

Linux の CLI と Python から、関連する atom を最大 N 件引く手順。iOS は対象外。GitHub の LOCK コメント URL は別ソースのまま使う。

表は [schema.sql](./schema.sql)。呼び出しの述語は [contract.py](../../scripts/intent_memory/contract.py)。なぜこの形かは [ADR 0001](../decisions/0001-intent-memory-postgres-pgvector.md)。

`source` は毎回必須。人間向けに読むときは `human` を渡す。

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
))

human_rows = store.by_tags(("fleet",), source=Source.HUMAN)
near = store.similar((1.0, 0.0, 0.0, 0.0), source=Source.HUMAN, limit=5)
```

`scripts/` を `PYTHONPATH` に入れるか、同じ import 経路で読む。本番の行は schema.sql どおり Postgres に置く。このモジュールは CI 可能な契約であり、プロダクト DB ではない。
