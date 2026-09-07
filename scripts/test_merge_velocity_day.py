#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
SCRIPT = _SCRIPTS / "merge-velocity-day.sh"

REPOS = (
    "maplefukku/ZuruNote",
    "maplefukku/sauna-master",
    "maplefukku/gakuse-ai",
    "maplefukku/DevTogether",
    "maplefukku/grok-bot-ops",
)

FAKE_GH = r"""#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

argv = sys.argv[1:]
log = os.environ.get("MERGE_VELOCITY_GH_LOG")
if log:
    Path(log).write_text(
        Path(log).read_text() + json.dumps(argv) + "\n"
        if Path(log).exists()
        else json.dumps(argv) + "\n"
    )
if len(argv) < 2 or argv[0] != "pr" or argv[1] != "list":
    sys.stderr.write("fake gh accepts pr list only\n")
    sys.exit(2)
repo = None
for i, arg in enumerate(argv):
    if arg in ("--repo", "-R") and i + 1 < len(argv):
        repo = argv[i + 1]
        break
    if arg.startswith("--repo="):
        repo = arg.split("=", 1)[1]
        break
if not repo:
    sys.stderr.write("fake gh needs --repo\n")
    sys.exit(2)
fixtures = json.loads(Path(os.environ["MERGE_VELOCITY_GH_FIXTURE"]).read_text())
print(json.dumps(fixtures.get(repo, [])))
"""


def _empty_by_repo() -> dict[str, list[dict[str, object]]]:
    return {repo: [] for repo in REPOS}


