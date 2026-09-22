r"""Software verification of ``SparseLocalityResidualAnalyzer``.

Evidence profile: routine

Bounded artifact scope: nondensifying global, core, exterior, coupling, and row-shell
residuals for compatible scalar finite-lattice operators.

Facet and represented meaning

The ActionObject subtracts only exact compatible representations and partitions stored
residual entries by one explicit minimum-image Chebyshev partition.

Intrinsic and cross-object scope

A hand-authored 4x4 sparse residual contains diagonal core/exterior terms and symmetric
core--exterior coupling.

VVUQ and scientific exclusions

Values are synthetic test data. This is software verification, not a physical locality
claim, numerical or scientific validation, UQ, campaign execution, or acceptance.
"""

import math

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.analysis.finite_domain_locality import (
    MinimumImageChebyshevPartitioner,
    SparseLocalityResidualAnalyzer,
)
from ksdft2effmass.operators import ComplexSparseMatrixQuantity, Unitless
from ksdft2effmass.solid_state import (
    BoundaryTwistLift,
    BoundaryTwistReducer,
    FiniteLatticeShape,
    LatticeCoordinate,
    LatticeDimension,
    ScalarFiniteLatticeOperator,
    ScalarFiniteLatticeOperatorCompatibilityAnalyzer,
    TwistFiber,
    TwistGaugeRepresentation,
)

pytestmark = pytest.mark.software_verification
SUT = SparseLocalityResidualAnalyzer


class TestSparseLocalityResidualAnalyzer:
    """Own software evidence for sparse locality residual analysis."""

    def test_method__execute__matches_hand_derived_block_and_shell_norms(self) -> None:
        """Evidence ID: SV-ANALYSIS-SPARSE-LOCALITY-RESIDUAL-001

        Requirement: Sparse residual entries contribute exactly once to row shells and
        to core, exterior, or combined cross-coupling blocks.

        Acceptance: Five authored entries yield maximum 4, Frobenius sqrt(46), core
        sqrt(5), exterior 3, coupling sqrt(32), and shell norms sqrt(17), 2, and 5.
        """
        shape = FiniteLatticeShape(LatticeDimension.TWO, (4, 4))
        fiber = TwistFiber(
            BoundaryTwistReducer().execute(
                BoundaryTwistLift(LatticeDimension.TWO, (0.0, 0.0))
            ),
            TwistGaugeRepresentation.CENTERED_UNIFORM_LINK,
        )
        reference = ScalarFiniteLatticeOperator(
            "reference",
            ComplexSparseMatrixQuantity.from_csr(
                sparse.csr_array((16, 16), dtype=np.complex128), Unitless()
            ),
            shape,
            fiber,
            "basis",
            "zero",
            (),
        )
        candidate_matrix = sparse.coo_array(
            (
                np.array([1.0, 2.0, 3.0, 4.0, 4.0], dtype=np.complex128),
                (np.array([0, 1, 10, 0, 10]), np.array([0, 1, 10, 10, 0])),
            ),
            shape=(16, 16),
        )
        candidate = ScalarFiniteLatticeOperator(
            "candidate",
            ComplexSparseMatrixQuantity.from_csr(candidate_matrix, Unitless()),
            shape,
            fiber,
            "basis",
            "zero",
            (),
        )
        compatibility = ScalarFiniteLatticeOperatorCompatibilityAnalyzer().execute(
            reference, candidate
        )
        partition = MinimumImageChebyshevPartitioner().execute(
            shape,
            LatticeCoordinate(LatticeDimension.TWO, (0, 0)),
            core_radius=1,
        )

        result = SparseLocalityResidualAnalyzer().execute(
            reference, candidate, compatibility, partition
        )

        assert result.maximum_absolute_residual == 4.0
        assert result.frobenius_residual == pytest.approx(math.sqrt(46.0))
        assert result.core_frobenius_residual == pytest.approx(math.sqrt(5.0))
        assert result.exterior_frobenius_residual == 3.0
        assert result.core_exterior_frobenius_residual == pytest.approx(math.sqrt(32.0))
        assert result.shell_row_frobenius_residuals == pytest.approx(
            (math.sqrt(17.0), 2.0, 5.0)
        )
