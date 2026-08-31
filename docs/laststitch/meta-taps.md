# HITL タップ（iPhone Instagram アプリ）

実行者は **ふっくー**。主経路は iPhone の Instagram アプリ。Linux は docs / CI / draft PR だけ。Instagram に触れない。ボットはログインしない。作成しない。投稿しない。DM しない。コードを受け取らない。

関連: [README.md](./README.md) · [name.md](./name.md) · [bio.md](./bio.md) · [account.md](./account.md) · [first-7-days.md](./first-7-days.md) · [schema.md](./schema.md)

## 順序（LOCK）

1. ふっくーがメール / 電話を用意する。iPhone の Instagram アプリ。
2. 新規作成。iPhone 公式アコーディオン（Accordion 1。Facebook なし）に従う。タップを足さない。
3. username `@laststitch.lab`。拒否なら `@laststitchlab`。
4. 名前と [bio.md](./bio.md)。
5. 2FA Authentication app（有効化は Instagram アプリのみ）。バックアップコードはふっくーだけ。
6. professional へ切替 → Creator。Page は Skip。Don't use my contact info。カテゴリラベルは隠す。
7. professional は非公開にできない。公開前提だけ書く。非公開のままを勧めない。
8. 確定値を [account.md](./account.md) に書く。スクショにコードを写さない。

Hub: Signing Up and Getting Started。

- 出典: https://help.instagram.com/3257948324491837 （取得: 2026-08-31）
- 出典: https://www.facebook.com/help/instagram/3257948324491837 （取得: 2026-08-31）

## 1. 新規作成（iPhone アコーディオン。タップを足さない）

一次は iPhone タブの公式ページ。2026-08-31 にアコーディオン本文を取得した。**ここに無いタップを足さない。**

- 出典: https://help.instagram.com/155940534568753/?cms_platform=iphone-app&helpref=platform_switcher （取得: 2026-08-31）
- Title: Create a new Instagram profile | Instagram Help Center

Notice（同ページ）:

- Meta Accounts / Accounts Center の文言が出ることがある。
- Must be at least 13.
- 作り方は 2 つ: アプリまたは instagram.com。既存の Facebook / Instagram からも、同じ Accounts Center に新しい IG を作れる。
- 最近作ったアカウントは new と出ることがある。
- login info の保存は任意。HITL の手元だけ。ボットは保存しない。

HITL は **Accordion 1**（new to Instagram, **NO Facebook account**）。Accordion 2（Facebook から作る）は公式の別経路として存在するが、勧めない。LOCK はオリジナル・コントロール + Page Skip。

### Accordion 1（iPhone。verbatim）

1. Download the Instagram app from the App Store (iPhone) or Google Play Store (Android).
2. Once the app is installed, tap Instagram logo to open it.
3. Tap Create New Account and enter your email address or mobile number, then tap Next. Note: If you sign up with email, make sure you enter your email address correctly and choose an email address that only you can access. If you log out and forget your password, you'll need to be able to access your email to get back into your Instagram account.
4. Enter the confirmation code sent to your email address or mobile number, then tap Next.
5. Create a password, then tap Next.
6. Enter your birthday, then tap Next. Note: Use your own birthday, even if this account is for a business, a pet or something else.
7. Add your name, then tap Next.（LOCK 名前: `最後の一針 / LAST STITCH LAB`。カタカナ 0。溢れ規則は [name.md](./name.md)）
8. Create a username, then tap Next.（LOCK: `@laststitch.lab`。拒否なら `@laststitchlab`）
9. Read Instagram’s terms and policies, then tap I agree, if you agree to the terms, to create your account.
10. Add a profile picture, then tap Next. If you’d like to add a profile picture later, tap Skip.（[visual-lock.md](./visual-lock.md) を受理してから載せる。D0 は Skip でよい）
11. If you want to share your profile picture as your first post, tap Toggle, then tap Done.（LOCK: プロフィール画像を初投稿にしない。toggle はオフのまま / 初投稿として共有しない。[first-7-days.md](./first-7-days.md)）

確認コード・パスワード・誕生日・メール・電話はふっくーだけ。ボットは受け取らない。bio の貼り付けは作成後（次節と [bio.md](./bio.md)）。

## 2. 名前・username・bio（作成後）

表示名と handle は [name.md](./name.md)。bio は [bio.md](./bio.md)。

公式「How to change your Instagram profile information」:

Update your profile on Instagram:

1. プロフィールへ行く
2. Edit profile
3. 情報を入力して Submit

