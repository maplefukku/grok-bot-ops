# 出荷単位（domain-unit）

A から D の手順の正本はこのファイルである。採択の理由は [0003. ドメイン単位で出荷量を管理する](../decisions/0003-domain-unit-throughput.md) にある。

## 呼び手

| 呼び手 | いつ | 見る節 |
|---|---|---|
| PdM | 平日 09:00 の leftover と merge sweep。Flag Y | 出荷単位、merge-ok、PR-body、CI 梯子、D. 平日 JST |
| Closer（今は `開発<product>` の CA） | bot スレッドが立ったとき | A. スレッドの分類 |
| Planner | unit の spec を書くとき | B. lane と契約 |
| job-brief | CA brief を書くとき | PR-body、CI 梯子 |
| 開発リーダー | ROUTE+FIRE のとき | CI 梯子、出荷単位 |
| impl CA | lane を 1 本受けたとき。PR を書くとき | B. lane と契約、quiet-test、PR-body、CI 梯子 |
| 全ボットと CA | spend / sign / send に触れる前 | anti-job |
| PR確認 | merge sweep | merge-ok、PR-body、CI 梯子 |
| 人 | Dependabot が PR を開いたあと。Flag の前 | PR-body Dependabot stamp |
| 編成評価 | 席の提案を出す前 | C. 席、[shared-computer](./shared-computer.md) |
| CBO | CreateAgent と席設計のとき | C. 席、[shared-computer](./shared-computer.md)、Marketplace survey |
| 開発リーダー、PdM、impl CA | overnight の /goal を切るとき。一晩の brief を受けるとき | overnight /goal |

## 出荷単位

