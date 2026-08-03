r"""Numerical verification of ``Geometry`` row-vector linear independence.

Mathematical contract and evidence class
----------------------------------------
For the stored row-lattice matrix :math:`\mathbf C\in\mathbb R^{3\times3}`, let

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

Scale, warning, and VVUQ boundary
---------------------------------
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
"""

import warnings
from itertools import permutations

import pytest

from ksdft2effmass.operators import Geometry

pytestmark = pytest.mark.numerical_verification

RTOL = Geometry.LINEAR_INDEPENDENCE_RTOL


def construct_geometry(
    cell: tuple[tuple[float, float, float], ...],
) -> Geometry:
    """Pass one synthetic cell unchanged to the public constructor.

    Evidence ID
        Supporting helper for ``NV-G-001`` through ``NV-G-009``; it owns no
        separate evidence identifier.
    Requirement
        Input rows/components pass unchanged; coercion with ``np.asarray``,
        ``float``, or ``tuple`` is intentionally absent.
    Method
        Supply fixed metadata ``synthetic``, ``open``, ``row Cartesian``, and
        synthetic length unit ``test-L``.
    Oracle
        Each owning test documents an independent analytical rank or singular-
        value-ratio argument.
    Acceptance
        The public Geometry constructor returns or raises its documented error.
    Interpretation
        The helper centralizes metadata without reproducing validation logic.
    Limitations
        Fixtures are synthetic; no DFT, Wannier, experimental, crystallographic,
        or impurity calculation produced them. The helper establishes no
        scientific validity, scientific validation, UQ, or Rust conformance.
    """

    return Geometry("synthetic", cell, "open", "row Cartesian", "test-L")


def test_well_conditioned_orthogonal_cell_is_admitted() -> None:
    r"""NV-G-001: admit an analytically well-conditioned diagonal cell.

    Evidence ID
        ``NV-G-001``.
    Requirement
        A clearly full-rank orthogonal row cell is admitted without warnings.
    Method
        Construct :math:`\operatorname{diag}(1,2,4)` under warning-as-error.
    Oracle
        Its singular values are exactly ``4``, ``2``, and ``1``; hence
        :math:`\rho=1/4\gg10^{-12}`.
    Acceptance
        Construction succeeds and preserves the exact selected nested floats.
    Interpretation
        Passing verifies a normal-scale accepted baseline.
    Limitations
        It does not validate arbitrary orthogonal cells, physical units,
        scientific validation, UQ, or Rust conformance.
    """

    cell = ((1.0, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, 0.0, 4.0))
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        geometry = construct_geometry(cell)

    assert geometry.cell == cell


def test_exactly_dependent_cell_is_rejected() -> None:
    r"""NV-G-002: reject exact duplicated-row dependence.

    Evidence ID
        ``NV-G-002``.
    Requirement
        Exactly linearly dependent row vectors violate the intrinsic invariant.
    Method
        Duplicate the first row exactly and construct under warning-as-error.
    Oracle
        ``row_2 = row_1`` gives the nontrivial exact relation
        ``row_2 - row_1 = 0``, so :math:`\sigma_{\min}=0`.
    Acceptance
        Exactly ``ValueError`` identifies linear independence; no warning leaks.
    Interpretation
        Passing verifies the exact-dependence rejection baseline.
    Limitations
        It does not quantify conditioning of arbitrary matrices or establish
        scientific validation, UQ, or Rust conformance.
    """

    cell = ((1.0, 2.0, 0.0), (1.0, 2.0, 0.0), (0.0, 0.0, 1.0))
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        with pytest.raises(ValueError, match="linearly independent"):
            construct_geometry(cell)


def test_skew_independent_cell_is_admitted() -> None:
    r"""NV-G-003: admit a nonorthogonal analytically full-rank cell.

    Evidence ID
        ``NV-G-003``.
    Requirement
        Orthogonality is not required; a clearly independent skew cell is valid.
    Method
        Construct a lower-triangular cell under warning-as-error.
    Oracle
        Forward substitution proves only zero coefficients solve the row linear
        combination; equivalently, the triangular diagonal product is
        ``2 * 3 * 4 = 24``, nonzero, without numerical determinant evaluation.
    Acceptance
        Construction succeeds and preserves the selected cell exactly.
    Interpretation
        Passing distinguishes independence from orthogonality.
    Limitations
        No crystallographic or physical realism, scientific validation, UQ, or
        Rust conformance is established.
    """

    cell = ((2.0, 0.0, 0.0), (1.0, 3.0, 0.0), (0.5, -1.0, 4.0))
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        geometry = construct_geometry(cell)

    assert geometry.cell == cell


