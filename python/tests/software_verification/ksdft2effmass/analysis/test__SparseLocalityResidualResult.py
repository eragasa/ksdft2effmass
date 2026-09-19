r"""Software verification of ``SparseLocalityResidualResult``.

Evidence profile: routine

Bounded artifact scope: immutable correlations and decompositions for sparse locality
residual metrics.

Facet and represented meaning

The ResultObject requires global Frobenius magnitude to agree, within binary64
representational allowance, with both block and row-shell decompositions.

Intrinsic and cross-object scope

A one-site zero result and contradictory edited global residual are included.

VVUQ and scientific exclusions

This is software record evidence, not a physical locality claim, validation, UQ,
campaign execution, or human acceptance.
"""

from dataclasses import replace

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.analysis.finite_domain_locality import (
    MinimumImageChebyshevPartitioner,
    SparseLocalityResidualAnalyzer,
    SparseLocalityResidualResult,
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
SUT = SparseLocalityResidualResult


class TestSparseLocalityResidualResult:
    """Own software evidence for locality residual ResultObject consistency."""

    def test_constructor__frobenius_decomposition__rejects_contradictory_metrics(
        self,
    ) -> None:
        """Evidence ID: SV-ANALYSIS-SPARSE-LOCALITY-RESULT-001

        Requirement: Global, block, and shell Frobenius values describe one residual.

        Acceptance: Equal one-site zero operators produce a zero result; replacing only
        the global Frobenius value by one raises ``ValueError``.
        """
        shape = FiniteLatticeShape(LatticeDimension.ONE, (1,))
        fiber = TwistFiber(
            BoundaryTwistReducer().execute(
                BoundaryTwistLift(LatticeDimension.ONE, (0.0,))
            ),
            TwistGaugeRepresentation.CENTERED_UNIFORM_LINK,
        )
        matrix = ComplexSparseMatrixQuantity.from_csr(
            sparse.csr_array((1, 1), dtype=np.complex128), Unitless()
        )
        reference = ScalarFiniteLatticeOperator(
            "reference", matrix, shape, fiber, "basis", "zero", ()
        )
        candidate = ScalarFiniteLatticeOperator(
            "candidate", matrix, shape, fiber, "basis", "zero", ()
        )
        result = SparseLocalityResidualAnalyzer().execute(
            reference,
            candidate,
            ScalarFiniteLatticeOperatorCompatibilityAnalyzer().execute(
                reference, candidate
            ),
            MinimumImageChebyshevPartitioner().execute(
                shape,
                LatticeCoordinate(LatticeDimension.ONE, (0,)),
                core_radius=0,
            ),
        )

        assert result.frobenius_residual == 0.0
        with pytest.raises(ValueError, match="block residuals"):
            replace(result, frobenius_residual=1.0)
