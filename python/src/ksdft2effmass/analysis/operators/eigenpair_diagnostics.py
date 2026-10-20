"""Reusable diagnostics for finite real-symmetric eigenpairs."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.operators import (
    MatrixQuantity,
    RealSymmetricEigenpairResult,
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
    """Analyze eigensolver residuals separately from reference-vector agreement."""

    __slots__ = ()

    def execute(
        self,
        eigenpairs: RealSymmetricEigenpairResult,
        reference_vectors: MatrixQuantity | None = None,
    ) -> RealSymmetricEigenpairDiagnosticResult:
        """Return residual and overlap diagnostics for the represented eigensystem."""
        if not isinstance(eigenpairs, RealSymmetricEigenpairResult):
            raise TypeError("eigenpairs must be RealSymmetricEigenpairResult")
        if reference_vectors is not None and not isinstance(
            reference_vectors, MatrixQuantity
        ):
            raise TypeError("reference_vectors must be MatrixQuantity or None")
        operator = eigenpairs.operator
        dense = (
            operator.magnitude
            if isinstance(operator, MatrixQuantity)
            else operator.to_dense().magnitude
        )
        values = eigenpairs.eigenvalues.magnitude
        vectors = eigenpairs.eigenvectors.magnitude
        residual = dense @ vectors - vectors * values[np.newaxis, :]
        spectral_scale = float(np.max(np.abs(values)))
        if spectral_scale == 0.0:
            raise ValueError("eigenvalue scale must be nonzero")
        scaled = np.asarray(
            [
                float(
                    np.linalg.norm(
                        dense @ vectors[:, index] - values[index] * vectors[:, index]
                    )
                    / spectral_scale
                )
                for index in range(values.size)
            ],
            dtype=np.float64,
        )
        overlaps: VectorQuantity | None = None
        if reference_vectors is not None:
            reference = reference_vectors.magnitude
            if reference.shape != vectors.shape:
                raise ValueError("reference_vectors must match eigenvector dimensions")
            overlap_values = np.asarray(
                [
                    max(
                        0.0,
                        1.0
                        - abs(float(vectors[:, index] @ reference[:, index])),
                    )
                    for index in range(values.size)
                ],
                dtype=np.float64,
            )
            overlaps = VectorQuantity(overlap_values, Unitless())
        return RealSymmetricEigenpairDiagnosticResult(
            algebraic_residual=MatrixQuantity(residual, operator.unit),
            scaled_column_residuals=VectorQuantity(scaled, Unitless()),
            overlap_defects=overlaps,
        )
