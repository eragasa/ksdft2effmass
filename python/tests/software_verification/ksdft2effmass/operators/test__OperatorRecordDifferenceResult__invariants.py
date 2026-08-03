"""Software-verification invariant tests for OperatorRecordDifferenceResult."""

from pathlib import Path
from typing import Any, cast

import numpy as np
import pytest

from ksdft2effmass.operators import (
    OperatorRecordCompatibilityIssue,
    OperatorRecordCompatibilityMismatchCode,
    OperatorRecordCompatibilityResult,
    OperatorRecordDifferenceResult,
)

pytestmark = pytest.mark.software_verification


class CustomArray(np.ndarray):
    """Synthetic ndarray subclass for strict public-boundary tests."""


def compatible_result() -> OperatorRecordCompatibilityResult:
    return OperatorRecordCompatibilityResult("reference", "candidate", ())


def test_requires_exact_compatibility_result_type() -> None:
    matrix = np.zeros((1, 1), dtype=np.complex128)

    with pytest.raises(TypeError, match="OperatorRecordCompatibilityResult"):
        OperatorRecordDifferenceResult(cast(Any, object()), matrix, "eV")


def test_requires_compatible_audit_result() -> None:
    issue = OperatorRecordCompatibilityIssue(
        OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH
    )
    incompatible = OperatorRecordCompatibilityResult("reference", "candidate", (issue,))

    with pytest.raises(ValueError, match="compatible"):
        OperatorRecordDifferenceResult(
            incompatible, np.zeros((1, 1), dtype=np.complex128), "eV"
        )


@pytest.mark.parametrize("energy_unit, error", [("", ValueError), (1, TypeError)])
def test_requires_nonempty_builtin_energy_unit_string(
    energy_unit: Any, error: type[Exception]
) -> None:
    with pytest.raises(error, match="energy_unit"):
        OperatorRecordDifferenceResult(
            compatible_result(), np.zeros((1, 1), dtype=np.complex128), energy_unit
        )


@pytest.mark.parametrize(
    "matrix, error, message",
    [
        ([[1.0]], TypeError, "exact NumPy ndarray"),
        (np.array([[1.0]], dtype=np.float64), TypeError, "np.complex128"),
        (
            np.array([[1.0 + 0.0j]], dtype=np.complex128).view(CustomArray),
            TypeError,
            "exact NumPy ndarray",
        ),
        (np.array([1.0 + 0.0j], dtype=np.complex128), ValueError, "square"),
        (np.ones((1, 2), dtype=np.complex128), ValueError, "square"),
        (np.zeros((0, 0), dtype=np.complex128), ValueError, "positive"),
        (np.array([[np.inf + 0.0j]], dtype=np.complex128), ValueError, "finite"),
        (np.array([[1.0 + np.nan * 1.0j]], dtype=np.complex128), ValueError, "finite"),
    ],
)
def test_requires_matrix_intrinsic_invariants(
    matrix: Any, error: type[Exception], message: str
) -> None:
    with pytest.raises(error, match=message):
        OperatorRecordDifferenceResult(compatible_result(), cast(Any, matrix), "eV")


def test_rejects_numpy_matrix_subclass() -> None:
    with pytest.warns(PendingDeprecationWarning):
        matrix = np.matrix([[1.0 + 0.0j]], dtype=np.complex128)

    with pytest.raises(TypeError, match="exact NumPy ndarray"):
        OperatorRecordDifferenceResult(compatible_result(), matrix, "eV")


def test_rejects_numpy_memmap(tmp_path: Path) -> None:
    memmap_path = tmp_path / "difference.dat"
    matrix = np.memmap(memmap_path, dtype=np.complex128, mode="w+", shape=(1, 1))
    matrix[0, 0] = 1.0 + 0.0j

    with pytest.raises(TypeError, match="exact NumPy ndarray"):
        OperatorRecordDifferenceResult(compatible_result(), matrix, "eV")
