# bot-ui

ボットを起こす専用 UI。

## 専門 Bot 多体 + Zoo Keeper（Code / Email / Schedule）

- 内容: 本番向け Grok Bot の zoo。Zoo Keeper と Code / Email / Schedule など役割 Bot を分ける構成例。
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
