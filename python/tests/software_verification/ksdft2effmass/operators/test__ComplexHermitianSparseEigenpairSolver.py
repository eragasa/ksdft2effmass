r"""Software verification of ``ComplexHermitianSparseEigenpairSolver``.

Evidence profile: routine

Bounded artifact scope: iterative lowest-state solution of canonical complex sparse
Hermitian matrices.

Facet and represented meaning

The ActionObject uses sparse ``eigsh``, ordered selected values, phase-canonicalized
vectors, and independently evaluated algebraic residuals.

Intrinsic and cross-object scope

Sparse preservation, Hermiticity admission, subset selection, and residual acceptance
are included for synthetic data.

VVUQ and scientific exclusions

This checks a software contract against NumPy on a tiny synthetic matrix. It is not
material validation, UQ, campaign execution, or human acceptance.
"""

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.operators import (
    ComplexHermitianEigensolverRequest,
    ComplexHermitianSparseEigenpairSolver,
    ComplexMatrixQuantity,
    ComplexSparseHermiticityAnalyzer,
    ComplexSparseMatrixQuantity,
    Unitless,
)

pytestmark = pytest.mark.software_verification
SUT = ComplexHermitianSparseEigenpairSolver


class TestComplexHermitianSparseEigenpairSolver:
    """Own software evidence for the complex sparse eigensolver boundary."""

    def test_method__execute__selects_lowest_without_dense_conversion(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Evidence ID: SV-OPERATORS-COMPLEX-EIGENSOLVER-002

        Requirement: Proper lowest-state selection preserves the sparse operator and
        retains passing independently evaluated residuals.

        Acceptance: Two lowest values match NumPy for a four-state Hermitian matrix,
        residuals pass, and forbidding the explicit dense boundary does not interfere.
        """
        dense = np.array(
            [
                [0.0, 1.0j, 0.0, 0.0],
                [-1.0j, 1.0, 0.0, 0.0],
                [0.0, 0.0, 2.0, 0.5j],
                [0.0, 0.0, -0.5j, 3.0],
            ],
            dtype=np.complex128,
        )
        operator = ComplexSparseMatrixQuantity.from_csr(
            sparse.csr_array(dense), Unitless()
        )
        hermiticity = ComplexSparseHermiticityAnalyzer().execute(
            operator, absolute_tolerance=0.0
        )
        monkeypatch.setattr(
            ComplexSparseMatrixQuantity, "to_dense", self.reject_dense_conversion
        )

        result = ComplexHermitianSparseEigenpairSolver().execute(
            operator,
            hermiticity,
            ComplexHermitianEigensolverRequest(2, 0.0, 500, 0, 1.0e-10),
        )

        np.testing.assert_allclose(
            result.eigenpairs.eigenvalues.magnitude,
            np.linalg.eigvalsh(dense)[:2],
            rtol=0.0,
            atol=1.0e-12,
        )
        assert result.passes
        assert result.eigenpairs.eigenvectors.magnitude.shape == (4, 2)
        with pytest.raises(ValueError, match="proper spectral subset"):
            ComplexHermitianSparseEigenpairSolver().execute(
                operator,
                hermiticity,
                ComplexHermitianEigensolverRequest(4, 0.0, 500, 0, 1.0e-10),
            )

    @staticmethod
    def reject_dense_conversion(
        quantity: ComplexSparseMatrixQuantity,
    ) -> ComplexMatrixQuantity:
        """Reject explicit sparse-to-dense conversion during solver execution."""
        del quantity
        raise AssertionError("complex sparse eigensolver must not materialize input")
