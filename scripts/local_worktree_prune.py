#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal, Mapping, Sequence, TextIO

Action = Literal["keep", "remove"]
JobState = Literal["live", "keep", "abandoned"]

LOCK_FILE_NAME = ".worktree-prune-keep"
DEFAULT_JOBS_NAME = ".worktree-prune-jobs.json"
_BANNED_GIT = tuple(
    " ".join(parts)
    for parts in (
        ("push", "--delete"),
        ("branch", "-d"),
        ("branch", "-D"),
        ("branch", "--delete"),
    )
)
_CHECK_PENDING = frozenset(
    {"PENDING", "QUEUED", "IN_PROGRESS", "WAITING", "REQUESTED", "EXPECTED"}
)


@dataclass(frozen=True)
class WorktreeFact:
    path: str
    is_primary: bool
    is_added: bool
    pr_open_or_ci: bool
    live_process: bool
    dirty: bool
    unique_only_here: bool
    branch_unmerged: bool
    live_job_names_path: bool
    locked: bool
    pr_merged: bool
    job_abandoned_clean: bool
    job_force: bool


@dataclass(frozen=True)
class Verdict:
    action: Action
    reasons: tuple[str, ...]
    force: bool


@dataclass(frozen=True)
class WorktreeRow:
    path: str
    head: str
    branch: str | None
    git_locked: bool
    is_primary: bool


@dataclass(frozen=True)
class Job:
    name: str
    path: str
    state: JobState
    force: bool


@dataclass(frozen=True)
class PrLookup:
    unknown: bool = False
    open_or_ci: bool = False
    merged: bool = False


@dataclass(frozen=True)
class Probes:
    process_cwds: tuple[str, ...] | None = None
    process_scan_failed: bool = False
    pr_by_branch: Mapping[str, PrLookup] | None = None


@dataclass(frozen=True)
class TreeSignals:
    uncommitted: bool
    unique_only_here: bool
    branch_unmerged: bool
    pr_open_or_ci: bool
    pr_merged: bool
    live_process: bool
    lock_file: bool
    git_locked: bool
    job_live: bool
    job_keep: bool
    job_abandoned: bool
    job_force: bool


ApplyRun = Callable[[Sequence[str]], int]

_KEEP_LIVE: tuple[tuple[str, Callable[[WorktreeFact], bool]], ...] = (
    ("primary", lambda f: f.is_primary),
    ("pr_open_or_ci", lambda f: f.pr_open_or_ci),
    ("live_process", lambda f: f.live_process),
    ("dirty", lambda f: f.dirty),
    ("unmerged_live_job", lambda f: f.branch_unmerged and f.live_job_names_path),
    ("locked", lambda f: f.locked),
)

_REMOVE_OK: tuple[tuple[str, Callable[[WorktreeFact], bool]], ...] = (
    ("is_added", lambda f: f.is_added),
    (
        "pr_merged_or_abandoned",
        lambda f: f.pr_merged or f.job_abandoned_clean,
    ),
    ("not_live_process", lambda f: not f.live_process),
    (
        "not_dirty_or_unique",
        lambda f: not f.dirty and not f.unique_only_here,
    ),
    ("not_live_job", lambda f: not f.live_job_names_path),
    ("not_locked", lambda f: not f.locked),
)


def decide(fact: WorktreeFact) -> Verdict:
    keep_hits = tuple(name for name, pred in _KEEP_LIVE if pred(fact))
    remove_misses = tuple(
        f"remove_ok_miss:{name}" for name, pred in _REMOVE_OK if not pred(fact)
    )
    if keep_hits or remove_misses:
        reasons = tuple(dict.fromkeys((*keep_hits, *remove_misses)))
        return Verdict(action="keep", reasons=reasons, force=False)
    return Verdict(action="remove", reasons=("remove_ok",), force=bool(fact.job_force))


def _ban_check(cmd: Sequence[str]) -> tuple[str, ...]:
    out = tuple(cmd)
    joined = " ".join(out)
    for banned in _BANNED_GIT:
        if banned in joined:
            raise RuntimeError(f"refusing git command that deletes a branch: {joined}")
    return out


