# pr-body（HARD LOCK）

## Purpose

ふっくー HARD LOCK 2026-09-08 である。適用 issue は [issue 46](https://github.com/maplefukku/grok-bot-ops/issues/46) である。引用は PdM JOB、GB、tool-path-prefer である。

## 対象

全リポジトリのすべての PR description である。書くのは impl CA と 開発 bots である。任意ではない。

## 範囲

### 対象にする

4 つの MUST H2 と CA brief と WRAP である。

### 対象にしない

product feature PR、CreateAgent、第 4 の契約 SoT、dual gate は対象外である。show-me の再実装は対象外である。invent harness は FAIL である。`run-pr-body.sh` も第二のテンプレ本体も置かない。

## SoT

このファイルが SoT である。WRAP only である。box の `/workspace/fleet-scripts/pr-show-me-template.md` を WRAP する。humanlayer の @dexhorthy /show-me を WRAP する。本体は [show-me SKILL.md](https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md) である。

OSS調査。show-me は pseudocode、call tree、file tree、Mermaid、diff を選ぶ。[describe_pr](https://github.com/humanlayer/humanlayer/blob/main/.claude/commands/describe_pr.md) はリポの既存テンプレを読む。新しい本文ハーネスは書かない。box テンプレはこの VM に無い。4 つの H2 は LOCK の文字であり、invent ではない。

`/show-me-your-work` は pstack の TSV 判断ログである。PR-body HARD LOCK ではない。TSV を 4 つの H2 の代わりに置かない。

## HARD LOCK

MUST H2 は次の 4 行である。全リポジトリのすべての PR description に置く。任意ではない。

```text
## Readable change (show-me)
## Pseudocode
## Mermaid
## TDD / BDD evidence
```

Opening a PR の Why、Scope、Tradeoffs、Blast Radius、Verification は 4 つの H2 の下に置く。4 つの H2 の代わりにはしない。

Readable change は humanlayer /show-me の diff、木、型である。長文で差分を語らない。
Pseudocode は変更後の手続きである。
Mermaid は流れまたは境界である。
TDD / BDD evidence は落ちたテストと通ったテストである。`quiet-test.sh -- <cmd>` を通す。

Beauty は show-me の visuals である。散文の壁は置かない。TDD と BDD の証拠は毎 PR で必須である。

merge-ok の行は 4 のままである。PR-body を 5 行目にしない。

## スキル

| スキル | すること |
|---|---|
| [job-brief](sand-workflow:job-brief) | SoT を brief へ書く |
| [Cloud開発](sand-workflow:cloud) | 4 つの H2 を PR 本文へ書く |
| [開発からPRグリーン](sand-workflow:pr-2) | 4 つの H2 を PR 本文へ書く |
| [PR確認](sand-workflow:pr) | merge-ok だけを観測する |

job-brief と cloud と pr の WRAP である。dual gate は置かない。

## CA brief

[job-brief](sand-workflow:job-brief)、[Cloud開発](sand-workflow:cloud)、[開発からPRグリーン](sand-workflow:pr-2) が CA prompt へ置く文は次である。

```text
PR 本文の正本は docs/process/pr-body.md である。全リポジトリのすべての PR description に次の 4 つの H2 を置く。任意ではない。

## Readable change (show-me)
## Pseudocode
## Mermaid
## TDD / BDD evidence

Readable change は humanlayer /show-me である。/show-me-your-work の TSV ではない。
Tests: quiet-test.sh -- <cmd>
```

## テスト

検査は `quiet-test.sh -- <cmd>` を通す。Quiet is not skip。TDD と BDD は [`scripts/test_pr_body_lock.py`](../../scripts/test_pr_body_lock.py) である。
