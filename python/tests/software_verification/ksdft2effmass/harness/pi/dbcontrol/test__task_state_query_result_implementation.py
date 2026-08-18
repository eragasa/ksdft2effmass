r"""Software verification of private Task-state query result.

Evidence profile: routine

Bounded artifact scope: private Task-state query-result representation.

Facet and represented meaning

The module verifies exact represented behavior of ``_TaskStateQueryResult``.

Intrinsic and cross-object scope

Only constructor mapping is exercised; collaborators are literal inputs.

VVUQ and scientific exclusions

This is software verification only; authority, scientific validation, and UQ are
excluded.
"""

import pytest

from ksdft2effmass.harness.pi.dbcontrol.inspection import _TaskStateQueryResult
from ksdft2effmass.harness.pi.validation import ValidationResult

pytestmark = pytest.mark.software_verification


def test_constructor__explicit_state__preserves_exact_values() -> None:
    """Evidence ID: software-verification.harness.dbcontrol.task-state-query-result.constructor.explicit-state

    Requirement: The private query result preserves every explicit field.

    Method: Construct the record from distinct literal values.

    Oracle: Dataclass positional mapping is exact.

    Acceptance: Status, selection, assignments, paths, limits, and validation agree.

    Interpretation: Failure indicates orchestration result-field drift.

    Limitations: Query execution is excluded.
    """  # noqa: E501
    validation = ValidationResult(1, "PASS", ())
    value = _TaskStateQueryResult(
        "active",
        "task.test",
        "check.py",
        ("python", "check.py"),
        (("writer", "agent"),),
        (("review", "reviewer"),),
        ("task.json",),
        ("task.json",),
        ("Runtime excluded.",),
        validation,
    )
    assert value.task_status == "active"
    assert value.selected_task_id == "task.test"
    assert value.completion_validator_path == "check.py"
    assert value.validation is validation
