# ADV disposition（採らなかった ADV の記憶 WRAP）

## Purpose

[issue 140](https://github.com/maplefukku/grok-bot-ops/issues/140) の WRAP である。bounded context 名は adv-disposition である。証拠は [sauna-master#297](https://github.com/maplefukku/sauna-master/pull/297) の mill である。ADV が plant を作り、FIX が land し、次の run が同ドメインの cousin を新しい MUST で出す。終端の形（WONTFIX / OOS）はすでにある。欠けているのは durable key、write-path の持ち主、次の ADV 投稿前の read-path である。

このページは WRAP だけである。スレッドの分類は [`README.md`](./README.md) の A 節と [`scripts/adv_closer.py`](../../scripts/adv_closer.py)（[issue 118](https://github.com/maplefukku/grok-bot-ops/issues/118) reopen guard）である。本 issue は cross-PR の sibling であり、第二の Closer ではない。記憶の器は既存の intent_atom（[ADR 0001](../decisions/0001-intent-memory-postgres-pgvector.md)）である。dedup の形は [ADR 0002](../decisions/0002-trend-adopt-loop.md) の先勝ちだけを借りる。Gaze の plant は [`trend-log.md`](../decisions/trend-log.md) に書かない。引用は [pr-2](sand-workflow:pr-2)、[Cloud開発](sand-workflow:cloud)、[finding-to-spec](sand-workflow:finding-to-spec)、[`fleet.md`](../knowhow/fleet.md) ADOPT B / ADOPT D である。

新しい disposition DB、OOS registry、新しいスキル、第二の Flag 定義は置かない。CreateAgent NONE。HOLD merge=PM。

## HITL LOCK（t13247u）

adversarial review は auto-intake ではない。終端は 3 つだけである。

| 指摘 | 終端 |
|---|---|
| IN scope | fix して resolve |
| OOS かつ有用 | finding-to-spec の follow-up issue を FILE する。この PR では直さない。resolve |
| NOT warranted | 理由を 1 文書いて decline し、resolve |

OOS の終端は boundary issue の FILE と resolve である。スレッドで直さない。

## durable key

| 単位 | 鍵 |
|---|---|
| claim | canonical thread URL（`https://github.com/<owner>/<repo>/pull/<n>#discussion_r<id>`）の first-wins と theme 行（path/glob × kind × 1 行 claim）。`/files#r<id>` 形は同じ鍵に正規化する |
| domain | finding-to-spec の OOS boundary issue 1 本（label `adv-followup`）。cousin の family を持つ |

leftover の prev-fps を finding ID にしない。kind は [`adv_closer.py`](../../scripts/adv_closer.py) の `Kind` である。

## write-path

Closer が thread の終端と OOS issue の FILE を持つ。intent_atom の行は Closer が draft し、人（`pdm` または `user`）が承認する。ADV は disposition を書かない。

写像は [`scripts/intent_memory/disposition.py`](../../scripts/intent_memory/disposition.py) の dry-run である。形は [`trend_log.py`](../../scripts/intent_memory/trend_log.py) と同じである。draft は `kind=decision`、`source=bot`、`actor=bot:Closer` である。`append` は IngestOff で落ちる。人が承認するときは `source=human` と `pdm` / `user` で書き直す。Write ACL は変えない。

tags は 3 つだけである。`adv`、`disposition:reject|oos|invalid`、`product:<repo>` である。`product` は thread URL の repo から取る。schema、ACL、pairing は変えない。

| disposition | 意味 | ref |
|---|---|---|
| `reject` | WONTFIX。理由とテスト証拠 | 証拠の URL |
| `oos` | OOS かつ有用 | boundary issue の URL（必須） |
| `invalid` | NOT warranted | 理由の参照 URL |

## read-path（2 つの gate）

| gate | いつ | 読むもの | 規則 |
|---|---|---|---|
| upstream | 次の ADV 投稿の前 | resolved の WONTFIX / OOS、`adv-followup` issue、disposition 行 | 境界の内側で新しい failing check が無い claim は投稿しない |
| downstream | Closer の返信の前 | 既存の Dup / Thrash（[`README.md`](./README.md) A 節） | 変えない |

新しい failing check は無条件に MUST である。どちらの gate も落とさない。

upstream gate の文言は pr-2 と ADV fire workflow の box にある。このリポジトリでは box を編集しない。1 行の amend draft は PR 本文に置き、owner が貼る。

## disposition ≠ ADV SUCCESS

disposition を保存しても ADV SUCCESS ではない。[`pr-body.md`](./pr-body.md) の Flag Y、merge-ok 4 行、ADV SUCCESS（skip / dismiss は SUCCESS ではない）は変わらない。

## 最初の slice（leftover / GFM GazeSweep）

fixture の seed は [`fixtures.json`](../../scripts/intent_memory/fixtures.json) の `adv` 行である。WONTFIX [r3952453491](https://github.com/maplefukku/sauna-master/pull/297#discussion_r3952453491) は `disposition:reject` の decision 行である。OOS [r3952411869](https://github.com/maplefukku/sauna-master/pull/297#discussion_r3952411869)、cousin の TeX color [r4028777512](https://github.com/maplefukku/sauna-master/pull/297#discussion_r4028777512)、UBA/RLO と ruby/MathML [r4029228334](https://github.com/maplefukku/sauna-master/pull/297#discussion_r4029228334) は `disposition:oos` である。mill の教訓は `critique_human` 1 行である。

boundary issue を FILE するまで、seed の `github_url` は issue 140 を指す。FILE したら人が差し替える。#297 は reopen しない。live apply は #287 であり、merge=PM である。

```sh
scripts/quiet-test.sh -- python3 scripts/intent_memory/read.py --tags adv product:sauna-master --fixture scripts/intent_memory/fixtures.json --reader cli
scripts/quiet-test.sh -- python3 scripts/intent_memory/disposition.py --dry-run --path <records.json>
```

## Domain WRAP

LOCK は GitHub Actions に依存しない。このページと [`scripts/test_adv_disposition_lock.py`](../../scripts/test_adv_disposition_lock.py) が持つ。[`scripts/ci.py`](../../scripts/ci.py) の `adv-disposition-lock` 経由で走る。証拠は `scripts/quiet-test.sh -- python3 scripts/ci.py` である。Quiet is not skip。新しい harness は置かない。

## 関連

出荷単位は [`README.md`](./README.md) である。PR 本文の 4 見出しは [`pr-body.md`](./pr-body.md) である。CI 梯子は [`ci-ladder.md`](./ci-ladder.md) である。読み方は [`read-recipe.md`](../intent-memory/read-recipe.md) である。
