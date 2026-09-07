# pr-body（HARD LOCK）

## Purpose

このページは WRAP だけである。親は [issue 46](https://github.com/maplefukku/grok-bot-ops/issues/46) である。ふっくー HARD LOCK 2026-09-08 である。recipe SoT は box `/workspace/fleet-scripts/pr-show-me-template.md` である。readable change の OSS は [humanlayer show-me](https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md) である。第二のチェックリストは置かない。harness は invent しない。新しい harness は FAIL である。

## OSS調査

GitHub は box ブラウザである。clone しない。

| 項目 | 値 |
|---|---|
| URL | https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md |
| ライセンス | MIT |
| 最終 push | 2026-08-13 |
| できること | 差分、pseudocode、call tree、Mermaid で変更を見せる |
| 不足 | PR 本文の必須見出しは持たない。見出し SoT は fleet テンプレである |
| clone | しない |

`xingyaoww/show-me` は HTML explainer である。WRAP しない。`pr-show-me-template.md` は GitHub 検索 0 件である。box パスだけを指す。この VM に `/workspace/fleet-scripts/` は無い。本文は vendor しない。

pstack の `/show-me-your-work` TSV ではない。

引用は [job-brief](sand-workflow:job-brief)、[Cloud開発](sand-workflow:cloud)、[PR確認](sand-workflow:pr)、[開発からPRグリーン](sand-workflow:pr-2) である。見出し表は invent しない。4 見出しは fleet テンプレの文字である。

テスト証拠は既存の [`scripts/quiet-test.sh`](../../scripts/quiet-test.sh) である。`quiet-test.sh -- <cmd>` である。quiet は skip ではない。CreateAgent しない。merge-ok に 5 行目は足さない。

## Readable change (show-me)

fleet テンプレの見出しである。書き方は humanlayer show-me である。

## Pseudocode

fleet テンプレの見出しである。書き方は humanlayer show-me の pseudocode である。

## Mermaid

fleet テンプレの見出しである。書き方は humanlayer show-me の Mermaid である。

## TDD / BDD evidence

fleet テンプレの見出しである。証拠は既存の `quiet-test.sh -- <cmd>` である。新しい harness は FAIL である。
