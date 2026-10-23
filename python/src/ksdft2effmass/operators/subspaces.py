"""Public spectral-subspace selection and operator compression."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np

from ksdft2effmass.linalg import (
    ComplexMatrixQuantity,
    CsrRealMatrixQuantity,
    RealMatrixQuantity,
    Unitless,
    VectorQuantity,
)

from .eigenpairs import RealSymmetricEigenpairResult, RealSymmetricOperator


class SpectralSubspace(ABC):
    """Define the common boundary for represented spectral subspaces.

    Notes
    -----
    Implementations must declare parent and subspace dimensions and materialize
    their represented spectral projector. The abstract contract does not require
    that projector to be orthogonal.
    """

    @property
    @abstractmethod
    def full_dimension(self) -> int:
        """Return the parent-space dimension.

        Returns
        -------
        int
            Positive parent-space dimension.
        """

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Return the spectral-subspace dimension.

        Returns
        -------
        int
            Positive subspace dimension not exceeding the parent dimension.
        """

    @abstractmethod
    def projector(self) -> RealMatrixQuantity | ComplexMatrixQuantity:
        """Return the represented spectral projector.

        Returns
        -------
        RealMatrixQuantity or ComplexMatrixQuantity
            Full-dimensional projector supplied by the concrete representation.
        """


@dataclass(frozen=True, slots=True, eq=False)
class OrthogonalSpectralSubspace(SpectralSubspace):
    """Retain selected real eigenvalues and an orthonormal column embedding.

    Parameters
    ----------
    eigenvalues
        Selected real eigenvalues with one entry per basis column.
    basis_vectors
        Unitless ``N`` by ``M`` real matrix whose columns form an orthonormal
        spectral-subspace basis.

    Raises
    ------
    TypeError
        If either field has the wrong quantity type.
    ValueError
        If units, dimensions, or numerical orthonormality fail the concrete
        contract.
    """

    eigenvalues: VectorQuantity
    basis_vectors: RealMatrixQuantity

    def __post_init__(self) -> None:
        if not isinstance(self.eigenvalues, VectorQuantity):
            raise TypeError("eigenvalues must be VectorQuantity")
        if not isinstance(self.basis_vectors, RealMatrixQuantity):
            raise TypeError("basis_vectors must be RealMatrixQuantity")
        if not isinstance(self.basis_vectors.unit, Unitless):
            raise ValueError("basis_vectors must be Unitless")
        rows, columns = self.basis_vectors.magnitude.shape
        if rows <= 0 or columns <= 0 or columns > rows:
            raise ValueError("basis_vectors must have shape N by K with 1 <= K <= N")
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

    def projector(self) -> RealMatrixQuantity:
        """Materialize the full-space orthogonal projector."""
        vectors = self.basis_vectors.magnitude
        return RealMatrixQuantity(vectors @ vectors.T, Unitless())

    def complement_projector(self) -> RealMatrixQuantity:
        """Materialize the complementary full-space orthogonal projector."""
        projector = self.projector().magnitude
        return RealMatrixQuantity(np.eye(self.full_dimension) - projector, Unitless())


class OrthogonalSpectralSubspaceSelector:
    """Select the lowest ordered eigenpairs as one orthogonal spectral subspace."""

    __slots__ = ()

    def execute(
        self, eigenpairs: RealSymmetricEigenpairResult, retained_dimension: int
    ) -> OrthogonalSpectralSubspace:
        """Return the first ``retained_dimension`` ordered eigenpairs."""
        if not isinstance(eigenpairs, RealSymmetricEigenpairResult):
            raise TypeError("eigenpairs must be RealSymmetricEigenpairResult")
        if type(retained_dimension) is not int:
            raise TypeError("retained_dimension must be a built-in int")
        available = eigenpairs.eigenvalues.magnitude.size
        if retained_dimension <= 0 or retained_dimension > available:
            raise ValueError("retained_dimension must select available eigenpairs")
        return OrthogonalSpectralSubspace(
            eigenvalues=VectorQuantity(
                eigenpairs.eigenvalues.magnitude[:retained_dimension],
                eigenpairs.eigenvalues.unit,
            ),
            basis_vectors=RealMatrixQuantity(
                eigenpairs.eigenvectors.magnitude[:, :retained_dimension], Unitless()
            ),
        )


@dataclass(frozen=True, slots=True, eq=False)
class OperatorCompressionResult:
    """Retain one operator in subspace coordinates and embedded full coordinates."""

    operator: RealSymmetricOperator
    subspace: OrthogonalSpectralSubspace
    coordinates: RealMatrixQuantity
    embedded: RealMatrixQuantity

    def __post_init__(self) -> None:
        if not isinstance(self.operator, RealMatrixQuantity | CsrRealMatrixQuantity):
            raise TypeError("operator must be a dense or sparse matrix quantity")
        if not isinstance(self.subspace, OrthogonalSpectralSubspace):
            raise TypeError("subspace must be OrthogonalSpectralSubspace")
        if not isinstance(self.coordinates, RealMatrixQuantity):
            raise TypeError("coordinates must be RealMatrixQuantity")
        if not isinstance(self.embedded, RealMatrixQuantity):
            raise TypeError("embedded must be RealMatrixQuantity")
        retained = self.subspace.dimension
        full = self.subspace.full_dimension
        if self.coordinates.magnitude.shape != (retained, retained):
            raise ValueError("coordinates must match the retained dimension")
        if self.embedded.magnitude.shape != (full, full):
            raise ValueError("embedded must match the full dimension")
        if self.coordinates.unit != self.embedded.unit:
            raise ValueError("coordinate and embedded units must agree exactly")


class OperatorCompression:
    """Compress one represented operator through an orthogonal subspace embedding."""

    __slots__ = ()

    def execute(
        self, operator: RealSymmetricOperator, subspace: OrthogonalSpectralSubspace
    ) -> OperatorCompressionResult:
        """Return ``Q.T @ H @ Q`` and ``Q @ (Q.T @ H @ Q) @ Q.T``."""
        if not isinstance(operator, RealMatrixQuantity | CsrRealMatrixQuantity):
            raise TypeError("operator must be a dense or sparse matrix quantity")
        if not isinstance(subspace, OrthogonalSpectralSubspace):
            raise TypeError("subspace must be OrthogonalSpectralSubspace")
        shape = (
            operator.magnitude.shape
            if isinstance(operator, RealMatrixQuantity)
            else operator.shape
        )
        if shape != (subspace.full_dimension, subspace.full_dimension):
            raise ValueError("operator and subspace full dimensions must agree")
        vectors = subspace.basis_vectors.magnitude
        dense = (
            operator.magnitude
            if isinstance(operator, RealMatrixQuantity)
            else operator.to_dense().magnitude
        )
        projector = subspace.projector().magnitude
        coordinates = vectors.T @ dense @ vectors
        embedded = projector @ dense @ projector
        return OperatorCompressionResult(
            operator=operator,
            subspace=subspace,
            coordinates=RealMatrixQuantity(coordinates, operator.unit),
            embedded=RealMatrixQuantity(embedded, operator.unit),
        )