def planned_commands(
    repo: str, pairs: Sequence[tuple[WorktreeFact, Verdict]]
) -> tuple[tuple[str, ...], ...]:
    cmds: list[tuple[str, ...]] = []
    for fact, verdict in pairs:
        if fact.is_primary or verdict.action != "remove":
            continue
        argv: list[str] = ["git", "-C", repo, "worktree", "remove"]
        if verdict.force:
            argv.append("--force")
        argv.append(fact.path)
        cmds.append(_ban_check(argv))
    if cmds:
        cmds.append(_ban_check(("git", "-C", repo, "worktree", "prune")))
    return tuple(cmds)


def parse_worktree_porcelain(text: str) -> tuple[WorktreeRow, ...]:
    rows: list[WorktreeRow] = []
    path = ""
    head = ""
    branch: str | None = None
    git_locked = False
    seen_worktree = False

    def flush() -> None:
        nonlocal path, head, branch, git_locked, seen_worktree
        if not seen_worktree or not path:
            path = ""
            head = ""
            branch = None
            git_locked = False
            seen_worktree = False
            return
        rows.append(
            WorktreeRow(
                path=path,
                head=head,
                branch=branch,
                git_locked=git_locked,
                is_primary=not rows,
            )
        )
        path = ""
        head = ""
        branch = None
        git_locked = False
        seen_worktree = False

    for line in text.splitlines():
        if line == "":
            flush()
            continue
        if line.startswith("worktree "):
            if seen_worktree:
                flush()
            seen_worktree = True
            path = line[len("worktree ") :]
        elif line.startswith("HEAD "):
            head = line[len("HEAD ") :]
        elif line.startswith("branch "):
            branch = line[len("branch ") :]
        elif line == "detached":
            branch = None
        elif line == "locked" or line.startswith("locked "):
            git_locked = True
    flush()
    return tuple(rows)


def _branch_name(ref: str | None) -> str | None:
    if not ref:
        return None
    prefix = "refs/heads/"
    if ref.startswith(prefix):
        return ref[len(prefix) :]
    if ref.startswith("refs/"):
        return None
    return ref


def _resolve_job_path(repo: Path, raw: str) -> str:
    candidate = Path(raw)
    if candidate.is_absolute():
        return str(candidate.resolve())
    return str((repo / candidate).resolve())


def parse_jobs_document(data: object, repo: Path) -> tuple[Job, ...]:
    if not isinstance(data, dict):
        raise ValueError("jobs root must be an object")
    raw_jobs = data.get("jobs", [])
    if not isinstance(raw_jobs, list):
        raise ValueError("jobs must be an array")
    jobs: list[Job] = []
    for item in raw_jobs:
        if not isinstance(item, dict):
            raise ValueError("each job must be an object")
        path = item.get("path")
        if not isinstance(path, str) or not path:
            raise ValueError("job path is required")
        state_raw = item.get("state", "live")
        if state_raw not in {"live", "keep", "abandoned"}:
            state: JobState = "live"
        else:
            state = state_raw
        name = item.get("name", "")
        if name is None:
            name = ""
        if not isinstance(name, str):
            name = str(name)
        jobs.append(
            Job(
                name=name,
                path=_resolve_job_path(repo, path),
                state=state,
                force=bool(item.get("force", False)),
            )
        )
    return tuple(jobs)


def load_jobs_file(path: Path, repo: Path) -> tuple[Job, ...]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return parse_jobs_document(data, repo)


def _jobs_for(path: str, jobs: Sequence[Job]) -> tuple[bool, bool, bool, bool]:
    target = Path(path).resolve()
    live = keep = abandoned = force = False
    for job in jobs:
        if Path(job.path).resolve() != target:
            continue
        if job.state == "live":
            live = True
        elif job.state == "keep":
            keep = True
        elif job.state == "abandoned":
            abandoned = True
        if job.force:
            force = True
    return live, keep, abandoned, force


