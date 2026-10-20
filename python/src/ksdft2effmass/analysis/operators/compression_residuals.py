"""Residual analysis for orthogonal finite-operator compression."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.operators import (
    MatrixQuantity,
    OperatorCompressionResult,
    OrthogonalSpectralSubspace,
    SparseMatrixQuantity,
)


@dataclass(frozen=True, slots=True, eq=False)
class OrthogonalCompressionResidualResult:
    """Retain distinct consistent, unmatched, and discarded-sector residuals."""

    consistent: MatrixQuantity
    unmatched: MatrixQuantity
    discarded_sector: MatrixQuantity


class OrthogonalCompressionResidualAnalyzer:
    """Analyze residuals without conflating compression and discarded sectors."""

    __slots__ = ()

    def execute(
        self,
        operator: MatrixQuantity | SparseMatrixQuantity,
        subspace: OrthogonalSpectralSubspace,
        compression: OperatorCompressionResult,
    ) -> OrthogonalCompressionResidualResult:
        """Return the three residual matrices on the original coordinate space."""
        if not isinstance(operator, MatrixQuantity | SparseMatrixQuantity):
            raise TypeError("operator must be MatrixQuantity or SparseMatrixQuantity")
        if not isinstance(subspace, OrthogonalSpectralSubspace):
            raise TypeError("subspace must be OrthogonalSpectralSubspace")
        if not isinstance(compression, OperatorCompressionResult):
            raise TypeError("compression must be OperatorCompressionResult")
        dense = (
            operator.magnitude
            if isinstance(operator, MatrixQuantity)
            else operator.to_dense().magnitude
        )
        projector = subspace.projector().magnitude
        complement = subspace.complement_projector().magnitude
        embedded = compression.embedded.magnitude
        if embedded.shape != dense.shape or projector.shape != dense.shape:
            raise ValueError(
                "operator, subspace, and compression dimensions must match"
            )
        return OrthogonalCompressionResidualResult(
            consistent=MatrixQuantity(
                embedded - projector @ dense @ projector, operator.unit
            ),
            unmatched=MatrixQuantity(embedded - dense, operator.unit),
            discarded_sector=MatrixQuantity(
                -(complement @ dense @ complement), operator.unit
            ),
        )
