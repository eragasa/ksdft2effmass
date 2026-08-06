#!/usr/bin/env python3
"""Validate the bounded P2-A02 provenance-audit correction evidence."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / ".pi/evidence/backend-neutral-cpn-P2-tools-provenance"
QUEUE = EVIDENCE / "provenance-audit-queue.json"
OWNERSHIP = EVIDENCE / "p2-a02-test-evidence-ownership.json"
MIGRATION = EVIDENCE / "p2-a02-test-evidence-node-migration.json"
INVENTORY = EVIDENCE / "p2-a02-test-evidence-inventory.json"
IMPLEMENTATION = EVIDENCE / "p2-a02-test-evidence-implementation.md"
REVIEW = EVIDENCE / "p2-a02-review.md"
COMPLETION = EVIDENCE / "p2-a02-completion.json"
PARENT = EVIDENCE / "p2-a02-parent-verification.md"
EXPECTED_IDS = tuple(f"P2-A{index:02d}" for index in range(12))
EXPECTED_PATHS = (
    "python/tests/software_verification/ksdft2effmass/provenance/test__VerificationStatus.py",
    "python/tests/software_verification/ksdft2effmass/provenance/test__InstallationObservation.py",
    "python/tests/software_verification/ksdft2effmass/provenance/test__VerificationObservation.py",
)


def load(path: Path, issues: list[str]) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        issues.append(f"missing or invalid JSON: {path.relative_to(ROOT)}")
        return {}
    if not isinstance(value, dict):
        issues.append(f"JSON root is not an object: {path.relative_to(ROOT)}")
        return {}
    return value


def main() -> int:
    issues: list[str] = []
    queue = load(QUEUE, issues)
    items = queue.get("items", [])
    if not isinstance(items, list) or tuple(
        item.get("id") for item in items if isinstance(item, dict)
    ) != EXPECTED_IDS:
        issues.append("queue must contain exactly ordered P2-A00--P2-A11")
        items = []
    statuses: dict[object, object] = {}
    if items:
        statuses = {item["id"]: item.get("final_status") for item in items}
        if statuses.get("P2-A00") != "audited_and_cleared":
            issues.append("P2-A00 must be audited_and_cleared")
        if statuses.get("P2-A01") != "audited_and_cleared":
            issues.append("P2-A01 must be audited_and_cleared")
        if statuses.get("P2-A02") not in {
            "bounded_correction_active",
            "deterministic_validation_passed",
            "targeted_review_complete",
            "audited_and_cleared",
        }:
            issues.append("P2-A02 must be active, validated, reviewed, or cleared")
        if statuses.get("P2-A03") != "pending_read_only_audit":
            issues.append("P2-A03 must remain pending_read_only_audit")
        if any(
            statuses.get(f"P2-A{i:02d}") != "pending_read_only_audit"
            for i in range(4, 7)
        ):
            issues.append("P2-A04--P2-A06 must remain pending_read_only_audit")
        if any(
            statuses.get(f"P2-A{i:02d}") != "pending_artifact_audit"
            for i in range(7, 12)
        ):
            issues.append("P2-A07--P2-A11 must remain pending_artifact_audit")
        cleared = statuses.get("P2-A02") == "audited_and_cleared"
        expected_active = None if cleared else "P2-A02"
        expected_next = "P2-A03" if cleared else None
        if queue.get("active_item") != expected_active:
            issues.append("queue active_item does not match P2-A02 state")
        if queue.get("next_item") != expected_next:
            issues.append("queue next_item does not match P2-A02 state")

    ownership = load(OWNERSHIP, issues)
    modules = ownership.get("modules", [])
    if not isinstance(modules, list) or tuple(
        item.get("path") for item in modules if isinstance(item, dict)
    ) != EXPECTED_PATHS:
        issues.append("P2-A02 ownership must cover exactly three ordered paths")

    migration = load(MIGRATION, issues)
    old = migration.get("expected_old_node_ids", [])
    new = migration.get("expected_new_node_ids", [])
    mappings = migration.get("mappings", [])
    if not all(isinstance(value, list) for value in (old, new, mappings)):
        issues.append("P2-A02 migration inventories must be lists")
    elif (
        len(old) != len(set(old))
        or len(new) != len(set(new))
        or {item.get("old_node_id") for item in mappings if isinstance(item, dict)}
        != set(old)
        or {item.get("new_node_id") for item in mappings if isinstance(item, dict)}
        != set(new)
        or len(mappings) != len(old)
        or len(old) != len(new)
    ):
        issues.append("P2-A02 migration must be complete and one-to-one")

    inventory = load(INVENTORY, issues)
    if inventory.get("paths") != list(EXPECTED_PATHS):
        issues.append("P2-A02 inventory paths do not match ownership")
    counts = inventory.get("counts", {})
    if not isinstance(counts, dict) or counts.get("historical_old_nodes") != len(old):
        issues.append("P2-A02 inventory historical count does not match migration")
    if isinstance(counts, dict) and counts.get("migration_new_nodes") != len(new):
        issues.append("P2-A02 inventory mapped count does not match migration")

    if not IMPLEMENTATION.is_file():
        issues.append(f"missing P2-A02 evidence record: {IMPLEMENTATION.relative_to(ROOT)}")
    if items and statuses.get("P2-A02") == "audited_and_cleared":
        for path in (REVIEW, COMPLETION, PARENT):
            if not path.is_file():
                issues.append(
                    f"missing cleared P2-A02 evidence record: {path.relative_to(ROOT)}"
                )

    result = {
        "schema_version": 1,
        "task_id": "P2",
        "audit_item": "P2-A02",
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "observed": {
            "queue_items": len(items),
            "owned_modules": len(modules) if isinstance(modules, list) else 0,
            "mapped_nodes": len(mappings) if isinstance(mappings, list) else 0,
            "collected_nodes": counts.get("collected_cases")
            if isinstance(counts, dict)
            else None,
        },
    }
    print(json.dumps(result, ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
