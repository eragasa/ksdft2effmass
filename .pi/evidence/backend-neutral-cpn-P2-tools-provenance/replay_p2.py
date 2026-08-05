#!/usr/bin/env python3
"""Execute the single bounded P2 replay against immutable input identities."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
INPUTS = Path(__file__).with_name("replay-inputs.json")
OUTPUT = Path(__file__).with_name("replay-evidence.json")


def main() -> int:
    specification = json.loads(INPUTS.read_text(encoding="utf-8"))
    mismatches: list[str] = []
    for item in specification["inputs"]:
        path = ROOT / item["path"]
        observed = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
        if observed != item["sha256"]:
            mismatches.append(item["path"])
    observations: list[dict[str, Any]] = []
    if not mismatches:
        environment = os.environ.copy()
        environment["PYTHONPATH"] = str(ROOT / "python/src")
        environment["MYPYPATH"] = str(ROOT / "python/src")
        for command in specification["commands"]:
            completed = subprocess.run(
                command,
                cwd=ROOT,
                env=environment,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                check=False,
            )
            observations.append(
                {
                    "command": command,
                    "exit_status": completed.returncode,
                    "stdout_sha256": hashlib.sha256(completed.stdout.encode()).hexdigest(),
                    "stderr_sha256": hashlib.sha256(completed.stderr.encode()).hexdigest(),
                }
            )
    passed = not mismatches and all(item["exit_status"] == 0 for item in observations)
    result = {
        "schema_version": 1,
        "task_id": "P2",
        "replay_id": specification["replay_id"],
        "input_set_sha256": hashlib.sha256(INPUTS.read_bytes()).hexdigest(),
        "input_mismatches": mismatches,
        "observations": observations,
        "status": "PASS" if passed else "FAIL",
        "claim_boundary": "software verification only; no numerical verification, scientific validation, uncertainty quantification, external execution, publication, or release",
    }
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
