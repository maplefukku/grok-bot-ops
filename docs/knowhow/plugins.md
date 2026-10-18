# plugins

プラグインの入手と自作。

## Tailscale（private tailnet の MCP）

- 内容: Grok Bot 0.49.0 以降（`cursor` は `never`）。自分の tailnet では `tag:grokbot` の 1 台として参加し、policy がその tag に許可した host と port だけに届く。company tailnet は Grok Bot の team admin が plugin で有効化し、メンバーは team row から自分の device で接続する。その場合 `tag:grokbot` の policy は要らない。Access controls で `tag:grokbot` を tagOwners（署名するユーザーまたは `autogroup:admin`）に足し、MCP の host と port だけへの grant を既存 policy にマージする。default の allow-all が残っていると、その tag は全 device に届く。plugin の Authenticate で Tailscale に sign in し device を承認する。device approval がオンなら Machines でも承認する。Tailnet Lock なら署名ノードで `tailscale lock sign <node-key>` するまで何にも届かない。MCP はいつもの追加で、host は `*.ts.net` か `100.x`。使えるのは bot owner、linked teammates、owner がスケジュールした routine。到達確認は plugin の Check host。bot computer の curl は personal connection だけを使う。切断は plugin ページの Remove。これは v0.70.2 changelog（2026-10-11）の「private Tailscale network の MCP はまだ届かないので Tailscale Funnel を提案する」を置き換える。PR 533（merged 2026-10-12）は、backend の Tailscale 行が Statsig `grok_bot_tailnet` でゲートされ、merge すると plugin が公開されると書いている。2026-10-17 の報告では、skill だけ入り Authenticate ボタンと MCP サーバ項目が出ない。
- 出典: [skill](https://github.com/cursor/plugins/blob/main/third_party/tailscale/skills/tailscale-setup/SKILL.md) · [README](https://github.com/cursor/plugins/blob/main/third_party/tailscale/README.md) · [plugin.json](https://github.com/cursor/plugins/blob/main/third_party/tailscale/.cursor-plugin/plugin.json) · [PR 533](https://github.com/cursor/plugins/pull/533) · [changelog v0.70.2](https://x.ai/changelog/bot) · [x.com/wookiist/status/2111320507274690824](https://x.com/wookiist/status/2111320507274690824)（2026-10-17）
- 確認: 未

## TikTok for Business

- 内容: SearchPlugins で要確認。公式の告知投稿は無い。公開ページは「TikTok for Business for Grok Bot」で、説明は Manage TikTok ad campaigns, ad groups, ads, audiences, creatives, and reports。cursor/plugins の README は Cursor Settings → Plugins で検索して Install、またはチャットで `/add-plugin tiktok-for-business`。MCP は `https://business-api.tiktok.com/open_mcp/tt-ads-mcp-layer`（Progressive Disclosure。接続時に about 40 core tools、必要になると残りの roughly 400 tools）。Full Disclosure の別 URL は `https://business-api.tiktok.com/open_mcp/tt-ads-mcp-flat`。OAuth は Dynamic Client Registration と PKCE。API key、developer app、client ID は無い。Authorization は 30 days で、その後は再度 sign in。plugin.json の minClientVersions は `cursor` 3.13.0 のみ。
- 出典: [x.ai/bot/plugin/76659963](https://x.ai/bot/plugin/76659963) · [README](https://github.com/cursor/plugins/blob/main/third_party/tiktok-for-business/README.md) · [plugin.json](https://github.com/cursor/plugins/blob/main/third_party/tiktok-for-business/.cursor-plugin/plugin.json)（2026-10-18 確認）
- 確認: 未

## Google Ads

- 内容: SearchPlugins で要確認。今回開いた範囲に @bot または @cursor_ai の告知投稿は無い。cursor/plugins の README は、Grok Bot Settings → Plugins で Google Ads を検索し、Install のあと Google の sign-in。OAuth 2.0 の scope は `https://www.googleapis.com/auth/adwords`。MCP は `https://api.cursor.com/rest-mcp/google-ads/mcp`。GAQL で account と campaign を報告し、keyword と audience を調べ、campaign を変更する。変更は `validate_mutate`（`validateOnly`）のあと `mutate`。plugin.json は Grok Bot のみ（`cursor: never`、grokbot / sand は 0.30.0 以上）。説明は Report on campaigns, research keywords, and make previewed changes。
- 出典: [README](https://github.com/cursor/plugins/blob/main/third_party/google-ads/README.md) · [plugin.json](https://github.com/cursor/plugins/blob/main/third_party/google-ads/.cursor-plugin/plugin.json) · [mcp.json](https://github.com/cursor/plugins/blob/main/third_party/google-ads/mcp.json)（2026-10-18 確認）
- 確認: 未

## Gopuff

- 内容: SearchPlugins で要確認。今回開いた範囲に @bot の告知投稿は無い。cursor/plugins は Grok Bot のみ（`cursor: never`、grokbot / sand は 0.49.0 以上）。MCP は `https://mcp.gopuff.com/mcp`、auth の CLIENT_ID は `mcp-grok-bot`。sign-in は Gopuff の OAuth（`https://goauth.gopuff.com`、email magic link または one-time code）。Grok Bot は Gopuff の credentials を見ない。search、cart、order はそのアカウントの Gopuff に行き、出した注文は通常の Gopuff 注文として課金・配送される。切断は plugin の Accounts。
- 出典: [README](https://github.com/cursor/plugins/blob/main/third_party/gopuff/README.md) · [plugin.json](https://github.com/cursor/plugins/blob/main/third_party/gopuff/.cursor-plugin/plugin.json) · [mcp.json](https://github.com/cursor/plugins/blob/main/third_party/gopuff/mcp.json)（2026-10-18 確認）
- 確認: 未

## Gusto

- 内容: 公開ページは「Gusto for Grok Bot」。説明は Work with payroll, employees, contractors, time off, and reports。README の MCP は `https://mcp.api.gusto.com/`。OAuth は Dynamic Client Registration と PKCE。API key も client ID も無い。接続には global または full admin の Gusto アカウントが要る。sign-in で選んだ data categories だけにアクセスが限られる。一部ツールは running payroll を含むデータ変更をする。承認前に毎回 tool call をレビューし、この server の auto-run はオフにする。Gusto は、payroll と employee のデータが他サービスへ渡らないよう、同じ chat に他の MCP server を置かない isolation を推奨している。client 側で model training を opt out する。Gusto 自身が契約する AI provider への不使用約束は、MCP で繋いだ client には及ばない。切断して再 sign-in するか plugin を外すと access を変えたり revoke したりできる。plugin.json の minClientVersions は `cursor` 3.13.0。README の導入は Cursor Settings → Plugins、またはチャットの `/add-plugin gusto`。
- 出典: [x.ai/bot/plugin/76659962](https://x.ai/bot/plugin/76659962) · [README](https://github.com/cursor/plugins/blob/main/third_party/gusto/README.md) · [Gusto MCP](https://docs.gusto.com/app-integrations/docs/mcp)（2026-10-18 確認）
- 確認: 未

## X Chat を読む

- 内容: @bot は、X を接続してから、メッセージ横断の作業を頼める、と書く。プラン制限や送信できる範囲は、その投稿には無い。@pjvann は、自分の Bot が新しい message request を見て承認し、inbox を追っていた、と書いている。
- 出典: [x.com/bot/status/2111184282903523440](https://x.com/bot/status/2111184282903523440)（2026-10-16） · [x.com/pjvann/status/2111104660773687646](https://x.com/pjvann/status/2111104660773687646)
- 確認: 未

## 2026-10-16 の connector と marketplace 提出

- 内容: @bot は Robinhood、Coinbase、Trello、PostHog、beehiiv、eToro、and more と書き、一覧全体、read か trade か、プラン制限は書いていない。提出ページは plugin または MCP server を、Grok（coming soon）、Grok Bot、Cursor の利用者へ配る。項目は unique organization handle（spaces も capitalization も無し）、website URL、logotype URL（1:1 の SVG または PNG で background plate 付き）、掲載先。review のあと marketplace に載る。
- 出典: [x.com/bot/status/2111184284786802881](https://x.com/bot/status/2111184284786802881)（2026-10-16） · [submit a plugin](https://x.ai/bot/marketplace/submit-a-plugin) · [x.com/ericzakariasson/status/2110492929920053441](https://x.com/ericzakariasson/status/2110492929920053441)（2026-10-14）
- 確認: 未

## v0.70.2 の X 検索と in-chat app

- 内容: X アカウントを繋がなくても、Bot は X の投稿とプロフィールを検索して読める。app 付き connector（例は Figma、Notion、Canva）はチャットに interactive card を出せる。connector のリンクを渡すと、catalog に対応 plugin があればそれを入れる。bank または brokerage の connector がデータを返したあと、Bot は他へ共有する前に確認する。
- 出典: [changelog v0.70.2](https://x.ai/changelog/bot)（2026-10-11）
- 確認: 未

## Tesla 車内 Grok Bot + Home Assistant MCP

- 内容: Tesla の最新 update で車内 Grok Bot が connectors 対応。Home Assistant MCP を追加して Meross 車庫ドア等を操作した報告。own-network / Route egress と組み合わせると localhost MCP 到達が改善する文脈あり。
- 出典: [x.com/wesbos/status/2102884716223291438](https://x.com/wesbos/status/2102884716223291438)（2026-09-23）
- 確認: 未

## ワンクリック plugin share deeplink

- 内容: プラグインページで share / link アイコンから `grokbot://app/v1/plugin/add?id=…` 形式の deeplink を取得。X desktop クライアントで動作。
- 出典: [x.com/mattyp/status/2101491045553070094](https://x.com/mattyp/status/2101491045553070094)（2026-09-20）
- 確認: 未

## MCP で共有 AI memory

- 内容: MCP を使って Bot 間・ツール間で AI memory を共有する、という用法の報告。
- 出典: [x.com/connorgallic/status/2099630749380956315](https://x.com/connorgallic/status/2099630749380956315)（2026-09-15）
- 確認: 未

## Microsoft Teams

- 内容: Teams for Grok Bot プラグインでチャット・チャネルメッセージの検索・閲覧・送信ができる。
- 出典: [x.com/bot/status/2098481256417866145](https://x.com/bot/status/2098481256417866145) · [Teams plugin](https://x.ai/bot/plugin/63354504)（2026-09-11）
- 確認: 未

## GTM connectors (Salesforce / HubSpot / Gong / Clay / Granola)

- 内容: Bot を Salesforce、HubSpot、Gong、Clay、Granola など GTM ツールに接続し、アカウント把握・フォローアップ・調査ができる、という公式告知。
- 出典: [x.com/bot/status/2098183353665261979](https://x.com/bot/status/2098183353665261979)（2026-09-10）
- 確認: 未

## Dialbot + Bland で Grok Bot に電話させる

- 内容: Dialbot を入れ、Bland の voice を繋いで Bot から電話をかけるデモ。transcript / cost 確認と bot 連鎖まで。template: [x.ai/bot/NJXi2SWEuhNxjOjspMMPi](https://x.ai/bot/NJXi2SWEuhNxjOjspMMPi)
- 出典: [x.com/mattyp/status/2098155792327381294](https://x.com/mattyp/status/2098155792327381294)（2026-09-10） · [template](https://x.ai/bot/NJXi2SWEuhNxjOjspMMPi) · [reply](https://x.com/mattyp/status/2098156079620542639)
- 確認: 未

## Grok Voice（Cursor marketplace）— dictation / realtime voice / read-aloud

- 内容: Cursor marketplace の Grok Voice プラグイン。/add-dictation、/add-voice、/add-read-aloud。/debug-voice もある。コード: [github.com/cursor/plugins/tree/main/grok-voice](https://github.com/cursor/plugins/tree/main/grok-voice)
- 出典: [x.com/ericzakariasson/status/2098080093562458445](https://x.com/ericzakariasson/status/2098080093562458445)（2026-09-10） · [marketplace](https://cursor.com/marketplace/cursor/grok-voice) · [code](https://github.com/cursor/plugins/tree/main/grok-voice) · [debug](https://x.com/ericzakariasson/status/2098080105654608018)
- 確認: 未

## Microsoft Outlook / Calendar / OneDrive

- 内容: 新しいプラグインで Bot が Outlook、Calendar、OneDrive に直接アクセスする。閲覧だけではなく読み書き・操作ができる。
- 出典: [x.com/bot/status/2094543253811183943](https://x.com/bot/status/2094543253811183943)（2026-08-31）
- 確認: 未

## メール送信の前に禁止事項を書く

- 内容: Bot がメールを送れるなら、先に「送ってはいけないもの」を書いてから inbox を繋ぐ。書いていないまま接ぐと、inbox を chatbot に渡したことになる。
- 出典: [x.com/PedroKnigge/status/2094562726236541406](https://x.com/PedroKnigge/status/2094562726236541406)（2026-08-31）
- 確認: 未

## X plugin / X connector

- 内容: X plugin / X connector で投稿検索・タイムライン・トレンド・ブックマークができる。有料 Grok Bot ユーザーには開始用の無料 X API credits が付く。
- 出典: [Grok Bot now works with X](https://x.ai/news/grok-bot-and-x)（2026-08-29）
- 確認: 未

## Settings → Plugins

- 内容: コネクタはアプリ上では Plugins と表示される。Settings → Plugins で追加し、Marketplace でコネクタとパッケージ済みスキルを探す。Yours で導入済みを見る。チャットでは `/` が保存スキル、`@` が Bot・グループ・routine・コネクタ。
- 出典: [Use the computer and apps](https://docs.x.ai/grok-bot/computer-and-apps)（2026-08-29 確認）、[Settings and notifications](https://docs.x.ai/grok-bot/settings-and-notifications)
- 確認: 未

## Cursor プラグインの自作

- 内容: `.cursor-plugin/plugin.json` をマニフェストとして作る。`skills/` へのパスをマニフェストで指す。実例: [pstack の plugin.json](https://github.com/cursor/plugins/blob/main/pstack/.cursor-plugin/plugin.json)。このリポジトリ自体も同じ形式（[`.cursor-plugin/plugin.json`](../../.cursor-plugin/plugin.json)）。
- 出典: [pstack/.cursor-plugin/plugin.json](https://github.com/cursor/plugins/blob/main/pstack/.cursor-plugin/plugin.json)
- 確認: 済
