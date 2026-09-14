#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QUERY = ROOT / "scripts" / "ui_library" / "query.py"
QUIET = ROOT / "scripts" / "quiet-test.sh"


def _run_query(args: list[str]) -> subprocess.CompletedProcess[str]:
    cmd = [str(QUIET), "--", sys.executable, str(QUERY), *args]
    return subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, check=False)


class TestQueryCli(unittest.TestCase):
    def test_search_view_examples_exit_zero(self):
        for args in (
            ["search", "ui.shadcn.com/blocks", "--use-case", "landing"],
            ["view", "ref-fixture-x-ui-blocks-hero"],
            ["examples", "FIXTURE", "--use-case", "landing"],
        ):
            proc = _run_query(args)
            self.assertEqual(
                proc.returncode, 0, msg=f"{args}: stderr={proc.stderr} stdout={proc.stdout}"
            )
            payload = json.loads(proc.stdout)
            self.assertIn("mcpTool", payload)

    def test_view_includes_meta_fleet_source_url(self):
        proc = _run_query(["view", "ref-seed-buddy-taiyo-find-index-mcp"])
        self.assertEqual(proc.returncode, 0)
        payload = json.loads(proc.stdout)
        item = payload["item"]
        self.assertEqual(
            item["meta"]["fleet"]["sourceUrl"], "https://ui.shadcn.com/docs/mcp"
        )

    def test_not_found_returns_nonzero(self):
        proc = _run_query(["view", "no-such-item-name"])
        self.assertNotEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
