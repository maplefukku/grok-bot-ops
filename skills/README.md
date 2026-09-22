# skills/

自作スキルの置き場です。Lauren の指示はこうです。最初から全スキルを入れない。効いたものだけ科学的に足す。

## #136 jenny-lite stall-adopt A–D（既存 4 本のみ）

既存 sand-workflow へ jenny-lite A–D を encode した。**第六 workflow 名は invent しない。** SoftHOLD merge=PM。CreateAgent NONE。

| Mode | Encode into | Path |
|---|---|---|
| A factory BROKEN until trusted fire | fleet-stall-sweep + author-routines + schedules-force-agency | `skills/fleet-stall-sweep/` `skills/author-routines/` `skills/schedules-force-agency/` |
| B JOB-flat idle-with-leftover ≥3 same-day | conductor-keep-moving + existing weekday pulses（監視 / 開発リーダー）。新 `weekday-pulse-cascade` skill は encode 先にしない | `skills/conductor-keep-moving/` |
| C agency silent-miss | schedules-force-agency | `skills/schedules-force-agency/` |
| D not-eng-only checklist | fleet-stall-sweep | `skills/fleet-stall-sweep/` |

Live SoT は box sand-workflow。このディレクトリは #136 の reviewable mirror である。出典 issue: https://github.com/maplefukku/grok-bot-ops/issues/136

## S1–S7（issue #12）

`author-shared-skill` / `fleet-stall-sweep` / `completion-handoff` / `fleet-composition-review` / `job-brief` / `ci-health-sweep` / `account-design-pack` はフリートの sand-workflow。上表の 4 本以外をこのディレクトリへ足すのは スキル作成が eval を通したあと。1 スキル 1 PR。新 skill 名 / Jenny seat / scanner / dash は invent しない。

初回 push 前セキュリティ監査の手順 WRAP は S1–S7 外である。[`docs/process/security-audit-wrap.md`](../docs/process/security-audit-wrap.md)（Fleet [security-audit-wrap](sand-workflow:security-audit-wrap)）。

`job-brief` / Cloud開発 (`sand-workflow:cloud`) / PR確認 (`sand-workflow:pr`) / 開発からPRグリーン (`sand-workflow:pr-2`) の PR 本文は [`docs/process/pr-body.md`](../docs/process/pr-body.md) である。recipe SoT は box `/workspace/fleet-scripts/pr-show-me-template.md` である。見出し表はそちらだけ。このディレクトリに第二のチェックリストは置かない。

`job-brief` と Cloud開発 (`sand-workflow:cloud`) の CI 梯子は [`docs/process/ci-ladder.md`](../docs/process/ci-ladder.md) である。梯子の中身は invent しない。

## スキルを足すゲート

1. 同じやり方が 2 回以上、実作業で効いたこと（1 回は逸話。`lessons/` 止まり）
2. [Authoring or modifying a skill プレイブック](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/authoring-a-skill.md) を通して書くこと。`SKILL.md` の手書き禁止
3. [Eval プレイブック](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/eval.md) の盲検評価を通し、結果を `evals/` に残すこと
4. 1 スキル 1 PR。機能作業に絡めて出荷しない

置き方は pstack と同じ形式です: `skills/<name>/SKILL.md`。ここに置いたスキルは、このリポジトリをプラグインとして読み込んだボットから使えます。

自分の作業履歴からモードを生やすなら `/automate-me`（生成先は各自の `.cursor/skills/<your-name>-mode/`）。ここに昇格させるのは、チームや複数ボットで共有する価値が証明されてからです。
