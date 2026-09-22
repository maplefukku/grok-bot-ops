---
name: schedules-force-agency
description: >-
  Use when designing or auditing seats or CreateAgent. HARD: every standing bot
  agency = forced schedule/routine OR named cascade from a scheduled parent;
  agency ≠ LLM vibe ≠ wait-for-ping; HANDS may inherit via conductor cron
  same-turn FIRE (weekday-pulse-cascade + parallel-fire-fleet); event seats OK
  if live; DISABLED cron without HOLD reason = FAIL. HARD jenny-lite A+C:
  factory enabled=true alone ≠ LIVE until trusted fire; enabled=true ∧ lastRun
  past schedule window = SILENT-MISS FAIL (runs.json ≠ disable SoT).
---
# Schedules force agency

HARD: standing-bot agency is forced by schedule (or a named cascade from a scheduled parent). Agency is not LLM mood and not wait-for-ping.

Cite [fleet-stall-sweep](sand-workflow:fleet-stall-sweep), [author-routines](sand-workflow:author-routines), [weekday-pulse-cascade](sand-workflow:weekday-pulse-cascade), [parallel-fire-fleet](sand-workflow:parallel-fire-fleet). invent=N. CreateAgent NONE.

## When

Designing or auditing seats, CreateAgent personas, or enable notes for standing bots. Before calling a seat “alive.” Not for writing cron expressions here (those belong in routines). Not product code.

## Inputs and access

- Seat role / ONE JOB
- Whether the seat is standing (always-on expectation) vs pure event/HITL
- Parent scheduled pulse (if HANDS inherit)
- Routine `enabled`, lastRun, schedule window, provenance trust
- [weekday-pulse-cascade](sand-workflow:weekday-pulse-cascade), [parallel-fire-fleet](sand-workflow:parallel-fire-fleet)

No bot ids. No repo names. No cron expressions in this skill body.

## HARD agency rules

1. **Every standing bot** must have an agency body that is one of:
   - a **forced schedule** (routine / cron owned outside this skill), or
   - a **named cascade** from a scheduled parent (same-turn FIRE after that parent’s pulse)
2. **Agency ≠ LLM vibe.** “I’ll check when I feel like it” is FAIL.
3. **Agency ≠ wait-for-ping.** Idle until someone messages is FAIL for standing seats (HITL-only apex may wait on human; that is HOLD, not standing ops).
4. **HANDS may inherit:** worker hands under a conductor may get agency via the conductor’s scheduled pulse → same-turn multi-FIRE ([weekday-pulse-cascade](sand-workflow:weekday-pulse-cascade) + [parallel-fire-fleet](sand-workflow:parallel-fire-fleet)). Name the parent pulse in the seat design.
5. **Event seats OK if live:** webhook / reaction / PR-event listeners count as forced agency when they are armed and live.
6. **DISABLED schedule without HOLD reason = FAIL.** Pausing or disabling a standing routine needs a named HOLD (human or CoS). Silent disable is FAIL.
7. **Root coordinator gate:** minimal useful composition first; Lead owns day-to-day cascade; Root relays verified results only (invent=N Soft-HOLD WRAP).
8. **Mode A — factory BROKEN until trusted fire:** Skip when named HOLD active or `enabled=false` (intentional GAP; no rearm). When `enabled=true` and HOLD cleared: `enabled=true` alone ≠ LIVE; provenance=untrusted OR lastRun stale >1d OR due slot miss → BROKEN. LIVE only after trusted fire updates lastRun. Soft Flag N content catch-up as fixed ([fleet-stall-sweep](sand-workflow:fleet-stall-sweep), [author-routines](sand-workflow:author-routines)).
9. **Mode C — agency silent-miss:** `enabled=true` **and** `lastRun` is past the schedule window = **SILENT-MISS FAIL**. Same-sweep JOB = **owner seat + routine-author**. Applies to linux-runner-offline-ping, keep-moving-*, tips-3x, and factory-class routines. **REJECT** treating filesystem `runs.json` as disable SoT.

## HARD — Root coordinator gate (mrbeko WRAP; invent=N)

When designing standing seats / cascades: (1) decide **minimal useful composition** before adding agency bodies; (2) day-to-day agency runs through the **Lead cascade** (HANDS inherit), not Root pinging every seat; (3) Root / apex OUT is **verified results only** (pass/fail + evidence), not WIP relays. Soft-HOLD WRAP existing HANDS-inherit + weekday-pulse-cascade + parallel-fire-fleet. **REJECT** inventing a Root Agent coordinator seat or new agency harness. CreateAgent NONE. Cite 1° mrbeko Root Agent coordinator + EXISTING schedules-force-agency — one-line WRAP only.

## Sequence

1. Classify seat: standing ops | event-live | HITL-only | HANDS-under-parent | factory-class.
2. Require an agency body matching the class (schedule, event arm, named cascade, or explicit HITL HOLD).
3. Score Mode A (factory) and Mode C (silent-miss) before calling the seat alive.
4. On CreateAgent / audit: write the agency line into the persona (kind + parent if cascade). Do not paste cron expressions into the skill library — attach them on the routine.
5. FAIL the design if standing + no schedule + no cascade + no live event.
6. SILENT-MISS → same-sweep JOB to owner + routine-author. Soft Flag N runs.json disable SoT.
7. OUT: seat class, agency kind, parent (if any), Mode A/C notes, FAIL/HOLD notes.

## Validate

- Standing seats have schedule or named cascade or live event
- No “ping me” agency for standing ops
- Disabled cron/routine has HOLD reason
- Mode A: enabled=true alone never LIVE; no content-catch-up fixed
- Mode C: enabled=true ∧ lastRun past window = SILENT-MISS FAIL; runs.json not used as disable SoT
- No cron expression text stored in this skill

## Return

Agency map per seat (class, kind, parent, HOLD, Mode A/C), PASS/FAIL.

## Approval

Disabling standing agency needs CoS/HITL HOLD. Do not CreateAgent without agency line. Do not merge.
