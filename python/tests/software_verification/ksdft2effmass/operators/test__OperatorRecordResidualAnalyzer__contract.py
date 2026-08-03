"""Software-verification evidence for the residual-analyzer public contract.

System under test
-----------------
``OperatorRecordResidualAnalyzer`` is the ActionObject that accepts an
``OperatorRecordDifferenceResult`` and returns an
``OperatorRecordComparisonResult`` or a structured public numerical error.

Evidence class and requirements
-------------------------------
This module is software verification. It checks public input-type enforcement,
successful ResultObject creation and metadata propagation, and translation of
residual-analysis failures into the documented public error-code taxonomy. It
does not verify numerical norm accuracy; analytical and floating-point evidence
belongs to the numerical-verification modules.

Strategy, oracles, and acceptance
---------------------------------
Tests invoke only the public ``execute()`` method. Public return types, retained
metadata, and exact enum members are the contract oracles. Controlled
replacement of ``numpy.linalg.svd`` exercises otherwise unreliable-to-reach
backend-failure, nonfinite-output, and material-order-violation translation
branches. These injections verify the ActionObject's translation behavior, not
NumPy's SVD implementation. The finite-input overflow case treats raw NumPy
``RuntimeWarning`` as an error so only the structured public failure can cross
the ActionObject boundary.

Exclusions and interpretation
-----------------------------
Private analyzer methods, SVD accuracy, physical adequacy of a Hamiltonian
comparison, scientific validation, and uncertainty quantification are excluded.
A passing module means the tested public software contract and error boundary
behave as documented. A failure indicates a software-contract, ownership, or
error-translation regression; it is not evidence about physical model validity.
Scientific validation and uncertainty quantification have not been performed.
"""

import warnings
from typing import Any, cast

import numpy as np
import numpy.typing as npt
import pytest

from ksdft2effmass.operators import (
    OperatorRecordComparisonNumericalError,
    OperatorRecordComparisonNumericalErrorCode,
    OperatorRecordComparisonResult,
    OperatorRecordCompatibilityResult,
    OperatorRecordDifferenceResult,
    OperatorRecordResidualAnalyzer,
)

pytestmark = pytest.mark.software_verification


def difference(matrix: npt.NDArray[np.complex128]) -> OperatorRecordDifferenceResult:
    """Construct synthetic software-verification represented-difference data.

    Parameters
    ----------
    matrix
        Exact ``numpy.ndarray`` with ``complex128`` dtype prepared by the caller.
        This helper performs no dtype, subclass, shape, or storage coercion.

    Returns
    -------
    OperatorRecordDifferenceResult
        A synthetic result with canonical identifiers ``"reference"`` and
        ``"candidate"`` and deterministic ``"eV"`` metadata.

    Notes
    -----
    The ``eV`` unit is metadata only. The object does not represent a
    scientifically validated physical operator difference.
    """

    return OperatorRecordDifferenceResult(
        OperatorRecordCompatibilityResult("reference", "candidate", ()),
        matrix,
        "eV",
    )


def test_residual_analyzer_rejects_non_difference_input() -> None:
    """SV-ORA-001: reject an input outside the public difference-result type.

    Requirement
        ``execute()`` accepts only ``OperatorRecordDifferenceResult``.
    Method and oracle
        Supply a plain object and require the documented public ``TypeError``.
    Acceptance and interpretation
        The exact public type name appears in the error. Passing establishes the
        ActionObject input boundary, not any numerical behavior.
    Limitations
        Other valid difference-result invariants are owned by that ResultObject.
    """

    with pytest.raises(TypeError, match="OperatorRecordDifferenceResult"):
        OperatorRecordResidualAnalyzer().execute(cast(Any, object()))


def test_residual_analyzer_creates_result_and_propagates_metadata() -> None:
    """SV-ORA-002: preserve public result type and difference metadata.

    Requirement
        Successful analysis returns ``OperatorRecordComparisonResult`` with the
        source identifiers, matrix dimension, and energy unit unchanged.
    Method and oracle
        Analyze a synthetic finite diagonal ``2 x 2`` ``complex128`` matrix and
        compare public metadata fields exactly with the prepared input.
    Acceptance and interpretation
        Exact type and field equality demonstrate construction and propagation;
        metric accuracy is intentionally not used as an oracle here.
    Limitations
        The synthetic matrix has no asserted physical meaning.
    """

    matrix: npt.NDArray[np.complex128] = np.array(
        [[1.0 + 0.0j, 0.0 + 0.0j], [0.0 + 0.0j, 2.0 + 0.0j]],
        dtype=np.complex128,
    )

    result = OperatorRecordResidualAnalyzer().execute(difference(matrix))

    assert isinstance(result, OperatorRecordComparisonResult)
    assert result.reference_identifier == "reference"
    assert result.candidate_identifier == "candidate"
    assert result.matrix_dimension == 2
    assert result.energy_unit == "eV"


