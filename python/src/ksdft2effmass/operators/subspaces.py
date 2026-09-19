"""Public orthogonal spectral-subspace selection and operator compression."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .eigenpairs import RealSymmetricEigenpairResult, RealSymmetricOperator
from .quantities import MatrixQuantity, SparseMatrixQuantity, Unitless, VectorQuantity


@dataclass(frozen=True, slots=True, eq=False)
class OrthogonalSpectralSubspace:
    """Retain selected eigenvalues and an orthonormal column embedding."""

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
    def retained_dimension(self) -> int:
        """Return the selected spectral-subspace dimension."""
        return int(self.basis_vectors.magnitude.shape[1])

    def projector(self) -> MatrixQuantity:
        """Materialize the full-space orthogonal projector at an explicit boundary."""
        vectors = self.basis_vectors.magnitude
        return MatrixQuantity(vectors @ vectors.T, Unitless())

    def complement_projector(self) -> MatrixQuantity:
        """Materialize the complementary full-space orthogonal projector."""
        projector = self.projector().magnitude
        return MatrixQuantity(np.eye(self.full_dimension) - projector, Unitless())


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
            basis_vectors=MatrixQuantity(
                eigenpairs.eigenvectors.magnitude[:, :retained_dimension], Unitless()
            ),
        )


@dataclass(frozen=True, slots=True, eq=False)
class OperatorCompressionResult:
    """Retain one operator in subspace coordinates and embedded full coordinates."""

    operator: RealSymmetricOperator
    subspace: OrthogonalSpectralSubspace
    coordinates: MatrixQuantity
    embedded: MatrixQuantity

    def __post_init__(self) -> None:
        if not isinstance(self.operator, MatrixQuantity | SparseMatrixQuantity):
            raise TypeError("operator must be a dense or sparse matrix quantity")
        if not isinstance(self.subspace, OrthogonalSpectralSubspace):
            raise TypeError("subspace must be OrthogonalSpectralSubspace")
        if not isinstance(self.coordinates, MatrixQuantity):
            raise TypeError("coordinates must be MatrixQuantity")
        if not isinstance(self.embedded, MatrixQuantity):
            raise TypeError("embedded must be MatrixQuantity")
        retained = self.subspace.retained_dimension
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
        if not isinstance(operator, MatrixQuantity | SparseMatrixQuantity):
            raise TypeError("operator must be a dense or sparse matrix quantity")
        if not isinstance(subspace, OrthogonalSpectralSubspace):
            raise TypeError("subspace must be OrthogonalSpectralSubspace")
        shape = (
            operator.magnitude.shape
            if isinstance(operator, MatrixQuantity)
            else operator.shape
        )
        if shape != (subspace.full_dimension, subspace.full_dimension):
            raise ValueError("operator and subspace full dimensions must agree")
        vectors = subspace.basis_vectors.magnitude
        dense = (
            operator.magnitude
            if isinstance(operator, MatrixQuantity)
            else operator.to_dense().magnitude
        )
        projector = subspace.projector().magnitude
        coordinates = vectors.T @ dense @ vectors
        embedded = projector @ dense @ projector
        return OperatorCompressionResult(
            operator=operator,
            subspace=subspace,
            coordinates=MatrixQuantity(coordinates, operator.unit),
            embedded=MatrixQuantity(embedded, operator.unit),
        )
