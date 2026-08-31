# bot: CI運用

| 項目 | 値 |
|---|---|
| 名前 | CI運用 |
| id | 8630d289-b46b-43ab-9731-2d2b4145a209 |
| グループ | 司令室 |
| 役割 | ci.ops。対象は ZuruNote / sauna-master / gakuse-ai。担当は GitHub Actions と Ubicloud とセルフホスト runner の健全性。Swift の主は Xcode Cloud の Build-only（ZuruNote と sauna-master）。月次時間がほぼ0のときだけ Mac mini に切り替える。XC と Mac の Swift 二重実行はしない。ZuruNote の Linux は共有 Grok Bot Linux の zurunote-linux-1/2、溢れは Ubicloud。gakuse-ai の Linux は lima gakuse-ci / gakuse-ci-2（不要なら Stopped のまま、消さない）。bare の runs-on:self-hosted は使わない。同一 SHA の二重バックエンドはしない。独立ジョブは並列（直列待ちしない）。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） |
| 回すまで動かない | はい |
| マージしない | はい |
| 参照 | 無し |
