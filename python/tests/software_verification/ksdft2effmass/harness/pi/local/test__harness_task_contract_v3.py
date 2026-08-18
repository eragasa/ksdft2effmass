r"""Software verification of HarnessTask version-3 cross-surface contract.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module verifies the focused public import, schema/fixture, mixed-format adapter,
and selected-state inspection boundaries of the minimum durable Task model.

Intrinsic and cross-object scope

The artifact owner is the HarnessTask version-3 cross-surface contract. Class-owned
modules separately verify the four retained Task-model interfaces.

VVUQ and scientific exclusions

Passing establishes software-contract agreement only. It does not migrate a Task,
activate work, validate science, or provide human acceptance.
"""

import json
import sqlite3
from collections import Counter
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator  # type: ignore[import-untyped]

import ksdft2effmass.harness as harness_api
import ksdft2effmass.harness.pi.local as local_api
from ksdft2effmass.harness import (
    HarnessTask,
    HarnessTaskDeserializer,
    HarnessTaskSerializer,
)
from ksdft2effmass.harness.pi.local import HarnessTaskGraphValidator

from .conftest import repository_root
from .task_model_examples import make_task

pytestmark = pytest.mark.software_verification

_RETAINED_PUBLIC_NAMES = (
    "ArchivedTaskSource",
    "HarnessTask",
    "HarnessTaskSerializer",
    "HarnessTaskDeserializer",
    "HarnessTaskGraphValidator",
    "HarnessTaskRegistry",
    "DevelopmentTaskSelection",
    "DevelopmentTaskSelectionSerializer",
    "DevelopmentTaskSelectionDeserializer",
)


def test_public_api__task_model__exports_retained_foundation_interfaces() -> None:
    """Evidence ID: SV-HT-020

    Requirement: The Task-model package publicly defines the retained Task graph,
    derived registry, and minimal selection-state foundation interfaces.

    Method: Compare package exports and module-owned public classes with fixed lists.

    Oracle: The approved Task-graph cutover foundation names the exact interfaces.

    Acceptance: Every retained name resolves and is exported; the Task and selection
    owner modules define only their exact assigned public classes.

    Interpretation: Failure identifies a missing core interface or an unaccepted
    compatibility facade.

    Limitations: Unrelated project-local package exports are outside this assertion.
    """
    assert all(name in local_api.__all__ for name in _RETAINED_PUBLIC_NAMES)
    v2_names = set(_RETAINED_PUBLIC_NAMES) - {"HarnessTaskGraphValidator"}
    assert v2_names <= set(harness_api.__all__)
    assert all(
        isinstance(getattr(local_api, name), type) for name in _RETAINED_PUBLIC_NAMES
    )
    assert all(
        getattr(local_api, name) is getattr(harness_api, name) for name in v2_names
    )

    task_model = __import__("ksdft2effmass.harness.task", fromlist=["unused"])
    defined = {
        name
        for name, value in vars(task_model).items()
        if isinstance(value, type)
        and value.__module__ == task_model.__name__
        and not name.startswith("_")
    }
    assert defined == {
        "ArchivedTaskSource",
        "HarnessTask",
        "HarnessTaskSerializer",
        "HarnessTaskDeserializer",
        "HarnessTaskRegistry",
    }
    local_task_model = __import__(
        "ksdft2effmass.harness.pi.local.task_model", fromlist=["unused"]
    )
    local_defined = {
        name
        for name, value in vars(local_task_model).items()
        if isinstance(value, type)
        and value.__module__ == local_task_model.__name__
        and not name.startswith("_")
    }
    assert local_defined == {"HarnessTaskGraphValidator"}

    task_selection = __import__(
        "ksdft2effmass.harness.task_selection", fromlist=["unused"]
    )
    selection_defined = {
        name
        for name, value in vars(task_selection).items()
        if isinstance(value, type)
        and value.__module__ == task_selection.__name__
        and not name.startswith("_")
    }
    assert selection_defined == {
        "DevelopmentTaskSelection",
        "DevelopmentTaskSelectionSerializer",
        "DevelopmentTaskSelectionDeserializer",
    }


