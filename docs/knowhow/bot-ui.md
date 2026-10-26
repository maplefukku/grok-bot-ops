# bot-ui

ボットを起こす専用 UI。

## Grok Voice 3.0（Bot の voice mode）

- 内容: 公式ニュースは、Grok Voice 3.0 が Grok Bot の voice mode を動かすと書く。Voice Agent API は `wss://api.x.ai/v1/realtime`。`grok-voice-latest` は `grok-voice-3.0` の alias で、その alias の session はすでに 3.0。`grok-voice-2.0` は deprecated で、pin しているなら `model` を `grok-voice-3.0` にする。endpoint、session parameters、events、価格は 2.0 と同じ。default の `reasoning.effort` は `"high"`。`"none"` で reasoning を切る。移行時は system prompt を短くし、前モデルの workaround 用の指示を外す、と docs。
- 出典: [Introducing Grok Voice 3.0](https://x.ai/news/grok-voice-3) · [Speech to Speech](https://docs.x.ai/developers/model-capabilities/audio/speech-to-speech) · [x.com/SpaceXSI/status/2110416580899168305](https://x.com/SpaceXSI/status/2110416580899168305)（2026-10-14）
- 確認: 未

## Voice（話す / voice notes）

- 内容: Bot の voice 会話と voice notes の公式告知。詳細は [`updates.md`](./updates.md) の 2026-09-17 / 2026-09-18 行。
- 出典: [x.com/bot/status/2100659463569170779](https://x.com/bot/status/2100659463569170779) · [2101014478255247544](https://x.com/bot/status/2101014478255247544)
- 確認: 未

## zoo of production（コミュニティ報告）

- 内容: コミュニティ自己報告（@Lance_Coolie_Vr）。本文は「I have created my zoo of production.」。添付画像（出典画像）に Zoo Keeper / Platinum Chimp / Email Monkey / Schedule Monkey / Code Monkey / Project Odin / Zoo Secretary / Writing Monkey / Maintenance Monkey / Finance Monkey / Task Monkey の役割名が見える。画像由来の役割名 KEEP。Soft Flag N invent Zoo Keeper seat。
- 出典: [x.com/Lance_Coolie_Vr/status/2100004765216501827](https://x.com/Lance_Coolie_Vr/status/2100004765216501827)（2026-09-15）
- 確認: 未

## 役割 Bot + ライブ Google Forms 構築（SF コーヒーショップ scrape）

- 内容: Bot の identity / role を設定し、ライブストリームで SF コーヒーショップデータを scrape して Google Forms を組み立てたデモ。
- 出典: [x.com/Lucian_Lc7/status/2099991450360660061](https://x.com/Lucian_Lc7/status/2099991450360660061)（2026-09-15）
- 確認: 未

## 通常 Grok チャットで Bot に言及すると role memory を引く

- 内容: 通常の Grok チャットで Bot に言及すると、その Bot の role memory が引き込まれる、という報告。
- 出典: [x.com/grok/status/2099627316129169526](https://x.com/grok/status/2099627316129169526)（2026-09-15）
- 確認: 未

## 役割付き Bot をグループで議論させて記事化する

- 内容: 役割付き Bot をグループに入れ、Bot 同士で議論しながらネタ集め→記事作成まで進める用法。
- 出典: [x.com/pcefancom/status/2096819736596398276](https://x.com/pcefancom/status/2096819736596398276) · [x.com/i/article/2092026643426803712](https://x.com/i/article/2092026643426803712)（2026-09-07）
- 確認: 未

## アカウントとグループの実用上限

- 内容: 実用上限の目安は、アカウントあたり約 50 Bots、グループチャットあたり 6。
- 出典: [Designing Grok Bot for a world of persistent agents](https://x.ai/news/designing-grok-bot)（2026-09-03）
- 確認: 未

## Memory / Routines と Tools / Skills の境界

- 内容: Memory と Routines は Bot 単位。Tools と Skills はアカウント単位。
- 出典: [Designing Grok Bot for a world of persistent agents](https://x.ai/news/designing-grok-bot)（2026-09-03）
- 確認: 未

## /make-bot-ui

- 内容: 人がクリックするページを作り、このコンピュータ上のサーバが webhook routine へ JSON を POST する。sender key はサーバ設定に置き、ブラウザ・チャット・スキル本文には書かない。ページは Tailscale の tailnet に出せる。
- 出典: [pstack `/make-bot-ui`](https://github.com/cursor/plugins/blob/main/pstack/skills/make-bot-ui/SKILL.md)
- 確認: 未

## iPhone の Action Button で voice chat

- 内容: iPhone 15 Pro 以降で Grok Bot を 1.16 にする。Settings → Action Button → Shortcut → Grok Bot → Start Voice Chat。押すと Bot と話せる。
- 出典: [x.com/bot/status/2112252507762368684](https://x.com/bot/status/2112252507762368684) · [手順](https://x.com/bot/status/2112282506284445787)（2026-10-19）
- 確認: 未

## 電話の Calendar、Reminders、Contacts

- 内容: 電話の Calendar、Reminders、Contacts を Bot に頼める。reminder を足す、今日の calendar を見る、contact を調べる。iOS と Android で今ロールアウト中。投稿は「and more apps」と書き、それ以外のアプリ名は無い。
- 出典: [x.com/bot/status/2113393684209176718](https://x.com/bot/status/2113393684209176718)（2026-10-22）
- 確認: 未

## Library の Pinned と shortcuts sheet

- 内容: Library の page、file、link は Pinned に固定でき、その節は上に残り、端末間で同期する。行を hover か focus すると、誰がいつ送り、Page を誰が見られるかの preview が出る。keyboard shortcuts sheet は ⌘/ と、Help、profile menu、command palette から開く。composer の行頭で `>` を打つと block quote になり、quote 行の先頭で Backspace すると戻る。添付は drag か、Alt と矢印で並べ替えられる。
- 出典: [changelog v0.75.2](https://x.ai/changelog/bot)（2026-10-23 確認）
- 確認: 未

## changelog v0.75.5 の承認と送信

- 内容: Auto-review は、自分の言葉で頼んだ動作については確認が減る。approval card を拒否したあと、Bot は次の message までその動作をやり直さない。自分で頼んだ email と Slack は、Auto-review が許した時点で送る。routine やその他の turn の送信は draft のまま待つ。site へ sign in するため computer を渡すとき、その site に connector があれば connect card も出す。
- 出典: [changelog v0.75.5](https://x.ai/changelog/bot)（2026-10-23）
- 確認: 未

## changelog v0.75.8 の Auto-review と背景作業

- 内容: Bot は、確認する card の上で、Auto-review の rule を 1 つ足す、変える、外すことを提案できる。Grok Bot 0.75.2 以降。Auto-review は approval card を出す前にもう一度見る。Bot が自分の routine を保存または編集することは、それだけでは risky と扱わない。背景の作業が終わると、Bot は頼まれたことを仕上げ、次に何をするかを言う。自分から、または別の agent の承認では動かない。
- 出典: [changelog v0.75.8](https://x.ai/changelog/bot)（2026-10-24）
- 確認: 未
