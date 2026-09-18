# fleet

フリート停滞、merge GATE、jenny-lite の ADOPT と REJECT の置き場。
対象窓は fleet stalls 2026-09-01..09-05（sauna#203 loop、ZN Swift cluster）、fleet stalls 平日 2026-09-15..09-18（factory BROKEN loop、idle-with-leftover eng、agency silent-miss、research/X weekday miss）、および jenny-lite 2026-09-07..09-11、jenny-lite 2026-09-12..09-18（#127 merge bottleneck / daily SoftACC）。出典は各エントリの URL。

## ADOPT A — factory BROKEN until trusted fire proves LIVE (jenny-lite 2026-09-15..09-18)

- 内容: factory は provenance=untrusted、または lastRun が >1d stale、または due slot miss のいずれかで BROKEN。LIVE 扱いは trusted fire が lastRun を更新するまで禁止。same-sweep で JOB は ルーチン作成（rearm trust）+ 工場長（catch-up は Discord seat ONLY）。`enabled=true` だけでは LIVE にしない。trusted lastRun 無しに content catch-up で fixed 扱いしない。eng-only sweep で factory を落とさない。encode 先は sand-workflow:fleet-stall-sweep / sand-workflow:author-routines / sand-workflow:schedules-force-agency knowhow（スキル本文パッチは Planner WRAP → スキル作成、本 PR では invent しない）。
- 決定: ADOPT
- 出典: https://github.com/maplefukku/grok-bot-ops/issues/16 · [`bots/監視.md`](../../bots/監視.md) · [`bots/工場長.md`](../../bots/工場長.md) · [`bots/ルーチン作成.md`](../../bots/ルーチン作成.md) （protocol 2026-09-18; factory BROKEN loop 09-15..09-18）
- 確認: 未

## ADOPT B — JOB-flat: idle-with-leftover ≥3 same-day sweeps → escalate once (jenny-lite 2026-09-15..09-18)

- 内容: 同一 idle-with-leftover JOB が同日 sweep で ≥3 回繰り返し、seat-class 昇格（Buddy/CTO / sand-workflow:conductor-keep-moving）が無いなら 1 回だけ escalate。infinite re-spam JOB は REJECT。weekday-pulse-cascade / conductor-keep-moving knowhow へ bake（スキル本文は Planner WRAP 後）。
- 決定: ADOPT
- 出典: https://github.com/maplefukku/grok-bot-ops/issues/16 （2026-09-11 idle-with-leftover 文脈; 09-15..09-18 eng thr/CA-only 再発） · [`bots/開発リーダー.md`](../../bots/開発リーダー.md) （protocol 2026-09-18）
- 確認: 未

## ADOPT C — agency silent-miss: enabled=true ∧ lastRun past schedule window (jenny-lite 2026-09-15..09-18)

- 内容: enabled=true かつ lastRun が schedule window より古い = SILENT-MISS FAIL。same-sweep JOB は owner seat + ルーチン作成。linux-runner-offline-ping、keep-moving-*、tips-3x、factory に適用。filesystem の runs.json を disable SoT にしない（REJECT）。encode 先は sand-workflow:schedules-force-agency。
- 決定: ADOPT
- 出典: [`docs/process/shared-computer.md`](../process/shared-computer.md) · [`bots/CBO.md`](../../bots/CBO.md) · https://github.com/maplefukku/grok-bot-ops/issues/91 （protocol 2026-09-18; agency silent-miss 09-15..09-18）
- 確認: 未

## ADOPT D — not-eng-only fleet-sweep / ca-merge-liveness checklist (jenny-lite 2026-09-15..09-18)

