"""Software-verification tests for compatibility audit result invariants.

The tests exercise direct ResultObject construction, not only analyzer-produced
values, because the immutable audit object must independently protect canonical
rule coverage, issue ordering, issue uniqueness, and derived compatibility
state.  These are software contract checks, not scientific validation.
"""

from dataclasses import FrozenInstanceError
from typing import Any

import pytest

from ksdft2effmass.operators import (
    OperatorRecordCompatibilityIssue,
    OperatorRecordCompatibilityMismatchCode,
    OperatorRecordCompatibilityResult,
)

CANONICAL_RULES = tuple(OperatorRecordCompatibilityMismatchCode)


def make_issue(
    code: OperatorRecordCompatibilityMismatchCode = (
        OperatorRecordCompatibilityMismatchCode.OPERATOR_KIND_MISMATCH
    ),
) -> OperatorRecordCompatibilityIssue:
    """Return a deterministic issue fixture for one canonical mismatch code."""

    return OperatorRecordCompatibilityIssue(code)


def test_public_import_constructs_result_and_derives_canonical_rules() -> None:
    issue = make_issue()
    result = OperatorRecordCompatibilityResult("reference", "candidate", (issue,))

    assert result.reference_identifier == "reference"
    assert result.candidate_identifier == "candidate"
    assert result.issues == (issue,)
    assert result.rules_applied == CANONICAL_RULES


def test_is_compatible_is_derived_from_empty_issue_collection() -> None:
    compatible = OperatorRecordCompatibilityResult("r", "c", ())
    incompatible = OperatorRecordCompatibilityResult("r", "c", (make_issue(),))

    assert compatible.is_compatible
    assert not incompatible.is_compatible
    unexpected_kwargs: dict[str, Any] = {"is_compatible": False}
    with pytest.raises(TypeError):
        OperatorRecordCompatibilityResult("r", "c", (), **unexpected_kwargs)


def test_result_is_immutable() -> None:
    result = OperatorRecordCompatibilityResult("r", "c", ())

    with pytest.raises(FrozenInstanceError):
        result.issues = (make_issue(),)  # type: ignore[misc]


@pytest.mark.parametrize("identifier", ["", 1, object()])
def test_result_requires_nonempty_identifiers(identifier: Any) -> None:
    expected_error = ValueError if identifier == "" else TypeError

    with pytest.raises(expected_error, match="identifier"):
        OperatorRecordCompatibilityResult(identifier, "candidate", ())
    with pytest.raises(expected_error, match="identifier"):
        OperatorRecordCompatibilityResult("reference", identifier, ())


def test_result_requires_public_issue_type() -> None:
    with pytest.raises(TypeError, match="issues"):
        OperatorRecordCompatibilityResult("r", "c", (object(),))  # type: ignore[arg-type]


def test_result_structurally_prevents_constructor_rule_override() -> None:
    with pytest.raises(TypeError):
        OperatorRecordCompatibilityResult("r", "c", (), CANONICAL_RULES)  # type: ignore[call-arg]


def test_result_rejects_duplicated_issue_codes() -> None:
    issue = make_issue()

    with pytest.raises(ValueError, match="must not be duplicated"):
        OperatorRecordCompatibilityResult("r", "c", (issue, issue))


def test_result_rejects_noncanonical_issue_ordering() -> None:
    issues = (
        make_issue(OperatorRecordCompatibilityMismatchCode.OPERATOR_KIND_MISMATCH),
        make_issue(OperatorRecordCompatibilityMismatchCode.STATE_SPACE_KIND_MISMATCH),
    )

    with pytest.raises(ValueError, match="canonical mismatch-code order"):
        OperatorRecordCompatibilityResult("r", "c", issues)


def test_result_rejects_non_tuple_issue_collection() -> None:
    with pytest.raises(TypeError, match="tuple"):
        OperatorRecordCompatibilityResult("r", "c", [make_issue()])  # type: ignore[arg-type]


def test_result_rejects_string_issue_collection() -> None:
    with pytest.raises(TypeError, match="issues"):
        OperatorRecordCompatibilityResult("r", "c", "issues")  # type: ignore[arg-type]


def test_compatibility_result_has_no_json_serialization_api() -> None:
    result = OperatorRecordCompatibilityResult("reference", "candidate", ())

    assert not hasattr(result, "to_json")
    assert not hasattr(result, "to_dict")
    assert not hasattr(result, "serialize")
    assert not hasattr(OperatorRecordCompatibilityResult, "from_json")
    assert not hasattr(OperatorRecordCompatibilityResult, "from_dict")
    assert not hasattr(OperatorRecordCompatibilityResult, "deserialize")
