r"""Numerical verification of ``HermiticityAnalyzer``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This class-owned module owns the analytical residuals facet. Evidence IDs
------------
``NV-HA-001`` through ``NV-HA-005``.

Requirement: For a stored binary64 matrix :math:`H`, ``HermiticityAnalyzer`` computes

.. math::

\varepsilon_{\mathrm H}=\max_{i,j}|H_{ij}-H_{ji}^{*}|.

All matrices and residuals in these cases use the explicit energy unit ``eV``.
Hermiticity status is invariant under unitary similarity, while a nonzero
entrywise maximum residual magnitude is generally basis dependent.

Method: ``NV-HA-001`` through ``NV-HA-005`` use five small explicitly prepared
``np.complex128`` matrices, closed-form analytical oracles independent of the
production algorithm, and public Analyzer execution with ``RuntimeWarning``
promoted to an error.

Oracle: Expected values are derived entry by entry in test documentation using exact
zero,
``math.sqrt(26.0)``, ``1.0``, and ``1.0 / math.sqrt(3.0)``. Expected values are
never formed with the production Analyzer, private helpers, or a replicated
``np.max(np.abs(H - H.conj().T))`` calculation.

Acceptance: Analytical zero must be exactly ``0.0``. Nonzero normal binary64 values
satisfy
``abs(actual - expected) <= 64 * eps * abs(expected)`` with both values and the
bound explicitly nonzero and the bound smaller than the expected magnitude.

Interpretation: Passing establishes agreement with five small analytical matrix cases
under the
stated binary64 criterion. Failure may indicate an Analyzer regression,
unsupported platform/backend behavior, or an oracle/evidence defect requiring
investigation; it does not by itself establish physical-model error.

Limitations: The relative criterion is local to small normal-scale cases, not an
arbitrary-
dimension forward-error theorem, production tolerance policy, or scientific
acceptance policy. Synthetic matrices make no DFT, Wannier, impurity, basis/gauge
correctness, or scientific-validity claim. Scientific validation, uncertainty
quantification, and Rust conformance are not established.

Intrinsic and cross-object scope

--------------------------------
The class-owned SUT is ``HermiticityAnalyzer``. Synthetic represented matrices,
declared binary64 scale regimes, units, warning-as-error policy, analytical expected
values, and exact or documented tolerance rules remain the independent oracles
recorded below; production private helpers are not oracles.

VVUQ and scientific exclusions

------------------------------
Passing establishes only agreement with the stated mathematics for the represented
shapes, dtypes, units, scales, zero exclusions, and warning policy. Failure may
identify implementation, oracle, tolerance, platform, or contract defects. It does
not establish physical correctness, scientific validation, UQ, portability, or
cross-language agreement.
"""

import math
import warnings

import numpy as np
import numpy.typing as npt
import pytest

from ksdft2effmass.operators import (
    Basis,
    EnergyReference,
    Geometry,
    HermiticityAnalyzer,
    HermiticityResult,
    OperatorRecord,
    StateSpace,
)

pytestmark = pytest.mark.numerical_verification

SUT = HermiticityAnalyzer

VALID_CELL = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))


def make_record(
    matrix: npt.NDArray[np.complex128],
    *,
    energy_unit: str = "eV",
) -> OperatorRecord:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: ----------- Numerical cases supply explicitly prepared
    ``np.complex128`` matrices
    with matching finite metadata and no broad matrix coercion.

    Method: ------ Derive dimension from the already valid square shape, then construct
    matching
    state-space and ordered-basis metadata with deterministic geometry/provenance.

    Oracle: ------ The supplied matrix is passed unchanged; public constructors validate
    state.

    Acceptance: ---------- A valid ``OperatorRecord`` is produced for public Analyzer
    execution.

    Interpretation: -------------- The helper isolates fixture construction from
    independently derived
    oracles.

    Limitations: ----------- It performs no ``np.asarray`` coercion and makes no DFT,
    Wannier,
    impurity, scientific-validation, UQ, or Rust-conformance claim.
    """

    dimension = matrix.shape[0]
    ordering = tuple(f"basis-{index}" for index in range(dimension))
    return OperatorRecord(
        identifier="synthetic-hermiticity-analytical",
        operator_kind="finite_test_hamiltonian",
        matrix=matrix,
        state_space=StateSpace("synthetic-state-space", "finite synthetic", dimension),
        basis=Basis("ordered-test-basis", "finite synthetic", ordering, True),
        geometry=Geometry(
            "synthetic",
            VALID_CELL,
            "finite synthetic",
            "cartesian row lattice vectors",
            "angstrom",
        ),
        energy_reference=EnergyReference("explicit synthetic zero", energy_unit),
        provenance={"source": "synthetic Hermiticity analytical evidence"},
    )


def execute_with_runtime_warnings_as_errors(
    analyzer: HermiticityAnalyzer, record: OperatorRecord
) -> HermiticityResult:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: ----------- Every numerical evidence execution must leak no
    ``RuntimeWarning``.

    Method: ------ Promote ``RuntimeWarning`` to an exception around public
    ``execute()``.

    Oracle: ------ Successful production execution returns the public ResultObject.

    Acceptance: ---------- Execution returns normally; any leaked warning fails before
    assertions.

    Interpretation: -------------- The helper makes the warning boundary uniform and
    auditable.

    Limitations: ----------- It does not suppress or validate other warning classes and
    establishes
    no scientific validation, UQ, or Rust conformance.
    """

    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        return analyzer.execute(record)


