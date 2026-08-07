r"""Numerical verification of ``OperatorRecordResidualAnalyzer``.

Facet and represented meaning
-----------------------------
This class-owned module owns the exact-zero floating-point facet for a represented
``1 x 1`` complex128 difference. The mathematical maximum-entry, Frobenius, and
spectral norms of the zero matrix are all exactly zero in eV.

Intrinsic and cross-object scope
--------------------------------
The SUT is ``OperatorRecordResidualAnalyzer``. A public compatible difference supplies
an exact zero matrix, and exact arithmetic supplies the independent oracle.
``RuntimeWarning`` is promoted to error; no approximate tolerance or backend-dependent
regression envelope is accepted.

VVUQ and scientific exclusions
------------------------------
Passing establishes exact agreement with the stated zero-matrix mathematics and public
metric ordering for this shape and dtype. It does not establish nonzero floating-point
error bounds, arbitrary-matrix numerical behavior, physical correctness, scientific
validation, UQ, portability, or cross-language agreement.
"""

import warnings

import numpy as np
import numpy.typing as npt
import pytest

from ksdft2effmass.operators import (
    OperatorRecordComparisonResult,
    OperatorRecordCompatibilityResult,
    OperatorRecordDifferenceResult,
    OperatorRecordResidualAnalyzer,
)

pytestmark = pytest.mark.numerical_verification

SUT = OperatorRecordResidualAnalyzer


def make_zero_difference(
    matrix: npt.NDArray[np.complex128],
) -> OperatorRecordDifferenceResult:
    r"""Evidence ID
    Owns no identifier; supports ``NV-ORA-017``.
    Requirement
    Exact-zero analysis requires a compatible represented difference containing the
    supplied complex128 matrix in eV.
    Method
    Construct the public compatibility and difference ResultObjects directly; this
    helper performs no residual calculation and owns no assertion result.
    Oracle
    Literal identifiers, the empty compatibility issue tuple, the supplied matrix, and
    the eV unit determine the fixture independently of residual analysis.
    Acceptance
    The helper returns the public difference object with those exact constructor values.
    Interpretation
    A helper defect can invalidate setup but cannot independently pass the evidence.
    Limitations
    This synthetic fixture establishes no norm, physical, validation, UQ, portability,
    or cross-language claim.
    """
    return OperatorRecordDifferenceResult(
        OperatorRecordCompatibilityResult("reference", "candidate", ()), matrix, "eV"
    )


def execute_zero_without_runtime_warning(
    matrix: npt.NDArray[np.complex128],
) -> OperatorRecordComparisonResult:
    r"""Evidence ID
    Owns no identifier; supports ``NV-ORA-017``.
    Requirement
    Exact-zero residual execution must not leak a NumPy RuntimeWarning.
    Method
    Promote RuntimeWarning to error and invoke the public analyzer on the supplied
    compatible difference.
    Oracle
    Python warning-filter semantics independently require any emitted RuntimeWarning to
    fail the owning test.
    Acceptance
    Public execution returns normally and yields an OperatorRecordComparisonResult.
    Interpretation
    Failure identifies warning leakage, analyzer failure, or fixture error.
    Limitations
    The helper does not validate NumPy or establish behavior for nonzero matrices.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        return OperatorRecordResidualAnalyzer().execute(make_zero_difference(matrix))


def test_method__execute__exact_scalar_zero_path() -> None:
    r"""Evidence ID
    NV-ORA-017
    Requirement
    The maximum-entry, Frobenius, and spectral norms of an exact ``1 x 1`` zero
    complex128 represented difference are exactly zero eV.
    Method
    Execute the public analyzer on ``array([[0+0j]], dtype=complex128)`` while treating
    RuntimeWarning as an error, then inspect all three public metrics.
    Oracle
    By the definitions of maximum absolute entry, Frobenius norm, and induced spectral
    norm, every norm of the zero matrix is exactly zero without numerical approximation.
    Acceptance
    All three metrics equal ``0.0`` exactly and satisfy
    ``0 <= maximum <= spectral <= Frobenius``; no tolerance is used.
    Interpretation
    A pass verifies the exact zero-scale branch for this representation; failure
    identifies analyzer, warning-policy, fixture, or accepted-mathematics drift.
    Limitations
    This case establishes no nonzero forward-error bound, arbitrary-shape behavior,
    physical correctness, scientific validation, UQ, portability, or cross-language
    agreement.
    """
    matrix: npt.NDArray[np.complex128] = np.array([[0.0 + 0.0j]], dtype=np.complex128)

    result = execute_zero_without_runtime_warning(matrix)

    assert result.maximum_absolute_residual == 0.0
    assert result.spectral_residual == 0.0
    assert result.frobenius_residual == 0.0
    assert (
        0.0
        <= result.maximum_absolute_residual
        <= result.spectral_residual
        <= result.frobenius_residual
    )
