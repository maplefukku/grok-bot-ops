# PR-body（Flag Y）

## Purpose

ふっくー HARD LOCK 2026-09-08 である。適用 issue は [#46](https://github.com/maplefukku/grok-bot-ops/issues/46) である。引用は [job-brief](sand-workflow:job-brief)、[Cloud開発](sand-workflow:cloud)、[PR確認](sand-workflow:pr)、[開発からPRグリーン](sand-workflow:pr-2)、[parallel-fire-fleet](sand-workflow:parallel-fire-fleet)、tool-path-prefer、GB である。

全リポジトリの PR 本文は、下の 4 見出しを文字どおり MUST で持つ。任意ではない。欠けたら Flag Y は出さない。merge しない。Quiet is not skip。

## 対象

impl CA、job-brief、cloud、pr、PR確認、PdM である。

## 範囲

### 対象にする

PR 本文の 4 見出し、Flag Y、CA / job-brief に貼る文、quiet-test でのテスト証拠である。

### 対象にしない

[humanlayer /show-me](https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md) 本体の実装は対象外である。pstack `/show-me-your-work` の TSV は対象外である。製品機能 PR は対象外である。CreateAgent は対象外である。[#45](https://github.com/maplefukku/grok-bot-ops/issues/45) の fail-cap B は対象外である。Coverage の数字は pending である。数字は invent しない。

## SoT

recipe SoT は box `/workspace/fleet-scripts/pr-show-me-template.md` である。このページはそれを WRAP する。第二のチェックリストは置かない。

readable change の作り方は [humanlayer /show-me](https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md)（@dexhorthy）である。pstack `/show-me-your-work` の TSV ではない。

テスト証拠は `/workspace/fleet-scripts/quiet-test.sh -- <cmd>` である。このリポジトリの WRAP は [`scripts/quiet-test.sh`](../../scripts/quiet-test.sh) である。quiet-test 節は [`README.md`](./README.md) である。

## Flag Y

Flag Y は squash の前の Flag である。人または CoS が付ける。merge-ok の 4 行のあとに見る。4 見出しが 1 つでも欠けたら Flag Y は出さない。merge しない。

| 事実 | 値 |
|---|---|
| recipe SoT | `/workspace/fleet-scripts/pr-show-me-template.md` |
| OSS | [humanlayer /show-me](https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md) |
| ではない | pstack `/show-me-your-work` TSV |
| 必須見出し | 下の 4 行を文字どおり H2 にする |
| 欠けたとき | no Flag Y。no merge |
| テスト証拠 | `/workspace/fleet-scripts/quiet-test.sh -- <cmd>` |
| quiet と skip | Quiet is not skip |
| Beauty | Beauty と TDD と BDD と tests は同じ PR である |
| Coverage | pending。% は invent しない |
| WRAP | [job-brief](sand-workflow:job-brief) / [Cloud開発](sand-workflow:cloud) / [PR確認](sand-workflow:pr) / [開発からPRグリーン](sand-workflow:pr-2) は同じ SoT を指す。見出し表はここだけ |

## 必須見出し

PR 本文に次の 4 見出しを文字どおり置く。文言を変えない。

```text
## Readable change (show-me)
## Pseudocode
## Mermaid
## TDD / BDD evidence
```

## CA と job-brief に貼る文

[job-brief](sand-workflow:job-brief) と [Cloud開発](sand-workflow:cloud) は、CA に次を貼る。見出し表は増やさない。

```text
PR description MUST use these exact H2 headers (Flag Y gate).
SoT: /workspace/fleet-scripts/pr-show-me-template.md
OSS: https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md
NOT pstack /show-me-your-work TSV.
Tests: /workspace/fleet-scripts/quiet-test.sh -- <cmd>
Repo WRAP: scripts/quiet-test.sh -- <cmd>
Quiet is not skip.
Beauty + TDD + BDD + tests same PR. Coverage % pending. Do not invent a coverage number.
Missing any header → no Flag Y / no merge.

## Readable change (show-me)
## Pseudocode
## Mermaid
## TDD / BDD evidence
```
