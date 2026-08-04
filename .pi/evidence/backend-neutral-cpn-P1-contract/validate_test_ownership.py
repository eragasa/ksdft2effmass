#!/usr/bin/env python3
"""Validate P1 class-owned and artifact-owned maintained pytest evidence."""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
EVIDENCE_ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = EVIDENCE_ROOT / "test-ownership-manifest.json"
TASK_OWNERSHIP_PATH = EVIDENCE_ROOT / "task-ownership.json"
BASELINE_PATH = (
    REPO_ROOT / ".pi/evidence/class-owned-evidence-convention/"
    "p1-pre-full-migration-baseline.json"
)
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
MODULE_HEADINGS = (
    "Evidence class and represented meaning",
    "Owned contract, oracle, and scope",
    "VVUQ and scientific exclusions",
)
TEST_FIELDS = (
    "Evidence ID",
    "Requirement",
    "Method",
    "Oracle",
    "Acceptance",
    "Interpretation",
    "Limitations",
)
SEMANTIC_TEST_NAME = re.compile(
    r"^test_(constructor|field|property|method|classmethod|staticmethod|protocol|public_api|artifact|workflow)"
    r"__[a-z0-9]+(?:_[a-z0-9]+)*__[a-z0-9]+(?:_[a-z0-9]+)*$"
)
APPROVED_ARTIFACT_PATHS = (
    INTEGRATION_ROOT + "test__workflow_cpn_python_public_api.py",
    INTEGRATION_ROOT + "test__workflow_cpn_v1_python_json_contract.py",
    INTEGRATION_ROOT + "test__workflow_cpn_v1_json_fixtures_python_runtime_contract.py",
    INTEGRATION_ROOT + "test__workflow_cpn_python_import_dependency_direction.py",
    INTEGRATION_ROOT
    + "test__workflow_cpn_python_snakes_and_deferred_engine_isolation.py",
)
SUPERSEDED_ARTIFACT_PATHS = (
    INTEGRATION_ROOT + "test__CpnPublicContract.py",
    INTEGRATION_ROOT + "test__CpnContractSchema.py",
    INTEGRATION_ROOT + "test__CpnJsonFixtures.py",
    INTEGRATION_ROOT + "test__CpnDependencyDirection.py",
    INTEGRATION_ROOT + "test__CpnSnakesIsolation.py",
)
APPROVED_INTEGRATION_OWNERS = (
    (
        "workflow_cpn_python_public_api",
        "artifact_owned_integration",
        "Workflow CPN Python public import/API surface",
    ),
    (
        "workflow_cpn_v1_python_json_contract",
        "boundary_owned",
        "version-1 CPN Python runtime <-> version-1 CPN JSON Schema and wire contract",
    ),
    (
        "workflow_cpn_v1_json_fixtures_python_runtime_contract",
        "artifact_owned_integration",
        "version-1 CPN JSON fixture family <-> Python runtime contract",
    ),
    (
        "workflow_cpn_python_import_dependency_direction",
        "artifact_owned_integration",
        "Workflow CPN Python import-dependency direction",
    ),
    (
        "workflow_cpn_python_snakes_and_deferred_engine_isolation",
        "artifact_owned_integration",
        "Workflow CPN Python isolation from SNAKES and deferred engine/persistence scope",
    ),
)
CONTROLLED_INTEGRATION_OWNERSHIP_TYPES = {
    "artifact_owned_integration",
    "boundary_owned",
}
PROHIBITED_GENERIC_ARTIFACT_STEMS = {
    "integration",
    "contract",
    "schema",
    "fixtures",
    "dependency_direction",
    "public_contract",
    "workflow",
    "subnet",
}


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


def _ordered_sections(docstring: str, labels: tuple[str, ...]) -> list[int]:
    """Return positions of exact, unique, ordered reStructuredText sections."""
    positions: list[int] = []
    for label in labels:
        matches = list(re.finditer(rf"(?m)^{re.escape(label)}$", docstring))
        assert len(matches) == 1, f"expected exactly one {label!r} section"
        positions.append(matches[0].start())
    assert positions == sorted(positions), f"sections out of order: {labels}"
    return positions


