# anti-job（spend / sign / send）

## Purpose

Planner が 2026-09-07 に ADOPT した Haggle anti-job の Domain WRAP である。判断行は [`trend-log.md`](../decisions/trend-log.md) の 2026-09-07 行である。適用 issue は [#90](https://github.com/maplefukku/grok-bot-ops/issues/90) である。一次は公式 Marketplace の [Haggle Bot](https://x.ai/bot/marketplace/bots/haggle-bot)、[Setting Grok Bot loose on procurement](https://x.ai/news/grok-bot-procurement)（2026-09-04）、[Approvals, security, and privacy](https://docs.x.ai/grok-bot/approvals-security-and-privacy) である。knowhow の出典行は [`shopping.md`](../knowhow/shopping.md) である。引用は [parallel-fire-fleet](sand-workflow:parallel-fire-fleet)、[Cloud開発](sand-workflow:cloud)、tool-path-prefer、[poteto-mode](../guide/02-poteto-mode.md) である。

このページは WRAP だけである。条項の本体は fleet の既存スキル purchases、send-on-behalf、Auto-review である。条項はそこへ寄せる。このリポジトリに SKILL.md は置かない。Haggle の調達ボットは CreateAgent しない。新しい承認画面は置かない。第二のチェックリストは置かない。

## 対象

全ボットと CA である。spend / sign / send を握る席は、purchases、send-on-behalf、Auto-review の WRAP 先である。CA のテスト証拠は既存の `scripts/quiet-test.sh -- <cmd>` である。

## 範囲

### 対象にする

spend / sign / send の 3 動詞と、explicit go の形である。既存 3 スキルへ寄せる 1 条項である。

### 対象にしない

Haggle 調達ボットの CreateAgent。SNS の投稿規則は X運用の席規則のままである。プロダクトの実装。新しい承認 UI と HITL 画面。完了済み作業の巻き戻し。公式 approvals は提案中の操作を止めるだけである。

## SoT

条項の SoT は fleet の purchases、send-on-behalf、Auto-review である。公式境界は Approvals ドキュメントである。fleet の判断行は trend-log の 2026-09-07 行である。このページは 3 動詞と go の形を 1 表に並べるだけである。本体は vendor しない。

## anti-job

| 動詞 | 中身 | 既存 WRAP 先 |
|---|---|---|
| spend | 購入、課金、サブスク開始、送金、カード入力 | purchases |
| sign | 契約、規約同意、署名、権限付与 | purchases、Auto-review |
| send | 外部メール、Slack、DM、人の名での送信 | send-on-behalf |

3 動詞は都度の explicit go なしにしない。go が無いときは提案で止まる。提案は下書き、見積、比較表、draft である。止まった提案は人へ渡す。人が go を出すまで待つ。待っている間に別件を進めてよい。

## explicit go

| go である | go ではない |
|---|---|
| 人が、対象（宛先、金額、相手）を特定して、その 1 件に出した一言 | 席の説明文、routine の存在、LIVE、ADOPT |
| 同じ件、同じスレッドの go | 前回の go。別件の go。standing approval |
| `request_box_help` と公式 approvals の承認 | digest、proposal、draft PR が開いたこと |

go は 1 件 1 回である。金額、宛先、相手が変われば別件である。別件は新しい go である。

[ADR 0004](../decisions/0004-chat-secrets-webhook-astra-thrift.md) の 2 は同じ形である。webhook の Bot fixer は提案で止まる。auto-exec は REJECT のままである。解除は人間または PdM の explicit go のあとである。

## 却下

| 却下 | 理由 |
|---|---|
| Haggle 調達ボットの CreateAgent | 既存 3 スキルで足りる。CreateAgent は [`CBO`](../../bots/CBO.md) である |
| 第二の承認チェックリスト、承認 UI | 公式 approvals と `request_box_help` がある |
| standing approval を go と読む | 都度が Haggle の条項である |
| 本物のカードへの直結 | [`shopping.md`](../knowhow/shopping.md) の運用ルールである |
| 3 動詞を席ごとに書き直す | 条項は 1 つである。席へ複製しない。台帳は [`bots/README.md`](../../bots/README.md) の LOCK 1 行で指す |

## Domain WRAP

LOCK は GitHub Actions に依存しない。ページと [`scripts/test_anti_job_lock.py`](../../scripts/test_anti_job_lock.py) が持つ。証拠は `scripts/quiet-test.sh -- python3 scripts/ci.py` である。Quiet is not skip。新しい harness は置かない。

## 関連

出荷単位は [`README.md`](./README.md) である。PR 本文は [`pr-body.md`](./pr-body.md) である。quiet-test は [`quiet-test.md`](./quiet-test.md) である。秘密と提案のみは [ADR 0004](../decisions/0004-chat-secrets-webhook-astra-thrift.md) である。食い違ったときは fleet の purchases、send-on-behalf、Auto-review が勝つ。