def fact_from_signals(row: WorktreeRow, signals: TreeSignals) -> WorktreeFact:
    dirty = signals.uncommitted or signals.unique_only_here
    locked = signals.lock_file or signals.git_locked or signals.job_keep
    abandoned_clean = (
        signals.job_abandoned and not dirty and not signals.unique_only_here
    )
    return WorktreeFact(
        path=row.path,
        is_primary=row.is_primary,
        is_added=not row.is_primary,
        pr_open_or_ci=signals.pr_open_or_ci,
        live_process=signals.live_process,
        dirty=dirty,
        unique_only_here=signals.unique_only_here,
        branch_unmerged=signals.branch_unmerged,
        live_job_names_path=signals.job_live,
        locked=locked,
        pr_merged=signals.pr_merged,
        job_abandoned_clean=abandoned_clean,
        job_force=signals.job_force,
    )


def _run_git(args: Sequence[str], *, cwd: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def _scan_proc_cwds() -> tuple[str, ...] | None:
    proc = Path("/proc")
    if not proc.is_dir():
        return None
    found: list[str] = []
    try:
        entries = list(proc.iterdir())
    except OSError:
        return None
    for entry in entries:
        if not entry.name.isdigit():
            continue
        try:
            found.append(os.readlink(entry / "cwd"))
        except OSError:
            continue
    return tuple(found)


def _scan_lsof_cwds() -> tuple[str, ...] | None:
    lsof = shutil.which("lsof")
    if not lsof:
        return None
    completed = subprocess.run(
        [lsof, "-a", "-d", "cwd", "-Fn"],
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        return None
    found: list[str] = []
    for line in completed.stdout.splitlines():
        if line.startswith("n/") or line.startswith("n~"):
            found.append(line[1:])
    return tuple(found)


def scan_process_cwds() -> tuple[str, ...] | None:
    proc = _scan_proc_cwds()
    if proc is not None:
        return proc
    return _scan_lsof_cwds()


def path_has_live_process(tree: str, cwds: tuple[str, ...] | None) -> bool:
    if cwds is None:
        return True
    try:
        tree_r = os.path.realpath(tree)
    except OSError:
        return True
    prefix = tree_r + os.sep
    for cwd in cwds:
        try:
            cwd_r = os.path.realpath(cwd)
        except OSError:
            continue
        if cwd_r == tree_r or cwd_r.startswith(prefix):
            return True
    return False


def _pr_from_items(items: object) -> PrLookup:
    if not isinstance(items, list):
        return PrLookup(unknown=True)
    open_or_ci = False
    merged = False
    for item in items:
        if not isinstance(item, dict):
            return PrLookup(unknown=True)
        state = str(item.get("state") or "").upper()
        if state == "OPEN":
            open_or_ci = True
        elif state == "MERGED":
            merged = True
        rollup = item.get("statusCheckRollup") or []
        if not isinstance(rollup, list):
            return PrLookup(unknown=True)
        for check in rollup:
            if not isinstance(check, dict):
                continue
            status = str(check.get("status") or "").upper()
            if status in _CHECK_PENDING:
                open_or_ci = True
    return PrLookup(unknown=False, open_or_ci=open_or_ci, merged=merged)


def lookup_pr_with_gh(branch: str | None, *, cwd: str) -> PrLookup:
    if not branch:
        return PrLookup(unknown=True)
    if shutil.which("gh") is None:
        return PrLookup(unknown=True)
    completed = subprocess.run(
        [
            "gh",
            "pr",
            "list",
            "--head",
            branch,
            # gh pr list defaults to open, so merged heads would never classify.
            "--state",
            "all",
            "--json",
            "number,state,statusCheckRollup",
            "--limit",
            "20",
        ],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        return PrLookup(unknown=True)
    try:
        items = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return PrLookup(unknown=True)
    return _pr_from_items(items)


def _uncommitted(path: str) -> bool | None:
    completed = _run_git(("status", "--porcelain"), cwd=path)
    if completed.returncode != 0:
        return None
    return bool(completed.stdout.strip())


def _unique_only_here(path: str) -> bool | None:
    upstream = _run_git(
        ("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"),
        cwd=path,
    )
    if upstream.returncode == 0 and upstream.stdout.strip():
        unique = _run_git(("rev-list", "--max-count=1", "@{u}..HEAD"), cwd=path)
        if unique.returncode != 0:
            return None
        return bool(unique.stdout.strip())
    unique = _run_git(("rev-list", "--max-count=1", "HEAD", "--not", "--remotes"), cwd=path)
    if unique.returncode != 0:
        return None
    return bool(unique.stdout.strip())


def _branch_unmerged(primary_path: str, head: str) -> bool | None:
    target = head if head else "HEAD"
    completed = _run_git(("merge-base", "--is-ancestor", target, "HEAD"), cwd=primary_path)
    if completed.returncode == 0:
        return False
    if completed.returncode == 1:
        return True
    return None


def _lock_file_present(path: str) -> bool:
    return (Path(path) / LOCK_FILE_NAME).is_file()


def _resolve_pr(branch: str | None, probes: Probes, *, cwd: str) -> PrLookup:
    if probes.pr_by_branch is not None:
        if not branch:
            return PrLookup(unknown=False, open_or_ci=False, merged=False)
        return probes.pr_by_branch.get(
            branch, PrLookup(unknown=False, open_or_ci=False, merged=False)
        )
    return lookup_pr_with_gh(branch, cwd=cwd)


def _resolve_cwds(probes: Probes) -> tuple[str, ...] | None:
    if probes.process_scan_failed:
        return None
    if probes.process_cwds is not None:
        return probes.process_cwds
    return scan_process_cwds()


def collect_facts(
    repo: str,
    *,
    jobs: Sequence[Job] = (),
    probes: Probes | None = None,
) -> tuple[WorktreeFact, ...]:
    used = probes if probes is not None else Probes()
    listed = _run_git(("worktree", "list", "--porcelain"), cwd=repo)
    if listed.returncode != 0:
        raise RuntimeError(listed.stderr.strip() or "git worktree list failed")
    rows = parse_worktree_porcelain(listed.stdout)
    if not rows:
        return ()
    primary_path = rows[0].path
    cwds = _resolve_cwds(used)
    facts: list[WorktreeFact] = []
    for row in rows:
        uncommitted = _uncommitted(row.path)
        unique = _unique_only_here(row.path)
        if uncommitted is None or unique is None:
            uncommitted = True if uncommitted is None else uncommitted
            unique = True if unique is None else unique
        unmerged = _branch_unmerged(primary_path, row.head)
        if unmerged is None:
            unmerged = True
        branch = _branch_name(row.branch)
        pr = _resolve_pr(branch, used, cwd=primary_path)
        if pr.unknown:
            pr_open_or_ci = True
            pr_merged = False
        else:
            pr_open_or_ci = pr.open_or_ci
            pr_merged = pr.merged
        job_live, job_keep, job_abandoned, job_force = _jobs_for(row.path, jobs)
        signals = TreeSignals(
            uncommitted=uncommitted,
            unique_only_here=unique,
            branch_unmerged=unmerged,
            pr_open_or_ci=pr_open_or_ci,
            pr_merged=pr_merged,
            live_process=path_has_live_process(row.path, cwds),
            lock_file=_lock_file_present(row.path),
            git_locked=row.git_locked,
            job_live=job_live,
            job_keep=job_keep,
            job_abandoned=job_abandoned,
            job_force=job_force,
        )
        facts.append(fact_from_signals(row, signals))
    return tuple(facts)


def apply_planned(
    repo: str,
    pairs: Sequence[tuple[WorktreeFact, Verdict]],
    run: ApplyRun,
) -> int:
    rc = 0
    for cmd in planned_commands(repo, pairs):
        got = run(cmd)
        if got != 0:
            rc = got
    return rc


def _default_apply_run(argv: Sequence[str]) -> int:
    completed = subprocess.run(list(argv), capture_output=True, text=True)
    return completed.returncode


def _load_jobs_for_cli(jobs_flag: str | None, primary: Path) -> tuple[Job, ...]:
    if jobs_flag:
        path = Path(jobs_flag)
        if not path.is_file():
            raise FileNotFoundError(f"--jobs file not found: {jobs_flag}")
        return load_jobs_file(path, primary)
    default = primary / DEFAULT_JOBS_NAME
    if not default.is_file():
        return ()
    return load_jobs_file(default, primary)


def _print_human(
    pairs: Sequence[tuple[WorktreeFact, Verdict]],
    *,
    dry_run: bool,
    out: TextIO,
    planned: Sequence[Sequence[str]],
) -> None:
    for fact, verdict in pairs:
        mark = "KEEP" if verdict.action == "keep" else "REMOVE"
        extra = " (primary)" if fact.is_primary else ""
        out.write(f"{mark}  {fact.path}{extra}\n")
        for reason in verdict.reasons:
            out.write(f"  {reason}\n")
        if verdict.force:
            out.write("  force\n")
    if dry_run:
        out.write("Dry-run: nothing will be removed.\n")
        out.write("Would run git worktree prune for stale metadata on --apply.\n")
        return
    if planned:
        out.write("Applied:\n")
        for cmd in planned:
            out.write("  " + " ".join(cmd) + "\n")
    else:
        out.write("Nothing removed.\n")


def _print_json(
    pairs: Sequence[tuple[WorktreeFact, Verdict]],
    *,
    dry_run: bool,
    out: TextIO,
    planned: Sequence[Sequence[str]],
) -> None:
    payload = {
        "dry_run": dry_run,
        "nothing_removed": dry_run or not any(
            v.action == "remove" and not f.is_primary for f, v in pairs
        ),
        "verdicts": [
            {
                "path": fact.path,
                "action": verdict.action,
                "reasons": list(verdict.reasons),
                "force": verdict.force,
                "is_primary": fact.is_primary,
            }
            for fact, verdict in pairs
        ],
        "planned": [list(cmd) for cmd in planned],
    }
    json.dump(payload, out, indent=2, ensure_ascii=True)
    out.write("\n")


def run(
    argv: Sequence[str] | None = None,
    *,
    apply_run: ApplyRun | None = None,
    probes: Probes | None = None,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    parser = argparse.ArgumentParser(
        description="Classify local git worktrees as keep or remove."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="remove allowed added worktrees, then git worktree prune",
    )
    parser.add_argument("--repo", default=".", help="git repo or primary checkout")
    parser.add_argument("--jobs", default=None, help="JSON jobs file")
    parser.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="machine-readable verdicts",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    out = stdout if stdout is not None else sys.stdout
    err = stderr if stderr is not None else sys.stderr
    repo = str(Path(args.repo).resolve())
    try:
        listed = _run_git(("worktree", "list", "--porcelain"), cwd=repo)
        if listed.returncode != 0:
            err.write(listed.stderr or "git worktree list failed\n")
            return 1
        rows = parse_worktree_porcelain(listed.stdout)
        if not rows:
            err.write("no worktrees found\n")
            return 1
        primary = Path(rows[0].path)
        jobs = _load_jobs_for_cli(args.jobs, primary)
        facts = collect_facts(repo, jobs=jobs, probes=probes)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        err.write(f"{exc}\n")
        return 1
    pairs = tuple((fact, decide(fact)) for fact in facts)
    planned = planned_commands(repo, pairs) if args.apply else ()
    if args.as_json:
        _print_json(pairs, dry_run=not args.apply, out=out, planned=planned)
    else:
        _print_human(pairs, dry_run=not args.apply, out=out, planned=planned)
    if not args.apply:
        return 0
    runner = apply_run if apply_run is not None else _default_apply_run
    return apply_planned(repo, pairs, runner)


def main(argv: Sequence[str] | None = None) -> int:
    return run(argv)


if __name__ == "__main__":
    sys.exit(main())
