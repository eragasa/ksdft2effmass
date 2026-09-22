r"""Software verification of ``ComplexHermitianEigenpairResidualResult``.

Evidence profile: routine

Bounded artifact scope: immutable per-vector and maximum algebraic residual metrics.

Facet and represented meaning

The ResultObject correlates one residual with each selected eigenpair and requires the
retained maximum to agree exactly.

Intrinsic and cross-object scope

An exact diagonal eigenpair and contradictory maximum replacement are included.

VVUQ and scientific exclusions

This is software record evidence; algebraic residuals do not establish scientific
accuracy, UQ, campaign execution, or human acceptance.
"""

from dataclasses import replace

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.operators import (
    ComplexHermitianEigenpairResidualAnalyzer,
    ComplexHermitianEigenpairResidualResult,
    ComplexHermitianEigenpairResult,
    ComplexMatrixQuantity,
    ComplexSparseHermiticityAnalyzer,
    ComplexSparseMatrixQuantity,
    HermitianEigenpairSelection,
    Unitless,
    VectorQuantity,
)

pytestmark = pytest.mark.software_verification
SUT = ComplexHermitianEigenpairResidualResult


class TestComplexHermitianEigenpairResidualResult:
    """Own software evidence for eigenpair residual result consistency."""

    def test_constructor__maximum_residual__must_equal_per_pair_maximum(self) -> None:
        """Evidence ID: SV-OPERATORS-COMPLEX-EIGENPAIR-RESIDUAL-002

        Requirement: The aggregate maximum is derived from all retained pair residuals.

        Acceptance: One exact diagonal eigenpair has zero residual; replacing only its
        maximum by one raises ``ValueError``.
        """
        operator = ComplexSparseMatrixQuantity.from_csr(
            sparse.csr_array([[-2.0 + 0.0j]]), Unitless()
        )
        eigenpairs = ComplexHermitianEigenpairResult(
            operator,
            ComplexSparseHermiticityAnalyzer().execute(
                operator, absolute_tolerance=0.0
            ),
            VectorQuantity(np.array([-2.0]), Unitless()),
            ComplexMatrixQuantity(np.array([[1.0 + 0.0j]]), Unitless()),
            HermitianEigenpairSelection.LOWEST,
        )
        result = ComplexHermitianEigenpairResidualAnalyzer().execute(
            eigenpairs, absolute_tolerance=0.0
        )

        assert result.maximum_residual == 0.0
        with pytest.raises(ValueError, match="retained residual maximum"):
            replace(result, maximum_residual=1.0)
