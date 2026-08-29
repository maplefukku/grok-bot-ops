# product: <名前>

| 項目 | 値 |
|---|---|
| リポジトリ | <owner/repo の URL> |
| デフォルトブランチ | main |
| 検証スキル | 無し / `.cursor/skills/verify-<app>/`（立てた日付） |
| feature map | `.cursor/skills/verify-<app>/features/` |
| maintain routine | 未設定 / <担当ボット名>・1 日 1 回 |
| automation パック | 無し / benny（`.cursor/automations/benny/`） |
| intake の対象 | <Slack チャンネル、X キーワードなど。無ければ「無し」> |
| 最終確認日 | 未 |
| 最終 outcome | 未 |
| 最終 PR | 無し |

`最終確認日` / `最終 outcome` / `最終 PR` は [`routines/maintain-verification.md`](../routines/maintain-verification.md) が毎日書き戻す。bootstrap 直後は `未` / `未` / `無し` のまま。outcome は `clean` / `changed` / `blocked` のどれか。

## メモ

<起動の癖、環境の注意、2 インスタンス並走の可否など、
cloud agent に伝えると事故が減ることだけ書く>
