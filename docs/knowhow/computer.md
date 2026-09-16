# computer

Bot のコンピュータ（Cloud Agent、ネットワーク、マシン上の永続化）。

## Settings の routine webhook（request_local_computer）

- 内容: Settings に routine webhook を貼れる。agent が `request_local_computer` 経由でノート PC に到達できる。キーは rest 時に暗号化。HTTP 200 は bot 起動を意味し、ローカル作業の完了を意味しない。
- 出典: [x.com/vvedantb/status/2100143317006610777](https://x.com/vvedantb/status/2100143317006610777)（2026-09-16）
- 確認: 未

## Bot 専用メールアドレス

- 内容: Grok Bot 用のメールアドレスを持たせる手順の community how-to（X 記事）。
- 出典: [x.com/nateherk/status/2100018258355110346](https://x.com/nateherk/status/2100018258355110346)（2026-09-16）
- 確認: 未

## コーディング agent 向けサンドボックス map（auto-approve）

- 内容: Docker Sandboxes、shuru、Brood Box など microVM オプションを含む、コーディング agent 用サンドボックスの map。auto-approve の文脈。
- 出典: [x.com/minchoi/status/2099881374710723013](https://x.com/minchoi/status/2099881374710723013)（2026-09-15）
- 確認: 未

## Route egress（Settings → Computer）— ユーザ報告

- 内容: Settings → Computer から desktop 経由 egress を有効にできる、というユーザ報告（datacenter IP 対策と Tailscale exit node 項と同系）。`docs.x.ai/grok-bot/computer-and-apps` には 2026-09-15 時点で Route egress の記載なし。公式 `@bot` / docs が取れるまで `updates.md` には載せない。
- 出典: [x.com/grok/status/2099610497259552906](https://x.com/grok/status/2099610497259552906) · [2099641777405743447](https://x.com/grok/status/2099641777405743447)（2026-09-14 UTC）
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
