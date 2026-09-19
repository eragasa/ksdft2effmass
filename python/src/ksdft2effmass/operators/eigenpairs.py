"""Deterministic eigenpair analysis for finite real-symmetric operators."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import linalg, sparse  # type: ignore[import-untyped]
from scipy.sparse import linalg as sparse_linalg  # type: ignore[import-untyped]

from .quantities import (
    MatrixQuantity,
    SparseMatrixQuantity,
    Unitless,
    VectorQuantity,
)

type RealSymmetricOperator = MatrixQuantity | SparseMatrixQuantity


@dataclass(frozen=True, slots=True, eq=False)
class RealSymmetricEigenpairResult:
    """Retain ordered eigenvalues and column eigenvectors of one finite operator."""

    operator: RealSymmetricOperator
    eigenvalues: VectorQuantity
    eigenvectors: MatrixQuantity

    def __post_init__(self) -> None:
        if not isinstance(self.operator, MatrixQuantity | SparseMatrixQuantity):
            raise TypeError("operator must be a dense or sparse matrix quantity")
        if not isinstance(self.eigenvalues, VectorQuantity):
            raise TypeError("eigenvalues must be VectorQuantity")
        if not isinstance(self.eigenvectors, MatrixQuantity):
            raise TypeError("eigenvectors must be MatrixQuantity")
        shape = (
            self.operator.magnitude.shape
            if isinstance(self.operator, MatrixQuantity)
            else self.operator.shape
        )
        dimension = shape[0]
        if shape != (dimension, dimension):
            raise ValueError("operator must be square")
        selected = self.eigenvalues.magnitude.size
        if selected <= 0 or selected > dimension:
            raise ValueError("eigenvalues must select between one and all states")
        if self.eigenvectors.magnitude.shape != (dimension, selected):
            raise ValueError("eigenvectors must match operator and selected dimensions")


class RealSymmetricEigenpairSolver:
    """Solve dense or sparse finite real-symmetric operators without densifying CSR.

    Complete sparse eigensystems are supported for tridiagonal operators through
    :func:`scipy.linalg.eigh_tridiagonal`, which consumes only the represented
    diagonals. Partial sparse eigensystems use :func:`scipy.sparse.linalg.eigsh`.
    A complete non-tridiagonal sparse eigensystem is rejected rather than silently
    materializing a dense matrix.
    """

    __slots__ = ()

    def execute(self, operator: RealSymmetricOperator) -> RealSymmetricEigenpairResult:
        """Return the complete ascending eigensystem without sparse densification."""
        dimension = self.validate(operator)
        if isinstance(operator, MatrixQuantity):
            eigenvalues, eigenvectors = np.linalg.eigh(operator.magnitude)
        else:
            matrix = operator.to_csr()
            diagonal = np.asarray(matrix.diagonal(), dtype=np.float64)
            off_diagonal = np.asarray(matrix.diagonal(1), dtype=np.float64)
            reconstructed = sparse.diags(
                (off_diagonal, diagonal, off_diagonal),
                offsets=(-1, 0, 1),
                shape=(dimension, dimension),
                format="csr",
                dtype=np.float64,
            )
            difference = matrix - reconstructed
            difference.eliminate_zeros()
            if difference.nnz != 0:
                raise ValueError(
                    "complete sparse eigensystems require a tridiagonal operator"
                )
            eigenvalues, eigenvectors = linalg.eigh_tridiagonal(
                diagonal,
                off_diagonal,
                check_finite=False,
                lapack_driver="auto",
            )
        return RealSymmetricEigenpairResult(
            operator=operator,
            eigenvalues=VectorQuantity(eigenvalues, operator.unit),
            eigenvectors=MatrixQuantity(eigenvectors, Unitless()),
        )

    def execute_lowest(
        self, operator: RealSymmetricOperator, count: int
    ) -> RealSymmetricEigenpairResult:
        """Return the lowest ``count`` eigenpairs without densifying sparse input."""
        dimension = self.validate(operator)
        if type(count) is not int:
            raise TypeError("count must be a built-in int")
        if count <= 0 or count > dimension:
            raise ValueError("count must select between one and all states")
        if count == dimension:
            return self.execute(operator)
        if isinstance(operator, MatrixQuantity):
            eigenvalues, eigenvectors = np.linalg.eigh(operator.magnitude)
            selected_values = eigenvalues[:count]
            selected_vectors = eigenvectors[:, :count]
        else:
            selected_values, selected_vectors = sparse_linalg.eigsh(
                operator.to_csr(),
                k=count,
                which="SA",
                v0=np.ones(dimension, dtype=np.float64),
            )
            order = np.argsort(selected_values)
            selected_values = selected_values[order]
            selected_vectors = selected_vectors[:, order]
            selected_vectors = self.canonicalize_signs(selected_vectors)
        return RealSymmetricEigenpairResult(
            operator=operator,
            eigenvalues=VectorQuantity(selected_values, operator.unit),
            eigenvectors=MatrixQuantity(selected_vectors, Unitless()),
        )

    @staticmethod
    def validate(operator: RealSymmetricOperator) -> int:
        """Validate one real-symmetric operator and return its dimension."""
        if not isinstance(operator, MatrixQuantity | SparseMatrixQuantity):
            raise TypeError("operator must be a dense or sparse matrix quantity")
        if isinstance(operator, MatrixQuantity):
            rows, columns = operator.magnitude.shape
            if rows != columns:
                raise ValueError("operator must be square")
            if not np.array_equal(operator.magnitude, operator.magnitude.T):
                raise ValueError("operator must be exactly real symmetric")
            return rows
        rows, columns = operator.shape
        if rows != columns:
            raise ValueError("operator must be square")
        difference = operator.to_csr() - operator.to_csr().transpose()
        difference.eliminate_zeros()
        if difference.nnz != 0:
            raise ValueError("operator must be exactly real symmetric")
        return rows

    @staticmethod
    def canonicalize_signs(
        eigenvectors: np.ndarray[tuple[int, int], np.dtype[np.float64]],
    ) -> np.ndarray[tuple[int, int], np.dtype[np.float64]]:
        """Choose deterministic signs using each vector's largest entry."""
        canonical = eigenvectors.copy()
        for column in range(canonical.shape[1]):
            vector = canonical[:, column]
            pivot = int(np.argmax(np.abs(vector)))
            if vector[pivot] < 0.0:
                canonical[:, column] *= -1.0
        return canonical
