# routine: maintain-verification

| 項目 | 値 |
|---|---|
| 目的 | 各プロダクトの検証スキルと feature map を腐らせない |
| 担当ボット | <専用ボット名>（メインボットには貼らない） |
| スケジュール | 1 日 1 回 |
| 出力先 | メインボットへの 1 通の結果報告 |
| 状態 | 下書き |

feature map はすぐ腐ります。Lauren はこれを **毎日** 回すことを繰り返し勧めています。強い検証スキルは品質・生産性・自動化の土台になるチームインフラです。

## プロンプト本文（Grok Bot に貼るもの）

```text
For each repository listed in grok-bot-ops/products/ that has a
verification skill:

Launch a Cursor cloud agent on that repository with this task:
  /maintain-verification-skill

Collect each agent's outcome. The skill ends in exactly one of:
  clean   - full coverage, nothing to ship
  changed - one PR of proven corrections, confined to the verify skill
  blocked - names the blocker

Send me one message: a table of product / outcome / PR link if any /
blocker if any, plus the count of products checked. If a live pass
caught a product regression, flag it first - that is a factory input,
not a docs fix.
```

## 備考

- `/maintain-verification-skill` はプロダクトコードを編集しない。`changed` の PR は検証スキルのディレクトリに閉じる。
- `blocked` や回帰の報告は、intake 系と同じく「工場に投げる素材」として扱う。
- まだ検証スキルが無いプロダクトは、先に [`automations/verification-bootstrap/`](../automations/verification-bootstrap/FOR_AGENTS.md) で立てる。
