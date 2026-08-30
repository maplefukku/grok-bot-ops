#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROOF_LOG = Path("/tmp/grok-bot-ops-cursor-hooks.log")
HOOK_PATH = ".cursor/hooks/run-ci.py"
MAX_OUTPUT = 8000
MUTATION_TOOLS = {
    "write",
    "strreplace",
    "delete",
    "editnotebook",
    "edit",
    "applypatch",
    "writefile",
    "deletefile",
}


def drain_stdin() -> dict:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def repo_root() -> Path:
    env = os.environ.get("CURSOR_PROJECT_DIR")
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[2]


def run_ci(root: Path) -> tuple[int, str]:
    proc = subprocess.run(
        ["python3", "scripts/ci.py"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def should_run_ci(event: str, payload: dict) -> bool:
    if event == "stop":
        return True
    if event != "pretooluse":
        return False
    name = str(payload.get("tool_name") or "").casefold()
    if not name:
        return True
    return name in MUTATION_TOOLS


def append_proof(root: Path, record: dict) -> None:
    line = json.dumps(record, ensure_ascii=False) + "\n"
    for path in (PROOF_LOG, root / ".git" / "cursor-hooks-fired.log"):
        try:
            with path.open("a", encoding="utf-8") as fh:
                fh.write(line)
        except OSError:
            pass


def fail_message(output: str) -> str:
    body = output if len(output) <= MAX_OUTPUT else output[:MAX_OUTPUT] + "\n...[truncated]"
    return "python3 scripts/ci.py failed\n" + body


def main() -> int:
    payload = drain_stdin()
    root = repo_root()
    event = str(payload.get("hook_event_name") or "").lower()
    ran = should_run_ci(event, payload)
    ci_exit = 0
    output = ""
    if ran:
        ci_exit, output = run_ci(root)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "hook_event_name": payload.get("hook_event_name"),
        "ci_exit": ci_exit,
        "ran_ci": ran,
        "hook_path": HOOK_PATH,
    }
    for key in ("conversation_id", "generation_id", "tool_name", "cursor_version"):
        if key in payload:
            record[key] = payload[key]
    append_proof(root, record)
    if event == "stop":
        if ci_exit != 0:
            print(
                json.dumps(
                    {"followup_message": fail_message(output)},
                    ensure_ascii=False,
                ),
                flush=True,
            )
        else:
            print("{}", flush=True)
        return 0
    print(json.dumps({"permission": "allow"}), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