Accounts Centre 経由:

1. More → Settings
2. Accounts Centre → Profiles
3. 対象プロフィール
4. name / username / profile picture を更新
5. Done

公式「Add a bio」:

1. プロフィールへ行く
2. Edit profile → Bio のテキストボックス
3. bio を書く
4. Submit

iPhone のラベルが違うときは、同じ公式ページの iPhone アコーディオンに従う。文字数の数字は、bio の 150 characters 以外は取得ページに無い。

- 出典: https://www.facebook.com/help/instagram/583107688369069 （取得: 2026-08-31）
- 出典: https://www.facebook.com/help/instagram/728994388226960 （取得: 2026-08-31）
- 出典: https://www.facebook.com/help/instagram/110121795815331 （取得: 2026-08-31）

ウェブサイトは公式に mobile で追加できるとある。今は置かない。URL を発明しない。コンピュータ向け本文は「This feature isn't available on computers」まで。端末別タップは未抽出。

- 出典: https://www.facebook.com/help/instagram/362497417173378 （取得: 2026-08-31）
- 出典: https://help.instagram.com/362497417173378/ （取得: 2026-08-31）

## 3. 2FA（Authentication app）

LOCK は Authentication app。SMS / WhatsApp は選ばない。

公式注記（そのまま）: 「Two-factor authentication through an authentication app can only be turned on using the Instagram app for Android and iPhone.」

Linux ではオンにしない。ボットに確認コードを送らない。

推奨例として公式が挙げるアプリ: Duo Mobile または Google Authenticator。

公式「Use an authentication app…」の手順（取得本文は Click 表記。有効化は iPhone アプリ）:

1. Accounts Centre → Password and security
2. Two-factor authentication → 対象アカウント
3. Authentication app → Next
4. 認証アプリの confirmation code を入力

バックアップコード: ふっくーだけが持つ。公式は clipboard / スクショ / 別保存を書いている。リポジトリとボットには貼らない。[account.md](./account.md) のスクショにコードを写さない。

追加デバイスは day-0 必須ではない。

- 出典: https://www.facebook.com/help/instagram/566810106808145 （取得: 2026-08-31）
- 出典: https://www.facebook.com/help/566810106808145 （取得: 2026-08-31）
- 出典: https://www.facebook.com/help/instagram/1582474155197965 （取得: 2026-08-31）
- 出典: https://www.facebook.com/help/1582474155197965/ （取得: 2026-08-31）
- 出典: https://www.facebook.com/help/instagram/1006568999411025 （取得: 2026-08-31）
- 出典: https://www.facebook.com/help/instagram/1124604297705184 （取得: 2026-08-31）
- 出典: https://www.facebook.com/help/1124604297705184/ （取得: 2026-08-31）

## 4. Convert = Meta UI only（Graph では切替しない）

Personal → Professional は **ふっくーが iPhone の Instagram / Meta ヘルプ UI をタップするだけ**。Graph、非公式ログイン、API を切替手段として書かない。Facebook Login for Business も切替手段ではない。

切替の公式ラップ（同じ番号手順）:

- https://www.facebook.com/help/instagram/2358103564437429 （取得: 2026-08-31。iPhone アコーディオン本文を読んだ）
- https://www.facebook.com/business/help/502981923235522 （取得: 2026-08-31。同じ手順）

Creator は公式どおり public figures, content producers, artists and influencers 向け。**Creator を選ぶ。Business ではない。** カテゴリは Creator / Business を決めない。

個人アカウントが非公開なら、切替で公開になる。未承認のフォローは自動承認。Professional は非公開にできない。

- 出典: https://www.facebook.com/help/instagram/2358103564437429 （取得: 2026-08-31）
- 出典: https://www.facebook.com/business/help/138925576505882 （取得: 2026-08-31）
- 出典: https://www.facebook.com/help/instagram/517073653436611 （取得: 2026-08-31）

### iPhone アプリ（公式番号。2358103564437429）

To set up your professional account from the Instagram app:

1. Tap Profile or your profile picture in the bottom right to go to your profile.
2. Tap More to go to your Settings and activity.
3. Below For professionals, tap Account type and tools.
4. Select Switch to professional account.
5. Select your category. You can choose a category that best describes what you do. Note: The category that you choose does not determine whether you'll set up a business or creator account.（HITL: **画面上で最も近いラベル**。名前をこちらで指定しない）
6. Tap Switch to professional account.
7. To set up a creator account, choose **Creator**. To set up a business account, choose Business.（HITL: **Creator**）
8. Tap Next.
9. If you're setting up a creator account, complete the optional steps to set up your profile. To skip this step, tap **X** on the top-right corner to return to your profile.