def assert_normal_binary64_close(actual: float, expected: float) -> None:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: ----------- Nonzero normal analytical values use a criterion that
    cannot accept
    zero.

    Method: ------ Compare absolute error with ``64 * binary64_eps * abs(expected)``.

    Oracle: ------ ``np.finfo(np.float64).eps`` defines machine epsilon; each caller
    supplies an
    independently derived closed-form expected value.

    Acceptance: ---------- Both values are nonzero, the bound is positive and smaller
    than the
    expected magnitude, and absolute error does not exceed the bound.

    Interpretation: -------------- Passing establishes local binary64 agreement for
    these small normal
    cases.

    Limitations: ----------- The bound is not a production tolerance, scientific
    criterion,
    arbitrary- dimension theorem, scientific validation, UQ, or Rust-conformance result.
    """

    assert expected != 0.0
    assert actual != 0.0

    absolute_error = abs(actual - expected)
    allowed_error = 64.0 * np.finfo(np.float64).eps * abs(expected)

    assert allowed_error > 0.0
    assert allowed_error < abs(expected)
    assert absolute_error <= allowed_error


def test_field__exact_hermitian_matrix_has_exact_zero_residual__is_exact() -> None:
    r"""Evidence ID: NV-HA-001

    Requirement: ----------- The stored matrix ``[[1, i], [-i, 2]]`` equals its
    conjugate transpose.

    Method: ------ Analyze the explicit 2x2 ``np.complex128`` representation.

    Oracle: ------ Diagonal imaginary parts vanish and ``H_01 = conj(H_10)`` exactly, so
    every
    entry of :math:`H-H^\dagger` is zero and :math:`\varepsilon_H=0\,\mathrm{eV}`.

    Acceptance: ---------- The residual is exactly ``0.0`` under warning-as-error
    execution.

    Interpretation: -------------- Passing verifies exact-zero behavior for this
    analytical case.

    Limitations: ----------- It is one small synthetic matrix, not arbitrary-dimension
    verification,
    physical Hermiticity, scientific validation, UQ, or Rust conformance.
    """

    matrix = np.array(
        [[1.0 + 0.0j, 0.0 + 1.0j], [0.0 - 1.0j, 2.0 + 0.0j]],
        dtype=np.complex128,
    )
    result = execute_with_runtime_warnings_as_errors(
        HermiticityAnalyzer(tolerance=0.0, energy_unit="eV"), make_record(matrix)
    )

    assert result.residual == 0.0


def test_method__execute__complex_two_by_two_residual_is_sqrt_26() -> None:
    r"""Evidence ID: NV-HA-002

    Requirement: ----------- The Analyzer implements the entrywise maximum
    conjugate-transpose
    residual.

    Method: ------ Analyze ``[[1, 2+i], [3+4i, 4]]`` as explicit ``np.complex128``.

    Oracle: ------ The upper residual is ``(2+i)-conj(3+4i)=-1+5i`` with magnitude
    :math:`\sqrt{26}\,\mathrm{eV}`; the lower is its negative conjugate and diagonals
    are zero.

    Acceptance: ---------- Actual residual satisfies the explicit 64-epsilon
    normal-value criterion
    against ``math.sqrt(26.0)`` with warnings treated as errors.

    Interpretation: -------------- Passing verifies this nonzero complex analytical
    case.

    Limitations: ----------- The local criterion is not production/scientific tolerance
    policy,
    arbitrary-dimension proof, scientific validation, UQ, or Rust conformance.
    """

    matrix = np.array(
        [[1.0 + 0.0j, 2.0 + 1.0j], [3.0 + 4.0j, 4.0 + 0.0j]],
        dtype=np.complex128,
    )
    result = execute_with_runtime_warnings_as_errors(
        HermiticityAnalyzer(tolerance=0.0, energy_unit="eV"), make_record(matrix)
    )

    assert_normal_binary64_close(result.residual, math.sqrt(26.0))


def test_method__execute__real_nonsymmetric_residual_is_one() -> None:
    r"""Evidence ID: NV-HA-003

    Requirement: ----------- The entrywise criterion applies to real nonsymmetric
    matrices.

    Method: ------ Analyze the explicit matrix ``[[1, 2], [3, 4]]``.

    Oracle: ------ :math:`H-H^\dagger=[[0,-1],[1,0]]`, so the maximum magnitude is
    :math:`1\,\mathrm{eV}`.

    Acceptance: ---------- Actual residual satisfies the explicit 64-epsilon
    normal-value criterion.

    Interpretation: -------------- Passing verifies this nonzero real analytical case.

    Limitations: ----------- It is not a production/scientific tolerance,
    arbitrary-dimension
    theorem, scientific validation, UQ, or Rust conformance.
    """

    matrix = np.array(
        [[1.0 + 0.0j, 2.0 + 0.0j], [3.0 + 0.0j, 4.0 + 0.0j]],
        dtype=np.complex128,
    )
    result = execute_with_runtime_warnings_as_errors(
        HermiticityAnalyzer(tolerance=0.0, energy_unit="eV"), make_record(matrix)
    )

    assert_normal_binary64_close(result.residual, 1.0)


def test_field__exact_hermiticity_survives_genuine_unitary__is_exact() -> None:
    r"""Evidence ID: NV-HA-004

    Requirement: ----------- If :math:`H=H^\dagger` and :math:`U^\dagger U=I`, then
    :math:`U^\dagger
    H U` is Hermitian.

    Method: ------ Use the exact phase unitary ``diag(1, i)`` and explicitly form
    ``U.conj().T @
    H @ U`` from an exact Hermitian matrix.

    Oracle: ------ The selected entries ``1, -1, i, -i`` are exactly representable; the
    transformed matrix is exactly ``[[1, -1], [-1, 2]]`` and both residuals are exactly
    :math:`0\,\mathrm{eV}`.

    Acceptance: ---------- Original and transformed residuals both equal exactly ``0.0``
    with
    warnings treated as errors.

    Interpretation: -------------- Passing verifies unitary invariance of exact
    Hermiticity for a
    genuine basis transformation, correcting the former unrotated fixture evidence.

    Limitations: ----------- It does not claim every floating similarity remains bitwise
    exact or
    establish basis/gauge correctness, scientific validation, UQ, or Rust conformance.
    """

    matrix = np.array(
        [[1.0 + 0.0j, 0.0 + 1.0j], [0.0 - 1.0j, 2.0 + 0.0j]],
        dtype=np.complex128,
    )
    unitary = np.array(
        [[1.0 + 0.0j, 0.0 + 0.0j], [0.0 + 0.0j, 0.0 + 1.0j]],
        dtype=np.complex128,
    )
    transformed = unitary.conj().T @ matrix @ unitary
    analyzer = HermiticityAnalyzer(tolerance=0.0, energy_unit="eV")

    original_result = execute_with_runtime_warnings_as_errors(
        analyzer, make_record(matrix)
    )
    transformed_result = execute_with_runtime_warnings_as_errors(
        analyzer, make_record(transformed)
    )

    assert original_result.residual == 0.0
    assert transformed_result.residual == 0.0


def test_method__execute__nonzero_entrywise_residual_is_basis_dependent() -> None:
    r"""Evidence ID: NV-HA-005

    Requirement: ----------- Hermiticity status is unitarily invariant, but the nonzero
    entrywise
    maximum residual generally is not.

    Method: ------ Set only ``H[0,1]=1`` and form ``U^dagger H U`` with the 3x3
    discrete-Fourier
    unitary using :math:`\omega=-1/2+i\sqrt{3}/2`.

    Oracle: ------ Initially ``H-H^dagger`` has two unit-magnitude entries, giving
    :math:`1\,\mathrm{eV}`. Fourier similarity distributes the skew-Hermitian residual
    so its largest entry has closed-form magnitude :math:`1/\sqrt{3}\,\mathrm{eV}`.

    Acceptance: ---------- Both results satisfy the explicit 64-epsilon criterion
    against ``1.0``
    and ``1.0 / math.sqrt(3.0)`` under warning-as-error execution.

    Interpretation: -------------- Passing shows nonzero magnitude basis dependence
    without
    contradicting invariance of zero-versus-nonzero Hermiticity status.

    Limitations: ----------- This one floating Fourier case is not a
    basis/gauge-correctness
    assessment, arbitrary-dimension theorem, scientific validation, UQ, or Rust
    conformance.
    """

    matrix = np.array(
        [
            [0.0 + 0.0j, 1.0 + 0.0j, 0.0 + 0.0j],
            [0.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j],
            [0.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j],
        ],
        dtype=np.complex128,
    )
    omega = complex(-0.5, math.sqrt(3.0) / 2.0)
    unitary = np.array(
        [
            [1.0 + 0.0j, 1.0 + 0.0j, 1.0 + 0.0j],
            [1.0 + 0.0j, omega, omega**2],
            [1.0 + 0.0j, omega**2, omega],
        ],
        dtype=np.complex128,
    ) / math.sqrt(3.0)
    transformed = unitary.conj().T @ matrix @ unitary
    analyzer = HermiticityAnalyzer(tolerance=0.0, energy_unit="eV")

    original_result = execute_with_runtime_warnings_as_errors(
        analyzer, make_record(matrix)
    )
    transformed_result = execute_with_runtime_warnings_as_errors(
        analyzer, make_record(transformed)
    )

    assert_normal_binary64_close(original_result.residual, 1.0)
    assert_normal_binary64_close(transformed_result.residual, 1.0 / math.sqrt(3.0))
