"""Reusable diagnostics for finite real-symmetric eigensystems."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from projectkoios.physkit.linalg.eigen import Eigensystem
from projectkoios.physkit.numerics.eigenproblems.residuals import (
    eigenpair_residual_norms,
)
from projectkoios.physkit.units import (
    MatrixQuantity,
    SparseMatrixQuantity,
    Unitless,
    VectorQuantity,
)


@dataclass(frozen=True, slots=True, eq=False)
class RealSymmetricEigenpairDiagnosticResult:
    """Retain algebraic residuals and optional reference-vector overlaps."""

    algebraic_residual: MatrixQuantity
    scaled_column_residuals: VectorQuantity
    overlap_defects: VectorQuantity | None


@dataclass(frozen=True, slots=True, eq=False)
class RealSymmetricEigenpairDiagnosticRequest:
    """Bind one represented real eigensystem and optional reference vectors."""

    eigensystem: Eigensystem
    reference_vectors: MatrixQuantity | None = None

    def __post_init__(self) -> None:
        """Admit the complete residual and overlap diagnostic request."""
        if not isinstance(self.eigensystem, Eigensystem):
            raise TypeError("eigensystem must be Eigensystem")
        _ = self.represented_matrix
        if not isinstance(self.eigensystem.eigenvectors, MatrixQuantity):
            raise TypeError("eigensystem eigenvectors must be real")
        if self.reference_vectors is not None and not isinstance(
            self.reference_vectors, MatrixQuantity
        ):
            raise TypeError("reference_vectors must be MatrixQuantity or None")
        vectors = self.eigensystem.eigenvectors.magnitude
        if (
            self.reference_vectors is not None
            and self.reference_vectors.magnitude.shape != vectors.shape
        ):
            raise ValueError("reference_vectors must match eigenvector dimensions")
        if float(np.max(np.abs(self.eigensystem.eigenvalues.magnitude))) == 0.0:
            raise ValueError("eigenvalue scale must be nonzero")

    @property
    def represented_matrix(self) -> MatrixQuantity | SparseMatrixQuantity:
        """Return the admitted real represented operator matrix."""
        matrix = self.eigensystem.matrix
        if not isinstance(matrix, MatrixQuantity | SparseMatrixQuantity):
            raise TypeError("eigensystem matrix must be real")
        return matrix


class RealSymmetricEigenpairDiagnosticAnalyzer:
    """Analyze residuals and reference agreement for one bound eigensystem."""

    __slots__ = ("_request",)

    def __init__(self, request: RealSymmetricEigenpairDiagnosticRequest) -> None:
        if type(request) is not RealSymmetricEigenpairDiagnosticRequest:
            raise TypeError("request must be RealSymmetricEigenpairDiagnosticRequest")
        self._request = request

    @property
    def request(self) -> RealSymmetricEigenpairDiagnosticRequest:
        """Return the complete immutable eigenpair diagnostic request."""
        return self._request

    def execute(self) -> RealSymmetricEigenpairDiagnosticResult:
        """Return residual and overlap diagnostics for the represented eigensystem."""
        eigensystem = self.request.eigensystem
        reference_vectors = self.request.reference_vectors
        operator = self.request.represented_matrix
        represented = (
            operator.magnitude
            if isinstance(operator, MatrixQuantity)
            else operator.to_csr()
        )
        values = eigensystem.eigenvalues.magnitude
        vectors = eigensystem.eigenvectors.magnitude
        residual = represented @ vectors - vectors * values[np.newaxis, :]
        spectral_scale = float(np.max(np.abs(values)))
        scaled = eigenpair_residual_norms(represented, values, vectors) / spectral_scale
        overlaps: VectorQuantity | None = None
        if reference_vectors is not None:
            reference = reference_vectors.magnitude
            overlap_values = np.asarray(
                [
                    max(
                        0.0,
                        1.0 - abs(float(vectors[:, index] @ reference[:, index])),
                    )
                    for index in range(values.size)
                ],
                dtype=np.float64,
            )
            overlaps = VectorQuantity(overlap_values, Unitless())
        return RealSymmetricEigenpairDiagnosticResult(
            algebraic_residual=MatrixQuantity(
                np.asarray(residual, dtype=np.float64), operator.unit
            ),
            scaled_column_residuals=VectorQuantity(
                np.asarray(scaled, dtype=np.float64), Unitless()
            ),
            overlap_defects=overlaps,
        )
