# product: ZuruNote

| 項目 | 値 |
|---|---|
| リポジトリ | https://github.com/maplefukku/ZuruNote |
| デフォルトブランチ | main |
| 検証スキル | `.cursor/skills/verify-zurunote/`（2026-08-30） |
| feature map | `.cursor/skills/verify-zurunote/features/` |
| maintain routine | 検証メンテ・平日1回 |
| automation パック | 無し |
| intake の対象 | 無し |
| 最終確認日 | 未 |
| 最終 outcome | 未 |
| 最終 PR | 無し |

`最終確認日` / `最終 outcome` / `最終 PR` は [`routines/maintain-verification.md`](../routines/maintain-verification.md) が毎日書き戻す。bootstrap 直後は `未` / `未` / `無し` のまま。outcome は `clean` / `changed` / `blocked` のどれか。

## メモ

- クライアントは SwiftUI iOS のみ (`apps/ios-swift`)
- 起動に Xcode と iOS シミュレータが要る
- 録音は端末。講義音声はサーバに置かない
- Linux では決定的なサーバと HTTP だけを駆動できる。Maestro と XCUITest には macOS が要る。対象は Simulator か実機
- Docker が無い VM は apt の PostgreSQL 16 で足りる。スキル PR で確認済み
- 開発用 DB とテスト用 DB はどちらもホストの 5433 を使うので同時には動かない
- 検証スキル PR: https://github.com/maplefukku/ZuruNote/pull/221
