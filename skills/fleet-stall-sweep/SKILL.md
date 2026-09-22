---
name: fleet-stall-sweep
description: >-
  Use when checking the fleet for stalls, leftover work, or ACK-then-stop. Live
  thr check before any bots-wait / IDLE / thr=0 ACK; false thr0 fails and
  restarts same sweep. Idle-with-leftover nudges CoS now. HARD jenny-lite A+D:
  factory BROKEN until trusted fire; every sweep scores factory+Discord +
  research/X weekday + untrusted provenance (eng thr/CA-only = FAIL). HOLD:
  REJECT webhook→fixer auto-exec. Not GTM drafts or TF Archive as stall.
---
# Fleet stall sweep

Read-only sweep for stalled bots and leftover work. Do not implement.

Cite [author-routines](sand-workflow:author-routines), [schedules-force-agency](sand-workflow:schedules-force-agency), [conductor-keep-moving](sand-workflow:conductor-keep-moving). invent=N. CreateAgent NONE.

## When

A scheduled sweep, or a JOB that asks whether the fleet is stuck.

## Inputs and access

- The ledger: who exists, who waits for a fire cue
- Observable surfaces: last activity in each conversation, open PRs, live Cloud Agents
- **Live unresolved review thread count (`thr`)** per open PR (gh / PR status facts — not a bot's claim)
- Factory / Discord / research / X weekday pulse surfaces (not eng thr/CA alone)
- Routine `enabled`, lastRun, due slot, and provenance trust when factory is in scope
- The stall threshold from the JOB or the owning role

No cron in this skill. No bot ids. No repo names.

## HARD — Mode A: factory BROKEN until trusted fire

Factory is **BROKEN** (not LIVE) when any hold:

1. `provenance=untrusted`, or
2. `lastRun` is stale **>1d**, or
3. a **due slot miss**

Rules:

- `enabled=true` alone **≠ LIVE**. Do not treat enabled as proof the factory is healthy.
- LIVE only after a **trusted fire** updates `lastRun`.
- Same-sweep JOB = **routine-author (rearm / restore trust)** + **factory Discord-only seat**. Soft Flag N non-factory Discord login. Soft Flag N Discord drip from the supervisor seat.
- Soft Flag N content catch-up as "fixed" while trusted `lastRun` is missing.
- Soft Flag N eng-only sweep that drops factory from the scoreboard.

## HARD — Mode D: not-eng-only checklist

Every sweep **must** score all of:

1. factory + Discord
2. research / X **weekday** pulse
3. untrusted provenance (factory and any seat that carries provenance)

**eng thr/CA-only** sweep = **FAIL**. Do not restate older LIVE thr / Sep11 HOLD rows here — this DELTA only blocks eng-only shrink.

## Live thr before bots待ち / IDLE / thr=0

Before accepting **any** 「bots待ち」「IDLE」「thr=0」ACK:

1. Read **live** `thr` on that PR (unresolved comment threads right now).
2. If the worker claims thr=0 (or bots待ち / IDLE) but live `thr` > 0 → **false thr0 = FAIL**. In **this same sweep**, draft restart JOB to the **impl conductor** and the **product worker** for that same PR / same CA path. Do not wait for the next cron slot. Do not soft-wait behind another PR.
3. Only treat bots待ち / IDLE as quiet when live `thr` is actually 0 (or the wait is a named human HOLD).

## Idle with leftover

If a lane is idle and leftover still exists for any product → **FAIL**. Draft an immediate nudge JOB to the chief of staff. Do not wait for the next cadence.

## HOLD — webhook→fixer

**REJECT** treating webhook→Bot fixer auto-exec as a stall fix. Keep proposal-only; do not invent auto-fixer seats ([tool-path-prefer](sand-workflow:tool-path-prefer)).

## Not stall (REJECT)

Do **not** treat these as stall leftover, and do **not** encode the opposite of these rejects:

- CreateAgent / Jenny seat / credit-audit or fixer bot
- Auto-merge / webhook-fixer auto-exec
- Supervisor Discord drip / non-factory discord.com / Forks wipe / cookie-seed
- eng-only stall sweep
- trusted-lastRun-less factory "fixed" via content catch-up
- Supervisor-run monkey Drive/E2E
- Mac Swift rerun or TestFlight Archive as leftover
- GTM drafts as stall
- Mem0 / new dash / invent sixth workflow name

## Sequence

1. List in-flight jobs. Leftover work first, then other still-can-do. Skip items in Not stall.
2. Run Mode D checklist (factory+Discord, research/X weekday, untrusted provenance). eng-only = FAIL this sweep.
3. Score factory via Mode A. BROKEN → same-sweep JOB to routine-author (rearm) + factory Discord-only seat. Soft Flag N content catch-up as fixed.
4. For each job, take the last observable progress (message time, PR update, Cloud Agent state).
5. For any PR marked bots待ち / IDLE / thr=0: run the live thr check above first.
6. Mark a stall when progress is older than the threshold, or the bot ACKed and then stopped with leftover, or false thr0, or idle-with-leftover, or Mode A/D fail.
7. Quiet if everything is moving, thr claims match live thr, and Mode A/D pass.
8. For each stall, draft one JOB to the chief of staff: restart or nudge whom. False thr0 → restart same sweep (impl conductor + product worker). Idle-with-leftover → nudge CoS now. Do not do the work.

## Validate

- Every stall has a timestamp
- Mode A: enabled=true alone never counted as factory LIVE; BROKEN produced rearm + factory Discord-only JOB; no content-catch-up "fixed"
- Mode D: factory+Discord, research/X weekday, and untrusted provenance were scored; eng-only = FAIL
- Every bots待ち / IDLE / thr=0 claim was checked against live thr
- False thr0 produced a same-sweep restart draft (not soft-wait behind another PR)
- Idle-with-leftover produced an immediate CoS nudge draft
- Not-stall items were not listed as stall
- The report includes how many jobs were checked

## Return

Stall list (including false-thr0, idle-with-leftover, Mode A BROKEN, Mode D eng-only fails), check count, and the drafted JOBs. Stay quiet when the sweep found no gap.

## Approval

None. Read and message only. Do not write code, clone, merge, approve, CreateAgent, auto-merge, launch a Cloud Agent, or run monkey.
