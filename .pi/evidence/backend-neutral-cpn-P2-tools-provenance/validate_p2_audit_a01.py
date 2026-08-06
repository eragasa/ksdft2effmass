#!/usr/bin/env python3
"""Validate the bounded P2 provenance audit queue and completed A01 evidence."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / ".pi/evidence/backend-neutral-cpn-P2-tools-provenance"
QUEUE = EVIDENCE / "provenance-audit-queue.json"
OWNERSHIP = EVIDENCE / "audit-a01-test-evidence-ownership.json"
MIGRATION = EVIDENCE / "audit-a01-test-evidence-node-migration.json"
INVENTORY = EVIDENCE / "audit-a01-test-evidence-inventory.json"
IMPLEMENTATION = EVIDENCE / "audit-a01-test-evidence-implementation.md"
REVIEW = EVIDENCE / "audit-a01-review.md"
COMPLETION = EVIDENCE / "audit-a01-completion.json"
PARENT = EVIDENCE / "audit-a01-parent-verification.md"
EXPECTED_IDS = tuple(f"A{index:02d}" for index in range(12))
EXPECTED_PATHS = (
    "python/tests/software_verification/ksdft2effmass/provenance/test__CapabilityKind.py",
    "python/tests/software_verification/ksdft2effmass/provenance/test__ExternalToolIdentity.py",
    "python/tests/software_verification/ksdft2effmass/provenance/test__ExternalToolSpecification.py",
    "python/tests/software_verification/ksdft2effmass/provenance/test__DeclaredCapability.py",
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
        issues.append("queue must contain exactly ordered A00-A11")
        items = []
    if items:
        statuses = {item["id"]: item.get("final_status") for item in items}
        if statuses.get("A00") != "audited_and_cleared":
            issues.append("A00 must be audited_and_cleared")
        if statuses.get("A01") not in {
            "corrected_pending_recheck",
            "audited_and_cleared",
        }:
            issues.append("A01 must be corrected_pending_recheck or audited_and_cleared")
        if any(statuses.get(f"A{i:02d}") != "pending_read_only_audit" for i in range(2, 7)):
            issues.append("A02-A06 must remain pending_read_only_audit")
        if any(statuses.get(f"A{i:02d}") != "pending_artifact_audit" for i in range(7, 12)):
            issues.append("A07-A11 must remain pending_artifact_audit")
        if queue.get("next_item") != "A02":
            issues.append("A02 must be next")
    ownership = load(OWNERSHIP, issues)
    modules = ownership.get("modules", [])
    if not isinstance(modules, list) or tuple(
        item.get("path") for item in modules if isinstance(item, dict)
    ) != EXPECTED_PATHS:
        issues.append("A01 ownership must cover exactly four ordered paths")
    migration = load(MIGRATION, issues)
    old = migration.get("expected_old_node_ids", [])
    new = migration.get("expected_new_node_ids", [])
    mappings = migration.get("mappings", [])
    if not all(isinstance(value, list) for value in (old, new, mappings)):
        issues.append("A01 migration inventories must be lists")
    elif (
        len(old) != len(set(old))
        or len(new) != len(set(new))
        or {item.get("old_node_id") for item in mappings if isinstance(item, dict)} != set(old)
        or {item.get("new_node_id") for item in mappings if isinstance(item, dict)} != set(new)
        or len(mappings) != len(old)
        or len(old) != len(new)
    ):
        issues.append("A01 migration must be complete and one-to-one")
    inventory = load(INVENTORY, issues)
    if inventory.get("paths") != list(EXPECTED_PATHS):
        issues.append("A01 inventory paths do not match ownership")
    if not IMPLEMENTATION.is_file():
        issues.append(f"missing A01 evidence record: {IMPLEMENTATION.relative_to(ROOT)}")
    if items and statuses.get("A01") == "audited_and_cleared":
        for path in (REVIEW, COMPLETION, PARENT):
            if not path.is_file():
                issues.append(
                    f"missing cleared A01 evidence record: {path.relative_to(ROOT)}"
                )
    checkpoint = load(ROOT / ".pi/checkpoints/P2-HC05-final-acceptance.json", issues)
    if checkpoint.get("status") != "pending":
        issues.append("P2-HC05 must remain pending")
    result = {
        "schema_version": 1,
        "task_id": "P2",
        "audit_item": "A01",
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "observed": {
            "queue_items": len(items),
            "owned_modules": len(modules) if isinstance(modules, list) else 0,
            "mapped_nodes": len(mappings) if isinstance(mappings, list) else 0,
            "collected_nodes": inventory.get("counts", {}).get("collected_cases")
            if isinstance(inventory.get("counts"), dict)
            else None,
        },
    }
    print(json.dumps(result, ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
