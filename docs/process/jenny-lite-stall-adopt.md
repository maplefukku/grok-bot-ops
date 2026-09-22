# jenny-lite stall-adopt A–D（box sand-workflow WRAP）

## Purpose

Issue [#136](https://github.com/maplefukku/grok-bot-ops/issues/136) の A–D を **existing sand-workflow** へ encode する WRAP である。本体は box の [fleet-stall-sweep](sand-workflow:fleet-stall-sweep) / [author-routines](sand-workflow:author-routines) / [schedules-force-agency](sand-workflow:schedules-force-agency) / [conductor-keep-moving](sand-workflow:conductor-keep-moving)。

Soft Flag N `skills/` への本体コピー（plugin HARD）。Soft Flag N 「reviewable mirror」。Soft Flag N fallen tip `1a58a0d` を SoT にする。Soft Flag N 第六 workflow 名。Soft Flag N CreateAgent / Jenny seat / credit-audit / auto-merge / webhook-fixer auto-exec / eng-only stall sweep。Flag Y 述語は [`pr-body.md`](./pr-body.md) のみ（第二定義 invent しない）。HOLD merge=PM。

## Encode map

| Mode | Box sand-workflow | Done-when (HARD) |
|---|---|---|
| A factory BROKEN until trusted fire | fleet-stall-sweep + author-routines + schedules-force-agency | Score only when `enabled=true` and named HOLD cleared. Named HOLD / `enabled=false` = intentional GAP（no rearm）. BROKEN → same-sweep JOB = routine-author (rearm) + factory Discord-only **only**. Soft Flag N content catch-up as fixed. Soft Flag N extra CoS / Mode C JOB on the same observation. |
| B JOB-flat idle-with-leftover ≥3 same-day | conductor-keep-moving + existing weekday pulses（supervisor / eng conductor）。Soft Flag N invent `weekday-pulse-cascade` skill as encode target | Same idle-with-leftover JOB ≥3 same-day **without** seat-class escalate → escalate **once** to apex/CTO class. Infinite re-spam REJECT. stall-sweep の初回 CoS nudge は escalate 済みに数えない。 |
| C agency silent-miss | schedules-force-agency | `enabled=true` ∧ lastRun past schedule window = SILENT-MISS FAIL → owner + routine-author. Soft Flag N `runs.json` as disable SoT. Soft Flag N apply Mode C to factory-class when Mode A already owns that observation（factory = Mode A only）. Soft Flag N invent cites to files that lack lastRun/silent-miss text. |
| D not-eng-only checklist | fleet-stall-sweep | Every sweep scores factory+Discord + research/X weekday + untrusted provenance. eng thr/CA-only = FAIL. |

## Flag Y

PdM Flag Y ONLY は [`pr-body.md`](./pr-body.md)（behind0 / thr0 unresolved∧¬outdated / FULL CLEAN / User APPROVED / ADV SUCCESS）。conductor / stall-sweep は Flag しない。Soft Flag N thrLIVE outdated-INCLUDED で pr-body thr0 を VOID。

## CreateAgent

CreateAgent NONE。agency 監査は既存 CBO 経路の審査メモだけ。Soft Flag N 「agency 行があれば CreateAgent してよい」。

## Testing / promotion

スキル作成 eval playbook。1 スキル 1 PR after eval。Planner / Mini は plugin `skills/` に本体を置かない。PM ACK + 文字撞突解消 DELTA が揃うまで SoftHOLD。

## SoftHOLD

merge=PM。Soft Flag N undraft Soft Flag N FlagY Soft Flag N SoftB FIRE Soft Flag N merge from Mini WRAP alone.
