# devin-queue

A small file-based job queue that runs [Devin CLI](./devin_queue.py) jobs on
fukku-mac-mini. One job = one fresh clone = one `devin -p` headless run. It is
**not installed anywhere yet**; this directory is the code, a LaunchAgent
template, and docs.

## Layout

Default root `~/devin-queue/` (override with `--root` or `DEVIN_QUEUE_ROOT`):

```text
inbox/<id>.json       submitted jobs, FIFO by mtime then name
running/<id>.json     claimed jobs (atomic rename under a flock on .lock)
done/<id>.json        finished job + <id>.result.json
failed/<id>.json      failed job + <id>.result.json
work/<id>/            fresh clone per job (deleted on success, kept 3 days on failure)
logs/<id>.log         runner output + redacted CLI stdout/stderr
logs/runner.log       runner stdout/stderr (via launchd)
STATUS.json           {"state": "ok" | "stopped_quota" | "stopped_auth", ...}
PAUSE                 if present, run-once claims nothing
config.json           max_concurrency, default_timeout_sec, max_timeout_sec,
                      model default, repos allowlist
```

## Job file

```json
{
  "schema": 1,
  "job_id": "bazure-fallback-01",
  "task_id": "B-02",
  "repo": "maplefukku/bazure-discord",
  "base_branch": "wip/mini-live-20261103",
  "branch": "devin/bazure-fallback-01",
  "prompt": "the full task text...",
  "model": "swe-2",
  "timeout_sec": 3600,
  "pr": {"draft": true, "title": "draft: fallback", "base": "wip/mini-live-20261103"},
  "submitted_by": "me",
  "submitted_at": "2026-11-03T10:00:00+09:00"
}
```

Rules: `job_id` matches `[a-z0-9-]{1,64}` and is unique across
inbox/running/done/failed. `repo` must be in `config.json` `repos`. `model`
must be in the SWE-2 family (`swe-2`, `swe-2-high`, ...; `-lightning` variants
are rejected). `timeout_sec` must be `<= max_timeout_sec` (default 7200).
`pr.draft` must be `true`. Optional `continue_branch: true` clones `branch`
instead of creating it. Remote checks (`base_branch` exists, `branch` absent)
run via `git ls-remote` right before the job starts; a failure sends the job
to `failed/` with reason `invalid_job`.

## Usage

```sh
# create ~/devin-queue/ (dirs mode 700) and a default config.json
python3 tools/devin-queue/devin_queue.py init
# edit ~/devin-queue/config.json: add repos to the allowlist first

# submit a job file (writes inbox/.<id>.tmp then renames to <id>.json)
python3 tools/devin-queue/devin_queue.py submit /path/to/job.json

# one iteration: claim at most one job and run it
python3 tools/devin-queue/devin_queue.py run-once

# state
python3 tools/devin-queue/devin_queue.py status

# pipe any log through the redactor
cat some.log | python3 tools/devin-queue/devin_queue.py redact
```

What a run does: clone `--branch <base>` (or `<branch>` when
`continue_branch`), `git switch -c <branch>`, then
`devin -p --prompt-file <prompt> --model <model> --permission-mode dangerous
--respect-workspace-trust false --export work/<id>/session.atif`
(**no `--sandbox`**: in CLI 3000.11.1 it forces autonomous mode and stalls
headless `-p` runs). On `timeout_sec` the process group gets SIGTERM, then
SIGKILL after 30 s. Afterwards it checks `gh pr list --repo <repo> --head
<branch>`; if there is no PR but the branch has new commits it pushes the
branch (no force) and opens a draft PR with `gh pr create --draft --fill`.
It never merges, marks ready, comments, or force-pushes.

## Watching

```sh
gh pr list --repo <repo> --head <branch>
python3 tools/devin-queue/devin_queue.py status
cat ~/devin-queue/done/<id>.result.json    # or failed/
```

## Quota stop / auth stop / resume

After every run the redacted output is scanned for `out_of_quota`,
`usage_limit_exceeded`, `total_session_limit_exceeded`,
`insufficient credits`, and HTTP 402 / "payment required". A hit fails the
job with that reason, writes `STATUS.json` `stopped_quota`, and creates
`PAUSE`. Before a job starts, `devin auth status` is checked; if it fails the
job goes **back to inbox/** (not burned), STATUS becomes `stopped_auth`, and
PAUSE is created. In both cases the runner claims nothing until a human
fixes the cause and runs:

```sh
python3 tools/devin-queue/devin_queue.py resume   # removes PAUSE, STATUS=ok
```

No retry, no model switch, no purchase — that is a human decision.

## Install (later, separately approved)

`com.fukku.devin-queue.plist.template` is a template only. Installing it is a
separate step that needs explicit approval: copy it to
`~/Library/LaunchAgents/com.fukku.devin-queue.plist`, replace `__HOME__` and
`__PYTHON__`, then `launchctl bootstrap gui/$UID <plist>`. It runs `run-once`
every 60 s, restarts only on crash, and logs to `logs/runner.log`. Do not
install it as part of building or testing this tool.

## Tests

```sh
python3 -m unittest discover -s tools/devin-queue -p 'test_*.py'
```

No network, no real `devin`/`git`/`gh` calls; the queue root is a temp dir.

## Out of scope

Cloud sessions, secrets inside job files, deploys, and LaunchAgent changes
for other bots from inside a job.
