r"""Software verification of ``ComplexHermitianEigensolverResult``.

Evidence profile: routine

Bounded artifact scope: correlation of one sparse solve request with retained
complex-Hermitian eigenpair residuals.

Facet and represented meaning

The ResultObject keeps selection count and residual acceptance tolerance tied to the
request that produced the selected eigenpairs.

Intrinsic and cross-object scope

Count mismatch rejection is included for a synthetic sparse solve.

VVUQ and scientific exclusions

This does not establish independent numerical verification, scientific validation,
UQ, campaign execution, or human acceptance.
"""

from dataclasses import replace

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.operators import (
    ComplexHermitianEigensolverRequest,
    ComplexHermitianEigensolverResult,
    ComplexHermitianSparseEigenpairSolver,
    ComplexSparseHermiticityAnalyzer,
    ComplexSparseMatrixQuantity,
    Unitless,
)

pytestmark = pytest.mark.software_verification
SUT = ComplexHermitianEigensolverResult


class TestComplexHermitianEigensolverResult:
    """Own software evidence for sparse eigensolver result correlation."""

    def test_constructor__request__must_match_retained_selection(self) -> None:
        """Evidence ID: SV-OPERATORS-COMPLEX-EIGENSOLVER-003

        Requirement: A solve result cannot be rebound to a request with a different
        selected-state count.

        Acceptance: Replacing a valid two-state request by a one-state request raises
        ``ValueError``.
        """
        dense = np.diag(np.array([-2.0, -1.0, 1.0, 2.0], dtype=np.complex128))
        operator = ComplexSparseMatrixQuantity.from_csr(
            sparse.csr_array(dense), Unitless()
        )
        hermiticity = ComplexSparseHermiticityAnalyzer().execute(
            operator, absolute_tolerance=0.0
        )
        result = ComplexHermitianSparseEigenpairSolver().execute(
            operator,
            hermiticity,
            ComplexHermitianEigensolverRequest(2, 0.0, 500, 0, 1.0e-10),
        )

        with pytest.raises(ValueError, match="selected eigenpair count"):
            replace(
                result,
                request=ComplexHermitianEigensolverRequest(1, 0.0, 500, 0, 1.0e-10),
            )
