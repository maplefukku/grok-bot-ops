# docs/laststitch/

最後の一針 / LAST STITCH LAB の Instagram Professional（Creator）を、ふっくーの HITL だけで成立させる docs。publish ボットではない。パスワードと 2FA とトークンはボットが触らない。

Refs #8: https://github.com/maplefukku/grok-bot-ops/issues/8

出典は Meta と Instagram の公式ヘルプだけ。二次ブログと GitHub のスキルは置かない。`products/` エントリは作らない。

## 誰が何をするか

| 誰 | すること | しないこと |
|---|---|---|
| docs ボット | このパックを書く。出典を貼る。PR を積む | Instagram ログイン、作成、投稿、DM。マージ。秘密の受領 |
| ふっくー | iPhone で HITL。秘密は手元。[account.md](./account.md) に確定値 | ボットへのコード送付。未受理の visual を載せる |
| 人間 | PR を見てマージ。CI 赤はマージしない | なし |

Linux は docs と CI と PR だけ。Instagram に触れない。ボットはマージしない。

## ファイル

| ファイル | 内容 |
|---|---|
| [name.md](./name.md) | 表示名、溢れ規則、handle fallback。表示名のカタカナは入れない |
| [bio.md](./bio.md) | 貼り付け用 bio。**非公式** 必須 |
| [visual-lock.md](./visual-lock.md) | 見た目の候補。禁止リスト。ふっくー受理待ち |
| [meta-taps.md](./meta-taps.md) | iPhone HITL。新規作成は公式の Facebook なし経路。切替は Meta UI のみ |
| [ip-stance.md](./ip-stance.md) | オリジナル・コントロール、三次、非公式。法律判断なし |
| [first-7-days.md](./first-7-days.md) | D0 から D1 はプロフィールと設定。既定は投稿なし |
| [account.md](./account.md) | 書き戻しテンプレート。いまは pending。トークンなし |

## HITL 順序

1. ふっくーがメールと電話を用意する。iPhone の Instagram アプリ。
2. 新規作成。公式の「Facebook アカウントなし」経路だけ。タップを足さない。
3. `@laststitch.lab`。拒否なら `@laststitchlab`。
4. 名前と [bio.md](./bio.md)。
5. 2FA は Authentication app。有効化は Instagram アプリのみ。バックアップコードはふっくーだけ。
6. professional へ切替し、**Creator** を選ぶ。Page は Skip。Don't use my contact info。カテゴリラベルは隠す。
7. professional は非公開にできない。公開前提だけ書く。
8. 確定値を [account.md](./account.md) に書く。スクショにコードを写さない。

詳細タップは [meta-taps.md](./meta-taps.md)。D0 から D1 は [first-7-days.md](./first-7-days.md)。

- 出典: https://help.instagram.com/155940534568753 （取得: 2026-09-05）
- 出典: https://www.facebook.com/help/instagram/155940534568753 （取得: 2026-09-05）
- 出典: https://www.facebook.com/business/help/502981923235522 （取得: 2026-09-05）
- 出典: https://www.facebook.com/help/instagram/2358103564437429 （取得: 2026-09-05）
- 出典: https://www.facebook.com/help/instagram/566810106808145 （取得: 2026-09-05）

アカウントが存在し account.md が書き戻されるまで、IG 運用と Pika と Graph は開始しない。切替は Meta UI。Graph を切替手段として書かない。

## 検証

- 表示名 `最後の一針 / LAST STITCH LAB` にカタカナなし
- bio に 非公式
- visual-lock に TechieBySA の蝶、猫、薔薇、元動画の禁止
- 切替は Meta UI
- 手順と政策の文に公式ドメインと取得日
- `python3 scripts/ci.py` が通る
