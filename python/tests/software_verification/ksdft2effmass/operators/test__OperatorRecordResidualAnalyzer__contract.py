r"""Software verification of ``OperatorRecordResidualAnalyzer``.

Facet and represented meaning

-----------------------------
This class-owned module owns the contract facet. System under test
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

Intrinsic and cross-object scope

--------------------------------
The primary owner is ``OperatorRecordResidualAnalyzer``; collaborators only
construct inputs or expose public outcomes. Accepted public contracts, literal
expected values, Python language semantics, and assigned schema or fixture artifacts
provide the oracles. No runtime warning is accepted unless a test explicitly states
otherwise.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the documented software contract and exact or explicitly
bounded acceptance rules. Failure may identify implementation, fixture, oracle,
environment, or contract defects. It does not establish numerical verification,
physical correctness, scientific validation, UQ, portability, or cross-language
agreement.
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

SUT = OperatorRecordResidualAnalyzer


def difference(matrix: npt.NDArray[np.complex128]) -> OperatorRecordDifferenceResult:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Residual analysis accepts a compatible represented difference with the
    supplied
    complex128 matrix and explicit eV unit.

    Method: Construct or inspect only the named synthetic fixture operation
    (difference); the
    helper owns no assertion result and introduces no hidden oracle.

    Oracle: Exact scalar identities, hand-derived matrix norms where stated, Python
    exception
    semantics, and the public structured-error taxonomy determine the expected result
    independently of analyzer private helpers.

    Acceptance: The helper returns exactly the requested fixture value or applies only
    the
    documented comparison; all pass/fail assertions remain in the owning test.

    Interpretation: A pass supports only the stated represented residual or
    error-boundary case; failure
    may identify analyzer, oracle, backend/environment, fixture, or accepted-contract
    drift.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """

    return OperatorRecordDifferenceResult(
        OperatorRecordCompatibilityResult("reference", "candidate", ()),
        matrix,
        "eV",
    )


def test_method__execute__residual_analyzer_rejects_non_difference_input() -> None:
    r"""Evidence ID: SV-ORA-001

    Requirement: OperatorRecordResidualAnalyzer enforces this public residual-analysis
    partition:
    execute: residual analyzer rejects non difference input.

    Method: Construct the declared complex128 represented difference for execute:
    residual
    analyzer rejects non difference input, invoke execute() with RuntimeWarning promoted
    to error where numerical operations occur, and inspect public outputs.

    Oracle: Exact scalar identities, hand-derived matrix norms where stated, Python
    exception
    semantics, and the public structured-error taxonomy determine the expected result
    independently of analyzer private helpers.

    Acceptance: The named partition raises exactly TypeError with the asserted public
    message, code,
    or attached result; no alternate exception is accepted.

    Interpretation: A pass supports only the stated represented residual or
    error-boundary case; failure
    may identify analyzer, oracle, backend/environment, fixture, or accepted-contract
    drift.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """

    with pytest.raises(TypeError, match="OperatorRecordDifferenceResult"):
        OperatorRecordResidualAnalyzer().execute(cast(Any, object()))