サイズ規則は [PdM HARD CORRECT](https://github.com/maplefukku/grok-bot-ops/issues/16#issuecomment-5543589865) である。[LOCK-READY](https://github.com/maplefukku/grok-bot-ops/issues/16#issuecomment-5543582190) の tiny-slice は使わない。境界と Done の品質は LOCK-READY のままである。

- 出荷単位はユーザーに見える機能 1 個、または bounded domain 1 個である。
- 1 unit は main への 1 merge である。unit PR は 1 本である。中央 CI は 1 回払う。
- 単位の内側では N CA を disjoint glob で並列にする。成果は同じ unit PR に畳む。内側の並列は local worktree である。
- 製品横断（ZuruNote、sauna-master、gakuse-ai）は独立した unit を並列にする。
- docs、contract、impl という工程だけを理由に PR を割らない。
- 指標は units merged / day である。PR 断片数でも bot 数でもない。日次の repo WRAP は [`scripts/merge-velocity-day.sh`](../../scripts/merge-velocity-day.sh) である。数え本体は box `/workspace/fleet-scripts/merge-count-jst.sh` である。

## merge-ok

4 行が全部 true のときだけ merge-ok である。

| 行 | true の条件 | 観測 |
|---|---|---|
| required CI | green | PR確認 |
| Cursor bots | done。skip と dismiss は done ではない | PR確認 |
| MUST threads | 未 resolve が 0 | Closer |
| NIT threads | 各スレッド返信 ≤ 1 かつ resolved | Closer |

ボットは merge しない。人だけが merge する。事実の観測は [`PR確認`](../../bots/PR確認.md) である。日付付きの観察は [`fleet.md`](../knowhow/fleet.md) である。fleet.md は正本ではない。

Flag Y は [`pr-body.md`](./pr-body.md) である。PR 本文の 4 見出しが欠けたら Flag しない。merge しない。Dependabot も同じである。Soft-OK はしない。stamp は [`pr-body.md`](./pr-body.md) の Dependabot stamp である。

required CI の green は same-BC を畳んだ FULL tip である。LIGHT-WT の green は merge-ok ではない。Flag と E2E は FULL tip だけである。梯子の正本は [`ci-ladder.md`](./ci-ladder.md) である。

## 禁止

| 禁止 | 破る規則 |
|---|---|
| feature を docs、contract、impl の PR に割る | 1 unit は 1 merge である。中央 CI を工程の数だけ払う |
| 同じ CI gate を待つ stacked PR | unit は 1 PR である。lane は同じ PR に land する |
| 同じファイルに 2 本の PR | lane の glob は disjoint である。同じファイルの writer は assembler 1 体である |
| プロダクトコードへの merge-train | 衝突は loser が rebase する |
| 第 4 の契約 SoT | 契約 SoT は ARCH issue 3 本だけである |
| 新しい impl ボット | impl の席を増やさない |
| PdM のクローン | PdM は CoS のままである |
| Soft-OK（4 見出し欠けのまま Flag） | Flag Y は 4 見出し MUST。Dependabot は stamp してから Flag する |

## A. スレッドの分類

| class | 信号 |
|---|---|
| MUST | failing test、contract break、security |
| NIT | style、extra docs、rename |
| DUP | 先行スレッドと同テーマ |

MUST は fix または WONTFIX（理由とテスト証拠）である。どちらも resolve する。

NIT の返信は最大 1 回である。2 回目で同テーマかつ新しい failing check が無いときは返信しない。resolve する。PR に label `adv-thrash` を付ける。新しい failing check がある指摘は MUST である。

Closer が返信済み（answered）のスレッドに bot が再度書いたときは返信しない。Dup として resolve する。ping-pong しない。

reopen 後で新しい failing check が無いときは返信しない。Thrash として resolve する。PR に label `adv-thrash` を付ける。返信数は増えない。

reopen 後で新しい failing check がある指摘は MUST である。MUST は再返信して終端する。

同テーマは同じファイル範囲、同じ指摘種別、新しい failing check 無しである。bot が違っても同テーマである。

DUP は先行スレッドへ畳む。

人が HOLD したスレッドは Closer が触らない。返信も resolve もしない。

Closer の終端は resolve である。verdict 待ちの Owed と HOLD は終端ではない。merge-ok の MUST threads 行と NIT threads 行は Closer が観測する。Flag Y は PdM である。Closer は Flag しない。

Closer は Resolve を所有する。Closer は実装を増やさない。MUST の fix を超えるコードは [`開発リーダー`](../../bots/開発リーダー.md) へ戻す。今の Closer は `開発<product>` の CA である。提案席 ADV closer は [ADR 0003](../decisions/0003-domain-unit-throughput.md) である。

NIT 1 回目の返信型は次の 1 行である。

```text
NIT <直す|直さない>。<理由 1 文>。<commit または参照 URL>。resolve。
```

## B. lane と契約

契約 SoT は次の 3 行だけである。4 行目は置かない。packing のコメントは [PdM HARD CORRECT](https://github.com/maplefukku/grok-bot-ops/issues/16#issuecomment-5543589865) である。

| product | contract SoT | 出典 |
|---|---|---|
| gakuse-ai | `packages/contract` | [gakuse-ai#2063](https://github.com/maplefukku/gakuse-ai/issues/2063) |
| sauna-master | `contract/openapi.yaml` | [sauna-master#197](https://github.com/maplefukku/sauna-master/issues/197) |
| ZuruNote | `server/openapi` を拡張 | [ZuruNote#242](https://github.com/maplefukku/ZuruNote/issues/242) |

このリポジトリに契約本文を置かない。第 4 の SoT を作らない。

lane は disjoint glob である。同じファイルと SoT の writer は assembler 1 体である。contract lane が先に同じ unit PR に land する。そのあと impl lane が並列に走る。契約境界は単位の内側の並列に使う。PR を増やす理由には使わない。

glob-lock 表は導出する。同じ製品の open unit PR の lane 表を union したものである。偶数時の thrash kill が導出する。このリポジトリに live な lock ファイルを置かない。

衝突したとき、loser は rebase するか glob を切り直す。merge-train はしない。

Planner の spec は FILES/globs と forbidden siblings を書く。

## C. 席

PdM は CoS のままである。クローンしない。席の定義は [`PM`](../../bots/PdM.md) である。

ADV closer と lane scheduler は提案である。product CoS は既定 NO である。ゲートと「CreateAgent しない」は [ADR 0003](../decisions/0003-domain-unit-throughput.md) を見よ。CreateAgent は [`CBO`](../../bots/CBO.md) である。共有 1 マシンでは owner 席が 1 つ成果物を持ち、詰まったときだけ既存 specialist に渡す。チェックは [`shared-computer.md`](./shared-computer.md) である。新規席は作らない。CreateAgent 前の Marketplace survey は [`marketplace-precheck.md`](./marketplace-precheck.md) である。

[`監視`](../../bots/監視.md)、[`開発リーダー`](../../bots/開発リーダー.md)、[`編成評価`](../../bots/編成評価.md) は維持する。新しい impl ボットは無い。

## D. 平日 JST

| JST | 曜日 | job | 出すもの | 今の席 | 提案席 |
|---|---|---|---|---|---|
| 09:00 | 平日 | morning stack | leftover graph。FIRE-ready と BLOCKED | PdM | 無し |
| 10、12、14、16、18 | 平日 | thrash kill | ADV NIT、duplicate CA、glob 衝突。PdM が Closer を火付けする | Closer と PdM | ADV closer と lane scheduler |
| 各偶数時の直後と 17:30 | 平日 | merge sweep | merge-ok の 4 行 | PR確認 → PdM | lane scheduler |
| 22:00-08:00 と土日 | | 静穏 | 無し | | incident または deploy deadline だけ例外 |

[`監視`](../../bots/監視.md) の sweep は平日 06-22 の 2 時間おきである。この時計は変えない。静穏のあいだ、監視は stall を PdM へ渡すだけである。FIRE と thrash kill と merge sweep は 09:00 まで待つ。incident または deploy deadline のときだけ動かす。

## quiet-test

Purpose pack. CA と bot のテストコマンドを fleet quiet-test に通す。本文は invent しない。Beauty は薄い exec である。TDD と BDD は [`scripts/test_quiet_test.py`](../../scripts/test_quiet_test.py) を同じ PR に置く。

新しいリポジトリの既定は次である。

```text
/workspace/fleet-scripts/quiet-test.sh -- <cmd>
```

このリポジトリの薄い WRAP は [`scripts/quiet-test.sh`](../../scripts/quiet-test.sh) である。box があるときだけそれを exec する。exit code はそのまま通す。

レーンの formatter を先に `<cmd>` へ入れる。vitest は `--silent=passed-only`、jest は `--silent`、xcbeautify、gotestsum。quiet は skip ではない。

CA は MUST で WRAP を通す。CI の quiet stdout は任意。fail-cap B の `QUIET_FAIL_LINES` 既定 500 は [`quiet-test.md`](./quiet-test.md)（[issue 45](https://github.com/maplefukku/grok-bot-ops/issues/45)、Domain WRAP は [issue 69](https://github.com/maplefukku/grok-bot-ops/issues/69)）である。SUCCESS line-budget の `QUIET_OK_LINES` 既定 10 は同じ [`quiet-test.md`](./quiet-test.md)（[issue 74](https://github.com/maplefukku/grok-bot-ops/issues/74)）である。この WRAP は既定を持たない。exit code の SUCCESS/FAIL contract は同じ [`quiet-test.md`](./quiet-test.md)（[issue 96](https://github.com/maplefukku/grok-bot-ops/issues/96)）である。exit-code contract は WRAP の exec そのものである。親 LOCK は [#42](https://github.com/maplefukku/grok-bot-ops/issues/42) である。Cloud スキルと tool-path-prefer が入口である。

FAIL verbose-tail の contract は同じ [`quiet-test.md`](./quiet-test.md)（[issue 93](https://github.com/maplefukku/grok-bot-ops/issues/93)）である。FAIL の chat は本体の tail 既定 500 行と full-log path である。この WRAP は tail を持たない。

## 関連

手順の理由は [0003. ドメイン単位で出荷量を管理する](../decisions/0003-domain-unit-throughput.md) である。席の台帳は [`bots/README.md`](../../bots/README.md) である。書き込み箱は [`AGENTS.md`](../../AGENTS.md) である。日付付きの観察は [`fleet.md`](../knowhow/fleet.md) である。fleet.md は正本ではない。食い違ったときはこのファイルが勝つ。

fail-cap B の LOCK は [`quiet-test.md`](./quiet-test.md) にあり、box の `/workspace/fleet-scripts/quiet-test.sh` が SoT である。Domain WRAP は [issue 69](https://github.com/maplefukku/grok-bot-ops/issues/69) である。SUCCESS line-budget の Domain WRAP は [issue 74](https://github.com/maplefukku/grok-bot-ops/issues/74) である。exit-code contract の Domain WRAP は [issue 96](https://github.com/maplefukku/grok-bot-ops/issues/96) である。LOCK は CI-independent である。HITL chrome は Soft-HOLD PARK のままである。

FAIL verbose-tail の Domain WRAP は [issue 93](https://github.com/maplefukku/grok-bot-ops/issues/93) である。FAIL は drip である。REJECT A のままである。

PR-body HARD LOCK は [`pr-body.md`](./pr-body.md) である。recipe SoT は box `/workspace/fleet-scripts/pr-show-me-template.md` である。Flag Y の 4 見出しはそこだけである。Dependabot の stamp は同じ [`pr-body.md`](./pr-body.md) である。WRAP は `gh api --method PATCH` である。Soft-OK はしない。

CI 梯子 LIGHT→FULL は [`ci-ladder.md`](./ci-ladder.md) である。SPEED NORM の太い lander は出荷単位である。

ADV closer reopen guard Domain WRAP は [issue 118](https://github.com/maplefukku/grok-bot-ops/issues/118) である。sibling は [issue 95](https://github.com/maplefukku/grok-bot-ops/issues/95) と [issue 73](https://github.com/maplefukku/grok-bot-ops/issues/73) である。引用は [parallel-fire-fleet](sand-workflow:parallel-fire-fleet)、[Cloud開発](sand-workflow:cloud)、[`quiet-test.md`](./quiet-test.md) である。

共有 1 マシンの owner 席 WRAP は [`shared-computer.md`](./shared-computer.md) である。CreateAgent と schedules-force-agency のチェックはそこだけである。新しい席は invent しない。

Marketplace survey（CreateAgent precheck）は [`marketplace-precheck.md`](./marketplace-precheck.md) である。export-bot-template は KEEP。並列 Marketplace は invent しない。CreateAgent 量産は NONE。

## anti-job

spend / sign / send は都度の explicit go なしにしない。条項の本体は fleet の purchases、send-on-behalf、Auto-review である。Domain WRAP は [`anti-job.md`](./anti-job.md)（[issue 90](https://github.com/maplefukku/grok-bot-ops/issues/90)）である。go の形と却下はそこだけである。Haggle 調達ボットは CreateAgent しない。

## overnight /goal

一晩の /goal brief の形は [`overnight-goal.md`](./overnight-goal.md) である。6 見出しは Goal、done-when、touch scope、diff cap、mid-run verify、verifier である。判定は [`scripts/overnight_goal.py`](../../scripts/overnight_goal.py) である。適用 issue は [issue 89](https://github.com/maplefukku/grok-bot-ops/issues/89) である。runner は既存の [overnight-goal-cleanup](sand-workflow:overnight-goal-cleanup) と [Cloud開発](sand-workflow:cloud) である。verifier 席は Soft-HOLD である。新しい harness は置かない。
