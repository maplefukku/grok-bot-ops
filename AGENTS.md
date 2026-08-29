# AGENTS.md

このリポジトリは、Grok Bot と Cursor エージェントが **検証可能な出荷** をするための運用知置き場です。チャットの雑用メモではなく、再現できる手順と証拠の置き場として扱ってください。

## 最初に読む

1. [`README.md`](./README.md) — 箱の地図
2. [`docs/guide/README.md`](./docs/guide/README.md) — pstack の使い方（日本語訳）

スキル本体（`SKILL.md`）はこのリポジトリにはありません。ガイド内のスキルリンクは [cursor/plugins の pstack](https://github.com/cursor/plugins/tree/main/pstack) を指します。

## 作業の原則

- 入口は `/poteto-mode`。個別スキルを列挙してマイクロマネジメントしない。
- ゴールと、合否が分かる完了条件を先に書く。
- ビルドが通ったことは証拠にしない。本物のコマンド、画面、保存された値、プロファイルを取る。
- 判断は [`/show-me-your-work`](https://github.com/cursor/plugins/blob/main/pstack/skills/show-me-your-work/SKILL.md) のログに残す。差分より判断を監査する。
- 空ディレクトリ（`.gitkeep` のみ）は、これからノウハウを足す箱です。今回の本文は `docs/guide/` だけです。

## まだ空の箱

`docs/philosophy/`、`docs/factory/`、`docs/verification/`、`docs/skills/`、`docs/grok-bot/`、`docs/recipes/`、`knowhow/`、`playbooks/`、`agents/`、`automations/`、`sources/`。

これらを埋める仕事を頼まれたときだけ書いてください。推測で埋めないこと。
