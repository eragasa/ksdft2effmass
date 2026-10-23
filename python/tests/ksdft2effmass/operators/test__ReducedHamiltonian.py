"""Software verification for a reduced Hamiltonian representation."""

from __future__ import annotations

import numpy as np
import pytest

from ksdft2effmass.linalg import (
    MatrixVerifier,
    RealMatrixQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.operators import (
    Hamiltonian,
    OrthogonalSpectralSubspace,
    ReducedHamiltonian,
    SpectralSubspace,
)

pytestmark = pytest.mark.software_verification


class _ObliqueSpectralSubspace(SpectralSubspace):
    """Supply a nonorthogonal test double through the abstract boundary."""

    __slots__ = ()

    @property
    def full_dimension(self) -> int:
        return 2

    @property
    def dimension(self) -> int:
        return 1

    def projector(self) -> RealMatrixQuantity:
        return RealMatrixQuantity(
            np.array([[1.0, 1.0], [0.0, 0.0]]),
            Unitless(),
        )


class TestReducedHamiltonian:
    """Own spectral-subspace and representation-shape invariants."""

    @staticmethod
    def subspace() -> OrthogonalSpectralSubspace:
        """Return one three-to-two-dimensional orthogonal spectral subspace."""
        return OrthogonalSpectralSubspace(
            eigenvalues=VectorQuantity(np.array([1.0, 2.0]), Unitless()),
            basis_vectors=RealMatrixQuantity(np.eye(3, 2), Unitless()),
        )

    def test_constructor__compatible_representations__retains_exact_objects(
        self,
    ) -> None:
        subspace = self.subspace()
        matrix = RealMatrixQuantity(np.diag(np.array([1.0, 2.0])), Unitless())
        embedded = Hamiltonian(
            matrix=RealMatrixQuantity(
                subspace.basis_vectors.magnitude
                @ matrix.magnitude
                @ subspace.basis_vectors.magnitude.T,
                Unitless(),
            )
        )

        reduced = ReducedHamiltonian(
            matrix=matrix,
            spectral_subspace=subspace,
            embedded=embedded,
        )

        assert isinstance(reduced, Hamiltonian)
        assert reduced.matrix is matrix
        assert reduced.spectral_subspace is subspace
        assert reduced.embedded is embedded

    def test_constructor__oblique_concrete_subspace__accepts_abstract_boundary(
        self,
    ) -> None:
        reduced = ReducedHamiltonian(
            matrix=RealMatrixQuantity(np.array([[2.0]]), Unitless()),
            spectral_subspace=_ObliqueSpectralSubspace(),
            embedded=Hamiltonian(
                matrix=RealMatrixQuantity(
                    np.array([[2.0, 2.0], [0.0, 0.0]]),
                    Unitless(),
                )
            ),
        )

        assert not MatrixVerifier(reduced.spectral_subspace.projector()).is_hermitian()

    def test_constructor__matrix_shape_mismatch__rejects(self) -> None:
        subspace = self.subspace()

        with pytest.raises(ValueError, match="spectral subspace dimension"):
            ReducedHamiltonian(
                matrix=RealMatrixQuantity(np.eye(3), Unitless()),
                spectral_subspace=subspace,
                embedded=Hamiltonian(matrix=RealMatrixQuantity(np.eye(3), Unitless())),
            )
