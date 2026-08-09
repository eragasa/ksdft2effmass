r"""Software verification of ``OperatorRecordResidualAnalyzer``.

Facet and represented meaning

-----------------------------
This class-owned module owns finite binary64 regression behavior at normal and
subnormal scales. Historical ``NV-ORA-007`` through ``NV-ORA-016`` identifiers remain
recorded as predecessors. Their software-verification successors are ``SV-ORA-007``
through ``SV-ORA-016`` because threshold-only claims cannot retain a
numerical-verification classification.

Intrinsic and cross-object scope

--------------------------------
The SUT is ``OperatorRecordResidualAnalyzer``. Synthetic ``complex128`` represented
differences exercise scalar magnitude, Frobenius, and spectral paths in eV. Independent
expected values remain exact or hand-derived, but the 64-epsilon and eight-ULP rules are
bounded regression envelopes, not proven forward-error bounds for NumPy, LAPACK, or an
arbitrary SVD backend.

VVUQ and scientific exclusions

------------------------------
Passing establishes only that the listed supported environment and shapes remain inside
the unchanged regression envelopes without leaked RuntimeWarning and preserve the
public metric ordering. It does not claim numerical verification for those approximate
thresholds, prove backend-independent error bounds, establish physical correctness,
scientific validation, UQ, portability, or cross-language agreement.
"""

import math
import warnings
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
import pytest

from ksdft2effmass.operators import (
    OperatorRecordComparisonResult,
    OperatorRecordCompatibilityResult,
    OperatorRecordDifferenceResult,
    OperatorRecordResidualAnalyzer,
)

pytestmark = pytest.mark.software_verification

SUT = OperatorRecordResidualAnalyzer

BINARY64_RELATIVE_TOLERANCE = 64.0 * np.finfo(np.float64).eps
SUBNORMAL_ACCEPTANCE_MAX_ULP = 8


@dataclass(frozen=True, slots=True)
class ScalarCase:
    r"""Stable evidence metadata for a synthetic scalar difference.

    Parameters
    ----------
    evidence_id
    Stable ``NV-ORA-###`` identifier retained across file reorganization.
    name
    Readable pytest parameter label.
    entry
    Scalar whose stored binary64 components define the exact ``1 x 1``
    ``complex128`` test matrix.

    Notes
    -----
    Cases are synthetic, use deterministic ``eV`` metadata, and carry no
    scientific interpretation.
    """

    evidence_id: str
    name: str
    entry: complex


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

    Limitations: Approximate nonzero cases are bounded binary64 regression checks for
    the listed
    shapes and environment, not numerical-verification proofs for arbitrary matrices or
    backends; they establish no physical correctness, scientific validation, UQ,
    portability, or cross-language agreement.
    """

    return OperatorRecordDifferenceResult(
        OperatorRecordCompatibilityResult("reference", "candidate", ()),
        matrix,
        "eV",
    )


def execute_without_runtime_warning(
    matrix: npt.NDArray[np.complex128],
) -> OperatorRecordComparisonResult:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Residual execution for finite synthetic matrices must not leak a NumPy
    RuntimeWarning.

    Method: Construct or inspect only the named synthetic fixture operation (execute
    without
    runtime warning); the helper owns no assertion result and introduces no hidden
    oracle.

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

    Limitations: Approximate nonzero cases are bounded binary64 regression checks for
    the listed
    shapes and environment, not numerical-verification proofs for arbitrary matrices or
    backends; they establish no physical correctness, scientific validation, UQ,
    portability, or cross-language agreement.
    """

    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        return OperatorRecordResidualAnalyzer().execute(difference(matrix))


