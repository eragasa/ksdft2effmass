r"""Software verification of ``HarnessValidationResult``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module owns the complete ordered repository-validation result contract.

Intrinsic and cross-object scope

Check ordering, aggregate status, claim boundaries, equality, and immutability are
intrinsic; domain check execution is excluded.

VVUQ and scientific exclusions

This is structural software verification only; scientific validation and UQ are
excluded.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.harness.pi.local import (
    HarnessValidationCheck,
    HarnessValidationResult,
)

SUT = HarnessValidationResult
pytestmark = pytest.mark.software_verification
_NAMES = (
    "python_evidence",
    "resources",
    "task_graph",
    "checkpoints",
    "skills",
    "control_state",
    "external_gates",
)
_BOUNDARIES = (
    "does not execute or establish pytest success",
    "does not execute or establish Ruff conformance",
    "does not execute or establish mypy conformance",
    "does not execute or establish Sphinx conformance",
    "does not establish numerical verification",
    "does not establish scientific validation",
    "does not establish uncertainty quantification",
    "does not authorize protected execution",
    "does not establish human acceptance",
)


def checks(*, warning: bool = False) -> tuple[HarnessValidationCheck, ...]:
    """Evidence ID: Owns no identifier; supports intrinsic result evidence.

    Requirement: Result tests require one complete stable check family.

    Method: Construct all seven literal checks and optionally replace the external
    gate with one warning.

    Oracle: The fixed check-name tuple and literal warning define support state.

    Acceptance: Return one complete ordered immutable check tuple.

    Interpretation: Failure indicates fixture construction drift.

    Limitations: This helper establishes no independent result claim.
    """  # noqa: E501
    values = [HarnessValidationCheck(name, "PASS", ()) for name in _NAMES]
    if warning:
        values[-1] = HarnessValidationCheck(
            "external_gates", "WARN", (("external.gate", None, "separate"),)
        )
    return tuple(values)


def test_constructor__complete_result__preserves_findings_boundaries_and_equality() -> (
    None
):
    """Evidence ID: software-verification.harness.repository-validation.result.complete-values

    Requirement: A result preserves complete ordered checks, their findings, aggregate
    status, and the exact ordered claim boundary with value semantics.

    Method: Construct two warning results from independent complete check tuples.

    Oracle: Literal check names and claim-boundary strings define the full contract.

    Acceptance: Results are equal; status, checks, finding, and boundaries are exact.

    Interpretation: Failure identifies incomplete or reordered aggregate state.

    Limitations: Domain checks are represented rather than executed.
    """  # noqa: E501
    result = SUT("WARN", checks(warning=True))
    assert result == SUT("WARN", checks(warning=True))
    assert tuple(check.name for check in result.checks) == _NAMES
    assert result.checks[-1].findings == (("external.gate", None, "separate"),)
    assert result.claim_boundaries == _BOUNDARIES


@pytest.mark.parametrize(
    ("status", "values", "boundaries", "error"),
    (
        pytest.param(
            "PASS", checks()[:-1], _BOUNDARIES, ValueError, id="missing_check"
        ),
        pytest.param(
            "PASS",
            checks()[:-1] + (checks()[-2],),
            _BOUNDARIES,
            ValueError,
            id="duplicate_check",
        ),
        pytest.param(
            "PASS",
            checks(warning=True),
            _BOUNDARIES,
            ValueError,
            id="aggregate_mismatch",
        ),
        pytest.param(
            "UNKNOWN", checks(), _BOUNDARIES, ValueError, id="unsupported_status"
        ),
        pytest.param(1, checks(), _BOUNDARIES, TypeError, id="wrong_status_type"),
        pytest.param(
            "PASS", list(checks()), _BOUNDARIES, TypeError, id="wrong_checks_container"
        ),
        pytest.param(
            "PASS",
            (*checks()[:-1], object()),
            _BOUNDARIES,
            TypeError,
            id="wrong_check_member",
        ),
        pytest.param(
            "PASS",
            checks(),
            list(_BOUNDARIES),
            TypeError,
            id="wrong_boundary_container",
        ),
        pytest.param(
            "PASS",
            checks(),
            (*_BOUNDARIES[:-1], 1),
            TypeError,
            id="wrong_boundary_member",
        ),
        pytest.param(
            "PASS", checks(), _BOUNDARIES[:-1], ValueError, id="missing_boundary"
        ),
        pytest.param(
            "PASS",
            checks(),
            (*_BOUNDARIES[:-1], _BOUNDARIES[0]),
            ValueError,
            id="duplicate_boundary",
        ),
        pytest.param(
            "PASS",
            checks(),
            tuple(reversed(_BOUNDARIES)),
            ValueError,
            id="reordered_boundary",
        ),
    ),
)
def test_constructor__aggregate_invariants__reject_invalid_partitions(
    status: object, values: object, boundaries: object, error: type[Exception]
) -> None:
    """Evidence ID: software-verification.harness.repository-validation.result.invalid-state

    Requirement: Complete check order, aggregate status, member types, and exact unique
    ordered claim boundaries fail closed.

    Method: Construct independently invalid aggregate partitions.

    Oracle: The fixed complete check and boundary tuples define exact acceptance.

    Acceptance: Every partition raises its expected exception category.

    Interpretation: Failure admits incomplete or inconsistent repository results.

    Limitations: Check-intrinsic finding structure is covered by its class owner.
    """  # noqa: E501
    with pytest.raises(error):
        SUT(status, values, boundaries)  # type: ignore[arg-type]


def test_constructor__immutability__rejects_field_assignment() -> None:
    """Evidence ID: software-verification.harness.repository-validation.result.immutable

    Requirement: Aggregate repository results reject public field mutation.

    Method: Assign a new status to a valid frozen result.

    Oracle: Frozen dataclass semantics define rejection.

    Acceptance: Assignment raises ``FrozenInstanceError``.

    Interpretation: Failure permits completed results to change after execution.

    Limitations: Check objects independently enforce their immutability.
    """  # noqa: E501
    result = SUT("PASS", checks())
    with pytest.raises(FrozenInstanceError):
        result.status = "FAIL"  # type: ignore[misc]
