# grok-bot-ops

Grok Bot と pstack を、秘書ではなく **検証可能なエージェント工場** として使うためのリポジトリです。

今回入っている本文は [pstack 公式ガイド](https://github.com/cursor/plugins/tree/main/pstack/docs/guide) の日本語訳だけです。ほかの箱は、運用ノウハウを足していくための空ディレクトリです。

エージェントは先に [`AGENTS.md`](./AGENTS.md) を読んでください。

## いま読めるもの

| 場所 | 内容 |
|---|---|
| [`docs/guide/`](./docs/guide/README.md) | pstack 公式ガイドの日本語訳。セットアップから一晩放置まで |

原文: [github.com/cursor/plugins/tree/main/pstack/docs/guide](https://github.com/cursor/plugins/tree/main/pstack/docs/guide)  
導入: Cursor では `/add-plugin pstack`、Grok Bot では `grokbot://app/v1/plugin/add?id=9717366`

## ディレクトリ構成

ノウハウを足すときの置き場所です。空のディレクトリは `.gitkeep` だけ置いてあります。

```text
docs/
  guide/            公式ガイド日本語訳（今回の本体）
  philosophy/       基本思想（Laziness / Impatience / Hubris）
  factory/          工場の全体像
    outer-loop/     Grok Bot routines。次に投げる仕事を耕す
    inner-loop/     pstack + cloud agents。所有・検証・出荷
    swarm/          安い高速ワーカーを大量に生やす
    coordinator/    ローカル1体、仕事はクラウドへ
  verification/     検証スキルとフィーチャーマップ
  skills/           スキルの使い分け
  grok-bot/         プロダクト機能
    routines/       定期実行とコスト
    plugins/        プラグインとディープリンク
    ui/             Make Bot UI / botvillage
    access/         言語・アプリ・加入
  recipes/          最短で真似する手順

knowhow/            現場で効いたこと
  poteto/           @poteto 投稿ベース
  operations/       運用 tips
  cost/             トークンとスケジュール
  models/           モデル選定

playbooks/          実例プレイブック
  swarm/
  overnight/
  bot-ui/

agents/             grok-bot が実行時に読むもの
  skills/
  rules/
  prompts/

automations/        routine / webhook の定義
  routines/
  webhooks/

sources/            出典・原文リンク
```

## 足し方

1. 空の箱に Markdown を置く。`.gitkeep` は本文が入ったら消してよい。
2. スキルやルールは `agents/`、定期実行は `automations/`、人間向けの説明は `docs/` か `knowhow/`。
3. 出典があるなら `sources/` にリンクを残す。