def assert_nonzero_normal_close(actual: float, expected: float) -> None:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: A nonzero normal binary64 result is compared with a nonzero
    independently calculated
    reference under the declared local regression envelope.

    Method: Construct or inspect only the named synthetic fixture operation (assert
    nonzero
    normal close); the helper owns no assertion result and introduces no hidden oracle.

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

    Limitations: Approximate nonzero cases are bounded binary64 regression checks for
    the listed
    shapes and environment, not numerical-verification proofs for arbitrary matrices or
    backends; they establish no physical correctness, scientific validation, UQ,
    portability, or cross-language agreement.
    """

    assert np.isfinite(expected)
    assert np.isfinite(actual)
    assert expected != 0.0
    assert actual != 0.0

    absolute_error = abs(actual - expected)
    allowed_error = BINARY64_RELATIVE_TOLERANCE * abs(expected)

    assert allowed_error > 0.0
    assert allowed_error < abs(expected)
    assert absolute_error <= allowed_error


def binary64_ulp_distance(actual: float, expected: float) -> int:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: The ULP regression check compares nonnegative binary64 bit patterns by
    their
    monotone unsigned encoding.

    Method: Construct or inspect only the named synthetic fixture operation (binary64
    ulp
    distance); the helper owns no assertion result and introduces no hidden oracle.

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

    Limitations: Approximate nonzero cases are bounded binary64 regression checks for
    the listed
    shapes and environment, not numerical-verification proofs for arbitrary matrices or
    backends; they establish no physical correctness, scientific validation, UQ,
    portability, or cross-language agreement.
    """

    actual_bits = int(np.asarray(actual, dtype=np.float64).view(np.uint64))
    expected_bits = int(np.asarray(expected, dtype=np.float64).view(np.uint64))
    return abs(actual_bits - expected_bits)


def assert_subnormal_ulp_close(actual: float, expected: float) -> int:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: A subnormal regression result must remain positive and within the
    declared inclusive
    ULP envelope of a positive subnormal reference.

    Method: Construct or inspect only the named synthetic fixture operation (assert
    subnormal
    ulp close); the helper owns no assertion result and introduces no hidden oracle.

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

    Limitations: Approximate nonzero cases are bounded binary64 regression checks for
    the listed
    shapes and environment, not numerical-verification proofs for arbitrary matrices or
    backends; they establish no physical correctness, scientific validation, UQ,
    portability, or cross-language agreement.
    """

    assert 0.0 < expected < np.finfo(np.float64).tiny
    assert actual > 0.0
    distance = binary64_ulp_distance(actual, expected)
    assert distance <= SUBNORMAL_ACCEPTANCE_MAX_ULP
    return distance


def assert_ordering(maximum: float, spectral: float, frobenius: float) -> None:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Stored residual metrics satisfy the public order zero <= maximum <=
    spectral <=
    Frobenius.

    Method: Construct or inspect only the named synthetic fixture operation (assert
    ordering);
    the helper owns no assertion result and introduces no hidden oracle.

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

    Limitations: Approximate nonzero cases are bounded binary64 regression checks for
    the listed
    shapes and environment, not numerical-verification proofs for arbitrary matrices or
    backends; they establish no physical correctness, scientific validation, UQ,
    portability, or cross-language agreement.
    """

    assert 0.0 <= maximum <= spectral <= frobenius


NORMAL_COMPLEX_CASES = (
    pytest.param(
        ScalarCase("SV-ORA-007", "complex-1-plus-i-e100", (1.0 + 1j) * 1e100),
        id="complex_1_plus_i_e100",
    ),
    pytest.param(
        ScalarCase("SV-ORA-008", "complex-1-plus-2i-e100", (1.0 + 2j) * 1e100),
        id="complex_1_plus_2i_e100",
    ),
)


@pytest.mark.parametrize("case", NORMAL_COMPLEX_CASES)
def test_method__execute__normal_complex_scalar_paths(case: ScalarCase) -> None:
    r"""Evidence ID: SV-ORA-007

    Requirement: OperatorRecordResidualAnalyzer enforces this public residual-analysis
    partition:
    execute: normal complex scalar paths.

    Method: Construct the declared complex128 represented difference for execute: normal
    complex
    scalar paths, invoke execute() with RuntimeWarning promoted to error where numerical
    operations occur, and inspect public outputs.

    Oracle: Exact scalar identities, hand-derived matrix norms where stated, Python
    exception
    semantics, and the public structured-error taxonomy determine the expected result
    independently of analyzer private helpers.

    Acceptance: Each scalar is finite and nonzero and its absolute error is at most
    64*epsilon*abs(expected), with a strictly positive bound smaller than the expected
    magnitude.

    Interpretation: A pass supports only the stated represented residual or
    error-boundary case; failure
    may identify analyzer, oracle, backend/environment, fixture, or accepted-contract
    drift.

    Limitations: Approximate nonzero cases are bounded binary64 regression checks for
    the listed
    shapes and environment, not numerical-verification proofs for arbitrary matrices or
    backends; they establish no physical correctness, scientific validation, UQ,
    portability, or cross-language agreement.
    """

    matrix: npt.NDArray[np.complex128] = np.array([[case.entry]], dtype=np.complex128)
    stored_entry = matrix[0, 0]
    expected = math.hypot(float(stored_entry.real), float(stored_entry.imag))

    result = execute_without_runtime_warning(matrix)

    assert_nonzero_normal_close(result.maximum_absolute_residual, expected)
    assert_nonzero_normal_close(result.spectral_residual, expected)
    assert_nonzero_normal_close(result.frobenius_residual, expected)
    assert result.maximum_absolute_residual == result.spectral_residual
    assert result.spectral_residual == result.frobenius_residual
    assert_ordering(
        result.maximum_absolute_residual,
        result.spectral_residual,
        result.frobenius_residual,
    )


