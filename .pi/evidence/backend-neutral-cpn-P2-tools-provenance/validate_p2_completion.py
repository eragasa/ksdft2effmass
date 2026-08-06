#!/usr/bin/env python3
"""Validate structural P2 completion conditions without frozen test totals."""

from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "python/src/ksdft2effmass/provenance"
TESTS = ROOT / "python/tests/software_verification/ksdft2effmass/provenance"
SCHEMA = ROOT / "specification/provenance/v1"
ARTIFACT_TEST = (
    ROOT / "python/tests/software_verification/ksdft2effmass/integration/provenance/"
    "test__json_fixtures_runtime_agreement_v1.py"
)
EVIDENCE_ROOT = ROOT / ".pi/evidence/backend-neutral-cpn-P2-tools-provenance"
OWNERSHIP_PATH = EVIDENCE_ROOT / "test-evidence-ownership.json"
MIGRATION_PATH = EVIDENCE_ROOT / "test-evidence-node-migration.json"
INVENTORY_PATH = EVIDENCE_ROOT / "test-evidence-inventory.json"
IMPLEMENTATION_PATH = EVIDENCE_ROOT / "test-evidence-implementation.md"
TOOLS_OWNERSHIP_PATH = (
    EVIDENCE_ROOT / "tools-decomposition-test-evidence-ownership.json"
)
TOOLS_MIGRATION_PATH = (
    EVIDENCE_ROOT / "tools-decomposition-test-evidence-node-migration.json"
)
TOOLS_INVENTORY_PATH = (
    EVIDENCE_ROOT / "tools-decomposition-test-evidence-inventory.json"
)
TOOLS_IMPLEMENTATION_PATH = (
    EVIDENCE_ROOT / "tools-decomposition-test-evidence-implementation.md"
)
TOOLS_CLASSES = (
    "CapabilityKind",
    "VerificationStatus",
    "ExternalExecutionStatus",
    "ExternalFailureStage",
    "ExternalFailureCode",
    "ExternalToolIdentity",
    "ExternalToolSpecification",
    "DeclaredCapability",
    "InstallationObservation",
    "VerificationObservation",
    "ExternalExecutionRequest",
    "ExternalExecutionResult",
    "ExternalExecutionFailure",
)
TOOLS_SOURCE_MODULES = (
    "external_tools.py",
    "tool_observations.py",
    "external_execution.py",
)
REQUIRED_DOCS = (
    "docs/api/provenance.md",
    "docs/concepts/provenance-and-artifacts.md",
    "docs/user-guide/provenance-and-artifacts.md",
    "docs/user-guide/external-tool-lifecycle.md",
    "docs/verification/provenance-contract.rst",
)
BANNED_TEXT = (
    "workflows.cpn",
    "import snakes",
    "from snakes",
    "import subprocess",
    "from subprocess",
    "scheduler",
    "service_locator",
    "backend_registry",
)


