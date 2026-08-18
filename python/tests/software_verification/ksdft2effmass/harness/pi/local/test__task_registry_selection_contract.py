r"""Software verification of the Task registry and selection cross-surface contract.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The artifact owner is agreement among selection-state schema, fixtures, canonical
repository state, public imports, and the Task/selection dependency boundary.

Intrinsic and cross-object scope

Class-owned modules verify individual runtime objects. This module verifies schema,
fixture, repository-state, public-surface, and source dependency agreement.

VVUQ and scientific exclusions

Passing establishes structural software agreement only. It grants no activation,
authority, persistence, scientific validity, or human acceptance.
"""

import ast
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator  # type: ignore[import-untyped]

import ksdft2effmass.harness.pi.local as local_api
from ksdft2effmass.harness.pi.local import (
    DevelopmentTaskSelectionDeserializer,
    DevelopmentTaskSelectionSerializer,
)

from .conftest import repository_root

pytestmark = pytest.mark.software_verification


def fixture_has_declared_selection_result(
    fixture_root: Path,
    validator: Draft202012Validator,
    relative: str,
    expectation: dict[str, object],
) -> bool:
    """Evidence ID: Owns no identifier; supports SV-HT-112.

    Requirement: Fixture-family evidence needs one explicit per-file oracle.

    Method: Apply schema validation and, where applicable, strict deserialization.

    Oracle: The declared layer selects the expected isolated failure boundary.

    Acceptance: Return true exactly when the fixture behaves as declared.

    Interpretation: False identifies schema/runtime fixture disagreement.

    Limitations: This helper owns no independent evidence claim.
    """
    payload = (fixture_root / relative).read_bytes()
    errors = tuple(validator.iter_errors(json.loads(payload)))
    layer = expectation["layer"]
    expected = expectation.get("expected", [])
    if (
        type(layer) is not str
        or type(expected) is not list
        or any(type(item) is not str for item in expected)
    ):
        return False
    if layer == "schema":
        return {error.validator for error in errors} == set(expected)
    if errors:
        return False
    if layer == "valid":
        value = DevelopmentTaskSelectionDeserializer().execute(payload)
        return DevelopmentTaskSelectionSerializer().execute(value) == payload
    try:
        DevelopmentTaskSelectionDeserializer().execute(payload)
    except (TypeError, ValueError) as exc:
        return {type(exc).__name__} == set(expected)
    return False


def resolved_from_imports(node: ast.ImportFrom, module_name: str) -> set[str]:
    """Evidence ID: Owns no identifier; supports SV-HT-113.

    Requirement: Relative-import dependency evidence needs absolute module targets.

    Method: Resolve one AST ``from`` node against its explicit owner module.

    Oracle: Python relative-import levels remove package components before appending
    the represented module or imported name.

    Acceptance: Return every represented absolute target exactly once.

    Interpretation: An incorrect target could hide or invent a dependency finding.

    Limitations: This helper owns no independent evidence claim.
    """
    package_parts = module_name.split(".")[:-1]
    if not node.level:
        return set() if node.module is None else {node.module}
    retained = package_parts[: len(package_parts) - node.level + 1]
    if node.module is not None:
        return {".".join((*retained, node.module))}
    return {".".join((*retained, alias.name)) for alias in node.names}


def direct_imports(path: Path, module_name: str) -> set[str]:
    """Evidence ID: Owns no identifier; supports SV-HT-113.

    Requirement: Dependency evidence needs direct imports from an explicit source.

    Method: Parse one Python module and collect ``import`` and ``from`` targets.

    Oracle: Python AST import nodes define the direct syntactic dependency set.

    Acceptance: Return every direct import target exactly once as a set.

    Interpretation: An incorrect set could hide or invent a dependency finding.

    Limitations: This helper does not detect dynamic imports.
    """
    tree = ast.parse(path.read_text())
    plain = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    from_imports = {
        target
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        for target in resolved_from_imports(node, module_name)
    }
    return plain | from_imports


