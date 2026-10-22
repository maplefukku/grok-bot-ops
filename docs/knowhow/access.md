# access

加入プランと、使えるアプリ。

## The X Subscription

- 内容: 発表ページの月額は Free $0、Plus $8/month、Premium $30/month（4x Plus。以前は SuperGrok と Cursor Pro と X Premium+ を合わせて $90/month）、Super $100/month（15x Plus）、Ultra $200/month（50x Plus）。pricing は allowance が weekly に更新され、Grok の中では Chat、Imagine、Voice、Bot が同じ pool。Grok API はその pool から引かない、と models-and-pricing の FAQ。@cursor_ai は、有料プランが Cursor、Grok Build、他の Grok 製品で 1 つの usage pool を共有し、同等の Cursor プランと比べ Grok モデルの coding usage が twice で、Premium、Super、Ultra に Grok Bot が含まれると書いている。pricing の Premium 行にも Grok Bot がある。third-party models は Premium 以上で API list price。使った分だけ払い、spending caps を置ける。@cursor_ai は、新プランでは Grok の usage を増やすため、Cursor の third-party models が API pricing に移る、と書いている。Team は Premium、Super、Ultra を individual と同じ per-seat 価格で、古い Cursor Teams より per seat が安く coding usage は 3x。SSO、admin controls、consolidated billing、usage analytics、SOC 2。Enterprise は 1 dashboard と、Grok と Cursor をまたぐ 1 usage pool。既存の SuperGrok、Cursor、X Premium は現行の plan、price、features のまま保てる。切替の limited-time offers は billing settings。
- 出典: [Introducing The X Subscription](https://x.ai/blog/x-subscription) · [pricing](https://x.ai/pricing) · [models and pricing](https://cursor.com/docs/models-and-pricing) · [x.com/SpaceXSI/status/2109783335296008414](https://x.com/SpaceXSI/status/2109783335296008414) · [x.com/cursor_ai/status/2109783879490191502](https://x.com/cursor_ai/status/2109783879490191502)（2026-10-12）
- 確認: 未

## Tesla 車内 Grok Bot は当面 SuperGrok Heavy

- 内容: Tesla 公式: 車内 Grok Bot は Currently available to SuperGrok Heavy subscribers, with more tiers to follow。
- 出典: [x.com/Tesla/status/2102431173314273633](https://x.com/Tesla/status/2102431173314273633)（2026-09-22）
- 確認: 未

## quota: Grok Bot 週枠と Cursor Cloud Agent

- 内容: 通常の会話・routine・CUA・shell・MCP は Grok Bot 週枠。例外は Bot が起動した Cursor Cloud Agent のみ Cursor プラン側。
- 出典: [forum.cursor.com/t/can-cursor-clarify-exactly-which-grok-bot-usage-counts-against-the-weekly-pool-vs-cursor-models-other-models/170951](https://forum.cursor.com/t/can-cursor-clarify-exactly-which-grok-bot-usage-counts-against-the-weekly-pool-vs-cursor-models-other-models/170951)（2026-09-10） · [x.com/ChingHanHo/status/2100395137469997112](https://x.com/ChingHanHo/status/2100395137469997112)（2026-09-17）
- 確認: 未

## Grok Heavy の weekly limit と Grok Bot usage は別

- 内容: Grok Heavy の weekly limit を使い切っても Grok Bot usage は別枠。Heavy 枯渇後も Bot SSH で続けた、という報告。
- 出典: [x.com/VibeDrummer/status/2099989791492149469](https://x.com/VibeDrummer/status/2099989791492149469)（2026-09-15）
- 確認: 未

## weekly limit 前に usage の使い方を直す（Ultra への安易なアップグレードを避ける）

- 内容: Grok Bot の weekly limit で Cursor Ultra に上げる前に、公式 docs 由来の使い方ルールを直す。メーターは message 数ではなく agent steps と tokens。曖昧タスクは wander して枠を食う、という要点。
- 出典: [x.com/unicodef1wn/status/2098087818564182038](https://x.com/unicodef1wn/status/2098087818564182038)（2026-09-10）
- 確認: 未

## Grok Heavy の usage pool は 3 つ

- 内容: Grok Heavy 加入では usage pool が Grok Build / Imagine / chat、Grok Bot、Cursor Cloud Agent の 3 つに分かれる。Grok Build の quota のほうが Bot の quota より長持ちするように見えるので、作業を Grok Build に寄せて Bot の quota を温存している、という報告。
- 出典: [x.com/justsomeguy2365/status/2097754146204193122](https://x.com/justsomeguy2365/status/2097754146204193122)（2026-09-09）
- 確認: 未

## コーディング時の token 消費と設定確認

- 内容: Grok Bot でコーディングすると設定次第で token 消費が大きい。設定を確認するガイド記事あり。
- 出典: [x.com/skunky/status/2097424315771994523](https://x.com/skunky/status/2097424315771994523) · [x.com/i/article/2097409599611830272](https://x.com/i/article/2097409599611830272)（2026-09-08）
- 確認: 未

## Cloud Agent 利用上限が UI で見えにくい

- 内容: 開発は Cursor Cloud Agent 経由だと気づいたあと、"You've hit your Cloud Agent usage limit." のメールで上限に達した。limits が Grok Bot UI 上でははっきり見えない、という報告。
- 出典: [x.com/NHv2Pro/status/2096948213282643975](https://x.com/NHv2Pro/status/2096948213282643975)（2026-09-07）
- 確認: 未

## 課金は Grok Bot / Grok Build / Cursor Cloud Agent で別

- 内容: Grok Bot、Grok Build、Cursor Cloud Agent（model selector）は別々の課金だという説明（返信での主張）。
- 出典: [x.com/icebakbum/status/2096507242820612547](https://x.com/icebakbum/status/2096507242820612547)（2026-09-06）
- 確認: 未

## Enterprise（2026-09-03）

- 内容: Grok / Cursor Enterprise 顧客は今後 2 週間無料で組織を招待できる。既存シートが無いメンバーも含む。
- 出典: [Grok Bot for Enterprise](https://x.ai/news/grok-bot-for-enterprise)（2026-09-03）
- 確認: 未

## Enterprise を live と扱う条件

- 内容: Enterprise は、2 週間の無料ウィンドウ内の Grok または Cursor Enterprise シートでのみ live 扱いすべき、という運用注意。
- 出典: [x.com/johnnynelai/status/2095675192039350349](https://x.com/johnnynelai/status/2095675192039350349)（2026-09-04）
- 確認: 未

## 加入

- 内容: 2026-08-26 の公式発表では、Grok Bot は SuperGrok / SuperGrok Plus / SuperGrok Heavy、Cursor Pro / Pro+ / Ultra、Cursor Teams（Standard と Premium）に含まれる。Enterprise はウェイトリスト。
- 出典: [Grok Bot is now included with more plans](https://x.ai/news/grok-bot-more-plans)（2026-08-26）
- 確認: 未

## 利用量

- 内容: Settings の Usage & Billing（出るアカウントだけ）は、週次の included usage と on-demand usage を見せる。アカウントメニューに Weekly usage が出ることもある。
- 出典: [Settings and notifications](https://docs.x.ai/grok-bot/settings-and-notifications)（2026-08-29 確認）
- 確認: 未

## アプリ

- 内容: 公式ページごとに書く（4 docs 同一マトリクスは invent しない。Bot changelog 新行は立てない）。[Get started](https://docs.x.ai/grok-bot/get-started) は desktop を macOS / Windows / Linux、mobile は generic（"You can also set up and use Grok Bot on mobile"；iPhone / Android の言及あり、**iPad は無い** — get-started を iPad の 1° にしない）。[overview](https://docs.x.ai/grok-bot/overview) 本文は macOS / Windows / Linux / iOS / Android。iPad の 1° は overview FAQ "Which platforms"、[mobile](https://docs.x.ai/grok-bot/mobile) の "The iOS app also runs on iPad (iPadOS 18 or later)"、[FAQ](https://docs.x.ai/grok-bot/faq) platforms 節。mobile Requirements は iPhone / Android phone。Android は 2026-09-02 に @bot が available on Android と告知。Play Store にはパッケージ `ai.x.grok.bot` の掲載がある。
- 出典: [Get started](https://docs.x.ai/grok-bot/get-started)、[overview](https://docs.x.ai/grok-bot/overview)、[FAQ](https://docs.x.ai/grok-bot/faq)、[Grok Bot for Mobile](https://docs.x.ai/grok-bot/mobile)（2026-09-22 確認）、[x.com/bot/status/2095168633559462197](https://x.com/bot/status/2095168633559462197)（2026-09-02）、[Play Store `ai.x.grok.bot`](https://play.google.com/store/apps/details?id=ai.x.grok.bot)
- 確認: 未

## The X Subscription の unify は完了すると戻せない

- 内容: 切替は任意で、変えるか解約するまで現行プランは続く。既存の Cursor 顧客は、unify せずに tier を変え、teammate を招待できる。例外は Apple App Store 請求のプランで、先に switch が要る。unify は対象の Cursor と Grok を 1 account、1 workspace、1 plan、1 bill にまとめ、個人の X account を足すと X の benefits が付く。完了した unification は永久で、取り消せず、Support も取り消せない。完了後の plan、billing、settings は grok.com/dashboard。開始地点は cursor.com/unify（Cursor）、accounts.x.ai/unify（Grok）、x.com の subscription settings。X から始める経路には Cursor が含まれないので、有料の Cursor は Cursor から始める。team は cursor.com/unify/team。Cursor は owner か admin が始め、既存の Grok team を足すにはその team の owner か billing admin でもある。Grok team からは owner、admin、billing admin。mobile app は既存の支払い者を web へ送る。email は一致しなくてよい。sign in しているその account を繋ぎ、確認前に各 account を見る。work と personal は分ける。違う account なら checkout の前に止めて Support に連絡する。組み合わせられないのは Enterprise と personal、personal と team、組織管理または affiliate の X。各 X account は 1 つの Grok account にしか入らない。未払いまたは past-due の invoice があると進めない。checkout で旧 subscription は解約され、未使用分は prorated refund。例外として、Apple App Store の Cursor はこちらで解約も refund もできないので、iOS Settings で解約し、refund は Apple に求める。App Store の Grok、Grok Bot、X Premium はこちらが解約し、未使用分の refund を Apple に依頼し、金額は Apple が決める。Google Play の Grok、Grok Bot、X Premium は、switch のあと subscriptions を見て、まだ更新する設定ならそこで解約する。Cursor の third-party models（Claude、GPT）はプランに含まれず、API list price で prepaid credit から払う。docs に公開日は無い。
- 出典: [How to unify accounts](https://docs.x.ai/x-subscription/unify-accounts) · [Unification eligibility](https://docs.x.ai/x-subscription/eligibility) · [Do I have to switch?](https://docs.x.ai/x-subscription/do-i-have-to-switch)（2026-10-21 確認）
- 確認: 未

## 1Password for Agents

- 内容: @bot は、共有したい login を承認すると Bot が sign in する、と書く。今後数日でユーザーへロールアウトする。@1Password は 1Password for Agents を発表し、Grok Bot を launch partner に含む。agent が sign-in form に着くと vault の credential を求め、承認すると 1Password が宛先の site へ直接 auto-fill し、agent は credential を見たり持ったりしない。connector に opt-in しない限り、agent は vault に触れない。changelog v0.53.0（September 15, 2026）は、Mac で Marketplace から 1Password を繋ぐ、と書く。今回の投稿はその Mac の Marketplace 接続とは別である。
- 出典: [x.com/bot/status/2113332983226831339](https://x.com/bot/status/2113332983226831339) · [x.com/1Password/status/2113276767582498943](https://x.com/1Password/status/2113276767582498943) · [changelog v0.53.0](https://x.ai/changelog/bot)（2026-10-22 確認）
- 確認: 未
