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
| 2026-09-05 | 最先端手法 | HydraFusion | https://x.com/github/status/2095907113201496216 | ADOPT | GitHub の HydraFusion はタスクごとにモデルとワークフローを組み合わせ、Terminal-Bench 2.1 で品質 +4.9pt・推定コスト -67%。フリートは同じ型を採る。発火したスキルは cloud と conductor-keep-moving である。 | skill | cloud+conductor-keep-moving HydraFusion; https://github.com/maplefukku/grok-bot-ops/issues/19#issuecomment-5547685067 |
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
| 2026-09-07 | Knowhow収集 | Haggle anti-job — spend/sign/send never without explicit go | https://x.ai/bot/marketplace/bots/haggle-bot | ADOPT | 公式 Marketplace の Haggle は anti-job を明示: spend / sign / send（外部メール・Slack・DM含む）は都度の explicit go なしで禁止。fleet の purchases / send-on-behalf / Auto-review と同型。Haggle 製品ボットを CreateAgent しない。既存スキルに anti-job 条項を寄せる。 | skill | anti-job Domain WRAP LIVE docs/process/anti-job.md; purchases/send-on-behalf/Auto-review clause; https://github.com/maplefukku/grok-bot-ops/issues/90; https://github.com/maplefukku/grok-bot-ops/pull/105; CreateAgent NONE |
| 2026-09-07 | Knowhow収集 | Shared one computer — owner seat + specialist only when stuck | https://x.com/madogiwacowork/status/2096721289599922688 | ADOPT | 席を増やす前に減らす LOCK と一致。共有1マシン上で owner 席が持ち、詰まったときだけ specialist、成果物を handoff。新規席や並列マシンを発明しない。CreateAgent / schedules-force-agency チェックに書く。 | ops | docs/process/shared-computer.md WRAP LIVE; CBO CreateAgent + schedules-force-agency checklist; https://github.com/maplefukku/grok-bot-ops/issues/91; CreateAgent NONE |
| 2026-09-07 | Knowhow収集 | Official Bot Marketplace templates (~69) + Haggle procurement | https://x.ai/news/grok-bot-procurement | ADOPT | 公式 Marketplace（約69）と調達記事は template/share の一次。CreateAgent 前に Marketplace を見て KEEP/WRAP。export-bot-template は残す。並列の自前公開経路は作らない。Haggle 調達ボット自体の量産はしない。 | ops |  |
| 2026-09-08 | Knowhow収集 | HARD — never write product code on Grok Bot computer; always Cloud Agent for repos | https://x.com/nikvassev/status/2096629495591502187 | ADOPT | 週次の bot-computer 枠はコードで燃えやすい。fleet は既に code-changes / cloud / tool-path-prefer でリポ作業=Cloud Agent。箱にプロダクトコードを書かない HARD を全席へ再ロックする。新規席は作らない。 | ops |  |
| 2026-09-08 | Knowhow収集 | Monitor / surface Cursor Cloud Agent spend and usage limits | https://x.com/NHv2Pro/status/2096948213282643975 | ADOPT | CA 上限がメール通知だけでアプリ内が不明瞭、想定外の高額報告もある。thrift と Cursor運用で spend/limit を先に見える化する。新ダッシュボード製品は作らない。既存 cursor skill / Cursor運用に寄せる。 | ops | Cursor運用 WRAP LIVE Usage+Spending only; JOB Cursor運用 read-lane; no invent monitors; thrift Fable Medium; on-demand OFF |
| 2026-09-08 | Knowhow収集 | CA-exhausted fallback path (Claude Code / Devin on bot machine or Mac mini) | https://x.com/jawestenberg/status/2096738605104521264 | ADOPT | CA 枠が尽きたときの代替コーディング経路。tool-path-prefer の既存順（scripts→OSS→CA→Mini Codex→GUI）に寄せ、Mac mini の Mini Codex を WRAP。Devin や Claude Code 製品席の CreateAgent はしない。パターンだけ。 | ops |  |
| 2026-09-08 | Knowhow収集 | Official Figma photomosaic template for design/SNS assets | https://x.com/mattyp/status/2097083263361958087 | REJECT | 証拠不足: SpaceXAI の Figma photomosaic 一次は有用だが、いまの P0 GTM に mosaic SNS 案件が無い。再浮上: CMO または デザイン考案が mosaic 投稿 JOB を切ったとき。テンプレ製品ボットは作らない。 | none |  |
| 2026-09-08 | 最先端手法 | Deploy Hatch / Hatchable OAuth+health CA deploy boundary | https://hatchable.com/howto/deploy-from-cursor | REJECT | 証拠不足: early product。OAuth+health gate / no host keys は CA deploy 境界として興味はあるが、fleet 自社即採用の証拠が足りない。PdM も即採用 REJECT。skill HOLD。再浮上: Cursor運用または CTO が CA deploy 境界 JOB を切り、本番ホスト鍵なし gate の受け入れ条件が書けたとき。CreateAgent しない。 | none |  |
| 2026-09-09 | Knowhow収集 | Chat内パスワードマネージャ／フォーム入力 | https://x.com/bot/status/2097383980748382239 | ADOPT | 公式は secret-request を汎用パスワードマネージャではないとし、ログインは request_box_help で人間が入力。fleet の purchases / send-on-behalf / Auto-review と同型。既存 handoff を WRAP し、チャットへ秘密を貼る経路は作らない。CreateAgent しない。 | ops |  |
| 2026-09-09 | Knowhow収集 | 例外監視→webhook→Bot fixer | https://x.com/claytonlz/status/2097381463847297443 | REJECT | 証拠不足: 自動 Bot fixer は Phase0 Guardian proposal-only と Haggle anti-job に反する。webhook→監視/PdM の通知は既存 routine 型で足りる。再浮上: proposal-only webhook digest が LIVE かつ fixer に都度 explicit go の受け入れ条件が書けたとき。自動修復席は作らない。 | none |  |
| 2026-09-09 | Knowhow収集 | OpenAI Astra フル展開（Codex + ChatGPT Work, Plus〜Enterprise） | https://x.com/OpenAI/status/2097431322117476423 | ADOPT | OpenAI 公式の Astra/Codex+Work 展開は既存 ChatGPT Astra Pro / Mini Codex 席の可用性・役割分担の判断材料。CBO 台帳と HARD TAB を WRAP。GitHub Astra mid-verify 行とは別 URL。新規席は作らない。 | ops |  |
| 2026-09-09 | Knowhow収集 | Grok Bot コーディング token 設定ガイド | https://x.com/skunky/status/2097424315771994523 | ADOPT | thrift / CA・Bot コスト制御の実践ガイド。既存 thrift HARD と Cursor運用 Usage+Spending WRAP に寄せる。新ダッシュボードや token 製品は作らない。設定見直しは ops。 | ops |  |
| 2026-09-09 | 最先端手法 | Claude Tag CI/CD first-responder — SITREP + lessons.md | https://x.com/ClaudeDevs/status/2097437571634639035 | ADOPT | 既存 ci-health-sweep は read-only 健康表まで。SITREP と lessons.md 追記の一次対応型は欠けている。fleet-stall-sweep / overnight-goal-cleanup は webhook→fixer auto-exec を HOLD REJECT 済み。Guardian proposal-only KEEP。ADOPT は WRAP: ci-health-sweep の下流に SITREP+lessons を厚くする（新ハーネス・自動修復席は作らない）。bake は スキル作成。CreateAgent NONE。 | skill | ci-health-sweep amend-in-place LIVE SITREP+lessons+escalate; sand-workflow:ci-health-sweep; CreateAgent NONE |
| 2026-09-09 | 最先端手法 | prompt-cache / session cost-optimize loop (Claude Tag cost) | https://x.com/ClaudeDevs/status/2097369738968195513 | ADOPT | cursor skill に Usage+Spending と thrift effort はあるが、セッション後の cache-miss/effort 較正ループは無い。Claude API 専用 cost-optimize ツールは invent しない。薄 WRAP: cursor skill に post-session audit を厚くする。新 skill 名 prompt-cache-cost-audit ハーネスは作らない。bake=スキル作成。ops=Cursor運用。CreateAgent NONE。Claude Tag SITREP 行とは別。 | skill | cursor post-session cost/effort audit LIVE; sand-workflow:cursor; invent=N; ops=Cursor運用; CreateAgent NONE |
| 2026-09-09 | 最先端手法 | Copilot harness cost — task-completion cost not per-tool shorten | https://x.com/github/status/2097388268237045883 | ADOPT | tool-path-prefer は経路順のみで原価メトリクスが無い。薄 WRAP: task-completion cost を SoT にし、per-tool token 短縮を既定にしない。背景完了通知は結果インライン。skill/prompt 短縮は behavior regression 必須。新 harness-cost skill/ADR は invent しない。bake=スキル作成。CreateAgent NONE。 | skill | tool-path-prefer harness cost WRAP LIVE; sand-workflow:tool-path-prefer; invent=N; CreateAgent NONE |