def main() -> int:
    issues: list[str] = []
    init_path = SOURCE / "__init__.py"
    if not init_path.is_file():
        issues.append("missing public provenance package")
        exports: tuple[str, ...] = ()
    else:
        try:
            tree = ast.parse(init_path.read_text(encoding="utf-8"))
            assignment = next(
                node
                for node in tree.body
                if isinstance(node, ast.Assign)
                and any(
                    isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets
                )
            )
            value = ast.literal_eval(assignment.value)
            exports = tuple(value) if isinstance(value, (tuple, list)) else ()
        except (OSError, UnicodeError, SyntaxError, StopIteration, ValueError):
            exports = ()
            issues.append("public __all__ is not a literal tuple or list")
        if (
            not exports
            or len(exports) != len(set(exports))
            or tuple(sorted(exports)) != exports
        ):
            issues.append("public __all__ must be nonempty, unique, and sorted")

    for path in SOURCE.glob("*.py"):
        text = path.read_text(encoding="utf-8").lower()
        for banned in BANNED_TEXT:
            if banned in text:
                issues.append(
                    f"forbidden dependency text {banned!r} in {path.relative_to(ROOT)}"
                )

    if exports and TESTS.is_dir():
        module_names = {path.name for path in TESTS.glob("test__*.py")}
        for name in exports:
            if name.endswith(("Status", "Kind", "Stage", "Algorithm", "ErrorCode")):
                continue
            expected = f"test__{name}.py"
            if expected not in module_names:
                issues.append(f"missing class-owned module {expected}")
        for path in TESTS.glob("test__*.py"):
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, SyntaxError):
                issues.append(f"unparseable test module {path.relative_to(ROOT)}")
                continue
            for node in ast.walk(tree):
                if (
                    isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and node.name.startswith("test_")
                    and "__" not in node.name
                ):
                    issues.append(f"nonsemantic test name {path.name}:{node.name}")
    elif not TESTS.is_dir():
        issues.append("missing class-owned provenance test directory")

    schemas = tuple(SCHEMA.glob("*.schema.json")) if SCHEMA.is_dir() else ()
    fixtures = tuple(SCHEMA.glob("fixtures/**/*.json")) if SCHEMA.is_dir() else ()
    if not schemas:
        issues.append("missing provenance schemas")
    if not fixtures:
        issues.append("missing provenance fixtures")
    for relative in REQUIRED_DOCS:
        if not (ROOT / relative).is_file():
            issues.append(f"missing maintained document {relative}")

    evidence_inputs: dict[str, object] = {}
    for label, path in (
        ("ownership", OWNERSHIP_PATH),
        ("migration", MIGRATION_PATH),
        ("inventory", INVENTORY_PATH),
    ):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            issues.append(f"missing or invalid P2 test-evidence {label} record")
            continue
        if not isinstance(value, dict):
            issues.append(f"P2 test-evidence {label} record must be an object")
            continue
        evidence_inputs[label] = value
    if not IMPLEMENTATION_PATH.is_file():
        issues.append("missing P2 test-evidence implementation record")

    tools_evidence_inputs: dict[str, object] = {}
    for label, path in (
        ("ownership", TOOLS_OWNERSHIP_PATH),
        ("migration", TOOLS_MIGRATION_PATH),
        ("inventory", TOOLS_INVENTORY_PATH),
    ):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            issues.append(f"missing or invalid tools-decomposition {label} record")
            continue
        if not isinstance(value, dict):
            issues.append(f"tools-decomposition {label} record must be an object")
            continue
        tools_evidence_inputs[label] = value
    if not TOOLS_IMPLEMENTATION_PATH.is_file():
        issues.append("missing tools-decomposition implementation record")

    expected_tools_paths = {
        str((TESTS / f"test__{name}.py").relative_to(ROOT)) for name in TOOLS_CLASSES
    }
    tools_ownership = tools_evidence_inputs.get("ownership", {})
    tools_modules = (
        tools_ownership.get("modules", []) if isinstance(tools_ownership, dict) else []
    )
    if (
        not isinstance(tools_modules, list)
        or {entry.get("path") for entry in tools_modules if isinstance(entry, dict)}
        != expected_tools_paths
        or len(tools_modules) != 13
        or any(
            entry.get("mode") != "class_owned"
            or entry.get("evidence_class") != "software_verification"
            or entry.get("sut") not in TOOLS_CLASSES
            for entry in tools_modules
            if isinstance(entry, dict)
        )
    ):
        issues.append(
            "tools-decomposition ownership must cover exactly 13 class-owned software-verification modules"
        )
    for source_name in TOOLS_SOURCE_MODULES:
        if not (SOURCE / source_name).is_file():
            issues.append(f"missing tools-decomposition source module {source_name}")
    if (SOURCE / "tools.py").exists():
        issues.append("retired provenance/tools.py must be absent")

    tools_migration = tools_evidence_inputs.get("migration", {})
    tools_old = (
        tools_migration.get("expected_old_node_ids", [])
        if isinstance(tools_migration, dict)
        else []
    )
    tools_new = (
        tools_migration.get("expected_new_node_ids", [])
        if isinstance(tools_migration, dict)
        else []
    )
    tools_mappings = (
        tools_migration.get("mappings", []) if isinstance(tools_migration, dict) else []
    )
    mapped_tools_old = (
        [
            entry.get("old_node_id")
            for entry in tools_mappings
            if isinstance(entry, dict)
        ]
        if isinstance(tools_mappings, list)
        else []
    )
    mapped_tools_new = (
        [
            entry.get("new_node_id")
            for entry in tools_mappings
            if isinstance(entry, dict)
        ]
        if isinstance(tools_mappings, list)
        else []
    )
    if (
        not all(
            isinstance(values, list)
            for values in (tools_old, tools_new, tools_mappings)
        )
        or len(tools_old) != 24
        or len(tools_old) != len(set(tools_old))
        or len(tools_new) != len(set(tools_new))
        or len(mapped_tools_old) != len(tools_mappings)
        or len(mapped_tools_old) != len(set(mapped_tools_old))
        or len(mapped_tools_new) != len(set(mapped_tools_new))
        or set(mapped_tools_old) != set(tools_old)
        or set(mapped_tools_new) != set(tools_new)
    ):
        issues.append(
            "tools-decomposition migration must map exactly 24 historical nodes one-to-one"
        )
    tools_inventory = tools_evidence_inputs.get("inventory", {})
    tools_complete = (
        tools_inventory.get("complete_new_node_ids", [])
        if isinstance(tools_inventory, dict)
        else []
    )
    tools_additional = (
        tools_inventory.get("new_node_ids_without_historical_predecessor", [])
        if isinstance(tools_inventory, dict)
        else []
    )
    tools_paths = (
        tools_inventory.get("paths", []) if isinstance(tools_inventory, dict) else []
    )
    if (
        not all(
            isinstance(values, list)
            for values in (tools_complete, tools_additional, tools_paths)
        )
        or set(tools_paths) != expected_tools_paths
        or len(tools_complete) != len(set(tools_complete))
        or set(tools_complete) != set(tools_new) | set(tools_additional)
        or set(tools_new) & set(tools_additional)
    ):
        issues.append("tools-decomposition complete-node inventory is inconsistent")

    expected_test_paths = {
        str(path.relative_to(ROOT))
        for path in TESTS.glob("test__*.py")
        if path.stem.removeprefix("test__")
        in {
            "ArtifactIdentity",
            "ArtifactSpecification",
            "ArtifactReference",
            "ArtifactLocation",
            "RunManifest",
            "ProvenanceRecord",
            "LineageRelation",
        }
    }
    expected_test_paths.add(str(ARTIFACT_TEST.relative_to(ROOT)))
    ownership = evidence_inputs.get("ownership", {})
    modules = ownership.get("modules", []) if isinstance(ownership, dict) else []
    if (
        not isinstance(modules, list)
        or {entry.get("path") for entry in modules if isinstance(entry, dict)}
        != expected_test_paths
    ):
        issues.append(
            "P2 test-evidence ownership must cover exactly the eight authorized modules"
        )
    elif (
        sum(entry.get("mode") == "class_owned" for entry in modules) != 7
        or sum(entry.get("mode") == "artifact_owned" for entry in modules) != 1
        or any(
            entry.get("evidence_class") != "software_verification" for entry in modules
        )
    ):
        issues.append("P2 test-evidence ownership classes are inconsistent")

    migration = evidence_inputs.get("migration", {})
    old_nodes = (
        migration.get("expected_old_node_ids", [])
        if isinstance(migration, dict)
        else []
    )
    new_nodes = (
        migration.get("expected_new_node_ids", [])
        if isinstance(migration, dict)
        else []
    )
    mappings = migration.get("mappings", []) if isinstance(migration, dict) else []
    if not all(isinstance(values, list) for values in (old_nodes, new_nodes, mappings)):
        issues.append("P2 node migration inventories must be lists")
    else:
        mapped_old = [
            entry.get("old_node_id") for entry in mappings if isinstance(entry, dict)
        ]
        mapped_new = [
            entry.get("new_node_id") for entry in mappings if isinstance(entry, dict)
        ]
        if (
            len(mapped_old) != len(mappings)
            or len(old_nodes) != len(set(old_nodes))
            or len(new_nodes) != len(set(new_nodes))
            or len(mapped_old) != len(set(mapped_old))
            or len(mapped_new) != len(set(mapped_new))
            or set(mapped_old) != set(old_nodes)
            or set(mapped_new) != set(new_nodes)
        ):
            issues.append("P2 node migration must be complete and one-to-one")

    inventory = evidence_inputs.get("inventory", {})
    complete_nodes = (
        inventory.get("complete_new_node_ids", [])
        if isinstance(inventory, dict)
        else []
    )
    additional_nodes = (
        inventory.get("new_node_ids_without_historical_predecessor", [])
        if isinstance(inventory, dict)
        else []
    )
    inventory_paths = inventory.get("paths", []) if isinstance(inventory, dict) else []
    if not all(
        isinstance(values, list)
        for values in (complete_nodes, additional_nodes, inventory_paths)
    ):
        issues.append("P2 test-evidence completeness inventories must be lists")
    elif (
        set(inventory_paths) != expected_test_paths
        or len(complete_nodes) != len(set(complete_nodes))
        or set(complete_nodes) != set(new_nodes) | set(additional_nodes)
        or set(new_nodes) & set(additional_nodes)
    ):
        issues.append("P2 test-evidence complete-node inventory is inconsistent")

    result = {
        "schema_version": 1,
        "task_id": "P2",
        "status": "PASS" if not issues else "FAIL",
        "observed": {
            "public_exports": len(exports),
            "class_owned_modules": len(tuple(TESTS.glob("test__*.py")))
            if TESTS.is_dir()
            else 0,
            "schemas": len(schemas),
            "fixtures": len(fixtures),
            "test_evidence_modules": len(modules) if isinstance(modules, list) else 0,
            "mapped_historical_nodes": len(mappings)
            if isinstance(mappings, list)
            else 0,
            "complete_migrated_nodes": len(complete_nodes)
            if isinstance(complete_nodes, list)
            else 0,
            "tools_decomposition_modules": len(tools_modules)
            if isinstance(tools_modules, list)
            else 0,
            "tools_decomposition_historical_nodes": len(tools_mappings)
            if isinstance(tools_mappings, list)
            else 0,
            "tools_decomposition_complete_nodes": len(tools_complete)
            if isinstance(tools_complete, list)
            else 0,
        },
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
