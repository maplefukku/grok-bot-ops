---
name: author-routines
description: >-
  Use when auditing or creating Grok Bot seat routines (update_state target
  routine). Fleet WRAP only: HOLD-named pause KEEP; no resume-all UnHOLD; no
  micro-cron; merge duplicates; Soft Flag N Discord drip. HARD jenny-lite A:
  factory enabled=true alone ≠ LIVE; rearm trust only after trusted fire updates
  lastRun; content catch-up ≠ fixed. Cite managed routines + schedules-force-agency.
  Not a second platform how-to.
---
# Author routines (fleet WRAP)

Fleet how-to for authoring and auditing Grok Bot seat routines via `update_state` (target `routine`). Managed **routines** owns the platform mechanics (cron shape, event triggers, intent prompts). This skill adds fleet HARD only — do not duplicate managed routines.

Cite managed **routines** + [schedules-force-agency](sand-workflow:schedules-force-agency) + [fleet-stall-sweep](sand-workflow:fleet-stall-sweep) + [author-shared-skill](sand-workflow:author-shared-skill). Soft Flag N Discord drip. CreateAgent NONE.

## When

Auditing or creating standing-seat routines (agency body on a bot). Before adding a second cron for the same ONE JOB. Before pause/resume of fleet standing routines. Before treating a factory routine as LIVE. Not for inventing a parallel cron skill. Not for user personal reminders already covered by managed routines alone.

## Inputs and access

- Seat ONE JOB + agency class from [schedules-force-agency](sand-workflow:schedules-force-agency)
- Existing routines on that seat (survey first)
- Managed **routines** for cron/trigger/prompt mechanics
- Named HOLD reason if pausing
- Factory provenance / lastRun / due slot when the seat is factory-class

No bot ids. No repo names. No Discord drip packs as cron substitutes.

## HARD fleet (missing from managed routines alone)

1. **Agency first** — standing seat needs schedule **or** named cascade ([schedules-force-agency](sand-workflow:schedules-force-agency)). Routine without agency class = FAIL.
2. **HOLD-named pause KEEP** — pause only with a **named HOLD** (who + why). Silent pause / disable = FAIL.
3. **No resume-all UnHOLD** — resume one routine at a time after the HOLD clears. Never bulk-resume every paused routine.
4. **No micro-cron spam** — reject `@every 5m` / dense polling for Soft Flag / STATUS / Discord drip. Prefer coarse weekday pulses or event listeners. Soft Flag N Discord drip as a standing cron substitute.
5. **重複は統合** — if two routines share the same ONE JOB / same wake, merge into one (update or delete the duplicate). Do not stack near-duplicate crons.
6. **Invent=N** — WRAP managed routines + schedules-force-agency. Do not invent a second platform routine skill or seat.
7. **Mode A — factory BROKEN until trusted fire** — Skip when named HOLD active or `enabled=false` (intentional GAP; no rearm). When `enabled=true` and HOLD cleared: `enabled=true` alone ≠ LIVE; provenance=untrusted OR lastRun stale >1d OR due slot miss → BROKEN. Rearm / restore trust only; LIVE only after a **trusted fire** updates `lastRun`. Soft Flag N content catch-up as fixed. Same-sweep pair with factory Discord-only seat when stall-sweep JOBs the rearm ([fleet-stall-sweep](sand-workflow:fleet-stall-sweep)).

## Sequence

1. Survey existing routines on the seat. List duplicates and unnamed pauses.
2. Confirm agency class (schedule / cascade / event / HITL HOLD).
3. If factory-class: score Mode A before claiming LIVE. BROKEN → rearm only; Soft Flag N content catch-up fixed.
4. Create or amend **one** routine per ONE JOB. Prompt = intent (managed routines). Cron/trigger lives on the routine, not in other skills.
5. On pause: write HOLD name + reason; keep paused until that HOLD clears.
6. On resume: clear only that HOLD; never resume-all. For factory, resume ≠ LIVE until trusted fire updates lastRun.
7. Merge duplicates. Delete micro-cron / Discord-drip substitutes.
8. OUT: routine id, agency kind, HOLD (if any), Mode A LIVE/BROKEN, duplicates merged.

## Validate

- Managed routines mechanics followed (weekday window, event-over-poll when possible)
- HOLD-named on every pause; no resume-all
- No micro-cron Soft Flag / Discord drip standing spam
- Duplicates merged
- Mode A: enabled=true alone never claimed LIVE; no content-catch-up fixed
- No CreateAgent from this skill

## Return

Agency + routine map (create/update/pause/merge), HOLD names, Mode A LIVE/BROKEN, 1-line delta.

## Approval

Fleet LIVE routine changes follow CoS / bot-HR JOB. Do not CreateAgent. Do not merge product code. Soft Flag N Discord drip.