def test_method__execute__creates_result_with_metadata() -> None:
    r"""Evidence ID: SV-ORA-002

    Requirement: OperatorRecordResidualAnalyzer enforces this public residual-analysis
    partition:
    execute: creates result with metadata.

    Method: Construct the declared complex128 represented difference for execute:
    creates result
    with metadata, invoke execute() with RuntimeWarning promoted to error where
    numerical operations occur, and inspect public outputs.

    Oracle: Exact scalar identities, hand-derived matrix norms where stated, Python
    exception
    semantics, and the public structured-error taxonomy determine the expected result
    independently of analyzer private helpers.

    Acceptance: All literal values, arrays, field names, ordering relations, object
    identities,
    absences, and deterministic text asserted by the case match exactly; no approximate
    fallback is used.

    Interpretation: A pass supports only the stated represented residual or
    error-boundary case; failure
    may identify analyzer, oracle, backend/environment, fixture, or accepted-contract
    drift.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
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


def test_method__execute__residual_analyzer_translates_svd_backend_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    r"""Evidence ID: SV-ORA-003

    Requirement: OperatorRecordResidualAnalyzer enforces this public residual-analysis
    partition:
    execute: residual analyzer translates svd backend failure.

    Method: Construct the declared complex128 represented difference for execute:
    residual
    analyzer translates svd backend failure, invoke execute() with RuntimeWarning
    promoted to error where numerical operations occur, and inspect public outputs.

    Oracle: Exact scalar identities, hand-derived matrix norms where stated, Python
    exception
    semantics, and the public structured-error taxonomy determine the expected result
    independently of analyzer private helpers.

    Acceptance: The named partition raises exactly
    OperatorRecordComparisonNumericalError with the
    asserted public message, code, or attached result; no alternate exception is
    accepted.

    Interpretation: A pass supports only the stated represented residual or
    error-boundary case; failure
    may identify analyzer, oracle, backend/environment, fixture, or accepted-contract
    drift.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """

    def fail_svd(*_args: object, **_kwargs: object) -> npt.NDArray[np.float64]:
        r"""Inject a deterministic ``numpy.linalg.LinAlgError`` from SVD."""

        raise np.linalg.LinAlgError("synthetic SVD failure")

    monkeypatch.setattr(np.linalg, "svd", fail_svd)
    matrix: npt.NDArray[np.complex128] = np.array([[1.0 + 0.0j]], dtype=np.complex128)

    with pytest.raises(OperatorRecordComparisonNumericalError) as exc_info:
        OperatorRecordResidualAnalyzer().execute(difference(matrix))

    assert (
        exc_info.value.code
        is OperatorRecordComparisonNumericalErrorCode.LINEAR_ALGEBRA_FAILURE
    )


def test_method__execute__residual_analyzer_translates_nonfinite_svd_result(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    r"""Evidence ID: SV-ORA-004

    Requirement: OperatorRecordResidualAnalyzer enforces this public residual-analysis
    partition:
    execute: residual analyzer translates nonfinite svd result.

    Method: Construct the declared complex128 represented difference for execute:
    residual
    analyzer translates nonfinite svd result, invoke execute() with RuntimeWarning
    promoted to error where numerical operations occur, and inspect public outputs.

    Oracle: Exact scalar identities, hand-derived matrix norms where stated, Python
    exception
    semantics, and the public structured-error taxonomy determine the expected result
    independently of analyzer private helpers.

    Acceptance: The named partition raises exactly
    OperatorRecordComparisonNumericalError with the
    asserted public message, code, or attached result; no alternate exception is
    accepted.

    Interpretation: A pass supports only the stated represented residual or
    error-boundary case; failure
    may identify analyzer, oracle, backend/environment, fixture, or accepted-contract
    drift.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """

    def nonfinite_svd(*_args: object, **_kwargs: object) -> npt.NDArray[np.float64]:
        r"""Inject a completed SVD call with a nonfinite singular value."""

        return np.array([np.nan], dtype=np.float64)

    monkeypatch.setattr(np.linalg, "svd", nonfinite_svd)
    matrix: npt.NDArray[np.complex128] = np.array([[1.0 + 0.0j]], dtype=np.complex128)

    with pytest.raises(OperatorRecordComparisonNumericalError) as exc_info:
        OperatorRecordResidualAnalyzer().execute(difference(matrix))

    assert (
        exc_info.value.code
        is OperatorRecordComparisonNumericalErrorCode.LINEAR_ALGEBRA_FAILURE
    )


def test_method__execute__residual_analyzer_reports_structured_metric_order(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    r"""Evidence ID: SV-ORA-005

    Requirement: OperatorRecordResidualAnalyzer enforces this public residual-analysis
    partition:
    execute: residual analyzer reports structured metric order.

    Method: Construct the declared complex128 represented difference for execute:
    residual
    analyzer reports structured metric order, invoke execute() with RuntimeWarning
    promoted to error where numerical operations occur, and inspect public outputs.

    Oracle: Exact scalar identities, hand-derived matrix norms where stated, Python
    exception
    semantics, and the public structured-error taxonomy determine the expected result
    independently of analyzer private helpers.

    Acceptance: The named partition raises exactly
    OperatorRecordComparisonNumericalError with the
    asserted public message, code, or attached result; no alternate exception is
    accepted.

    Interpretation: A pass supports only the stated represented residual or
    error-boundary case; failure
    may identify analyzer, oracle, backend/environment, fixture, or accepted-contract
    drift.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """

    def zero_svd(*_args: object, **_kwargs: object) -> npt.NDArray[np.float64]:
        r"""Inject an impossible zero spectral norm for a nonzero matrix."""

        return np.array([0.0], dtype=np.float64)

    monkeypatch.setattr(np.linalg, "svd", zero_svd)
    matrix: npt.NDArray[np.complex128] = np.array([[1.0 + 0.0j]], dtype=np.complex128)

    with pytest.raises(OperatorRecordComparisonNumericalError) as exc_info:
        OperatorRecordResidualAnalyzer().execute(difference(matrix))

    assert (
        exc_info.value.code
        is OperatorRecordComparisonNumericalErrorCode.METRIC_ORDER_VIOLATION
    )


def test_field__represented_state__residual_analyzer_reports_nonrepresentable() -> None:
    r"""Evidence ID: SV-ORA-006

    Requirement: OperatorRecordResidualAnalyzer enforces this public residual-analysis
    partition:
    represented state: residual analyzer reports nonrepresentable.

    Method: Construct the declared complex128 represented difference for represented
    state:
    residual analyzer reports nonrepresentable, invoke execute() with RuntimeWarning
    promoted to error where numerical operations occur, and inspect public outputs.

    Oracle: Exact scalar identities, hand-derived matrix norms where stated, Python
    exception
    semantics, and the public structured-error taxonomy determine the expected result
    independently of analyzer private helpers.

    Acceptance: The named partition raises exactly
    OperatorRecordComparisonNumericalError with the
    asserted public message, code, or attached result; no alternate exception is
    accepted.

    Interpretation: A pass supports only the stated represented residual or
    error-boundary case; failure
    may identify analyzer, oracle, backend/environment, fixture, or accepted-contract
    drift.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
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
