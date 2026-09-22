#!/usr/bin/env python3
"""Validate complete P1 CPN evidence-documentation structural conformance."""

from __future__ import annotations

import ast
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
P1_ROOT = ROOT / ".pi/evidence/backend-neutral-cpn-P1-contract"
MANIFEST = P1_ROOT / "test-ownership-manifest.json"
EVIDENCE_ROOT = ROOT / ".pi/evidence/class-owned-evidence-convention"
MIGRATION = EVIDENCE_ROOT / "migration-inventory.json"
COMPLETE_NODE_MAP = EVIDENCE_ROOT / "cpn-complete-directory-node-id-map.json"
REFERENCE = ROOT / ".pi/skills/document-research-python/references/test-evidence-documentation.md"
CPN_TEST_ROOT = ROOT / "python/tests/software_verification/ksdft2effmass/workflows/cpn"
APPROVED_ARTIFACT_MODULES = (
    "python/tests/software_verification/ksdft2effmass/integration/test__workflow_cpn_python_public_api.py",
    "python/tests/software_verification/ksdft2effmass/integration/test__workflow_cpn_v1_python_json_contract.py",
    "python/tests/software_verification/ksdft2effmass/integration/test__workflow_cpn_v1_json_fixtures_python_runtime_contract.py",
    "python/tests/software_verification/ksdft2effmass/integration/test__workflow_cpn_python_import_dependency_direction.py",
    "python/tests/software_verification/ksdft2effmass/integration/test__workflow_cpn_python_snakes_and_deferred_engine_isolation.py",
)
OLD_ARTIFACT_MODULES = (
    "python/tests/software_verification/ksdft2effmass/integration/test__CpnPublicContract.py",
    "python/tests/software_verification/ksdft2effmass/integration/test__CpnContractSchema.py",
    "python/tests/software_verification/ksdft2effmass/integration/test__CpnJsonFixtures.py",
    "python/tests/software_verification/ksdft2effmass/integration/test__CpnDependencyDirection.py",
    "python/tests/software_verification/ksdft2effmass/integration/test__CpnSnakesIsolation.py",
)
GEOMETRY_NUMERICAL = ROOT / "python/tests/numerical_verification/ksdft2effmass/operators/test__Geometry__linear_independence.py"
NV_G_COMPARISON = EVIDENCE_ROOT / "nv-g-001-009-comparison.json"
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
NAME = re.compile(
    r"^test_(constructor|field|property|method|classmethod|staticmethod|protocol|public_api|artifact|workflow)"
    r"__[a-z0-9]+(?:_[a-z0-9]+)*__[a-z0-9]+(?:_[a-z0-9]+)*$"
)
ID = re.compile(r"\b(?:SV|NV)-[A-Z][A-Z0-9]*-\d{3}\b")
SECTION = re.compile(r"(?m)^([^\n]+)\n(-{3,})$")


def _load(path: Path) -> dict[str, Any]:
    """Load one JSON object used as authoritative structural input."""
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"expected JSON object: {path}"
    return value


def _exact_sections(docstring: str, labels: tuple[str, ...]) -> list[int]:
    """Require exactly the declared reStructuredText sections in order."""
    observed = [match.group(1) for match in SECTION.finditer(docstring)]
    assert observed == list(labels), f"sections differ: expected={labels!r} observed={observed!r}"
    positions: list[int] = []
    for label in labels:
        match = re.search(rf"(?m)^{re.escape(label)}\n{'-' * len(label)}$", docstring)
        assert match is not None, f"invalid underline for {label!r}"
        positions.append(match.start())
    return positions


