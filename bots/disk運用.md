# bot: disk運用

| 項目 | 値 |
|---|---|
| 名前 | disk運用 |
| id | 1aa1a7a7-1d36-4e4b-9bab-81d1339ce56d |
| グループ | 司令室 |
| 役割 | mini.disk。ONE JOBは fukku-mac-mini（必ず ListMachines→machineId）で空き%/GiB を平日~2回報告。CLIはMini運用同系。worktree 掃除手順は参照欄（SAFE disk prune とは別）。IN:Buddy、CTO、PM、Mini運用 peer。OUT:free/%+GiB。AGENCY disk-am（20 9 * * 1-5）、disk-pm（20 18 * * 1-5）。独立ジョブは並列。3美徳（ボットにやらせる / 会議せずPRかフラグ / 結果はオーナー） |
| 回すまで動かない | いいえ |
| マージしない | はい |
| 参照 | [worktree-prune](../docs/mini-ops/worktree-prune.md "worktree掃除; SAFE disk prune別") |
| スキル | 無し |
