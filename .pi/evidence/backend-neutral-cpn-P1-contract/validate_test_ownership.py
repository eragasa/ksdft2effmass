#!/usr/bin/env python3
"""Validate P1 class-owned and artifact-owned maintained pytest evidence."""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
EVIDENCE_ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = EVIDENCE_ROOT / "test-ownership-manifest.json"
TASK_OWNERSHIP_PATH = EVIDENCE_ROOT / "task-ownership.json"
ID_PATTERN = re.compile(r"SV-CPN-\d{3}")
WORKFLOW_ROOT = "python/tests/software_verification/ksdft2effmass/workflows/cpn/"
INTEGRATION_ROOT = "python/tests/software_verification/ksdft2effmass/integration/"
FORMER_MODULE_BY_ID = {
    **{index: WORKFLOW_ROOT + "test__CpnToken__contract.py" for index in range(1, 6)},
    **{
        index: WORKFLOW_ROOT + "test__DeclarativeExpressions.py"
        for index in range(6, 11)
    },
    **{
        index: WORKFLOW_ROOT + "test__CpnDefinitionAndMarking.py"
        for index in range(11, 15)
    },
    **{
        index: WORKFLOW_ROOT + "test__TransitionExecution.py"
        for index in (*range(15, 20), 34)
    },
    **{
        index: WORKFLOW_ROOT + "test__RetryRecoveryIteration.py"
        for index in range(20, 23)
    },
    **{
        index: WORKFLOW_ROOT + "test__CpnStructuredErrorsAndImports.py"
        for index in range(23, 27)
    },
    **{index: INTEGRATION_ROOT + "test__CpnJsonSchemas.py" for index in range(27, 29)},
    **{index: INTEGRATION_ROOT + "test__CpnJsonFixtures.py" for index in range(29, 32)},
    32: INTEGRATION_ROOT + "test__CpnDependencyDirection.py",
    33: INTEGRATION_ROOT + "test__CpnSnakesIsolation.py",
}
SPLIT_PREDECESSOR = {35: 10, 36: 12, 37: 18, 38: 19, 39: 19}
RESTORED_IDS = {23, *range(27, 34)}


def _assigned_name(tree: ast.Module, target: str) -> str | None:
    """Return the simple name assigned to a module constant."""
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(
            isinstance(item, ast.Name) and item.id == target for item in node.targets
        ):
            return node.value.id if isinstance(node.value, ast.Name) else None
    return None


def _has_software_marker(tree: ast.Module) -> bool:
    """Recognize the exact executable module-level software marker."""
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(
            isinstance(item, ast.Name) and item.id == "pytestmark"
            for item in node.targets
        ):
            continue
        return ast.unparse(node.value) == "pytest.mark.software_verification"
    return False


