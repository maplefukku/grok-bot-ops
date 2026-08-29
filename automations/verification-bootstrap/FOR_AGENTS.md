# verification bootstrap intent

## what i want

i want one product repository to gain a working verification skill and
feature map, proven end to end, plus a daily maintenance routine, so
that every future agent can verify app behavior in that repo without a
setup conversation.

## for the agent

the human enters this flow by pointing you at this file and naming the
target product repository. the work spans two repositories with a
strict split: all verification code (the skill, the feature map, the
proof) lives in the product repository; grok-bot-ops holds only the
product's ledger entry under `products/`, which you must keep current.

1. ask which repository is the target if not already named. confirm it
   has a ledger entry under `products/` in grok-bot-ops; if not, add
   one there now, copied from `products/_template.md`. this ledger
   write in grok-bot-ops is required, and is exactly what its
   AGENTS.md write rules allow.
2. launch a cloud agent rooted in the target repository.
3. in that repository, check for an existing `verify-*` skill under
   `.cursor/skills/` or an existing harness that can drive the app. if
   one exists and passes its own doctor check, skip to step 6.
4. run `/create-verification-skill`. it interviews the repository, not
   the human: how the app launches, what can drive it (existing harness
   first, otherwise browser and CDP, a PTY, or plain HTTP), what
   evidence proves behavior, and whether two instances can run side by
   side. it writes `.cursor/skills/verify-<app>/` with Launch, Doctor,
   Drive, Evidence, and Cleanup sections plus a feature map under
   `features/`.
5. the generator must prove the skill once end to end: launch, doctor
   check, drive one feature, capture evidence, clean up. if that proof
   fails, do not ship the output; fix and retry. open the result as a
   PR on the product repository.
6. back in grok-bot-ops, update the product's ledger entry under
   `products/`: verify-skill path, feature map path, date.
7. tell the human to attach `routines/maintain-verification.md` to a
   dedicated bot if not already running, so the feature map is
   refreshed daily.

## boundaries

- never write the verification skill or feature map into grok-bot-ops.
  it must live in the product repository, or cloud agents checking out
  the product will not see it.
- the only grok-bot-ops writes in this flow are the ledger entry under
  `products/` (steps 1 and 6). do not skip them: the daily
  maintain-verification routine finds its targets by reading
  `grok-bot-ops/products/`, so an unrecorded product is never
  maintained.
- on the product repository, draft PRs only. do not merge anywhere.
- if the app cannot be launched from the repository alone (missing
  secrets, external services), stop and list exactly what the human
  must provide. do not fake a passing proof.
