#!/usr/bin/env python3
"""Validate the bounded P2 actions and owned test-evidence correction."""

from __future__ import annotations

import ast
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / ".pi/evidence/backend-neutral-cpn-P2-tools-provenance"
ACTIVATION = EVIDENCE / "actions-correction-activation.json"
SOURCE = ROOT / "python/src/ksdft2effmass/provenance/actions.py"
PUBLIC_INIT = ROOT / "python/src/ksdft2effmass/provenance/__init__.py"
OWNERSHIP = EVIDENCE / "actions-test-evidence-ownership.json"
MIGRATION = EVIDENCE / "actions-test-evidence-node-migration.json"
INVENTORY = EVIDENCE / "actions-test-evidence-inventory.json"
IMPLEMENTATION = EVIDENCE / "actions-test-evidence-implementation.md"
CHECKPOINT = ROOT / ".pi/checkpoints/P2-HC03-final-acceptance.json"
RENEWED_CHECKPOINT = ROOT / ".pi/checkpoints/P2-HC04-final-acceptance.json"
CHAIN = ROOT / ".pi/chains/backend-neutral-kohn-sham-qe.chain.json"
EXPECTED_CLASSES = (
    "ArtifactIdentityVerificationStatus",
    "CorrelationStatus",
    "CorrelationIssue",
    "ArtifactIdentityVerificationResult",
    "ArtifactIdentityVerifier",
    "ExecutionCorrelationResult",
    "ExecutionOutcomeCorrelator",
)
EXPECTED_TEST_PATHS = {
    f"python/tests/software_verification/ksdft2effmass/provenance/test__{name}.py"
    for name in EXPECTED_CLASSES
}


def load_object(path: Path, issues: list[str]) -> dict[str, object]:
    """Return one required JSON object or append a structural issue."""
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        issues.append(f"missing or invalid JSON: {path.relative_to(ROOT)}")
        return {}
    if not isinstance(value, dict):
        issues.append(f"JSON root must be an object: {path.relative_to(ROOT)}")
        return {}
    return value