def test_method__execute__small_normal_real_scalar_path() -> None:
    r"""Evidence ID: SV-ORA-009

    Requirement: OperatorRecordResidualAnalyzer enforces this public residual-analysis
    partition:
    execute: small normal real scalar path.

    Method: Construct the declared complex128 represented difference for execute: small
    normal
    real scalar path, invoke execute() with RuntimeWarning promoted to error where
    numerical operations occur, and inspect public outputs.

    Oracle: Exact scalar identities, hand-derived matrix norms where stated, Python
    exception
    semantics, and the public structured-error taxonomy determine the expected result
    independently of analyzer private helpers.

    Acceptance: Each scalar is finite and nonzero and its absolute error is at most
    64*epsilon*abs(expected), with a strictly positive bound smaller than the expected
    magnitude.

    Interpretation: A pass supports only the stated represented residual or
    error-boundary case; failure
    may identify analyzer, oracle, backend/environment, fixture, or accepted-contract
    drift.

    Limitations: Approximate nonzero cases are bounded binary64 regression checks for
    the listed
    shapes and environment, not numerical-verification proofs for arbitrary matrices or
    backends; they establish no physical correctness, scientific validation, UQ,
    portability, or cross-language agreement.
    """

    matrix: npt.NDArray[np.complex128] = np.array(
        [[1.0e-200 + 0.0j]], dtype=np.complex128
    )
    expected = abs(float(matrix[0, 0].real))

    result = execute_without_runtime_warning(matrix)

    assert_nonzero_normal_close(result.maximum_absolute_residual, expected)
    assert_nonzero_normal_close(result.spectral_residual, expected)
    assert_nonzero_normal_close(result.frobenius_residual, expected)
    assert_ordering(
        result.maximum_absolute_residual,
        result.spectral_residual,
        result.frobenius_residual,
    )


COMPLEX_SUBNORMAL_CASES = (
    pytest.param(
        ScalarCase(
            "SV-ORA-010", "complex-subnormal-1-plus-i-e-310", (1.0 + 1j) * 1e-310
        ),
        id="complex_subnormal_1_plus_i_e_310",
    ),
    pytest.param(
        ScalarCase(
            "SV-ORA-011", "complex-subnormal-1-plus-2i-e-310", (1.0 + 2j) * 1e-310
        ),
        id="complex_subnormal_1_plus_2i_e_310",
    ),
)


@pytest.mark.parametrize("case", COMPLEX_SUBNORMAL_CASES)
def test_method__execute__complex_subnormal_scalar_paths(
    case: ScalarCase,
) -> None:
    r"""Evidence ID: SV-ORA-010

    Requirement: OperatorRecordResidualAnalyzer enforces this public residual-analysis
    partition:
    execute: complex subnormal scalar paths.

    Method: Construct the declared complex128 represented difference for execute:
    complex
    subnormal scalar paths, invoke execute() with RuntimeWarning promoted to error where
    numerical operations occur, and inspect public outputs.

    Oracle: Exact scalar identities, hand-derived matrix norms where stated, Python
    exception
    semantics, and the public structured-error taxonomy determine the expected result
    independently of analyzer private helpers.

    Acceptance: Each expected and actual scalar is strictly positive, their unsigned
    binary64
    encodings differ by at most eight ULPs inclusively, and zero cannot satisfy
    acceptance.

    Interpretation: A pass supports only the stated represented residual or
    error-boundary case; failure
    may identify analyzer, oracle, backend/environment, fixture, or accepted-contract
    drift.

    Limitations: Approximate nonzero cases are bounded binary64 regression checks for
    the listed
    shapes and environment, not numerical-verification proofs for arbitrary matrices or
    backends; they establish no physical correctness, scientific validation, UQ,
    portability, or cross-language agreement.
    """

    matrix: npt.NDArray[np.complex128] = np.array([[case.entry]], dtype=np.complex128)
    stored_entry = matrix[0, 0]
    expected = math.hypot(float(stored_entry.real), float(stored_entry.imag))

    result = execute_without_runtime_warning(matrix)

    assert_subnormal_ulp_close(result.maximum_absolute_residual, expected)
    assert_subnormal_ulp_close(result.spectral_residual, expected)
    assert_subnormal_ulp_close(result.frobenius_residual, expected)
    assert_ordering(
        result.maximum_absolute_residual,
        result.spectral_residual,
        result.frobenius_residual,
    )