def fixture_matches_expectation(
    root: Path,
    validator: Draft202012Validator,
    relative: str,
    layer: str,
) -> bool:
    """Evidence ID: Owns no identifier; supports SV-HT-022.

    Requirement: Fixture-family evidence needs one explicit per-file oracle.

    Method: Apply schema validation and, for runtime cases, strict deserialization.

    Oracle: The declared layer selects the expected isolated failure boundary.

    Acceptance: Return true exactly when the fixture behaves as declared.

    Interpretation: False identifies schema/runtime fixture disagreement.

    Limitations: This helper owns no independent evidence claim.
    """
    payload = (root / relative).read_bytes()
    schema_errors = list(validator.iter_errors(json.loads(payload)))
    if layer == "valid":
        return not schema_errors and (
            HarnessTaskSerializer().execute(HarnessTaskDeserializer().execute(payload))
            == payload
        )
    if layer == "schema":
        return bool(schema_errors)
    if schema_errors:
        return False
    try:
        HarnessTaskDeserializer().execute(payload)
    except TypeError, ValueError:
        return True
    return False


def test_artifact__fixture_family__agrees_with_schema_and_runtime() -> None:
    """Evidence ID: SV-HT-022

    Requirement: Indexed valid fixtures agree with schema and runtime behavior, while
    each invalid fixture fails at its declared boundary.

    Method: Compare discovered fixtures with the explicit index, Draft 2020-12 schema
    validation, and strict deserialization.

    Oracle: The maintained schema and hand-authored fixture index define the expected
    partitions independently of production dispatch.

    Acceptance: The index is complete and every fixture has its declared result.

    Interpretation: Failure identifies schema, fixture, or runtime disagreement.

    Limitations: JSON Schema cannot express every runtime Unicode invariant.
    """
    root = repository_root() / "harness/local/fixtures/task-record-v3"
    index = json.loads((root / "fixture-index.json").read_text())
    schema = json.loads(
        (
            repository_root() / "harness/local/schemas/task-record-v3.schema.json"
        ).read_text()
    )
    validator = Draft202012Validator(schema)
    indexed = set(index["valid"]) | set(index["invalid"])
    discovered = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*.json")
        if path.name != "fixture-index.json"
    }
    assert indexed == discovered
    assert all(
        fixture_matches_expectation(root, validator, relative, "valid")
        for relative in index["valid"]
    )
    assert all(
        fixture_matches_expectation(root, validator, relative, expectation["layer"])
        for relative, expectation in index["invalid"].items()
    )


def test_method__graph_findings__use_deterministic_precedence() -> None:
    """Evidence ID: SV-HT-024

    Requirement: Graph findings use exact codes and deterministic lexical precedence.

    Method: Supply a parent cycle, missing prerequisite, and duplicate paths.

    Oracle: The documented graph contract fixes ``(code, path, detail)`` ordering.

    Acceptance: Findings equal the exact expected sequence.

    Interpretation: Failure identifies graph-code or ordering drift.

    Limitations: Lifecycle meaning and chain activation are excluded.
    """
    first = make_task(
        task_id="a",
        parent_task_id="b",
        superseded_by_task_ids=("b",),
        intake_path="same",
        documentation_path="same",
    )
    second = make_task(
        task_id="b",
        parent_task_id="a",
        task_prerequisite_ids=("missing",),
        superseded_by_task_ids=("a", "absent"),
        intake_path="same",
        documentation_path="same",
    )
    issues = HarnessTaskGraphValidator().execute((first, second)).issues
    assert tuple((item.code, item.path, item.detail) for item in issues) == (
        ("PIHL.TASK.DOCUMENTATION_PATH_DUPLICATE", "same", "a,b"),
        ("PIHL.TASK.INTAKE_PATH_DUPLICATE", "same", "a,b"),
        ("PIHL.TASK.PARENT_CYCLE", None, "a,b"),
        ("PIHL.TASK.PREREQUISITE_MISSING", "same", "missing"),
        ("PIHL.TASK.SUPERSESSION_CYCLE", None, "a,b"),
        ("PIHL.TASK.SUPERSESSION_MISSING", "same", "absent"),
    )


