# fleet

フリート停滞、merge GATE、jenny-lite の ADOPT と REJECT の置き場。
対象窓は fleet stalls 2026-09-01..09-05（sauna#203 loop、ZN Swift cluster）および jenny-lite 2026-09-07..09-11。出典は各エントリの URL。

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
