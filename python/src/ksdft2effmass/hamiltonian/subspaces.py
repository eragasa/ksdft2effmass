"""Hamiltonian spectral-subspace representations and selection."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
from projectkoios.physkit.linalg.eigen import Eigensystem
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    MatrixQuantity,
    Unitless,
    VectorQuantity,
)

type CoordinateMap = MatrixQuantity | ComplexMatrixQuantity


class SpectralSubspace(ABC):
    """Define coordinate maps for one represented Hamiltonian spectral subspace."""

    @property
    @abstractmethod
    def full_dimension(self) -> int:
        """Return the positive parent-space dimension."""

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Return the positive reduced-space dimension."""

    @property
    @abstractmethod
    def reduction_map(self) -> CoordinateMap:
        """Return the map from parent coordinates to reduced coordinates."""

    @property
    @abstractmethod
    def embedding_map(self) -> CoordinateMap:
        """Return the map from reduced coordinates to parent coordinates."""

    @property
    @abstractmethod
    def projector(self) -> CoordinateMap:
        """Return embedding followed by reduction in parent coordinates."""


@dataclass(frozen=True, slots=True, eq=False)
class OrthogonalSpectralSubspace(SpectralSubspace):
    r"""Retain selected real eigenvalues and an orthonormal column embedding.

    Parameters
    ----------
    eigenvalues
        Selected real eigenvalues with one entry per basis column.
    basis_vectors
        Unitless ``N`` by ``M`` real matrix whose columns form an orthonormal
        spectral-subspace basis $\Phi_M$.

    Raises
    ------
    TypeError
        If either field has the wrong quantity type.
    ValueError
        If units, dimensions, or numerical orthonormality fail the concrete
        contract.
    """

    eigenvalues: VectorQuantity
    basis_vectors: MatrixQuantity

    def __post_init__(self) -> None:
        if not isinstance(self.eigenvalues, VectorQuantity):
            raise TypeError("eigenvalues must be VectorQuantity")
        if not isinstance(self.basis_vectors, MatrixQuantity):
            raise TypeError("basis_vectors must be MatrixQuantity")
        if not isinstance(self.basis_vectors.unit, Unitless):
            raise ValueError("basis_vectors must be Unitless")
        rows, columns = self.basis_vectors.magnitude.shape
        if rows <= 0 or columns <= 0 or columns > rows:
            raise ValueError("basis_vectors must have shape N by M with 1 <= M <= N")
        if self.eigenvalues.magnitude.shape != (columns,):
            raise ValueError("eigenvalues must match the retained dimension")
        gram = self.basis_vectors.magnitude.T @ self.basis_vectors.magnitude
        tolerance = 128.0 * np.finfo(np.float64).eps * max(rows, columns)
        if not np.allclose(gram, np.eye(columns), rtol=0.0, atol=tolerance):
            raise ValueError(
                "basis_vectors must be orthonormal within binary64 tolerance"
            )

    @property
    def full_dimension(self) -> int:
        """Return the represented full-space dimension."""
        return int(self.basis_vectors.magnitude.shape[0])

    @property
    def dimension(self) -> int:
        """Return the spectral-subspace dimension."""
        return int(self.basis_vectors.magnitude.shape[1])

    @property
    def retained_dimension(self) -> int:
        """Return the selected dimension using the established selector vocabulary."""
        return self.dimension

    @property
    def reduction_map(self) -> MatrixQuantity:
        r"""Return $\Phi_M^{\mathsf T}$ from parent to retained coordinates."""
        return MatrixQuantity(self.basis_vectors.magnitude.T, Unitless())

    @property
    def embedding_map(self) -> MatrixQuantity:
        r"""Return $\Phi_M$ from retained to parent coordinates."""
        return self.basis_vectors

    @property
    def projector(self) -> MatrixQuantity:
        r"""Return $P_M=\Phi_M\Phi_M^{\mathsf T}$."""
        return MatrixQuantity(
            self.embedding_map.magnitude @ self.reduction_map.magnitude,
            Unitless(),
        )

    @property
    def complement_projector(self) -> MatrixQuantity:
        """Return the complementary orthogonal projector $I-P_M$."""
        return MatrixQuantity(
            np.eye(self.full_dimension) - self.projector.magnitude,
            Unitless(),
        )


class OrthogonalSpectralSubspaceSelector:
    """Select the lowest ordered eigenpairs as one orthogonal spectral subspace."""

    __slots__ = ()

    def execute(
        self, eigensystem: Eigensystem, retained_dimension: int
    ) -> OrthogonalSpectralSubspace:
        """Return the first ``retained_dimension`` ordered real eigenpairs."""
        if not isinstance(eigensystem, Eigensystem):
            raise TypeError("eigensystem must be Eigensystem")
        if not isinstance(eigensystem.eigenvectors, MatrixQuantity):
            raise TypeError("eigensystem eigenvectors must be real")
        if type(retained_dimension) is not int:
            raise TypeError("retained_dimension must be a built-in int")
        available = eigensystem.n_rank
        if retained_dimension <= 0 or retained_dimension > available:
            raise ValueError("retained_dimension must select available eigenpairs")
        return OrthogonalSpectralSubspace(
            eigenvalues=VectorQuantity(
                eigensystem.eigenvalues.magnitude[:retained_dimension],
                eigensystem.eigenvalues.unit,
            ),
            basis_vectors=MatrixQuantity(
                eigensystem.eigenvectors.magnitude[:, :retained_dimension], Unitless()
            ),
        )
