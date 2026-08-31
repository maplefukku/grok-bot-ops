# schema（汎用レイヤ。laststitch は instance 1）

Instagram Professional プロフィールのフィールド一覧。OSS-SURVEY 2026-08-31（PdM）。**instagram-skills を wrap しない。** OSS に IG Professional の drop-in SPEC は無かった。フィールド名だけ借りる。値は LOCK。

機械可読は [schema.yaml](./schema.yaml)。切替手順は [meta-taps.md](./meta-taps.md)。貼り付け bio は [bio.md](./bio.md)。

## フィールド（OSS checklist → 汎用）

出典はフィールド名の借用。Meta の手順や制限ではない。

| フィールド | 型 | laststitch（instance 1） |
|---|---|---|
| `account_type` | `creator` \| `business` | `creator` |
| `category` | 画面の最も近いラベル | pending（HITL。ラベルは隠す） |
| `name_field` | 表示名 | `最後の一針 / LAST STITCH LAB`（溢れは `最後の一針`） |
| `username` | handle（@ なし） | `laststitch.lab`（拒否なら `laststitchlab`） |
| `bio` | 文字列 | [bio.md](./bio.md)。**非公式** を含む |
| `links[]` | リスト | `[]`（URL を発明しない） |
| `highlights[]` | リスト | `[]`（HITL 待ち） |
| `pinned` | リスト | `[]`（HITL 待ち） |
| `grid_notes` | 文字列 | 空（HITL 待ち） |
| `pillar` | `Reel` / `carousel` / `story` | pending（D0 では投稿しない） |

- フィールド一覧の借用: https://github.com/sergebulaev/instagram-skills/blob/main/skills/ig-profile-optimizer/SKILL.md （取得: 2026-08-31）。プラグインとしては使わない。
- 表示名のカタカナ 0 と溢れ規則は [name.md](./name.md)。

## bio の 150

OSS checklist も 150 と書いている。**公式 1° でも 150 characters。** 数字を発明していない。FLAG しない。

- 出典: https://www.facebook.com/help/instagram/728994388226960 （取得: 2026-08-31）

OSS checklist は NAME を 30 chars とも書いている。取得した Meta 1° に名前欄の数字は無い。**FLAG。公式上限としては使わない。**

- FLAG 出典（2°。公式ではない）: https://github.com/sergebulaev/instagram-skills/blob/main/skills/ig-profile-optimizer/SKILL.md （取得: 2026-08-31）

## 任意キー（BRAND.md 見出し。wrap しない）

任意: `positioning` / `audience` / `voice` / `visual` / `pillars`。見出しの借用だけ。BRAND.md ファイルは置かない。laststitch はすべて pending。visual の禁止は [visual-lock.md](./visual-lock.md)。

- 見出し出典: https://github.com/caiopizzol/brand.md （MIT、取得: 2026-08-31）
- LICENSE: https://github.com/caiopizzol/brand.md/blob/main/LICENSE （取得: 2026-08-31）
- spec: https://github.com/caiopizzol/brand.md/blob/main/spec/brand-md.md （取得: 2026-08-31）

## 切替と Graph

`account_type: creator` にする手段は Meta UI だけ。Graph が personal を Professional に変えるとは書かない。

- 出典: https://www.facebook.com/help/instagram/2358103564437429 （取得: 2026-08-31）
- 出典: https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-facebook-login/business-login-for-instagram （取得: 2026-08-31）
