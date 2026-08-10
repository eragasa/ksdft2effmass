r"""Software verification of ``_TaskStateQueryResult``.

Facet and represented meaning

The module owns the intrinsic represented behavior of ``_TaskStateQueryResult``.

Intrinsic and cross-object scope

Only the object's bounded contract is exercised; collaborators are literal inputs.

VVUQ and scientific exclusions

This is software verification only; scientific validation and UQ are excluded.
"""

import pytest

from ksdft2effmass.harness.pi.dbcontrol.inspection import _TaskStateQueryResult
from ksdft2effmass.harness.pi.validation import ValidationResult

SUT = _TaskStateQueryResult

pytestmark = pytest.mark.software_verification


def test_constructor__explicit_state__preserves_exact_values() -> None:
    """Evidence ID: software-verification.harness.dbcontrol.task-state-query-result.constructor.explicit-state

    Requirement: The generic query result preserves every reconciled field without implicit defaults.

    Method: Construct the record from distinct literal values.

    Oracle: Dataclass positional mapping is exact and independently visible.

    Acceptance: The first status fields and record statuses equal the supplied literals.

    Interpretation: Failure indicates orchestration result-field drift.

    Limitations: Query execution is excluded.
    """  # noqa: E501
    value = _TaskStateQueryResult(
        "active",
        "task.test",
        None,
        None,
        None,
        (),
        (),
        (),
        (),
        (),
        (),
        "not_declared",
        "not_declared",
        (),
        (),
        (),
        ValidationResult(1, "PASS", ()),
    )
    assert (value.task_status, value.active_task_id) == ("active", "task.test")
    assert (value.durable_run_record_status, value.durable_handoff_record_status) == (
        "not_declared",
        "not_declared",
    )
