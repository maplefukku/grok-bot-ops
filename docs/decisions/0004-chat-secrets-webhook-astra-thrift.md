# 0004. チャット秘密・Webhook提案のみ・Astra WRAP・thrift

- ステータス: Accepted
- 日付: 2026-09-09
- LOCK: PdM+CTO ADOPT bake 2026-09-09

## 文脈

ボットがチャットで秘密を集める。webhook から Bot fixer を自動実行する。Astra の穴を CreateAgent で埋める。spend 用の新ダッシュボードを置く。Planner と GB は 2026-09-09 にこの 4 つを REJECT した。採るのは既存の WRAP だけである。

[0003](./0003-domain-unit-throughput.md) は手順を ADR の外に置いた。この ADR も手順を外に置く。新しい bot、スクリプト、process ページは作らない。

## 決定

1. ボットが資格情報を集めてよいのは `request_box_help` と `secret-request` だけである。チャットにトークン、キー、パスワードを貼らせない。セッション cookie とセッショントークンを拾って自分に権限を付けない。pstack の secret-request は `/make-bot-ui` の規則である。出典は [`docs/knowhow/bot-ui.md`](../knowhow/bot-ui.md) と [`docs/knowhow/routines.md`](../knowhow/routines.md) である。sender key はチャットに置かない。パスワードとトークンの受領禁止は [`docs/laststitch/account.md`](../laststitch/account.md) である。`request_box_help` と `secret-request` は既存の tool と skill の名前である。このリポジトリに SKILL.md は足さない。
2. webhook から Bot fixer を自動実行しない。提案だけの経路を残す。[`routines/watch-proposal-digest.md`](../../routines/watch-proposal-digest.md) は LIVE であり、提案だけである。監視の `guardian-phase0-propose` に折り込む。枠は Mon 10:00 JST である。[`bots/監視.md`](../../bots/監視.md) は提案のみであり、CreateAgent は 0 である。digest は既に LIVE である。auto-exec は REJECT のままである。解除は人間または PdM の明示の go のあとである。watch と proposal digest は提案してよい。修正を自動適用しない。新しい Guardian ボットは作らない。
3. Astra は既存席だけを WRAP する。席は [`bots/ChatGPT_Astra_Pro.md`](../../bots/ChatGPT_Astra_Pro.md)、[`bots/Mini_Codex.md`](../../bots/Mini_Codex.md)、[`bots/Mini運用.md`](../../bots/Mini運用.md) である。Mini運用は CLI である。Codex と GUI は Mini Codex である。Astra の穴埋めの CreateAgent は NONE である。CreateAgent は [`CBO`](../../bots/CBO.md) である。[0003](./0003-domain-unit-throughput.md) の Accepted は CreateAgent 承認ではない。新しい Astra のコーディング席は作らない。
4. コーディングのトークンと spend の案内は既存の thrift と Cursor運用に寄せる。新ダッシュボードは作らない。規則は thrift-2d である。Max は稀。medium が既定。Fast は OFF 寄り。席は [`bots/Cursor運用.md`](../../bots/Cursor運用.md) である。スキルは [Cursor運用](sand-workflow:cursor) である。[`trend-log.md`](./trend-log.md) の 2026-09-08 行は spend 監視を ADOPT した。Cursor運用へ WRAP する。利用上限の観察は [`docs/knowhow/access.md`](../knowhow/access.md) である。コーディング経路は [Cloud開発](sand-workflow:cloud) と tool-path-prefer である。thrift-2d はこのリポジトリのファイルではない。作らない。

## 結果

- 秘密はチャットに出ない。
- webhook の修正は提案で止まる。自動適用しない。
- Astra の席は増えない。CreateAgent は動かない。
- spend の画面は Cursor運用のままである。新しいダッシュボードは無い。

## 却下した案

- チャットにトークン、キー、パスワードを貼らせる。集め先は `request_box_help` と `secret-request` だけである。
- セッション cookie とセッショントークンを拾って自分に権限を付ける。
- digest が LIVE なので Bot fixer を自動実行する。LIVE は提案の稼働であり、自動適用の許可ではない。
- 新しい Guardian ボット。監視が提案する。
- Astra の穴埋めに CreateAgent する。新しい Astra のコーディング席。既存席で足りる。
- spend 用の新ダッシュボード。Cursor運用で足りる。
- `request_box_help` と `secret-request` の SKILL.md をこのリポジトリに置く。名前は既存である。
- thrift-2d をこのリポジトリのファイルにする。規則名でありファイルではない。
- この ADR に手順を全文載せる。手順は既存の WRAP 先にある。
