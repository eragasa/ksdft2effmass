r"""Numerical verification of ``Geometry``.

Facet and represented meaning

-----------------------------
This class-owned module owns the linear independence facet. For the stored
row-lattice matrix :math:`\mathbf C\in\mathbb R^{3\times3}`, let

.. math::

\rho(\mathbf C)=\frac{\sigma_{\min}(\mathbf C)}
{\sigma_{\max}(\mathbf C)}.

The public ``Geometry.LINEAR_INDEPENDENCE_RTOL`` owns the dimensionless tolerance
:math:`r_{\mathrm{tol}}=10^{-12}`. Construction accepts exactly when
:math:`\sigma_{\max}>0` and :math:`\rho(\mathbf C)>r_{\mathrm{tol}}`; equality is
rejected by the strict implemented contract. ``NV-G-001`` through ``NV-G-009``
verify this numerical policy using analytical diagonal, triangular, dependent,
scaled, and row-permuted cases. Expected decisions are not manufactured with
NumPy rank, SVD, determinant, or private Geometry methods.

Cells contain built-in binary64-compatible floats in synthetic length unit
``test-L`` under metadata convention ``row Cartesian``. Every public construction
executes with ``RuntimeWarning`` promoted to an error. Passing establishes the
documented validity decision, scale robustness over tested normal extreme
scales, and absence of leaked runtime warnings. Failure may indicate a Geometry
numerical regression, unsupported platform/LAPACK behavior, contract mismatch, or
evidence defect requiring investigation; it does not by itself establish a
physical-model error. No DFT, Wannier, experimental, crystallographic, impurity,
scientific-validation, or uncertainty-quantification evidence is produced. Rust
conformance is not established.

Intrinsic and cross-object scope

--------------------------------
The class-owned SUT is ``Geometry``. Synthetic represented matrices, declared
binary64 scale regimes, units, warning-as-error policy, analytical expected values,
and exact or documented tolerance rules remain the independent oracles recorded
below; production private helpers are not oracles.

VVUQ and scientific exclusions

------------------------------
Passing establishes only agreement with the stated mathematics for the represented
shapes, dtypes, units, scales, zero exclusions, and warning policy. Failure may
identify implementation, oracle, tolerance, platform, or contract defects. It does
not establish physical correctness, scientific validation, UQ, portability, or
cross-language agreement.
"""

import warnings

import pytest

from ksdft2effmass.operators import Geometry

pytestmark = pytest.mark.numerical_verification

SUT = Geometry

RTOL = Geometry.LINEAR_INDEPENDENCE_RTOL


