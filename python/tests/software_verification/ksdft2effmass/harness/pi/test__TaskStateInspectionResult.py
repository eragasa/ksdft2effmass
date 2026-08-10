r"""Software verification of ``TaskStateInspectionResult``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

This module verifies immutable bounded task-state results and deterministic collections.

Intrinsic and cross-object scope

The sole SUT is ``TaskStateInspectionResult``; ``ValidationResult`` is a collaborator
and literal state supplies the exact invariant oracle.

VVUQ and scientific exclusions

Passing establishes result representation only, not repository completeness, runtime
history, numerical verification, scientific validation, UQ, or acceptance.
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

    Requirement: Result tests require one complete valid represented baseline.

    Method: Construct the public result from literal values and apply explicit field
    overrides.

    Oracle: The result constructor contract fixes the valid baseline and permitted
    overrides.

    Acceptance: The helper returns exactly one public result or propagates its public
    exception.

    Interpretation: Failure supports diagnosis of result-construction or fixture drift
    only.

    Limitations: This helper owns no evidence and does not inspect repository state.
    """
    values: dict[str, object] = {
        "schema_version": 1,
        "repository_root": Path("/repo"),
        "task_id": "example.task",
        "task_status": "completed",
        "active_task_id": None,
        "chain_path": "chain.json",
        "task_record_path": "task.md",
        "ownership_manifest_path": "ownership.json",
        "completion_validator_path": "tools/check.py",
        "completion_command": ("python", "tools/check.py"),
        "writers": (("implementation", "writer"),),
        "reviewers": (("review", "reviewer"),),
        "artifact_paths": (),
        "run_record_paths": (),
        "handoff_record_paths": (),
        "durable_run_record_status": "not_declared",
        "durable_handoff_record_status": "not_declared",
        "inspected_paths": (
            "chain.json",
            "ownership.json",
            "task.md",
            "tools/check.py",
        ),
        "read_paths": ("chain.json", "ownership.json", "task.md", "tools/check.py"),
        "limitations": ("Runtime state is outside the result.",),
        "validation": ValidationResult(1, "PASS", ()),
    }
    values.update(changes)
    return SUT(**values)  # type: ignore[arg-type]


def test_constructor__durable_state__preserves_explicit_statuses() -> None:
    """Evidence ID: SV-HARNESS-069

    Requirement: The result preserves explicit durable references, declaration statuses,
    and limits.

    Method: Construct the complete valid baseline and inspect representative public
    fields.

    Oracle: Literal constructor values independently fix the expected represented state.

    Acceptance: Task status, completion command, record status, paths, and validation
    match exactly.

    Interpretation: Failure identifies result-field loss, coercion, or construction
    drift.

    Limitations: This does not establish that represented files exist.
    """
    result = make_result()
    assert result.task_status == "completed"
    assert result.completion_command == ("python", "tools/check.py")
    assert result.durable_run_record_status == "not_declared"
    assert result.inspected_paths == result.read_paths
    assert result.validation.status == "PASS"
    with pytest.raises(FrozenInstanceError):
        result.task_status = "active"  # type: ignore[misc]


@pytest.mark.parametrize(
    "changes",
    (
        pytest.param(
            {"writers": (("z", "writer"), ("a", "other"))}, id="unsorted_writers"
        ),
        pytest.param(
            {"read_paths": ("uninspected.json",)}, id="read_path_not_inspected"
        ),
        pytest.param(
            {"durable_run_record_status": "unknown"}, id="unknown_record_status"
        ),
        pytest.param({"limitations": ("z", "a")}, id="unsorted_limitations"),
    ),
)
def test_constructor__deterministic_state__rejects_noncanonical_values(
    changes: dict[str, object],
) -> None:
    """Evidence ID: SV-HARNESS-070

    Requirement: Result collections and declaration statuses have one deterministic
    representation.

    Method: Replace one valid baseline field with a controlled noncanonical value.

    Oracle: The public result invariant requires sorted unique values, known statuses,
    and
    read-path containment.

    Acceptance: Every declared noncanonical partition raises ValueError.

    Interpretation: Failure identifies weakened deterministic-result invariants.

    Limitations: Action ordering and filesystem reads are covered separately.
    """
    with pytest.raises(ValueError):
        make_result(**changes)
