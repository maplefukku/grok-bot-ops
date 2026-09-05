#!/usr/bin/env python3
from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from local_worktree_prune import (  # noqa: E402
    DEFAULT_JOBS_NAME,
    LOCK_FILE_NAME,
    PrLookup,
    Probes,
    TreeSignals,
    Verdict,
    WorktreeFact,
    WorktreeRow,
    _default_apply_run,
    _scan_lsof_cwds,
    apply_planned,
    collect_facts,
    decide,
    fact_from_signals,
    load_jobs_file,
    parse_jobs_document,
    parse_worktree_porcelain,
    path_has_live_process,
    planned_commands,
    run,
)


def _removable(
    *,
    path: str = "/tmp/added-wt",
    is_primary: bool = False,
    is_added: bool = True,
    pr_open_or_ci: bool = False,
    live_process: bool = False,
    dirty: bool = False,
    unique_only_here: bool = False,
    branch_unmerged: bool = False,
    live_job_names_path: bool = False,
    locked: bool = False,
    pr_merged: bool = True,
    job_abandoned_clean: bool = False,
    job_force: bool = False,
) -> WorktreeFact:
    return WorktreeFact(
        path=path,
        is_primary=is_primary,
        is_added=is_added,
        pr_open_or_ci=pr_open_or_ci,
        live_process=live_process,
        dirty=dirty,
        unique_only_here=unique_only_here,
        branch_unmerged=branch_unmerged,
        live_job_names_path=live_job_names_path,
        locked=locked,
        pr_merged=pr_merged,
        job_abandoned_clean=job_abandoned_clean,
        job_force=job_force,
    )


class RecordingRun:
    def __init__(self) -> None:
        self.cmds: list[tuple[str, ...]] = []

    def __call__(self, argv: object) -> int:
        self.cmds.append(tuple(str(x) for x in argv))
        return 0


class _OrderRecordingRun:
    def __init__(self, out: io.StringIO) -> None:
        self.out = out
        self.cmds: list[tuple[str, ...]] = []
        self.saw_applied_before_run = False

    def __call__(self, argv: object) -> int:
        if "Applied:" in self.out.getvalue():
            self.saw_applied_before_run = True
        self.cmds.append(tuple(str(x) for x in argv))
        return 0


def _git(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.setdefault("GIT_AUTHOR_NAME", "wt-test")
    env.setdefault("GIT_AUTHOR_EMAIL", "wt-test@example.test")
    env.setdefault("GIT_COMMITTER_NAME", "wt-test")
    env.setdefault("GIT_COMMITTER_EMAIL", "wt-test@example.test")
    completed = subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        env=env,
    )
    if check and completed.returncode != 0:
        raise RuntimeError(completed.stderr or completed.stdout or args)
    return completed