def _run(
    args: list[str],
    fixtures: dict[str, list[dict[str, object]]],
    extra_env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        fixture_path = tmp / "fixtures.json"
        fixture_path.write_text(json.dumps(fixtures), encoding="utf-8")
        log_path = tmp / "gh.log"
        bindir = tmp / "bin"
        bindir.mkdir()
        gh = bindir / "gh"
        gh.write_text(FAKE_GH, encoding="utf-8")
        gh.chmod(gh.stat().st_mode | stat.S_IXUSR)
        env = os.environ.copy()
        env["PATH"] = f"{bindir}{os.pathsep}{env.get('PATH', '')}"
        env["MERGE_VELOCITY_GH_FIXTURE"] = str(fixture_path)
        env["MERGE_VELOCITY_GH_LOG"] = str(log_path)
        env.pop("GH_TOKEN", None)
        env.pop("GITHUB_TOKEN", None)
        if extra_env:
            env.update(extra_env)
        proc = subprocess.run(
            ["bash", str(SCRIPT), *args],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )
        proc.gh_log = (  # type: ignore[attr-defined]
            log_path.read_text(encoding="utf-8") if log_path.exists() else ""
        )
        return proc


def _payload(proc: subprocess.CompletedProcess[str]) -> dict[str, object]:
    return json.loads(proc.stdout)


class MergeVelocityDayTests(unittest.TestCase):
    def test_script_is_executable(self) -> None:
        self.assertTrue(SCRIPT.is_file(), "scripts/merge-velocity-day.sh is the SoT")
        self.assertTrue(os.access(SCRIPT, os.X_OK), "SoT script must be executable")

    def test_json_sot_keys_and_five_repos(self) -> None:
        fixtures = _empty_by_repo()
        fixtures["maplefukku/ZuruNote"] = [
            {"number": 1, "mergedAt": "2026-09-06T16:00:00Z"},
        ]
        proc = _run(["2026-09-07", "2026-09-06"], fixtures)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = _payload(proc)
        self.assertEqual(payload["day"], "2026-09-07")
        self.assertEqual(payload["total"], 1)
        by_repo = payload["by_repo"]
        self.assertIsInstance(by_repo, dict)
        for repo in REPOS:
            self.assertIn(repo, by_repo)
        self.assertEqual(by_repo["maplefukku/ZuruNote"], 1)
        self.assertEqual(sum(int(v) for v in by_repo.values()), payload["total"])

    def test_prior_zero_pass_when_today_at_least_one(self) -> None:
        fixtures = _empty_by_repo()
        fixtures["maplefukku/sauna-master"] = [
            {"number": 10, "mergedAt": "2026-09-06T15:00:00Z"},
        ]
        proc = _run(["2026-09-07", "2026-09-06"], fixtures)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = _payload(proc)
        self.assertEqual(payload["prior"], 0)
        self.assertEqual(payload["need_2x"], 1)
        self.assertTrue(payload["pass"], "prior=0 and today>=1 is PASS")

    def test_prior_zero_fail_when_today_is_zero(self) -> None:
        proc = _run(["2026-09-07", "2026-09-06"], _empty_by_repo())
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = _payload(proc)
        self.assertEqual(payload["total"], 0)
        self.assertEqual(payload["prior"], 0)
        self.assertEqual(payload["need_2x"], 1)
        self.assertFalse(payload["pass"], "prior=0 and today=0 is miss")

    def test_need_2x_is_prior_times_two_when_prior_positive(self) -> None:
        fixtures = _empty_by_repo()
        fixtures["maplefukku/gakuse-ai"] = [
            {"number": 1, "mergedAt": "2026-09-05T16:00:00Z"},
            {"number": 2, "mergedAt": "2026-09-05T17:00:00Z"},
            {"number": 3, "mergedAt": "2026-09-06T16:00:00Z"},
            {"number": 4, "mergedAt": "2026-09-06T17:00:00Z"},
            {"number": 5, "mergedAt": "2026-09-06T18:00:00Z"},
            {"number": 6, "mergedAt": "2026-09-06T19:00:00Z"},
        ]
        proc = _run(["2026-09-07", "2026-09-06"], fixtures)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = _payload(proc)
        self.assertEqual(payload["prior"], 2)
        self.assertEqual(payload["need_2x"], 4)
        self.assertEqual(payload["total"], 4)
        self.assertTrue(payload["pass"])

    def test_jst_day_excludes_utc_neighbor(self) -> None:
        fixtures = _empty_by_repo()
        fixtures["maplefukku/DevTogether"] = [
            {"number": 1, "mergedAt": "2026-09-06T14:59:59Z"},
            {"number": 2, "mergedAt": "2026-09-06T15:00:00Z"},
            {"number": 3, "mergedAt": "2026-09-07T14:59:59Z"},
            {"number": 4, "mergedAt": "2026-09-07T15:00:00Z"},
        ]
        proc = _run(["2026-09-07", "2026-09-06"], fixtures)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = _payload(proc)
        self.assertEqual(payload["total"], 2)
        self.assertEqual(payload["prior"], 1)
        self.assertEqual(payload["by_repo"]["maplefukku/DevTogether"], 2)

    def test_weekend_day_is_counted(self) -> None:
        fixtures = _empty_by_repo()
        fixtures["maplefukku/grok-bot-ops"] = [
            {"number": 7, "mergedAt": "2026-09-05T03:00:00Z"},
        ]
        proc = _run(["2026-09-05", "2026-09-04"], fixtures)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = _payload(proc)
        self.assertEqual(payload["day"], "2026-09-05")
        self.assertEqual(payload["total"], 1)
        self.assertTrue(payload["pass"])

    def test_hook_writes_accelerate_on_stderr_and_keeps_json_stdout(self) -> None:
        proc = _run(["2026-09-07", "2026-09-06", "--hook"], _empty_by_repo())
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = _payload(proc)
        self.assertFalse(payload["pass"])
        self.assertIn("ACCELERATE", proc.stderr)
        self.assertNotIn("ACCELERATE", proc.stdout)

    def test_hook_silent_on_pass(self) -> None:
        fixtures = _empty_by_repo()
        fixtures["maplefukku/ZuruNote"] = [
            {"number": 1, "mergedAt": "2026-09-06T16:00:00Z"},
        ]
        proc = _run(["--hook", "2026-09-07", "2026-09-06"], fixtures)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(_payload(proc)["pass"])
        self.assertNotIn("ACCELERATE", proc.stderr)

    def test_box_sot_reshape_does_not_recount(self) -> None:
        fleet = {
            "day": "2026-09-07",
            "prior_day": "2026-09-06",
            "products": {
                "ZuruNote": {"today": 1, "prior": 0},
                "sauna-master": {"today": 0, "prior": 0},
                "gakuse-ai": {"today": 0, "prior": 0},
                "DevTogether": {"today": 0, "prior": 0},
                "grok-bot-ops": {"today": 0, "prior": 0},
            },
        }
        with tempfile.TemporaryDirectory() as raw:
            box = Path(raw) / "merge-count-jst.sh"
            box.write_text(
                "#!/bin/sh\nprintf '%s\\n' '" + json.dumps(fleet) + "'\n",
                encoding="utf-8",
            )
            box.chmod(box.stat().st_mode | stat.S_IXUSR)
            proc = _run(
                ["2026-09-07", "2026-09-06"],
                _empty_by_repo(),
                extra_env={"MERGE_COUNT_JST": str(box)},
            )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = _payload(proc)
        self.assertEqual(payload["total"], 1)
        self.assertEqual(payload["by_repo"]["maplefukku/ZuruNote"], 1)
        self.assertEqual(payload["prior"], 0)
        self.assertEqual(payload["need_2x"], 1)
        self.assertTrue(payload["pass"])
        self.assertEqual(proc.gh_log, "")  # type: ignore[attr-defined]

    def test_wraps_gh_pr_list_only(self) -> None:
        proc = _run(["2026-09-07", "2026-09-06"], _empty_by_repo())
        self.assertEqual(proc.returncode, 0, proc.stderr)
        lines = [
            json.loads(line)
            for line in proc.gh_log.splitlines()  # type: ignore[attr-defined]
            if line
        ]
        self.assertEqual(len(lines), len(REPOS))
        seen: set[str] = set()
        for argv in lines:
            self.assertEqual(argv[0], "pr")
            self.assertEqual(argv[1], "list")
            self.assertNotIn("api", argv)
            repo = None
            for i, arg in enumerate(argv):
                if arg in ("--repo", "-R"):
                    repo = argv[i + 1]
            self.assertIn(repo, REPOS)
            seen.add(repo)
        self.assertEqual(seen, set(REPOS))


if __name__ == "__main__":
    unittest.main()
