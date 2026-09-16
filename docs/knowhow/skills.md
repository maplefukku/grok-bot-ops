# skills

Grok Bot の skill（再利用できる手順の単位）の作り方と使い方。Teach a task の手順は [`routines.md`](./routines.md) にある。

## skill と routine の順序（recipe と alarm）

- 内容: skill は recipe（how）、routine は alarm（when）。一度タスクを完走してから skill として保存し、その後 routine でスケジュールする、という順序。
- 出典: [x.com/Tesla_FANtastic/status/2099877085439283361](https://x.com/Tesla_FANtastic/status/2099877085439283361) · [x.com/grokbotrocks/status/2100065882013610339](https://x.com/grokbotrocks/status/2100065882013610339)（2026-09-15）
- 確認: 未

## Notion 3.7 Agent Skills

- 内容: Notion で skill を作成・更新し、SKILL.md と supporting files として Claude Code、Codex、Cursor、Gemini、Grok へダウンロードできる。
- 出典: [notion.com/releases/2026-09-15](https://www.notion.com/releases/2026-09-15) · [help: create and manage skills](https://www.notion.com/help/create-and-manage-skills)（2026-09-15）
- 確認: 未

## skill は再利用できるワークフローの単位

- 内容: skill は「いつ使うか、手順、判断ルール、期待する出力、境界」を持つ再利用できるレシピ。自分で書く、直す、Teach a task で Bot のコンピュータ上の作業を録画してデモから下書きさせる、のいずれでも作れる。チャットの記憶は 1 会話に閉じるが、skill は自分の全 Bot で共有され、他の Bot が呼べ、routine が指せ、template に指示・skill・routine をまとめて同梱して配れる、という主張。
- 出典: [x.com/brianzhan1/status/2097455378179162132](https://x.com/brianzhan1/status/2097455378179162132)（2026-09-08）
- 確認: 未