def _fielded_id(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """Validate the fielded grammar and return its sole evidence identifier."""
    doc = ast.get_docstring(node) or ""
    assert doc.strip(), f"empty docstring: {node.name}"
    positions = _ordered_sections(doc, TEST_FIELDS)
    boundaries = positions[1:] + [len(doc)]
    for label, start, end in zip(TEST_FIELDS, positions, boundaries, strict=True):
        body_start = doc.find("\n", start) + 1
        assert doc[body_start:end].strip(), f"empty {label}: {node.name}"
    identifiers = ID_PATTERN.findall(doc[positions[0] : positions[1]])
    assert len(identifiers) == 1, f"missing/ambiguous fielded ID: {node.name}"
    return identifiers[0]


def _historical_first_line_id(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """Return the sole summary-line ID retained by unmigrated historical modules."""
    doc = ast.get_docstring(node) or ""
    first_line = doc.splitlines()[0] if doc else ""
    identifiers = ID_PATTERN.findall(first_line)
    assert len(identifiers) == 1, f"missing/ambiguous first-line ID: {node.name}"
    return identifiers[0]


def _validate_module_headings(tree: ast.Module) -> None:
    """Enforce the authorized headings for every migrated CPN module."""
    module_doc = ast.get_docstring(tree) or ""
    _ordered_sections(module_doc, MODULE_HEADINGS)
    for heading in MODULE_HEADINGS:
        assert f"{heading}\n{'-' * len(heading)}" in module_doc, (
            f"invalid reStructuredText underline for {heading!r}"
        )


def _validate_fielded_structure(
    tree: ast.Module,
    tests: list[ast.FunctionDef | ast.AsyncFunctionDef],
    owner: str,
) -> None:
    """Enforce the authorized headings, primary owner, and semantic test names."""
    _validate_module_headings(tree)
    sut_assignments = [
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "SUT"
            for target in node.targets
        )
    ]
    assert len(sut_assignments) == 1, (
        "fielded module must declare exactly one primary SUT"
    )
    assert _assigned_name(tree, "SUT") == owner
    for node in tests:
        assert SEMANTIC_TEST_NAME.fullmatch(node.name), (
            f"invalid semantic fielded test name: {node.name}"
        )
        assert len(node.name.split("__")) == 3


def _validate_artifact_structure(
    tree: ast.Module,
    tests: list[ast.FunctionDef | ast.AsyncFunctionDef],
    integration_owner: str,
    ownership_type: str,
) -> None:
    """Enforce fielded integration grammar without fabricating a class SUT."""
    _validate_module_headings(tree)
    assert _assigned_name(tree, "SUT") is None
    module_doc = ast.get_docstring(tree) or ""
    normalized_doc = " ".join(module_doc.split())
    owner_phrase = (
        "primary boundary owner"
        if ownership_type == "boundary_owned"
        else "primary artifact owner"
    )
    assert owner_phrase in normalized_doc
    assert integration_owner in normalized_doc
    for node in tests:
        assert SEMANTIC_TEST_NAME.fullmatch(node.name)
        assert node.name.startswith("test_artifact__")
        assert len(node.name.split("__")) == 3


def _validate_module_evidence(
    path: Path,
    declared_entries: list[dict[str, str]],
    observed_ids: dict[str, tuple[str, str]],
    fielded_owner: str | None = None,
    integration_owner: str | None = None,
    ownership_type: str | None = None,
) -> ast.Module:
    """Validate shared marker, declaration, and stable-ID properties."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    assert _has_software_marker(tree), f"missing software marker: {path}"
    tests = _tests(tree)
    relative_path = path.relative_to(REPO_ROOT).as_posix()
    if fielded_owner is not None:
        _validate_fielded_structure(tree, tests, fielded_owner)
    elif integration_owner is not None and ownership_type is not None:
        _validate_artifact_structure(tree, tests, integration_owner, ownership_type)
    declared = {entry["test"]: entry for entry in declared_entries}
    assert {node.name for node in tests} == set(declared), (
        f"test manifest drift: {path}"
    )
    for node in tests:
        evidence_id = (
            _fielded_id(node)
            if fielded_owner is not None or integration_owner is not None
            else _historical_first_line_id(node)
        )
        assert evidence_id == declared[node.name]["evidence_id"], (
            f"ID mismatch: {path}:{node.name}"
        )
        assert evidence_id not in observed_ids, f"duplicate {evidence_id}"
        observed_ids[evidence_id] = (relative_path, node.name)
    return tree


def _validate_helpers(manifest: dict[str, object]) -> None:
    """Require fielded documentation and complete support lists for every helper."""
    declared_items = manifest["helpers"]
    assert isinstance(declared_items, list)
    declared = {
        (item["module"], item["helper"]): item["supported_evidence_ids"]
        for item in declared_items
    }
    observed: set[tuple[str, str]] = set()
    workflow_root = REPO_ROOT / WORKFLOW_ROOT
    for path in sorted(workflow_root.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        relative = path.relative_to(REPO_ROOT).as_posix()
        if path.name == "conftest.py":
            _validate_module_headings(tree)
            assert _assigned_name(tree, "SUT") is None, (
                "conftest helpers must not fabricate a primary SUT"
            )
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if node.name.startswith("test_"):
                continue
            key = (relative, node.name)
            assert key in declared, (
                f"undeclared evidence helper: {relative}:{node.name}"
            )
            doc = ast.get_docstring(node) or ""
            positions = _ordered_sections(doc, TEST_FIELDS)
            boundaries = positions[1:] + [len(doc)]
            for label, start, end in zip(
                TEST_FIELDS, positions, boundaries, strict=True
            ):
                body_start = doc.find("\n", start) + 1
                assert doc[body_start:end].strip(), f"empty {label}: {key}"
            evidence_section = doc[positions[0] : positions[1]]
            normalized_evidence_section = " ".join(evidence_section.split())
            assert "owns no independent evidence ID" in normalized_evidence_section
            assert ID_PATTERN.findall(evidence_section) == declared[key]
            observed.add(key)
    assert observed == set(declared), "helper manifest inventory differs"


def _normalized_helper_hash(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """Hash helper executable AST after recursively removing documentation."""
    normalized = copy.deepcopy(node)
    for child in ast.walk(normalized):
        if not isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if (
            child.body
            and isinstance(child.body[0], ast.Expr)
            and isinstance(child.body[0].value, ast.Constant)
            and isinstance(child.body[0].value.value, str)
        ):
            child.body = child.body[1:]
    return hashlib.sha256(
        ast.dump(normalized, include_attributes=False).encode()
    ).hexdigest()


def _validate_artifact_helpers(manifest: dict[str, object]) -> None:
    """Validate all artifact helper fields, support IDs, and baseline-neutral AST."""
    entries = manifest["artifact_helpers"]
    assert isinstance(entries, list) and len(entries) == 14
    trees: dict[str, ast.Module] = {}
    for entry in entries:
        module = entry["module"]
        tree = trees.setdefault(
            module,
            ast.parse(
                (REPO_ROOT / module).read_text(encoding="utf-8"), filename=module
            ),
        )
        matches = [
            node
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == entry["helper"]
        ]
        assert len(matches) == 1
        node = matches[0]
        doc = ast.get_docstring(node) or ""
        positions = _ordered_sections(doc, TEST_FIELDS)
        evidence_section = doc[positions[0] : positions[1]]
        assert ID_PATTERN.findall(evidence_section) == entry["supported_evidence_ids"]
        assert "owns no independent Evidence ID" in " ".join(evidence_section.split())
        assert (
            _normalized_helper_hash(node) == entry["baseline_normalized_ast_sha256"]
        ), f"helper executable AST drift: {module}:{node.name}"


def _normalized_test_hash(
    node: ast.FunctionDef | ast.AsyncFunctionDef, old_name: str
) -> str:
    """Hash executable test AST after removing documentation and restoring its old name."""

    normalized = copy.deepcopy(node)
    normalized.name = old_name
    if (
        normalized.body
        and isinstance(normalized.body[0], ast.Expr)
        and isinstance(normalized.body[0].value, ast.Constant)
        and isinstance(normalized.body[0].value.value, str)
    ):
        normalized.body = normalized.body[1:]
    prior_nested_helper_docs = {
        "field": "Construct one public field read over synthetic maximum controls.",
        "execute_two_cycles": (
            "Execute twice with explicit index 7 and return immutable state."
        ),
        "definition_validator": "Return a local validator for one named contract definition.",
        "runtime_token": "Construct one complete synthetic token with both controls equal.",
        "wire_token": "Return the exact wire counterpart of ``runtime_token``.",
    }
    for child in ast.walk(normalized):
        if not isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        prior_doc = prior_nested_helper_docs.get(child.name)
        if prior_doc is None:
            continue
        assert (
            child.body
            and isinstance(child.body[0], ast.Expr)
            and isinstance(child.body[0].value, ast.Constant)
            and isinstance(child.body[0].value.value, str)
        )
        child.body[0].value.value = prior_doc
    payload = ast.dump(normalized, include_attributes=False).encode()
    return hashlib.sha256(payload).hexdigest()


def _validate_documentation_migration(
    manifest: dict[str, object], observed_ids: dict[str, tuple[str, str]]
) -> None:
    """Check complete node mappings and documentation-neutral executable AST."""
    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    baseline_tests = {
        test["evidence_id"]: (entry["module"], test)
        for entry in baseline["modules"]
        if entry["module"].startswith(WORKFLOW_ROOT)
        for test in entry["tests"]
    }
    mappings = manifest["documentation_node_mappings"]
    assert isinstance(mappings, list) and len(mappings) == 78
    assert {item["evidence_id"] for item in mappings} == set(baseline_tests)
    by_id = {item["evidence_id"]: item for item in mappings}
    for evidence_id, (module, test) in baseline_tests.items():
        current_module, current_name = observed_ids[evidence_id]
        mapping = by_id[evidence_id]
        assert mapping["old_node_id"] == f"{module}::{test['old_name']}"
        assert mapping["new_node_id"] == f"{current_module}::{current_name}"
        path = REPO_ROOT / current_module
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        node = next(item for item in _tests(tree) if item.name == current_name)
        assert (
            _normalized_test_hash(node, test["old_name"])
            == test["normalized_ast_sha256"]
        ), f"executable AST drift: {evidence_id}"


def _validate_artifact_documentation_migration(
    manifest: dict[str, object], observed_ids: dict[str, tuple[str, str]]
) -> None:
    """Require exact artifact rename mappings and documentation-neutral test AST."""
    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    baseline_tests = {
        test["evidence_id"]: (entry["module"], test)
        for entry in baseline["modules"]
        if entry["module"] in SUPERSEDED_ARTIFACT_PATHS
        for test in entry["tests"]
    }
    mappings = manifest["artifact_documentation_node_mappings"]
    assert isinstance(mappings, list) and len(mappings) == 10
    assert {item["evidence_id"] for item in mappings} == set(baseline_tests)
    by_id = {item["evidence_id"]: item for item in mappings}
    for evidence_id, (old_module, test) in baseline_tests.items():
        current_module, current_name = observed_ids[evidence_id]
        mapping = by_id[evidence_id]
        assert mapping["old_node_id"] == f"{old_module}::{test['old_name']}"
        assert mapping["new_node_id"] == f"{current_module}::{current_name}"
        tree = ast.parse((REPO_ROOT / current_module).read_text(encoding="utf-8"))
        node = next(item for item in _tests(tree) if item.name == current_name)
        assert (
            _normalized_test_hash(node, test["old_name"])
            == test["normalized_ast_sha256"]
        ), f"artifact executable AST drift: {evidence_id}"


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

    actual_artifact_paths = tuple(
        item["module"] for item in manifest["artifact_modules"]
    )
    assert actual_artifact_paths == APPROVED_ARTIFACT_PATHS
    assert all((REPO_ROOT / path).is_file() for path in actual_artifact_paths)
    assert not any((REPO_ROOT / path).exists() for path in SUPERSEDED_ARTIFACT_PATHS)
    assert not any(
        Path(path).stem.removeprefix("test__") in PROHIBITED_GENERIC_ARTIFACT_STEMS
        for path in actual_artifact_paths
    )

    sys.path.insert(0, str(REPO_ROOT / "python" / "src"))
    from ksdft2effmass.workflows import cpn

    exports = manifest["public_exports"]
    assert [item["name"] for item in exports] == cpn.__all__
    assert len(exports) == 49

    observed_ids: dict[str, tuple[str, str]] = {}
    for entry in manifest["modules"]:
        path = REPO_ROOT / entry["module"]
        owner = entry["public_class"]
        assert path.name == f"test__{owner}.py"
        assert owner in cpn.__all__
        tree = _validate_module_evidence(
            path, entry["evidence"], observed_ids, fielded_owner=owner
        )
        module_doc = ast.get_docstring(tree) or ""
        assert owner in module_doc and "sole primary SUT" in module_doc
        assert _assigned_name(tree, "SUT") == owner
        for node in _tests(tree):
            assert any(
                (isinstance(item, ast.Name) and item.id in {"SUT", owner})
                or (isinstance(item, ast.Attribute) and item.attr == owner)
                for item in ast.walk(node)
            ), f"owner not exercised: {path}:{node.name}"

    for entry, (filename_owner, ownership_type, integration_owner) in zip(
        manifest["artifact_modules"], APPROVED_INTEGRATION_OWNERS, strict=True
    ):
        path = REPO_ROOT / entry["module"]
        assert entry["ownership_type"] in CONTROLLED_INTEGRATION_OWNERSHIP_TYPES
        assert entry["ownership_type"] == ownership_type
        if ownership_type == "boundary_owned":
            assert "artifact_owner" not in entry
            assert entry["boundary_owner"] == integration_owner
        else:
            assert "boundary_owner" not in entry
            assert entry["artifact_owner"] == filename_owner
        assert entry["boundary_agreement"] == integration_owner
        assert path.name == f"test__{filename_owner}.py"
        tree = _validate_module_evidence(
            path,
            entry["evidence"],
            observed_ids,
            integration_owner=integration_owner,
            ownership_type=ownership_type,
        )
        assert _assigned_name(tree, "SUT") is None

    expected_ids = {f"SV-CPN-{index:03d}" for index in range(1, 89)}
    assert set(observed_ids) == expected_ids, "P1 evidence range must be 001-088"
    _validate_helpers(manifest)
    _validate_artifact_helpers(manifest)
    _validate_documentation_migration(manifest, observed_ids)
    _validate_artifact_documentation_migration(manifest, observed_ids)
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
    assert (
        tuple(manifest["evidence_script"]["authoritative_modules"])
        == APPROVED_ARTIFACT_PATHS
    )
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
