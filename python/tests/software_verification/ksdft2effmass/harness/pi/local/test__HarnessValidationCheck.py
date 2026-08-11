r"""Software verification of ``HarnessValidationCheck``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module owns one stable named repository check and its structured findings.

Intrinsic and cross-object scope

Construction, deterministic finding state, status consistency, equality, and
immutability are intrinsic; repository execution is excluded.

VVUQ and scientific exclusions

This is structural software verification only; scientific validation and UQ are
excluded.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.harness.pi.local import HarnessValidationCheck

SUT = HarnessValidationCheck
pytestmark = pytest.mark.software_verification
_FINDING = ("task.invalid_record", "harness/tasks/x.json", "unsupported")


def test_constructor__fields__preserve_exact_value_semantics() -> None:
    """Evidence ID: software-verification.harness.repository-validation.check.values

    Requirement: A valid stable check preserves exact immutable field values and value
    equality.

    Method: Construct two equal warning checks from independent literal tuples.

    Oracle: The registered check name, status, and finding triple are fixed literals.

    Acceptance: The records are equal and every field remains exact.

    Interpretation: Failure identifies normalized check-state loss.

    Limitations: Aggregate status belongs to ``HarnessValidationResult``.
    """  # noqa: E501
    expected = SUT("task_graph", "WARN", (_FINDING,))
    assert expected == SUT("task_graph", "WARN", (_FINDING,))
    assert (expected.name, expected.status, expected.findings) == (
        "task_graph",
        "WARN",
        (_FINDING,),
    )


@pytest.mark.parametrize(
    ("name", "status", "findings", "error"),
    (
        pytest.param(1, "PASS", (), TypeError, id="wrong_name_type"),
        pytest.param("unknown", "PASS", (), ValueError, id="unsupported_name"),
        pytest.param("resources", 1, (), TypeError, id="wrong_status_type"),
        pytest.param("resources", "UNKNOWN", (), ValueError, id="unsupported_status"),
        pytest.param("resources", "PASS", [], TypeError, id="wrong_findings_container"),
        pytest.param(
            "resources", "FAIL", ((1, None, "bad"),), TypeError, id="wrong_code_type"
        ),
        pytest.param(
            "resources", "FAIL", (("code", 1, "bad"),), TypeError, id="wrong_path_type"
        ),
        pytest.param(
            "resources",
            "FAIL",
            (("code", None, 1),),
            TypeError,
            id="wrong_message_type",
        ),
        pytest.param(
            "resources",
            "FAIL",
            (_FINDING, _FINDING),
            ValueError,
            id="duplicate_finding",
        ),
        pytest.param(
            "resources",
            "FAIL",
            ((_FINDING[0], "z", "z"), _FINDING),
            ValueError,
            id="unsorted_findings",
        ),
        pytest.param(
            "resources", "PASS", (_FINDING,), ValueError, id="pass_with_finding"
        ),
        pytest.param("resources", "FAIL", (), ValueError, id="fail_without_finding"),
    ),
)
def test_constructor__invariants__reject_invalid_partitions(
    name: object, status: object, findings: object, error: type[Exception]
) -> None:
    """Evidence ID: software-verification.harness.repository-validation.check.invalid-state

    Requirement: Check names, statuses, finding structure/order/uniqueness, and
    status/finding consistency fail closed.

    Method: Construct one check for each independently invalid partition.

    Oracle: The closed check registry and literal structured-finding contract define
    exact exception categories.

    Acceptance: Every partition raises its expected error type.

    Interpretation: Failure admits ambiguous or internally inconsistent check state.

    Limitations: Finding-code domain vocabularies remain owned by their domain checks.
    """  # noqa: E501
    with pytest.raises(error):
        SUT(name, status, findings)  # type: ignore[arg-type]


def test_constructor__immutability__rejects_field_assignment() -> None:
    """Evidence ID: software-verification.harness.repository-validation.check.immutable

    Requirement: Validation checks reject public field mutation.

    Method: Assign a status to a valid frozen check.

    Oracle: Frozen dataclass semantics define rejection.

    Acceptance: Assignment raises ``FrozenInstanceError``.

    Interpretation: Failure permits aggregate state to change after validation.

    Limitations: Nested findings are immutable tuples.
    """  # noqa: E501
    check = SUT("resources", "PASS", ())
    with pytest.raises(FrozenInstanceError):
        check.status = "FAIL"  # type: ignore[misc]
