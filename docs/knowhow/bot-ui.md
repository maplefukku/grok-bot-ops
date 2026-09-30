# bot-ui

ボットを起こす専用 UI。

## Voice（話す / voice notes）

- 内容: Bot の voice 会話と voice notes の公式告知。詳細は [`updates.md`](./updates.md) の 2026-09-17 / 2026-09-18 行。
- 出典: [x.com/bot/status/2100659463569170779](https://x.com/bot/status/2100659463569170779) · [2101014478255247544](https://x.com/bot/status/2101014478255247544)
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