- 内容: 毎回の fleet-sweep と ca-merge-liveness は factory+Discord、research/X 平日 pulse、untrusted provenance をスコアに含める必須 checklist。eng thr/CA のみに sweep を落とすのは FAIL。既存 LIVE thr check（09-06）と Sep11 ADOPT 行（*-HOLD / ACK-then-stop / overnight babysit）の再掲はしない — 本行は 09-15..09-18 の eng-only 縮退 miss 用 DELTA。
- 決定: ADOPT
- 出典: [`bots/監視.md`](../../bots/監視.md) · [`bots/GrokBot特化リサーチ.md`](../../bots/GrokBot特化リサーチ.md) · https://github.com/maplefukku/grok-bot-ops/issues/16 （protocol 2026-09-18; research/X weekday miss 09-15..09-18）
- 確認: 未

## REJECT — jenny-lite stall fire companion 2026-09-15..09-18 (modes A–D)

- 内容: CreateAgent / 新 Jenny seat / credit-audit や fixer bot の invent。auto-merge と webhook-fixer auto-exec。監視からの Discord drip、非工場長が discord.com を開く、Forks wipe、cookie-seed。eng-only stall sweep。trusted lastRun 無しの content catch-up で factory fixed 扱い。監視または impl CA が knowhow を書く（Knowhow収集が write を持つ）。Soft Flag invent しない。
- 決定: REJECT
- 出典: https://github.com/maplefukku/grok-bot-ops/issues/16 · [`docs/decisions/trend-log.md`](../decisions/trend-log.md) （2026-09-09 webhook→fixer auto-exec HOLD REJECT） · [`bots/監視.md`](../../bots/監視.md) · [`bots/Knowhow収集.md`](../../bots/Knowhow収集.md) （protocol 2026-09-18）
- 確認: 未

## ADOPT — #127 Flag Y ONLY writeback landed in process + ci lock (jenny-lite 2026-09-12..09-18)

- 内容: tip-sot behind0 は #128 で [`pr-body.md`](../process/pr-body.md) の PdM Flag Y ONLY 表（behind0/thr0/FULL CLEAN/APPROVED/ADV SUCCESS）に WRAP 済み。述語 pin は `test_flag_y_only_lock.py` → `ci.py` `flag-y-only-lock`。scanner・第二 Flag 定義は invent しない。HOLD merge=PM。GATE 観測（09-07..09-11）の behind 半分の writeback はここで close。
- 決定: ADOPT
- 出典: https://github.com/maplefukku/grok-bot-ops/pull/128 · https://github.com/maplefukku/grok-bot-ops/issues/127 （2026-09-14）
- 確認: 未

## ADOPT — daily knowhow: @bot / x.ai / docs official-only before stall-adjacent land (jenny-lite 2026-09-12..09-18)

- 内容: merge-leftover daily lane は knowhow 追記前に公式-only gate を通す。@grok LLM 返信・community recap・Grok Build-only 記事を stall 対策として載せない。SoftACC thr-close で差し戻した行と同型。jenny-lite の ADOPT|REJECT は [`collect-grokbot-knowhow.md`](../../routines/collect-grokbot-knowhow.md) の Planner 候補と分離し、fleet には PM ACK 分だけ DELTA する。
- 決定: ADOPT
- 出典: https://github.com/maplefukku/grok-bot-ops/pull/134 · https://github.com/maplefukku/grok-bot-ops/issues/127 （2026-09-17..09-18）
- 確認: 未

## REJECT — Grok Bot Voice / Team Bots WIP / new seat as repeated-stall unstick (jenny-lite 2026-09-12..09-18)

- 内容: #127 leftover の答えは既存 knowhow+skills+Flag Y ONLY+Closer thr-close。Voice rollout や Team Bots 実験を CreateAgent・Jenny seat・監視 monkey で埋めない。GTM connector / Grok Voice marketplace を製品 STT/TTS stall  fix に載せない（trend-log REJECT 済みと同型）。Soft Flag invent しない。
- 決定: REJECT
- 出典: https://github.com/maplefukku/grok-bot-ops/issues/127 · https://x.com/bot/status/2100659463569170779 （2026-09-17 Voice 文脈）
- 確認: 未

