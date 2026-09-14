# ui-library

Fleet が **use-case で索引した UI 参照** を、既存の shadcn registry MCP 席から問い合わせるための置き場。第二の MCP プロトコル席や mcp-ui（Apps UI host SDK）をライブラリ索引としては使わない。

## shadcn registry MCP（Primary WRAP）

- 内容: shadcn CLI 付属 MCP が `list` / `search` / `view` / `get_add` を提供する。任意の shadcn 互換 `registry.json` を `@namespace` として `components.json` に載せれば、fleet 索引も同じ席から検索できる。
- 出典: [MCP Server - shadcn/ui](https://ui.shadcn.com/docs/registry/mcp)（2026-09-14）
- 確認: 未

## 代替（survey の Alt）

- 内容: コミュニティ実装 `Jpisnice/shadcn-ui-mcp-server` は同種の registry 操作を提供する。Primary が足りないときだけ Alt として検討する。fleet は shadcn CLI MCP を正とする。
- 出典: [shadcn-ui-mcp-server（GitHub 検索）](https://github.com/search?q=shadcn-ui-mcp-server&type=repositories)（2026-09-14）
- 確認: 未

## fleet 索引 JSON の置き場

- 内容: 正本は [`scripts/ui_library/data/registry.json`](../../scripts/ui_library/data/registry.json)。X UI収集から ingest された URL+why は `meta.fleet` に載る。use-case は `categories` と `meta.fleet.useCases` の両方に揃える。
- 出典: [registry schema](https://ui.shadcn.com/schema/registry.json) · [ui-library MCP process](https://github.com/maplefukku/grok-bot-ops/blob/main/docs/process/ui-library-mcp.md)（2026-09-14）
- 確認: 未

## UI調査との境界

- 内容: [UI調査 bot 台帳](https://github.com/maplefukku/grok-bot-ops/blob/main/bots/UI調査.md) は「近い事例 URL と why を返す」調査席。ui-library は **索引 + MCP 問い合わせ** だけを持つ。UI調査を置き換えない。Discord drip も invent しない。
- 出典: https://github.com/maplefukku/grok-bot-ops/blob/main/bots/UI調査.md（2026-09-14）
- 確認: 未
