r"""Software verification of ``TaskStateInspectionResult``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

This module verifies immutable explicit-input Task-state results.

Intrinsic and cross-object scope

The sole SUT is ``TaskStateInspectionResult``; literal state and ``ValidationResult``
provide exact invariant oracles.

VVUQ and scientific exclusions

Passing establishes result representation only, not authority, runtime completeness,
numerical verification, scientific validation, UQ, or acceptance.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi import TaskStateInspectionResult, ValidationResult

pytestmark = pytest.mark.software_verification
SUT = TaskStateInspectionResult


def make_result(**changes: object) -> TaskStateInspectionResult:
    """Evidence ID: Owns no identifier; supports SV-HARNESS-069 and SV-HARNESS-070.

    Requirement: Constructor evidence requires one valid complete result baseline.

    Method: Build literal fields and apply explicit overrides.

    Oracle: The public constructor contract fixes the baseline.

    Acceptance: Return one result or propagate its public exception.

    Interpretation: Failure supports fixture diagnosis only.

    Limitations: The helper performs no repository inspection.
    """
    values: dict[str, object] = {
        "schema_version": 2,
        "repository_root": Path("/repo"),
        "task_id": "example.task",
        "task_status": "completed",
        "selected_task_id": None,
        "task_path": "harness/tasks/example.json",
        "selection_path": "harness/task-selection.json",
        "ownership_manifest_path": "ownership.json",
        "completion_validator_path": "tools/check.py",
        "completion_command": ("python", "tools/check.py"),
        "writers": (("implementation", "writer"),),
        "reviewers": (("review", "reviewer"),),
        "inspected_paths": (
            "harness/task-selection.json",
            "harness/tasks/example.json",
            "ownership.json",
            "tools/check.py",
        ),
        "read_paths": (
            "harness/task-selection.json",
            "harness/tasks/example.json",
            "ownership.json",
            "tools/check.py",
        ),
        "limitations": ("Runtime state is outside the result.",),
        "validation": ValidationResult(1, "PASS", ()),
    }
    values.update(changes)
    return SUT(**values)  # type: ignore[arg-type]


def test_constructor__durable_state__preserves_explicit_inputs() -> None:
    """Evidence ID: SV-HARNESS-069

    Requirement: The result preserves exact Task, selection, and ownership facts.

    Method: Construct the valid baseline and inspect representative fields.

    Oracle: Literal constructor values fix the expected state.

    Acceptance: Status, command, paths, and validation match exactly; state is frozen.

    Interpretation: Failure identifies result-field loss or mutability.

    Limitations: This does not establish that represented files exist.
    """
    result = make_result()
    assert result.task_status == "completed"
    assert result.selected_task_id is None
    assert result.completion_command == ("python", "tools/check.py")
    assert result.inspected_paths == result.read_paths
    assert result.validation.status == "PASS"
    with pytest.raises(FrozenInstanceError):
        result.task_status = "active"  # type: ignore[misc]


@pytest.mark.parametrize(
    "changes",
    (
        pytest.param(
            {"writers": (("z", "writer"), ("a", "other"))},
            id="unsorted_writers",
        ),
        pytest.param(
            {"read_paths": ("uninspected.json",)},
            id="read_path_not_inspected",
        ),
        pytest.param({"limitations": ("z", "a")}, id="unsorted_limitations"),
    ),
)
def test_constructor__deterministic_state__rejects_noncanonical_values(
    changes: dict[str, object],
) -> None:
    """Evidence ID: SV-HARNESS-070

    Requirement: Result collections have one deterministic representation.

    Method: Replace one baseline field with a controlled noncanonical value.

    Oracle: Public invariants require sorted unique values and read containment.

    Acceptance: Every noncanonical partition raises ValueError.

    Interpretation: Failure identifies weakened deterministic-result invariants.

    Limitations: Filesystem ordering is covered by the action evidence.
    """
    with pytest.raises(ValueError):
        make_result(**changes)
