#!/usr/bin/env python3
"""Build deterministic M4 node-migration and new-owner artifacts from collections."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / ".pi/evidence/test-evidence-repository-conformance"


def module(node: str) -> str:
    """Return the module path portion of a pytest node ID."""
    return node.split("::", 1)[0]


def load_nodes(path: Path) -> list[str]:
    """Load exact nonempty pytest node IDs in collection order."""
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]


def dump(name: str, value: object) -> None:
    """Write one stable indented JSON artifact."""
    (OUT / name).write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> None:
    """Pair old and new nodes within each module and isolate genuinely new nodes."""
    parser = argparse.ArgumentParser()
    parser.add_argument("old", type=Path)
    parser.add_argument("new", type=Path)
    args = parser.parse_args()
    old = load_nodes(args.old)
    new = load_nodes(args.new)
    old_groups: dict[str, list[str]] = defaultdict(list)
    new_groups: dict[str, list[str]] = defaultdict(list)
    for node in old:
        old_groups[module(node)].append(node)
    for node in new:
        normalized = "python/" + node if node.startswith("tests/") else node
        new_groups[module(normalized)].append(normalized)
    mappings: list[dict[str, str]] = []
    additions: list[str] = []
    for path in sorted(old_groups):
        old_nodes = old_groups[path]
        new_nodes = new_groups[path]
        if len(new_nodes) < len(old_nodes):
            raise ValueError(
                f"node loss for {path}: {len(old_nodes)} -> {len(new_nodes)}"
            )
        mappings.extend(
            {"old_node_id": before, "new_node_id": after}
            for before, after in zip(old_nodes, new_nodes, strict=False)
        )
        additions.extend(new_nodes[len(old_nodes) :])
    if set(new_groups) != set(old_groups):
        raise ValueError("M4 module inventory changed")
    dump("m4-historical-node-inventory.json", {"schema_version": 1, "node_ids": old})
    before_hashes = {
        path: hashlib.sha256(
            subprocess.check_output(["git", "show", f"HEAD:{path}"], cwd=ROOT)
        ).hexdigest()
        for path in sorted(old_groups)
    }
    dump(
        "m4-invocation.json",
        {
            "schema_version": 1,
            "request_id": "TEST-EVIDENCE-CONVENTIONS-2-M4",
            "task_id": "TEST-EVIDENCE-CONVENTIONS-2",
            "parent_workflow_id": "test-evidence-repository-conformance",
            "attempt_id": "M4-attempt-1",
            "profile": "AUTHORIZED_TEST_EVIDENCE_WRITE",
            "writer_authority": "validated task ownership assigns the listed tests, support, parser, validators, resources, and M4 evidence to ksdft2effmass-tests",
            "ownership": "m4-ownership.json",
            "historical_node_inventory": "m4-historical-node-inventory.json",
            "explicit_test_paths": sorted(old_groups),
            "immutable_inputs": {
                "baseline_revision": subprocess.check_output(
                    ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
                ).strip(),
                "content_sha256_before": before_hashes,
            },
            "permitted_mutations": [
                "listed explicit test paths and test-owned support helpers",
                "python/src/ksdft2effmass/harness/pi/evidence.py",
                "current test-evidence validators and focused regression evidence",
                "current resource profiles/manifests and classification fixtures",
                ".pi/evidence/test-evidence-repository-conformance/m4-*",
                ".pi/evidence/test-evidence-repository-conformance/maintained-test-inventory.json",
            ],
            "stop_policy": "Stop on ownership conflict, incomplete mapping, contract ambiguity, unauthorized mutation, or required-gate failure.",
        },
    )
    dump(
        "m4-node-migration-map.json",
        {
            "schema_version": 1,
            "expected_old_node_ids": old,
            "expected_new_node_ids": [item["new_node_id"] for item in mappings],
            "mappings": mappings,
        },
    )
    dump("m4-new-split-nodes.json", {"schema_version": 1, "node_ids": additions})
    dump(
        "m4-new-evidence-owners.json",
        {
            "schema_version": 1,
            "evidence_ids": [
                *(f"SV-HL-{value:03d}" for value in range(14, 38)),
                "SV-HARNESS-066",
            ],
        },
    )
    inventory_path = OUT / "maintained-test-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    owned_paths = set(old_groups)
    updated = 0
    for entry in inventory["modules"]:
        if entry["path"] not in owned_paths:
            continue
        entry["content_sha256"] = hashlib.sha256(
            (ROOT / entry["path"]).read_bytes()
        ).hexdigest()
        entry["conformance_status"] = "conforming"
        updated += 1
    if updated != 47:
        raise ValueError(f"expected 47 inventory updates, got {updated}")
    pre_m4_expected_nodes = 2568
    inventory["expected_collected_node_count"] = (
        pre_m4_expected_nodes + len(new) - len(old)
    )
    inventory_path.write_text(
        json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        f"mapped={len(mappings)} new_nodes={len(additions)} final={len(new)} "
        f"inventory_updates={updated}"
    )


if __name__ == "__main__":
    main()
