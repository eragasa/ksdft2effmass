"""Software-verification tests for the public operator-record API.

These tests exercise object construction, invariants, numerical policies, and
serialization or comparison contracts for maintained first-party Python code.
They are software verification checks and do not constitute scientific
validation of a represented Hamiltonian or reduced model.
"""

from typing import Any, cast

import pytest

from ksdft2effmass.operators import (
    IncompatibleOperatorRecordsError,
    OperatorRecordCompatibilityIssue,
    OperatorRecordCompatibilityMismatchCode,
    OperatorRecordCompatibilityResult,
)


def make_result() -> OperatorRecordCompatibilityResult:
    return OperatorRecordCompatibilityResult(
        "reference",
        "candidate",
        (
            OperatorRecordCompatibilityIssue(
                OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH,
            ),
        ),
    )


def test_public_import_constructs_error_with_public_compatibility_result() -> None:
    result = make_result()
    error = IncompatibleOperatorRecordsError(result)

    assert error.compatibility_result is result
    assert "operator records are not compatible" in str(error)
    assert "energy_unit_mismatch" in str(error)


def test_error_requires_public_compatibility_result() -> None:
    with pytest.raises(TypeError, match="compatibility_result"):
        IncompatibleOperatorRecordsError(cast(Any, object()))


def test_error_has_no_json_serialization_api() -> None:
    error = IncompatibleOperatorRecordsError(make_result())

    assert not hasattr(error, "to_json")
    assert not hasattr(error, "to_dict")
    assert not hasattr(error, "serialize")
    assert not hasattr(IncompatibleOperatorRecordsError, "from_json")
    assert not hasattr(IncompatibleOperatorRecordsError, "from_dict")
    assert not hasattr(IncompatibleOperatorRecordsError, "deserialize")
