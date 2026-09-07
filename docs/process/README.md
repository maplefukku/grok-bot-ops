# 出荷単位（domain-unit）

A から D の手順の正本はこのファイルである。採択の理由は [0003. ドメイン単位で出荷量を管理する](../decisions/0003-domain-unit-throughput.md) にある。

## 呼び手

| 呼び手 | いつ | 見る節 |
|---|---|---|
| PdM | 平日 09:00 の leftover と merge sweep | 出荷単位、merge-ok、D. 平日 JST |
| Closer（今は `開発<product>` の CA） | bot スレッドが立ったとき | A. スレッドの分類 |
| Planner | unit の spec を書くとき | B. lane と契約 |
| impl CA | lane を 1 本受けたとき | B. lane と契約、quiet-test |
| PR確認 | merge sweep | merge-ok |
| 編成評価 | 席の提案を出す前 | C. 席 |

## 出荷単位

サイズ規則は [PdM HARD CORRECT](https://github.com/maplefukku/grok-bot-ops/issues/16#issuecomment-5543589865) である。[LOCK-READY](https://github.com/maplefukku/grok-bot-ops/issues/16#issuecomment-5543582190) の tiny-slice は使わない。境界と Done の品質は LOCK-READY のままである。

- 出荷単位はユーザーに見える機能 1 個、または bounded domain 1 個である。
- 1 unit は main への 1 merge である。unit PR は 1 本である。中央 CI は 1 回払う。
- 単位の内側では N CA を disjoint glob で並列にする。成果は同じ unit PR に畳む。
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

## A. スレッドの分類

| class | 信号 |
|---|---|
| MUST | failing test、contract break、security |
| NIT | style、extra docs、rename |
| DUP | 先行スレッドと同テーマ |

MUST は fix または WONTFIX（理由とテスト証拠）である。どちらも resolve する。

NIT の返信は最大 1 回である。2 回目で同テーマかつ新しい failing check が無いときは返信しない。resolve する。PR に label `adv-thrash` を付ける。新しい failing check がある指摘は MUST である。

同テーマは同じファイル範囲、同じ指摘種別、新しい failing check 無しである。bot が違っても同テーマである。

DUP は先行スレッドへ畳む。

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

PdM は CoS のままである。クローンしない。席の定義は [`PdM`](../../bots/PdM.md) である。

ADV closer と lane scheduler は提案である。product CoS は既定 NO である。ゲートと「CreateAgent しない」は [ADR 0003](../decisions/0003-domain-unit-throughput.md) を見よ。CreateAgent は [`CBO`](../../bots/CBO.md) である。

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

CA は MUST で WRAP を通す。CI の quiet stdout は任意。fail-cap B の `QUIET_FAIL_LINES` 既定 500 は [`quiet-test.md`](./quiet-test.md)（[#45](https://github.com/maplefukku/grok-bot-ops/issues/45)）である。この WRAP は既定を持たない。親 LOCK は [#42](https://github.com/maplefukku/grok-bot-ops/issues/42) である。Cloud スキルと tool-path-prefer が入口である。

## Dependabot と GitHub セキュリティ WRAP

このリポジトリの依存更新と静的セキュリティは、GitHub 公式スキーマと sibling キーの薄い WRAP である。新しい scanner、Renovate、Merge Queue、`merge_group` は置かない。

- Dependabot version 2 は [Dependabot options](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference) に従い、`github-actions` だけを weekly に見る。`groups` で Action 更新を 1 PR に畳む。sibling の gakuse-ai `.github/dependabot.yml` と同じ official キーは weekly、`open-pull-requests-limit`、labels、commit-message prefix、groups である。ファイル本体はこのトークンから private で 404 だった。`reviewers` は公式が closing down と書いてあるので置かない。レビューは [CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) の `@maplefukku` である。
- CodeQL は [starter-workflows の `codeql.yml`](https://github.com/actions/starter-workflows/blob/main/code-scanning/codeql.yml) である。言語は javascript-typescript、`build-mode: none` である。
- Scorecard は report-only である。出典は [ossf/scorecard-action](https://github.com/ossf/scorecard-action) と [ossf/scorecard の workflow 例](https://github.com/ossf/scorecard/blob/main/.github/workflows/scorecard-analysis.yml) である。
- Secret Protection と Push Protection は GitHub Settings の Advanced Security である。人が [Secret Scanning を有効にする](https://docs.github.com/en/code-security/how-tos/secure-your-secrets/detect-secret-leaks/enable-secret-scanning) と [Push Protection を有効にする](https://docs.github.com/en/code-security/how-tos/secure-your-secrets/prevent-future-leaks/enable-push-protection) を入れる。repo ファイルでは有効にならない。
- [`secret_scanning.yml`](https://docs.github.com/en/code-security/how-tos/secure-your-secrets/customize-leak-detection/exclude-folders-and-files) は `paths-ignore` の除外専用である。除外する path が無いので、このファイルは置かない。
- main の保護は ZuruNote gold [`main-pr-only` id=18800881](https://github.com/maplefukku/ZuruNote/rules/18800881) の薄い WRAP である。形は [Rulesets REST](https://docs.github.com/en/rest/repos/rules#create-a-repository-ruleset) の `deletion` / `non_fast_forward` / `pull_request`（`required_review_thread_resolution=true`、approvals=0）/ `required_status_checks` である。チェック名は gbo 実測の CI `check` と `Cursor Approval Agent: Pull Request Router and Approver` だけである。ZN 専用の TypeScript / Coverage / Drizzle はコピーしない。payload は [`scripts/main-pr-only-ruleset.json`](../../scripts/main-pr-only-ruleset.json)、適用は [`scripts/apply-main-pr-only-ruleset.sh`](../../scripts/apply-main-pr-only-ruleset.sh) である。この CA トークンの POST は 403 だった。人が admin で script を回す。設定画面は [Rulesets](https://github.com/maplefukku/grok-bot-ops/settings/rules) である。
- Dependabot auto-merge は公式の [`dependabot/fetch-metadata` + `gh pr merge --auto`](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/automate-dependabot-with-actions) である。delete-branch は公式の [`delete_branch_on_merge`](https://docs.github.com/en/rest/repos/repos#update-a-repository) である。

## 関連

手順の理由は [0003. ドメイン単位で出荷量を管理する](../decisions/0003-domain-unit-throughput.md) である。席の台帳は [`bots/README.md`](../../bots/README.md) である。書き込み箱は [`AGENTS.md`](../../AGENTS.md) である。日付付きの観察は [`fleet.md`](../knowhow/fleet.md) である。fleet.md は正本ではない。食い違ったときはこのファイルが勝つ。

fail-cap B の LOCK は [`quiet-test.md`](./quiet-test.md) にあり、box の `/workspace/fleet-scripts/quiet-test.sh` が SoT である。
