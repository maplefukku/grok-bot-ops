# security-audit-wrap（初回 push 前）

## Purpose

Fleet WRAP [security-audit-wrap](sand-workflow:security-audit-wrap) の手順正本である。upstream OSS は [Cloudflare security-audit-skill](https://github.com/cloudflare/security-audit-skill) のみである。引用は [Cloud開発](sand-workflow:cloud)、[job-brief](sand-workflow:job-brief)、[開発からPRグリーン](sand-workflow:pr-2)、tool-path-prefer、[parallel-fire-fleet](sand-workflow:parallel-fire-fleet) である。

このページは WRAP だけである。監査本体・ATTACK-CLASSES・validator スクリプトは upstream と Fleet スキルが持つ。grok-bot-ops へ skill tree を vendor しない。scanner を invent しない。第二の監査 harness は置かない。CreateAgent NONE。

[`AGENTS.md`](../../AGENTS.md) はこのファイルへのポインタのみである。手順の詳細を AGENTS に複製しない。

## 対象

**プロダクトリポジトリ**で lane を受けた impl CA である。初回 `git push` の前に必ず通す。司令室（grok-bot-ops）で product コードを書く CA は対象外である（そもそも product コードはここに置かない）。

[job-brief](sand-workflow:job-brief) が brief を書くとき、done-when に初回 push 前ゲートとして本ページを **MUST** で含める。[Cloud開発](sand-workflow:cloud) と [pr-2](sand-workflow:pr-2) の CA 手順と矛盾させない。

## upstream（OSS）

| 項目 | 値 |
|---|---|
| URL | https://github.com/cloudflare/security-audit-skill |
| ライセンス | MIT |
| できること | 多段 subagent による structured security audit（recon → hunt → validate → report） |
| 不足 | Fleet の初回 push ゲート・job-brief 連携は本 WRAP が持つ |
| clone / vendor | grok-bot-ops へしない。プロダクト CA は subagent 経由で upstream を参照する |

プロダクト側で Skills CLI が必要なときだけ、**そのプロダクトリポのルート**で upstream を登録する:

```bash
npx skills add https://github.com/cloudflare/security-audit-skill --skill security-audit
```

Skills CLI の project scope は当該リポの `.agents/skills/` 等へ書く。grok-bot-ops のルートでこのコマンドを実行しない。司令室へ skill 本体を commit しない。

## 手順（初回 push 前 MUST）

1. **親 impl CA** は監査本体を自分で最後まで走らせない。subagent に委譲する（[security-audit-wrap](sand-workflow:security-audit-wrap) + upstream）。
2. subagent は対象を **プロダクトリポ** とし、変更 diff / trust boundary に沿って upstream の workflow を起動する。成果物の置き場は upstream [SKILL.md — Output directory](https://github.com/cloudflare/security-audit-skill/blob/main/skills/security-audit/SKILL.md) のみである。既定は target 外 `~/security-audit-skill/<repo-name>/run-<N>`。target 内は利用者が明示し、**親**が VCS がその directory 全体を ignore することを確認したときだけ。それ以外は外の path を要求して止まる。brief が path を書くときも ignore 確認は MUST。
3. **初回 push しない**条件は upstream 終端と同型である。(a) Phase 6 成果物が揃い `validate-findings.cjs` と `validate-coverage-ledger.cjs` が exit 0、かつ `run_status` が `incomplete` でない。(b) `run_status: "incomplete"` と理由を残すときは push しない。(a) のとき brief が書いた severity 閾値を超える `confirmed` が 0 件（brief 無指定なら `confirmed` 0）。`needs_validation` だけでは (a) とみなさない。判断は `/show-me-your-work` に残す。
4. grok-bot-ops への PR では本手順を実行しない（docs-only 変更は subagent によるメタレビューで足りる）。

Quiet is not skip。テスト証拠は [Cloud開発](sand-workflow:cloud) と [pr-2](sand-workflow:pr-2) の quiet-test 規約に従う（プロダクトリポの process / 薄い WRAP。司令室の `scripts/quiet-test.sh` を字面どおり打たない）。SoT の読み方は [`quiet-test.md`](./quiet-test.md) である。

## 禁止

| 禁止 | 破る規則 |
|---|---|
| grok-bot-ops ルートで `npx skills add` して skill tree を commit | 司令室へ本体をコピーしない |
| ATTACK-CLASSES / SKILL.md ツリーを grok-bot-ops `skills/` へ複製 | eval ゲート外の vendor |
| 親 CA が監査フェーズを代走 | subagent 必須 |
| 自前 scanner・第二監査スキル | invent=N |

HOLD merge=PM。Flag Y は [pr-body.md](./pr-body.md) の述語のみ。Flag≠Bugbot。
