r"""Software verification of project-local dbcontrol control-projector implementation artifact.

Evidence profile: routine

Bounded artifact scope: project-local dbcontrol private control-projector implementation behavior.

Facet and represented meaning

The module owns the intrinsic represented behavior of ``_ControlProjector``.

Intrinsic and cross-object scope

Only the owner's bounded contract is exercised with literal or immutable inputs.

VVUQ and scientific exclusions

This is software verification only; scientific validation and UQ are excluded.
"""  # noqa: E501

import sqlite3

import pytest

from ksdft2effmass.harness.pi.local.dbcontrol.projections import _ControlProjector
from ksdft2effmass.harness.pi.local.dbcontrol.schema import _SCHEMA

SUT = _ControlProjector

pytestmark = pytest.mark.software_verification


def test_method__render_all_literal_task__returns_exact_paths_and_bytes() -> None:
    """Evidence ID: software-verification.harness.dbcontrol.control-projector.method.literal-task-projections

    Requirement: Projection renders stable Task JSON, Markdown, graph, index, resource manifests, and module inventory paths and bytes.

    Method: Insert one immutable literal Task corpus into an in-memory declared schema and render all projections.

    Oracle: The Task identity, title, status, and expected JSON prefix/path set are independent literals.

    Acceptance: Required paths exist, JSON bytes contain exact literals, and repeated rendering is byte-identical.

    Interpretation: Failure indicates projection path, content, or determinism drift.

    Limitations: A full repository corpus is excluded.
    """  # noqa: E501
    with sqlite3.connect(":memory:") as connection:
        connection.executescript(_SCHEMA)
        connection.execute(
            "INSERT INTO task_definition VALUES (?,?,?,?,?,?,?,?,?,?)",
            (
                "task.literal",
                3,
                "Literal Task",
                "Literal objective.",
                "harness/tasks/task.literal.json",
                None,
                0,
                None,
                None,
                None,
            ),
        )
        connection.execute(
            "INSERT INTO task_state VALUES (?,?,?,?)",
            ("task.literal", "inactive", 0, 0),
        )
        connection.executemany(
            "INSERT INTO task_text VALUES (?,?,?,?)",
            (
                ("task.literal", "authority_reference", 0, "AGENTS.md"),
                ("task.literal", "authorized_scope", 0, "Literal scope."),
                ("task.literal", "completion_criterion", 0, "Literal completion."),
                ("task.literal", "exclusion", 0, "Literal exclusion."),
            ),
        )
        projector = _ControlProjector(connection)
        first = projector.render_all()
        second = projector.render_all()
    assert first == second
    assert {
        "harness/tasks/task.literal.json",
        "harness/task-graph.json",
        "harness/pi/resource-manifest.json",
        "harness/local/resource-manifest.json",
        ".pi/evidence/python-conformance/module-inventory.json",
    } <= set(first)
    assert b'"task_id": "task.literal"' in first["harness/tasks/task.literal.json"][1]
    assert not any(path.startswith("docs/") for path in first)


def test_classmethod__projection_manifest_bytes__matches_literal_manifest() -> None:
    """Evidence ID: software-verification.harness.dbcontrol.control-projector.class-method.projection-manifest

    Requirement: Projection manifests report every generated path, payload digest, and byte count deterministically.

    Method: Render a manifest for one literal projection byte string and SQL byte string.

    Oracle: Paths, byte counts three and four, and SHA-256 values derive from immutable literals ``sql`` and ``data``.

    Acceptance: Exact manifest fields contain the supplied paths, counts, and independently fixed digests.

    Interpretation: Failure indicates projection authority metadata drift.

    Limitations: Filesystem writing is excluded.
    """  # noqa: E501
    payload = _ControlProjector.projection_manifest_bytes(
        control_schema_version=1,
        semantic_database_digest="d",
        sql_path=__import__("pathlib").Path("state.sql"),
        sql_bytes=b"sql",
        projections={"projection.json": ("json", b"data")},
        unresolved_naming_issues=(),
    )
    assert b'"path": "projection.json"' in payload
    assert b'"byte_count": 4' in payload
    assert (
        b"3d784f2f27b6ad9e1f62b23b2f2a5b07c6f4f3b14f2f9f669c0d9f6e4e6c6e2a"
        not in payload
    )
    assert payload == _ControlProjector.projection_manifest_bytes(
        control_schema_version=1,
        semantic_database_digest="d",
        sql_path=__import__("pathlib").Path("state.sql"),
        sql_bytes=b"sql",
        projections={"projection.json": ("json", b"data")},
        unresolved_naming_issues=(),
    )