def _tests(tree: ast.Module) -> list[ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return maintained pytest functions declared at module scope."""
    return [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name.startswith("test_")
    ]


def _first_line_id(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """Return the sole evidence identifier on a test's summary line."""
    doc = ast.get_docstring(node) or ""
    first_line = doc.splitlines()[0] if doc else ""
    identifiers = ID_PATTERN.findall(first_line)
    assert len(identifiers) == 1, f"missing/ambiguous first-line ID: {node.name}"
    return identifiers[0]


def _validate_module_evidence(
    path: Path,
    declared_entries: list[dict[str, str]],
    observed_ids: dict[str, tuple[str, str]],
) -> ast.Module:
    """Validate shared marker, declaration, and stable-ID properties."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    assert _has_software_marker(tree), f"missing software marker: {path}"
    tests = _tests(tree)
    declared = {entry["test"]: entry for entry in declared_entries}
    assert {node.name for node in tests} == set(declared), (
        f"test manifest drift: {path}"
    )
    for node in tests:
        evidence_id = _first_line_id(node)
        assert evidence_id == declared[node.name]["evidence_id"], (
            f"ID mismatch: {path}:{node.name}"
        )
        assert evidence_id not in observed_ids, f"duplicate {evidence_id}"
        observed_ids[evidence_id] = (path.relative_to(REPO_ROOT).as_posix(), node.name)
    return tree


def _validate_migration_traceability(
    manifest: dict[str, object], current_targets: dict[str, tuple[str, str]]
) -> None:
    """Require exact predecessor coverage for the original 001-039 surface."""
    migration = manifest["migration_traceability"]
    assert isinstance(migration, dict)
    former_modules = migration["former_modules"]
    assert isinstance(former_modules, list) and len(former_modules) == 10
    old_items: set[int] = set()
    current_partitions: dict[int, int] = {}
    for module_entry in former_modules:
        assert isinstance(module_entry, dict)
        old_module = module_entry["old_module_path"]
        assert isinstance(old_module, str)
        items = module_entry["evidence_items"]
        assert isinstance(items, list)
        for item in items:
            assert isinstance(item, dict)
            old_id_text = item["old_evidence_id"]
            assert isinstance(old_id_text, str) and ID_PATTERN.fullmatch(old_id_text)
            old_id = int(old_id_text[-3:])
            assert old_id not in old_items and FORMER_MODULE_BY_ID[old_id] == old_module
            old_items.add(old_id)
            partitions = item["partitions"]
            assert isinstance(partitions, list) and partitions
            retained = 0
            for partition in partitions:
                assert isinstance(partition, dict)
                current_id_text = partition["current_evidence_id"]
                assert isinstance(current_id_text, str) and ID_PATTERN.fullmatch(
                    current_id_text
                )
                current_id = int(current_id_text[-3:])
                assert current_id not in current_partitions
                if current_id == old_id:
                    assert partition["disposition"] == "stable_id_retained"
                    retained += 1
                else:
                    assert partition["disposition"] == "assertion_split_to_new_id"
                    assert SPLIT_PREDECESSOR[current_id] == old_id
                target = partition["current_target"]
                name = partition["current_test_or_gate"]
                assert (target, name) == current_targets[current_id_text]
                current_partitions[current_id] = old_id
            assert retained == 1
    assert old_items == set(range(1, 35))
    assert set(current_partitions) == set(range(1, 40))


def validate_ownership() -> tuple[int, int, int]:
    """Enforce object, artifact, inventory, classification, and traceability rules."""
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    task_ownership = json.loads(TASK_OWNERSHIP_PATH.read_text(encoding="utf-8"))
    assert manifest["manifest_version"] == 3

    class_root = REPO_ROOT / manifest["canonical_test_directory"]
    actual_class_paths = sorted(class_root.glob("test__*.py"))
    expected_class_paths = sorted(
        REPO_ROOT / item["module"] for item in manifest["modules"]
    )
    assert actual_class_paths == expected_class_paths, "class module inventory differs"

    integration_root = REPO_ROOT / manifest["canonical_integration_directory"]
    declared_artifact_names = task_ownership["test_ownership"]["artifact_modules"]
    actual_artifact_paths = sorted(
        integration_root / name for name in declared_artifact_names
    )
    expected_artifact_paths = sorted(
        REPO_ROOT / item["module"] for item in manifest["artifact_modules"]
    )
    assert actual_artifact_paths == expected_artifact_paths
    assert all(path.is_file() for path in actual_artifact_paths)

    sys.path.insert(0, str(REPO_ROOT / "python" / "src"))
    import ksdft2effmass.workflows.cpn as cpn

    exports = manifest["public_exports"]
    assert [item["name"] for item in exports] == cpn.__all__
    assert len(exports) == 49

    observed_ids: dict[str, tuple[str, str]] = {}
    for entry in manifest["modules"]:
        path = REPO_ROOT / entry["module"]
        owner = entry["public_class"]
        assert path.name == f"test__{owner}.py"
        assert owner in cpn.__all__
        tree = _validate_module_evidence(path, entry["evidence"], observed_ids)
        module_doc = ast.get_docstring(tree) or ""
        assert owner in module_doc and "sole primary SUT" in module_doc
        assert _assigned_name(tree, "SUT") == owner
        for node in _tests(tree):
            assert any(
                (isinstance(item, ast.Name) and item.id in {"SUT", owner})
                or (isinstance(item, ast.Attribute) and item.attr == owner)
                for item in ast.walk(node)
            ), f"owner not exercised: {path}:{node.name}"

    for entry in manifest["artifact_modules"]:
        path = REPO_ROOT / entry["module"]
        tree = _validate_module_evidence(path, entry["evidence"], observed_ids)
        assert "Artifact-owned" in (ast.get_docstring(tree) or "")
        assert _assigned_name(tree, "SUT") is None

    expected_ids = {f"SV-CPN-{index:03d}" for index in range(1, 89)}
    assert set(observed_ids) == expected_ids, "P1 evidence range must be 001-088"
    current_targets = dict(observed_ids)
    _validate_migration_traceability(manifest, current_targets)

    restored = manifest["gate_restoration_traceability"]
    assert {int(item["evidence_id"][-3:]) for item in restored} == RESTORED_IDS
    for item in restored:
        evidence_id = item["evidence_id"]
        assert item["disposition"] == "stable_id_restored_to_maintained_pytest"
        assert (item["restored_module"], item["restored_test"]) == current_targets[
            evidence_id
        ]
        assert item["temporary_gate"].startswith("gate_sv_cpn_")

    extension = manifest["completeness_extension"]
    assert [item["evidence_id"] for item in extension] == [
        f"SV-CPN-{index:03d}" for index in range(40, 89)
    ]
    for item in extension:
        expected_classification = (
            "DETERMINISTIC_NOW"
            if int(item["evidence_id"][-3:]) < 80
            else "RESOLVED_BY_P1_HC01_A_AND_P1_HC02_B"
        )
        assert item["classification"] == expected_classification
        assert (item["module"], item["test"]) == current_targets[item["evidence_id"]]

    dedicated = {entry["public_class"] for entry in manifest["modules"]}
    exceptions = task_ownership["test_ownership"]["exceptions"]
    expected_exceptions = set(exceptions["enums"]) | set(
        exceptions["marker_exceptions"]
    )
    assert set(cpn.__all__) == dedicated | expected_exceptions
    assert not (dedicated & expected_exceptions)
    for export in exports:
        assert export["dedicated_module"] is (export["name"] in dedicated)
        if export["name"] in dedicated:
            owner_entry = next(
                item
                for item in manifest["modules"]
                if item["public_class"] == export["name"]
            )
            assert export["module"] == owner_entry["module"]
            assert export["evidence_ids"] == [
                item["evidence_id"] for item in owner_entry["evidence"]
            ]
        else:
            assert export["module"] is None and export["evidence_ids"] == []

    blocked = manifest["blocked_by_p1_hc01"]
    assert blocked == []
    return len(actual_class_paths), len(actual_artifact_paths), len(observed_ids)


def main() -> int:
    """Run the structural ownership and traceability audit."""
    class_count, artifact_count, evidence_count = validate_ownership()
    print(
        f"P1 ownership audit passed: class_modules={class_count} "
        f"artifact_modules={artifact_count} public_exports=49 "
        f"evidence_ids={evidence_count} restored_pytest_gates=8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