def test_left_handed_independent_cell_is_admitted() -> None:
    r"""NV-G-004: admit an independent negative-orientation cell.

    Evidence ID
        ``NV-G-004``.
    Requirement
        Handedness and determinant sign are not Geometry invariants.
    Method
        Construct a lower-triangular cell with a negative final diagonal entry.
    Oracle
        The diagonal product ``2 * 3 * -4 = -24`` is nonzero and negative,
        proving full rank and left handedness analytically.
    Acceptance
        Construction succeeds without warnings and preserves signs exactly.
    Interpretation
        Passing confirms independence policy does not impose right handedness.
    Limitations
        Admission is not a physical or crystallographic validity claim and
        establishes no scientific validation, UQ, or Rust conformance.
    """

    cell = ((2.0, 0.0, 0.0), (1.0, 3.0, 0.0), (-0.5, 1.0, -4.0))
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        geometry = construct_geometry(cell)

    assert geometry.cell == cell


def test_cell_clearly_below_public_threshold_is_rejected() -> None:
    r"""NV-G-005: reject an analytical ratio of ``RTOL / 2``.

    Evidence ID
        ``NV-G-005``.
    Requirement
        A cell clearly below the strict public relative threshold is invalid.
    Method
        Construct ``diag(1, RTOL / 2, 1)`` under warning-as-error.
    Oracle
        The approved public tolerance is independently fixed at ``1e-12``.
        Positive diagonal singular values are their absolute diagonal entries,
        so :math:`\rho=r_{\mathrm{tol}}/2<r_{\mathrm{tol}}` analytically. For the
        exact diagonal equality companion, the ratio is the same stored public
        binary64 tolerance and the documented strict inequality rejects equality.
    Acceptance
        The public tolerance equals exactly ``1e-12``. Both clearly below and
        exact-equality diagonal cells raise ``ValueError`` identifying
        independence, and no warning leaks.
    Interpretation
        Passing verifies the public tolerance value, below-threshold rejection,
        and the explicitly documented strict equality boundary.
    Limitations
        This is numerical verification of binary64 policy, not UQ or selection of
        a scientifically appropriate threshold; Rust conformance is not tested.
    """

    assert RTOL == 1.0e-12
    below = ((1.0, 0.0, 0.0), (0.0, RTOL / 2.0, 0.0), (0.0, 0.0, 1.0))
    equality = ((1.0, 0.0, 0.0), (0.0, RTOL, 0.0), (0.0, 0.0, 1.0))
    for cell in (below, equality):
        with warnings.catch_warnings():
            warnings.simplefilter("error", RuntimeWarning)
            with pytest.raises(ValueError, match="linearly independent"):
                construct_geometry(cell)


def test_cell_clearly_above_public_threshold_is_admitted() -> None:
    r"""NV-G-006: admit an analytical ratio of ``2 * RTOL``.

    Evidence ID
        ``NV-G-006``.
    Requirement
        A cell clearly above the strict public relative threshold is valid.
    Method
        Construct ``diag(1, 2 * RTOL, 1)`` under warning-as-error.
    Oracle
        Positive diagonal singular values are their absolute diagonal entries,
        so :math:`\rho=2r_{\mathrm{tol}}>r_{\mathrm{tol}}` analytically.
    Acceptance
        Construction succeeds and preserves the diagonal value exactly.
    Interpretation
        Passing verifies above-threshold admission without probing equality.
    Limitations
        This does not select a scientific tolerance, perform UQ, or establish
        scientific validation or Rust conformance.
    """

    cell = ((1.0, 0.0, 0.0), (0.0, 2.0 * RTOL, 0.0), (0.0, 0.0, 1.0))
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        geometry = construct_geometry(cell)

    assert geometry.cell[1][1] == 2.0 * RTOL


