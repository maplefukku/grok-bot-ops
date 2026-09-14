# PR-body（Flag Y）

## Purpose

ふっくー HARD LOCK 2026-09-08 である。適用 issue は [#46](https://github.com/maplefukku/grok-bot-ops/issues/46) と merge sweep の [#127](https://github.com/maplefukku/grok-bot-ops/issues/127) である。引用は [job-brief](sand-workflow:job-brief)、[Cloud開発](sand-workflow:cloud)、[PR確認](sand-workflow:pr)、[開発からPRグリーン](sand-workflow:pr-2)、[pr-status-dedupe-quiet](sand-workflow:pr-status-dedupe-quiet)、[conductor-keep-moving](sand-workflow:conductor-keep-moving)、[parallel-fire-fleet](sand-workflow:parallel-fire-fleet) Merge Gate、tool-path-prefer、GB、OSS調査 である。

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

[job-brief](sand-workflow:job-brief) と [Cloud開発](sand-workflow:cloud) と [PR確認](sand-workflow:pr) と [開発からPRグリーン](sand-workflow:pr-2) は、box `/workspace/fleet-scripts/pr-show-me-template.md` を指す。見出し表は invent しない。readable change は humanlayer /show-me で書く。

### PdM merge sweep（Flag Y ONLY）

PdM が merge sweep で Flag Y するときの条件 ONLY である。[#127](https://github.com/maplefukku/grok-bot-ops/issues/127) の WRAP である。第二の Flag 定義、harness、scanner、hourly cron は invent しない。Bugbot の green は Flag ではない（Flag≠Bugbot）。

| 条件 | true の意味 | 観測 |
|---|---|---|
| behind0 | PR head が base tip-sot に behind 0 | [pr-2](sand-workflow:pr-2) / [pr-status-dedupe-quiet](sand-workflow:pr-status-dedupe-quiet) LIVE |
| thr0 | `reviewThreads` を paginate し、unresolved かつ outdated でないスレッドが 0 | [pr](sand-workflow:pr) / [pr-status-dedupe-quiet](sand-workflow:pr-status-dedupe-quiet) LIVE |
| FULL CLEAN | required CI green が same-BC を畳んだ FULL tip | [PR確認](sand-workflow:pr)、[`ci-ladder.md`](./ci-ladder.md) |
| APPROVED | GitHub PR review APPROVED | [pr-2](sand-workflow:pr-2) |
| ADV SUCCESS | ADV が SUCCESS。skip / dismiss は SUCCESS ではない | [parallel-fire-fleet](sand-workflow:parallel-fire-fleet) Merge Gate、[`fleet.md`](../knowhow/fleet.md) ADOPT D |

4 見出し MUST が先である。上表が全部 true のときだけ PdM が Flag Y する。HOLD merge=PM である。ボットは merge しない。Soft Flag invent しない。

impl CA が credits EXHAUST のときは、Closer の thr-close を Mini WRAP で続ける（tool-path-prefer）。on-demand impl CA は REJECT である。[conductor-keep-moving](sand-workflow:conductor-keep-moving) は same-sweep で ACK-then-stop しない。

テスト証拠は既存の `/workspace/fleet-scripts/quiet-test.sh -- <cmd>` である。このリポジトリの WRAP は [`scripts/quiet-test.sh`](../../scripts/quiet-test.sh) である。新しい test harness は置かない。

Beauty と TDD と BDD と tests は同じ PR である。Coverage は pending である。% は invent しない。

### Dependabot stamp

Dependabot の初期本文は fleet テンプレの 4 見出しを持たない。欠けたまま Flag Y は出さない。Soft-OK は 4 見出し欠けのまま Flag することである。Soft-OK はしない。merge しない。Dependabot が本文を書き直したら 4 見出しを再確認する。欠けたら再 stamp する。

stamp は GitHub の [Update a pull request](https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#update-a-pull-request) である。`PATCH /repos/{owner}/{repo}/pulls/{pull_number}` の `body` である。このリポジトリの WRAP は `gh api --method PATCH` である。新しい stamp スクリプトは置かない。見出しは invent しない。recipe SoT は box `/workspace/fleet-scripts/pr-show-me-template.md` である。

```text
gh api --method PATCH repos/{owner}/{repo}/pulls/{pull_number} -F body=@-
```

gh が埋めるのは `{owner}` と `{repo}` だけである。`{pull_number}` は置き換える。`body` はテンプレの 4 見出しを文字どおり持つ。readable change は humanlayer /show-me である。pstack `/show-me-your-work` の TSV ではない。観測の stamp は Dependabot の初期本文を残さない。PATCH の `body` が本文になる。

観測は 2026-09-07 の [#54](https://github.com/maplefukku/grok-bot-ops/pull/54) [#55](https://github.com/maplefukku/grok-bot-ops/pull/55) [#56](https://github.com/maplefukku/grok-bot-ops/pull/56) [#57](https://github.com/maplefukku/grok-bot-ops/pull/57) である。editor は maplefukku である。stamp するのは人である。Flag Y の呼び手は PdM である。新しい席は置かない。#54 の `lastEditedAt` は 2026-09-07T17:11:37Z である。#55 は 17:11:52Z、#56 は 17:11:54Z、#57 は 17:11:55Z である。PdM Flag Y `CI CLEAN + 4-pack stamped` は #54 の review である。クライアントは GitHub に残らない。WRAP は `gh api --method PATCH` である。この JOB はこの WRAP を実行していない。

## Readable change (show-me)

humanlayer /show-me の diff / tree を使う。

## Pseudocode

fleet テンプレの見出しである。本文の書き方は humanlayer /show-me の pseudocode 形である。

## Mermaid

fleet テンプレの見出しである。本文の書き方は humanlayer /show-me の Mermaid 形である。

## TDD / BDD evidence

テストがあるときだけ、既存の `quiet-test.sh -- <cmd>` を通す。quiet は skip ではない。新しい harness は FAIL である。