def _field_bodies(docstring: str) -> dict[str, str]:
    """Return nonempty bodies for exactly seven ordered evidence fields."""
    positions: list[int] = []
    for label in TEST_FIELDS:
        matches = list(re.finditer(rf"(?m)^{re.escape(label)}$", docstring))
        assert len(matches) == 1, f"expected one {label!r} field"
        positions.append(matches[0].start())
    assert positions == sorted(positions), "evidence fields are out of order"
    boundaries = positions[1:] + [len(docstring)]
    bodies: dict[str, str] = {}
    for label, start, end in zip(TEST_FIELDS, positions, boundaries, strict=True):
        body_start = docstring.find("\n", start) + 1
        body = docstring[body_start:end].strip()
        if body.startswith("-" * len(label)):
            body = body.split("\n", 1)[1].strip() if "\n" in body else ""
        assert body, f"empty {label!r} field"
        bodies[label] = body
    return bodies


def _functions(tree: ast.AST) -> list[ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return all functions, including the declared nested fixture helper."""
    return [node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]


def _validate_class_module(entry: dict[str, Any]) -> tuple[int, dict[str, str]]:
    """Validate one manifest-declared class module and its evidence owners."""
    path = ROOT / entry["module"]
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    public_class = entry["public_class"]
    assert path.name == f"test__{public_class}.py", f"class filename differs from sole SUT: {path}"
    module_doc = ast.get_docstring(tree) or ""
    _exact_sections(module_doc, MODULE_HEADINGS)
    normalized_doc = " ".join(module_doc.split())
    assert f"``{public_class}``" in normalized_doc and "sole primary SUT" in normalized_doc, f"missing exact SUT ownership: {path}"
    assert "pytest.mark.software_verification" in ast.unparse(tree), f"missing software marker: {path}"
    sut = [
        node for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "SUT" for target in node.targets)
    ]
    assert len(sut) == 1 and isinstance(sut[0].value, ast.Name) and sut[0].value.id == public_class, f"wrong sole SUT assignment: {path}"

    tests = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_")]
    observed: dict[str, str] = {}
    for node in tests:
        assert NAME.fullmatch(node.name), f"invalid semantic test name: {path}:{node.name}"
        bodies = _field_bodies(ast.get_docstring(node) or "")
        identifiers = ID.findall(bodies["Evidence ID"])
        assert len(identifiers) == 1 and identifiers[0].startswith("SV-"), f"one software evidence ID required: {path}:{node.name}"
        assert identifiers[0] not in observed, f"duplicate local evidence ID: {identifiers[0]}"
        assert not ID.search(node.name), f"evidence ID embedded in test name: {node.name}"
        observed[identifiers[0]] = node.name
    declared = {item["evidence_id"]: item["test"] for item in entry["evidence"]}
    assert observed == declared, f"manifest differs from executable owners: {path}"
    return len(tests), observed


def _validate_artifact_modules(manifest: dict[str, Any]) -> tuple[int, int]:
    """Validate approved artifact/boundary modules and rename traceability."""
    entries = manifest["artifact_modules"]
    declared_paths = tuple(entry["module"] for entry in entries)
    assert declared_paths == APPROVED_ARTIFACT_MODULES, "artifact manifest paths differ from approved filenames"
    assert not any((ROOT / path).exists() for path in OLD_ARTIFACT_MODULES), "superseded artifact module remains on disk"

    observed: dict[str, tuple[str, str]] = {}
    for entry in entries:
        path = ROOT / entry["module"]
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        module_doc = ast.get_docstring(tree) or ""
        _exact_sections(module_doc, MODULE_HEADINGS)
        normalized_doc = " ".join(module_doc.split())
        ownership_type = entry["ownership_type"]
        assert ownership_type in {"artifact_owned_integration", "boundary_owned"}
        if ownership_type == "boundary_owned":
            assert "artifact_owner" not in entry
            assert entry["boundary_owner"] == entry["boundary_agreement"]
            owner_statement = f"{entry['boundary_owner']} is the primary boundary owner."
            assert owner_statement in normalized_doc, f"boundary owner/docs disagreement: {path}"
        else:
            assert "boundary_owner" not in entry
            assert entry["artifact_owner"] == path.stem.removeprefix("test__")
            assert "primary artifact owner" in normalized_doc, f"artifact ownership boundary missing: {path}"
        assert "pytest.mark.software_verification" in ast.unparse(tree), f"missing software marker: {path}"
        assignments = [
            node for node in tree.body
            if isinstance(node, (ast.Assign, ast.AnnAssign))
            and any(
                isinstance(target, ast.Name) and target.id == "SUT"
                for target in (node.targets if isinstance(node, ast.Assign) else [node.target])
            )
        ]
        assert not assignments, f"artifact module must not fabricate a class SUT: {path}"

        tests = [
            node for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_")
        ]
        local: dict[str, str] = {}
        for node in tests:
            assert NAME.fullmatch(node.name), f"invalid semantic artifact test name: {path}:{node.name}"
            assert node.name.startswith("test_artifact__"), f"artifact surface required: {path}:{node.name}"
            bodies = _field_bodies(ast.get_docstring(node) or "")
            identifiers = ID.findall(bodies["Evidence ID"])
            assert len(identifiers) == 1 and identifiers[0].startswith("SV-CPN-"), f"one P1 software ID required: {path}:{node.name}"
            assert identifiers[0] not in local, f"duplicate local artifact evidence ID: {identifiers[0]}"
            local[identifiers[0]] = node.name
            observed[identifiers[0]] = (entry["module"], node.name)
        declared = {item["evidence_id"]: item["test"] for item in entry["evidence"]}
        assert local == declared, f"artifact manifest differs from executable owners: {path}"

    mappings = manifest["artifact_documentation_node_mappings"]
    assert len(mappings) == len(observed) == 10, "all ten artifact evidence owners require node mappings"
    mapped: dict[str, tuple[str, str]] = {}
    for item in mappings:
        assert item["old_node_id"] != item["new_node_id"]
        assert any(item["old_node_id"].startswith(f"{path}::") for path in OLD_ARTIFACT_MODULES)
        assert item["evidence_id"] not in mapped
        new_module, new_test = item["new_node_id"].rsplit("::", 1)
        mapped[item["evidence_id"]] = (new_module, new_test)
    assert mapped == observed, "artifact node map differs from current manifest/executable owners"
    return len(entries), len(observed)


def _validate_helpers(manifest: dict[str, Any]) -> int:
    """Validate every declared helper against its complete manifest ID list."""
    helper_entries = manifest["helpers"]
    assert len(helper_entries) == 11, "P1 manifest must declare exactly 11 evidence helpers"
    trees: dict[str, ast.Module] = {}
    for entry in helper_entries:
        module = entry["module"]
        tree = trees.setdefault(module, ast.parse((ROOT / module).read_text(encoding="utf-8"), filename=module))
        matches = [node for node in _functions(tree) if node.name == entry["helper"]]
        assert len(matches) == 1, f"declared helper not unique: {module}:{entry['helper']}"
        bodies = _field_bodies(ast.get_docstring(matches[0]) or "")
        evidence_body = bodies["Evidence ID"]
        observed_ids = ID.findall(evidence_body)
        assert len(observed_ids) == len(set(observed_ids)), f"duplicate supported ID in helper: {module}:{entry['helper']}"
        assert observed_ids == entry["supported_evidence_ids"], f"incomplete or reordered helper ID list: {module}:{entry['helper']}"
        lowered = " ".join(evidence_body.lower().split())
        assert "supports exactly" in lowered and "owns no independent evidence id" in lowered, f"helper ownership statement missing: {module}:{entry['helper']}"

    conftest = trees["python/tests/software_verification/ksdft2effmass/workflows/cpn/conftest.py"]
    _exact_sections(ast.get_docstring(conftest) or "", MODULE_HEADINGS)
    assignments = [
        node for node in conftest.body
        if isinstance(node, (ast.Assign, ast.AnnAssign))
        and any(isinstance(target, ast.Name) and target.id == "SUT" for target in (node.targets if isinstance(node, ast.Assign) else [node.target]))
    ]
    assert not assignments, "conftest.py must not fabricate a SUT assignment"
    assert "without fabricating a class SUT" in (ast.get_docstring(conftest) or ""), "conftest helper ownership boundary missing"
    return len(helper_entries)


def _validate_complete_node_map(observed: dict[str, tuple[str, str]]) -> int:
    """Require one standalone old-to-new mapping for every migrated test function."""
    node_map = _load(COMPLETE_NODE_MAP)
    mappings = node_map["mappings"]
    assert node_map["module_count"] == 32 and node_map["test_function_count"] == 78
    assert len(mappings) == 78
    mapped: dict[str, tuple[str, str]] = {}
    for item in mappings:
        assert item["old_node_id"] != item["new_node_id"]
        assert item["evidence_id"] not in mapped
        mapped[item["evidence_id"]] = (item["module"], item["new_node_id"].rsplit("::", 1)[1])
    assert mapped == observed, "complete node map differs from current manifest/executable owners"
    return len(mappings)


def main() -> int:
    """Run complete-directory structural checks; semantic adequacy remains review-owned."""
    manifest = _load(MANIFEST)
    modules = manifest["modules"]
    assert len(modules) == 32, "P1 manifest must declare exactly 32 class modules"
    declared_paths = {entry["module"] for entry in modules}
    disk_paths = {str(path.relative_to(ROOT)) for path in CPN_TEST_ROOT.glob("test__*.py")}
    assert disk_paths == declared_paths, "complete CPN test directory differs from P1 manifest"

    test_count = 0
    observed: dict[str, tuple[str, str]] = {}
    for entry in modules:
        count, module_evidence = _validate_class_module(entry)
        test_count += count
        for evidence_id, test_name in module_evidence.items():
            assert evidence_id not in observed, f"duplicate directory evidence ID: {evidence_id}"
            observed[evidence_id] = (entry["module"], test_name)
    assert test_count == 78 and len(observed) == 78
    helper_count = _validate_helpers(manifest)
    mapping_count = _validate_complete_node_map(observed)
    artifact_module_count, artifact_test_count = _validate_artifact_modules(manifest)

    migration = _load(MIGRATION)
    assert migration["schema_version"] == 1
    assert migration["snapshot_counts"]["total_modules"] == 96
    assert migration["snapshot_counts"]["cpn_directory_modules_migrated"] == 32
    assert len(migration["cpn_directory_modules_migrated"]) == 32
    assert tuple(sorted(migration["artifact_owned_integration_modules_migrated"])) == tuple(sorted(APPROVED_ARTIFACT_MODULES))
    assert not migration["software_verification_modules_needing_migration"]
    assert not migration["artifact_owned_integration_modules_needing_migration"]
    inventoried = (
        len(migration["cpn_directory_modules_migrated"])
        + len(migration["numerical_verification_modules_needing_migration"])
        + len(migration["artifact_owned_integration_modules_migrated"])
        + len(migration["protected_historical_modules_left_unchanged"])
    )
    assert inventoried == 96
    assert migration["scientific_validation_marker_policy"] == "no_new_marker_or_id_family"

    reference = REFERENCE.read_text(encoding="utf-8")
    for label in MODULE_HEADINGS + TEST_FIELDS:
        assert label in reference
    assert "test_<surface>__<facet>__<behavior>" in reference
    for filename in (Path(path).name for path in APPROVED_ARTIFACT_MODULES):
        assert filename in reference
    assert "Reserve ``_to_``" in reference
    assert "Structural tooling" in reference and "cannot" in reference

    comparison = _load(NV_G_COMPARISON)
    assert comparison["module_sha256"] == hashlib.sha256(GEOMETRY_NUMERICAL.read_bytes()).hexdigest()
    assert comparison["disposition"] == "protected_historical_left_unchanged"
    assert [item["id"] for item in comparison["evidence"]] == [f"NV-G-{number:03d}" for number in range(1, 10)]

    print(
        "evidence documentation validation passed: "
        f"cpn_modules={len(modules)} tests={test_count} evidence_ids={len(observed)} "
        f"helpers={helper_count} node_mappings={mapping_count} "
        f"artifact_modules={artifact_module_count} artifact_tests={artifact_test_count} inventoried_modules={inventoried}; "
        "structural checks do not establish semantic adequacy or final acceptance"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
