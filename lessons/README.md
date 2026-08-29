# lessons/

`/reflect` で受理された教訓だけを置きます。

```text
/reflect that took way too long. capture what we learned so the next run doesn't repeat it.
```

`/reflect` は提案を `Accepted` / `Rejected` / `Backlog` に分け、承認を待ちます。ここに書くのは **Accepted だけ** です。奇妙なセッション 1 回は逸話であり、規則ではありません。

## 記録の形式

1 教訓 1 ファイル: `lessons/<YYYY-MM-DD>-<slug>.md`

- 何が起きたか（1 段落）
- 将来のどの判断を変えるか（これが書けないなら受理しない）
- 出典（セッション、PR、decisions.tsv へのポインタ）

## 卒業ルール

同じ教訓を 2 回書いたら、それは文章でなく構造にする番です（[Encode Lessons in Structure](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-encode-lessons-in-structure/SKILL.md)）。lint、チェック、スクリプト、または `evals/` のゲートを通して `skills/` のスキルへ。
