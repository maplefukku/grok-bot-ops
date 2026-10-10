# fleet

フリート停滞、merge GATE、jenny-lite の ADOPT と REJECT の置き場。
対象窓は fleet stalls 2026-09-01..09-05（sauna#203 loop、ZN Swift cluster）、jenny-lite 2026-09-07..09-11、jenny-lite 2026-09-12..09-18（#127 merge bottleneck / daily SoftACC）、および jenny-lite 2026-09-22..09-25。出典は各エントリの URL。

## Jenny-lite stall-adopt 2026-10-05〜10-09 (監視 93e56b37)

- 出典: 席の台帳 [bots/監視.md](https://github.com/maplefukku/grok-bot-ops/blob/main/bots/監視.md)（id 93e56b37）。各項の観測出典の表記は「監視 jenny-lite 2026-10-09」。

### 観測 (jenny-lite 2026-10-05..10-09)

- 内容: (1) 箱 Shell 固着 7回以上（10/5 09:45・17:51・19:46・21:45、10/9 16:06・17:10・17:56 JST）。840s timeout または 'still starting up'。1回あたり約14分を失い、Mode D と agency の確認ができなかった。出典: 監視 jenny-lite 2026-10-09
- 内容: (2) sauna#449 は tip 6ba6dbdb で CLEAN・thrLIVE 0 だが、APPROVED は旧 tip c2732f13 のみ。07:55 に PM と開発リーダーへ1回送ったあと、8回以上のスイープで「再送しない」を続け、約12時間だれも動いていない。出典: 監視 jenny-lite 2026-10-09
- 内容: (3) 10/9 14:00 JST 以降マージ 0 件。5回以上のスイープが「差分なし」だけで終わった。出典: 監視 jenny-lite 2026-10-09
- 内容: (4) 優先度低: 工場 Mode A BROKEN と tips 発火漏れが、08:49 JST の JOB 1回のあと 10/8〜9 のスイープで保留のまま運ばれた。出典: 監視 jenny-lite 2026-10-09
- 確認: 未（出典: 監視 jenny-lite 2026-10-09）

### ADOPT B — 承認が古い tip にあるときの「再送しない」は昼間4時間まで (jenny-lite 2026-10-05..10-09)

- 内容: APPROVED が旧 tip にしかなく、新 tip が CLEAN・thrLIVE 0 のとき、「再送しない」で静かにしてよいのは昼間4時間まで。出典: 監視 jenny-lite 2026-10-09
- 内容: 4時間を超えたら PdM（2f5b9c0d）に1回だけ、PR・tip・だれが再承認するかを伝える。そのあとはまた静かにする（毎スイープ再送しない）。出典: 監視 jenny-lite 2026-10-09
- 決定: ADOPT（出典: 監視 jenny-lite 2026-10-09）
- 出典: 監視 jenny-lite 2026-10-09（sauna#449 tip 6ba6dbdb / 旧 APPROVED c2732f13）
- 確認: 未（出典: 監視 jenny-lite 2026-10-09）

### ADOPT C — マージ差分なし 3回連続 + 詰まり判明なら PdM に一覧を1回 (jenny-lite 2026-10-05..10-09)

- 内容: 昼間スイープで3回以上続けてマージ差分がなく、かつ各 open PR の詰まりが1つずつわかっているときは、PdM に PR・詰まり・担当の短い一覧を1回送る。出典: 監視 jenny-lite 2026-10-09
- 内容: 「差分なし」を書き続けない。9/11 の ADOPT C と「ADOPT — overnight babysit CA count ≠ lane moving」（idle-with-leftover）の延長。出典: 監視 jenny-lite 2026-10-09
- 決定: ADOPT（出典: 監視 jenny-lite 2026-10-09）
- 出典: 監視 jenny-lite 2026-10-09
- 確認: 未（出典: 監視 jenny-lite 2026-10-09）

### 記録のみ — A: 箱 Shell プリチェック（スキル化は PM 経由） (jenny-lite 2026-10-05..10-09)

- 内容: fleet-stall-sweep / ci-health-sweep で、長い走査の前に60秒以下の箱 Shell で箱を確かめる。固まっていたら GitHub コネクタと RecallMemory に切り替え、箱を使う項目は stall ではなく「UNSCORED (box)」と書く。出典: 監視 jenny-lite 2026-10-09
- 内容: 1日3回以上なら箱の不調として debugging-the-box を1回だけ案内し、再起動はしない。出典: 監視 jenny-lite 2026-10-09
- 決定: 記録のみ。スキル化は PM 経由でスキル作成へ。Knowhow は skill を書かない。出典: 監視 jenny-lite 2026-10-09
- 確認: 未（出典: 監視 jenny-lite 2026-10-09）

### REJECT — 新 bot / 自動マージ / monkey 変更 / 箱不調の stall 再起動 / #449 毎回再送 (jenny-lite 2026-10-05..10-09)

- 内容: 新しい bot や CreateAgent はしない。自動マージや再承認の強制はしない。monkey は変えない。箱の不調を stall として再起動しない。#449 を毎回再送しない。出典: 監視 jenny-lite 2026-10-09
- 決定: REJECT（出典: 監視 jenny-lite 2026-10-09）
- 確認: 未（出典: 監視 jenny-lite 2026-10-09）

## REJECT — Mode A factory の age_d>3 escalate (jenny-lite 2026-09-22..09-25)

- 内容: 最初の rearm JOB のあと age_d>3 で Buddy|CBO|ルーチン作成へ escalate する案。Mode A の定義と閾値（lastRun stale>1d）は issue 136 の表が正本で、ここで閾値 age_d>3 を足さない。再 ADOPT しない。
- 決定: REJECT（証拠不足: age_d>3 を示す fleet 内の観測 URL が無い。再浮上: daily-character-factory の lastRun が 3 日を超えて止まった run を URL 付きで 1 件残し、issue 136 の表を改めるとき）
- 出典: https://github.com/maplefukku/grok-bot-ops/issues/136 · https://github.com/maplefukku/grok-bot-ops/issues/16 （daily-character-factory lastRun~2026-09-16、窓 2026-09-22..25）
- 確認: 未

## REJECT — GraphQL RATE_LIMIT 下の thr0 の再 ADOPT (jenny-lite 2026-09-22..09-25)

- 内容: RATE_LIMIT で reviewThreads の pagination が完了しないときに thr0 と数えない、という案。これは既存の「ADOPT — LIVE thr check」と「ADOPT — PdM Flag Y ONLY behind0+thr0+FULL CLEAN+APPROVED+ADV SUCCESS (#127)」の thr0 と同型なので、再 ADOPT しない。
- 決定: REJECT（LIVE 同型。証拠不足: RATE_LIMIT で page が欠けた観測の URL が無い。再浮上: pagination 未完了を thr0 と誤って数えた run を URL 付きで 1 件残したとき）
- 出典: https://github.com/maplefukku/grok-bot-ops/issues/127 （thr0 の定義、2026-09-22..25 の窓で参照）
- 確認: 未

## REJECT — Mode D research/X SILENT_MISS >3d の rearm (jenny-lite 2026-09-22..09-25)

- 内容: research/X weekday pulse の SILENT_MISS >3d で CMO|ルーチン作成へ rearm JOB を出す案。research/X は issue 136 Mode D（not-eng-only checklist）の採点対象で、閾値 >3d は issue 136 に無い。新 X 席は invent しない。GTM drafts は stall ではない。
- 決定: REJECT（証拠不足: fleet 内の lastRun URL が無い。再浮上: ルーチン作成が SILENT-MISS を 1 件 URL 付きで観測したとき）
- 出典: https://github.com/maplefukku/grok-bot-ops/issues/136 · https://github.com/maplefukku/grok-bot-ops/issues/16 （grokbot-tips last~2026-09-17、窓 2026-09-22..25）
- 確認: 未

## KEEP — 2026-09-06 / 09-11 の既存 ADOPT (jenny-lite 2026-09-22..09-25)

- 内容: behind0+ADV SUCCESS GATE、overnight idle≠babysit、monkey HOLD intentional、false thr0 same-sweep restart は既存の行のまま。指す先は「ADOPT D — GATE IFF = CI + bots + thr0; ADV skip ≠ SUCCESS; Flag before squash」「ADOPT — named *-HOLD + enabled=false = intentional GAP」「ADOPT — overnight babysit CA count ≠ lane moving」「ADOPT — LIVE thr check」。この火で再 ADOPT しない。
- 決定: KEEP（再 ADOPT しない）
- 出典: https://github.com/maplefukku/grok-bot-ops/issues/16 （2026-09-06 / 2026-09-11）
- 確認: 未

## REJECT — CreateAgent / tip remint SoT / Discord drip / invent thr0 under RATE_LIMIT / sixth micro-cron (jenny-lite 2026-09-22..09-25)

- 内容: CreateAgent / Jenny seat / credit-audit fixer bot しない。auto-merge / webhook→fixer auto-exec しない。prefer-corr remint を tip SoT にしない。Discord drip / content catch-up を factory fixed にしない。監視に monkey Drive/E2E させない。RATE_LIMIT 下で thr0 invent しない。sixth micro-cron / */10 invent しない。GTM drafts / TF Archive を stall にしない。
- 決定: REJECT
- 出典: https://github.com/maplefukku/grok-bot-ops/issues/16 （2026-09-22..25）
- 確認: 未

## Grok 4.7 + GrokBot の 3-agent（PM / Designer / Developer）

- 内容: 共有 brief から Project Manager がタスク分解、Designer が UI、Developer が実装、GrokBot が調整、という 3 ロール構成の報告。Planner 判断用候補のみ（新 Bot invent しない）。
- 出典: [x.com/Brankotrcek/status/2102463454858940705](https://x.com/Brankotrcek/status/2102463454858940705)（2026-09-22）
- 確認: 未

## ADOPT — #127 Flag Y ONLY writeback landed in process + ci lock (jenny-lite 2026-09-12..09-18)

- 内容: tip-sot behind0 は #128 で [`pr-body.md`](../process/pr-body.md) の PdM Flag Y ONLY 表（behind0/thr0/FULL CLEAN/APPROVED/ADV SUCCESS）に WRAP 済み。述語 pin は `test_flag_y_only_lock.py` → `ci.py` `flag-y-only-lock`。scanner・第二 Flag 定義は invent しない。HOLD merge=PM。GATE 観測（09-07..09-11）の behind 半分の writeback はここで close。
- 決定: ADOPT
- 出典: https://github.com/maplefukku/grok-bot-ops/pull/128 · https://github.com/maplefukku/grok-bot-ops/issues/127 （2026-09-14）
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
