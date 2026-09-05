# Mini のローカル worktree を掃除する

マージ後や CA の引き渡し後に、fukku-mac-mini 上のチェックアウトへ残った added worktree を分類して消す。対象のチェックアウトは ZuruNote、sauna-master、gakuse-ai である。GitHub Actions の cache は触らない。リモートブランチは消さない。

この手順は [issue 28](https://github.com/maplefukku/grok-bot-ops/issues/28) に対応する常設ツールである。ディスクを一度空けた Mini CLI の SAFE prune とは別物なので、そちらの記録はここに置かない。

## いつ実行するか

次のあとで、主チェックアウトを指定して実行する。

- Mini運用でマージが終わったとき
- CA を fukku-mac-mini のチェックアウトへ引き渡したあと
- ローカルの added worktree が増えてディスクを圧迫しているとき

主チェックアウトは消さない。スクリプトは primary を REMOVE にしない。

## まず dry-run する

grok-bot-ops を clone したマシンで実行する。`--repo` には掃除する対象の主チェックアウトを渡す。

```sh
python3 /path/to/grok-bot-ops/scripts/local_worktree_prune.py --repo /path/to/checkout
```

既定は dry-run である。各 worktree の KEEP または REMOVE と理由が出る。何も消えない。

primary の行は必ず KEEP である。REMOVE と出た行だけが `--apply` の候補になる。

JOB を渡すときは `--jobs` に JSON を付ける。省略すると主チェックアウトの `.worktree-prune-jobs.json` を読む。ファイルが無ければ、JOB はどのパスも指していない。`state` は `live`、`keep`、`abandoned` のいずれかである。

```json
{
  "jobs": [
    {
      "name": "follow-up",
      "path": "/path/to/added-worktree",
      "state": "live",
      "force": false
    }
  ]
}
```

残したい木の中に `.worktree-prune-keep` を置くと、その木は locked として残る。

## 一覧を見てから --apply する

dry-run の REMOVE が、マージ済みでプロセスも JOB も汚れた作業も無い added worktree だけであることを確認する。確認できたら同じ `--repo` で `--apply` を付ける。

```sh
python3 /path/to/grok-bot-ops/scripts/local_worktree_prune.py --repo /path/to/checkout --apply
```

スクリプトは許可した木にだけ `git worktree remove` を実行する。成功したあと `git worktree prune` で古いメタデータを捨てる。`--force` は JOB が force を true にした行にだけ付く。判定そのものは force では変わらない。

## 残す条件

次のいずれかが一つでも成り立つ木は残す。

- 開いている PR、または進行中の CI がある
- そのパスを使うプロセスがある
- 未コミット、またはリモートに無いコミットがある
- 未マージのブランチで、JOB がそのパスを live と書いている
- `.worktree-prune-keep` がある、JOB が keep と書いている、または git が locked にしている
- 主チェックアウトである

消してよいのは added worktree だけである。さらに PR が merged か、JOB が abandoned で残り作業が無いこと。プロセスが無く、未コミットも無く、JOB が live と書いておらず、locked でもないこと。squash マージ済みの PR では、その木にだけ残るコミットは失われる作業とはみなさない。PR が merged でなければ、リモートに無いコミットは残す。

信号が取れないときは残す。`gh` が無い、または PR 照会が失敗したら、開いている PR があるとみなして残す。プロセス走査が失敗したら、その木は使用中とみなして残す。

## やってはいけないこと

- 主チェックアウトを `git worktree remove` しない
- `git branch -d` や `git push --delete` でブランチを消さない
- GitHub Actions の cache をこのスクリプトで掃除しない
- dry-run の一覧を見ずに `--apply` しない
- JOB が force を書いていない木へ `--force` を付けない
- 実機の fukku-mac-mini を、確認の取れていない CA から直接 prune しない
