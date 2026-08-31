# docs/laststitch/

最後の一針 / LAST STITCH LAB の Instagram Professional（Creator）を、ふっくーの HITL だけで成立させる docs。publish ボットではない。パスワードと 2FA とトークンはボットが触らない。

Refs #8: https://github.com/maplefukku/grok-bot-ops/issues/8

OSS-SURVEY 2026-08-31（PdM）を折り込んだ。OSS に IG Professional の drop-in SPEC は無い。instagram-skills は wrap しない。

## 誰が何をするか

| 誰 | すること | しないこと |
|---|---|---|
| docs ボット | このパックを書く。出典を貼る。draft PR を積む | Instagram ログイン / 作成 / 投稿 / DM。マージ。秘密の受領 |
| ふっくー | iPhone で HITL。秘密は手元。[account.md](./account.md) に確定値 | ボットへのコード送付。未受理の visual を載せる |
| 人間 | draft PR を見てマージ。CI 赤はマージしない | — |

Linux は docs / CI / draft PR だけ。Instagram に触れない。ボットはマージしない。

## ファイル

| ファイル | 内容 |
|---|---|
| [name.md](./name.md) | 表示名、溢れ規則、handle fallback。表示名のカタカナ 0 |
| [bio.md](./bio.md) | 貼り付け用 bio。**非公式** 必須 |
| [visual-lock.md](./visual-lock.md) | 見た目の候補。禁止リスト。ふっくー受理待ち |
| [meta-taps.md](./meta-taps.md) | iPhone HITL。新規作成は公式 Accordion 1。切替は Meta UI のみ |
| [ip-stance.md](./ip-stance.md) | オリジナル・コントロール / 三次 / 非公式。法律判断なし。API 切替なし |
| [first-7-days.md](./first-7-days.md) | D0–D1 はプロフィールと設定。既定は投稿なし |
| [account.md](./account.md) | 書き戻しテンプレート。いまは pending。トークンなし |
| [schema.md](./schema.md) | 汎用フィールド。laststitch は instance 1 |
| [schema.yaml](./schema.yaml) | 同上の機械可読 |

`products/` エントリは作らない。`docs/knowhow` / `docs/guide` / `bots/` / `routines/` / `skills/` / SPEC.yaml / X 本文 / note / GTM は書かない。SDK ファイルも置かない。

## HITL 順序

1. ふっくーがメール / 電話を用意する。iPhone の Instagram アプリ。
2. 新規作成。iPhone Accordion 1（Facebook なし）。https://help.instagram.com/155940534568753/?cms_platform=iphone-app&helpref=platform_switcher （取得: 2026-08-31）。タップを足さない。Facebook 経由は勧めない。
3. `@laststitch.lab`。拒否なら `@laststitchlab`。
4. 名前と [bio.md](./bio.md)。
5. 2FA Authentication app（有効化は Instagram アプリのみ）。バックアップコードはふっくーだけ。
6. professional → **Creator**（Meta UI のみ。Business ではない）。Page Skip。Don't use my contact info。カテゴリラベル非表示。
7. professional は非公開不可。公開前提。非公開のままを勧めない。
8. [account.md](./account.md) に確定値。スクショにコードを写さない。

詳細タップは [meta-taps.md](./meta-taps.md)。D0–D1 は [first-7-days.md](./first-7-days.md)。

## PATH（1–6。あとで。この PR では実装しない）

1. Switch-to-professional HITL **Creator**（Business ではない）+ カテゴリ。**Meta UI only**
2. Facebook Page なし（あとで使う Instagram Login 経路）
3. あとで: Business-type Meta app + Instagram product
4. あとで: Instagram Login → `graph.instagram.com`
5. あとで: short（code 1 hour）→ long（`expires_in` 秒、約 60 days）。トークンはこの docs に置かない
6. publish はあと。D0–D1 はプロフィールだけ。初投稿は HITL iPhone。**publish-bot なし**

Graph が personal を Professional に変えるとは書かない。Facebook Login 経路は使わない（Page が要る。LOCK は Page Skip）。

- 出典: https://www.facebook.com/help/instagram/2358103564437429 （取得: 2026-08-31）
- 出典: https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-facebook-login/business-login-for-instagram （取得: 2026-08-31）
- 出典: https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-instagram-login （取得: 2026-08-31）
- 出典: https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-instagram-login/business-login （取得: 2026-08-31）
- 出典: https://developers.facebook.com/blog/post/2024/07/30/instagram-api-with-instagram-login/ （取得: 2026-08-31）

アカウントが存在し account.md が書き戻されるまで、IG 運用と Pika と Graph は開始しない。

## SDK（メモだけ。このリポにコードは置かない）

製品リポが後で依存を足すとき、`facebook-*-business-sdk` は **v26.0.1 を保つ**。fork しない。codegen fork しない。community wrapper を製品 SDK にしない。OAuth と list-connected-IG は、あとで薄い in-tree。NEW-SDK なし。**この grok-bot-ops に SDK ファイルを足さない。**

## 検証（このパック）

- 表示名 `最後の一針 / LAST STITCH LAB` にカタカナ 0
- bio に 非公式
- visual-lock に TechieBySA の蝶・猫・薔薇・元動画の禁止
- 切替は Meta UI。Graph 切替を主張しない
- 手順と政策の文に公式ドメインと取得日
- `python3 scripts/ci.py` が通る