Continue to follow the steps below:

1. Add contact details for your business and tap Next. To skip this step, tap **Don't use my contact info**.
2. To connect to an existing Facebook Page, tap Log in to Facebook. … To skip this step, tap **Skip**.
3. To display or hide business information on your profile, go to your profile and tap Edit profile. Go to Profile display below Public business information to choose whether you want to hide or display your category label and contact info. Then tap Done.（HITL: カテゴリラベルと連絡先を隠す）

日本語 UI なら、取得した英語ラベルと同趣旨の項目を押す。無いラベルは発明しない。

- 出典: https://www.facebook.com/help/instagram/2358103564437429 （取得: 2026-08-31）
- 出典: https://www.facebook.com/business/help/502981923235522 （取得: 2026-08-31）

## 5. Page は Skip

公式は Page 接続を business tools のため推奨している。LOCK は **今は Skip**。後の Instagram Login 経路は Page 不要。接続手順は day-0 では踏まない。

- 出典: https://www.facebook.com/help/instagram/2358103564437429 （取得: 2026-08-31）
- 出典: https://www.facebook.com/business/help/138925576505882 （取得: 2026-08-31）
- 出典: https://www.facebook.com/business/help/connect-instagram-to-page （取得: 2026-08-31）
- 出典: https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-instagram-login （取得: 2026-08-31）

個人アカウントへ戻す手順は参照のみ。今は使わない。

- 出典: https://www.facebook.com/business/help/1717693135113805 （取得: 2026-08-31）

## 5b. Graph は切替ではない（あとで。実装しない）

Facebook Login 経路は、公式どおり **すでに** Professional へ切替え、Facebook Page を作り、Page を繋いだあとで API に出す流れ。`extras {"setup":{"channel":"IG_API_ONBOARDING"}}` はその convert + Page + link の窓を **ホストするだけ**。ユーザーが切替と Page と接続を行う。LOCK は Page なしなので、この経路は使わない。Graph が personal を Professional に変えるとは書かない。

- 出典: https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-facebook-login/business-login-for-instagram （取得: 2026-08-31）

あとで使う経路（Professional の Creator が存在してから。D0 ではない。この PR では実装しない）:

1. Meta UI だけで Creator 切替（上の節）
2. Facebook Page なし（Instagram Login 経路）
3. あとで Business-type Meta app + Instagram product
4. あとで Instagram Login → `graph.instagram.com`
5. あとで short（code は 1 hour）→ long（`expires_in` 秒。約 60 days）。トークンはこの docs に書かない
6. publish はあと。D0–D1 はプロフィールだけ。初投稿は HITL iPhone。publish-bot なし

公式: Instagram API with Instagram Login は Facebook Page のリンクを必要としない。Professional = business or creator。host は `graph.instagram.com`。token 交換は `api.instagram.com/oauth/access_token` のあと `graph.instagram.com/access_token`。scopes 例: `instagram_business_basic` ほか。GA 2024-07-23、この setup では Page 不要。

- 出典: https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-instagram-login （取得: 2026-08-31）
- 出典: https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-instagram-login/business-login （取得: 2026-08-31）
- 出典: https://developers.facebook.com/blog/post/2024/07/30/instagram-api-with-instagram-login/ （取得: 2026-08-31）

PATH の一覧は [README.md](./README.md)。SDK ファイルはこのリポに置かない。

## 6. 公開前提

professional は非公開にできない。公開前提だけ書く。非公開のままを勧めない。プロフィールの名前・username・画像・bio は、公開/非公開に関係なく誰でも見られると公式が書いている。

- 出典: https://www.facebook.com/help/instagram/2358103564437429 （取得: 2026-08-31）
- 出典: https://www.facebook.com/business/help/138925576505882 （取得: 2026-08-31）
- 出典: https://www.facebook.com/help/instagram/517073653436611 （取得: 2026-08-31）
- 出典: https://www.facebook.com/help/instagram/347751748650214 （取得: 2026-08-31）

## 7. 書き戻し

[account.md](./account.md): handle、Creator、2FA 方式名（コードではない）、Page skipped、切替は Meta UI、トークンなし、完了日。スクショにコードを写さない。

D0–D1 は [first-7-days.md](./first-7-days.md)。
