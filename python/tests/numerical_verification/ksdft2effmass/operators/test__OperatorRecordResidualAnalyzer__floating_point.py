r"""Numerical verification of residual-analysis floating-point behavior.

Evidence class and mathematical quantities
-------------------------------------------
This module provides numerical-verification evidence ``NV-ORA-007`` through
``NV-ORA-017`` for ``OperatorRecordResidualAnalyzer``. For a finite represented
difference :math:`\Delta H`, the analyzer computes
:math:`\varepsilon_{\max}`, :math:`\varepsilon_{\mathrm F}`, and
:math:`\varepsilon_2`, with exact stored ordering
``0 <= maximum <= spectral <= Frobenius``.

Floating-point model and platform assumptions
---------------------------------------------
Inputs are exact ``numpy.ndarray`` objects with ``numpy.complex128`` entries;
public metrics are binary64 floats. The verified environment is the
repository-supported Python 3.14 and NumPy environment. Subnormal evidence
assumes IEEE-754 binary64 gradual underflow. An environment that flushes
subnormal values to zero does not satisfy this verified numerical contract.
Inputs are finite. True nonrepresentable output is not repeated here: structured
translation for finite entries whose Frobenius norm exceeds binary64 range is
software-verification evidence ``SV-ORA-006``.

Reference oracles and scale regimes
-----------------------------------
Complex scalar expected magnitudes use ``math.hypot()`` on the actual stored
binary64 real and imaginary components. This is an independent scalar binary64
oracle, not the production residual analyzer, NumPy SVD, or NumPy norm. Purely
real scalar cases use the exact stored absolute value. ``NV-ORA-015`` uses an
independent analytical derivation for its ``2 x 2`` coefficient matrix.

The cases cover normal complex values near ``1e100``, a small normal value near
``1e-200``, complex subnormals near ``1e-310``, deep subnormals near ``1e-320``,
the smallest positive binary64 subnormal, a two-dimensional subnormal ordering
regression, the largest finite binary64 scalar, and exact zero. Evidence
identifiers are stable traceability identifiers, not generated test counters.

Acceptance, warnings, and canonicalization
------------------------------------------
Nonzero normal values require an explicit
``64 * epsilon_machine * abs(expected)`` binary64 error bound, with nonzero
actual output and zero absolute tolerance. This local regression criterion is
not applicable to subnormals and is not a scientific tolerance. Subnormal
values require positive actual and expected values and at most eight ULPs, where
one ULP is the spacing between adjacent representable binary64 values in the
relevant subnormal region. Relative tolerance is unsuitable there because its
allowed error can underflow to zero. Eight ULPs is a conservative regression
bound for the scalar-magnitude, scaled-Frobenius, and scaled-spectral paths
exercised here; it is not a formal bound for arbitrary matrices, conditioning,
or SVD backends and is not a physical tolerance.

Every public execution promotes ``RuntimeWarning`` to an exception. Small
metric-order discrepancies may be canonically adjusted upward by the public
analyzer; ``NV-ORA-015`` expects spectral and Frobenius metrics to be stored
equal after that policy. Exact zero remains exact and publicly exercises the
zero-scale path without calling private implementation.

Boundaries and interpretation
-----------------------------
Passing establishes representable floating-point behavior for these cases,
absence of leaked NumPy runtime warnings, and the documented stored ordering. A
failure may indicate an analyzer regression, unsupported platform or backend
behavior, or an evidence/oracle defect requiring investigation; it does not by
itself establish physical-model error or scientific invalidity. Passing does
not validate NumPy or BLAS independently, establish arbitrary-dimension
forward-error bounds, determine physical residual acceptability, align bases or
gauges, validate DFT or Wannier calculations, validate a scientific model, or
quantify uncertainty. Scientific validation and uncertainty quantification have
not been performed.
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

pytestmark = pytest.mark.numerical_verification

BINARY64_RELATIVE_TOLERANCE = 64.0 * np.finfo(np.float64).eps
SUBNORMAL_ACCEPTANCE_MAX_ULP = 8


@dataclass(frozen=True, slots=True)
class ScalarCase:
    """Stable evidence metadata for a synthetic scalar difference.

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
    """Construct a synthetic compatible represented difference.

    The compatibility audit is synthetic and compatible by construction; ``eV``
    is deterministic metadata only. The helper performs no dtype, subclass,
    rank, shape, or storage coercion. The matrix is not derived from DFT,
    Wannierization, an impurity calculation, or experiment, and the helper
    establishes no scientific validity.
    """

    return OperatorRecordDifferenceResult(
        OperatorRecordCompatibilityResult("reference", "candidate", ()),
        matrix,
        "eV",
    )


def execute_without_runtime_warning(
    matrix: npt.NDArray[np.complex128],
) -> OperatorRecordComparisonResult:
    """Execute publicly while promoting every NumPy runtime warning to error.

    A returned result establishes that no raw ``RuntimeWarning`` leaked across
    this execution boundary. The helper does not suppress or translate
    structured public numerical errors raised by the analyzer.
    """

    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        return OperatorRecordResidualAnalyzer().execute(difference(matrix))


