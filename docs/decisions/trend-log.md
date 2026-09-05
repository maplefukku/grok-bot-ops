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
| 2026-09-05 | 最先端手法 | Hermes /goal overnight repo cleanup | https://x.com/Teknium/status/2095412050751332838 | ADOPT | 長い /goal 一発のほうが細切れ TODO よりリポ掃除に効く。overnight CA に合う。既存 Cloud開発の done-when / domain-unit と重なるが、overnight 掃除専用の形（done-criteria + touch scope + diff cap、micro-step 禁止）はまだスキルに無い。Copilot/Hermes 製品そのものは採用しない。パターンだけ。 | skill |  |
| 2026-09-05 | 最先端手法 | Maestro agent-authored deterministic YAML (Viewer/MCP) | https://maestro.dev/blog/maestro-cli-v2-6-0 | ADOPT | CI は LLM なしで deterministic Maestro。エージェントは YAML 作成と Viewer/デバッグのみ。品質Drive + Monkey (fukku-mac-mini) に直結。ADR: E2E runtime=deterministic Maestro、agent=author+debug only。関連 https://maestro.dev/blog/maestro-cli-2-7-0 | ADR |  |
| 2026-09-05 | 最先端手法 | Maestro 2.9 light/dark dual assert one flow | https://maestro.dev/blog/maestro-cli-2-9-0 | ADOPT | UI 回帰の定量ゲート。1 flow で light/dark。ZuruNote UI 安定と fleet E2E に使える。製品新規は作らない。 | skill |  |
| 2026-09-05 | 最先端手法 | on-device thermal+perf long-session KPI | https://developer.apple.com/documentation/foundation/processinfo/thermalstate | REJECT | 証拠不足: 48h X 1次なし。ProcessInfo.thermalState × FPS × model latency の同一セッション記録は有望だが、今は Apple 公式を指すだけ。再浮上: ZuruNote 実機熱JOBの ADR Phase0 で MetricKit/signpost と並べて採否。カスタム熱プロダクトは作らない。 | none |  |
| 2026-09-05 | 最先端手法 | Maestro assertScreenshot + theme dual gate | https://docs.maestro.dev/reference/commands-available/assertscreenshot | ADOPT | 2.9 light/dark dual assert とセットで視覚回帰の定量ゲート。deterministic Maestro ADR/skill に同梱。新規ハーネスは作らない。 | ADR |  |
| 2026-09-05 | 最先端手法 | Apple Power Profiler on-device power/thermal | https://developer.apple.com/documentation/xcode/measuring-your-app-s-power-use-with-power-profiler | ADOPT | Simulator 不可の公式 on-device 計測。ZuruNote 熱/重モデル JOB の Phase0 はこれを ADOPT し、自前プロファイラを作らない。MetricKit/signpost と併用可。 | ADR |  |
| 2026-09-05 | 最先端手法 | Warp scorers (Software Factory evals) | https://www.warp.dev/articles/evals-and-scorers-software-factory | REJECT | 証拠不足: fleet eval/bench ops が先。再浮上: ARC dual-harness 再浮上と同じ窓で ADR。 | none |  |
| 2026-09-05 | 最先端手法 | F2PF harness | https://arxiv.org/abs/2608.26218 | REJECT | 学術ハーネス。Maestro 定量ゲートが先。再浮上: Maestro 後に eval SoT が足りないときだけ。 | none |  |
| 2026-09-05 | 最先端手法 | Astra long-running loop mid-verify + independent verifier | https://x.com/github/status/2095971389190885815 | ADOPT | 長時間 CA / overnight /goal に mid-run 検証と完了前の独立 verifier を移植できる。HydraFusion Critique（終端の別ファミリー批判）と Hermes overnight one-shot を補う。Copilot Astra 製品は採用しない。スキル文が先、実装は後。 | skill |  |