def test_residual_analyzer_translates_svd_backend_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """SV-ORA-003: translate an SVD exception to linear-algebra failure.

    Requirement
        An SVD backend exception maps to ``LINEAR_ALGEBRA_FAILURE``.
    Method
        Replace ``numpy.linalg.svd`` with a deterministic callable raising
        ``numpy.linalg.LinAlgError``; valid public input cannot reliably induce
        this dependency failure.
    Oracle and acceptance
        ``execute()`` raises ``OperatorRecordComparisonNumericalError`` whose
        code is exactly ``LINEAR_ALGEBRA_FAILURE``.
    Interpretation and limitations
        Passing verifies public error translation only. It does not test NumPy's
        SVD implementation, availability, or numerical accuracy.
    """

    def fail_svd(*_args: object, **_kwargs: object) -> npt.NDArray[np.float64]:
        """Inject a deterministic ``numpy.linalg.LinAlgError`` from SVD."""

        raise np.linalg.LinAlgError("synthetic SVD failure")

    monkeypatch.setattr(np.linalg, "svd", fail_svd)
    matrix: npt.NDArray[np.complex128] = np.array([[1.0 + 0.0j]], dtype=np.complex128)

    with pytest.raises(OperatorRecordComparisonNumericalError) as exc_info:
        OperatorRecordResidualAnalyzer().execute(difference(matrix))

    assert (
        exc_info.value.code
        is OperatorRecordComparisonNumericalErrorCode.LINEAR_ALGEBRA_FAILURE
    )


def test_residual_analyzer_translates_nonfinite_svd_result(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """SV-ORA-004: translate nonfinite SVD output to linear-algebra failure.

    Requirement
        A completed SVD that returns a nonfinite singular value maps to
        ``LINEAR_ALGEBRA_FAILURE``.
    Method
        Replace ``numpy.linalg.svd`` with a deterministic ``nan`` result because
        valid finite public input cannot reliably force this backend behavior.
    Oracle and acceptance
        The public structured exception carries exactly the required enum code.
    Interpretation and limitations
        Passing verifies dependency-output translation, not SVD correctness.
    """

    def nonfinite_svd(*_args: object, **_kwargs: object) -> npt.NDArray[np.float64]:
        """Inject a completed SVD call with a nonfinite singular value."""

        return np.array([np.nan], dtype=np.float64)

    monkeypatch.setattr(np.linalg, "svd", nonfinite_svd)
    matrix: npt.NDArray[np.complex128] = np.array([[1.0 + 0.0j]], dtype=np.complex128)

    with pytest.raises(OperatorRecordComparisonNumericalError) as exc_info:
        OperatorRecordResidualAnalyzer().execute(difference(matrix))

    assert (
        exc_info.value.code
        is OperatorRecordComparisonNumericalErrorCode.LINEAR_ALGEBRA_FAILURE
    )


def test_residual_analyzer_reports_structured_metric_order_violation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """SV-ORA-005: report a material public metric-order violation.

    Requirement
        A norm-order defect beyond analyzer-owned roundoff allowance maps to
        ``METRIC_ORDER_VIOLATION``.
    Method
        Replace ``numpy.linalg.svd`` with zero for a nonzero ``1 x 1`` matrix,
        creating a deterministic material violation that valid backend behavior
        cannot reliably produce.
    Oracle and acceptance
        The public structured exception carries exactly the required enum code.
    Interpretation and limitations
        Passing verifies public translation and does not validate the private
        allowance calculation or NumPy's SVD implementation.
    """

    def zero_svd(*_args: object, **_kwargs: object) -> npt.NDArray[np.float64]:
        """Inject an impossible zero spectral norm for a nonzero matrix."""

        return np.array([0.0], dtype=np.float64)

    monkeypatch.setattr(np.linalg, "svd", zero_svd)
    matrix: npt.NDArray[np.complex128] = np.array([[1.0 + 0.0j]], dtype=np.complex128)

    with pytest.raises(OperatorRecordComparisonNumericalError) as exc_info:
        OperatorRecordResidualAnalyzer().execute(difference(matrix))

    assert (
        exc_info.value.code
        is OperatorRecordComparisonNumericalErrorCode.METRIC_ORDER_VIOLATION
    )


def test_residual_analyzer_reports_nonrepresentable_finite_input_norm() -> None:
    """SV-ORA-006: contain warning and report nonrepresentable finite metric.

    Requirement
        Finite entries whose true Frobenius norm exceeds binary64 range produce
        ``NONFINITE_METRIC`` without leaking a raw NumPy ``RuntimeWarning``.
    Method
        Analyze a diagonal ``2 x 2`` ``complex128`` matrix with both diagonal
        entries equal to the largest finite binary64 value while promoting every
        ``RuntimeWarning`` to an exception at the public boundary.
    Oracle and acceptance
        Only ``OperatorRecordComparisonNumericalError`` is observed and its code
        is exactly ``NONFINITE_METRIC``.
    Interpretation and limitations
        Passing verifies structured failure containment, not representability in
        other floating-point formats or physical validity of the synthetic data.
    """

    largest = np.finfo(np.float64).max
    # Two largest finite entries have a finite representation, but their true
    # Frobenius norm is larger than the maximum representable binary64 scalar.
    matrix: npt.NDArray[np.complex128] = np.array(
        [[largest + 0.0j, 0.0 + 0.0j], [0.0 + 0.0j, largest + 0.0j]],
        dtype=np.complex128,
    )

    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        with pytest.raises(OperatorRecordComparisonNumericalError) as exc_info:
            OperatorRecordResidualAnalyzer().execute(difference(matrix))

    assert (
        exc_info.value.code
        is OperatorRecordComparisonNumericalErrorCode.NONFINITE_METRIC
    )