def construct_geometry(
    cell: tuple[tuple[float, float, float], ...],
) -> Geometry:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Input rows/components pass unchanged; coercion with ``np.asarray``,
    ``float``, or
    ``tuple`` is intentionally absent.

    Method: Supply fixed metadata ``synthetic``, ``open``, ``row Cartesian``, and
    synthetic
    length unit ``test-L``.

    Oracle: Each owning test documents an independent analytical rank or singular-
    value-ratio
    argument.

    Acceptance: The public Geometry constructor returns or raises its documented error.

    Interpretation: The helper centralizes metadata without reproducing validation
    logic.

    Limitations: Fixtures are synthetic; no DFT, Wannier, experimental,
    crystallographic, or impurity
    calculation produced them. The helper establishes no scientific validity, scientific
    validation, UQ, or Rust conformance.
    """

    return Geometry("synthetic", cell, "open", "row Cartesian", "test-L")


def test_constructor__well_conditioned_orthogonal_cell_is__is_enforced() -> None:
    r"""Evidence ID: NV-G-001

    Requirement: A clearly full-rank orthogonal row cell is admitted without warnings.

    Method: Construct :math:`\operatorname{diag}(1,2,4)` under warning-as-error.

    Oracle: Its singular values are exactly ``4``, ``2``, and ``1``; hence
    :math:`\rho=1/4\gg10^{-12}`.

    Acceptance: Construction succeeds and preserves the exact selected nested floats.

    Interpretation: Passing verifies a normal-scale accepted baseline.

    Limitations: It does not validate arbitrary orthogonal cells, physical units,
    scientific
    validation, UQ, or Rust conformance.
    """

    cell = ((1.0, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, 0.0, 4.0))
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        geometry = construct_geometry(cell)

    assert geometry.cell == cell


def test_constructor__exactly_dependent_cell_is_rejected__is_enforced() -> None:
    r"""Evidence ID: NV-G-002

    Requirement: Exactly linearly dependent row vectors violate the intrinsic invariant.

    Method: Duplicate the first row exactly and construct under warning-as-error.

    Oracle: ``row_2 = row_1`` gives the nontrivial exact relation ``row_2 - row_1 = 0``,
    so
    :math:`\sigma_{\min}=0`.

    Acceptance: Exactly ``ValueError`` identifies linear independence; no warning leaks.

    Interpretation: Passing verifies the exact-dependence rejection baseline.

    Limitations: It does not quantify conditioning of arbitrary matrices or establish
    scientific
    validation, UQ, or Rust conformance.
    """

    cell = ((1.0, 2.0, 0.0), (1.0, 2.0, 0.0), (0.0, 0.0, 1.0))
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        with pytest.raises(ValueError, match="linearly independent"):
            construct_geometry(cell)


def test_constructor__skew_independent_cell_is_admitted__is_enforced() -> None:
    r"""Evidence ID: NV-G-003

    Requirement: Orthogonality is not required; a clearly independent skew cell is
    valid.

    Method: Construct a lower-triangular cell under warning-as-error.

    Oracle: Forward substitution proves only zero coefficients solve the row linear
    combination;
    equivalently, the triangular diagonal product is ``2 * 3 * 4 = 24``, nonzero,
    without numerical determinant evaluation.

    Acceptance: Construction succeeds and preserves the selected cell exactly.

    Interpretation: Passing distinguishes independence from orthogonality.

    Limitations: No crystallographic or physical realism, scientific validation, UQ, or
    Rust
    conformance is established.
    """

    cell = ((2.0, 0.0, 0.0), (1.0, 3.0, 0.0), (0.5, -1.0, 4.0))
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        geometry = construct_geometry(cell)

    assert geometry.cell == cell


def test_constructor__left_handed_independent_cell_is_admitted__is_enforced() -> None:
    r"""Evidence ID: NV-G-004

    Requirement: Handedness and determinant sign are not Geometry invariants.

    Method: Construct a lower-triangular cell with a negative final diagonal entry.

    Oracle: The diagonal product ``2 * 3 * -4 = -24`` is nonzero and negative, proving
    full rank
    and left handedness analytically.

    Acceptance: Construction succeeds without warnings and preserves signs exactly.

    Interpretation: Passing confirms independence policy does not impose right
    handedness.

    Limitations: Admission is not a physical or crystallographic validity claim and
    establishes no
    scientific validation, UQ, or Rust conformance.
    """

    cell = ((2.0, 0.0, 0.0), (1.0, 3.0, 0.0), (-0.5, 1.0, -4.0))
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        geometry = construct_geometry(cell)

    assert geometry.cell == cell


def test_constructor__cell_clearly_below_public_threshold__is_rejected() -> None:
    r"""Evidence ID: NV-G-005

    Requirement: A diagonal cell with singular-value ratio ``RTOL / 2`` is invalid.

    Method: Construct the analytical diagonal case under RuntimeWarning-as-error.

    Oracle: Positive diagonal singular values are their entries, so the ratio is exactly
    half
    the independently fixed threshold.

    Acceptance: ``RTOL`` is exactly ``1e-12`` and construction raises independence
    ``ValueError``.

    Interpretation: A pass verifies clearly-below-threshold rejection without testing
    equality.

    Limitations: This does not select a scientific tolerance, validate a cell, perform
    UQ, or
    establish Rust agreement.
    """
    assert RTOL == 1.0e-12
    cell = ((1.0, 0.0, 0.0), (0.0, RTOL / 2.0, 0.0), (0.0, 0.0, 1.0))
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        with pytest.raises(ValueError, match="linearly independent"):
            construct_geometry(cell)


def test_constructor__cell_at_strict_public_threshold__is_rejected() -> None:
    r"""Evidence ID: NV-G-010

    Requirement: Equality with the strict public singular-value-ratio threshold is
    invalid.

    Method: Construct ``diag(1, RTOL, 1)`` under RuntimeWarning-as-error.

    Oracle: The positive diagonal singular values give ratio exactly the stored binary64
    ``RTOL`` and the public inequality is strict.

    Acceptance: Construction raises independence ``ValueError`` without warning.

    Interpretation: A pass verifies the inclusive rejection side of the exact threshold
    boundary.

    Limitations: This does not select a scientific tolerance, validate a cell, perform
    UQ, or
    establish Rust agreement.
    """
    cell = ((1.0, 0.0, 0.0), (0.0, RTOL, 0.0), (0.0, 0.0, 1.0))
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        with pytest.raises(ValueError, match="linearly independent"):
            construct_geometry(cell)


def test_constructor__cell_clearly_above_public_threshold_is__is_enforced() -> None:
    r"""Evidence ID: NV-G-006

    Requirement: A cell clearly above the strict public relative threshold is valid.

    Method: Construct ``diag(1, 2 * RTOL, 1)`` under warning-as-error.

    Oracle: Positive diagonal singular values are their absolute diagonal entries, so
    :math:`\rho=2r_{\mathrm{tol}}>r_{\mathrm{tol}}` analytically.

    Acceptance: Construction succeeds and preserves the diagonal value exactly.

    Interpretation: Passing verifies above-threshold admission without probing equality.

    Limitations: This does not select a scientific tolerance, perform UQ, or establish
    scientific
    validation or Rust conformance.
    """

    cell = ((1.0, 0.0, 0.0), (0.0, 2.0 * RTOL, 0.0), (0.0, 0.0, 1.0))
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        geometry = construct_geometry(cell)

    assert geometry.cell[1][1] == 2.0 * RTOL


@pytest.mark.parametrize(
    "scale",
    [
        pytest.param(-1e-200, id="scale_negative_1e_200"),
        pytest.param(1e-200, id="scale_positive_1e_200"),
        pytest.param(-1.0, id="scale_negative_1"),
        pytest.param(1.0, id="scale_positive_1"),
        pytest.param(-1e200, id="scale_negative_1e200"),
        pytest.param(1e200, id="scale_positive_1e200"),
    ],
)
def test_field__uniform_scale_invariance_for_well_conditioned_cells__is_exact(
    scale: float,
) -> None:
    r"""Evidence ID: NV-G-007

    Requirement: :math:`\rho(s\mathbf C)=\rho(\mathbf C)` for nonzero uniform ``s``.

    Method: Scale the identity cell by both signs of ``1e-200``, ``1``, and ``1e200``
    and
    construct each under warning-as-error.

    Oracle: All singular values of :math:`s\mathbf I` are analytically ``abs(s)``, so
    :math:`\rho=1` at every tested nonzero signed scale.

    Acceptance: Every construction succeeds, preserves ``scale`` on the diagonal, and
    leaks no
    ``RuntimeWarning``.

    Interpretation: Passing establishes tested scale robustness of accepted cells.

    Limitations: Scales are representative finite normal binary64 values, not an
    exhaustive platform
    proof; no scientific validation, UQ, or Rust conformance follows.
    """

    cell = ((scale, 0.0, 0.0), (0.0, scale, 0.0), (0.0, 0.0, scale))
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        geometry = construct_geometry(cell)

    assert geometry.cell[0][0] == scale


@pytest.mark.parametrize(
    "scale",
    [
        pytest.param(-1e-200, id="scale_negative_1e_200"),
        pytest.param(1e-200, id="scale_positive_1e_200"),
        pytest.param(-1.0, id="scale_negative_1"),
        pytest.param(1.0, id="scale_positive_1"),
        pytest.param(-1e200, id="scale_negative_1e200"),
        pytest.param(1e200, id="scale_positive_1e200"),
    ],
)
def test_field__uniform_scale_invariance_for_near_dependent_cells__is_exact(
    scale: float,
) -> None:
    r"""Evidence ID: NV-G-008

    Requirement: Uniform nonzero scaling cannot change a clearly invalid relative ratio.

    Method: Scale ``diag(1, RTOL / 2, 1)`` by both signs of each representative finite
    normal
    scale and construct under warning-as-error.

    Oracle: Singular values scale uniformly, leaving :math:`\rho=r_{\mathrm{tol}}/2`
    analytically at every scale.

    Acceptance: Every construction raises exactly independence ``ValueError`` and leaks
    no
    ``RuntimeWarning``.

    Interpretation: Passing establishes tested scale robustness of rejected
    near-dependence.

    Limitations: This does not cover exact-threshold behavior, select scientific
    tolerance, perform
    UQ, or establish scientific validation/Rust conformance.
    """

    cell = (
        (scale, 0.0, 0.0),
        (0.0, scale * (RTOL / 2.0), 0.0),
        (0.0, 0.0, scale),
    )
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        with pytest.raises(ValueError, match="linearly independent"):
            construct_geometry(cell)


@pytest.mark.parametrize(
    "permuted",
    [
        pytest.param(
            ((2.0, 0.0, 0.0), (1.0, 3.0, 0.0), (0.5, -1.0, 4.0)), id="valid_rows_abc"
        ),
        pytest.param(
            ((2.0, 0.0, 0.0), (0.5, -1.0, 4.0), (1.0, 3.0, 0.0)), id="valid_rows_acb"
        ),
        pytest.param(
            ((1.0, 3.0, 0.0), (2.0, 0.0, 0.0), (0.5, -1.0, 4.0)), id="valid_rows_bac"
        ),
        pytest.param(
            ((1.0, 3.0, 0.0), (0.5, -1.0, 4.0), (2.0, 0.0, 0.0)), id="valid_rows_bca"
        ),
        pytest.param(
            ((0.5, -1.0, 4.0), (2.0, 0.0, 0.0), (1.0, 3.0, 0.0)), id="valid_rows_cab"
        ),
        pytest.param(
            ((0.5, -1.0, 4.0), (1.0, 3.0, 0.0), (2.0, 0.0, 0.0)), id="valid_rows_cba"
        ),
    ],
)
def test_constructor__valid_row_permutation__preserves_independence(
    permuted: tuple[tuple[float, float, float], ...],
) -> None:
    r"""Evidence ID: NV-G-009

    Requirement: Every row permutation of the analytical full-rank triangular cell
    remains valid.

    Method: Construct all six literal permutations under RuntimeWarning-as-error.

    Oracle: Row permutation preserves the nonzero triangular determinant magnitude and
    singular
    values.

    Acceptance: Construction succeeds and preserves selected row order exactly.

    Interpretation: A pass verifies valid permutation invariance for this represented
    cell.

    Limitations: Other matrices, physical validity, validation, UQ, and Rust are
    excluded.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        geometry = construct_geometry(permuted)
    assert geometry.cell == permuted


