"""Software-verification construction tests for OperatorRecordDifferenceResult."""

import numpy as np
import pytest

from ksdft2effmass.operators import (
    OperatorRecordCompatibilityResult,
    OperatorRecordDifferenceResult,
)

pytestmark = pytest.mark.software_verification


def compatible_result(
    reference_identifier: str = "reference", candidate_identifier: str = "candidate"
) -> OperatorRecordCompatibilityResult:
    return OperatorRecordCompatibilityResult(
        reference_identifier, candidate_identifier, ()
    )


def test_constructs_valid_difference_result_with_public_metadata() -> None:
    matrix = np.array([[1.0 + 2.0j]], dtype=np.complex128)

    result = OperatorRecordDifferenceResult(compatible_result(), matrix, "eV")

    assert result.reference_identifier == "reference"
    assert result.candidate_identifier == "candidate"
    assert result.energy_unit == "eV"
    assert result.shape == (1, 1)
    assert result.matrix_dimension == 1
    np.testing.assert_array_equal(result.matrix, matrix)


def test_accepts_arbitrary_positive_square_dimension() -> None:
    matrix = np.eye(3, dtype=np.complex128)

    result = OperatorRecordDifferenceResult(compatible_result(), matrix, "eV")

    assert result.shape == (3, 3)
    assert result.matrix_dimension == 3
    np.testing.assert_array_equal(result.matrix, matrix)


def test_has_no_serialization_or_impurity_interpretation_api() -> None:
    result = OperatorRecordDifferenceResult(
        compatible_result(), np.zeros((1, 1), dtype=np.complex128), "eV"
    )

    assert not hasattr(result, "serialize")
    assert not hasattr(result, "deserialize")
    assert not hasattr(result, "to_impurity_operator")
