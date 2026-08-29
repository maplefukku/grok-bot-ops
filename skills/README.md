# skills/

自作スキルの置き場です。**いまは意図的に 0 個です。**

Lauren の指示はこうです。最初から全スキルを入れない。スキル 0 で観察し、効いたものだけ科学的に足す。

## スキルを足すゲート

1. 同じやり方が 2 回以上、実作業で効いたこと（1 回は逸話。`lessons/` 止まり）
2. [Authoring or modifying a skill プレイブック](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/authoring-a-skill.md) を通して書くこと。`SKILL.md` の手書き禁止
3. [Eval プレイブック](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/eval.md) の盲検評価を通し、結果を `evals/` に残すこと
4. 1 スキル 1 PR。機能作業に絡めて出荷しない

置き方は pstack と同じ形式です: `skills/<name>/SKILL.md`。ここに置いたスキルは、このリポジトリをプラグインとして読み込んだボットから使えます。

自分の作業履歴からモードを生やすなら `/automate-me`（生成先は各自の `.cursor/skills/<your-name>-mode/`）。ここに昇格させるのは、チームや複数ボットで共有する価値が証明されてからです。
