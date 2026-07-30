"""Object tests for ``OperatorRecordCompatibilityIssue``.

The issue object stores only an authoritative mismatch code; human-readable text
is a canonical derived property.
"""

from dataclasses import FrozenInstanceError
from typing import Any

import pytest

from ksdft2effmass.operators import (
    OperatorRecordCompatibilityIssue,
    OperatorRecordCompatibilityMismatchCode,
)


def test_public_import_constructs_compatibility_issue() -> None:
    issue = OperatorRecordCompatibilityIssue(
        OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH
    )

    assert issue.code is OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH
    assert issue.description == "energy unit must match exactly"


def test_description_is_canonical_for_each_mismatch_code() -> None:
    descriptions = {
        code.description for code in OperatorRecordCompatibilityMismatchCode
    }

    assert len(descriptions) == len(tuple(OperatorRecordCompatibilityMismatchCode))
    assert "basis kind must match exactly" in descriptions


def test_compatibility_issue_is_immutable() -> None:
    issue = OperatorRecordCompatibilityIssue(
        OperatorRecordCompatibilityMismatchCode.BASIS_KIND_MISMATCH
    )

    with pytest.raises(FrozenInstanceError):
        issue.code = OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH  # type: ignore[misc]


@pytest.mark.parametrize("code", ["energy_unit_mismatch", object()])
def test_compatibility_issue_requires_public_mismatch_code(code: Any) -> None:
    with pytest.raises(TypeError, match="OperatorRecordCompatibilityMismatchCode"):
        OperatorRecordCompatibilityIssue(code)


def test_free_form_description_constructor_is_not_supported() -> None:
    with pytest.raises(TypeError):
        OperatorRecordCompatibilityIssue(  # type: ignore[call-arg]
            OperatorRecordCompatibilityMismatchCode.MATRIX_DIMENSION_MISMATCH,
            "contradictory free-form text",
        )


def test_compatibility_issue_has_no_json_serialization_api() -> None:
    issue = OperatorRecordCompatibilityIssue(
        OperatorRecordCompatibilityMismatchCode.STATE_SPACE_KIND_MISMATCH
    )

    assert not hasattr(issue, "to_json")
    assert not hasattr(issue, "to_dict")
    assert not hasattr(issue, "serialize")
    assert not hasattr(OperatorRecordCompatibilityIssue, "from_json")
    assert not hasattr(OperatorRecordCompatibilityIssue, "from_dict")
    assert not hasattr(OperatorRecordCompatibilityIssue, "deserialize")