def test_artifact__repository_catalog__agrees_with_schema_runtime_and_graph() -> None:
    """Evidence ID: SV-HT-040

    Requirement: Every regular source Task uses schema version 3, satisfies its
    runtime contract, and agrees structurally with every maintained projection.

    Method: Discover the explicit ``harness/tasks`` source catalog, apply the version-3
    schema and deserializer, then compare source identities with the graph, immutable
    SQLite state, and projection manifest under the same explicit repository root.

    Oracle: Regular ``harness/tasks/*.json`` files determine Task identity and
    cardinality; the accepted schema determines wire shape independently of generated
    projections.

    Acceptance: Every source file is discovered exactly once, parses as one canonical
    HarnessTask, and has a unique nonempty identity; source identities equal the graph,
    SQLite, and manifest identities with no missing, unexpected, or duplicate
    projection, independent of source discovery order.

    Interpretation: Failure identifies exact source, schema, runtime, root-resolution,
    or generated-projection drift.

    Limitations: This establishes structural software agreement only; it does not
    activate work, authorize execution, or establish scientific validity.
    """
    root = repository_root()
    relative_artifacts = (
        Path("harness/tasks"),
        Path("harness/local/schemas/task-record-v3.schema.json"),
        Path("harness/task-graph.json"),
        Path("harness/state/harness-control.sqlite3"),
        Path("harness/state/projection-manifest.json"),
    )
    artifacts = tuple(root / relative for relative in relative_artifacts)
    resolved_root = root.resolve(strict=True)
    resolved_artifacts = tuple(path.resolve(strict=True) for path in artifacts)
    assert not any(path.is_symlink() for path in artifacts), {
        "repository_root": resolved_root.as_posix(),
        "symlinked_artifacts": sorted(
            path.relative_to(root).as_posix() for path in artifacts if path.is_symlink()
        ),
    }
    assert all(path.is_relative_to(resolved_root) for path in resolved_artifacts), {
        "repository_root": resolved_root.as_posix(),
        "artifacts_outside_root": sorted(
            path.as_posix()
            for path in resolved_artifacts
            if not path.is_relative_to(resolved_root)
        ),
    }
    task_directory, schema_path, graph_path, database_path, manifest_path = artifacts

    regular_source_paths = frozenset(
        path
        for path in task_directory.iterdir()
        if path.is_file() and path.suffix == ".json"
    )
    discovered_paths = tuple(
        path for path in task_directory.glob("*.json") if path.is_file()
    )
    source_path_counts = Counter(discovered_paths)
    duplicate_source_paths = sorted(
        path.relative_to(root).as_posix()
        for path, count in source_path_counts.items()
        if count != 1
    )
    symlinked_source_paths = sorted(
        path.relative_to(root).as_posix()
        for path in discovered_paths
        if path.is_symlink()
    )
    escaped_source_paths = sorted(
        path.relative_to(root).as_posix()
        for path in discovered_paths
        if not path.resolve(strict=True).is_relative_to(resolved_root)
    )
    assert not duplicate_source_paths, {
        "duplicate_source_paths": duplicate_source_paths
    }
    assert not symlinked_source_paths, {
        "symlinked_source_paths": symlinked_source_paths
    }
    assert not escaped_source_paths, {"escaped_source_paths": escaped_source_paths}
    discovered_source_paths = frozenset(discovered_paths)
    assert discovered_source_paths == regular_source_paths, {
        "missing_source_paths": sorted(
            path.relative_to(root).as_posix()
            for path in regular_source_paths - discovered_source_paths
        ),
        "unexpected_source_paths": sorted(
            path.relative_to(root).as_posix()
            for path in discovered_source_paths - regular_source_paths
        ),
    }

    schema = json.loads(schema_path.read_text())
    validator = Draft202012Validator(schema)
    payloads = tuple(path.read_bytes() for path in discovered_paths)
    documents = tuple(json.loads(payload) for payload in payloads)
    assert {document["schema_version"] for document in documents} == {3}
    assert all(not tuple(validator.iter_errors(document)) for document in documents)
    tasks = tuple(HarnessTaskDeserializer().execute(payload) for payload in payloads)
    assert all(type(task) is HarnessTask for task in tasks)
    assert tuple(HarnessTaskSerializer().execute(task) for task in tasks) == payloads

    task_id_counts = Counter(task.task_id for task in tasks)
    duplicate_task_ids = sorted(
        task_id for task_id, count in task_id_counts.items() if count != 1
    )
    empty_task_source_paths = sorted(
        path.relative_to(root).as_posix()
        for path, task in zip(discovered_paths, tasks, strict=True)
        if not task.task_id
    )
    assert not duplicate_task_ids, {"duplicate_task_ids": duplicate_task_ids}
    assert not empty_task_source_paths, {
        "empty_task_id_source_paths": empty_task_source_paths
    }
    expected_task_ids = frozenset(task.task_id for task in tasks)
    reordered_task_ids = frozenset(task.task_id for task in reversed(tasks))
    assert reordered_task_ids == expected_task_ids

    graph = json.loads(graph_path.read_text())
    graph_id_counts = Counter(node["task_id"] for node in graph["nodes"])
    duplicate_graph_task_ids = sorted(
        task_id for task_id, count in graph_id_counts.items() if count != 1
    )
    graph_task_ids = frozenset(graph_id_counts)
    assert not duplicate_graph_task_ids, {
        "duplicate_graph_task_ids": duplicate_graph_task_ids
    }
    assert graph_task_ids == expected_task_ids, {
        "missing_task_ids": sorted(expected_task_ids - graph_task_ids),
        "unexpected_task_ids": sorted(graph_task_ids - expected_task_ids),
        "projection": graph_path.relative_to(root).as_posix(),
    }

    with sqlite3.connect(
        database_path.resolve().as_uri() + "?mode=ro&immutable=1", uri=True
    ) as connection:
        sqlite_rows = tuple(
            connection.execute(
                "SELECT task_id,source_path FROM task_definition ORDER BY task_id"
            )
        )
    sqlite_task_ids = frozenset(row[0] for row in sqlite_rows)
    sqlite_source_paths = frozenset(row[1] for row in sqlite_rows)
    expected_task_sources = frozenset(
        (task.task_id, path.relative_to(root).as_posix())
        for path, task in zip(discovered_paths, tasks, strict=True)
    )
    expected_source_paths = frozenset(path for _, path in expected_task_sources)
    assert sqlite_task_ids == expected_task_ids, {
        "missing_task_ids": sorted(expected_task_ids - sqlite_task_ids),
        "unexpected_task_ids": sorted(sqlite_task_ids - expected_task_ids),
        "projection": database_path.relative_to(root).as_posix(),
    }
    assert sqlite_source_paths == expected_source_paths, {
        "missing_source_paths": sorted(expected_source_paths - sqlite_source_paths),
        "unexpected_source_paths": sorted(sqlite_source_paths - expected_source_paths),
        "projection": database_path.relative_to(root).as_posix(),
    }
    sqlite_task_sources = frozenset(sqlite_rows)
    assert sqlite_task_sources == expected_task_sources, {
        "missing_task_sources": sorted(expected_task_sources - sqlite_task_sources),
        "unexpected_task_sources": sorted(sqlite_task_sources - expected_task_sources),
        "projection": database_path.relative_to(root).as_posix(),
    }

    manifest = json.loads(manifest_path.read_text())
    task_json_projection_sequence = tuple(
        entry["path"]
        for entry in manifest["projections"]
        if entry["projection_kind"] == "task-json"
    )
    duplicate_task_json_projections = sorted(
        path
        for path, count in Counter(task_json_projection_sequence).items()
        if count != 1
    )
    assert not duplicate_task_json_projections, {
        "duplicate_task_projections": duplicate_task_json_projections
    }
    task_json_projection_paths = frozenset(task_json_projection_sequence)
    assert task_json_projection_paths == expected_source_paths, {
        "missing_task_projections": sorted(
            expected_source_paths - task_json_projection_paths
        ),
        "unexpected_task_projections": sorted(
            task_json_projection_paths - expected_source_paths
        ),
    }
    assert not any(
        entry["path"].startswith("docs/") for entry in manifest["projections"]
    )

    assert {
        (edge["source"], edge["target"])
        for edge in graph["edges"]
        if edge["kind"] == "superseded_by"
    } == {
        (task.task_id, replacement)
        for task in tasks
        for replacement in task.superseded_by_task_ids
    }
