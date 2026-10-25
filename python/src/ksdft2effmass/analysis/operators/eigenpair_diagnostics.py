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


class RealSymmetricEigenpairDiagnosticAnalyzer:
    """Analyze eigensystem residuals separately from reference-vector agreement."""

    __slots__ = ()

    def execute(
        self,
        eigensystem: Eigensystem,
        reference_vectors: MatrixQuantity | None = None,
    ) -> RealSymmetricEigenpairDiagnosticResult:
        """Return residual and overlap diagnostics for the represented eigensystem."""
        if not isinstance(eigensystem, Eigensystem):
            raise TypeError("eigensystem must be Eigensystem")
        if not isinstance(eigensystem.matrix, MatrixQuantity | SparseMatrixQuantity):
            raise TypeError("eigensystem matrix must be real")
        if not isinstance(eigensystem.eigenvectors, MatrixQuantity):
            raise TypeError("eigensystem eigenvectors must be real")
        if reference_vectors is not None and not isinstance(
            reference_vectors, MatrixQuantity
        ):
            raise TypeError("reference_vectors must be MatrixQuantity or None")
        operator = eigensystem.matrix
        represented = (
            operator.magnitude
            if isinstance(operator, MatrixQuantity)
            else operator.to_csr()
        )
        values = eigensystem.eigenvalues.magnitude
        vectors = eigensystem.eigenvectors.magnitude
        residual = represented @ vectors - vectors * values[np.newaxis, :]
        spectral_scale = float(np.max(np.abs(values)))
        if spectral_scale == 0.0:
            raise ValueError("eigenvalue scale must be nonzero")
        scaled = eigenpair_residual_norms(represented, values, vectors) / spectral_scale
        overlaps: VectorQuantity | None = None
        if reference_vectors is not None:
            reference = reference_vectors.magnitude
            if reference.shape != vectors.shape:
                raise ValueError("reference_vectors must match eigenvector dimensions")
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
