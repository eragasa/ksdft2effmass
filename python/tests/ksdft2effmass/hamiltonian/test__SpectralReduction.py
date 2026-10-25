"""Software verification of reusable Hamiltonian spectral reduction."""

from __future__ import annotations

import numpy as np
import pytest
from projectkoios.physkit.linalg.eigen import SpectralDecomposition
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    MatrixQuantity,
    SparseMatrixQuantity,
    Unitless,
)
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.hamiltonian import (
    Hamiltonian,
    OrthogonalSpectralSubspace,
    OrthogonalSpectralSubspaceSelector,
    SpectralReduction,
    SpectralSubspace,
)

pytestmark = pytest.mark.software_verification
SUT = SpectralReduction


class _ObliqueSpectralSubspace(SpectralSubspace):
    """Supply explicit oblique reduction and embedding maps."""

    __slots__ = ()

    @property
    def full_dimension(self) -> int:
        return 2

    @property
    def dimension(self) -> int:
        return 1

    @property
    def reduction_map(self) -> MatrixQuantity:
        return MatrixQuantity(np.array([[1.0, 1.0]]), Unitless())

    @property
    def embedding_map(self) -> MatrixQuantity:
        return MatrixQuantity(np.array([[1.0], [0.0]]), Unitless())

    @property
    def projector(self) -> MatrixQuantity:
        return MatrixQuantity(
            self.embedding_map.magnitude @ self.reduction_map.magnitude,
            Unitless(),
        )


class TestSpectralReduction:
    """Own the coordinate-reduction and embedding behavior."""

    def test_property__reduced_hamiltonian__retains_one_eager_correlated_result(
        self,
    ) -> None:
        """Sparse parent input is reduced and embedded through one exact subspace."""
        matrix = SparseMatrixQuantity.from_csr(
            sparse.diags([1.0, 2.0, 3.0], offsets=0, format="csr"), Unitless()
        )
        subspace = OrthogonalSpectralSubspaceSelector().execute(
            SpectralDecomposition(matrix).eigensystem(), 2
        )
        hamiltonian = Hamiltonian(matrix=matrix)

        reduction = SUT(
            hamiltonian=hamiltonian,
            spectral_subspace=subspace,
        )
        result = reduction.reduced_hamiltonian

        assert reduction.reduced_hamiltonian is result
        assert result.spectral_subspace is subspace
        assert isinstance(result.matrix, MatrixQuantity)
        assert isinstance(result.embedded.matrix, MatrixQuantity)
        np.testing.assert_array_equal(result.matrix.magnitude, np.diag([1.0, 2.0]))
        np.testing.assert_array_equal(
            result.embedded.matrix.magnitude, np.diag([1.0, 2.0, 0.0])
        )

    def test_reduction__complex_parent__preserves_complex_representation(self) -> None:
        """A real orthogonal basis may reduce a complex Hamiltonian."""
        subspace = OrthogonalSpectralSubspace(
            eigenvalues=SpectralDecomposition(
                MatrixQuantity(np.diag([1.0, 2.0]), Unitless())
            )
            .eigensystem()
            .eigenvalues,
            basis_vectors=MatrixQuantity(np.eye(2), Unitless()),
        )
        matrix = ComplexMatrixQuantity(
            np.array([[1.0, 1.0j], [-1.0j, 2.0]], dtype=np.complex128),
            Unitless(),
        )

        result = SUT(
            hamiltonian=Hamiltonian(matrix=matrix),
            spectral_subspace=subspace,
        ).reduced_hamiltonian

        assert isinstance(result.matrix, ComplexMatrixQuantity)
        np.testing.assert_array_equal(result.matrix.magnitude, matrix.magnitude)

    def test_reduction__oblique_subspace__uses_explicit_coordinate_maps(self) -> None:
        """A general subspace defines coordinates separately from its projector."""
        subspace = _ObliqueSpectralSubspace()
        matrix = MatrixQuantity(np.diag([2.0, 3.0]), Unitless())

        result = SUT(
            hamiltonian=Hamiltonian(matrix=matrix),
            spectral_subspace=subspace,
        ).reduced_hamiltonian

        np.testing.assert_array_equal(result.matrix.magnitude, np.array([[2.0]]))
        np.testing.assert_array_equal(
            result.embedded.matrix.magnitude,
            np.array([[2.0, 2.0], [0.0, 0.0]]),
        )