def aggregate_tracked(paths: list[Path]) -> str:
    """Return a path-qualified aggregate SHA-256 for tracked files."""
    digest = hashlib.sha256()
    for path in paths:
        digest.update(str(path.relative_to(ROOT)).encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def public_shape(source: str) -> dict[str, object]:
    """Return the public class, field, enum, property, and method signature shape."""
    tree = ast.parse(source)
    result: dict[str, object] = {}
    for node in tree.body:
        if not isinstance(node, ast.ClassDef) or node.name.startswith("_"):
            continue
        fields: list[tuple[str, str]] = []
        enum_values: list[tuple[str, object]] = []
        methods: list[tuple[str, str, str, tuple[str, ...]]] = []
        for member in node.body:
            if isinstance(member, ast.AnnAssign) and isinstance(
                member.target, ast.Name
            ):
                fields.append((member.target.id, ast.unparse(member.annotation)))
            elif isinstance(member, ast.Assign):
                for target in member.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        try:
                            enum_values.append(
                                (target.id, ast.literal_eval(member.value))
                            )
                        except ValueError:
                            enum_values.append((target.id, ast.unparse(member.value)))
            elif isinstance(
                member, (ast.FunctionDef, ast.AsyncFunctionDef)
            ) and not member.name.startswith("_"):
                decorators = tuple(ast.unparse(item) for item in member.decorator_list)
                methods.append(
                    (
                        member.name,
                        ast.dump(member.args, include_attributes=False),
                        ast.unparse(member.returns) if member.returns else "",
                        decorators,
                    )
                )
        result[node.name] = {
            "bases": tuple(ast.unparse(base) for base in node.bases),
            "fields": tuple(fields),
            "enum_values": tuple(enum_values),
            "methods": tuple(methods),
        }
    return result


def main() -> int:
    issues: list[str] = []
    activation = load_object(ACTIVATION, issues)
    ownership = load_object(OWNERSHIP, issues)
    migration = load_object(MIGRATION, issues)
    inventory = load_object(INVENTORY, issues)
    checkpoint = load_object(CHECKPOINT, issues)
    renewed_checkpoint = (
        load_object(RENEWED_CHECKPOINT, issues) if RENEWED_CHECKPOINT.exists() else {}
    )
    chain = load_object(CHAIN, issues)

    starting_revision = activation.get("starting_revision")
    if not isinstance(starting_revision, str):
        issues.append("activation lacks starting_revision")
    else:
        try:
            baseline_source = subprocess.check_output(
                [
                    "git",
                    "show",
                    f"{starting_revision}:python/src/ksdft2effmass/provenance/actions.py",
                ],
                cwd=ROOT,
                text=True,
            )
        except (OSError, subprocess.CalledProcessError):
            issues.append("cannot read baseline actions.py")
        else:
            if public_shape(baseline_source) != public_shape(
                SOURCE.read_text(encoding="utf-8")
            ):
                issues.append(
                    "public actions class/field/enum/method signature shape changed"
                )

    source_tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    class_names = tuple(
        node.name
        for node in source_tree.body
        if isinstance(node, ast.ClassDef) and not node.name.startswith("_")
    )
    if class_names != EXPECTED_CLASSES:
        issues.append("public actions class inventory changed")
    private_definitions = [
        node.name
        for node in source_tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and node.name.startswith("_")
    ]
    if private_definitions:
        issues.append(f"private module definitions remain: {private_definitions}")
    source_text = SOURCE.read_text(encoding="utf-8")
    for retired in ("_require_identifier", "_require_sha256"):
        if retired in source_text:
            issues.append(f"retired helper remains: {retired}")

    baseline_hashes = activation.get("baseline_hashes", {})
    if not isinstance(baseline_hashes, dict):
        issues.append("activation baseline_hashes must be an object")
        baseline_hashes = {}
    if hashlib.sha256(PUBLIC_INIT.read_bytes()).hexdigest() != baseline_hashes.get(
        "public_init_py"
    ):
        issues.append("public export module bytes changed")
    schema_paths = [
        ROOT / value
        for value in subprocess.check_output(
            ["git", "ls-files", "--", "specification/provenance/v1"],
            cwd=ROOT,
            text=True,
        ).splitlines()
    ]
    if aggregate_tracked(schema_paths) != baseline_hashes.get(
        "schema_and_fixtures_aggregate_sha256"
    ):
        issues.append("schema or fixture bytes changed")
    for relative, key in (
        ("python/pyproject.toml", "python_pyproject_toml"),
        ("python/uv.lock", "python_uv_lock"),
    ):
        if hashlib.sha256(
            (ROOT / relative).read_bytes()
        ).hexdigest() != baseline_hashes.get(key):
            issues.append(f"dependency or lock bytes changed: {relative}")

    modules = ownership.get("modules", [])
    if not isinstance(modules, list):
        issues.append("actions ownership modules must be a list")
        modules = []
    module_paths = {entry.get("path") for entry in modules if isinstance(entry, dict)}
    if module_paths != EXPECTED_TEST_PATHS:
        issues.append("actions ownership must cover exactly seven class modules")
    if any(
        not isinstance(entry, dict)
        or entry.get("mode") != "class_owned"
        or entry.get("evidence_class") != "software_verification"
        for entry in modules
    ):
        issues.append("actions ownership classification is inconsistent")

    old_nodes = migration.get("expected_old_node_ids", [])
    mapped_nodes = migration.get("expected_new_node_ids", [])
    mappings = migration.get("mappings", [])
    if not all(
        isinstance(value, list) for value in (old_nodes, mapped_nodes, mappings)
    ):
        issues.append("actions migration inventories must be lists")
        old_nodes, mapped_nodes, mappings = [], [], []
    mapping_old = [
        entry.get("old_node_id") for entry in mappings if isinstance(entry, dict)
    ]
    mapping_new = [
        entry.get("new_node_id") for entry in mappings if isinstance(entry, dict)
    ]
    if (
        len(mapping_old) != len(mappings)
        or len(old_nodes) != len(set(old_nodes))
        or len(mapped_nodes) != len(set(mapped_nodes))
        or len(mapping_old) != len(set(mapping_old))
        or len(mapping_new) != len(set(mapping_new))
        or set(mapping_old) != set(old_nodes)
        or set(mapping_new) != set(mapped_nodes)
    ):
        issues.append("actions migration is not complete and one-to-one")

    current_inventory = inventory.get("current_collection_inventory", {})
    if not isinstance(current_inventory, dict):
        issues.append("current_collection_inventory must be an object")
        current_nodes: list[object] = []
    else:
        current_nodes = [
            node
            for values in current_inventory.values()
            if isinstance(values, list)
            for node in values
        ]
    if set(current_inventory) != EXPECTED_TEST_PATHS:
        issues.append("current collection inventory paths are incomplete")
    if len(current_nodes) != len(set(current_nodes)) or not set(mapped_nodes) <= set(
        current_nodes
    ):
        issues.append("current collection node inventory is inconsistent")
    historical_ids = inventory.get("historical_evidence_ids", [])
    if not isinstance(historical_ids, list) or len(historical_ids) != len(
        set(historical_ids)
    ):
        issues.append("historical evidence identifier inventory is invalid")
    if not IMPLEMENTATION.is_file():
        issues.append("missing actions test-evidence implementation record")

    if activation.get("status") == "durable_complete_pending_P2-HC04_human_acceptance":
        if checkpoint.get("status") != "superseded":
            issues.append(
                "P2-HC03 must be superseded without resolution after durability"
            )
        if (
            renewed_checkpoint.get("status") != "pending"
            or renewed_checkpoint.get("checkpoint_id") != "P2-HC04"
        ):
            issues.append("P2-HC04 must be the renewed pending checkpoint")
    elif (
        checkpoint.get("status") != "pending"
        or checkpoint.get("checkpoint_id") != "P2-HC03"
    ):
        issues.append("P2-HC03 must remain pending before the correction is durable")
    task_states = {
        item.get("id"): item.get("status")
        for item in chain.get("task_sequence", [])
        if isinstance(item, dict)
    }
    if any(task_states.get(f"P{number}") != "blocked" for number in range(3, 12)):
        issues.append("a P3-P11 successor is not blocked")
    if chain.get("production_execution_authorized") is not False:
        issues.append("production execution became authorized")

    result = {
        "schema_version": 1,
        "task_id": "P2",
        "correction_id": "P2-ACTIONS-EVIDENCE-1",
        "status": "PASS" if not issues else "FAIL",
        "observed": {
            "public_classes": len(class_names),
            "private_module_definitions": len(private_definitions),
            "owned_test_modules": len(modules),
            "mapped_historical_nodes": len(mappings),
            "current_collected_nodes": len(current_nodes),
            "schema_and_fixture_files": len(schema_paths),
        },
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
