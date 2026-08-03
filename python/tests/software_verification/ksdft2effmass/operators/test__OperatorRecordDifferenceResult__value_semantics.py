"""Software-verification value-semantics tests for OperatorRecordDifferenceResult."""

from collections.abc import Hashable
from dataclasses import FrozenInstanceError

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


def make_result(
    matrix: np.ndarray | None = None,
    *,
    energy_unit: str = "eV",
    compatibility_result: OperatorRecordCompatibilityResult | None = None,
) -> OperatorRecordDifferenceResult:
    if matrix is None:
        matrix = np.array([[1.0 + 0.0j]], dtype=np.complex128)
    if compatibility_result is None:
        compatibility_result = compatible_result_fixture
    return OperatorRecordDifferenceResult(compatibility_result, matrix, energy_unit)


compatible_result_fixture = compatible_result()


def test_owns_source_array_and_exposes_immutable_bytes_backed_storage() -> None:
    source = np.array([[1.0 + 0.0j]], dtype=np.complex128)

    result = make_result(source)
    source[0, 0] = 9.0 + 0.0j

    assert result.matrix[0, 0] == 1.0 + 0.0j
    assert not result.matrix.flags.writeable
    with pytest.raises(ValueError):
        result.matrix.setflags(write=True)


def test_dataclass_state_is_frozen() -> None:
    result = make_result()

    with pytest.raises(FrozenInstanceError):
        result.energy_unit = "hartree"  # type: ignore[misc]


def test_canonical_c_order_storage_preserves_fortran_source_values() -> None:
    source = np.asfortranarray(
        np.array(
            [[1.0 + 2.0j, 3.0 + 4.0j], [5.0 + 6.0j, 7.0 + 8.0j]],
            dtype=np.complex128,
        )
    )

    result = make_result(source)
    source[0, 0] = 99.0 + 0.0j

    np.testing.assert_array_equal(
        result.matrix,
        np.array(
            [[1.0 + 2.0j, 3.0 + 4.0j], [5.0 + 6.0j, 7.0 + 8.0j]],
            dtype=np.complex128,
        ),
    )
    assert result.matrix.flags.c_contiguous
    assert not result.matrix.flags.f_contiguous or result.matrix.shape == (1, 1)
    assert not result.matrix.flags.writeable
    with pytest.raises(ValueError):
        result.matrix.setflags(write=True)


def test_exact_equality_covers_complete_public_state() -> None:
    left = make_result(np.array([[1.0j]], dtype=np.complex128))
    same = make_result(np.array([[1.0j]], dtype=np.complex128))
    different_matrix = make_result(np.array([[2.0j]], dtype=np.complex128))
    different_unit = make_result(
        np.array([[1.0j]], dtype=np.complex128), energy_unit="hartree"
    )
    different_audit = make_result(
        np.array([[1.0j]], dtype=np.complex128),
        compatibility_result=compatible_result("other-reference", "candidate"),
    )

    assert left == same
    assert left != different_matrix
    assert left != different_unit
    assert left != different_audit
    assert (left == object()) is False


def test_unhashable_under_python_data_model() -> None:
    result = make_result()

    assert OperatorRecordDifferenceResult.__hash__ is None
    assert not isinstance(result, Hashable)
    with pytest.raises(TypeError):
        hash(result)
