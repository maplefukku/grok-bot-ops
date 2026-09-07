#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT / ".github"
CI_YML = GITHUB / "workflows" / "ci.yml"
DEPENDABOT = GITHUB / "dependabot.yml"
CODEOWNERS = GITHUB / "CODEOWNERS"
CODEQL = GITHUB / "workflows" / "codeql.yml"
SCORECARD = GITHUB / "workflows" / "scorecard.yml"
RULESET = GITHUB / "rulesets" / "main-pr-only.json"

FORBIDDEN = (
    ROOT / "renovate.json",
    GITHUB / "renovate.json",
    ROOT / ".renovaterc",
    GITHUB / "workflows" / "merge-queue.yml",
    GITHUB / "merge-queue.yml",
    GITHUB / "secret_scanning.yml",
    GITHUB / "workflows" / "secret-scanning.yml",
)

DEPENDABOT_NEEDLES = (
    "version: 2",
    "package-ecosystem: github-actions",
    "directory: /",
    "interval: weekly",
)

CODEOWNERS_NEEDLES = ("@maplefukku",)
CODEQL_NEEDLES = (
    "github/codeql-action/init@",
    "github/codeql-action/analyze@",
    "language: python",
    "build-mode: none",
)
SCORECARD_NEEDLES = (
    "ossf/scorecard-action@",
    "results_format: sarif",
    "results_file: results.sarif",
    "publish_results: false",
    "contents: read",
    "actions: read",
)
CI_NEEDLES = (
    "check:",
    "./scripts/quiet-test.sh -- python3 scripts/ci.py",
)
FORBIDDEN_ECOSYSTEMS = (
    "package-ecosystem: npm",
    "package-ecosystem: pip",
    "package-ecosystem: docker",
    "package-ecosystem: gomod",
    "package-ecosystem: bundler",
    "package-ecosystem: cargo",
    "package-ecosystem: composer",
)
SCORECARD_FAIL_TOKENS = ("fail-on:", "fail_on:", "publish_results: true")
HOLD_TOKENS = (
    "secret_scanning",
    "secret-scanning",
    "GHAS",
    "push_protection",
    "push-protection",
)
RENOVATE_TOKENS = ("renovate", "merge-queue", "merge_queue", "Merge Queue")


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def wrap_errors() -> list[str]:
    errors: list[str] = []
    for path, needles in (
        (DEPENDABOT, DEPENDABOT_NEEDLES),
        (CODEOWNERS, CODEOWNERS_NEEDLES),
        (CODEQL, CODEQL_NEEDLES),
        (CI_YML, CI_NEEDLES),
    ):
        if not path.is_file():
            errors.append(f"missing {path.relative_to(ROOT)}")
            continue
        body = _text(path)
        for needle in needles:
            if needle not in body:
                errors.append(f"{path.relative_to(ROOT)}: missing {needle}")
    if not RULESET.is_file():
        errors.append(f"missing {RULESET.relative_to(ROOT)}")
    else:
        try:
            payload = json.loads(_text(RULESET))
        except json.JSONDecodeError as exc:
            errors.append(f"{RULESET.relative_to(ROOT)}: {exc}")
        else:
            errors.extend(ruleset_errors(payload))
    dep = _text(DEPENDABOT)
    for token in FORBIDDEN_ECOSYSTEMS:
        if token in dep:
            errors.append(f"dependabot.yml invents {token}")
    if not SCORECARD.is_file():
        errors.append(f"missing {SCORECARD.relative_to(ROOT)}")
        score_active = ""
    else:
        score_active = "\n".join(
            line
            for line in _text(SCORECARD).splitlines()
            if not line.lstrip().startswith("#")
        )
        for needle in SCORECARD_NEEDLES:
            if needle not in score_active:
                errors.append(f"{SCORECARD.relative_to(ROOT)}: missing {needle}")
    for token in SCORECARD_FAIL_TOKENS:
        if token in score_active:
            errors.append(f"scorecard.yml is not report-only: {token}")
    for path in FORBIDDEN:
        if path.exists():
            errors.append(f"SKIP target present: {path.relative_to(ROOT)}")
    for path in (CODEQL, SCORECARD, DEPENDABOT, RULESET, CODEOWNERS, CI_YML):
        body = _text(path)
        for token in RENOVATE_TOKENS + HOLD_TOKENS:
            if token in body:
                errors.append(f"{path.relative_to(ROOT)} mentions {token}")
    return errors


def ruleset_errors(payload: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["ruleset is not an object"]
    if payload.get("name") != "main-pr-only":
        errors.append("ruleset name is not main-pr-only")
    include = payload.get("conditions", {}).get("ref_name", {}).get("include", [])
    if "refs/heads/main" not in include:
        errors.append("ruleset does not target refs/heads/main")
    contexts: list[str] = []
    for rule in payload.get("rules", []):
        if not isinstance(rule, dict):
            continue
        if rule.get("type") != "required_status_checks":
            continue
        for check in rule.get("parameters", {}).get("required_status_checks", []):
            if isinstance(check, dict) and check.get("context"):
                contexts.append(str(check["context"]))
    if contexts != ["check"]:
        errors.append(
            f"ruleset required checks must be exactly [check], got {contexts}"
        )
    return errors


COMPLETE_RULESET = {
    "name": "main-pr-only",
    "conditions": {"ref_name": {"include": ["refs/heads/main"]}},
    "rules": [
        {
            "type": "required_status_checks",
            "parameters": {"required_status_checks": [{"context": "check"}]},
        }
    ],
}


class DevopsWrapTests(unittest.TestCase):
    def test_wrap_files_match_registry(self) -> None:
        self.assertEqual(wrap_errors(), [])

    def test_parser_accepts_complete_fixture(self) -> None:
        self.assertEqual(ruleset_errors(COMPLETE_RULESET), [])

    def test_parser_rejects_wrong_required_check(self) -> None:
        broken = {
            "name": "main-pr-only",
            "conditions": {"ref_name": {"include": ["refs/heads/main"]}},
            "rules": [
                {
                    "type": "required_status_checks",
                    "parameters": {
                        "required_status_checks": [{"context": "CI"}]
                    },
                }
            ],
        }
        found = ruleset_errors(broken)
        self.assertTrue(found)
        self.assertTrue(any("check" in item for item in found))


if __name__ == "__main__":
    unittest.main()
