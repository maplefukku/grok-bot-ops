# HITL タップ（iPhone Instagram アプリ）

実行者はふっくー。主経路は iPhone の Instagram アプリ。Linux は docs と CI と PR だけ。Instagram に触れない。ボットはログインしない。作成しない。投稿しない。DM しない。コードを受け取らない。

関連: [README.md](./README.md) · [name.md](./name.md) · [bio.md](./bio.md) · [account.md](./account.md) · [first-7-days.md](./first-7-days.md)

## 順序（LOCK）

1. ふっくーがメールと電話を用意する。iPhone の Instagram アプリ。
2. 新規作成。公式の「Facebook アカウントなし」経路に従う。タップを足さない。
3. username `@laststitch.lab`。拒否なら `@laststitchlab`。
4. 名前と [bio.md](./bio.md)。
5. 2FA Authentication app。有効化は Instagram アプリのみ。バックアップコードはふっくーだけ。
6. professional へ切替し、Creator を選ぶ。Page は Skip。Don't use my contact info。カテゴリラベルは隠す。
7. professional は非公開にできない。公開前提だけ書く。非公開のままを勧めない。
8. 確定値を [account.md](./account.md) に書く。スクショにコードを写さない。

Signing Up and Getting Started が入口。

- 出典: https://help.instagram.com/3257948324491837 （取得: 2026-09-05）
- 出典: https://www.facebook.com/help/instagram/3257948324491837 （取得: 2026-09-05）

## 1. 新規作成

一次は Create a new Instagram profile。2026-09-05 に facebook.com/help ミラーを読んだ。help.instagram.com の同番号は、この取得経路ではログイン壁に落ちることがある。Instagram にはログインしない。本文は facebook.com/help ミラーを正とする。

- 出典: https://www.facebook.com/help/instagram/155940534568753 （取得: 2026-09-05）
- 出典: https://help.instagram.com/155940534568753 （取得: 2026-09-05）

同ページが書いていること:

- Meta Accounts と Accounts Center の文言が出ることがある
- 13 歳以上
- 作り方は 2 つ。アプリまたは instagram.com。既存の Facebook または Instagram からも、同じ Accounts Center に新しい IG を作れる
- 最近作ったアカウントは new と出ることがある
- login info の保存は任意。HITL の手元だけ。ボットは保存しない

アコーディオン題（2026-09-05 に確認）:

- To create an account if you're new to Instagram and you don't have a Facebook account
- To create an account if you have a Facebook account

HITL は第一（Facebook なし）だけ。第二は勧めない。LOCK はオリジナル・コントロールと Page Skip。

アコーディオンの番号手順は、公式ページを iPhone App Help で開いて従う。ここに無いタップを足さない。確認コード、パスワード、誕生日、メール、電話はふっくーだけ。ボットは受け取らない。

LOCK の上書き（公式タップではない）:

- 名前: `最後の一針 / LAST STITCH LAB`。カタカナを足さない。溢れは [name.md](./name.md)
- username: `@laststitch.lab`。拒否なら `@laststitchlab`
- プロフィール画像は [visual-lock.md](./visual-lock.md) を受理してから載せる。未受理なら Skip
- プロフィール画像を初投稿にしない。[first-7-days.md](./first-7-days.md)

bio の貼り付けは作成後。

## 2. 名前、username、bio（作成後）

表示名と handle は [name.md](./name.md)。bio は [bio.md](./bio.md)。

公式 How to change your Instagram profile information（コンピュータ表記）:

Update your profile on Instagram:

1. プロフィールへ行く
2. Edit profile
3. 情報を入力して Submit

Accounts Center 経由:

1. More から Settings
2. Accounts Center の Profiles
3. 対象プロフィール
4. name、username、profile picture を更新
5. Done

公式 Add a bio:

1. プロフィールへ行く
2. Edit profile の Bio テキストボックス
3. bio を書く
4. Submit

iPhone のラベルが違うときは、同じ公式ページの iPhone アコーディオンに従う。文字数の数字は、bio の 150 characters 以外は取得ページに無い。

- 出典: https://www.facebook.com/help/instagram/583107688369069 （取得: 2026-09-05）
- 出典: https://www.facebook.com/help/instagram/728994388226960 （取得: 2026-09-05）
- 出典: https://www.facebook.com/help/instagram/110121795815331 （取得: 2026-09-05）

ウェブサイトは公式に、コンピュータでは使えないとある。今は置かない。URL を発明しない。

- 出典: https://www.facebook.com/help/instagram/362497417173378 （取得: 2026-09-05）

## 3. 2FA（Authentication app）

LOCK は Authentication app。SMS と WhatsApp は選ばない。

公式注記（そのまま）: 「Two-factor authentication through an authentication app can only be turned on using the Instagram app for Android and iPhone.」

Linux ではオンにしない。ボットに確認コードを送らない。

推奨例として公式が挙げるアプリ: Duo Mobile または Google Authenticator。

公式 Use an authentication app for two-factor authentication on Instagram（取得本文は Click 表記。有効化は iPhone アプリ）:

