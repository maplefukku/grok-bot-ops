# fleet

フリート停滞、merge GATE、jenny-lite の ADOPT と REJECT の置き場。
対象窓は fleet stalls 2026-09-01..09-05（sauna#203 loop、ZN Swift cluster）。出典は各エントリの URL。

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

- 内容: jenny-lite / repeated-stall の答えは knowhow と skills。CreateAgent・新 QA ボットで穴を埋めない。auto-merge しない。監視に monkey / Drive を走らせない。Mac-Swift-TF leftover path を残さない。GTM drafts を stall 扱いしない。
- 決定: REJECT
- 出典: https://github.com/maplefukku/grok-bot-ops/issues/16 （2026-09-06）
- 確認: 未
