# 最初の 7 日

D0 から D1 はプロフィールと設定だけ。既定は投稿しない。初投稿はふっくーが決めたときだけ、HITL で iPhone から手動。publish-bot なし。Pika なし。Graph は、Professional（Creator）が存在し [account.md](./account.md) が書き戻されたあと。D0 では始めない。切替は Meta UI だけ。Graph が personal を Professional に変えるとは書かない。

関連: [meta-taps.md](./meta-taps.md) · [visual-lock.md](./visual-lock.md) · [name.md](./name.md) · [bio.md](./bio.md) · [README.md](./README.md)

## D0 から D1（やる）

| 項目 | 内容 | 状態の見方 |
|---|---|---|
| 表示名 | [name.md](./name.md)。第一 `最後の一針 / LAST STITCH LAB`。ダメなら `最後の一針` | 画面の名前欄 |
| handle | `@laststitch.lab`。拒否なら `@laststitchlab` | [account.md](./account.md) |
| bio | [bio.md](./bio.md)。**非公式** 必須 | 画面の bio |
| プロフィール画像 | [visual-lock.md](./visual-lock.md) をふっくーが受理したあとだけ。作成時は公式 Skip 可。プロフィール画像を初投稿にしない | 未受理なら空のまま可 |
| 2FA | Authentication app。バックアップコードはふっくーだけ | 方式名だけ書き戻す |
| 種別 | Creator（Meta UI のみ。Business ではない） | professional は非公開にできない |
| Facebook Page | Skip。今は繋がない | skipped |
| 連絡先 | Don't use my contact info | 未使用 |
| カテゴリラベル | 画面で最も近いカテゴリを選び、ラベルは隠す | 非表示 |
| ウェブサイト | 置かない。URL を発明しない | なし |

Professional 切替は公開前提。非公開のままにする提案はしない。個人アカウントが非公開なら、切替で公開になり、未承認のフォローは自動承認されると公式が書いている。

- 出典: https://www.facebook.com/help/instagram/2358103564437429 （取得: 2026-09-05）
- 出典: https://www.facebook.com/business/help/502981923235522 （取得: 2026-09-05）
- 出典: https://www.facebook.com/business/help/138925576505882 （取得: 2026-09-05）
- 出典: https://www.facebook.com/help/instagram/517073653436611 （取得: 2026-09-05）

名前、username、画像の更新は Edit profile または Accounts Center。bio は最大 150 characters（公式）。プロフィール画像は誰でも見られる。

- 出典: https://www.facebook.com/help/instagram/583107688369069 （取得: 2026-09-05）
- 出典: https://www.facebook.com/help/instagram/728994388226960 （取得: 2026-09-05）
- 出典: https://www.facebook.com/help/instagram/557544397610546 （取得: 2026-09-05）
- 出典: https://www.facebook.com/help/instagram/347751748650214 （取得: 2026-09-05）
- 出典: https://www.facebook.com/help/instagram/155940534568753 （取得: 2026-09-05）

2FA の Authentication app は Instagram アプリ（Android と iPhone）でのみオンにできる。追加デバイスは day-0 必須ではない。

- 出典: https://www.facebook.com/help/instagram/566810106808145 （取得: 2026-09-05）
- 出典: https://www.facebook.com/help/instagram/1124604297705184 （取得: 2026-09-05）

## D0 から D1（やらない）

- 初投稿（既定）。作成時にプロフィール画像を初投稿として共有しない
- ふっくーが後で HITL iPhone 手動と決めたときだけ、別途投稿してよい
- 予約投稿、publish-bot、Graph API、Pika、工場、IG 運用ボット
- Graph や API での personal から Professional 切替（手段として存在させない）
- Page 接続、連絡先の公開、カテゴリラベルの表示
- Linux からの Instagram 操作
- ボットへのコード、パスワード、トークン送付

## D2 から D7

D0 から D1 と同じ禁止。Graph は、Creator が存在し account.md が埋まってから。実装はこのパックではしない。

## 完了

[account.md](./account.md) の pending を確定値に置き換える。コードもトークンも写っていないこと。その時点でも IG 運用と Pika と publish-bot は開始していない。