def test_artifact__selection_fixtures__agree_with_schema_runtime_and_live_state() -> (
    None
):
    """Evidence ID: SV-HT-112

    Requirement: Indexed selection fixtures and canonical repository selection state
    agree with the version-1 schema and strict runtime wire contract.

    Method: Compare explicit fixture discovery with the index, apply Draft 2020-12
    validation, execute runtime cases, and compare canonical inactive bytes.

    Oracle: The maintained schema, hand-authored fixture index, and approved inactive
    repository state independently define expected partitions.

    Acceptance: The fixture index is complete; schema/runtime layers behave as
    declared; live state equals the canonical valid fixture and round trips exactly.

    Interpretation: Failure identifies schema, fixture, runtime, or repository-state
    drift.

    Limitations: Structural agreement does not validate receipt existence or authority.
    """
    root = repository_root()
    fixture_root = root / "harness/local/fixtures/task-selection-v1"
    index = json.loads((fixture_root / "fixture-index.json").read_text())
    schema = json.loads(
        (root / "harness/local/schemas/task-selection-v1.schema.json").read_text()
    )
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    indexed = set(index["valid"]) | set(index["invalid"])
    discovered = {
        path.relative_to(fixture_root).as_posix()
        for path in fixture_root.rglob("*.json")
        if path.name != "fixture-index.json"
    }
    assert indexed == discovered

    assert all(
        fixture_has_declared_selection_result(
            fixture_root, validator, relative, {"layer": "valid"}
        )
        for relative in index["valid"]
    )
    assert all(
        fixture_has_declared_selection_result(
            fixture_root, validator, relative, expectation
        )
        for relative, expectation in index["invalid"].items()
    )

    trailing_line_terminator = {
        "schema_version": 1,
        "active_task_id": "task\n",
        "explicit_activation_receipt_ids": [],
        "automatic_successor_activation": False,
    }
    assert {
        error.validator for error in validator.iter_errors(trailing_line_terminator)
    } == {"oneOf"}
    with pytest.raises(ValueError):
        DevelopmentTaskSelectionDeserializer().execute(
            json.dumps(trailing_line_terminator).encode()
        )

    canonical = (fixture_root / "valid/inactive.json").read_bytes()
    live = (root / "harness/task-selection.json").read_bytes()
    assert live == canonical


def test_artifact__dependency__excludes_chain_and_cpn_coupling() -> None:
    """Evidence ID: SV-HT-113

    Requirement: Registry and selection interfaces are public project-local contracts
    whose owner modules import neither chain nor scientific CPN/Workflow code.

    Method: Assert exact required public exports and inspect direct import syntax of the
    two owner modules.

    Oracle: The approved Task-graph cutover defines project-local ownership and
    prohibits chain/CPN coupling.

    Acceptance: Every required name is exported and no direct import begins with a
    prohibited chain or workflow module path.

    Interpretation: Failure identifies missing public API or reversed dependency
    direction.

    Limitations: This static check does not prove absence of all dynamic imports.
    """
    required = {
        "HarnessTaskRegistry",
        "DevelopmentTaskSelection",
        "DevelopmentTaskSelectionSerializer",
        "DevelopmentTaskSelectionDeserializer",
    }
    assert required <= set(local_api.__all__)
    assert all(isinstance(getattr(local_api, name), type) for name in required)

    source_root = repository_root() / "python/src/ksdft2effmass/harness/pi/local"
    prohibited = {
        "ksdft2effmass.harness.pi.chains",
        "ksdft2effmass.workflows",
    }
    imported = direct_imports(
        source_root / "task_model.py",
        "ksdft2effmass.harness.pi.local.task_model",
    ) | direct_imports(
        source_root / "task_selection.py",
        "ksdft2effmass.harness.pi.local.task_selection",
    )
    assert not {
        name
        for name in imported
        if any(name == prefix or name.startswith(prefix + ".") for prefix in prohibited)
    }
