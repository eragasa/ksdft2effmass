r"""Software verification of ``TaskStateInspectionRequest``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

This module verifies the immutable explicit Task, selection, and optional ownership
inspection request.

Intrinsic and cross-object scope

The sole SUT is ``TaskStateInspectionRequest``; literal paths and identifiers provide
exact constructor oracles.

VVUQ and scientific exclusions

Passing establishes request software semantics only, not repository truth, authority,
runtime history, numerical verification, scientific validation, UQ, or acceptance.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi import TaskStateInspectionRequest

pytestmark = pytest.mark.software_verification
SUT = TaskStateInspectionRequest


def test_constructor__explicit_boundary__preserves_exact_state(tmp_path: Path) -> None:
    """Evidence ID: SV-HARNESS-066

    Requirement: The request represents exact Task, selection, identity, root, and
    optional operation-scoped ownership inputs.

    Method: Construct the request from controlled literal values.

    Oracle: Constructor inputs independently fix every represented field.

    Acceptance: All public fields equal the supplied values exactly.

    Interpretation: Failure identifies request construction or represented-state drift.

    Limitations: Filesystem existence and cross-record validity are action-owned.
    """
    root = tmp_path.resolve()
    request = SUT(
        2,
        root,
        "harness/tasks/example.json",
        "harness/task-selection.json",
        "example.task",
        ".pi/task-ownership/example.json",
    )
    assert request.schema_version == 2
    assert request.repository_root == root
    assert request.task_path == "harness/tasks/example.json"
    assert request.selection_path == "harness/task-selection.json"
    assert request.task_id == "example.task"
    assert request.ownership_manifest_path == ".pi/task-ownership/example.json"


def test_field__immutable_state__rejects_reassignment(tmp_path: Path) -> None:
    """Evidence ID: SV-HARNESS-067

    Requirement: A Task-state inspection request is operationally immutable.

    Method: Construct a valid request and attempt public identity reassignment.

    Oracle: Frozen dataclass semantics require FrozenInstanceError.

    Acceptance: Reassignment raises exactly FrozenInstanceError.

    Interpretation: Failure identifies loss of the immutable request boundary.

    Limitations: Filesystem behavior is excluded.
    """
    request = SUT(2, tmp_path.resolve(), "task.json", "selection.json", "task")
    with pytest.raises(FrozenInstanceError):
        request.task_id = "other.task"  # type: ignore[misc]


@pytest.mark.parametrize(
    "arguments",
    (
        pytest.param(
            (True, Path("/tmp"), "task.json", "selection.json", "task"),
            id="boolean_version_wrong_type",
        ),
        pytest.param(
            (2, "/tmp", "task.json", "selection.json", "task"),
            id="string_root_wrong_type",
        ),
        pytest.param(
            (2, Path("relative"), "task.json", "selection.json", "task"),
            id="relative_root",
        ),
        pytest.param(
            (2, Path("/tmp"), "/task.json", "selection.json", "task"),
            id="absolute_task_path",
        ),
        pytest.param(
            (2, Path("/tmp"), "task.json", "../selection.json", "task"),
            id="traversal_selection_path",
        ),
        pytest.param(
            (2, Path("/tmp"), "task.json", "selection.json", "bad task"),
            id="invalid_task_identity",
        ),
    ),
)
def test_constructor__input_invariants__reject_invalid_values(
    arguments: tuple[object, ...],
) -> None:
    """Evidence ID: SV-HARNESS-068

    Requirement: Request fields reject wrong semantic types and unsafe boundaries.

    Method: Supply one controlled invalid constructor partition per case.

    Oracle: The explicit-input contract fixes version, Path, ResourcePath, and ID forms.

    Acceptance: Every partition raises TypeError or ValueError.

    Interpretation: Failure identifies weakened explicit-input invariants.

    Limitations: Existing-file and symlink checks are action-owned.
    """
    with pytest.raises((TypeError, ValueError)):
        SUT(*arguments)  # type: ignore[arg-type]