## REJECT — trend-log `fired` pre-fill before PdM FIRE LIVE (jenny-lite 2026-09-12..09-18)

- 内容: Planner daily の `fired` セルは PdM FIRE と人間 writeback まで空のまま。LIVE 先取りは ADV MUST で差し戻す。stall 対策として fired を先に埋めて「出荷済み」に見せない。CreateAgent NONE。
- 決定: REJECT
- 出典: https://github.com/maplefukku/grok-bot-ops/pull/125 · https://github.com/maplefukku/grok-bot-ops/pull/134 （2026-09-11..09-17）
- 確認: 未

## ADOPT — named *-HOLD + enabled=false = intentional GAP

- 内容: 名前付き `*-HOLD` かつ enabled=false は intentional GAP。stall leftover 一覧に載せない。monkey *-HOLD no OUT は stall ではない。
- 決定: ADOPT
- 出典: https://github.com/maplefukku/grok-bot-ops/issues/16 （2026-09-11）
- 確認: 未

## ADOPT — ACK-then-stop after CORR flood → JOB again SAME sweep

- 内容: PM/conductor が inbound CORR flood のあと leftover があるのに ACK-then-stop したら、同じ sweep で JOB し直す（次 sweep 待ち禁止）。cite parallel-fire-fleet。
- 決定: ADOPT
- 出典: https://github.com/maplefukku/grok-bot-ops/issues/16 （2026-09-11; PdM ACK-then-stop after squash/CORR 09-10 16:12 文脈）
- 確認: 未

## ADOPT — overnight babysit CA count ≠ lane moving

- 内容: overnight babysit の CA 本数は lane moving の証拠にしない。leftover があり product idle age が閾値超なら same-sweep で CoS（PM）へ nudge。
- 決定: ADOPT
- 出典: https://github.com/maplefukku/grok-bot-ops/issues/16 （2026-09-11; idle-with-leftover evening/overnight 09-10..09-11）
- 確認: 未

## GATE 観測 — ADV skip≠SUCCESS は ADOPT D 済み、tip-sot behind=0 は未カバー (jenny-lite 2026-09-07..09-11)

- 内容: ADV skip≠SUCCESS の必須化は既存 ADOPT D（GATE IFF = CI + bots + thr0）でカバー済み。tip-sot behind=0 は当時 process WRAP に無い — 正本 merge-ok 4 行（required CI / Cursor bots / MUST threads / NIT threads）にも `bots/PR確認.md` にも LIVE thr check にも behind の行は無く、カバー済みと書かない。behind>0 時の STEER rebase only は miss の観測であり、merge-ok 表へ行を足すかは Planner の decide-trend-adopt。新スキルはここで invent しない。
- 決定: ADV 半分は既存 ADOPT D。behind 半分は観測のみ（ADOPT しない）
- 出典: https://github.com/maplefukku/sauna-master/pull/362 · https://github.com/maplefukku/sauna-master/pull/406 · https://github.com/maplefukku/ZuruNote/pull/328 · https://github.com/maplefukku/grok-bot-ops/issues/16 （2026-09-11; modes false-GATE tip-sot behind miss / ADV skip≠SUCCESS）
- 確認: 未

## ADOPT — PdM Flag Y ONLY behind0+thr0+FULL CLEAN+APPROVED+ADV SUCCESS (#127)

- 内容: merge sweep の PdM Flag Y は 1 述語（4 見出し MUST + merge-ok 4 行 all true + behind0/thr0/FULL CLEAN/APPROVED/ADV SUCCESS）。APPROVED は GraphQL `author.__typename`=`User` の `APPROVED`（`Bot`/`reviewDecision` 単体不可）。Flag≠Bugbot。thr0∧merge-ok 食い違い時は merge-ok false の間 Flag しない。HOLD merge=PM。針は `test_flag_y_only_lock.py`。#127 slice A thr-close は issue 本文。decide-trend writeback は `ops/daily-*` owed。cite cloud / pr-2 / pr / pr-status-dedupe-quiet / conductor-keep-moving / parallel-fire-fleet Merge Gate / tool-path-prefer。scanner・hourly cron・第二 Flag 定義は invent しない。
- 決定: ADOPT
- 出典: https://github.com/maplefukku/grok-bot-ops/issues/127 （2026-09-14）
- 確認: 未

