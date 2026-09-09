#!/usr/bin/env python3
from __future__ import annotations

import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
_ROOT = _SCRIPTS.parent
SCRIPT = _SCRIPTS / "quiet-test.sh"
HOOK = _ROOT / ".cursor" / "hooks" / "run-ci.py"
GHA = _ROOT / ".github" / "workflows" / "ci.yml"

FLEET_STAMP = "FLEET-QUIET-TEST"
HARNESS_MARKERS = (
    "QUIET_OK_LINES",
    "QUIET_FAIL_LINES",
    "tail -n",
    "tail -",
)


def _run(
    args: list[str],
    extra_env: dict[str, str] | None = None,
    fleet_text: str | None = None,
    fleet_exit: int | None = None,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.pop("QUIET_TEST", None)
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        if fleet_text is not None:
            fleet = tmp / "quiet-test.sh"
            fleet.write_text(fleet_text, encoding="utf-8")
            fleet.chmod(fleet.stat().st_mode | stat.S_IXUSR)
            env["QUIET_TEST"] = str(fleet)
        else:
            env["QUIET_TEST"] = str(tmp / "missing-quiet-test.sh")
        if extra_env:
            env.update(extra_env)
        if fleet_exit is not None and fleet_text is None:
            raise AssertionError("fleet_exit needs fleet_text")
        return subprocess.run(
            ["bash", str(SCRIPT), *args],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )


def _fleet_echo_exit(code: int) -> str:
    return (
        "#!/bin/sh\n"
        f"printf '%s\\n' '{FLEET_STAMP}'\n"
        "printf 'ARGV:%s\\n' \"$*\"\n"
        f"exit {code}\n"
    )


class QuietTestWrapTests(unittest.TestCase):
    def test_script_is_executable(self) -> None:
        self.assertTrue(SCRIPT.is_file(), "scripts/quiet-test.sh is the WRAP")
        self.assertTrue(os.access(SCRIPT, os.X_OK), "WRAP must be executable")

    def test_given_fleet_present_when_cmd_exits_nonzero_then_wrap_exits_same(self) -> None:
        proc = _run(
            ["--", "sh", "-c", "exit 0"],
            fleet_text=_fleet_echo_exit(7),
        )
        self.assertEqual(proc.returncode, 7, proc.stderr)
        self.assertIn(FLEET_STAMP, proc.stdout)

    def test_given_fleet_present_when_invoked_then_fleet_receives_original_argv(self) -> None:
        proc = _run(
            ["--", "python3", "-c", "print(1)"],
            fleet_text=_fleet_echo_exit(0),
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("ARGV:-- python3 -c print(1)", proc.stdout)

    def test_given_fleet_absent_when_cmd_exits_nonzero_then_wrap_exits_same(self) -> None:
        proc = _run(["--", "sh", "-c", "exit 3"])
        self.assertEqual(proc.returncode, 3, proc.stderr)
        self.assertNotIn(FLEET_STAMP, proc.stdout)

    def test_given_fleet_absent_when_cmd_exits_zero_then_wrap_exits_zero(self) -> None:
        proc = _run(["--", "sh", "-c", "exit 0"])
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_quiet_is_not_skip_failing_cmd_still_fails(self) -> None:
        proc = _run(["--", "false"])
        self.assertNotEqual(proc.returncode, 0, "quiet must not hide a failing cmd")

    def test_wrap_source_does_not_invent_quiet_body(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        for marker in HARNESS_MARKERS:
            self.assertNotIn(marker, text, f"WRAP must not invent {marker}")
        self.assertIn("/workspace/fleet-scripts/quiet-test.sh", text)
        self.assertIn("exec", text)

    def test_given_no_args_when_fleet_absent_then_wrap_exits_2(self) -> None:
        proc = _run([])
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertIn("fleet missing", proc.stderr)

    def test_given_success_cmd_when_fleet_prints_many_lines_then_wrap_does_not_trim(
        self,
    ) -> None:
        fleet = (
            "#!/bin/sh\n"
            "i=1\n"
            "while [ \"$i\" -le 20 ]; do\n"
            "  printf 'LINE-%s\\n' \"$i\"\n"
            "  i=$((i + 1))\n"
            "done\n"
            "exit 0\n"
        )
        proc = _run(["--", "sh", "-c", "exit 0"], fleet_text=fleet)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        lines = [ln for ln in proc.stdout.splitlines() if ln.startswith("LINE-")]
        self.assertEqual(len(lines), 20, "WRAP must not invent SUCCESS tail")

    def test_hook_and_gha_invoke_wrap(self) -> None:
        hook = HOOK.read_text(encoding="utf-8")
        gha = GHA.read_text(encoding="utf-8")
        self.assertIn("quiet-test.sh", hook)
        self.assertIn("quiet-test.sh", gha)
        self.assertIn('"--", "python3", "scripts/ci.py"', hook)
        self.assertIn("./scripts/quiet-test.sh -- python3 scripts/ci.py", gha)


if __name__ == "__main__":
    unittest.main()
