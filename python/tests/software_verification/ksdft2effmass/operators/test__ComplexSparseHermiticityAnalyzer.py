r"""Software verification of ``ComplexSparseHermiticityAnalyzer``.

Evidence profile: routine

Bounded artifact scope: nondensifying fixed-representation Hermiticity analysis for
complex CSR quantities.

Facet and represented meaning

The ActionObject computes the maximum entrywise ``abs(H - H.conjugate().T)`` residual
under an inclusive caller tolerance.

Intrinsic and cross-object scope

Exact Hermiticity, a hand-derived nonzero residual, inclusive acceptance, and square
shape requirements are included.

VVUQ and scientific exclusions

This verifies represented software behavior, not physical Hermiticity, scientific
validation, uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.operators import (
    ComplexSparseHermiticityAnalyzer,
    ComplexSparseMatrixQuantity,
    Unitless,
)

pytestmark = pytest.mark.software_verification
SUT = ComplexSparseHermiticityAnalyzer


class TestComplexSparseHermiticityAnalyzer:
    """Own software evidence for ``ComplexSparseHermiticityAnalyzer``."""

    def test_method__execute__computes_hand_derived_sparse_residual(self) -> None:
        """Evidence ID: SV-OPERATORS-COMPLEX-SPARSE-HERMITICITY-001

        Requirement: The action computes the declared maximum residual directly from
        sparse complex entries.

        Acceptance: An exactly Hermitian matrix has residual zero; changing one lower
        entry by ``0.5j`` produces residual ``0.5``.
        """
        hermitian = ComplexSparseMatrixQuantity.from_csr(
            sparse.csr_array(np.array([[1.0, 2.0 + 1.0j], [2.0 - 1.0j, 3.0]])),
            Unitless(),
        )
        nonhermitian = ComplexSparseMatrixQuantity.from_csr(
            sparse.csr_array(np.array([[1.0, 2.0 + 1.0j], [2.0 - 0.5j, 3.0]])),
            Unitless(),
        )
        analyzer = ComplexSparseHermiticityAnalyzer()

        exact = analyzer.execute(hermitian, absolute_tolerance=0.0)
        residual = analyzer.execute(nonhermitian, absolute_tolerance=0.5)

        assert exact.maximum_absolute_residual == 0.0
        assert exact.is_hermitian
        assert residual.maximum_absolute_residual == 0.5
        assert residual.is_hermitian

    def test_method__execute__rejects_nonsquare_quantity(self) -> None:
        """Evidence ID: SV-OPERATORS-COMPLEX-SPARSE-HERMITICITY-002

        Requirement: Hermiticity analysis requires equal domain and codomain dimension.

        Acceptance: A one-by-two sparse quantity raises ``ValueError``.
        """
        matrix = ComplexSparseMatrixQuantity.from_csr(
            sparse.csr_array(np.array([[1.0 + 0.0j, 2.0 + 0.0j]])), Unitless()
        )

        with pytest.raises(ValueError, match="square matrix"):
            ComplexSparseHermiticityAnalyzer().execute(matrix, absolute_tolerance=0.0)