DEEP_SUBNORMAL_CASES = (
    pytest.param(
        ScalarCase("SV-ORA-012", "deep-real-subnormal-e-320", 1e-320 + 0j),
        id="deep_real_subnormal_e_320",
    ),
    pytest.param(
        ScalarCase(
            "SV-ORA-013", "deep-complex-subnormal-1-plus-i-e-320", (1.0 + 1j) * 1e-320
        ),
        id="deep_complex_subnormal_1_plus_i_e_320",
    ),
)


@pytest.mark.parametrize("case", DEEP_SUBNORMAL_CASES)
def test_method__execute__deep_subnormal_scalar_paths(case: ScalarCase) -> None:
    r"""Evidence ID: SV-ORA-012

    Requirement: OperatorRecordResidualAnalyzer enforces this public residual-analysis
    partition:
    execute: deep subnormal scalar paths.

    Method: Construct the declared complex128 represented difference for execute: deep
    subnormal
    scalar paths, invoke execute() with RuntimeWarning promoted to error where numerical
    operations occur, and inspect public outputs.

    Oracle: Exact scalar identities, hand-derived matrix norms where stated, Python
    exception
    semantics, and the public structured-error taxonomy determine the expected result
    independently of analyzer private helpers.

    Acceptance: Each expected and actual scalar is strictly positive, their unsigned
    binary64
    encodings differ by at most eight ULPs inclusively, and zero cannot satisfy
    acceptance.

    Interpretation: A pass supports only the stated represented residual or
    error-boundary case; failure
    may identify analyzer, oracle, backend/environment, fixture, or accepted-contract
    drift.

    Limitations: Approximate nonzero cases are bounded binary64 regression checks for
    the listed
    shapes and environment, not numerical-verification proofs for arbitrary matrices or
    backends; they establish no physical correctness, scientific validation, UQ,
    portability, or cross-language agreement.
    """

    matrix: npt.NDArray[np.complex128] = np.array([[case.entry]], dtype=np.complex128)
    stored_entry = matrix[0, 0]
    expected = math.hypot(float(stored_entry.real), float(stored_entry.imag))

    result = execute_without_runtime_warning(matrix)

    assert_subnormal_ulp_close(result.maximum_absolute_residual, expected)
    assert_subnormal_ulp_close(result.spectral_residual, expected)
    assert_subnormal_ulp_close(result.frobenius_residual, expected)
    assert_ordering(
        result.maximum_absolute_residual,
        result.spectral_residual,
        result.frobenius_residual,
    )


def test_method__execute__smallest_positive_binary64_subnormal_path() -> None:
    r"""Evidence ID: SV-ORA-014

    Requirement: OperatorRecordResidualAnalyzer enforces this public residual-analysis
    partition:
    execute: smallest positive binary64 subnormal path.

    Method: Construct the declared complex128 represented difference for execute:
    smallest
    positive binary64 subnormal path, invoke execute() with RuntimeWarning promoted to
    error where numerical operations occur, and inspect public outputs.

    Oracle: Exact scalar identities, hand-derived matrix norms where stated, Python
    exception
    semantics, and the public structured-error taxonomy determine the expected result
    independently of analyzer private helpers.

    Acceptance: Each expected and actual scalar is strictly positive, their unsigned
    binary64
    encodings differ by at most eight ULPs inclusively, and zero cannot satisfy
    acceptance.

    Interpretation: A pass supports only the stated represented residual or
    error-boundary case; failure
    may identify analyzer, oracle, backend/environment, fixture, or accepted-contract
    drift.

    Limitations: Approximate nonzero cases are bounded binary64 regression checks for
    the listed
    shapes and environment, not numerical-verification proofs for arbitrary matrices or
    backends; they establish no physical correctness, scientific validation, UQ,
    portability, or cross-language agreement.
    """

    smallest_subnormal = np.nextafter(np.float64(0.0), np.float64(1.0))
    matrix: npt.NDArray[np.complex128] = np.array(
        [[complex(float(smallest_subnormal), 0.0)]], dtype=np.complex128
    )
    expected = float(smallest_subnormal)

    result = execute_without_runtime_warning(matrix)

    assert_subnormal_ulp_close(result.maximum_absolute_residual, expected)
    assert_subnormal_ulp_close(result.spectral_residual, expected)
    assert_subnormal_ulp_close(result.frobenius_residual, expected)
    assert_ordering(
        result.maximum_absolute_residual,
        result.spectral_residual,
        result.frobenius_residual,
    )


