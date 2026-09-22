---
name: conductor-keep-moving
description: >-
  Use when a conductor keeps ROUTE+FIRE on free lanes and leftover work. Live
  thrLIVE (paginated; outdated INCLUDED; Prefer newer 2026-09-17 10:04 JST) before bots-wait IDLE; false thr0 restarts same pass. Fat 1
  unit=1 PR user-story Soft Flag N 1-issue drip; CA multi-agent/nested OK on
  Cascade/Critique. Flag Y ONLY behind0+thrLIVE0 (outdated INCLUDED)+FULL CLEAN+APPROVED+ADV SUCCESS.
  Never ACK-then-stop. Pass Single/Cascade/Critique. HARD jenny-lite B: idle-with-leftover
  ≥3 same-day sweeps without seat-class escalate → escalate once to apex/CoS;
  infinite re-spam JOB REJECT. Existing weekday pulses only (no new weekday-pulse-cascade skill). No monkey.
---
# Conductor keep moving

Route and fire. When a worker lane is free and leftover exists, fire the next independent JOB now. An ACK with no next fire is not done. Cite [job-brief](sand-workflow:job-brief) for JOB shape. invent=N — WRAP existing; Soft Flag N Discord.

For product, social, and X conductors. Not job-brief (the brief form). Not stall-sweep (read-only for the chief of staff). Not monkey Drive/E2E (that is a separate ops skill and role).

## When

Leftover work exists or a worker lane is free. Also on a STATUS pass. Do not stop after acknowledging a JOB.

## Inputs and access

- Leftover list (open JOBs, PRs waiting to be assigned)
- Live lanes: which workers are busy or idle
- Independent next jobs that do not wait on each other
- Difficulty hint per JOB when known (Single / Cascade / Critique)
- **Live unresolved review thread count (`thr`)** on PRs claimed bots待ち / IDLE / thr=0 — **must paginate** (not page1/first100 only)
- Branch `behind` vs base when Flag is in play
- Same-day idle-with-leftover repeat count for Mode B
- Who receives STATUS (from the JOB or owning role)
- Existing weekday pulses (supervisor / eng conductor) — Soft Flag N invent a new weekday-pulse-cascade skill as the encode target

No bot ids. No repo names. No cron.

## HARD — fat unit / no drip (Buddy SoftACC WRAP)

When FIREing eng/impl leftover:

1. **1 unit = 1 PR** at **user-story grain** (fat BDD/scenario lander). Soft Flag N **1-issue=1-PR drip**.
2. Batch related issues into one lander JOB via [job-brief](sand-workflow:job-brief). Cite [parallel-fire-fleet](sand-workflow:parallel-fire-fleet) for independent units only.
3. Encode **Cursor CA multi-agent ON + nested subagents OK** on Cascade/Critique JOBs. Astra lane stays no-subagents ([cloud](sand-workflow:cloud) / job-brief).

## HARD — Flag Y ONLY (not conductor merge)

Do **not** Flag Y / treat as merge-ready unless **all** hold:

- `behind=0`
- live `thrLIVE=0` **paginated** — thrLIVE = count reviewThreads where isResolved=false (**outdated INCLUDED**); outdated_unresolved is SEPARATE; Soft Flag VOID thrLIVE=unresolved AND not outdated; Soft Flag VOID fresh-only thrLIVE; void first-page-only thr0 claims (Cite Buddy 2026-09-17 09:56 JST; Evidence #314 tip 527028c7 KEEP thrLIVE=3 VOID thrLIVE=1)
- **FULL CLEAN**
- **APPROVED**
- **ADV SUCCESS**

Flag ≠ Bugbot. SoftHOLD junk ≠ Flag Y. Merge ownership stays with **PM**. Soft Flag N Discord drip Flag spam.

## HARD — Mode B: JOB-flat idle-with-leftover ≥3 same-day

When the **same** idle-with-leftover JOB repeats across **≥3 same-day** sweeps / STATUS pulses and there has been **no seat-class escalate** (apex / CTO / Buddy-class CoS):

1. **Escalate once** to apex / CoS (Buddy/CTO class). Soft Flag N invent a new weekday-pulse-cascade skill — use **existing** weekday pulses (supervisor / eng conductor) plus this skill.
2. **Infinite re-spam JOB = REJECT.** Do not keep FIREing the same flat JOB after the one escalate.
3. Cite [fleet-stall-sweep](sand-workflow:fleet-stall-sweep) for the idle-with-leftover detection; this skill owns the escalate-once gate.

## Difficulty (pass through on FIRE)

When FIREing an impl JOB, name one HydraFusion task pattern so the worker maps it to Cursor Cloud Agent routing only.

Do not adopt the Copilot HydraFusion product or `/experimental`. Distinct from Cognition Fusion (plan vs execute). Patterns:

| Difficulty | Pattern | Pass in the JOB |
| --- | --- | --- |
| Easy / clear slice | **Single CA** | One CA, stay through closer |
| Medium / multi-file | **Cascade** | Cheap draft → gate → stronger model on same PR; multi-agent/nested OK |
| Hard / high-risk | **Critique** | Cross-family read-only critic → one fix round; multi-agent/nested OK |

Default: omit and let the worker choose per Cloud開発. Do not launch Cloud Agents yourself from this skill.

## Live thr before bots待ち / IDLE / thr=0

Before STATUS or ACK treats a lane as 「bots待ち」「IDLE」「thr=0」:

1. Read **live** `thrLIVE` on that PR (**paginate** all isResolved=false threads; **outdated INCLUDED**; Soft Flag VOID exclude-outdated thrLIVE).
2. If the worker reported thr=0 / bots待ち but live `thr` > 0 → **false thr0 = FAIL**. FIRE restart on the **same** PR / same CA **now** (this pass). Do not park until the next cadence. Do not soft-wait behind another PR.
3. Bots待ち / IDLE is only valid when live `thr` is 0 (or a named human HOLD).

## ADV leftover is resolve, not wait bots

Never ACK-then-stop while **live `thr` > 0** and the Cloud Agent has finished and review bots are done. That leftover is an **ADV resolve path** (MUST fix or WONTFIX; NIT one round then reason+resolve). It is not 「bots待ち」. FIRE the closer / restart on that same PR this pass.

## Not leftover (REJECT)

Do **not** treat these as leftover to fire, and do **not** encode the opposite:

- CreateAgent
- Auto-merge
- Supervisor-run monkey Drive/E2E
- Mac Swift rerun or TestFlight Archive as leftover
- GTM drafts as stall leftover
- Soft Flag Discord drip / 1-issue micro PRs as “progress”
- Infinite re-spam of the same idle-with-leftover JOB after Mode B escalate-once
- Inventing a sixth workflow / new weekday-pulse-cascade skill as Mode B encode target

## Sequence

1. List leftover. List free lanes. Skip items in Not leftover. Prefer fat user-story units over drip issues.
2. For any leftover marked bots待ち / IDLE / thr=0: run the live thr check (paginated). False thr0 → FIRE restart same pass. thr>0 with CA finished + bots done → FIRE ADV resolve path, not wait-bots.
3. Score Mode B: same idle-with-leftover JOB ≥3 same-day without seat-class escalate → escalate once to apex/CoS; Soft Flag N infinite re-spam.
4. ROUTE: match each free lane to an independent leftover JOB that the worker's role covers ([job-brief](sand-workflow:job-brief) shape).
5. FIRE: send that JOB now, with difficulty if known. Do not wait for an in-flight PR or CA if the next job is independent. Stack more whenever a lane frees. Serialize-wait is a fail.
6. Never ACK-then-stop. An ACK must include the next fire, or a clear empty-leftover / no-free-lane reason (after thr check), or the Mode B escalate-once note.
7. OUT STATUS only: moving Y/N; per lane live work and leftover; unused lanes; next independent job already fired Y/N; thr-check fails / ADV-resolve fires this pass; Mode B escalate Y/N; Flag Y eligibility (behind0+thr0 paginated+FULL CLEAN+APPROVED+ADV SUCCESS) when relevant; difficulty named on fires when set.
8. Do not COLLECT product bots into a PR-status handoff. PR status review is someone else's JOB after impl finishes. Do not run or dispatch monkey Drive/E2E from this skill. Do not Flag Y yourself unless the gate passes — PM owns merge.

## Validate

- Idle lane with leftover means a JOB was fired, or STATUS names why not
- Fat 1 unit=1 PR; no 1-issue drip FIREs as “done”
- Every bots待ち / IDLE / thr=0 claim was live-checked (paginated)
- False thr0 caused a same-pass restart FIRE
- thr>0 + CA done + bots done never became wait-bots ACK; ADV resolve was fired
- Mode B: ≥3 same-day idle-with-leftover without escalate produced exactly one apex/CoS escalate; no infinite re-spam; no new weekday-pulse-cascade skill invent
- Flag Y only when behind0+thrLIVE0 paginated (outdated INCLUDED)+FULL CLEAN+APPROVED+ADV SUCCESS
- STATUS has moving Y/N and unused lanes
- No ACK without next fire or empty reason
- Not-leftover rejects were not fired
- No collect-then-PR-status path
- No monkey path / CreateAgent / Discord drip
- Difficulty, if set, is Single / Cascade / Critique only

## Return

STATUS block and the JOBs fired this pass (including false-thr0 restarts, ADV-resolve fires, Mode B escalate-once; difficulty when set; Flag gate notes when relevant).

## Approval

Internal dispatch needs none. Do not merge. Do not auto-merge. Do not CreateAgent. Do not implement. Do not launch Cloud Agents yourself. Do not collect for PR review. Do not fire monkey. Soft Flag N Discord.
