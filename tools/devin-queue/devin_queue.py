#!/usr/bin/env python3
"""File-based job queue runner for the Devin CLI.

Layout under the queue root (default ~/devin-queue, override with the
DEVIN_QUEUE_ROOT env var or --root):

    inbox/<id>.json      submitted jobs, FIFO by mtime then name
    running/<id>.json    claimed jobs (moved by atomic rename)
    done/<id>.json       plus <id>.result.json
    failed/<id>.json     plus <id>.result.json
    work/<id>/           fresh clone per job
    logs/<id>.log        redacted run log; logs/runner.log for the runner
    STATUS.json          {"state": "ok" | "stopped_quota" | "stopped_auth", ...}
    PAUSE                if present, run-once claims nothing
    config.json          queue settings (see DEFAULT_CONFIG)

Subcommands: init, submit, run-once, status, resume, redact.
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional, Sequence

ENV_ROOT = "DEVIN_QUEUE_ROOT"
DEFAULT_ROOT = Path.home() / "devin-queue"
DIRS = ("inbox", "running", "done", "failed", "work", "logs")
RESULT_SUFFIX = ".result.json"

DEFAULT_CONFIG = {
    "max_concurrency": 1,
    "default_timeout_sec": 3600,
    "max_timeout_sec": 7200,
    "model": "swe-2",
    "repos": [],
}

JOB_ID_RE = re.compile(r"[a-z0-9-]{1,64}")
REPO_RE = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
# SWE-2 family only; paid "-lightning" variants are rejected separately.
SWE2_RE = re.compile(r"swe-2(?:-[a-z0-9]+)*")

GRACE_SEC = 30
WORK_KEEP_SEC = 3 * 24 * 3600
LOG_KEEP_SEC = 14 * 24 * 3600

REDACTIONS = tuple(
    re.compile(pattern)
    for pattern in (
        r"cog_[A-Za-z0-9]+",
        r"gh[pousr]_[A-Za-z0-9]{20,}",
        r"github_pat_\w+",
        r"AIza[0-9A-Za-z_-]{35}",
        r"sk-[A-Za-z0-9_-]{20,}",
        r"Bearer \S+",
        r"xox[abp]-\S+",
    )
)

QUOTA_MARKERS = (
    ("out_of_quota", re.compile(r"out_of_quota", re.IGNORECASE)),
    ("usage_limit_exceeded", re.compile(r"usage_limit_exceeded", re.IGNORECASE)),
    (
        "total_session_limit_exceeded",
        re.compile(r"total_session_limit_exceeded", re.IGNORECASE),
    ),
    ("insufficient_credits", re.compile(r"insufficient credits", re.IGNORECASE)),
    (
        "payment_required",
        re.compile(r"\b402\b|payment required", re.IGNORECASE),
    ),
)


def redact(text: str) -> str:
    for pattern in REDACTIONS:
        text = pattern.sub("[REDACTED]", text)
    return text


def quota_reason(output: str) -> Optional[str]:
    for reason, pattern in QUOTA_MARKERS:
        if pattern.search(output):
            return reason
    return None


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


@dataclass(frozen=True)
class CmdResult:
    returncode: int
    output: str
    timed_out: bool = False


# Signature shared by the real runner and test fakes. argv is a sequence of
# strings; cwd is a directory or None; timeout_sec is a wall-clock limit or
# None for no limit. Output is stdout and stderr combined.
Run = Callable[[Sequence[str], Optional[str], Optional[int]], CmdResult]


def default_run(
    argv: Sequence[str],
    cwd: Optional[str] = None,
    timeout_sec: Optional[int] = None,
) -> CmdResult:
    proc = subprocess.Popen(
        [str(a) for a in argv],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        start_new_session=True,
    )
    timed_out = False
    try:
        out, _ = proc.communicate(timeout=timeout_sec)
    except subprocess.TimeoutExpired:
        timed_out = True
        _kill_group(proc, signal.SIGTERM)
        try:
            out, _ = proc.communicate(timeout=GRACE_SEC)
        except subprocess.TimeoutExpired:
            _kill_group(proc, signal.SIGKILL)
            out, _ = proc.communicate()
    return CmdResult(proc.returncode or 0, out or "", timed_out)


def _kill_group(proc: subprocess.Popen, sig: int) -> None:
    try:
        # start_new_session=True makes the child a session leader, so its
        # process group id equals its pid.
        os.killpg(proc.pid, sig)
    except (ProcessLookupError, PermissionError):
        pass


def remote_branch_check(job: dict, run: Run) -> list:
    """Remote branch invariants, checked via git ls-remote.

    Kept behind this function so local validation can be tested offline.
    """
    url = "https://github.com/{}.git".format(job["repo"])
    errors = []
    base = run(("git", "ls-remote", "--heads", url, job["base_branch"]))
    if base.returncode != 0 or not base.output.strip():
        errors.append("base_branch not on origin: {}".format(job["base_branch"]))
    branch = run(("git", "ls-remote", "--heads", url, job["branch"]))
    branch_exists = branch.returncode == 0 and bool(branch.output.strip())
    if branch_exists and not job.get("continue_branch"):
        errors.append("branch already on origin: {}".format(job["branch"]))
    if job.get("continue_branch") and not branch_exists:
        errors.append(
            "continue_branch set but branch not on origin: {}".format(job["branch"])
        )
    return errors


def _iso_with_offset(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.fromisoformat(
            value[:-1] + "+00:00" if value.endswith("Z") else value
        )
    except ValueError:
        return False
    return parsed.tzinfo is not None


def model_allowed(model: object) -> bool:
    return (
        isinstance(model, str)
        and bool(SWE2_RE.fullmatch(model))
        and "lightning" not in model
    )


def validate_job(data: object, config: dict) -> list:
    """Local-only job validation. Returns a list of human-readable errors."""
    if not isinstance(data, dict):
        return ["job file is not a JSON object"]
    errors = []
    if data.get("schema") != 1:
        errors.append("schema must be 1")
    job_id = data.get("job_id")
    if not isinstance(job_id, str) or not JOB_ID_RE.fullmatch(job_id):
        errors.append("job_id must match [a-z0-9-]{1,64}")
    if not isinstance(data.get("task_id"), str) or not data["task_id"].strip():
        errors.append("task_id is required")
    repo = data.get("repo")
    if not isinstance(repo, str) or not REPO_RE.fullmatch(repo):
        errors.append("repo must look like owner/name")
    elif repo not in config.get("repos", []):
        errors.append("repo not in config.json repos: {}".format(repo))
    if not isinstance(data.get("base_branch"), str) or not data["base_branch"]:
        errors.append("base_branch is required")
    if not isinstance(data.get("branch"), str) or not data["branch"]:
        errors.append("branch is required")
    if not isinstance(data.get("continue_branch", False), bool):
        errors.append("continue_branch must be a bool")
    if not isinstance(data.get("prompt"), str) or not data["prompt"].strip():
        errors.append("prompt is required")
    model = data.get("model", config.get("model"))
    if not model_allowed(model):
        errors.append("model must be in the SWE-2 family: {!r}".format(model))
    timeout = data.get("timeout_sec", config.get("default_timeout_sec"))
    if (
        type(timeout) is not int
        or timeout <= 0
        or timeout > config.get("max_timeout_sec", DEFAULT_CONFIG["max_timeout_sec"])
    ):
        errors.append(
            "timeout_sec must be 1..{}".format(
                config.get("max_timeout_sec", DEFAULT_CONFIG["max_timeout_sec"])
            )
        )
    pr = data.get("pr")
    if not isinstance(pr, dict):
        errors.append("pr object is required")
    else:
        if pr.get("draft") is not True:
            errors.append("pr.draft must be true")
        if not isinstance(pr.get("title"), str) or not pr["title"].strip():
            errors.append("pr.title is required")
        if not isinstance(pr.get("base"), str) or not pr["base"]:
            errors.append("pr.base is required")
    if not isinstance(data.get("submitted_by"), str) or not data["submitted_by"]:
        errors.append("submitted_by is required")
    if not _iso_with_offset(data.get("submitted_at")):
        errors.append("submitted_at must be ISO 8601 with an offset")
    return errors


def _safe_mtime(path: Path) -> float:
    try:
        return path.stat().st_mtime
    except OSError:
        return float("inf")


class Queue:
    def __init__(self, root: Path):
        self.root = Path(root)

    def d(self, name: str) -> Path:
        return self.root / name

    def config(self) -> dict:
        cfg = dict(DEFAULT_CONFIG)
        try:
            loaded = json.loads((self.root / "config.json").read_text())
        except FileNotFoundError:
            loaded = {}
        if isinstance(loaded, dict):
            cfg.update(loaded)
        return cfg

    def paused(self) -> bool:
        return (self.root / "PAUSE").exists()

    def status_state(self) -> str:
        try:
            data = json.loads((self.root / "STATUS.json").read_text())
        except FileNotFoundError:
            return "ok"
        except (OSError, ValueError):
            return "stopped_error"
        if not isinstance(data, dict):
            return "stopped_error"
        return str(data.get("state", "ok"))

    def stop(self, state: str, reason: str, job_id: Optional[str]) -> None:
        payload = {"state": state, "reason": reason, "at": now_iso()}
        if job_id:
            payload["job_id"] = job_id
        (self.root / "STATUS.json").write_text(
            json.dumps(payload, indent=2) + "\n", encoding="utf-8"
        )
        (self.root / "PAUSE").touch()

    def _job_files(self, dirname: str) -> list:
        return sorted(
            p
            for p in self.d(dirname).glob("*.json")
            if not p.name.startswith(".") and not p.name.endswith(RESULT_SUFFIX)
        )

    def running_count(self) -> int:
        return len(self._job_files("running"))

    def init(self) -> None:
        self.root.mkdir(mode=0o700, parents=True, exist_ok=True)
        os.chmod(self.root, 0o700)
        for name in DIRS:
            path = self.d(name)
            path.mkdir(exist_ok=True)
            os.chmod(path, 0o700)
        config = self.root / "config.json"
        if not config.exists():
            config.write_text(
                json.dumps(DEFAULT_CONFIG, indent=2) + "\n", encoding="utf-8"
            )
        status = self.root / "STATUS.json"
        if not status.exists():
            status.write_text(json.dumps({"state": "ok"}) + "\n", encoding="utf-8")

    def submit(self, data: object) -> Path:
        errors = validate_job(data, self.config())
        if errors:
            raise ValueError("invalid job: " + "; ".join(errors))
        job_id = data["job_id"]
        for dirname in ("inbox", "running", "done", "failed"):
            if (self.d(dirname) / (job_id + ".json")).exists():
                raise ValueError("job_id already used: " + job_id)
        tmp = self.d("inbox") / ("." + job_id + ".tmp")
        tmp.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        dst = self.d("inbox") / (job_id + ".json")
        os.rename(tmp, dst)
        return dst

    def claim_next(self) -> Optional[Path]:
        """Pick the oldest inbox job and rename it into running/, under flock.

        Returns the claimed path in running/, or None. A rename that loses a
        race (another runner took it first) just moves to the next candidate.
        """
        with open(self.root / ".lock", "a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            try:
                candidates = sorted(
                    self._job_files("inbox"),
                    key=lambda p: (_safe_mtime(p), p.name),
                )
                for src in candidates:
                    dst = self.d("running") / src.name
                    try:
                        os.rename(src, dst)
                    except OSError:
                        continue
                    return dst
                return None
            finally:
                fcntl.flock(lock, fcntl.LOCK_UN)

    def prune(self, now: Optional[float] = None) -> None:
        now = time.time() if now is None else now
        for path in self.d("work").iterdir():
            if path.is_dir() and now - path.stat().st_mtime > WORK_KEEP_SEC:
                shutil.rmtree(path, ignore_errors=True)
        for path in self.d("logs").glob("*.log"):
            try:
                stale = now - path.stat().st_mtime > LOG_KEEP_SEC
            except OSError:
                continue
            if stale:
                path.unlink()


def _write_result(
    queue: Queue,
    job: dict,
    claimed: Path,
    *,
    state: str,
    reason: str,
    detail: Optional[str] = None,
    pr_url: Optional[str] = None,
    head_sha: Optional[str] = None,
    started_at: Optional[str] = None,
    exit_code: Optional[int] = None,
    log_rel: Optional[str] = None,
) -> None:
    job_id = str(job.get("job_id") or claimed.stem)
    result = {
        "job_id": job_id,
        "state": state,
        "reason": reason,
        "pr_url": pr_url,
        "branch": job.get("branch"),
        "head_sha": head_sha,
        "started_at": started_at,
        "ended_at": now_iso(),
        "exit_code": exit_code,
        "model": job.get("model"),
        "usage": None,
        "log": log_rel,
    }
    if detail:
        result["detail"] = detail
    dest = queue.d("done" if state == "done" else "failed")
    dest.mkdir(exist_ok=True)
    (dest / (job_id + RESULT_SUFFIX)).write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    try:
        os.rename(claimed, dest / (job_id + ".json"))
    except OSError:
        pass


def _finish_failed(
    queue: Queue,
    job: dict,
    claimed: Path,
    reason: str,
    detail: str,
    **kwargs,
) -> None:
    _write_result(
        queue, job, claimed, state="failed", reason=reason, detail=detail, **kwargs
    )


def _pr_url(repo: str, branch: str, run: Run, child) -> Optional[str]:
    res = run(("gh", "pr", "list", "--repo", repo, "--head", branch, "--json", "url"))
    child(res)
    if res.returncode != 0:
        return None
    try:
        items = json.loads(res.output)
    except ValueError:
        return None
    if isinstance(items, list) and items and isinstance(items[0], dict):
        url = items[0].get("url")
        return url if isinstance(url, str) and url else None
    return None


def execute_job(queue: Queue, job: dict, claimed: Path, run: Run, config: dict) -> None:
    job_id = job["job_id"]
    repo = job["repo"]
    branch = job["branch"]
    workdir = queue.d("work") / job_id
    log_rel = "logs/{}.log".format(job_id)
    started_at = now_iso()
    workdir.mkdir(parents=True, exist_ok=True)
    log_fh = open(queue.d("logs") / (job_id + ".log"), "a", encoding="utf-8")

    def note(line: str) -> None:
        log_fh.write(line.rstrip("\n") + "\n")
        log_fh.flush()

    def child(res: CmdResult) -> None:
        if res.output:
            log_fh.write(redact(res.output))
            if not res.output.endswith("\n"):
                log_fh.write("\n")
            log_fh.flush()

    def failed(reason: str, detail: str, **kwargs) -> None:
        _finish_failed(
            queue,
            job,
            claimed,
            reason,
            detail,
            started_at=started_at,
            log_rel=log_rel,
            **kwargs,
        )

    try:
        note(
            "[runner] {} start job={} repo={} branch={}".format(
                started_at, job_id, repo, branch
            )
        )
        clone_branch = branch if job.get("continue_branch") else job["base_branch"]
        res = run(
            (
                "git",
                "clone",
                "--branch",
                clone_branch,
                "https://github.com/{}.git".format(repo),
                str(workdir),
            ),
            timeout_sec=600,
        )
        child(res)
        if res.returncode != 0:
            failed("error", "git clone failed (rc={})".format(res.returncode))
            return
        if not job.get("continue_branch"):
            res = run(("git", "-C", str(workdir), "switch", "-c", branch))
            child(res)
            if res.returncode != 0:
                failed("error", "git switch -c failed (rc={})".format(res.returncode))
                return
        prompt_path = workdir / "prompt.txt"
        prompt_path.write_text(job["prompt"], encoding="utf-8")
        atif = workdir / "session.atif"
        model = job.get("model") or config.get("model")
        timeout = int(job.get("timeout_sec") or config["default_timeout_sec"])
        res = run(
            (
                "devin",
                "-p",
                "--prompt-file",
                str(prompt_path),
                "--model",
                str(model),
                "--permission-mode",
                "dangerous",
                "--respect-workspace-trust",
                "false",
                "--export",
                str(atif),
                # NOTE: no --sandbox. In CLI 3000.11.1 --sandbox forces the
                # autonomous permission mode, which rejects tool calls and
                # stalls a headless -p session.
            ),
            cwd=str(workdir),
            timeout_sec=timeout,
        )
        child(res)
        if atif.exists():
            os.chmod(atif, 0o600)
        reason = quota_reason(redact(res.output))
        if reason:
            note("[runner] quota stop: {}".format(reason))
            failed(reason, "quota or billing marker in CLI output")
            queue.stop("stopped_quota", reason, job_id)
            return
        if res.timed_out:
            failed("timeout", "exceeded timeout_sec={}".format(timeout))
            return
        if res.returncode != 0:
            failed(
                "error",
                "devin exited rc={}".format(res.returncode),
                exit_code=res.returncode,
            )
            return
        head = run(("git", "-C", str(workdir), "rev-parse", "HEAD"))
        head_sha = head.output.strip() if head.returncode == 0 else None
        ahead_res = run(
            (
                "git",
                "-C",
                str(workdir),
                "rev-list",
                "--count",
                "origin/{}..HEAD".format(job["base_branch"]),
            )
        )
        try:
            ahead = int(ahead_res.output.strip()) if ahead_res.returncode == 0 else 0
        except ValueError:
            ahead = 0
        pr_url = _pr_url(repo, branch, run, child)
        if not pr_url and ahead > 0:
            push = run(("git", "-C", str(workdir), "push", "-u", "origin", branch))
            child(push)
            if push.returncode == 0:
                created = run(
                    (
                        "gh",
                        "pr",
                        "create",
                        "--repo",
                        repo,
                        "--draft",
                        "--fill",
                        "--base",
                        job["pr"]["base"],
                        "--head",
                        branch,
                    )
                )
                child(created)
                pr_url = _pr_url(repo, branch, run, child)
        if pr_url:
            note("[runner] done pr={}".format(pr_url))
            _write_result(
                queue,
                job,
                claimed,
                state="done",
                reason="ok",
                pr_url=pr_url,
                head_sha=head_sha,
                started_at=started_at,
                exit_code=res.returncode,
                log_rel=log_rel,
            )
            shutil.rmtree(workdir, ignore_errors=True)
        elif ahead == 0:
            failed("no_changes", "no PR and no new commits", head_sha=head_sha)
        else:
            failed(
                "error",
                "new commits but no PR could be opened",
                head_sha=head_sha,
            )
    finally:
        log_fh.close()


def run_once(
    queue: Queue,
    *,
    run: Run = default_run,
    remote_check: Callable[[dict, Run], list] = remote_branch_check,
) -> int:
    if queue.paused():
        print("run-once: PAUSE present, nothing claimed")
        return 0
    if queue.status_state() != "ok":
        print("run-once: STATUS is {}, nothing claimed".format(queue.status_state()))
        return 0
    config = queue.config()
    if queue.running_count() >= int(config["max_concurrency"]):
        print("run-once: max_concurrency reached, nothing claimed")
        return 0
    claimed = queue.claim_next()
    if claimed is None:
        print("run-once: inbox empty")
        return 0
    job_id = claimed.stem
    try:
        job = json.loads(claimed.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        _finish_failed(
            queue,
            {"job_id": job_id},
            claimed,
            "invalid_job",
            "unreadable job file: {}".format(exc),
        )
        return 0
    errors = validate_job(job, config)
    if not errors:
        auth = run(("devin", "auth", "status"))
        if auth.returncode != 0:
            try:
                os.rename(claimed, queue.d("inbox") / claimed.name)
            except OSError:
                pass
            queue.stop("stopped_auth", "devin auth status failed", job_id)
            print("run-once: devin not authenticated, job returned to inbox")
            return 0
        if remote_check is not None:
            errors = remote_check(job, run)
    if errors:
        _finish_failed(
            queue, job, claimed, "invalid_job", "; ".join(str(e) for e in errors)
        )
        return 0
    print("run-once: claimed {}".format(job_id))
    execute_job(queue, job, claimed, run, config)
    queue.prune()
    return 0


def print_status(queue: Queue, out) -> None:
    status_path = queue.root / "STATUS.json"
    try:
        out.write("STATUS.json: " + status_path.read_text().strip() + "\n")
    except OSError:
        out.write("STATUS.json: (missing)\n")
    out.write("PAUSE: {}\n".format("present" if queue.paused() else "absent"))
    for name in ("inbox", "running", "done", "failed", "work", "logs"):
        path = queue.d(name)
        count = len(list(path.iterdir())) if path.is_dir() else 0
        out.write("{}: {}\n".format(name, count))


def resume(queue: Queue) -> None:
    try:
        (queue.root / "PAUSE").unlink()
    except FileNotFoundError:
        pass
    (queue.root / "STATUS.json").write_text(
        json.dumps({"state": "ok", "at": now_iso()}) + "\n", encoding="utf-8"
    )


def resolve_root(flag: Optional[str]) -> Path:
    raw = flag or os.environ.get(ENV_ROOT) or str(DEFAULT_ROOT)
    return Path(raw).expanduser()


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="devin-queue", description=__doc__)
    parser.add_argument(
        "--root",
        default=None,
        help="queue root (default $DEVIN_QUEUE_ROOT or ~/devin-queue)",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init", help="create the queue layout and default config")
    sp = sub.add_parser("submit", help="submit a job JSON file to inbox/")
    sp.add_argument("job_json", help="path to the job JSON file")
    sub.add_parser("run-once", help="claim and run at most one job")
    sub.add_parser("status", help="print STATUS.json, PAUSE, and dir counts")
    sub.add_parser("resume", help="remove PAUSE and reset STATUS to ok")
    sub.add_parser("redact", help="redact stdin to stdout")
    args = parser.parse_args(argv)

    if args.command == "redact":
        sys.stdout.write(redact(sys.stdin.read()))
        return 0

    queue = Queue(resolve_root(args.root))
    if args.command == "init":
        queue.init()
        print("initialized {}".format(queue.root))
        return 0
    if args.command == "submit":
        try:
            data = json.loads(Path(args.job_json).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            print("submit: cannot read job file: {}".format(exc), file=sys.stderr)
            return 1
        try:
            dst = queue.submit(data)
        except ValueError as exc:
            print("submit: {}".format(exc), file=sys.stderr)
            return 1
        print("submitted {}".format(dst.name))
        return 0
    if args.command == "run-once":
        queue.init()
        return run_once(queue)
    if args.command == "status":
        print_status(queue, sys.stdout)
        return 0
    if args.command == "resume":
        resume(queue)
        print("resumed")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
