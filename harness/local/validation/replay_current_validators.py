#!/usr/bin/env -S python/.venv/bin/python
"""Replay the maintained current local resource validators without H4 catalogs."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

CHECKS = (
    (
        "current-h3-resources",
        "harness/pi/validation/validate_h3_resources.py",
        "RESOURCE VALIDATION PASS",
    ),
    (
        "current-skill-capabilities",
        ".pi/skills/validate_skill_capabilities.py",
        "validation_errors=0",
    ),
    (
        "current-architecture-decision-cases",
        "harness/pi/validation/validate_architecture_decision_cases.py",
        '"status":"PASS"',
    ),
    (
        "current-task-schema-projection",
        "harness/local/validation/validate_task_schema_projection.py",
        '"status":"PASS"',
    ),
)


def emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True))


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] != "--repository-root":
        emit(
            {
                "schema_version": 1,
                "side": "local",
                "status": "FAIL",
                "checks": [],
                "error": "arguments-invalid",
            }
        )
        return 2
    root = Path(sys.argv[2])
    if not root.is_absolute() or not root.is_dir():
        emit(
            {
                "schema_version": 1,
                "side": "local",
                "status": "FAIL",
                "checks": [],
                "error": "repository-root-invalid",
            }
        )
        return 2
    checks: list[dict[str, Any]] = []
    for check_id, relative, required_output in CHECKS:
        target = root / relative
        if not target.is_file() or target.is_symlink():
            checks.append({"check_id": check_id, "exit_status": 127, "status": "FAIL"})
            continue
        try:
            command = [sys.executable, str(target)]
            if check_id == "current-task-schema-projection":
                explicit_paths = {
                    "generic-validator": "harness/pi/validation/validate_documentation_projection.py",
                    "task-schema": "harness/local/schemas/task-record.schema.json",
                    "profile-schema": "harness/pi/schemas/documentation-projection-profile.schema.json",
                    "profile": "harness/local/projections/task-control-reference-v1.json",
                    "task": ".pi/tasks/harness.simplification.docs-json.schema-projection.json",
                    "chain": ".pi/chains/harness-simplification.chain.json",
                    "expected": "harness/local/fixtures/task-control-reference/expected/harness.simplification.docs-json.schema-projection.md",
                    "generated": ".pi/tasks/harness.simplification.docs-json.schema-projection.md",
                    "oracle-index": "harness/local/fixtures/oracle-index.json",
                    "fixtures-root": "harness/local/fixtures/task-record",
                }
                for name, relative_path in explicit_paths.items():
                    command.extend((f"--{name}", str(root / relative_path)))
                command.extend(
                    (
                        "--task-record-path",
                        ".pi/tasks/harness.simplification.docs-json.schema-projection.json",
                    )
                )
            completed = subprocess.run(
                command,
                cwd=root,
                env={**os.environ, "PYTHONHASHSEED": "0", "PYTHONIOENCODING": "utf-8"},
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError:
            checks.append({"check_id": check_id, "exit_status": 127, "status": "FAIL"})
            continue
        passed = completed.returncode == 0 and required_output in completed.stdout
        checks.append(
            {
                "check_id": check_id,
                "exit_status": completed.returncode,
                "status": "PASS" if passed else "FAIL",
            }
        )
    passed = len(checks) == len(CHECKS) and all(
        item["status"] == "PASS" for item in checks
    )
    emit(
        {
            "checks": checks,
            "schema_version": 1,
            "side": "local",
            "status": "PASS" if passed else "FAIL",
        }
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