def _init_repo(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init")
    _git(root, "config", "user.email", "wt-test@example.test")
    _git(root, "config", "user.name", "wt-test")
    (root / "README").write_text("x\n", encoding="utf-8")
    _git(root, "add", "README")
    _git(root, "commit", "-m", "init")
    _git(root, "branch", "-M", "main")


KEEP_LIVE_CASES = (
    (
        "primary",
        dict(
            is_primary=True,
            is_added=True,
            pr_open_or_ci=False,
            live_process=False,
            dirty=False,
            unique_only_here=False,
            branch_unmerged=False,
            live_job_names_path=False,
            locked=False,
            pr_merged=True,
            job_abandoned_clean=True,
            job_force=True,
        ),
        "primary",
    ),
    ("pr_open_or_ci", dict(pr_open_or_ci=True), "pr_open_or_ci"),
    ("live_process", dict(live_process=True), "live_process"),
    ("dirty", dict(dirty=True), "dirty"),
    (
        "unmerged_live_job",
        dict(branch_unmerged=True, live_job_names_path=True),
        "unmerged_live_job",
    ),
    ("locked", dict(locked=True), "locked"),
)

REMOVE_OK_MISS_CASES = (
    ("is_added", dict(is_added=False), "remove_ok_miss:is_added"),
    (
        "pr_merged_or_abandoned",
        dict(pr_merged=False, job_abandoned_clean=False),
        "remove_ok_miss:pr_merged_or_abandoned",
    ),
    ("not_live_process", dict(live_process=True), "remove_ok_miss:not_live_process"),
    ("not_dirty_or_unique_dirty", dict(dirty=True), "remove_ok_miss:not_dirty_or_unique"),
    (
        "not_dirty_or_unique_unique",
        dict(unique_only_here=True),
        "remove_ok_miss:not_dirty_or_unique",
    ),
    (
        "not_live_job",
        dict(live_job_names_path=True, branch_unmerged=False),
        "remove_ok_miss:not_live_job",
    ),
    ("not_locked", dict(locked=True), "remove_ok_miss:not_locked"),
)


class TestDecideKeepLive(unittest.TestCase):
    def test_primary_never_removed_even_when_every_other_field_is_remove_shaped(self):
        fact = _removable(
            is_primary=True,
            is_added=True,
            pr_open_or_ci=False,
            live_process=False,
            dirty=False,
            unique_only_here=False,
            branch_unmerged=False,
            live_job_names_path=False,
            locked=False,
            pr_merged=True,
            job_abandoned_clean=True,
            job_force=True,
        )
        verdict = decide(fact)
        self.assertEqual(verdict.action, "keep")
        self.assertIn("primary", verdict.reasons)
        self.assertFalse(verdict.force)

    def test_each_keep_live_reason_alone_keeps(self):
        for name, overrides, reason in KEEP_LIVE_CASES:
            with self.subTest(name=name):
                verdict = decide(_removable(**overrides))
                self.assertEqual(verdict.action, "keep")
                self.assertIn(reason, verdict.reasons)
                self.assertFalse(verdict.force)


class TestDecideRemoveOk(unittest.TestCase):
    def test_remove_only_when_all_six_remove_ok_hold(self):
        verdict = decide(_removable())
        self.assertEqual(verdict.action, "remove")
        self.assertEqual(verdict.reasons, ("remove_ok",))
        self.assertFalse(verdict.force)

    def test_each_remove_ok_miss_keeps(self):
        for name, overrides, reason in REMOVE_OK_MISS_CASES:
            with self.subTest(name=name):
                verdict = decide(_removable(**overrides))
                self.assertEqual(verdict.action, "keep")
                self.assertIn(reason, verdict.reasons)

    def test_abandoned_clean_allows_remove_without_pr_merged(self):
        verdict = decide(_removable(pr_merged=False, job_abandoned_clean=True))
        self.assertEqual(verdict.action, "remove")


class TestDecideDirtyAndJobs(unittest.TestCase):
    def test_uncommitted_dirty_keeps(self):
        verdict = decide(_removable(dirty=True, unique_only_here=False))
        self.assertEqual(verdict.action, "keep")
        self.assertIn("dirty", verdict.reasons)

    def test_unpushed_unique_keeps(self):
        verdict = decide(_removable(dirty=True, unique_only_here=True))
        self.assertEqual(verdict.action, "keep")
        self.assertIn("dirty", verdict.reasons)

    def test_unique_without_dirty_still_fails_remove_ok(self):
        verdict = decide(_removable(dirty=False, unique_only_here=True))
        self.assertEqual(verdict.action, "keep")
        self.assertIn("remove_ok_miss:not_dirty_or_unique", verdict.reasons)

    def test_unmerged_plus_live_job_keeps(self):
        verdict = decide(
            _removable(branch_unmerged=True, live_job_names_path=True)
        )
        self.assertEqual(verdict.action, "keep")
        self.assertIn("unmerged_live_job", verdict.reasons)

    def test_unmerged_without_job_does_not_by_itself_allow_remove(self):
        still_blocked = decide(
            _removable(
                branch_unmerged=True,
                live_job_names_path=False,
                pr_merged=False,
                job_abandoned_clean=False,
            )
        )
        self.assertEqual(still_blocked.action, "keep")
        self.assertIn("remove_ok_miss:pr_merged_or_abandoned", still_blocked.reasons)

    def test_unmerged_without_job_still_removes_when_pr_merged(self):
        verdict = decide(
            _removable(
                branch_unmerged=True,
                live_job_names_path=False,
                pr_merged=True,
            )
        )
        self.assertEqual(verdict.action, "remove")


class TestDecideForce(unittest.TestCase):
    def test_force_true_only_when_remove_and_job_force(self):
        removed = decide(_removable(job_force=True))
        self.assertEqual(removed.action, "remove")
        self.assertTrue(removed.force)
        kept = decide(_removable(job_force=True, locked=True))
        self.assertEqual(kept.action, "keep")
        self.assertFalse(kept.force)
        plain = decide(_removable(job_force=False))
        self.assertEqual(plain.action, "remove")
        self.assertFalse(plain.force)


class TestPlannedCommands(unittest.TestCase):
    def test_planned_apply_never_includes_remote_branch_delete(self):
        pairs = [(_removable(), decide(_removable()))]
        cmds = planned_commands("/repo", pairs)
        blob = " ".join(" ".join(cmd) for cmd in cmds)
        self.assertNotIn("push --delete", blob)
        self.assertNotIn("branch -d", blob)
        self.assertNotIn("branch -D", blob)
        self.assertNotIn("branch --delete", blob)
        self.assertIn("worktree remove", blob)
        self.assertIn("worktree prune", blob)
        self.assertNotIn("--force", blob)

    def test_force_flag_only_on_remove_command(self):
        fact = _removable(job_force=True)
        cmds = planned_commands("/repo", [(fact, decide(fact))])
        self.assertEqual(
            cmds[0],
            ("git", "-C", "/repo", "worktree", "remove", "--force", fact.path),
        )

    def test_primary_verdict_remove_is_still_skipped(self):
        fact = _removable(is_primary=True, is_added=True)
        fake = Verdict("remove", ("remove_ok",), True)
        cmds = planned_commands("/repo", [(fact, fake)])
        self.assertEqual(
            cmds,
            (("git", "-C", "/repo", "worktree", "prune"),),
        )

    def test_apply_without_removes_still_prunes_stale_metadata(self):
        fact = _removable(locked=True)
        cmds = planned_commands("/repo", [(fact, decide(fact))])
        self.assertEqual(
            cmds,
            (("git", "-C", "/repo", "worktree", "prune"),),
        )

    def test_script_source_never_deletes_branches(self):
        text = Path(_SCRIPTS / "local_worktree_prune.py").read_text(encoding="utf-8")
        self.assertNotIn("git push --delete", text)
        self.assertNotIn("git branch -d", text)
        self.assertNotIn("git branch -D", text)
        self.assertNotIn("git branch --delete", text)


class TestCliDryRun(unittest.TestCase):
    def test_default_does_not_execute_worktree_remove(self):
        with tempfile.TemporaryDirectory() as tmp:
            primary = Path(tmp) / "repo"
            added = Path(tmp) / "added"
            _init_repo(primary)
            _git(primary, "worktree", "add", "-b", "feature", str(added))
            rec = RecordingRun()
            buf = io.StringIO()
            code = run(
                ["--repo", str(primary), "--json"],
                apply_run=rec,
                probes=Probes(process_cwds=(), pr_by_branch={}),
                stdout=buf,
            )
            self.assertEqual(code, 0)
            self.assertEqual(rec.cmds, [])
            payload = json.loads(buf.getvalue())
            self.assertTrue(payload["dry_run"])
            self.assertTrue(payload["nothing_removed"])
            self.assertEqual(payload["planned"], [])
            self.assertTrue(any(row["is_primary"] for row in payload["verdicts"]))
            for row in payload["verdicts"]:
                if row["is_primary"]:
                    self.assertEqual(row["action"], "keep")

    def test_human_dry_run_says_nothing_will_be_removed(self):
        with tempfile.TemporaryDirectory() as tmp:
            primary = Path(tmp) / "repo"
            _init_repo(primary)
            rec = RecordingRun()
            buf = io.StringIO()
            code = run(
                ["--repo", str(primary)],
                apply_run=rec,
                probes=Probes(process_cwds=(), pr_by_branch={}),
                stdout=buf,
            )
            self.assertEqual(code, 0)
            self.assertEqual(rec.cmds, [])
            self.assertIn("Dry-run: nothing will be removed.", buf.getvalue())
            self.assertIn("KEEP", buf.getvalue())

    def test_apply_executes_recorded_remove_and_prune(self):
        rec = RecordingRun()
        fact = _removable()
        code = apply_planned("/repo", [(fact, decide(fact))], rec)
        self.assertEqual(code, 0)
        self.assertEqual(
            rec.cmds,
            [
                ("git", "-C", "/repo", "worktree", "remove", fact.path),
                ("git", "-C", "/repo", "worktree", "prune"),
            ],
        )


class TestLockAndJobs(unittest.TestCase):
    def test_lock_file_keeps(self):
        row = WorktreeRow(
            path="/tmp/added-wt",
            head="abc",
            branch="refs/heads/feature",
            git_locked=False,
            is_primary=False,
        )
        signals = TreeSignals(
            uncommitted=False,
            unique_only_here=False,
            branch_unmerged=False,
            pr_open_or_ci=False,
            pr_merged=True,
            live_process=False,
            lock_file=True,
            git_locked=False,
            job_live=False,
            job_keep=False,
            job_abandoned=False,
            job_force=False,
        )
        fact = fact_from_signals(row, signals)
        self.assertTrue(fact.locked)
        self.assertTrue(fact.is_added)
        verdict = decide(fact)
        self.assertEqual(verdict.action, "keep")
        self.assertIn("locked", verdict.reasons)

    def test_job_keep_locks(self):
        jobs = parse_jobs_document(
            {
                "jobs": [
                    {
                        "name": "hold",
                        "path": "/tmp/added-wt",
                        "state": "keep",
                        "force": False,
                    }
                ]
            },
            Path("/tmp"),
        )
        self.assertEqual(jobs[0].state, "keep")
        row = WorktreeRow(
            path="/tmp/added-wt",
            head="abc",
            branch="refs/heads/feature",
            git_locked=False,
            is_primary=False,
        )
        signals = TreeSignals(
            uncommitted=False,
            unique_only_here=False,
            branch_unmerged=False,
            pr_open_or_ci=False,
            pr_merged=True,
            live_process=False,
            lock_file=False,
            git_locked=False,
            job_live=False,
            job_keep=True,
            job_abandoned=False,
            job_force=False,
        )
        fact = fact_from_signals(row, signals)
        self.assertTrue(fact.locked)
        self.assertEqual(decide(fact).action, "keep")

    def test_invalid_job_state_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_jobs_document(
                {"jobs": [{"path": "/tmp/added-wt", "state": "maybe"}]},
                Path("/tmp"),
            )

    def test_merged_pr_does_not_treat_local_commits_as_unique_loss(self):
        row = WorktreeRow(
            path="/tmp/added-wt",
            head="abc",
            branch="refs/heads/feature",
            git_locked=False,
            is_primary=False,
        )
        fact = fact_from_signals(
            row,
            TreeSignals(
                uncommitted=False,
                unique_only_here=True,
                branch_unmerged=True,
                pr_open_or_ci=False,
                pr_merged=True,
                live_process=False,
                lock_file=False,
                git_locked=False,
                job_live=False,
                job_keep=False,
                job_abandoned=False,
                job_force=False,
            ),
        )
        self.assertFalse(fact.unique_only_here)
        self.assertFalse(fact.dirty)
        self.assertEqual(decide(fact).action, "remove")

    def test_abandoned_sets_clean_only_when_not_unique(self):
        row = WorktreeRow(
            path="/tmp/added-wt",
            head="abc",
            branch="refs/heads/feature",
            git_locked=False,
            is_primary=False,
        )
        clean = fact_from_signals(
            row,
            TreeSignals(
                uncommitted=False,
                unique_only_here=False,
                branch_unmerged=False,
                pr_open_or_ci=False,
                pr_merged=False,
                live_process=False,
                lock_file=False,
                git_locked=False,
                job_live=False,
                job_keep=False,
                job_abandoned=True,
                job_force=False,
            ),
        )
        self.assertTrue(clean.job_abandoned_clean)
        self.assertEqual(decide(clean).action, "remove")
        dirty = fact_from_signals(
            row,
            TreeSignals(
                uncommitted=True,
                unique_only_here=False,
                branch_unmerged=False,
                pr_open_or_ci=False,
                pr_merged=False,
                live_process=False,
                lock_file=False,
                git_locked=False,
                job_live=False,
                job_keep=False,
                job_abandoned=True,
                job_force=False,
            ),
        )
        self.assertFalse(dirty.job_abandoned_clean)
        self.assertEqual(decide(dirty).action, "keep")

    def test_job_force_does_not_bypass_keep(self):
        fact = fact_from_signals(
            WorktreeRow(
                path="/tmp/added-wt",
                head="abc",
                branch="refs/heads/feature",
                git_locked=False,
                is_primary=False,
            ),
            TreeSignals(
                uncommitted=False,
                unique_only_here=False,
                branch_unmerged=False,
                pr_open_or_ci=False,
                pr_merged=True,
                live_process=False,
                lock_file=True,
                git_locked=False,
                job_live=False,
                job_keep=False,
                job_abandoned=False,
                job_force=True,
            ),
        )
        verdict = decide(fact)
        self.assertEqual(verdict.action, "keep")
        self.assertFalse(verdict.force)


class TestPorcelainAndProcess(unittest.TestCase):
    def test_first_worktree_entry_is_primary(self):
        rows = parse_worktree_porcelain(
            "worktree /main\nHEAD abc\nbranch refs/heads/main\n\n"
            "worktree /added\nHEAD def\nbranch refs/heads/feature\n"
        )
        self.assertEqual(len(rows), 2)
        self.assertTrue(rows[0].is_primary)
        self.assertFalse(rows[1].is_primary)
        self.assertEqual(rows[0].path, "/main")
        self.assertEqual(rows[1].branch, "refs/heads/feature")

    def test_process_scan_fail_closed_when_cwds_unknown(self):
        self.assertTrue(path_has_live_process("/tmp/wt", None))

    def test_process_scan_empty_is_not_live(self):
        self.assertFalse(path_has_live_process("/tmp/wt", ()))

    def test_process_under_tree_is_live(self):
        self.assertTrue(path_has_live_process("/tmp/wt", ("/tmp/wt/src",)))

    def test_lsof_exit_1_with_cwd_lines_is_not_scan_failure(self):
        completed = subprocess.CompletedProcess(
            args=["lsof", "-a", "-d", "cwd", "-Fn"],
            returncode=1,
            stdout="p123\nfcwd\nn/tmp/added-wt\n",
            stderr="lsof: WARNING: output information may be incomplete.\n",
        )
        with (
            patch("local_worktree_prune.shutil.which", return_value="/usr/sbin/lsof"),
            patch("local_worktree_prune.subprocess.run", return_value=completed),
        ):
            cwds = _scan_lsof_cwds()
        self.assertEqual(cwds, ("/tmp/added-wt",))
        self.assertFalse(path_has_live_process("/tmp/other", cwds))
        self.assertTrue(path_has_live_process("/tmp/added-wt", cwds))

    def test_lsof_nonzero_without_cwd_lines_is_scan_failure(self):
        completed = subprocess.CompletedProcess(
            args=["lsof", "-a", "-d", "cwd", "-Fn"],
            returncode=2,
            stdout="",
            stderr="lsof: unknown option\n",
        )
        with (
            patch("local_worktree_prune.shutil.which", return_value="/usr/sbin/lsof"),
            patch("local_worktree_prune.subprocess.run", return_value=completed),
        ):
            self.assertIsNone(_scan_lsof_cwds())


class TestTempGitIntegration(unittest.TestCase):
    def test_primary_is_keep_and_lock_file_keeps_added(self):
        with tempfile.TemporaryDirectory() as tmp:
            primary = Path(tmp) / "repo"
            added = Path(tmp) / "added"
            _init_repo(primary)
            _git(primary, "worktree", "add", "-b", "feature", str(added))
            (added / LOCK_FILE_NAME).write_text("keep\n", encoding="utf-8")
            facts = collect_facts(
                str(primary),
                probes=Probes(process_cwds=(), pr_by_branch={}),
            )
            self.assertGreaterEqual(len(facts), 2)
            primary_fact = next(f for f in facts if f.is_primary)
            added_fact = next(f for f in facts if f.is_added)
            self.assertEqual(decide(primary_fact).action, "keep")
            self.assertTrue(added_fact.locked)
            self.assertEqual(decide(added_fact).action, "keep")
            rec = RecordingRun()
            buf = io.StringIO()
            code = run(
                ["--repo", str(primary), "--json"],
                apply_run=rec,
                probes=Probes(process_cwds=(), pr_by_branch={}),
                stdout=buf,
            )
            self.assertEqual(code, 0)
            self.assertEqual(rec.cmds, [])
            payload = json.loads(buf.getvalue())
            primary_row = next(r for r in payload["verdicts"] if r["is_primary"])
            self.assertEqual(primary_row["action"], "keep")

    def test_default_jobs_file_and_live_job(self):
        with tempfile.TemporaryDirectory() as tmp:
            primary = Path(tmp) / "repo"
            added = Path(tmp) / "added"
            _init_repo(primary)
            _git(primary, "worktree", "add", "-b", "feature", str(added))
            jobs_path = primary / DEFAULT_JOBS_NAME
            jobs_path.write_text(
                json.dumps(
                    {
                        "jobs": [
                            {
                                "name": "follow-up",
                                "path": str(added),
                                "state": "live",
                                "force": False,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            jobs = load_jobs_file(jobs_path, primary)
            facts = collect_facts(
                str(primary),
                jobs=jobs,
                probes=Probes(process_cwds=(), pr_by_branch={}),
            )
            added_fact = next(f for f in facts if f.is_added)
            self.assertTrue(added_fact.live_job_names_path)
            self.assertEqual(decide(added_fact).action, "keep")

    def test_injected_merged_pr_does_not_call_github(self):
        with tempfile.TemporaryDirectory() as tmp:
            primary = Path(tmp) / "repo"
            added = Path(tmp) / "added"
            _init_repo(primary)
            _git(primary, "worktree", "add", "-b", "feature", str(added))
            facts = collect_facts(
                str(primary),
                probes=Probes(
                    process_cwds=(),
                    pr_by_branch={
                        "feature": PrLookup(unknown=False, open_or_ci=False, merged=True),
                        "main": PrLookup(unknown=False, open_or_ci=False, merged=False),
                    },
                ),
            )
            added_fact = next(f for f in facts if f.is_added)
            self.assertTrue(added_fact.pr_merged)
            self.assertFalse(added_fact.pr_open_or_ci)
            self.assertEqual(decide(added_fact).action, "remove")

    def test_apply_removes_added_worktree_when_remove_ok(self):
        with tempfile.TemporaryDirectory() as tmp:
            primary = Path(tmp) / "repo"
            added = Path(tmp) / "added"
            _init_repo(primary)
            _git(primary, "worktree", "add", "-b", "feature", str(added))
            probes = Probes(
                process_cwds=(),
                pr_by_branch={
                    "feature": PrLookup(
                        unknown=False, open_or_ci=False, merged=True
                    ),
                    "main": PrLookup(
                        unknown=False, open_or_ci=False, merged=False
                    ),
                },
            )
            buf = io.StringIO()
            code = run(
                ["--repo", str(primary), "--apply", "--json"],
                probes=probes,
                stdout=buf,
            )
            self.assertEqual(code, 0)
            payload = json.loads(buf.getvalue())
            self.assertFalse(payload["dry_run"])
            listed = _git(primary, "worktree", "list", "--porcelain")
            self.assertNotIn(str(added.resolve()), listed.stdout)
            self.assertIn(str(primary.resolve()), listed.stdout)
            self.assertTrue(primary.is_dir())
            self.assertFalse(added.exists())

    def test_apply_prints_applied_only_after_commands_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            primary = Path(tmp) / "repo"
            added = Path(tmp) / "added"
            _init_repo(primary)
            _git(primary, "worktree", "add", "-b", "feature", str(added))
            buf = io.StringIO()
            rec = _OrderRecordingRun(buf)
            code = run(
                ["--repo", str(primary), "--apply"],
                apply_run=rec,
                probes=Probes(
                    process_cwds=(),
                    pr_by_branch={
                        "feature": PrLookup(
                            unknown=False, open_or_ci=False, merged=True
                        ),
                        "main": PrLookup(
                            unknown=False, open_or_ci=False, merged=False
                        ),
                    },
                ),
                stdout=buf,
            )
            self.assertEqual(code, 0)
            self.assertFalse(rec.saw_applied_before_run)
            self.assertGreaterEqual(len(rec.cmds), 1)
            self.assertIn("Applied:", buf.getvalue())

    def test_apply_failure_does_not_claim_applied(self):
        with tempfile.TemporaryDirectory() as tmp:
            primary = Path(tmp) / "repo"
            added = Path(tmp) / "added"
            _init_repo(primary)
            _git(primary, "worktree", "add", "-b", "feature", str(added))
            buf = io.StringIO()
            code = run(
                ["--repo", str(primary), "--apply"],
                apply_run=lambda _argv: 128,
                probes=Probes(
                    process_cwds=(),
                    pr_by_branch={
                        "feature": PrLookup(
                            unknown=False, open_or_ci=False, merged=True
                        ),
                        "main": PrLookup(
                            unknown=False, open_or_ci=False, merged=False
                        ),
                    },
                ),
                stdout=buf,
            )
            self.assertEqual(code, 128)
            text = buf.getvalue()
            self.assertNotIn("Applied:", text)
            self.assertIn("Apply failed:", text)
            self.assertTrue(added.exists())

    def test_default_apply_run_forwards_fatal_text(self):
        err = io.StringIO()
        code = _default_apply_run(
            [
                sys.executable,
                "-c",
                "import sys; sys.stderr.write('fatal: refused\\n'); sys.exit(128)",
            ],
            err,
        )
        self.assertEqual(code, 128)
        self.assertIn("fatal: refused", err.getvalue())


if __name__ == "__main__":
    unittest.main()
