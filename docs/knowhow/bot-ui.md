# bot-ui

ボットを起こす専用 UI。

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
