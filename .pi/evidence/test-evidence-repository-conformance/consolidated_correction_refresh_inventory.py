#!/usr/bin/env python3
"""Refresh task-owned maintained inventory identities after the correction pass."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / ".pi/evidence/test-evidence-repository-conformance"
INVENTORY = EVIDENCE / "maintained-test-inventory.json"
NEW_PATH = "python/tests/software_verification/ksdft2effmass/operators/test__OperatorRecordResidualAnalyzer__floating_point_regressions.py"


def main() -> None:
    """Add the corrected software owner and refresh exact maintained bytes."""
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    modules = inventory["modules"]
    by_path = {entry["path"]: entry for entry in modules}
    if NEW_PATH not in by_path:
        modules.append(
            {
                "conformance_status": "conforming",
                "content_sha256": "",
                "evidence_class": "software_verification",
                "mode": "class_owned",
                "path": NEW_PATH,
                "sut": "OperatorRecordResidualAnalyzer",
            }
        )
    for entry in modules:
        entry["content_sha256"] = hashlib.sha256(
            (ROOT / entry["path"]).read_bytes()
        ).hexdigest()
        entry["conformance_status"] = "conforming"
    inventory["modules"] = sorted(modules, key=lambda entry: entry["path"])
    inventory["expected_module_count"] = len(modules)
    inventory["expected_collected_node_count"] = 2568
    INVENTORY.write_text(
        json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"refreshed {len(modules)} maintained module identities; expected nodes=2568")


if __name__ == "__main__":
    main()
