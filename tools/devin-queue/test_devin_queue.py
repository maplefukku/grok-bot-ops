#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

_DIR = Path(__file__).resolve().parent
if str(_DIR) not in sys.path:
    sys.path.insert(0, str(_DIR))

import devin_queue as dq  # noqa: E402


def _make_queue(tmp: str) -> dq.Queue:
    queue = dq.Queue(Path(tmp) / "queue")
    queue.init()
    config = json.loads((queue.root / "config.json").read_text())
    config["repos"] = ["acme/widget"]
    (queue.root / "config.json").write_text(json.dumps(config, indent=2) + "\n")
    return queue


def _job(job_id: str = "job-01", **overrides) -> dict:
    job = {
        "schema": 1,
        "job_id": job_id,
        "task_id": "B-02",
        "repo": "acme/widget",
        "base_branch": "main",
        "branch": "devin/{}".format(job_id),
        "prompt": "implement the thing, push, open a draft PR",
        "model": "swe-2",
        "timeout_sec": 60,
        "pr": {"draft": True, "title": "draft: {}".format(job_id), "base": "main"},
        "submitted_by": "ops",
        "submitted_at": "2026-11-03T10:00:00+09:00",
    }
    job.update(overrides)
    return job


def _put_inbox(queue: dq.Queue, job: dict, mtime=None) -> Path:
    path = queue.d("inbox") / (job["job_id"] + ".json")
    path.write_text(json.dumps(job), encoding="utf-8")
    if mtime is not None:
        import os

        os.utime(path, (mtime, mtime))
    return path


def _result(queue: dq.Queue, dirname: str, job_id: str) -> dict:
    return json.loads(
        (queue.d(dirname) / (job_id + dq.RESULT_SUFFIX)).read_text()
    )


class FakeRun:
    """Records argv and returns canned results; never touches the network."""

    def __init__(self, devin_output: str = "", devin_rc: int = 0, auth_rc: int = 0):
        self.calls = []
        self.envs = []
        self.devin_output = devin_output
        self.devin_rc = devin_rc
        self.auth_rc = auth_rc

    def __call__(self, argv, cwd=None, timeout_sec=None, env=None) -> dq.CmdResult:
        argv = tuple(str(a) for a in argv)
        self.calls.append(argv)
        self.envs.append(env)
        if argv[:3] == ("devin", "auth", "status"):
            return dq.CmdResult(self.auth_rc, "auth status", False)
        if argv[0] == "devin":
            return dq.CmdResult(self.devin_rc, self.devin_output, False)
        return dq.CmdResult(0, "", False)


