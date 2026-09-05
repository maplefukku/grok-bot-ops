# 判断台帳（trend-log）

Planner が 1 日 1 回、候補を ADOPT または REJECT して残す台帳である。正本は [`0002-trend-adopt-loop.md`](./0002-trend-adopt-loop.md)。日常の追記は [`routines/decide-trend-adopt.md`](../../routines/decide-trend-adopt.md) が当日の `ops/daily-YYYY-MM-DD` ブランチへ書く。

保留は WATCH にしない。REJECT とし、理由に「証拠不足」と再浮上条件を書く。

`source_url` は正規化（空白除去、末尾 `/` 削除）して一意。先に書いた行が勝つ。後発は行を足さず、既存行を Planner に知らせる。ボットは行をマージしない。

## 欄の規則

この表は判断行ではない。CI は `## 判断記録` の下で、見出しに `decision`、`source_url`、`理由` を持つ表だけを見る。

| 欄 | 規則 |
|---|---|
| date_jst | JST の日付。CI は形式を見ない |
| source_bot | 最先端手法 または Knowhow収集 |
| title | 候補の短い名 |
| source_url | 1次の http(s) URL。CI が強制する。正規化して一意 |
| decision | ADOPT または REJECT。これ以外は CI が落とす |
| 理由 | 空禁止。保留なら証拠不足と再浮上条件を書く。セル内に縦線は使わない |
| route | skill、ADR、product-impl、ops、none。CI は見ない |
| fired | FIRE 後に JOB、issue、PR の URL を埋める。空でよい |

## 判断記録

次の 2 行は足場の例である。列の形を固定する。日次の候補配信から書いた行ではない。

| date_jst | source_bot | title | source_url | decision | 理由 | route | fired |
|---|---|---|---|---|---|---|---|
| 2026-09-05 | 最先端手法 | 判断の形を CI で強制する | https://github.com/cursor/plugins/blob/main/pstack/skills/principle-encode-lessons-in-structure/SKILL.md | ADOPT | 同じ指示を記憶に書き直していた。decision と理由と source_url を CI の検査にする。 | ops |  |
| 2026-09-05 | Knowhow収集 | 調査用の第4ボットを立てる | https://github.com/maplefukku/grok-bot-ops/issues/19 | REJECT | 調査は最先端手法と Knowhow収集、判断は Planner、発火は PdM と開発リーダー。席は既にある。足す前に席を減らす。 | none |  |
| 2026-09-05 | 最先端手法 | HydraFusion | https://x.com/github/status/2095907113201496216 | ADOPT | GitHub の HydraFusion はタスクごとにモデルとワークフローを組み合わせ、Terminal-Bench 2.1 で品質 +4.9pt・推定コスト -67%。フリートは同じ型を採る。発火したスキルは cloud と conductor-keep-moving である。 | skill |  |
| 2026-09-05 | 最先端手法 | ARC dual-harness Standard vs Provider Adapter | https://x.com/arcprize/status/2095597602545025138 | REJECT | 証拠不足: eval 単位を model+harness にする論点は強いが、今の post/ops ループへの直接ヒットではない。bench ops が先。再浮上: フリートに bench/eval 運用が立ったら ADR のみ再開。agents を model+harness として、visible notes と opaque state/compaction の二条件で採点する。スキルはまだ作らない。 | none |  |
