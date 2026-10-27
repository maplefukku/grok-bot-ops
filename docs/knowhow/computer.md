# computer

Bot のコンピュータ（Cloud Agent、ネットワーク、マシン上の永続化）。

## Cloud agent の canvas 共有と Environments API

- 内容: canvas toolbar の Publish で共有を公開または更新し、リンクをコピーしてチームに送る。開いたチームメンバーは read-only。dashboard の Shared Canvases は自分が公開したものだけを並べ、teammate の分はリンクをもらって開く。共有できるのは有料プラン（Premium 以上、Teams、Enterprise、legacy の Pro、Pro+、Ultra）。free は共有を作れない。開けるのは team のメンバーなので、team に入っている必要がある。individual の有料でも team に属していれば共有できる。storage を許す privacy mode が要り、Legacy Privacy Mode は共有を止める。team admin は team settings の Shared Canvases で組織ごとオフにできる。Environments API は Cloud Agents API v1 の public beta で、一般提供前に変わり得る。作成は POST `/v1/environments`（`https://api.cursor.com`）。owner は `personal` か `team`。name は 255 文字までで、その owner の他の environment と重ならない。repos は最大 300。届かない repository は `400 repository_access`。不正な `environmentJson` は `400 validation_error`。同じ name は `409 environment_name_conflict`。changelog の repository 上限は 300、同日の @cursor_ai は up to 500 repos と書いている。どちらも large environments は 5x faster。
- 出典: [changelog](https://cursor.com/changelog/cloud-agent-canvases-and-environments) · [Sharing canvases](https://cursor.com/docs/agent/tools/canvas) · [Environments](https://cursor.com/docs/cloud-agent/api/endpoints) · [x.com/cursor_ai/status/2111193957527146711](https://x.com/cursor_ai/status/2111193957527146711) · [2111193969355084011](https://x.com/cursor_ai/status/2111193969355084011) · [2111193980981665837](https://x.com/cursor_ai/status/2111193980981665837)（2026-10-16）
- 確認: 未

## Origin App Marketplace の公開と制約

- 内容: Origin は early beta。Apps は codebase settings（`https://cursor.com/codebase/settings/apps`）で入れ、repository の Apps tab で有効なものを見る。early beta では marketplace の閲覧に Cursor への sign in が要る。Depot と Buildkite は Origin-hosted の repository だけで、GitHub から mirror した repo では動かない。mirror は CI を GitHub に残す。公開は、namespace で private app を作り、Origin API（app JWT と installation access token、webhook、check run、PR comment、review）に対して組み、Visibility を Public にしてから、slug、suggested tags、demo video を添えて提出する。video は install、uninstall、中核の流れを含み、about 5 to 10 minutes、sign-in なしで見られること。Cursor が承認すると Listed。公開前のインストール URL の `client_id` は slug ではなく app ID（`app_01…`）。visibility は Private、Public、Listed。Public には少なくとも 1 つの default scope が要る。unlist または Private に戻すと marketplace からは消えるが、既存 install は動いたまま。一度 Listed だったものを Private にしてから Public に戻しても再掲載されず、再提出が要る。Origin Apps plugin は、生きている Origin API docs への質問と、既存 app の移植の計画に答えられる。
- 出典: [changelog](https://cursor.com/changelog/origin-app-marketplace)（2026-10-13） · [Origin Apps](https://cursor.com/docs/origin/apps) · [Publish](https://cursor.com/docs/origin/apps/publish)
- 確認: 未

## Factory OpenCompute

- 内容: @FactoryAI は OpenCompute を、選んだ runtime 上の agent sandbox 向け self-hosted orchestrator として紹介している。自律的なソフトウェア開発を採るのに、code と context を他人の cloud に渡す必要はない。remote agent の fleet を、自分の VPC に置いたままスケールする、と投稿は書く。
- 出典: [x.com/FactoryAI/status/2110403273903808988](https://x.com/FactoryAI/status/2110403273903808988)（2026-10-14）
- 確認: 未

## GitHub Copilot app の巨大 PR 描画

- 内容: GitHub Copilot app の pull request view を、巨大な diff と inline review comment 向けに作り直した、という GitHub Blog。開いた open source の PR は 2,200 files、over a million changed lines、more than 400 inline review comments。comment の高さは markdown の折返し、展開できる details、開いた reply box、まだ読み込み中の画像に依存し、描画するまで分からない。code 行は高さが事前に分かる geometry のままにし、review thread など高さ不明のものは別の dynamic block にした、と記事は書く。
- 出典: [Rendering huge pull requests in the GitHub Copilot app](https://github.blog/engineering/user-experience/rendering-huge-pull-requests-in-the-github-copilot-app/)（2026-09-23） · [x.com/github/status/2109707357857218667](https://x.com/github/status/2109707357857218667)（2026-10-12）
- 確認: 未

## Cloud Agent 起動時に MCP の on/off が無い — コミュニティ報告

- 内容: コミュニティ報告: Grok Bot から Cloud Agent を起動するとき、使う MCP サーバを有効/無効にする手段が無い。毎回の CA 起動で使わない MCP を付けっぱなしにしない運用が必要、という指摘。
- 出典: [x.com/LukeDiebold/status/2102925714928603480](https://x.com/LukeDiebold/status/2102925714928603480)（2026-09-24）
- 確認: 未

## コーディングは Cursor 等の harness — Bot をソフトウェア部門ゲートにしない

- 内容: Grok Bot harness は一般タスクと delegation に向く。コーディングは Cursor（または別の coding harness）を優先する。coding harness が既に包んでいるゲートを Bot 側で二重に作らない、という整理。
- 出典: [x.com/PhilShteuck/status/2103219368679403916](https://x.com/PhilShteuck/status/2103219368679403916)（2026-09-24）
- 確認: 未

## Grok Bot を日次 router、Cursor を think-then-code 席

- 内容: Grok Bot を日次の router、Cursor を think-then-code 席に分けると、高コストな coding model を routine チケットから外しやすい、という tip。
- 出典: [x.com/ChristianXCesar/status/2103229143500386397](https://x.com/ChristianXCesar/status/2103229143500386397)（2026-09-24）
- 確認: 未

## desktop 53 perf fixes（poteto 一次）

- 内容: Grok Bot desktop にここ数日で 53 件の perf fix。例: flaky reconnect 60s→0.7s、laptop wake 23s→1s、Computer view 切替 868ms→27ms、長い chat を開く速度改善。
- 出典: [x.com/poteto/status/2102504221648339170](https://x.com/poteto/status/2102504221648339170)（2026-09-22） · 公式まとめ [x.com/bot/status/2102532704797610313](https://x.com/bot/status/2102532704797610313)
- 確認: 未

## モバイルの Bot から仕事場 PC へ — コミュニティ報告（未確認）

- 内容: 未確認のユーザ報告。phone の Grok Bot から、仕事場に置いてきた PC が online のまま届くか見た、という話。同一投稿は remote desktop アプリをインストール中であることと、X credentials を守ること（求められたことは何でもする、という警告）にも触れる。
- 出典: [x.com/duncanstives/status/2102165842230116686](https://x.com/duncanstives/status/2102165842230116686)（2026-09-21）
- 確認: 未

## quota tip — VM ターミナルから Grok Build へコーディングタスク

- 内容: Grok Bot にコーディングタスクを VM ターミナル経由で Grok Build に送らせる（別 rate-limit pool）。
- 出典: [x.com/theaaron/status/2102134190540255686](https://x.com/theaaron/status/2102134190540255686)（2026-09-21）
- 確認: 未

## ローカル Mac で Grok CLI + Cursor CLI を併用（Bot VM token 節約）

- 内容: Bot VM の token 消費を避けるため、ローカル Mac / computer 上でも Grok CLI と Cursor CLI を動かす tip。
- 出典: [x.com/Kevin_Logan/status/2102134995108110395](https://x.com/Kevin_Logan/status/2102134995108110395)（2026-09-21）
- 確認: 未

## Bot モデルを Cursor Usage から推定

- 内容: Cursor Settings → Dashboard → Usage の `Grok-Bot-Default` ラベル配下で、usage graph に underlying model（例: cursor-grok-4.6-high-fast）が出る、という報告。
- 出典: [x.com/theaaron/status/2102127976699904354](https://x.com/theaaron/status/2102127976699904354)（2026-09-21）
- 確認: 未

## 旧 Mac + Tailscale + custom connector（メッセージ / カレンダー）

- 内容: 旧 Mac をサーバにし、Tailscale 越しの custom connector で Bot からメッセージ送信やカレンダー reminder / notes の閲覧・更新。
- 出典: [x.com/joshidell/status/2102166659460985186](https://x.com/joshidell/status/2102166659460985186)（2026-09-21）
- 確認: 未

## 重い仕事は Cloud Agent に振る skill

- 内容: livestream 末尾の token tip「prefer cloud agent for heavy work」。
- 出典: [x.com/kononovme/status/2100333225885180238](https://x.com/kononovme/status/2100333225885180238)（2026-09-16）
- 確認: 未

## 開発は Cursor Projects、日常は Grok Bot

- 内容: 永続コンテキスト目的だけで Bot から Cloud Agent を起動し続けなくてよい、という切り分け。
- 出典: [x.com/2020_hira/status/2100169429921497413](https://x.com/2020_hira/status/2100169429921497413)（2026-09-16）
- 確認: 未

## usage 分離: GitHub/Origin 接続と Cloud Agent

- 内容: GitHub/Origin を接続し、重い作業は Cloud Agent に任せて Grok Bot 枠と Cursor 枠を分ける。
- 出典: [x.com/TSLAshareholder/status/2099862329529860119](https://x.com/TSLAshareholder/status/2099862329529860119)（2026-09-15）
- 確認: 未

## Cloud Agent に短いレビュー動画を PR description に

- 内容: Cloud Agent に短いレビュー動画を撮らせ PR description に添付。verification skill を always-on にする（Galaxy livestream / poteto）。
- 出典: [x.com/ChrisSimpson/status/2099973597947428927](https://x.com/ChrisSimpson/status/2099973597947428927)（2026-09-15）
- 確認: 未

## credit 監査 Bot（cloud / screenshot 消費）

- 内容: Grok Bot が cloud computer と頻繁な screenshot で credit を消費したため、credit 監査 Bot を作った、という報告。
- 出典: [x.com/KOJIRYUJI1/status/2100005121895862548](https://x.com/KOJIRYUJI1/status/2100005121895862548)（2026-09-15）
- 確認: 未

## Galaxy Day 1 スタック（Cursor cloud agents + computer-use routines）— `@grok` LLM 返信

- 内容: `@grok` LLM 返信の Day 1 例（GitHub、Vercel+PlanetScale、Cursor cloud agents、Slack、Notion、computer-use routines、専門 Bot）。公式ライブの SoT は `@bot` Day 1 と [x.ai/galaxy](https://x.ai/galaxy)。この URL は Route egress 項と同型の `@grok` LLM 返信であり、`updates.md` には載せない。
- 出典: [x.com/grok/status/2100005127125889216](https://x.com/grok/status/2100005127125889216)（2026-09-15）
- 確認: 未

## Hermes 保守は SSH、会話は API、@bot でオーケストレーション

- 内容: Hermes Agent の保守レールは SSH のまま。Hermes との chat は API。メンテナンスの束ねは @bot に任せる、という分離。
- 出典: [x.com/PixelRainbowNFT/status/2099998602944794823](https://x.com/PixelRainbowNFT/status/2099998602944794823)（2026-09-15）
- 確認: 未

## Route egress（Settings → Computer）— 公式 docs + @bot 告知

- 内容: Settings → Computer の「Route egress through this desktop」をオンにすると、Grok Bot の computer の web 通信が今の desktop を通る。送り先には desktop の IP が見え、その端末から届くネットワークに Bot が入れる。設定は desktop ごと。Enterprise admin が Allow Local Egress を切るとトグルはロックされる。2026-09-22 に公式 `@bot` が own-network routing を告知した（[`updates.md`](./updates.md) 参照）。
- 出典: [docs.x.ai/grok-bot/settings-and-notifications](https://docs.x.ai/grok-bot/settings-and-notifications)（2026-09-30 取得） · 公式告知 [x.com/bot/status/2102532701886861429](https://x.com/bot/status/2102532701886861429)（2026-09-22） · 2 次: `@grok` LLM 返信 [x.com/grok/status/2099610497259552906](https://x.com/grok/status/2099610497259552906) · [2099641777405743447](https://x.com/grok/status/2099641777405743447)（2026-09-14 UTC）
- 確認: 未

## Projects Manager = 1 project channel + 専門 Bot — コミュニティ例

- 内容: 1 project channel に専門 Bot を束ねる構成例。quote 先は作者自身の 2026-08-19 記事。CreateChannel + CBO + Cursor Projects WRAP は既存 LIVE。新 seat invent 不要。
- 出典: [x.com/0xRafy/status/2098901444644458629](https://x.com/0xRafy/status/2098901444644458629)（2026-09-12 UTC）
- 確認: 未

## Outer loop Bot → Cursor Cloud Agent（公式 Grok Bot 101）

- 内容: dirty context をコーディング harness に入れないため、収集・整理は Grok Bot、実装は Cursor Cloud Agent に分ける、という公式ガイド上のパターン。
- 出典: [Grok Bot 101](https://x.ai/bot/guides/grok-bot-101)（2026-09-11）
- 確認: 未

## Cursor Projects をチャット用の特別フォルダとして使う

- 内容: Projects をチャットの特別フォルダとみなし、sidebar の既存チャットを Project にドラッグできる、という poteto の比喩・使い方。公式の定義ではない。公式は coordinator（コードは書かず、独自コンピュータ上で subagent を監督し、Slack / schedule / PR CI の Subscriptions で未プロンプト動作する）であり、公式発表の記録は [`updates.md`](./updates.md) にある。
- 出典: [x.com/poteto/status/2098186080839475568](https://x.com/poteto/status/2098186080839475568)（2026-09-10） · [tip](https://x.com/poteto/status/2098186602241822974)
- 確認: 未

## pstack を Projects と併用

- 内容: Projects と pstack を併用し、先に /setup-pstack でモデルを選ぶ、という poteto の助言。
- 出典: [x.com/poteto/status/2098181726782841254](https://x.com/poteto/status/2098181726782841254)（2026-09-10） · [pstack](https://cursor.com/marketplace/cursor/pstack)
- 確認: 未

## Grok Bot hacks 動画（webhook bridge、plugins / Composio、marketplace、スマホからのコンピュータ操作 ほか）

- 内容: 動画で扱う項目: webhook bridge、plugins と Composio、Bot marketplace、スマホからのコンピュータ操作、project channels、agent inboxes、Command K、token 効率のよいスクリプト。plugins の話（[`plugins.md`](./plugins.md)）と marketplace の話（[`templates.md`](./templates.md)）も同じ出典に含まれる。
- 出典: [x.com/moritzkremb/status/2097717640479334652](https://x.com/moritzkremb/status/2097717640479334652)（2026-09-09）
- 確認: 未

## Cloud Agent は同じ agent への reply で同一ブランチを続けさせる

- 内容: Grok Bot から Cursor Cloud Agent に同じブランチで作業を続けさせたいとき、nudge ごとに第二の agent を立てない。同じ agent に reply すると branch と context を保ったまま続く、という報告。
- 出典: [x.com/iPuneetSingh/status/2097453766635044890](https://x.com/iPuneetSingh/status/2097453766635044890)（2026-09-08）
- 確認: 未

## CA 枯渇後に Devin CLI を Bot 内で使う

- 内容: Cursor Cloud Agent の usage を使い切ったあと、Grok Bot 内で Devin CLI を動かしてコーディングを続ける、という報告。
- 出典: [x.com/danielkhunter/status/2096844273115386245](https://x.com/danielkhunter/status/2096844273115386245)（2026-09-07）
- 確認: 未

## Mac mini 上の Claude Max を Bot がオーケストレーション

- 内容: Cloud Agent 費用が急増したため、自宅 Mac mini の Claude Max を Grok Bot がオーケストレーション／pstack ループする戦術に切り替えた、という報告。
- 出典: [x.com/JoshuaMakeSmile/status/2096765875080835191](https://x.com/JoshuaMakeSmile/status/2096765875080835191)（2026-09-07）
- 確認: 未

## コードは Bot コンピュータに書かせない（週次枠）

- 内容: コード作業を Grok Bot コンピュータ上で書かせると weekly bucket を消費する。リポジトリは Cloud Agent に送り、マージする運用にする、という報告。
- 出典: [x.com/nikvassev/status/2096629495591502187](https://x.com/nikvassev/status/2096629495591502187)（2026-09-06）
- 確認: 未

## Bot に Basecamp + Claude Code を渡す

- 内容: Bot に専用の Basecamp アカウントを渡し、Bot マシンに Claude Code を入れてコーディングを任せ、コンテンツは Spiral（@every）に振る、という用法。
- 出典: [x.com/jawestenberg/status/2096738605104521264](https://x.com/jawestenberg/status/2096738605104521264)（2026-09-06）
- 確認: 未

## Bot を増やせとは公式は書いていない

- 内容: Bot を増やせとは公式は書いていない。仕事の持ち主を1体置き、詰まりで専門席を足し、共有1台では成果物で受け渡し、戻せないことだけ人が触る。
- 出典: [x.com/madogiwacowork/status/2096721289599922688](https://x.com/madogiwacowork/status/2096721289599922688)（2026-09-06）、[Grok Bot](https://docs.x.ai/grok-bot)、[Use the computer and apps](https://docs.x.ai/grok-bot/computer-and-apps)
- 確認: 未

## Tailscale exit node

- 内容: 常時稼働の home Mac を Tailscale exit node にし、Bot の通信をそこ経由にする。datacenter IP でログインが弾かれる対策。
- 出典: [x.com/vohnvest/status/2095159871239053392](https://x.com/vohnvest/status/2095159871239053392)（2026-09-02）
- 確認: 未

## Cloud Agent のモデル指定

- 内容: Cloud Agent 起動時に使うモデルを Bot に明示できる。条件付きのモデル選択も指示できる。
- 出典: [x.com/lingxi/status/2094522117362688471](https://x.com/lingxi/status/2094522117362688471)（2026-08-31）
- 確認: 未

## マシン上の SQLite

- 内容: Bot マシン上の SQLite に PMM や SNS コンテンツなどを置いて永続化する用法。
- 出典: [x.com/harriskennyx/status/2094528680160891220](https://x.com/harriskennyx/status/2094528680160891220)（2026-08-31）
- 確認: 未

## Tailscale で tailnet に繋ぐ

- 内容: Bot を tailnet に繋ぐ。キーは reusable と ephemeral にする。
- 出典: [x.com/hopedj/status/2093724286309564619](https://x.com/hopedj/status/2093724286309564619)（2026-08-29）
- 確認: 未

## Computer Use

- 内容: agent は browser だけでなく、コンピュータ上のどの app でも click と type ができる。例は、作った機能を試すため iOS Simulator を動かす。Cursor は task が要するとき自分で使い、prompt で Computer Use を @-mention しても頼める。試すには Cursor を更新する。投稿はプランの範囲を書いていない。cursor.com/changelog には、2026-10-23 の確認時点で Computer Use の項目は無い。
- 出典: [x.com/cursor_ai/status/2113661506634305834](https://x.com/cursor_ai/status/2113661506634305834) · [2113661518780998003](https://x.com/cursor_ai/status/2113661518780998003) · [changelog](https://cursor.com/changelog)（2026-10-23）
- 確認: 未

## Agent SDK

- 内容: Cursor Agent SDK は GA（changelog の日付は Oct 20, 2026）。agent は project folder で、中身は instructions.md、tools/（typed TypeScript）、skills/、mcp-connections/、channels/。`npx @cursor/agent-sdk init ./my-bot` のあと、`agent-sdk dev` で local playground。`--template` は security reviewer、owners-policy approver、PR autofixer、Linear/Jira triager。`agent-sdk deploy` は Cursor 上で動かし、self-hosting もできる。trigger は GitHub、GitLab、Bitbucket の PR、comment、CI event、Slack の mention と DM、webhook、cron。`agent-sdk eval` は eval を local か CI で走らせる。`agent-sdk github replay <pr-url>` は本物の PR を webhook payload として再生する。
- 出典: [changelog](https://cursor.com/changelog) · [x.com/cursor_ai/status/2114793714531102901](https://x.com/cursor_ai/status/2114793714531102901)（2026-10-20）
- 確認: 未

## DeepSeek V4.1 Flash

- 内容: DeepSeek V4.1 Flash は Cursor Settings の Models にある。
- 出典: [x.com/cursor_ai/status/2114839997568405608](https://x.com/cursor_ai/status/2114839997568405608)
- 確認: 未
