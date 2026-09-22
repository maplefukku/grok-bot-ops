# skills/

自作スキルの置き場です。**いまは意図的に 0 個です。**

Lauren の指示はこうです。最初から全スキルを入れない。スキル 0 で観察し、効いたものだけ科学的に足す。

## #136 jenny-lite stall-adopt A–D（plugin には載せない）

A–D の encode 先は **box sand-workflow** である（[fleet-stall-sweep](sand-workflow:fleet-stall-sweep) / [author-routines](sand-workflow:author-routines) / [schedules-force-agency](sand-workflow:schedules-force-agency) / [conductor-keep-moving](sand-workflow:conductor-keep-moving)）。手順 WRAP は [`docs/process/jenny-lite-stall-adopt.md`](../docs/process/jenny-lite-stall-adopt.md)。

`.cursor-plugin/plugin.json` の `"skills": "./skills/"` は **plugin HARD** である。ここへ `SKILL.md` を置くとボット全員が実行する。Soft Flag N 「reviewable mirror」。Soft Flag N eval / 1 スキル 1 PR ゲートの例外書き。Soft Flag N fallen tip `1a58a0d` / SoftACC Prefer drop を SoT にしない。PM ACK + 文字撞突解消 DELTA と eval が揃うまで、このディレクトリは 0 個のまま。

## S1–S7（issue #12）

`author-shared-skill` / `fleet-stall-sweep` / `completion-handoff` / `fleet-composition-review` / `job-brief` / `ci-health-sweep` / `account-design-pack` はフリートの sand-workflow。このディレクトリに SKILL.md は無い。足すのは スキル作成が eval を通したあと。1 スキル 1 PR。

初回 push 前セキュリティ監査の手順 WRAP は S1–S7 外である。[`docs/process/security-audit-wrap.md`](../docs/process/security-audit-wrap.md)（Fleet [security-audit-wrap](sand-workflow:security-audit-wrap)）。

`job-brief` / Cloud開発 (`sand-workflow:cloud`) / PR確認 (`sand-workflow:pr`) / 開発からPRグリーン (`sand-workflow:pr-2`) の PR 本文は [`docs/process/pr-body.md`](../docs/process/pr-body.md) である。recipe SoT は box `/workspace/fleet-scripts/pr-show-me-template.md` である。見出し表はそちらだけ。このディレクトリに第二のチェックリストは置かない。Flag Y 述語は pr-body.md のみ。第二の Flag 定義は invent しない。

`job-brief` と Cloud開発 (`sand-workflow:cloud`) の CI 梯子は [`docs/process/ci-ladder.md`](../docs/process/ci-ladder.md) である。梯子の中身は invent しない。

## スキルを足すゲート

1. 同じやり方が 2 回以上、実作業で効いたこと（1 回は逸話。`lessons/` 止まり）
2. [Authoring or modifying a skill プレイブック](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/authoring-a-skill.md) を通して書くこと。`SKILL.md` の手書き禁止
3. [Eval プレイブック](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/eval.md) の盲検評価を通し、結果を `evals/` に残すこと
4. 1 スキル 1 PR。機能作業に絡めて出荷しない

置き方は pstack と同じ形式です: `skills/<name>/SKILL.md`。ここに置いたスキルは、このリポジトリをプラグインとして読み込んだボットから使えます。

自分の作業履歴からモードを生やすなら `/automate-me`（生成先は各自の `.cursor/skills/<your-name>-mode/`）。ここに昇格させるのは、チームや複数ボットで共有する価値が証明されてからです。
