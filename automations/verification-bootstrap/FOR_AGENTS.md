# verification bootstrap intent

## what i want

i want one product repository to gain a working verification skill and
feature map, proven end to end, plus a daily maintenance routine, so
that every future agent can verify app behavior in that repo without a
setup conversation.

## for the agent

the human enters this flow by pointing you at this file and naming the
target product repository. work on the product repository, not on
grok-bot-ops.

1. ask which repository is the target if not already named. confirm it
   is registered in `grok-bot-ops/products/`; if not, add an entry from
   `products/_template.md` first.
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
6. update the product's entry in `grok-bot-ops/products/`: verify-skill
   path, feature map path, date.
7. tell the human to attach `routines/maintain-verification.md` to a
   dedicated bot if not already running, so the feature map is
   refreshed daily.

## boundaries

- never write the verification skill or feature map into grok-bot-ops.
  it must live in the product repository, or cloud agents checking out
  the product will not see it.
- draft PRs only on the product repository. do not merge.
- if the app cannot be launched from the repository alone (missing
  secrets, external services), stop and list exactly what the human
  must provide. do not fake a passing proof.
