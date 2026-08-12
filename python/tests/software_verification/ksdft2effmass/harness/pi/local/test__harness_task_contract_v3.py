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
from typing import Any, cast

import pytest
from jsonschema import Draft202012Validator  # type: ignore[import-untyped]

import ksdft2effmass.harness.pi.local as local_api
from ksdft2effmass.harness.pi import TaskStateInspectionRequest, TaskStateInspector
from ksdft2effmass.harness.pi.local import (
    HarnessTask,
    HarnessTaskDeserializer,
    HarnessTaskGraphValidator,
    HarnessTaskSerializer,
    TaskRecordAdapter,
)

from .conftest import repository_root
from .task_model_examples import make_task

pytestmark = pytest.mark.software_verification

_RETAINED_PUBLIC_NAMES = (
    "ArchivedTaskSource",
    "HarnessTask",
    "HarnessTaskSerializer",
    "HarnessTaskDeserializer",
    "HarnessTaskGraphValidator",
)


def test_public_api__task_model__exports_five_retained_interfaces() -> None:
    """Evidence ID: SV-HT-020

    Requirement: The Task-model module publicly defines the five retained core
    interfaces.

    Method: Compare package exports and module-owned public classes with a fixed list.

    Oracle: The bootstrap Task architecture names the exact five interfaces.

    Acceptance: All five names resolve, all are exported, and no other public class is
    defined by ``task_model``.

    Interpretation: Failure identifies a missing core interface or an unaccepted
    compatibility facade.

    Limitations: Unrelated project-local package exports are outside this assertion.
    """
    assert all(name in local_api.__all__ for name in _RETAINED_PUBLIC_NAMES)
    assert all(
        isinstance(getattr(local_api, name), type) for name in _RETAINED_PUBLIC_NAMES
    )
    task_model = __import__(
        "ksdft2effmass.harness.pi.local.task_model", fromlist=["unused"]
    )
    defined = {
        name
        for name, value in vars(task_model).items()
        if isinstance(value, type)
        and value.__module__ == task_model.__name__
        and not name.startswith("_")
    }
    assert defined == set(_RETAINED_PUBLIC_NAMES)


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
    SQLite state, projection manifest, and generated Task documentation under the same
    explicit repository root.

    Oracle: Regular ``harness/tasks/*.json`` files determine Task identity and
    cardinality; the accepted schema determines wire shape independently of generated
    projections.

    Acceptance: Every source file is discovered exactly once, parses as one canonical
    HarnessTask, and has a unique nonempty identity; source identities equal the graph,
    SQLite, manifest, and generated-document identities with no missing, unexpected, or
    duplicate projection, independent of source discovery order.

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
        Path("docs/harness/tasks"),
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
    task_directory, schema_path, graph_path, database_path, manifest_path, docs_path = (
        artifacts
    )

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
    projection_entries = tuple(manifest["projections"])
    task_json_projection_sequence = tuple(
        entry["path"]
        for entry in projection_entries
        if entry["projection_kind"] == "task-json"
    )
    task_document_projection_sequence = tuple(
        entry["path"]
        for entry in projection_entries
        if entry["projection_kind"] == "task-markdown"
    )
    index_projection_sequence = tuple(
        entry["path"]
        for entry in projection_entries
        if entry["projection_kind"] == "task-index-markdown"
    )
    duplicate_task_json_projections = sorted(
        path
        for path, count in Counter(task_json_projection_sequence).items()
        if count != 1
    )
    duplicate_task_document_projections = sorted(
        path
        for path, count in Counter(task_document_projection_sequence).items()
        if count != 1
    )
    duplicate_index_projections = sorted(
        path for path, count in Counter(index_projection_sequence).items() if count != 1
    )
    assert not duplicate_task_json_projections, {
        "duplicate_task_projections": duplicate_task_json_projections
    }
    assert not duplicate_task_document_projections, {
        "duplicate_generated_pages": duplicate_task_document_projections
    }
    assert not duplicate_index_projections, {
        "duplicate_task_indexes": duplicate_index_projections
    }
    task_json_projection_paths = frozenset(task_json_projection_sequence)
    task_document_projection_paths = frozenset(task_document_projection_sequence)
    index_projection_paths = frozenset(index_projection_sequence)
    expected_document_paths = frozenset(
        f"docs/harness/tasks/{task_id}.md" for task_id in expected_task_ids
    )
    assert task_json_projection_paths == expected_source_paths, {
        "missing_task_projections": sorted(
            expected_source_paths - task_json_projection_paths
        ),
        "unexpected_task_projections": sorted(
            task_json_projection_paths - expected_source_paths
        ),
    }
    assert task_document_projection_paths == expected_document_paths, {
        "missing_generated_pages": sorted(
            expected_document_paths - task_document_projection_paths
        ),
        "unexpected_generated_pages": sorted(
            task_document_projection_paths - expected_document_paths
        ),
    }
    assert index_projection_paths == frozenset({"docs/harness/tasks/index.md"}), {
        "missing_task_index": sorted(
            {"docs/harness/tasks/index.md"} - index_projection_paths
        ),
        "unexpected_task_indexes": sorted(
            index_projection_paths - {"docs/harness/tasks/index.md"}
        ),
    }

    observed_document_files = tuple(
        path for path in docs_path.glob("*.md") if path.is_file()
    )
    escaped_document_paths = sorted(
        path.relative_to(root).as_posix()
        for path in observed_document_files
        if path.is_symlink()
        or not path.resolve(strict=True).is_relative_to(resolved_root)
    )
    assert not escaped_document_paths, {
        "symlinked_or_escaped_generated_pages": escaped_document_paths
    }
    observed_document_paths = frozenset(
        path.relative_to(root).as_posix() for path in observed_document_files
    )
    observed_task_document_paths = observed_document_paths - index_projection_paths
    assert observed_task_document_paths == expected_document_paths, {
        "missing_generated_pages": sorted(
            expected_document_paths - observed_task_document_paths
        ),
        "unexpected_generated_pages": sorted(
            observed_task_document_paths - expected_document_paths
        ),
    }
    projected_document_task_ids = frozenset(
        Path(path).stem for path in observed_task_document_paths
    )
    assert projected_document_task_ids == expected_task_ids, {
        "missing_task_ids": sorted(expected_task_ids - projected_document_task_ids),
        "unexpected_task_ids": sorted(projected_document_task_ids - expected_task_ids),
        "projection": docs_path.relative_to(root).as_posix(),
    }

    assert {
        (edge["source"], edge["target"])
        for edge in graph["edges"]
        if edge["kind"] == "superseded_by"
    } == {
        (task.task_id, replacement)
        for task in tasks
        for replacement in task.superseded_by_task_ids
    }


def test_artifact__mixed_task_formats__adapt_in_one_explicit_chain() -> None:
    """Evidence ID: SV-HT-031

    Requirement: One chain may select Markdown, version-1 JSON, and version-3 JSON
    without transferring JSON-owned Task fields into the chain.

    Method: Adapt three synthetic records and then duplicate v3 status in its entry.

    Oracle: Retained Markdown/v1 behavior and version-3 dispatch define the exact
    references and fail-closed duplication rule.

    Acceptance: Mixed adaptation passes in Task-ID order; duplicated status fails.

    Interpretation: Failure identifies compatibility or authority-boundary drift.

    Limitations: Synthetic records do not migrate maintained Tasks.
    """
    markdown_path = "records/markdown.md"
    v1_path = "records/version-one.json"
    v3_path = "records/version-three.json"
    v1 = {
        "schema_version": 1,
        "task_id": "format.v1",
        "title": "Version one",
        "status": "completed",
        "parent_task_id": None,
        "task_prerequisite_ids": [],
        "external_prerequisite_ids": [],
        "explicit_activation_required": False,
        "objective": "Retain v1 compatibility.",
        "authority_reference_paths": ["records/decision.md"],
        "authorized_scope": ["Adapt synthetic data."],
        "completion_criteria": ["Reference is produced."],
        "exclusions": ["No migration."],
        "intake_path": "records/v1.intake.md",
        "archived_source": None,
    }
    v3 = make_task(task_id="format.v3", status="active")
    chain: dict[str, Any] = {
        "active_task": v3.task_id,
        "automatic_successor_activation": False,
        "explicitly_activated_task_ids": [v3.task_id],
        "task_sequence": [
            {
                "id": "format.markdown",
                "record": markdown_path,
                "status": "completed",
                "prerequisites": [],
            },
            {"id": "format.v1", "record": v1_path},
            {"id": v3.task_id, "record": v3_path},
        ],
    }
    documents = (
        (markdown_path, b"# Markdown Task\n\nStatus: completed\n"),
        (v1_path, json.dumps(v1).encode()),
        (v3_path, HarnessTaskSerializer().execute(v3)),
    )
    adapted = TaskRecordAdapter().execute(documents, json.dumps(chain).encode(), b"{}")
    assert adapted.validation.status == "PASS"
    assert tuple(item.task_id for item in cast(Any, adapted.value)) == (
        "format.markdown",
        "format.v1",
        "format.v3",
    )
    chain["task_sequence"][2]["status"] = "active"
    duplicated = TaskRecordAdapter().execute(
        documents, json.dumps(chain).encode(), b"{}"
    )
    assert duplicated.validation.status == "FAIL"


@pytest.mark.parametrize(
    "record_kind",
    (
        pytest.param("markdown", id="markdown_record_selected"),
        pytest.param("v1", id="version_one_json_selected"),
        pytest.param("v3", id="version_three_json_selected"),
    ),
)
def test_method__task_state_inspector__preserves_format_selection(
    tmp_path: Path, record_kind: str
) -> None:
    """Evidence ID: SV-HT-032

    Requirement: TaskStateInspector preserves selected Markdown, v1 JSON, and v3 JSON
    status behavior.

    Method: Build and inspect one bounded temporary chain per format.

    Oracle: The inspector contract assigns Markdown status to the chain and JSON status
    to the selected JSON record.

    Acceptance: Every format passes with the exact selected path and expected status.

    Interpretation: Failure identifies selected-state compatibility drift.

    Limitations: Full local schema validation remains owned by TaskRecordAdapter.
    """
    task_id = "format.task"
    suffix = "md" if record_kind == "markdown" else "json"
    record_path = f"records/{record_kind}.{suffix}"
    chain_path = "records/chain.json"
    chain = {
        "active_task": None,
        "task_sequence": [
            {
                "id": task_id,
                "record": record_path,
                "status": "chain_status",
                "prerequisites": [],
            }
        ],
    }
    (tmp_path / "records").mkdir()
    (tmp_path / chain_path).write_text(json.dumps(chain))
    if record_kind == "markdown":
        (tmp_path / record_path).write_text("# Task\n\nStatus: ignored prose\n")
        expected_status = "chain_status"
    elif record_kind == "v1":
        (tmp_path / record_path).write_text(
            json.dumps({"task_id": task_id, "status": "v1_status"})
        )
        expected_status = "v1_status"
    else:
        task = make_task(task_id=task_id, status="v3_status")
        (tmp_path / record_path).write_bytes(HarnessTaskSerializer().execute(task))
        expected_status = "v3_status"
    result = TaskStateInspector().execute(
        TaskStateInspectionRequest(1, tmp_path, chain_path, task_id)
    )
    assert result.validation.status == "PASS"
    assert result.task_status == expected_status
    assert result.task_record_path == record_path
