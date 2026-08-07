r"""Numerical verification of ``OperatorRecordResidualAnalyzer``.

Facet and represented meaning
-----------------------------
This class-owned module owns the analytical norms facet. System under test and
evidence class
------------------------------------
``OperatorRecordResidualAnalyzer`` computes, for a finite represented difference
:math:`\Delta H`,

.. math::

\varepsilon_{\max}=\max_{i,j}|\Delta H_{ij}|,
\qquad
\varepsilon_{\mathrm F}=\sqrt{\sum_{i,j}|\Delta H_{ij}|^2},
\qquad
\varepsilon_2=\sigma_{\max}(\Delta H).

This module supplies numerical-verification evidence for six matrices of shape at
most ``2 x 2`` and dtype ``numpy.complex128``. Stored metrics are binary64
floats. The synthetic common energy unit is ``eV``; metadata propagation is
verified elsewhere and is not an oracle here.

Independent analytical reference cases
--------------------------------------
``NV-ORA-001`` — exact zero ``2 x 2`` matrix
For :math:`\Delta H=\begin{pmatrix}0&0\\0&0\end{pmatrix}`, every entry and
singular value is zero, so all three metrics are exactly zero.

``NV-ORA-002`` — diagonal 3-4 matrix
For :math:`\Delta H=\begin{pmatrix}3&0\\0&4\end{pmatrix}`, the largest
absolute entry is 4, the Euclidean sum is
:math:`\sqrt{3^2+4^2}=5`, and the singular values are 3 and 4. Therefore
:math:`(\varepsilon_{\max},\varepsilon_{\mathrm F},\varepsilon_2)=(4,5,4)`.

``NV-ORA-003`` — complex scalar 3+4i
For the ``1 x 1`` matrix :math:`\Delta H=(3+4i)`, the only singular value
is :math:`|3+4i|=5`, so all three metrics equal 5.

``NV-ORA-004`` — nonsymmetric rank-one matrix
For :math:`\Delta H=\begin{pmatrix}0&3\\0&4\end{pmatrix}`, the nonzero
column has Euclidean norm 5. The matrix has rank one, so its only nonzero
singular value is 5. Thus
:math:`(\varepsilon_{\max},\varepsilon_{\mathrm F},\varepsilon_2)=(4,5,5)`.

``NV-ORA-005`` and ``NV-ORA-006`` — normal-scale rank-one matrices
For :math:`\Delta H=\begin{pmatrix}a&0\\0&0\end{pmatrix}` with
:math:`a=10^{200}` or :math:`a=10^{-200}`, there is one nonzero entry and
one nonzero singular value. Hence all metrics equal :math:`|a|`.

These expected values are derived analytically. They are not generated with
``numpy.linalg.svd``, ``numpy.linalg.norm``, or the production analyzer.

Acceptance, warning boundary, and interpretation
------------------------------------------------
Expected zero requires exact equality. For nonzero normal-scale references,
acceptance requires

.. math::

|x_{\mathrm{actual}}-x_{\mathrm{expected}}|
\leq 64\epsilon_{\mathrm{mach}}|x_{\mathrm{expected}}|.

For every nonzero value in this module, the allowed error is representable,
positive, and strictly smaller than :math:`|x_{\mathrm{expected}}|`; an actual
zero therefore cannot pass. The bound is a conservative regression criterion
for these small binary64 cases, whose computation includes absolute values,
scaled summation, and SVD. It is not a formal global forward-error bound for
arbitrary dimensions or conditioning, a production comparison policy, or a
scientific acceptance tolerance. Subnormal acceptance is excluded and belongs
to the floating-point regression module, where ULP criteria are required.

Every execution promotes ``RuntimeWarning`` to an error. Passing means the
finite-matrix residual kernel agrees with these analytical oracles under the
stated criterion without leaking a NumPy runtime warning. Passing does not
establish physical equivalence, basis or gauge alignment, scientific residual
acceptability, DFT or Wannier accuracy, model validation, or uncertainty
quantification. Scientific validation and uncertainty quantification have not
been performed.

Intrinsic and cross-object scope
--------------------------------
The class-owned SUT is ``OperatorRecordResidualAnalyzer``. Synthetic represented
matrices, declared binary64 scale regimes, units, warning-as-error policy,
analytical expected values, and exact or documented tolerance rules remain the
independent oracles recorded below; production private helpers are not oracles.

VVUQ and scientific exclusions
------------------------------
Passing establishes only agreement with the stated mathematics for the represented
shapes, dtypes, units, scales, zero exclusions, and warning policy. Failure may
identify implementation, oracle, tolerance, platform, or contract defects. It does
not establish physical correctness, scientific validation, UQ, portability, or
cross-language agreement.
"""

