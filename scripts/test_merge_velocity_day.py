#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import stat
import subprocess
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
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

_FAKE_GH = r"""#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

argv = sys.argv[1:]
log = Path(os.environ["MERGE_VELOCITY_GH_LOG"])
log.write_text(
    (log.read_text() if log.exists() else "") + json.dumps(argv) + "\n",
    encoding="utf-8",
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
if repo is None:
    sys.stderr.write("fake gh needs --repo\n")
    sys.exit(2)
fixtures = json.loads(Path(os.environ["MERGE_VELOCITY_GH_FIXTURE"]).read_text())
print(json.dumps(fixtures.get(repo, [])))
"""


def _empty() -> dict[str, list[dict[str, str]]]:
    return {repo: [] for repo in REPOS}


def _run(
    args: list[str],
    fixtures: dict[str, list[dict[str, str]]],
) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        fixture = tmp / "fixtures.json"
        fixture.write_text(json.dumps(fixtures), encoding="utf-8")
        log = tmp / "gh.log"
        bindir = tmp / "bin"
        bindir.mkdir()
        gh = bindir / "gh"
        gh.write_text(_FAKE_GH, encoding="utf-8")
        gh.chmod(gh.stat().st_mode | stat.S_IXUSR)
        env = os.environ.copy()
        env["PATH"] = f"{bindir}{os.pathsep}{env.get('PATH', '')}"
        env["MERGE_VELOCITY_GH_FIXTURE"] = str(fixture)
        env["MERGE_VELOCITY_GH_LOG"] = str(log)
        env.pop("GH_TOKEN", None)
        env.pop("GITHUB_TOKEN", None)
        proc = subprocess.run(
            ["bash", str(SCRIPT), *args],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )
        setattr(proc, "gh_log", log.read_text(encoding="utf-8") if log.exists() else "")
        return proc


def _json(proc: subprocess.CompletedProcess[str]) -> dict[str, object]:
    return json.loads(proc.stdout)


class MergeVelocityDayTests(unittest.TestCase):
    def test_sot_script_is_executable(self) -> None:
        self.assertTrue(SCRIPT.is_file())
        self.assertTrue(os.access(SCRIPT, os.X_OK))

    def test_report_keys_five_repos_and_total(self) -> None:
        fixtures = _empty()
        fixtures["maplefukku/DevTogether"] = [
            {"number": "11", "mergedAt": "2026-09-06T15:30:00Z"},
            {"number": "12", "mergedAt": "2026-09-06T18:00:00Z"},
        ]
        proc = _run(["2026-09-07", "2026-09-06"], fixtures)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = _json(proc)
        self.assertEqual(payload["day"], "2026-09-07")
        self.assertEqual(payload["total"], 2)
        by_repo = payload["by_repo"]
        self.assertIsInstance(by_repo, dict)
        self.assertEqual(list(by_repo), list(REPOS))
        self.assertEqual(by_repo["maplefukku/DevTogether"], 2)
        self.assertEqual(sum(int(v) for v in by_repo.values()), payload["total"])

    def test_prior_zero_passes_when_today_at_least_one(self) -> None:
        fixtures = _empty()
        fixtures["maplefukku/ZuruNote"] = [
            {"number": "90", "mergedAt": "2026-09-06T15:00:00Z"},
        ]
        proc = _run(["2026-09-07", "2026-09-06"], fixtures)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = _json(proc)
        self.assertEqual(payload["prior"], 0)
        self.assertEqual(payload["need_2x"], 1)
        self.assertTrue(payload["pass"])

    def test_prior_zero_misses_when_today_is_zero(self) -> None:
        proc = _run(["2026-09-07", "2026-09-06"], _empty())
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = _json(proc)
        self.assertEqual(payload["total"], 0)
        self.assertEqual(payload["prior"], 0)
        self.assertEqual(payload["need_2x"], 1)
        self.assertFalse(payload["pass"])

    def test_need_2x_is_twice_prior_when_prior_positive(self) -> None:
        fixtures = _empty()
        fixtures["maplefukku/sauna-master"] = [
            {"number": "1", "mergedAt": "2026-09-05T15:10:00Z"},
            {"number": "2", "mergedAt": "2026-09-05T20:00:00Z"},
            {"number": "3", "mergedAt": "2026-09-05T22:00:00Z"},
            {"number": "4", "mergedAt": "2026-09-06T15:10:00Z"},
            {"number": "5", "mergedAt": "2026-09-06T16:00:00Z"},
            {"number": "6", "mergedAt": "2026-09-06T17:00:00Z"},
        ]
        proc = _run(["2026-09-07", "2026-09-06"], fixtures)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = _json(proc)
        self.assertEqual(payload["prior"], 3)
        self.assertEqual(payload["need_2x"], 6)
        self.assertEqual(payload["total"], 3)
        self.assertFalse(payload["pass"])

    def test_jst_window_is_half_open_on_utc_neighbors(self) -> None:
        fixtures = _empty()
        fixtures["maplefukku/gakuse-ai"] = [
            {"number": "1", "mergedAt": "2026-09-06T14:59:59Z"},
            {"number": "2", "mergedAt": "2026-09-06T15:00:00Z"},
            {"number": "3", "mergedAt": "2026-09-07T14:59:59Z"},
            {"number": "4", "mergedAt": "2026-09-07T15:00:00Z"},
        ]
        proc = _run(["2026-09-07", "2026-09-06"], fixtures)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = _json(proc)
        self.assertEqual(payload["total"], 2)
        self.assertEqual(payload["prior"], 1)
        self.assertEqual(payload["by_repo"]["maplefukku/gakuse-ai"], 2)

    def test_weekend_jst_day_counts(self) -> None:
        fixtures = _empty()
        fixtures["maplefukku/grok-bot-ops"] = [
            {"number": "39", "mergedAt": "2026-09-05T03:15:00Z"},
        ]
        proc = _run(["2026-09-05", "2026-09-04"], fixtures)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = _json(proc)
        self.assertEqual(payload["day"], "2026-09-05")
        self.assertEqual(payload["total"], 1)
        self.assertTrue(payload["pass"])

    def test_default_day_is_asia_tokyo_today(self) -> None:
        proc = _run([], _empty())
        self.assertEqual(proc.returncode, 0, proc.stderr)
        today = datetime.now(timezone(timedelta(hours=9))).date().isoformat()
        self.assertEqual(_json(proc)["day"], today)

    def test_wraps_gh_pr_list_only(self) -> None:
        proc = _run(["2026-09-07", "2026-09-06"], _empty())
        self.assertEqual(proc.returncode, 0, proc.stderr)
        lines = [
            json.loads(line)
            for line in getattr(proc, "gh_log").splitlines()
            if line
        ]
        self.assertEqual(len(lines), len(REPOS))
        seen: set[str] = set()
        for argv in lines:
            self.assertEqual(argv[0], "pr")
            self.assertEqual(argv[1], "list")
            self.assertNotIn("api", argv)
            self.assertIn("--state", argv)
            self.assertIn("merged", argv)
            repo = None
            for i, arg in enumerate(argv):
                if arg in ("--repo", "-R"):
                    repo = argv[i + 1]
            self.assertIn(repo, REPOS)
            seen.add(repo)
        self.assertEqual(seen, set(REPOS))


if __name__ == "__main__":
    unittest.main()
