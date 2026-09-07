# PR-body（Flag Y）

## Purpose

ふっくー HARD LOCK 2026-09-08 である。適用 issue は [#46](https://github.com/maplefukku/grok-bot-ops/issues/46) である。引用は [job-brief](sand-workflow:job-brief)、[Cloud開発](sand-workflow:cloud)、[PR確認](sand-workflow:pr)、[parallel-fire-fleet](sand-workflow:parallel-fire-fleet)、tool-path-prefer、GB、OSS調査 である。

このページは WRAP だけである。recipe SoT は box `/workspace/fleet-scripts/pr-show-me-template.md` である。readable change の OSS は [humanlayer /show-me](https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md) である。第二のチェックリストは置かない。harness は invent しない。

## OSS調査

| 項目 | 値 |
|---|---|
| URL | https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md |
| ライセンス | MIT |
| 最終 push | 2026-08-13 |
| できること | 差分、pseudocode、call tree、Mermaid で変更を見せる |
| 不足 | PR 本文の必須見出しと Flag Y は持たない。見出し SoT は fleet テンプレである |
| clone | しない |

pstack `/show-me-your-work` の TSV ではない。

## Flag Y

全リポジトリの PR 本文は、fleet テンプレの 4 見出しを文字どおり MUST で持つ。欠けたら Flag Y は出さない。merge しない。Quiet is not skip。

[job-brief](sand-workflow:job-brief) と [Cloud開発](sand-workflow:cloud) と [PR確認](sand-workflow:pr) は、box `/workspace/fleet-scripts/pr-show-me-template.md` を指す。見出し表は invent しない。readable change は humanlayer /show-me で書く。

テスト証拠は既存の `/workspace/fleet-scripts/quiet-test.sh -- <cmd>` である。このリポジトリの WRAP は [`scripts/quiet-test.sh`](../../scripts/quiet-test.sh) である。新しい test harness は置かない。

Beauty と TDD と BDD と tests は同じ PR である。Coverage は pending である。% は invent しない。

## Readable change (show-me)

humanlayer /show-me の diff / tree を使う。

## Pseudocode

fleet テンプレの見出しである。本文の書き方は humanlayer /show-me の pseudocode 形である。

## Mermaid

fleet テンプレの見出しである。本文の書き方は humanlayer /show-me の Mermaid 形である。

## TDD / BDD evidence

テストがあるときだけ、既存の `quiet-test.sh -- <cmd>` を通す。quiet は skip ではない。新しい harness は FAIL である。