def test_field__two_dimensional_subnormal_ordering_regression__is_exact() -> None:
    r"""Evidence ID: SV-ORA-015

    Requirement: OperatorRecordResidualAnalyzer enforces this public residual-analysis
    partition: two
    dimensional subnormal ordering regression: is exact.

    Method: Construct the declared complex128 represented difference for two dimensional
    subnormal ordering regression: is exact, invoke execute() with RuntimeWarning
    promoted to error where numerical operations occur, and inspect public outputs.

    Oracle: Exact scalar identities, hand-derived matrix norms where stated, Python
    exception
    semantics, and the public structured-error taxonomy determine the expected result
    independently of analyzer private helpers.

    Acceptance: Each expected and actual scalar is strictly positive, their unsigned
    binary64
    encodings differ by at most eight ULPs inclusively, and zero cannot satisfy
    acceptance.

    Interpretation: A pass supports only the stated represented residual or
    error-boundary case; failure
    may identify analyzer, oracle, backend/environment, fixture, or accepted-contract
    drift.

    Limitations: Approximate nonzero cases are bounded binary64 regression checks for
    the listed
    shapes and environment, not numerical-verification proofs for arbitrary matrices or
    backends; they establish no physical correctness, scientific validation, UQ,
    portability, or cross-language agreement.
    """

    scale = np.float64(1.0e-310)
    matrix: npt.NDArray[np.complex128] = np.array(
        [
            [2.0 * scale + 2.0j * scale, 2.0 * scale - 2.0j * scale],
            [scale + 0.0j, 0.0 - 1.0j * scale],
        ],
        dtype=np.complex128,
    )
    expected_maximum = 2.0 * math.sqrt(2.0) * float(scale)
    expected_frobenius = 3.0 * math.sqrt(2.0) * float(scale)
    expected_spectral = 3.0 * math.sqrt(2.0) * float(scale)

    result = execute_without_runtime_warning(matrix)

    assert_subnormal_ulp_close(result.maximum_absolute_residual, expected_maximum)
    assert_subnormal_ulp_close(result.spectral_residual, expected_spectral)
    assert_subnormal_ulp_close(result.frobenius_residual, expected_frobenius)
    assert result.spectral_residual == result.frobenius_residual
    assert_ordering(
        result.maximum_absolute_residual,
        result.spectral_residual,
        result.frobenius_residual,
    )


def test_method__execute__largest_finite_binary64_scalar_path() -> None:
    r"""Evidence ID: SV-ORA-016

    Requirement: OperatorRecordResidualAnalyzer enforces this public residual-analysis
    partition:
    execute: largest finite binary64 scalar path.

    Method: Construct the declared complex128 represented difference for execute:
    largest finite
    binary64 scalar path, invoke execute() with RuntimeWarning promoted to error where
    numerical operations occur, and inspect public outputs.

    Oracle: Exact scalar identities, hand-derived matrix norms where stated, Python
    exception
    semantics, and the public structured-error taxonomy determine the expected result
    independently of analyzer private helpers.

    Acceptance: Each scalar is finite and nonzero and its absolute error is at most
    64*epsilon*abs(expected), with a strictly positive bound smaller than the expected
    magnitude.

    Interpretation: A pass supports only the stated represented residual or
    error-boundary case; failure
    may identify analyzer, oracle, backend/environment, fixture, or accepted-contract
    drift.

    Limitations: Approximate nonzero cases are bounded binary64 regression checks for
    the listed
    shapes and environment, not numerical-verification proofs for arbitrary matrices or
    backends; they establish no physical correctness, scientific validation, UQ,
    portability, or cross-language agreement.
    """

    largest = np.finfo(np.float64).max
    matrix: npt.NDArray[np.complex128] = np.array(
        [[largest + 0.0j]], dtype=np.complex128
    )
    expected = float(largest)

    result = execute_without_runtime_warning(matrix)

    assert_nonzero_normal_close(result.maximum_absolute_residual, expected)
    assert_nonzero_normal_close(result.spectral_residual, expected)
    assert_nonzero_normal_close(result.frobenius_residual, expected)
    assert_ordering(
        result.maximum_absolute_residual,
        result.spectral_residual,
        result.frobenius_residual,
    )
