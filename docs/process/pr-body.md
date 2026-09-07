# pr-body（HARD LOCK）

## Purpose

親 SoT は [issue 46](https://github.com/maplefukku/grok-bot-ops/issues/46) である。ふっくー HARD LOCK 2026-09-08 である。引用は [job-brief](sand-workflow:job-brief)、[Cloud開発](sand-workflow:cloud)、[PR確認](sand-workflow:pr)、[開発からPRグリーン](sand-workflow:pr-2)、[humanlayer show-me](https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md) である。

全リポジトリの PR 本文に、このページの 4 MUST 見出しをこの順で置く。任意ではない。

## 対象

PdM と 開発リーダーが [job-brief](sand-workflow:job-brief) で CA brief を書くとき。impl CA と 開発 bots が [Cloud開発](sand-workflow:cloud) と [開発からPRグリーン](sand-workflow:pr-2) で PR を書くとき。[PR確認](sand-workflow:pr) が本文の正本を尋ねるとき。

## 範囲

### 対象にする

PR 本文の 4 MUST 見出しと、CA brief の指し先である。

### 対象にしない

show-me 本体の実装は対象外である。プロダクト機能 PR の中身は対象外である。CreateAgent は対象外である。[quiet-test.md](./quiet-test.md) の fail-cap は対象外である。pstack の `/show-me-your-work` TSV は対象外である。merge-ok に 5 行目は足さない。

## SoT

見た目の正本は box の `/workspace/fleet-scripts/pr-show-me-template.md` である。読み方の正本は [humanlayer show-me](https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md) である。このページは WRAP である。テンプレ本文は vendor しない。第二のチェックリストは置かない。

`/show-me-your-work` は判断ログの TSV である。PR 本文の readable change ではない。混同しない。

テストコマンドは [`scripts/quiet-test.sh`](../../scripts/quiet-test.sh) を通す。`quiet-test.sh -- <cmd>` である。quiet は skip ではない。

## CA brief

[job-brief](sand-workflow:job-brief) と [Cloud開発](sand-workflow:cloud) が貼る文は次である。見出しの文言は変えない。

```text
PR body HARD LOCK. SoT: https://github.com/maplefukku/grok-bot-ops/blob/main/docs/process/pr-body.md
WRAP /workspace/fleet-scripts/pr-show-me-template.md
show-me: https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md
job-brief / sand-workflow:cloud / sand-workflow:pr / sand-workflow:pr-2 cite that SoT only.
Not pstack /show-me-your-work TSV.
Every PR body MUST include these headings in this order:
## Readable change (show-me)
## Pseudocode
## Mermaid
## TDD / BDD evidence
Tests: scripts/quiet-test.sh -- <cmd>
CreateAgent しない.
```

## Readable change (show-me)

humanlayer show-me の diff 形で、何が変わったかを見せる。ファイル木、呼び出し木、状態のどれか最短の 1 枚を置く。box テンプレがあるときはそれを WRAP する。

## Pseudocode

変更後の流れを `on(event)` 形で書く。実コードの貼り付けではない。

## Mermaid

制御またはデータの流れを 1 枚以上置く。装飾の図は置かない。

## TDD / BDD evidence

先に RED、あとで GREEN を書く。Given / When / Then か表で、回したコマンドと終了コードを残す。コマンドは `scripts/quiet-test.sh -- <cmd>` である。