@pytest.mark.parametrize(
    "scale",
    [
        pytest.param(-1.0e-200, id="NV-G-007-scale-negative-1e-200"),
        pytest.param(1.0e-200, id="NV-G-007-scale-positive-1e-200"),
        pytest.param(-1.0, id="NV-G-007-scale-negative-1"),
        pytest.param(1.0, id="NV-G-007-scale-positive-1"),
        pytest.param(-1.0e200, id="NV-G-007-scale-negative-1e200"),
        pytest.param(1.0e200, id="NV-G-007-scale-positive-1e200"),
    ],
)
def test_uniform_scale_invariance_for_well_conditioned_cells(scale: float) -> None:
    r"""NV-G-007: preserve a valid decision across finite normal extreme scales.

    Evidence ID
        ``NV-G-007`` with stable scale IDs.
    Requirement
        :math:`\rho(s\mathbf C)=\rho(\mathbf C)` for nonzero uniform ``s``.
    Method
        Scale the identity cell by both signs of ``1e-200``, ``1``, and ``1e200``
        and construct each under warning-as-error.
    Oracle
        All singular values of :math:`s\mathbf I` are analytically ``abs(s)``, so
        :math:`\rho=1` at every tested nonzero signed scale.
    Acceptance
        Every construction succeeds, preserves ``scale`` on the diagonal, and
        leaks no ``RuntimeWarning``.
    Interpretation
        Passing establishes tested scale robustness of accepted cells.
    Limitations
        Scales are representative finite normal binary64 values, not an exhaustive
        platform proof; no scientific validation, UQ, or Rust conformance follows.
    """

    cell = ((scale, 0.0, 0.0), (0.0, scale, 0.0), (0.0, 0.0, scale))
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        geometry = construct_geometry(cell)

    assert geometry.cell[0][0] == scale


@pytest.mark.parametrize(
    "scale",
    [
        pytest.param(-1.0e-200, id="NV-G-008-scale-negative-1e-200"),
        pytest.param(1.0e-200, id="NV-G-008-scale-positive-1e-200"),
        pytest.param(-1.0, id="NV-G-008-scale-negative-1"),
        pytest.param(1.0, id="NV-G-008-scale-positive-1"),
        pytest.param(-1.0e200, id="NV-G-008-scale-negative-1e200"),
        pytest.param(1.0e200, id="NV-G-008-scale-positive-1e200"),
    ],
)
def test_uniform_scale_invariance_for_near_dependent_cells(scale: float) -> None:
    r"""NV-G-008: preserve a below-threshold decision across extreme scales.

    Evidence ID
        ``NV-G-008`` with stable scale IDs.
    Requirement
        Uniform nonzero scaling cannot change a clearly invalid relative ratio.
    Method
        Scale ``diag(1, RTOL / 2, 1)`` by both signs of each representative
        finite normal scale and construct under warning-as-error.
    Oracle
        Singular values scale uniformly, leaving
        :math:`\rho=r_{\mathrm{tol}}/2` analytically at every scale.
    Acceptance
        Every construction raises exactly independence ``ValueError`` and leaks
        no ``RuntimeWarning``.
    Interpretation
        Passing establishes tested scale robustness of rejected near-dependence.
    Limitations
        This does not cover exact-threshold behavior, select scientific tolerance,
        perform UQ, or establish scientific validation/Rust conformance.
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


def test_row_permutation_does_not_change_validity_decision() -> None:
    r"""NV-G-009: preserve valid and invalid decisions under every row permutation.

    Evidence ID
        ``NV-G-009``.
    Requirement
        Row permutations change stored representation order but not linear
        independence or the singular-value ratio.
    Method
        Construct every permutation of one triangular valid cell and one exactly
        duplicated-row invalid cell, promoting runtime warnings to errors.
    Oracle
        Permutation only reorders equations: the valid triangular rows retain the
        nonzero diagonal-product full-rank argument, while the invalid cell retains
        two exactly equal rows.
    Acceptance
        All six valid permutations succeed and preserve their selected row order;
        all six invalid permutations raise exactly independence ``ValueError``;
        no warning leaks.
    Interpretation
        Passing separates ordering-sensitive stored equality from invariant
        validity decision.
    Limitations
        It is limited to these analytical fixtures and establishes no scientific
        validation, UQ, physical equivalence, or Rust conformance.
    """

    valid = ((2.0, 0.0, 0.0), (1.0, 3.0, 0.0), (0.5, -1.0, 4.0))
    invalid = ((1.0, 2.0, 0.0), (1.0, 2.0, 0.0), (0.0, 0.0, 1.0))

    for permuted in permutations(valid):
        with warnings.catch_warnings():
            warnings.simplefilter("error", RuntimeWarning)
            geometry = construct_geometry(permuted)
        assert geometry.cell == permuted

    for permuted in permutations(invalid):
        with warnings.catch_warnings():
            warnings.simplefilter("error", RuntimeWarning)
            with pytest.raises(ValueError, match="linearly independent"):
                construct_geometry(permuted)
