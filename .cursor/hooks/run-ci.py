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


def append_proof(payload: dict, ci_exit: int) -> None:
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "hook_event_name": payload.get("hook_event_name"),
        "ci_exit": ci_exit,
        "hook_path": HOOK_PATH,
    }
    if "conversation_id" in payload:
        record["conversation_id"] = payload["conversation_id"]
    if "tool_name" in payload:
        record["tool_name"] = payload["tool_name"]
    try:
        with PROOF_LOG.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError:
        pass


def fail_message(output: str) -> str:
    body = output if len(output) <= MAX_OUTPUT else output[:MAX_OUTPUT] + "\n...[truncated]"
    return "python3 scripts/ci.py failed\n" + body


def main() -> int:
    payload = drain_stdin()
    ci_exit, output = run_ci(repo_root())
    append_proof(payload, ci_exit)
    event = str(payload.get("hook_event_name") or "").lower()
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
    if ci_exit != 0:
        print(
            json.dumps(
                {"permission": "deny", "agent_message": fail_message(output)},
                ensure_ascii=False,
            ),
            flush=True,
        )
        return 2
    print(json.dumps({"permission": "allow"}), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
