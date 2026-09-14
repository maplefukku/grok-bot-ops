# ui-library

Fleet が **use-case kebab + description** で索引した UI 参照（URL+why+optional source）を、**1 つの shadcn MCP 席**から invoke する置き場。Buddy pattern: find → implement → index → remote MCP invoke（[2098811650484863400](https://x.com/taiyo_ai_gakuse/status/2098811650484863400) · [2098423635338002618](https://x.com/taiyo_ai_gakuse/status/2098423635338002618)）。Mem0 / 第二 library skill / 第二 MCP — invent しない。

## find（既存 WRAP）

- 内容: **X UI収集**（X plugin find）と [**UI調査**](../../bots/UI調査.md) が find。新 seat なし。handoff は **URL MUST + why MUST + source optional**。
- 出典: [Grok Bot now works with X](https://x.ai/news/grok-bot-and-x) · https://github.com/maplefukku/grok-bot-ops/blob/main/bots/UI調査.md（2026-09-14）
- 確認: 未

## invoke（ui-library-invoke 手順 — skill ファイルは置かない）

- 内容: **第一** Cursor `/add-plugin shadcn` または `npx shadcn@latest mcp` + `@ui-refs` registry。CA VM で MCP 不可時は [`query.py`](../../scripts/ui_library/query.py) で registry 読み（[`skills/`](../../skills/README.md) に第二 skill は足さない）。
- 出典: [MCP Server - shadcn/ui](https://ui.shadcn.com/docs/mcp) · [Cursor marketplace shadcn](https://cursor.com/marketplace/shadcn)（2026-09-14）
- 確認: 未

## shadcn MCP（Primary WRAP — 1° docs）

- 内容: shadcn CLI 付属 MCP が `search_items_in_registries` / `view_items_in_registries` / `list_items_in_registries` / `get_add_command_for_items` を提供する。fleet 索引 namespace は **`@ui-refs`**（[`registry.json`](../../scripts/ui_library/data/registry.json)）。第二 MCP 席は増やさない。
- 出典: [MCP Server（利用者向け）](https://ui.shadcn.com/docs/mcp) · [MCP Server（registry 開発者向け）](https://ui.shadcn.com/docs/registry/mcp)（2026-09-14）
- 確認: 未

## X UI収集 → ingest（既存 find WRAP）

- 内容: **find** は既存の X plugin / X connector（[`plugins.md`](./plugins.md)）と [`collect-grokbot-knowhow.md`](../../routines/collect-grokbot-knowhow.md) 型の外側ループ routine に任せる。新しい find 席は invent しない。UI収集 lane が ui-library に渡すのは **UI 参照 URL + why だけ**。索引は `@ui-refs`、MCP query/get は shadcn 席。fixture サンプル: `ref-fixture-x-ui-blocks-hero`（`meta.fleet.fixture: true`）。
- 出典: [Grok Bot now works with X](https://x.ai/news/grok-bot-and-x) · [x.com/pcefancom/status/2096819736596398276](https://x.com/pcefancom/status/2096819736596398276)（2026-09-14）
- 確認: 未

## 代替（survey の Alt）

- 内容: コミュニティ Alt [Jpisnice/shadcn-ui-mcp-server](https://github.com/Jpisnice/shadcn-ui-mcp-server)（MIT）。Primary が足りないときだけ。fleet は shadcn CLI MCP を正とする。
- 出典: https://github.com/Jpisnice/shadcn-ui-mcp-server（2026-09-14）
- 確認: 未

## fleet 索引 JSON の置き場

- 内容: 正本は [`scripts/ui_library/data/registry.json`](../../scripts/ui_library/data/registry.json)（`name`: `@ui-refs`）。ingest された URL+why は `meta.fleet.sourceUrl` / `ingestedWhy`。use-case は `categories` と `meta.fleet.useCases`。
- 出典: [registry schema](https://ui.shadcn.com/schema/registry.json) · [ui-library MCP process](https://github.com/maplefukku/grok-bot-ops/blob/main/docs/process/ui-library-mcp.md)（2026-09-14）
- 確認: 未

## UI調査との境界

- 内容: [UI調査 bot 台帳](https://github.com/maplefukku/grok-bot-ops/blob/main/bots/UI調査.md) は「近い事例 URL と why を返す」調査席。ui-library は **索引 + MCP 問い合わせ** だけを持つ。UI調査を置き換えない。Discord drip も invent しない。
- 出典: https://github.com/maplefukku/grok-bot-ops/blob/main/bots/UI調査.md（2026-09-14）
- 確認: 未