## Astra が Codex と ChatGPT Work にフル展開

- 内容: OpenAI 公式: Astra が Codex と ChatGPT Work の Plus / Pro / Business / Enterprise にフル展開。
- 出典: [x.com/OpenAI/status/2097431322117476423](https://x.com/OpenAI/status/2097431322117476423) · [openai.com/gpt-tv](https://openai.com/gpt-tv/)（2026-09-08）
- 確認: 未

## ADOPT — LIVE thr check

- 内容: LIVE の unresolved-thread 判定は毎回実測する。「bots待ちIDLE」を thr=0 の誤判定で ACK しない。同じ sweep で thr を取り直してから restart / escalate する。false thr=0 での idle ACK は禁止。
- 決定: ADOPT
- 出典: https://github.com/maplefukku/grok-bot-ops/issues/16 （fleet stalls 2026-09-01..09-05 / sauna#203 loop 文脈）（2026-09-06）
- 確認: 未

## ADOPT B — ADV reopen: reason+resolve nits, not infinite loop

- 内容: ADV / Bugbot の NIT は reason を残して resolve。無限に reopen / 往復しない。MUST は fix か明示 WONTFIX+根拠。NIT は最大1往復。同じテーマの2回目で新しい failing check が無いなら ignore + resolve。Closer が Resolve を持ち、追加実装はしない。無限の code loop ではない（sauna#203 パターン）。
- 決定: ADOPT
- 出典: https://github.com/maplefukku/grok-bot-ops/issues/16 （2026-09-06）
- 確認: 未

## ADOPT C — Swift flake: Swift-only auto-kick vs ONE fix-CA when signal6 reproducible

- 内容: Mac Swift package の signal 6 flake は、まず Swift-only の auto-kick（再実行）で様子を見る。再現が固まったら fix CA は1本だけ。無限 auto-kick や並列の追加 XC / 二重 CA はしない。toolchain 由来なら product merge で逃げない。
- 決定: ADOPT
- 出典: https://github.com/maplefukku/ZuruNote/pull/263 （2026-09-06）
- 確認: 未

## ADOPT D — GATE IFF = CI + bots + thr0; ADV skip ≠ SUCCESS; Flag before squash

- 内容: merge GATE は CI green かつ Cursor bots done かつ unresolved threads 0 のときだけ（GATE IFF = CI + bots + thr0）。ADV skip / dismiss を SUCCESS 扱いしない。ADV skip は done ではない。ADV を SUCCESS と扱う前に Flag する。GATE-soft だけでは merge しない。squash / merge の前に Flag（人または CoS）する。ボットは squash しない。
- 決定: ADOPT
- 出典: https://github.com/maplefukku/grok-bot-ops/issues/16 と https://github.com/maplefukku/grok-bot-ops/blob/main/AGENTS.md （2026-09-06）
- 確認: 未

## REJECT — new QA bot / auto-merge / 監視 monkey / Mac-Swift-TF leftover / GTM drafts as stall

- 内容: jenny-lite / repeated-stall の答えは knowhow と skills。CreateAgent NONE・Jenny seat を増やさない。Soft Flag invent しない。auto-merge しない。監視に monkey / Drive を走らせない。Mac-Swift-TF leftover path を残さない。GTM drafts を stall 扱いしない。false-thr0 LIVE check の再 ADOPT しない（既存 LIVE）。
- 決定: REJECT
- 出典: https://github.com/maplefukku/grok-bot-ops/issues/16 （2026-09-06）
- 確認: 未