@pytest.mark.parametrize(
    "permuted",
    [
        pytest.param(
            ((1.0, 2.0, 0.0), (1.0, 2.0, 0.0), (0.0, 0.0, 1.0)), id="dependent_rows_abc"
        ),
        pytest.param(
            ((1.0, 2.0, 0.0), (0.0, 0.0, 1.0), (1.0, 2.0, 0.0)), id="dependent_rows_acb"
        ),
        pytest.param(
            ((1.0, 2.0, 0.0), (1.0, 2.0, 0.0), (0.0, 0.0, 1.0)), id="dependent_rows_bac"
        ),
        pytest.param(
            ((1.0, 2.0, 0.0), (0.0, 0.0, 1.0), (1.0, 2.0, 0.0)), id="dependent_rows_bca"
        ),
        pytest.param(
            ((0.0, 0.0, 1.0), (1.0, 2.0, 0.0), (1.0, 2.0, 0.0)), id="dependent_rows_cab"
        ),
        pytest.param(
            ((0.0, 0.0, 1.0), (1.0, 2.0, 0.0), (1.0, 2.0, 0.0)), id="dependent_rows_cba"
        ),
    ],
)
def test_constructor__dependent_row_permutation__preserves_rejection(
    permuted: tuple[tuple[float, float, float], ...],
) -> None:
    r"""Evidence ID: NV-G-011

    Requirement: Every row permutation of the duplicated-row cell remains invalid.

    Method: Construct all six literal permutations under RuntimeWarning-as-error.

    Oracle: Permutation preserves the exact relation between duplicated rows.

    Acceptance: Every case raises independence ``ValueError`` without warning.

    Interpretation: A pass verifies invalid permutation invariance for this represented
    cell.

    Limitations: Near dependence, physical validity, validation, UQ, and Rust are
    excluded.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        with pytest.raises(ValueError, match="linearly independent"):
            construct_geometry(permuted)