class TestClaim(unittest.TestCase):
    """Gate:
    1. Contract: run-once claims the oldest inbox job first and moves it into
       running/; PAUSE or a full running/ slot blocks the claim; two racers
       on one job produce exactly one winner.
    2. Guards regressions where a newer job wins, a claim leaves the file in
       inbox/ (double-run), or paused/full state still consumes a job.
    3. No existing coverage touches the queue claim path; this tool owns it.
    4. Uses only the queue root and the claim path itself; no test-only seams.
    """

    def test_oldest_job_is_claimed_first_into_running(self):
        with tempfile.TemporaryDirectory() as tmp:
            queue = _make_queue(tmp)
            newer = _put_inbox(queue, _job("job-new"), mtime=2000)
            _put_inbox(queue, _job("job-old"), mtime=1000)
            claimed = queue.claim_next()
            self.assertIsNotNone(claimed)
            self.assertEqual(claimed.name, "job-old.json")
            self.assertTrue((queue.d("running") / "job-old.json").exists())
            self.assertTrue(newer.exists())

    def test_pause_claims_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            queue = _make_queue(tmp)
            path = _put_inbox(queue, _job("job-01"))
            (queue.root / "PAUSE").touch()
            run = FakeRun()
            self.assertEqual(dq.run_once(queue, run=run), 0)
            self.assertTrue(path.exists())
            self.assertEqual(queue._job_files("running"), [])
            self.assertEqual(run.calls, [])

    def test_max_concurrency_claims_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            queue = _make_queue(tmp)
            path = _put_inbox(queue, _job("job-01"))
            (queue.d("running") / "other.json").write_text("{}")
            run = FakeRun()
            self.assertEqual(dq.run_once(queue, run=run), 0)
            self.assertTrue(path.exists())
            self.assertEqual(run.calls, [])

    def test_two_claimers_one_winner(self):
        with tempfile.TemporaryDirectory() as tmp:
            queue = _make_queue(tmp)
            _put_inbox(queue, _job("job-01"))
            results = []

            def claim():
                results.append(queue.claim_next())

            threads = [threading.Thread(target=claim) for _ in range(2)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            winners = [r for r in results if r is not None]
            self.assertEqual(len(winners), 1)
            self.assertTrue((queue.d("running") / "job-01.json").exists())


class TestQuotaStop(unittest.TestCase):
    """Gate:
    1. Contract: CLI output containing a quota/billing marker moves the job to
       failed/ with the matching reason, writes STATUS.json stopped_quota,
       creates PAUSE, and a later run-once claims nothing.
    2. Guards regressions where a quota hit is logged but the queue keeps
       draining the wallet, or the wrong reason lands in the result file.
    3. No existing coverage of the quota-stop path; this tool owns it.
    4. Uses the queue root and the injected run fn the production runner also
       uses (run_once's real `run` parameter) plus the real remote_check hook.
    """

    def _run_once(self, queue, run):
        return dq.run_once(queue, run=run, remote_check=lambda job, r: [])

    def test_out_of_quota_stops_queue(self):
        with tempfile.TemporaryDirectory() as tmp:
            queue = _make_queue(tmp)
            _put_inbox(queue, _job("job-01"))
            _put_inbox(queue, _job("job-02"))
            run = FakeRun(devin_output="Session aborted: out_of_quota reached")
            self.assertEqual(self._run_once(queue, run), 0)
            result = _result(queue, "failed", "job-01")
            self.assertEqual(result["state"], "failed")
            self.assertEqual(result["reason"], "out_of_quota")
            status = json.loads((queue.root / "STATUS.json").read_text())
            self.assertEqual(status["state"], "stopped_quota")
            self.assertTrue((queue.root / "PAUSE").exists())
            calls_after = len(run.calls)
            self.assertEqual(self._run_once(queue, run), 0)
            self.assertEqual(len(run.calls), calls_after)
            self.assertTrue((queue.d("inbox") / "job-02.json").exists())

    def test_http_402_is_payment_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            queue = _make_queue(tmp)
            _put_inbox(queue, _job("job-01"))
            run = FakeRun(devin_output="request failed: HTTP 402 payment required")
            self.assertEqual(self._run_once(queue, run), 0)
            result = _result(queue, "failed", "job-01")
            self.assertEqual(result["reason"], "payment_required")
            status = json.loads((queue.root / "STATUS.json").read_text())
            self.assertEqual(status["state"], "stopped_quota")


class TestRedactor(unittest.TestCase):
    """Gate:
    1. Contract: every listed secret pattern becomes [REDACTED] and ordinary
       text passes through unchanged.
    2. Guards regressions where a token shape leaks into logs/ on disk.
    3. No existing coverage of the redactor; this tool owns it.
    4. Tests the pure redact() function only; no seams added.
    """

    def test_each_pattern_is_redacted(self):
        samples = {
            "cog_ABCDEF0123456789": "cog_ token",
            "ghp_" + "A1" * 20: "ghp_ token",
            "github_pat_" + "x" * 30: "github_pat_ token",
            "AIza" + "Q" * 35: "AIza key",
            "sk-" + "z" * 24: "sk- key",
            "Bearer abc.def.ghi": "Bearer token",
            "xoxb-123-456-abc": "xoxb token",
        }
        for needle in samples:
            with self.subTest(kind=samples[needle]):
                self.assertNotIn(needle, dq.redact("prefix " + needle + " suffix"))
                self.assertIn("[REDACTED]", dq.redact("prefix " + needle))

    def test_ordinary_text_is_untouched(self):
        text = "runner claimed job-01 on branch devin/job-01, exit 0"
        self.assertEqual(dq.redact(text), text)
        self.assertEqual(dq.redact("xox- not a token sk-short"), "xox- not a token sk-short")


class TestValidation(unittest.TestCase):
    """Gate:
    1. Contract: a job whose fields fail local validation (non-SWE-2 model,
       bad job_id) lands in failed/ with reason invalid_job and a detail.
    2. Guards regressions where a rejected job model still reaches the CLI.
    3. No existing coverage of job validation; this tool owns it.
    4. Uses only the queue root plus the injected run/remote_check params.
    """

    def test_non_swe2_model_goes_to_failed_invalid_job(self):
        with tempfile.TemporaryDirectory() as tmp:
            queue = _make_queue(tmp)
            _put_inbox(queue, _job("job-01", model="swe-2-lightning"))
            run = FakeRun()
            dq.run_once(queue, run=run, remote_check=lambda job, r: [])
            result = _result(queue, "failed", "job-01")
            self.assertEqual(result["reason"], "invalid_job")
            self.assertIn("model", result["detail"])
            self.assertFalse(
                any(c[0] == "devin" for c in run.calls),
                "invalid job must never reach the devin CLI",
            )

    def test_validate_job_rejects_bad_job_id(self):
        queue = dq.Queue(Path("/nonexistent"))
        errors = dq.validate_job(_job("Bad_ID!"), dq.DEFAULT_CONFIG)
        self.assertTrue(any("job_id" in e for e in errors))
        self.assertEqual(dq.validate_job(_job("job-ok"), {"repos": ["acme/widget"]}), [])


class TestDevinChildEnv(unittest.TestCase):
    """Gate:
    1. Contract: every devin child call (`auth status` and the `-p` run)
       receives an env built only from DEVIN_ENV_ALLOWLIST; secret-shaped
       names present in the parent never pass through.
    2. Guards regressions where the runner's full environment (API keys,
       tokens, secrets) leaks into the devin subprocess.
    3. No existing coverage of the child env; this tool owns it.
    4. Asserts on the env argument handed to the run() boundary — the same
       value default_run passes to subprocess.Popen — not internals.
    """

    def test_allowlisted_env_reaches_devin_child(self):
        with tempfile.TemporaryDirectory() as tmp:
            queue = _make_queue(tmp)
            _put_inbox(queue, _job("job-01"))
            run = FakeRun()
            parent = {
                "HOME": "/home/test",
                "PATH": "/usr/bin:/bin",
                "FOO_API_KEY": "fake-foo-key",
                "BAR_KEY": "fake-bar-key",
                "BAZ_TOKEN": "fake-baz-token",
                "QUX_SECRET": "fake-qux-secret",
            }
            with mock.patch.dict(os.environ, parent, clear=True):
                dq.run_once(queue, run=run, remote_check=lambda job, r: [])
            devin_idxs = [
                i for i, argv in enumerate(run.calls) if argv[0] == "devin"
            ]
            self.assertEqual(len(devin_idxs), 2)  # auth status + the -p run
            for i in devin_idxs:
                env = run.envs[i]
                self.assertIsNotNone(env)
                for name in ("FOO_API_KEY", "BAR_KEY", "BAZ_TOKEN", "QUX_SECRET"):
                    self.assertNotIn(name, env)
                self.assertEqual(env.get("HOME"), "/home/test")
                self.assertEqual(env.get("PATH"), "/usr/bin:/bin")


class TestRefValidation(unittest.TestCase):
    """Gate:
    1. Contract: branch, base_branch and pr.base must be safe ref names; an
       unsafe value fails the job as invalid_job before any git/gh/devin
       command runs.
    2. Guards option-injection regressions (e.g. --upload-pack=evil reaching
       a git call as an option instead of a ref).
    3. No existing coverage of ref validation; this tool owns it.
    4. Goes through run_once, the public validation/run path; FakeRun
       records every subprocess call so "no git/gh ran" is observable.
    """

    BAD_REFS = ("-x", "--upload-pack=evil", "a..b", "a b", "foo.lock", ".hidden")

    def test_bad_refs_fail_as_invalid_job_without_subprocess(self):
        for field in ("branch", "base_branch", "pr.base"):
            for value in self.BAD_REFS:
                with self.subTest(field=field, value=value):
                    with tempfile.TemporaryDirectory() as tmp:
                        queue = _make_queue(tmp)
                        job = _job("job-01")
                        if field == "pr.base":
                            job["pr"]["base"] = value
                        else:
                            job[field] = value
                        _put_inbox(queue, job)
                        run = FakeRun()
                        dq.run_once(queue, run=run, remote_check=lambda j, r: [])
                        result = _result(queue, "failed", "job-01")
                        self.assertEqual(result["reason"], "invalid_job")
                        self.assertIn(field, result["detail"])
                        self.assertEqual(
                            run.calls,
                            [],
                            "invalid ref must fail before any subprocess runs",
                        )

    def test_normal_ref_names_pass_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            queue = _make_queue(tmp)
            job = _job(
                "job-01",
                branch="devin/bazure-fallback-01",
                base_branch="wip/mini-live-20261103",
            )
            job["pr"]["base"] = "wip/mini-live-20261103"
            _put_inbox(queue, job)
            run = FakeRun()
            dq.run_once(queue, run=run, remote_check=lambda j, r: [])
            self.assertTrue(
                any(argv[0] == "devin" for argv in run.calls),
                "valid refs should reach the devin run",
            )
            result = _result(queue, "failed", "job-01")
            self.assertNotEqual(result["reason"], "invalid_job")


if __name__ == "__main__":
    unittest.main()