import warnings
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
import pytest

from ksdft2effmass.operators import (
    OperatorRecordCompatibilityResult,
    OperatorRecordDifferenceResult,
    OperatorRecordResidualAnalyzer,
)

pytestmark = pytest.mark.numerical_verification

SUT = OperatorRecordResidualAnalyzer

BINARY64_RELATIVE_TOLERANCE = 64.0 * np.finfo(np.float64).eps


@dataclass(frozen=True, slots=True)
class AnalyticalCase:
    r"""Module-owned analytical reference data for one numerical test case.

    Parameters
    ----------
    evidence_id
    Stable ``NV-ORA-###`` traceability identifier retained across future
    file reorganization.
    name
    Readable case label used in pytest parameter identification.
    matrix
    Exact module-owned ``numpy.ndarray`` with ``complex128`` dtype. Tests
    must not mutate this reference array.
    maximum
    Independently derived expected entrywise maximum norm, in ``eV``.
    frobenius
    Independently derived expected Frobenius norm, in ``eV``.
    spectral
    Independently derived expected spectral norm, in ``eV``.

    Notes
    -----
    Every case uses the synthetic common energy unit ``eV``. Expected values
    must be derived without ``numpy.linalg.svd``, ``numpy.linalg.norm``, or the
    production analyzer. ``frozen=True`` prevents field reassignment but does
    not make the contained NumPy array immutable; the arrays are module-owned
    reference data and must not be mutated. This test-only record is not a
    production DataObject and carries no claim of scientific validity.
    """

    evidence_id: str
    name: str
    matrix: npt.NDArray[np.complex128]
    maximum: float
    frobenius: float
    spectral: float


def difference(matrix: npt.NDArray[np.complex128]) -> OperatorRecordDifferenceResult:
    r"""Evidence ID
    Owns no identifier; supports evidence in this module.
    Requirement
    Residual analysis accepts a compatible represented difference with the supplied
    complex128 matrix and explicit eV unit.
    Method
    Construct or inspect only the named synthetic fixture operation (difference); the
    helper owns no assertion result and introduces no hidden oracle.
    Oracle
    Exact scalar identities, hand-derived matrix norms where stated, Python exception
    semantics, and the public structured-error taxonomy determine the expected result
    independently of analyzer private helpers.
    Acceptance
    The helper returns exactly the requested fixture value or applies only the
    documented comparison; all pass/fail assertions remain in the owning test.
    Interpretation
    A pass supports only the stated represented residual or error-boundary case; failure
    may identify analyzer, oracle, backend/environment, fixture, or accepted-contract
    drift.
    Limitations
    The synthetic matrices cover only the stated shapes, complex128 precision, eV units,
    and scales; they do not establish physical correctness, scientific validation, UQ,
    portability, or cross-language agreement.
    """

    return OperatorRecordDifferenceResult(
        OperatorRecordCompatibilityResult("reference", "candidate", ()),
        matrix,
        "eV",
    )


def assert_nonzero_normal_close(actual: float, expected: float) -> None:
    r"""Evidence ID
    Owns no identifier; supports evidence in this module.
    Requirement
    A nonzero normal binary64 result is compared with a nonzero independently calculated
    reference under the declared local regression envelope.
    Method
    Construct or inspect only the named synthetic fixture operation (assert nonzero
    normal close); the helper owns no assertion result and introduces no hidden oracle.
    Oracle
    Exact scalar identities, hand-derived matrix norms where stated, Python exception
    semantics, and the public structured-error taxonomy determine the expected result
    independently of analyzer private helpers.
    Acceptance
    The helper returns exactly the requested fixture value or applies only the
    documented comparison; all pass/fail assertions remain in the owning test.
    Interpretation
    A pass supports only the stated represented residual or error-boundary case; failure
    may identify analyzer, oracle, backend/environment, fixture, or accepted-contract
    drift.
    Limitations
    The synthetic matrices cover only the stated shapes, complex128 precision, eV units,
    and scales; they do not establish physical correctness, scientific validation, UQ,
    portability, or cross-language agreement.
    """

    assert expected != 0.0
    assert actual != 0.0

    absolute_error = abs(actual - expected)
    allowed_error = BINARY64_RELATIVE_TOLERANCE * abs(expected)

    assert allowed_error > 0.0
    assert allowed_error < abs(expected)
    assert absolute_error <= allowed_error


