r"""Software verification of generic dbcontrol task-state-query implementation artifact.

Evidence profile: routine

Bounded artifact scope: generic dbcontrol private task-state-query implementation behavior.

Facet and represented meaning

The module owns the intrinsic represented behavior of ``_TaskStateQuery``.

Intrinsic and cross-object scope

Only the object's bounded contract is exercised; collaborators are literal inputs.

VVUQ and scientific exclusions

This is software verification only; scientific validation and UQ are excluded.
"""  # noqa: E501

import pytest

from ksdft2effmass.harness.pi.dbcontrol.inspection import _TaskStateQuery

SUT = _TaskStateQuery

pytestmark = pytest.mark.software_verification


def test_staticmethod__record_status__distinguishes_declared_missing() -> None:
    """Evidence ID: software-verification.harness.dbcontrol.task-state-query.static-method.record-status

    Requirement: Durable-record status distinguishes undeclared, inspected, and declared-missing paths.

    Method: Evaluate three literal path/missing-set partitions.

    Oracle: The accepted vocabulary maps absence, present declaration, and missing declaration exactly.

    Acceptance: Results equal ``not_declared``, ``inspected``, and ``declared_missing`` in order.

    Interpretation: Failure indicates loss of durable-evidence absence meaning.

    Limitations: Filesystem access is excluded.
    """  # noqa: E501
    classify = _TaskStateQuery._record_status
    assert (
        classify((), set()),
        classify(("run.json",), set()),
        classify(("run.json",), {"run.json"}),
    ) == ("not_declared", "inspected", "declared_missing")
