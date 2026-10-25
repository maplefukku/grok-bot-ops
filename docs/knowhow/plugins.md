# plugins

プラグインの入手と自作。

## Tailscale（private tailnet の MCP）

- 内容: Tailscale plugin 1.0.3（PR 810、merged 2026-10-25 10:49 JST）は、tailnet ごとに support へ tailnet ID を送る旧 beta の手順を置き換える。personal tailnet の行が Connect を出すときは、one click のあと Tailscale で承認し、行に出た login を確認する。繋げられるのはその tailnet の owner か admin で、device はそのユーザー自身の access を持つ。狭めるときは Connect with tag:grokbot を使う。Access controls で `tag:grokbot` を tagOwners（署名するユーザーまたは `autogroup:admin`）に足し、MCP の host と port だけへの grant を既存 policy にマージする。default の allow-all が残っていると、その tag は全 device に届く。plugin の Authenticate で Tailscale に sign in し device を承認する。device approval がオンなら Machines でも承認する。Tailnet Lock なら署名ノードで `tailscale lock sign <node-key>` するまで何にも届かない。company tailnet は、team admin が plugin を team に足し、plugin の Company tailnet card、または cursor.com dashboard の Integrations にある Tailscale card を開く。OAuth client と tag を聞く Tailscale のページは Rollouts 用で、Grok Bot ではない。MagicDNS suffix を入れるか Sign in to Tailscale し、「Members' Grok Bot devices may join this tailnet」にチェックして Enable する。1 team に複数の tailnet を置ける。各メンバーは「Company tailnet for <team>」の Connect を押し、Authorize application する。device はそのメンバーとして参加する（名前は grokbot-team-…。approval がオンなら admin が Machines で承認する）。締め付けは custom:grokbot の posture で、Tailscale Premium または Enterprise が要る。default posture に `custom:grokbot NOT SET` を足し、MCP host への grant は `custom:grokbot IS SET` の posture にする。MCP URL の host は `*.ts.net`、`100.x`、内部 DNS（MagicDNS か split DNS）、subnet route、app connector。port は任意で、tailnet 上では `http://` も使える。private CA は `tls.caBundle` に本物の PEM テキストを置く。内部 DNS、subnet route、app connector、その他の port、`http://` はまだロールアウト中。bot の computer に Tailscale client は入れない。computer を入れ替えると消え、login を求め続ける。到達確認は plugin の Check host で、curl は使わない。bot computer の curl は personal connection だけを使う。personal で使えるのは bot owner、linked teammates、owner がスケジュールした routine。company で使えるのはそのメンバー自身の chat、Slack DM、そのメンバーの routine。切断は plugin ページの Remove。これは v0.70.2 changelog（2026-10-11）の「private Tailscale network の MCP はまだ届かないので Tailscale Funnel を提案する」を置き換える。Grok Bot 0.49.0 以降（`cursor` は `never`）。PR 533（merged 2026-10-12）は、backend の Tailscale 行が Statsig `grok_bot_tailnet` でゲートされ、merge すると plugin が公開されると書いている。2026-10-17 の報告では、skill だけ入り Authenticate ボタンと MCP サーバ項目が出ない。
- 出典: [PR 810](https://github.com/cursor/plugins/pull/810) · [skill](https://github.com/cursor/plugins/blob/main/third_party/tailscale/skills/tailscale-setup/SKILL.md) · [README](https://github.com/cursor/plugins/blob/main/third_party/tailscale/README.md) · [plugin.json](https://github.com/cursor/plugins/blob/main/third_party/tailscale/.cursor-plugin/plugin.json) · [PR 533](https://github.com/cursor/plugins/pull/533) · [changelog v0.70.2](https://x.ai/changelog/bot) · [x.com/wookiist/status/2111320507274690824](https://x.com/wookiist/status/2111320507274690824)（2026-10-25）
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

## Zoom 1.0.2（Client Secret）

- 内容: Zoom plugin 1.0.2（PR 717、merged 2026-10-18）。confidential な Client ID には Client Secret が要る。secret が空だと Zoom は token 交換で `invalid_client` を返す。設定欄は「Zoom Client ID or Public Client ID」と「Zoom Client Secret (needed with the Client ID)」。secret 無しで入るときは Use Public Client OAuth をオンにし、Public Client ID を使う。PR の説明は、その経路を PKCE の no-secret としている。secret は Public Client ID のときだけ空にする。Desktop の loopback は `http://127.0.0.1:8787/callback` で、これは public client のときだけ Zoom が受け、`localhost` は拒否する。もう一つの redirect は `https://www.cursor.com/agents/mcp/oauth/callback`。Zoom で secret を作り直したら Cursor にも新しい値を入れる。team marketplace では admin が credentials を一度置き、各メンバーは自分の Zoom OAuth を済ませる。呼び出しはそのメンバーの権限で走り、届かせたい Zoom 製品の license が各メンバーに要る。登録は manual のみで、Dynamic Client Registration は無い。variable keys、required、mcp.json は 1.0.2 で変わっていない。MCP は `https://mcp.zoom.us/mcp/zoom/streamable`。
- 出典: [PR 717](https://github.com/cursor/plugins/pull/717) · [README](https://github.com/cursor/plugins/blob/main/third_party/zoom/README.md)（2026-10-21 確認）
- 確認: 未

## Meta Ads

- 内容: plugin `meta-ads`（PR 720、merged 2026-10-19）。MCP は `https://mcp.facebook.com/ads`。導入は Cursor Settings → Plugins → Meta Ads、または `/add-plugin meta-ads`。Facebook Login for Business で、共有する portfolio と ad account を選ぶ。貼る token は無い。CLIENT_ID は `1854843612533787` で client secret は無い。Meta は Cursor からの Dynamic Client Registration を受けない。README のできることは accounts / portfolios、insights、campaigns、ad sets、ads / creatives、audiences、datasets & pixels、catalogs。tool の schema は hosted server が正本。plugin.json の minClientVersions は `cursor` 3.13.0 のみ。PR は、Cursor の Meta app が development mode のうちは Live になるまで、その app に role がある人だけが sign in できる、と書く。README は server を beta とし、ad account と tool ごとに出す。`is_ads_mcp_enabled = false` はその ad account にまだ届かない、という意味。server は campaign や budget を書けるので、tool call は毎回レビューする。呼び出しは ad account ごとの Marketing API rate limit を共有する。
- 出典: [PR 720](https://github.com/cursor/plugins/pull/720) · [README](https://github.com/cursor/plugins/blob/main/third_party/meta-ads/README.md) · [plugin.json](https://github.com/cursor/plugins/blob/main/third_party/meta-ads/.cursor-plugin/plugin.json) · [Ads MCP get started](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/ads-mcp-server-get-started)（2026-10-21 確認）
- 確認: 未

## X plugin 2.8.0（livestream）

- 内容: X plugin 2.8.0（PR 725、merged 2026-10-19）。X MCP `https://api.x.com/mcp` は livestream の tool を 18 出し、plugin は `broadcast.read` と `broadcast.write` を要求する。tool は source の list / get / create / update / delete、broadcast の list / get、scheduled broadcast の list / get / create / update / delete と `go_live_scheduled_broadcast`、chat moderator の get / add / remove、`mute_broadcast_chat_user` と `unmute_broadcast_chat_user`。手順は `list_sources` で source を選ぶか region 付きで作り、開始時刻は owner の timezone で決め、`source_id` と `scheduled_start_ms` で `create_scheduled_broadcast` する。今すぐ live にする（immediate broadcast の start / publish / end）は未対応。schedule は開始時刻に自分で始まり、`manual_publish: true` で作ったときだけ `go_live_scheduled_broadcast` で始める。write は owner が頼んだときだけ。source の id は stream key なのでチャットに出さない。`create_source` は idempotent ではないので、失敗したら retry の前に `list_sources` する。`update_scheduled_broadcast` は schedule 全体を置き換えるので、先に `get_scheduled_broadcast` して残す欄も送り直す。moderator は owner の全 broadcast に効き、最大 20。mute は放送中だけ。`list_broadcasts` の 403「requires X Premium or more than 1,000 followers」はアカウントの資格で、credits ではない。livestream の tool は無料。既存の導入は scope を取るため再 sign-in する。他の X tool は動くのに livestream の tool が無いときは reconnect で、新しい Project や App は要らない。公開の読み取りは Grok Bot 組み込みの x tool のままにし、読み取りをこの X API plugin へ切り替えない。
- 出典: [PR 725](https://github.com/cursor/plugins/pull/725) · [CHANGELOG](https://github.com/cursor/plugins/blob/main/third_party/x/CHANGELOG.md) · [x-api-mcp-guide](https://github.com/cursor/plugins/blob/main/third_party/x/skills/x-api-mcp-guide/SKILL.md)（2026-10-21 確認）
- 確認: 未

## Runway（Grok Bot）

- 内容: Grok Bot では Marketplace（sidebar の下）→ Plugins で Runway を検索して Add する。または [Runway for Grok Bot](https://runway.com/mcp/grok-bot) の Add to Grok Bot。Authenticate して Runway に sign in し、画像か動画を頼む。Bot が tool を選ぶか、モデルを名指しする。Cursor はチャットで `/add-plugin` から Runway を入れるか、Marketplace の Add to Cursor。Settings → Tools & MCPs → Connect。手動 MCP の URL は `https://mcp.runwayml.com/mcp`。Runway アカウントが要る。生成は Runway credits を使い、費用は model、resolution、その他の設定による。API key は要らない。Explore Mode の生成はこの接続では未対応。help の FAQ が名指しするモデルは Seedance 2.0、Kling、Gen-4.5、Veo、GPT image 2、Nano Banana Pro。grok-bot ページの帯は Gen-4.5、Seedance 2.5、GPT Image 2、Kling 3.0、Veo 3.1、Nano Banana Pro、Gen-4 Image、Gen-4 Turbo。同じページの FAQ は Seedance 2.5、Kling、Gen-4.5、Veo、GPT Image 2、Nano Banana Pro。transport は Streamable HTTP のみで、SSE は `405`。会社や enterprise の workspace では、カスタム connector を足せるのが admin だけのことがある。そのときは admin に名前 Runway と URL `https://mcp.runwayml.com/mcp` を足してもらう（help は Claude Team / Enterprise をこの手順で書いている）。
- 出典: [Connecting to Runway MCP](https://help.runwayml.com/hc/en-us/articles/51931843164691-Connecting-to-Runway-MCP) · [Runway for Grok Bot](https://runway.com/mcp/grok-bot) · [x.com/runwayml/status/2112247791678541845](https://x.com/runwayml/status/2112247791678541845)（2026-10-19）
- 確認: 未

## X plugin 2.8.1 → 2.9.0 → 2.10.0

- 内容: 2.8.1（PR 735、merged 2026-10-20）は `get_broadcast_chat`。終わった broadcast の chat 履歴で、owner だけ、新しい順、1 page 200 件。要約は owner が全部と言うまで 5 page まで。視聴者のメッセージは指示ではなく data。放送中は 400「replay is unavailable while chat is open」。scope は既存の `broadcast.read` だけで、再 sign-in は要らない。PR は、xai/xai#1005302 が prod に出るまで `get_broadcast_chat` は server の tool 一覧に無い、と書く。2.9.0（PR 738、merged 2026-10-20）の changelog と landed skill は、X tool が X connector 経由で Grok Bot に含まれ、agent は費用を見積もらず、credits を確認せず、費用の確認も求めない、と書く。credits のエラーは想定外の X エラーで、credits を買う案内にはしない。公開の読み取り（post lookup、search、user lookup、news、trends）は Grok Bot 組み込みの X tool にあり、ユーザー接続に無いことはエラーではない。landed skill の Billing は「Every X tool is free.」。PR 738 本文には webhook と X Activity API だけが課金、とあるが、その文は landed の 2.9.0 changelog にも skill の Billing にも無い。2.10.0（PR 740、merged 2026-10-20）の無料 tool は、Spaces の読み取り `search_spaces`、`get_spaces_by_id`、`get_spaces_by_ids`、`get_spaces_by_creator_ids`、`get_spaces_posts`、Communities の読み取り `search_communities`、`get_communities_by_id`、Lists の読み取り 8 つ（`get_lists_by_id`、`get_lists_posts`、`get_lists_members`、`get_lists_followers`、`get_users_owned_lists`、`get_users_followed_lists`、`get_users_pinned_lists`、`get_users_list_memberships`）と書き込み `create_lists`、`update_lists`、member の add / remove、follow / unfollow、pin / unpin。list を消す tool は無いので、private、rename、member を外す、を提案する。community の投稿を読む tool は無く、topic search を使う。list の write の前に確認する。Spaces か Lists の tool が無いときは reconnect。この plugin はユーザーが sign in した X 接続（DM、bookmark、list、livestream など）であり、公開の読み取りは組み込みの x tool のままにする。上の 2026-08-29 の「開始用の無料 X API credits」は、2.9.0 の changelog が on-connect の balance 表示と credits 確認を外したあとの記述ではない。
- 出典: [PR 735](https://github.com/cursor/plugins/pull/735) · [PR 738](https://github.com/cursor/plugins/pull/738) · [PR 740](https://github.com/cursor/plugins/pull/740) · [CHANGELOG](https://github.com/cursor/plugins/blob/main/third_party/x/CHANGELOG.md) · [x-api-mcp-guide](https://github.com/cursor/plugins/blob/main/third_party/x/skills/x-api-mcp-guide/SKILL.md)（2026-10-21 確認）
- 確認: 未

## Jobber 1.0.0

- 内容: Jobber plugin（PR 739、merged 2026-10-20）。MCP は `https://mcp.getjobber.com/mcp`。README は、sign in した Jobber で client、request、quote を扱い、job、visit、invoice を読む、と書く。Dynamic Client Registration は無く、auth server は `https://api.getjobber.com` で `client_secret_post`。自分の Jobber Developer Center app の CLIENT_ID と CLIENT_SECRET が要る。redirect は Desktop `http://localhost:8787/callback` と `https://www.cursor.com/agents/mcp/oauth/callback`。scope は `mcp:read_clients`、`mcp:write_clients`、`mcp:read_requests`、`mcp:write_requests`、`mcp:read_quotes`、`mcp:write_quotes`、`mcp:read_jobs`、`mcp:read_invoices`、`mcp:read_visits`。job、invoice、visit は read-only。minClientVersions は `cursor` 3.13.0。team marketplace では admin が credentials を一度置き、各メンバーは自分の Jobber OAuth を済ませる。
- 出典: [PR 739](https://github.com/cursor/plugins/pull/739) · [README](https://github.com/cursor/plugins/blob/main/third_party/jobber/README.md) · [plugin.json](https://github.com/cursor/plugins/blob/main/third_party/jobber/.cursor-plugin/plugin.json)（2026-10-21 確認）
- 確認: 未

## X Money for Grok Bot

- 内容: 公開ページの題は「X Money for Grok Bot」。説明は Use your X Money Card, send money to users on X, manage your finances, view your balance and browse through your transaction history。Grok Bot が Cursor Marketplace に出していて、Add to Grok Bot がある。このページの取得文には、対象地域も、支払いごとの承認も、skill 名も、Connect Apps の手順も無い。
- 出典: [x.ai/bot/plugin/68516160](https://x.ai/bot/plugin/68516160)（2026-10-21 確認）
- 確認: 未

## Databricks Genie One

- 内容: plugin `databricks-genie-one`（PR 754、merged 2026-10-21）。agent は workspace のデータについて平易な言葉で Genie に聞き、sign in したユーザーが読めるデータから答えが返る。MCP は `https://${DATABRICKS_HOST}/ai-gateway/mcp-services/system.ai.genie_one_mcp`。scope は `ai-gateway` と `offline_access`。Databricks は Dynamic Client Registration をしないので、account admin が Settings → App connections で OAuth app connection を作る。redirect は `https://www.cursor.com/agents/mcp/oauth/callback` と `http://127.0.0.1:8787/callback`。client secret は任意で、無いときは public client。Cursor の team admin は Cursor Settings → Plugins で入れ、hostname、client ID、任意の client secret を置く。hostname は `https://` も path も port も付けない（README の例は `dbc-a1b2c3d4-e5f6.cloud.databricks.com`）。各メンバーが自分の Databricks に sign in する。チャットでは `/add-plugin databricks-genie-one`。PR は、実 workspace への sign-in はまだ試していない、と書く。README は、Databricks admin が app connection で `ai-gateway` scope を許可する、とはまだ書いていない。PR の minimum Cursor version は `3.19.0`（Workday から写した）。同じ PR は、古い desktop は Databricks の sign-in が Cursor の server 経由だと知らないので、おそらく `3.28.0` であるべき、と書く。
- 出典: [PR 754](https://github.com/cursor/plugins/pull/754) · [README](https://github.com/cursor/plugins/blob/main/third_party/databricks-genie-one/README.md)（2026-10-21 確認）
- 確認: 未

## Vanta

- 内容: Vanta plugin 1.0.0（PR 766、merged 2026-10-22）。compliance の test、control、framework、risk、vulnerability を読み、失敗した test の修正を手伝える。agent は risk の作成や policy の upload のように compliance data を変えられるので、変更は Vanta で見る。region ごとに MCP server が分かれる。`vanta-us` は `https://mcp.vanta.com/mcp`、`vanta-eu` は `https://mcp.eu.vanta.com/mcp`、`vanta-aus` は `https://mcp.aus.vanta.com/mcp`。使う region だけ接続する。sign in は Vanta account の MCP OAuth（Dynamic Client Registration と PKCE）で、貼る key は無い。各 server は `"placement": "server"` で、Grok Bot は Cursor の hosted path 経由で繋ぐ。minClientVersions は `cursor` 3.13.0。PR 766 は、3 接続の表示と、sign in しない 2 server がエラーになるかは未試験、Cursor または Grok Bot からの full sign-in と tool 一覧も未試験、と書く。tool は sign-in のあと出る。PR 768（merged 2026-10-23）は、この 3 つの region server を、region picker 付きの 1 server に置き換える。3 server に分かれる記述は PR 768 で置き換わる。
- 出典: [PR 766](https://github.com/cursor/plugins/pull/766) · [PR 768](https://github.com/cursor/plugins/pull/768)（2026-10-23 確認）
- 確認: 未

## Framer

- 内容: Framer plugin 1.0.0（PR 764、merged 2026-10-22）。site、page、CMS を読み、編集する。MCP は `https://mcp.framer.com/mcp`。sign in は Framer account の MCP OAuth（Dynamic Client Registration と PKCE）で、貼る key は無い。Framer の sign-in は `http://localhost` と `https` の return address を受け、`cursor://` と `grokbot://` は拒否する。`"placement": "server"` により、Grok Bot は Cursor の hosted `https` callback 経由で sign in する。minClientVersions は `cursor` 3.13.0。PR は、Cursor または Grok Bot からの full sign-in と tool 一覧は未試験、と書く。tool は sign-in のあとだけ出る。agent は site を変更し publish できるので、publish 前に Framer editor で見る。
- 出典: [PR 764](https://github.com/cursor/plugins/pull/764)（2026-10-22）
- 確認: 未

## Lark と Feishu

- 内容: PR 763（merged 2026-10-22）は 2 plugin。`lark` は国際向け Lark Suite で MCP は `https://mcp.larksuite.com/mcp`。`feishu` は中国向け Feishu で MCP は `https://mcp.feishu.cn/mcp`。どちらも MCP OAuth と Dynamic Client Registration で、API key、client secret、custom header は無い。Lark は sign in した account の Docs を検索・作成・取得・更新し、doc comment と file を扱い、IM の group と message を読む。Feishu README は、中国 server が国際 Lark と同じ tool 面を出す、と書く。国際向けは `lark`、中国向けはこの `feishu`。minClientVersions はどちらも `cursor` 3.13.0。この PR は #403 を置き換える。
- 出典: [PR 763](https://github.com/cursor/plugins/pull/763)（2026-10-22）
- 確認: 未

## Google Cloud BigQuery 1.1.0（breaking）

- 内容: PR 761（merged 2026-10-22）は plugin を 1.1.0 にし、OAuth をチーム所有の Google client に変える。Cursor 同梱の client は使わない。必須の team 変数は CLIENT_ID と CLIENT_SECRET。team admin は、次の connect の前に Cursor dashboard の team plugin 設定へ両方を置く。Google Cloud console では Web application の OAuth client を作り、Cursor の OAuth callback URL を redirect URI に足し、OAuth consent screen に `https://www.googleapis.com/auth/bigquery` を足す。MCP は `https://bigquery.googleapis.com/mcp`。minimum Cursor は 3.19.0。secret は暗号化されて Cursor の backend に残り、メンバーのマシンへは送られない。client を変えるとメンバーは sign out し、一度 reconnect する。既存の導入は、次の connect の前にこの値を置く。
- 出典: [PR 761](https://github.com/cursor/plugins/pull/761)（2026-10-22）
- 確認: 未

## Stable

- 内容: Stable plugin 1.0.0（PR 778、merged 2026-10-22）。virtual mailbox の mail を探し、scan した document を読み、Stable API を呼ぶ。MCP は `https://mcp.usestable.com/mcp`。auth は `x-api-key` header の `STABLE_API_KEY` で、必須。key は https://dashboard.usestable.com/settings/api-keys で作り、Dashboard → Plugins → Configure に置く。commit しない。tool は `find-mail`、`read-mail-document`、`list-endpoints`、`get-endpoint`、`search-endpoints`、`execute-request`。schema の正本は hosted runtime。minClientVersions は `cursor` 3.13.0。導入は Cursor Settings → Plugins で Stable を検索するか、`/add-plugin stable`。
- 出典: [PR 778](https://github.com/cursor/plugins/pull/778)（2026-10-22）
- 確認: 未

## changelog v0.75.2 の connector

- 内容: GitHub connector は repository の一覧、commit の比較、pull request の commit 一覧、branch と issue の comment を読む。組み込みの Gmail は draft と送信へ file を付け、reply all、forward のときの note、label の color ができる。Google Calendar は複数 event の create、update、delete を一段で行い、編集した event は別の時刻へずれない。Zoho CRM は sign in の前に、account の regional data center を選んで接続する。
- 出典: [changelog v0.75.2](https://x.ai/changelog/bot)（2026-10-23 確認）
- 確認: 未

## changelog v0.75.5 の email 転送と Slack の依頼者

- 内容: Bot は自分の inbox の email を、元の formatting、画像、添付のまま転送できる。Grok Bot 0.75.2 以降。Slack に出した各 message には、誰が頼んだかを記録するので、thread の誰もが誰の依頼かを聞ける。
- 出典: [changelog v0.75.5](https://x.ai/changelog/bot)（2026-10-23）
- 確認: 未

## X Money を one tap で繋ぐ

- 内容: changelog v0.75.2 は、X に sign in したうえで、chat、connector page、checkout から X Money を one tap で繋げると書く。上の catalog ページの説明とは別の項目である。
- 出典: [changelog v0.75.2](https://x.ai/changelog/bot)（2026-10-23 確認）
- 確認: 未

## Power BI

- 内容: Power BI plugin（PR 843、merged 2026-10-24 12:27 JST）。Grok Bot 向けの hosted MCP は `https://api.cursor.com/rest-mcp/power-bi/mcp`。Cursor には出さない。app は 0.30.0 以降。sign in は Microsoft Entra ID。read-only scope は Workspace.Read.All、Report.Read.All、Dataset.Read.All、offline_access。tool は list_workspaces、list_reports、list_datasets、render_report（PNG）。描画には Premium、Embedded、または Fabric の capacity と、tenant 設定「Export reports as image files」が要る。PR は、Entra の permission を足したあと provider を server 側で有効にする必要があり、Grok Bot からの Microsoft sign-in と tool call は未試験、と書く。live であることは未確認。
- 出典: [PR 843](https://github.com/cursor/plugins/pull/843)（2026-10-24）
- 確認: 未

## Krea

- 内容: Krea plugin（Grok Bot）。@krea_ai は、Grok の中から最良の model で画像と動画を生成できる、と書く（2026-10-24 01:00 JST）。Connect Apps catalog の Krea（id 70800059、Design、connector 1、skill 3）は、Krea の creative AI suite で画像と動画を generate、edit、enhance、produce する。追加は https://cursor.com/grok-bot/link/v1/plugin/add?id=70800059 で、そのあと sign in する。changelog v0.75.2 の組み込みの動画作成とは別である。価格と上限は出典に無い。cursor/plugins には無い。
- 出典: [@krea_ai](https://x.com/krea_ai/status/2113661958331494461) · [catalog](https://x.ai/bot/plugin/70800059) · [追加リンク](https://cursor.com/grok-bot/link/v1/plugin/add?id=70800059)（2026-10-24）
- 確認: 未