def assert_metric(actual: float, expected: float) -> None:
    r"""Evidence ID
    Owns no identifier; supports evidence in this module.
    Requirement
    An analytical residual metric is either exactly zero or a nonzero normal binary64
    value within its declared forward-error criterion.
    Method
    Construct or inspect only the named synthetic fixture operation (assert metric); the
    helper owns no assertion result and introduces no hidden oracle.
    Oracle
    Exact scalar identities, hand-derived matrix norms where stated, Python exception
    semantics, and the public structured-error taxonomy determine the expected result
    independently of analyzer private helpers.
    Acceptance
    The helper returns exactly the requested fixture value or applies only the
    documented comparison; all pass/fail assertions remain in the owning test.
    Interpretation
    A pass supports only the stated represented residual or error-boundary case; failure
    may identify analyzer, oracle, backend/environment, fixture, or accepted-contract
    drift.
    Limitations
    The synthetic matrices cover only the stated shapes, complex128 precision, eV units,
    and scales; they do not establish physical correctness, scientific validation, UQ,
    portability, or cross-language agreement.
    """

    if expected == 0.0:
        assert actual == 0.0
    else:
        assert_nonzero_normal_close(actual, expected)


CASES = (
    pytest.param(
        AnalyticalCase(
            "NV-ORA-001",
            "zero-2x2",
            np.array([[0.0 + 0j, 0.0 + 0j], [0.0 + 0j, 0.0 + 0j]], dtype=np.complex128),
            0.0,
            0.0,
            0.0,
        ),
        id="zero_2x2",
    ),
    pytest.param(
        AnalyticalCase(
            "NV-ORA-002",
            "diagonal-3-4",
            np.array([[3.0 + 0j, 0.0 + 0j], [0.0 + 0j, 4.0 + 0j]], dtype=np.complex128),
            4.0,
            5.0,
            4.0,
        ),
        id="diagonal_3_4",
    ),
    pytest.param(
        AnalyticalCase(
            "NV-ORA-003",
            "complex-3-plus-4i",
            np.array([[3.0 + 4j]], dtype=np.complex128),
            5.0,
            5.0,
            5.0,
        ),
        id="complex_3_plus_4i",
    ),
    pytest.param(
        AnalyticalCase(
            "NV-ORA-004",
            "nonsymmetric-rank-one",
            np.array([[0.0 + 0j, 3.0 + 0j], [0.0 + 0j, 4.0 + 0j]], dtype=np.complex128),
            4.0,
            5.0,
            5.0,
        ),
        id="nonsymmetric_rank_one",
    ),
    pytest.param(
        AnalyticalCase(
            "NV-ORA-005",
            "large-normal-rank-one",
            np.array(
                [[1e200 + 0j, 0.0 + 0j], [0.0 + 0j, 0.0 + 0j]], dtype=np.complex128
            ),
            1e200,
            1e200,
            1e200,
        ),
        id="large_normal_rank_one",
    ),
    pytest.param(
        AnalyticalCase(
            "NV-ORA-006",
            "small-normal-rank-one",
            np.array(
                [[1e-200 + 0j, 0.0 + 0j], [0.0 + 0j, 0.0 + 0j]], dtype=np.complex128
            ),
            1e-200,
            1e-200,
            1e-200,
        ),
        id="small_normal_rank_one",
    ),
)


@pytest.mark.parametrize("case", CASES)
def test_method__execute__matches_independent_analytical_norms(
    case: AnalyticalCase,
) -> None:
    r"""Evidence ID
    NV-ORA-001
    Requirement
    The finite-matrix residual kernel returns the analytical maximum-entry, Frobenius,
    and spectral norms in documented metric order.
    Method
    Execute each module-owned ``complex128`` matrix through the public analyzer while
    treating every ``RuntimeWarning`` as an error.
    Oracle
    Independently derived values documented in the module and stored in
    ``AnalyticalCase``; production NumPy norm or SVD calls do not construct expected
    values.
    Acceptance
    Expected zero is exact. Nonzero normal values satisfy the explicit ``64 * eps``
    relative-error bound, which cannot accept zero. Stored metrics satisfy ``0 <=
    maximum <= spectral <= Frobenius``.
    Interpretation
    Passing establishes agreement for these six finite analytical cases and absence of
    leaked NumPy runtime warnings.
    Limitations
    Passing does not establish physical equivalence, basis or gauge alignment,
    scientific residual acceptability, DFT or Wannier accuracy, model validation, or
    uncertainty quantification. Subnormal behavior is outside this module.
    """

    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        result = OperatorRecordResidualAnalyzer().execute(difference(case.matrix))

    assert_metric(result.maximum_absolute_residual, case.maximum)
    assert_metric(result.frobenius_residual, case.frobenius)
    assert_metric(result.spectral_residual, case.spectral)
    assert 0.0 <= result.maximum_absolute_residual
    assert result.maximum_absolute_residual <= result.spectral_residual
    assert result.spectral_residual <= result.frobenius_residual
