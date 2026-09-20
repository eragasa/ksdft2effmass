r"""Software verification of ``RealSymmetricEigenpairSolver``.

Evidence profile: routine

Bounded artifact scope: public deterministic finite real-symmetric eigensolver.

Facet and represented meaning

The ActionObject uses a dense, tridiagonal, or iterative sparse eigensolver without
materializing a sparse input as a dense operator and retains ordered eigenpairs.

Intrinsic and cross-object scope

Symmetry admission, ordering, units, and reconstruction are included.

VVUQ and scientific exclusions

This verifies a finite software operation, not an independent eigensolver error bound,
scientific validation, uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.operators import (
    MatrixQuantity,
    RealSymmetricEigenpairSolver,
    SparseMatrixQuantity,
    Unitless,
)

pytestmark = pytest.mark.software_verification
SUT = RealSymmetricEigenpairSolver


class TestRealSymmetricEigenpairSolver:
    """Own software evidence for ``RealSymmetricEigenpairSolver``."""

    def test_method__execute__returns_ordered_reconstructing_eigenpairs(self) -> None:
        """Evidence ID: SV-OPERATORS-EIGENPAIR-002

        Requirement: Execution returns ascending eigenvalues and orthonormal column
        eigenvectors for one exact real-symmetric matrix.

        Acceptance: The two-dimensional result reconstructs the input to binary64
        tolerance and a nonsymmetric input is rejected.
        """
        operator = MatrixQuantity(np.array([[2.0, -1.0], [-1.0, 2.0]]), Unitless())
        result = RealSymmetricEigenpairSolver().execute(operator)

        np.testing.assert_allclose(result.eigenvalues.magnitude, [1.0, 3.0])
        np.testing.assert_allclose(
            result.eigenvectors.magnitude
            @ np.diag(result.eigenvalues.magnitude)
            @ result.eigenvectors.magnitude.T,
            operator.magnitude,
            atol=8.0 * np.finfo(np.float64).eps,
        )
        with pytest.raises(ValueError, match="exactly real symmetric"):
            RealSymmetricEigenpairSolver().execute(
                MatrixQuantity(np.array([[1.0, 1.0], [0.0, 1.0]]), Unitless())
            )

    def test_method__execute__solves_sparse_tridiagonal_without_densifying(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Evidence ID: SV-OPERATORS-EIGENPAIR-003

        Requirement: A complete sparse tridiagonal eigensystem uses its diagonals
        directly and never converts the represented operator to a dense matrix.

        Acceptance: A three-point tridiagonal operator reconstructs to tolerance even
        when the sparse quantity's explicit dense-conversion method is forbidden.
        """
        operator = SparseMatrixQuantity.from_csr(
            sparse.diags(
                ([-1.0, -1.0], [2.0, 2.0, 2.0], [-1.0, -1.0]),
                offsets=(-1, 0, 1),
                format="csr",
            ),
            Unitless(),
        )

        monkeypatch.setattr(
            SparseMatrixQuantity, "to_dense", self.reject_dense_conversion
        )
        result = RealSymmetricEigenpairSolver().execute(operator)

        reconstructed = (
            result.eigenvectors.magnitude
            @ np.diag(result.eigenvalues.magnitude)
            @ result.eigenvectors.magnitude.T
        )
        np.testing.assert_allclose(
            reconstructed,
            operator.to_csr().toarray(),
            atol=16.0 * np.finfo(np.float64).eps,
        )

    def test_method__execute_lowest__uses_iterative_sparse_selection(self) -> None:
        """Evidence ID: SV-OPERATORS-EIGENPAIR-004

        Requirement: A proper subset of a sparse symmetric spectrum uses an iterative
        sparse solver rather than complete dense diagonalization.

        Acceptance: Selecting two states from a four-state diagonal operator returns
        the two lowest ordered eigenvalues and a four-by-two eigenvector matrix.
        """
        operator = SparseMatrixQuantity.from_csr(
            sparse.diags([4.0, 1.0, 3.0, 2.0], offsets=0, format="csr"),
            Unitless(),
        )

        result = RealSymmetricEigenpairSolver().execute_lowest(operator, 2)

        np.testing.assert_allclose(result.eigenvalues.magnitude, [1.0, 2.0])
        assert result.eigenvectors.magnitude.shape == (4, 2)

    def test_method__execute__rejects_complete_nontridiagonal_sparse_spectrum(
        self,
    ) -> None:
        """Evidence ID: SV-OPERATORS-EIGENPAIR-005

        Requirement: Complete sparse solution must not silently densify a general
        sparse operator for which no supported structure-specific solver exists.

        Acceptance: A symmetric matrix with a second off-diagonal is rejected with an
        explicit tridiagonal-contract error.
        """
        operator = SparseMatrixQuantity.from_csr(
            sparse.csr_array(
                np.array([[2.0, -1.0, 0.5], [-1.0, 2.0, -1.0], [0.5, -1.0, 2.0]])
            ),
            Unitless(),
        )

        with pytest.raises(ValueError, match="tridiagonal"):
            RealSymmetricEigenpairSolver().execute(operator)

    @staticmethod
    def reject_dense_conversion(
        quantity: SparseMatrixQuantity,
    ) -> MatrixQuantity:
        """Reject any attempted sparse-to-dense conversion during a solver test."""
        del quantity
        raise AssertionError("sparse eigensolver must not materialize dense input")
