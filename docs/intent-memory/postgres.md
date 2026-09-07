# 専用 Postgres（pgvector WRAP）

Phase0 のホストは専用 Postgres である。製品は [pgvector](https://github.com/pgvector/pgvector) である。新しい DB 製品は置かない。感情はプロダクト DB に置かない。

CI は Postgres を起動しない。隔離の証明は [`../decisions/0001-intent-memory-postgres-pgvector.md`](../decisions/0001-intent-memory-postgres-pgvector.md) どおりインメモリの `MemoryStore` である。

## 出典

| 項目 | 値 |
|---|---|
| OSS | [pgvector/pgvector](https://github.com/pgvector/pgvector) |
| Docker イメージ | [pgvector/pgvector](https://hub.docker.com/r/pgvector/pgvector) |
| 取得 | 2026-09-08 |
| 公式 pull 例 | `docker pull pgvector/pgvector:pg18-trixie` |
| 拡張 | `CREATE EXTENSION vector;` |

公式 README の Docker 節を WRAP する。自前の Dockerfile は書かない。

## 起動

リポジトリルートではなく、このディレクトリで公式イメージを上げる。

```sh
cd docs/intent-memory
docker compose up -d
```

[`docker-compose.yml`](./docker-compose.yml) は公式タグ `pgvector/pgvector:pg18-trixie` を指す。初回だけ [`schema.sql`](./schema.sql) を `/docker-entrypoint-initdb.d/001-schema.sql` として読む。`schema.sql` の先頭が `CREATE EXTENSION IF NOT EXISTS vector;` である。

compose を使わないときも同じイメージである。

```sh
docker pull pgvector/pgvector:pg18-trixie
docker run --name intent-memory -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d pgvector/pgvector:pg18-trixie
psql -h 127.0.0.1 -U postgres -f docs/intent-memory/schema.sql
```

パスワードはローカル確認用である。本番の秘密はここへ書かない。

## 読み

起動したあとも、艦隊の読み方は [`read-recipe.md`](./read-recipe.md) である。本番クライアントはこのリポジトリにまだ無い。CI と Planner の dry-run は fixture を使う。
