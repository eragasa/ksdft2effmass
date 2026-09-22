r"""Software verification of ``ComplexHermitianEigenpairResidualAnalyzer``.

Evidence profile: routine

Bounded artifact scope: sparse-matrix algebraic residuals for retained selected complex
vectors.

Facet and represented meaning

The ActionObject computes ``||H v - lambda v||_2`` without densifying the represented
operator.

Intrinsic and cross-object scope

Rotated orthonormal vectors for a diagonal operator provide a hand-derived nonzero
residual oracle.

VVUQ and scientific exclusions

Inputs are synthetic test data. Algebraic residuals do not establish continuum or
scientific accuracy, UQ, campaign execution, or human acceptance.
"""

import math

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.operators import (
    ComplexHermitianEigenpairResidualAnalyzer,
    ComplexHermitianEigenpairResult,
    ComplexMatrixQuantity,
    ComplexSparseHermiticityAnalyzer,
    ComplexSparseMatrixQuantity,
    HermitianEigenpairSelection,
    Unitless,
    VectorQuantity,
)

pytestmark = pytest.mark.software_verification
SUT = ComplexHermitianEigenpairResidualAnalyzer


class TestComplexHermitianEigenpairResidualAnalyzer:
    """Own software evidence for sparse complex eigenpair residuals."""

    def test_method__execute__matches_rotated_two_state_residual(self) -> None:
        """Evidence ID: SV-OPERATORS-COMPLEX-EIGENPAIR-RESIDUAL-001

        Requirement: Residual norms use sparse operator multiplication and retained
        complex selected vectors.

        Acceptance: A 45-degree rotation of eigenvectors for diagonal values -2 and -1
        gives residual ``1/sqrt(2)`` for each assigned eigenvalue.
        """
        scale = 1.0 / math.sqrt(2.0)
        operator = ComplexSparseMatrixQuantity.from_csr(
            sparse.diags([-2.0, -1.0, 1.0], format="csr"), Unitless()
        )
        eigenpairs = ComplexHermitianEigenpairResult(
            operator,
            ComplexSparseHermiticityAnalyzer().execute(
                operator, absolute_tolerance=0.0
            ),
            VectorQuantity(np.array([-2.0, -1.0]), Unitless()),
            ComplexMatrixQuantity(
                np.array(
                    [[scale, -scale], [scale, scale], [0.0, 0.0]],
                    dtype=np.complex128,
                ),
                Unitless(),
            ),
            HermitianEigenpairSelection.LOWEST,
        )

        result = ComplexHermitianEigenpairResidualAnalyzer().execute(
            eigenpairs, absolute_tolerance=1.0
        )

        assert result.residuals == pytest.approx((scale, scale))
        assert result.maximum_residual == pytest.approx(scale)
        assert result.passes
