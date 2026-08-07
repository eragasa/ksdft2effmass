#!/usr/bin/env python3
"""Validate bounded completion of ARCHITECTURE-DECISION-SKILL-1."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
START = "3927d41b93e6be480e9c29013984b9385808ad4c"
TASK = "ARCHITECTURE-DECISION-SKILL-1"
CHAIN = ".pi/chains/develop-architecture-decision-skill.chain.json"
EVIDENCE = ".pi/evidence/develop-architecture-decision-skill"
REQUIRED = (
    ".pi/tasks/develop-architecture-decision-skill.md",
    CHAIN,
    f"{EVIDENCE}/activation.json",
    f"{EVIDENCE}/task-ownership.json",
    f"{EVIDENCE}/validate_completion.py",
    "harness/pi/skills/develop-architecture-decision/SKILL.md",
    "harness/pi/skills/develop-architecture-decision/descriptor.json",
    "harness/pi/skills/develop-architecture-decision/references/architecture-decision-conventions.md",
    "harness/pi/fixtures/architecture-decision/cases.json",
    "harness/pi/validation/validate_architecture_decision_cases.py",
    ".pi/skills/develop-architecture-decision/SKILL.md",
    ".pi/skills/develop-architecture-decision/references/architecture-decision-conventions.md",
)
FORBIDDEN_PREFIXES = (
    ".pi/agents/",
    ".pi/checkpoints/P2-",
    ".pi/evidence/backend-neutral-cpn-P2-tools-provenance/",
    ".pi/evidence/pi-harness-incubation/H4/",
    "python/",
    "specification/",
    "fixtures/",
)
FORBIDDEN_EXACT = {
    "package-lock.json",
    "python/pyproject.toml",
    "harness/local/validation-route.json",
    ".pi/task-ownership/validate_task_ownership.py",
}


def run(arguments: list[str]) -> tuple[int, str, str]:
    completed = subprocess.run(
        arguments,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return completed.returncode, completed.stdout, completed.stderr


def main() -> int:
    issues: list[str] = []
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            issues.append(f"missing required file: {relative}")

    canonical = ROOT / "harness/pi/skills/develop-architecture-decision"
    live = ROOT / ".pi/skills/develop-architecture-decision"
    for relative in ("SKILL.md", "references/architecture-decision-conventions.md"):
        if (
            (canonical / relative).is_file()
            and (live / relative).is_file()
            and (canonical / relative).read_bytes() != (live / relative).read_bytes()
        ):
            issues.append(f"canonical/live byte mismatch: {relative}")

    chain = json.loads((ROOT / CHAIN).read_text(encoding="utf-8"))
    matches = [
        item for item in chain.get("task_sequence", []) if item.get("id") == TASK
    ]
    if len(matches) != 1:
        issues.append("chain must contain exactly one task")
    checkpoint = (
        ROOT
        / ".pi/checkpoints/ARCHITECTURE-DECISION-SKILL-1-HC01-final-acceptance.json"
    )
    if checkpoint.exists():
        record = json.loads(checkpoint.read_text(encoding="utf-8"))
        expected_chain_status = {
            "pending": "pending_human_acceptance",
            "resolved": "closed_human_accepted_pass",
        }.get(record.get("status"))
        if (
            expected_chain_status is None
            or chain.get("status") != expected_chain_status
        ):
            issues.append("final checkpoint and chain lifecycle status disagree")
        if record.get("status") == "resolved" and (
            record.get("normalized_decision") != "A"
            or chain.get("active_task") is not None
            or matches[0].get("status") != "closed_human_accepted_pass"
        ):
            issues.append("resolved Option A does not close only the skill task")
    elif chain.get("status") != "active":
        issues.append("pre-checkpoint chain must remain active")

    changed_result = run(["git", "diff", "--name-only", START, "--"])
    untracked_result = run(["git", "ls-files", "--others", "--exclude-standard"])
    if changed_result[0] != 0 or untracked_result[0] != 0:
        issues.append("cannot determine changed paths from starting revision")
        changed: list[str] = []
    else:
        changed = sorted(
            {line for line in changed_result[1].splitlines() if line}
            | {line for line in untracked_result[1].splitlines() if line}
        )
    for path in changed:
        if path in FORBIDDEN_EXACT or any(
            path.startswith(prefix) for prefix in FORBIDDEN_PREFIXES
        ):
            issues.append(f"forbidden path changed: {path}")

    for path in changed:
        candidate = ROOT / path
        if candidate.suffix == ".json" and candidate.is_file():
            try:
                json.loads(candidate.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError) as error:
                issues.append(f"invalid JSON {path}: {error}")
        if candidate.suffix == ".md" and candidate.is_file():
            text = candidate.read_text(encoding="utf-8")
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                target = target.split("#", 1)[0]
                if not target or "://" in target or target.startswith(("#", "$")):
                    continue
                if not (candidate.parent / target).resolve().exists():
                    issues.append(f"broken Markdown link {path}: {target}")

    commands = (
        (
            [
                sys.executable,
                ".pi/task-ownership/validate_task_ownership.py",
                "--task",
                TASK,
                "--chain",
                CHAIN,
            ],
            "task ownership preflight passed",
        ),
        (
            [
                sys.executable,
                "harness/pi/validation/validate_architecture_decision_cases.py",
            ],
            '"status":"PASS"',
        ),
        (
            [sys.executable, "harness/pi/validation/validate_h3_resources.py"],
            "RESOURCE VALIDATION PASS",
        ),
        (
            [sys.executable, ".pi/skills/validate_skill_capabilities.py"],
            "validation_errors=0",
        ),
        (
            [
                sys.executable,
                ".pi/skills/validate_harness.py",
                "--repository-root",
                str(ROOT),
                "--route-config",
                str(ROOT / "harness/local/validation-route.json"),
            ],
            '"status":"PASS"',
        ),
        (["git", "diff", "--check", START, "--"], ""),
    )
    command_results: list[dict[str, object]] = []
    for arguments, expected in commands:
        status, stdout, stderr = run(arguments)
        passed = status == 0 and (not expected or expected in stdout)
        command_results.append(
            {
                "command": arguments,
                "exit_status": status,
                "status": "PASS" if passed else "FAIL",
            }
        )
        if not passed:
            issues.append(
                f"command failed: {' '.join(arguments)}: {(stdout + stderr).strip()}"
            )

    payload = {
        "schema_version": 1,
        "task_id": TASK,
        "starting_revision": START,
        "status": "PASS" if not issues else "FAIL",
        "changed_paths": changed,
        "commands": command_results,
        "issues": issues,
    }
    print(json.dumps(payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