def assert_nonzero_normal_close(actual: float, expected: float) -> None:
    r"""Apply the normal-value ``64 * eps`` relative-error criterion.

    Both values must be finite and nonzero. Acceptance requires
    ``abs(actual - expected) <= 64 * eps * abs(expected)`` with no absolute
    tolerance. The allowed error must be positive and smaller than the expected
    magnitude, so zero cannot pass. This criterion excludes subnormal expected
    values and is neither a global forward-error bound nor a scientific
    tolerance.
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
    """Return representable-step distance for two positive binary64 values.

    Positive binary64 bit patterns are monotonically ordered, so subtraction of
    their unsigned integer encodings counts adjacent representable values. Zero
    and negative inputs are rejected by the calling acceptance helper.
    """

    actual_bits = int(np.asarray(actual, dtype=np.float64).view(np.uint64))
    expected_bits = int(np.asarray(expected, dtype=np.float64).view(np.uint64))
    return abs(actual_bits - expected_bits)


def assert_subnormal_ulp_close(actual: float, expected: float) -> int:
    """Apply the positive-subnormal acceptance bound of at most eight ULPs.

    One ULP is one adjacent binary64 representable step in this subnormal
    region. Both values must be strictly positive, so zero cannot pass. The ULP
    rule avoids a relative allowance that can underflow. It is local to these
    regression paths and is not a formal arbitrary-matrix or scientific bound.

    Returns
    -------
    int
        Observed ULP distance, available for environment auditing.
    """

    assert 0.0 < expected < np.finfo(np.float64).tiny
    assert actual > 0.0
    distance = binary64_ulp_distance(actual, expected)
    assert distance <= SUBNORMAL_ACCEPTANCE_MAX_ULP
    return distance


def assert_ordering(maximum: float, spectral: float, frobenius: float) -> None:
    """Require the exact public stored metric ordering for finite results."""

    assert 0.0 <= maximum <= spectral <= frobenius


NORMAL_COMPLEX_CASES = (
    ScalarCase("NV-ORA-007", "complex-1-plus-i-e100", (1.0 + 1.0j) * 1.0e100),
    ScalarCase("NV-ORA-008", "complex-1-plus-2i-e100", (1.0 + 2.0j) * 1.0e100),
)


@pytest.mark.parametrize(
    "case",
    NORMAL_COMPLEX_CASES,
    ids=[f"{case.evidence_id}-{case.name}" for case in NORMAL_COMPLEX_CASES],
)
def test_normal_complex_scalar_paths(case: ScalarCase) -> None:
    """Verify normal complex scalar evidence ``NV-ORA-007`` and ``008``.

    Evidence IDs
        ``NV-ORA-007`` and ``NV-ORA-008``.
    Requirement
        All three ``1 x 1`` norms agree with the magnitude of the stored complex
        scalar without leaked runtime warnings.
    Method and oracle
        Execute the public analyzer and derive the independent scalar oracle
        with ``math.hypot(float(real), float(imag))``.
    Acceptance
        Apply the explicit normal-value ``64 * eps`` criterion, require exact
        equality after public canonicalization, and enforce stored ordering.
    Interpretation and limitations
        Passing verifies these normal-scale scalar paths only; ``math.hypot`` is
        independent of the production analyzer but is not a general SVD oracle.
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


def test_small_normal_real_scalar_path() -> None:
    """Verify small normal scalar evidence ``NV-ORA-009``.

    Evidence ID
        ``NV-ORA-009``.
    Requirement and method
        Analyze the stored real scalar ``1e-200`` without runtime warnings.
    Oracle
        The exact absolute value of the stored binary64 real component.
    Acceptance
        Every metric satisfies the explicit normal-value criterion and stored
        ordering; zero cannot pass.
    Interpretation and limitations
        This is a normal-value regression, not subnormal or scientific evidence.
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
    ScalarCase(
        "NV-ORA-010",
        "complex-subnormal-1-plus-i-e-310",
        (1.0 + 1.0j) * 1.0e-310,
    ),
    ScalarCase(
        "NV-ORA-011",
        "complex-subnormal-1-plus-2i-e-310",
        (1.0 + 2.0j) * 1.0e-310,
    ),
)


@pytest.mark.parametrize(
    "case",
    COMPLEX_SUBNORMAL_CASES,
    ids=[f"{case.evidence_id}-{case.name}" for case in COMPLEX_SUBNORMAL_CASES],
)
def test_complex_subnormal_scalar_paths(case: ScalarCase) -> None:
    """Verify complex subnormal evidence ``NV-ORA-010`` and ``011``.

    Evidence IDs
        ``NV-ORA-010`` and ``NV-ORA-011``.
    Requirement and method
        Preserve positive representable metrics for stored complex subnormals
        under warning-as-error execution.
    Oracle
        ``math.hypot`` of the stored binary64 components.
    Acceptance
        Each metric is positive, within eight ULPs of the oracle, and satisfies
        exact stored ordering; zero cannot pass.
    Interpretation and limitations
        Passing covers these gradual-underflow scalar paths, not arbitrary
        subnormal matrices or a formal SVD error bound.
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
    ScalarCase("NV-ORA-012", "deep-real-subnormal-e-320", 1.0e-320 + 0.0j),
    ScalarCase(
        "NV-ORA-013",
        "deep-complex-subnormal-1-plus-i-e-320",
        (1.0 + 1.0j) * 1.0e-320,
    ),
)