1. Accounts Center の Password and security
2. Two-factor authentication から対象アカウント
3. Authentication app を選び、Next
4. 認証アプリの confirmation code を入力

バックアップコード: ふっくーだけが持つ。公式は clipboard、スクショ、別保存を書いている。リポジトリとボットには貼らない。[account.md](./account.md) のスクショにコードを写さない。

追加デバイスは day-0 必須ではない。

- 出典: https://www.facebook.com/help/instagram/566810106808145 （取得: 2026-09-05）
- 出典: https://help.instagram.com/566810106808145 （取得: 2026-09-05）
- 出典: https://www.facebook.com/help/instagram/1582474155197965 （取得: 2026-09-05）
- 出典: https://www.facebook.com/help/instagram/1006568999411025 （取得: 2026-09-05）
- 出典: https://www.facebook.com/help/instagram/1124604297705184 （取得: 2026-09-05）

## 4. Convert は Meta UI only

Personal から Professional は、ふっくーが iPhone の Instagram と Meta ヘルプ UI をタップするだけ。Graph、非公式ログイン、API を切替手段として書かない。

切替の公式ラップ（同じ番号手順）:

- https://www.facebook.com/help/instagram/2358103564437429 （取得: 2026-09-05。本文を読んだ）
- https://www.facebook.com/business/help/502981923235522 （取得: 2026-09-05。同じ手順）

Creator は公式どおり public figures, content producers, artists and influencers 向け。**Creator を選ぶ。Business ではない。** カテゴリは Creator と Business を決めない。

個人アカウントが非公開なら、切替で公開になる。未承認のフォローは自動承認。Professional は非公開にできない。

- 出典: https://www.facebook.com/help/instagram/2358103564437429 （取得: 2026-09-05）
- 出典: https://www.facebook.com/business/help/502981923235522 （取得: 2026-09-05）
- 出典: https://www.facebook.com/business/help/138925576505882 （取得: 2026-09-05）
- 出典: https://www.facebook.com/help/instagram/517073653436611 （取得: 2026-09-05）

### iPhone アプリ（公式番号。2358103564437429 と 502981923235522）

To set up your professional account from the Instagram app:

1. Tap Profile or your profile picture in the bottom right to go to your profile.
2. Tap More to go to your Settings and activity.
3. Below For professionals, tap Account type and tools.
4. Select Switch to professional account.
5. Select your category. You can choose a category that best describes what you do. Note: The category that you choose does not determine whether you'll set up a business or creator account.（HITL: 画面上で最も近いラベル。名前をこちらで指定しない）
6. Tap Switch to professional account.
7. To set up a creator account, choose **Creator**. To set up a business account, choose Business.（HITL: **Creator**）
8. Tap Next.
9. If you're setting up a creator account, complete the optional steps to set up your profile. To skip this step, tap **X** on the top-right corner to return to your profile.

Continue to follow the steps below:

1. Add contact details for your business and tap Next. To skip this step, tap **Don't use my contact info**.
2. To connect to an existing Facebook Page, tap Log in to Facebook. To skip this step, tap **Skip**.
3. To display or hide business information on your profile, go to your profile and tap Edit profile. Go to Profile display below Public business information to choose whether you want to hide or display your category label and contact info. Then tap Done.（HITL: カテゴリラベルと連絡先を隠す）

日本語 UI なら、取得した英語ラベルと同趣旨の項目を押す。無いラベルは発明しない。

- 出典: https://www.facebook.com/help/instagram/2358103564437429 （取得: 2026-09-05）
- 出典: https://www.facebook.com/business/help/502981923235522 （取得: 2026-09-05）

## 5. Page は Skip

公式は Page 接続を business tools のため推奨している。LOCK は今は Skip。接続手順は day-0 では踏まない。つなぐ公式ページはある。今は開いて実行しない。

- 出典: https://www.facebook.com/help/instagram/2358103564437429 （取得: 2026-09-05）
- 出典: https://www.facebook.com/business/help/138925576505882 （取得: 2026-09-05）
- 出典: https://www.facebook.com/business/help/connect-instagram-to-page （取得: 2026-09-05）

個人アカウントへ戻す手順は参照しない。今は使わない。

## 6. 公開前提

professional は非公開にできない。公開前提だけ書く。非公開のままを勧めない。プロフィールの名前、username、画像、bio は、公開と非公開に関係なく誰でも見られると公式が書いている。

- 出典: https://www.facebook.com/help/instagram/2358103564437429 （取得: 2026-09-05）
- 出典: https://www.facebook.com/business/help/138925576505882 （取得: 2026-09-05）
- 出典: https://www.facebook.com/help/instagram/517073653436611 （取得: 2026-09-05）
- 出典: https://www.facebook.com/help/instagram/347751748650214 （取得: 2026-09-05）

## 7. 書き戻し

[account.md](./account.md) に handle、Creator、2FA 方式名（コードではない）、Page skipped、切替は Meta UI、完了日を書く。トークンは書かない。スクショにコードを写さない。

D0 から D1 は [first-7-days.md](./first-7-days.md)。
