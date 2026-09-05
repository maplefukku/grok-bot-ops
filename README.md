# grok-bot-ops

Grok Bot でプロダクト開発を回すための **司令室リポジトリ** です。工場そのものではありません。

役割は 2 つです。3 層の工場（下図）を運転するための記録と原稿を持つこと、そして **Grok Bot 全般のノウハウを人に縛らず貯める** ことです。工場の骨格は Lauren（@poteto）の運用を下敷きにしていますが、ノウハウの出典は問いません。

```text
【外側ループ】 Grok Bot 本体
    routine が Slack のバグ、X の苦情、アイデアを耕す
    メインボットはチーフ・オブ・スタッフ。定期作業は専用ボットへ
          │ 次に工場へ投げる仕事
          ▼
【内側ループ】 各プロダクトリポジトリ
    /poteto-mode が入口。cloud agents が所有・検証・出荷
    ローカルは coordinator 1体、仕事は全部クラウドへ
          │ 信頼の根拠
          ▼
【検証インフラ】 同じプロダクトリポジトリの中
    .cursor/skills/verify-<app>/ + feature map
    毎日 /maintain-verification-skill で腐らせない
    マージ前は差分より /show-me-your-work（判断の監査）
```

## 何がどこに住むか

| もの | 住む場所 | このリポジトリが持つもの |
|---|---|---|
| スキル本体（pstack） | [cursor/plugins の pstack](https://github.com/cursor/plugins/tree/main/pstack) | 使い方の日本語ガイド（`docs/guide/`） |
| 検証スキル・feature map | **各プロダクトリポジトリ** の `.cursor/skills/verify-<app>/` | 立ち上げ用パック（`automations/verification-bootstrap/`）と台帳（`products/`） |
| 稼働中の routine | Grok Bot 本体の設定 | 原稿と運用ルール（`routines/`）。ここが正本、貼り付け先が実体 |
| Grok Bot のノウハウ | このリポジトリの `docs/knowhow/` | アップデート情報と活用法。X から定期収集して貯める。出典リンク必須 |
| 自作スキル | このリポジトリの `skills/`（プラグインとして読み込む） | 最初は 0 個。評価を通ったものだけ増える |
| 教訓 | `lessons/` | `/reflect` で受理されたものだけ |

## ディレクトリ

```text
.cursor-plugin/plugin.json   このリポジトリ自体が Cursor プラグイン
.cursor/hooks.json           Cloud Agent が scripts/ci.py を回す（wrapper: .cursor/hooks/run-ci.py）
.github/workflows/ci.yml     相対リンク・knowhow 出典・plugin.json・intent-memory 契約
scripts/ci.py                上と同じ検査（ローカルでもこれを実行）
scripts/intent_memory/       Intent/Memory の query contract と fixture テスト
skills/                      自作スキル。スキル0から始め、evalを通ったものだけ足す
routines/                    Grok Bot routine の原稿（外側ループの正本）。使いながら増やす
  examples/                  プロダクトを持ったとき用の型見本
products/                    工場が出荷するプロダクトの台帳
automations/
  verification-bootstrap/    プロダクトに検証スキルを立てる移植パック
evals/                       スキル・プロンプト変更の盲検評価の記録
lessons/                     /reflect で受理された教訓
docs/
  guide/                     pstack 公式ガイドの日本語訳
  knowhow/                   Grok Bot 全般のノウハウ（人に縛らない。出典リンク必須）
  laststitch/                IG Creator HITL パック（最後の一針）。アカウントができるまで運用しない
  mini-ops/                  Mini運用の常設手順（worktree prune）
  decisions/                 ADR。Intent/Memory は 0001
  intent-memory/             schema.sql と read recipe。GitHub LOCK の代替ではない
AGENTS.md                    エージェントが最初に読むもの
```

## 最短で工場を立ち上げる

1. Grok Bot に pstack を入れる: `grokbot://app/v1/plugin/add?id=9717366`（Cursor なら `/add-plugin pstack`）
2. `/setup-pstack` でトークン効率のよいモデル（Grok 4.6 / Auto）を選ぶ
3. プロダクトごとに検証スキルを立てる。cloud agent に [`automations/verification-bootstrap/FOR_AGENTS.md`](./automations/verification-bootstrap/FOR_AGENTS.md) を読ませ、対象リポジトリを名指す
4. [`routines/maintain-verification.md`](./routines/maintain-verification.md) を毎日の routine として専用ボットに貼る
5. [`routines/collect-grokbot-knowhow.md`](./routines/collect-grokbot-knowhow.md) を専用ボットに貼り、Grok Bot のノウハウを貯め始める。プロダクト固有の収集（Slack バグ、X の反応）は [`routines/examples/`](./routines/examples/) の型から、必要になったときに起こす
6. 日常は `/poteto-mode`。大きい仕事は `/goal` `/loop` `/swarm` + cloud agents
7. マージ前は `/show-me-your-work` で判断ログを見る
8. 効いたやり方が 2 回繰り返されたら、`evals/` のゲートを通して `skills/` に結晶させる

詳しい使い方は [`docs/guide/`](./docs/guide/README.md)（pstack 公式ガイド日本語訳）、Grok Bot 自体の知識は [`docs/knowhow/`](./docs/knowhow/README.md)。