@pytest.mark.parametrize(
    "case",
    DEEP_SUBNORMAL_CASES,
    ids=[f"{case.evidence_id}-{case.name}" for case in DEEP_SUBNORMAL_CASES],
)
def test_deep_subnormal_scalar_paths(case: ScalarCase) -> None:
    """Verify deep-subnormal evidence ``NV-ORA-012`` and ``013``.

    Evidence IDs
        ``NV-ORA-012`` and ``NV-ORA-013``.
    Requirement and method
        Analyze deep real and complex stored subnormals without warning leakage
        or flush-to-zero behavior.
    Oracle
        ``math.hypot`` of the actual stored binary64 components.
    Acceptance
        Positive results remain within eight ULPs and preserve stored ordering.
    Interpretation and limitations
        Passing depends on gradual underflow and does not generalize to runtimes
        that flush subnormals or to arbitrary matrix dimensions.
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


def test_smallest_positive_binary64_subnormal_path() -> None:
    """Verify smallest-positive-subnormal evidence ``NV-ORA-014``.

    Evidence ID
        ``NV-ORA-014``.
    Requirement and method
        Analyze the exact ``1 x 1`` smallest positive binary64 subnormal under
        warning-as-error execution.
    Oracle
        ``numpy.nextafter(0, 1)`` supplies the representable scalar itself; all
        three mathematical norms equal that exact positive value.
    Acceptance
        Every result is positive, within eight ULPs, and correctly ordered.
    Interpretation and limitations
        Passing verifies IEEE-754 gradual underflow. A flush-to-zero runtime
        fails the supported numerical contract for this evidence.
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


def test_two_dimensional_subnormal_ordering_regression() -> None:
    r"""Verify analytical subnormal matrix evidence ``NV-ORA-015``.

    Evidence ID
        ``NV-ORA-015``.
    Requirement and method
        Analyze ``1e-310 * [[2+2i, 2-2i], [1, -i]]`` without warning leakage.
    Oracle
        The largest coefficient magnitude is ``2*sqrt(2)``. The coefficient
        Frobenius norm is ``sqrt(18)=3*sqrt(2)``. Its Gram matrix is
        ``[[9, -9i], [9i, 9]]`` with eigenvalues 18 and 0, so the spectral norm
        is also ``3*sqrt(2)``. Expected scalars use ``math.sqrt`` and the stored
        scale, independently of production norm and SVD code.
    Acceptance
        All metrics are positive and within eight ULPs. Public roundoff
        canonicalization is expected to store spectral and Frobenius metrics
        exactly equal, with exact metric ordering.
    Interpretation and limitations
        Passing strengthens the prior positivity-only regression for this one
        matrix; it is not an arbitrary-dimensional subnormal guarantee.
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


def test_largest_finite_binary64_scalar_path() -> None:
    """Verify largest-representable scalar evidence ``NV-ORA-016``.

    Evidence ID
        ``NV-ORA-016``.
    Requirement and method
        Analyze a ``1 x 1`` matrix containing ``float64.max`` with runtime
        warnings forbidden; scale restoration must remain representable.
    Oracle
        Every mathematical norm of this real scalar matrix equals the exact
        stored largest finite binary64 value.
    Acceptance
        Metrics satisfy the explicit normal-value bound and exact ordering.
    Interpretation and limitations
        This representable scalar differs from ``SV-ORA-006``, where multiple
        finite entries have a true Frobenius norm beyond binary64 range.
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


def test_exact_scalar_zero_path() -> None:
    """Verify exact zero-scale evidence ``NV-ORA-017``.

    Evidence ID
        ``NV-ORA-017``.
    Requirement and method
        Analyze an exact scalar zero with warning-as-error execution through the
        public ActionObject, without calling private allowance logic.
    Oracle and acceptance
        Every mathematical norm and every stored metric is exactly ``0.0``;
        approximate comparison is prohibited.
    Interpretation and limitations
        Passing exercises the public zero-scale path only and carries no
        scientific-validation or uncertainty-quantification meaning.
    """

    matrix: npt.NDArray[np.complex128] = np.array([[0.0 + 0.0j]], dtype=np.complex128)

    result = execute_without_runtime_warning(matrix)

    assert result.maximum_absolute_residual == 0.0
    assert result.spectral_residual == 0.0
    assert result.frobenius_residual == 0.0
    assert_ordering(
        result.maximum_absolute_residual,
        result.spectral_residual,
        result.frobenius_residual,
    )
