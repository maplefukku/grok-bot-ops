# routine: maintain-verification

| 項目 | 値 |
|---|---|
| 目的 | 各プロダクトの検証スキルと feature map を腐らせない |
| 担当ボット | <専用ボット名>（メインボットには貼らない） |
| スケジュール | 1 日 1 回 |
| 出力先 | メインボットへの 1 通の結果報告 |
| 状態 | 下書き |

feature map はすぐ腐ります。Lauren はこれを **毎日** 回すことを繰り返し勧めています。強い検証スキルは品質・生産性・自動化の土台になるチームインフラです。

## 書き込み先（これ以外は禁止）

- **対象プロダクトリポジトリ**: `.cursor/skills/verify-<app>/` だけ（`/maintain-verification-skill` の出力）。プロダクトコードは禁止
- **このリポジトリ**: `products/` の台帳書き戻しだけ。検証スキル本体はここに置かない

## since last run

前回確認は各プロダクト台帳の `最終確認日`。値が `未` なら、そのプロダクトはまだ maintain が一度も書き戻していない。対象の選び方は台帳を読むこと。別ファイルのカーソルは持たない。

## 台帳への書き戻し

各プロダクトの cloud agent が終わったら、https://github.com/maplefukku/grok-bot-ops の `products/<名前>.md` を更新する。

| 欄 | 書く値 |
|---|---|
| 最終確認日 | その日の UTC 日付 `YYYY-MM-DD` |
| 最終 outcome | `clean` / `changed` / `blocked` |
| 最終 PR | `changed` ならプロダクト側 PR の URL。それ以外は `無し` |

書き戻しは draft PR にする。マージは人間。検証スキル本体はプロダクト側、台帳は ops 側、という境界は [`automations/verification-bootstrap/FOR_AGENTS.md`](../automations/verification-bootstrap/FOR_AGENTS.md) と同じ。

## プロンプト本文（Grok Bot に貼るもの）

```text
For each repository listed in
https://github.com/maplefukku/grok-bot-ops/tree/main/products
that has a verification skill:

Launch a Cursor cloud agent on that repository with this task:
  /maintain-verification-skill
  Write only inside .cursor/skills/verify-<app>/. No product code.
  Open a draft PR if you have corrections. Do not merge.

Collect each agent's outcome. The skill ends in exactly one of:
  clean   - full coverage, nothing to ship
  changed - one PR of proven corrections, confined to the verify skill
  blocked - names the blocker

Then launch one Cursor cloud agent on
https://github.com/maplefukku/grok-bot-ops
with this task:
  For each product you just checked, update products/<name>.md:
  最終確認日 = today's UTC YYYY-MM-DD,
  最終 outcome = clean|changed|blocked,
  最終 PR = the product PR URL or 無し.
  Write only under products/. Open one draft PR. Do not merge.

Send me one message: a table of product / outcome / PR link if any /
blocker if any, plus the count of products checked. If a live pass
caught a product regression, flag it first - that is a factory input,
not a docs fix.
```

## 備考

- `/maintain-verification-skill` はプロダクトコードを編集しない。`changed` の PR は検証スキルのディレクトリに閉じる。
- `blocked` や回帰の報告は、intake 系と同じく「工場に投げる素材」として扱う。
- まだ検証スキルが無いプロダクトは、先に [`automations/verification-bootstrap/`](../automations/verification-bootstrap/FOR_AGENTS.md) で立てる。
- draft PR のマージは人間。ボットは draft のまま。ルールは [`AGENTS.md`](../AGENTS.md) の「draft PR のマージ」。

### 手動 1 周チェックリスト（未実施）

この原稿を Grok Bot に貼って 1 周回した記録はまだ無い。嘘の「確認済」は書かない。プロダクト台帳が空のあいだは、回す対象が無い。

- [ ] 対象プロダクトを `products/` に登録し、検証スキルを立てた
- [ ] 担当ボットを作り、grok-bot-ops と各プロダクトリポジトリへの書き込み権限を付けた
- [ ] Cursor cloud agent を対象リポジトリと grok-bot-ops の両方で起動できる
- [ ] プロダクト側の verify PR と、ops 側の台帳書き戻し PR が draft で開く
- [ ] マージ担当は人間（オーナー）。毎日 draft を見る。ボットはマージしない
