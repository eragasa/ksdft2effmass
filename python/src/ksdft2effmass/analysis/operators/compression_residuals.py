"""Residual analysis for orthogonal finite-operator compression."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.linalg import (
    CsrRealMatrixQuantity,
    RealMatrixQuantity,
)
from ksdft2effmass.operators import (
    OperatorCompressionResult,
    OrthogonalSpectralSubspace,
)


@dataclass(frozen=True, slots=True, eq=False)
class OrthogonalCompressionResidualResult:
    """Retain distinct consistent, unmatched, and discarded-sector residuals."""

    consistent: RealMatrixQuantity
    unmatched: RealMatrixQuantity
    discarded_sector: RealMatrixQuantity


class OrthogonalCompressionResidualAnalyzer:
    """Analyze residuals without conflating compression and discarded sectors."""

    __slots__ = ()

    def execute(
        self,
        operator: RealMatrixQuantity | CsrRealMatrixQuantity,
        subspace: OrthogonalSpectralSubspace,
        compression: OperatorCompressionResult,
    ) -> OrthogonalCompressionResidualResult:
        """Return the three residual matrices on the original coordinate space."""
        if not isinstance(operator, RealMatrixQuantity | CsrRealMatrixQuantity):
            raise TypeError(
                "operator must be RealMatrixQuantity or CsrRealMatrixQuantity"
            )
        if not isinstance(subspace, OrthogonalSpectralSubspace):
            raise TypeError("subspace must be OrthogonalSpectralSubspace")
        if not isinstance(compression, OperatorCompressionResult):
            raise TypeError("compression must be OperatorCompressionResult")
        dense = (
            operator.magnitude
            if isinstance(operator, RealMatrixQuantity)
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
            consistent=RealMatrixQuantity(
                embedded - projector @ dense @ projector, operator.unit
            ),
            unmatched=RealMatrixQuantity(embedded - dense, operator.unit),
            discarded_sector=RealMatrixQuantity(
                -(complement @ dense @ complement), operator.unit
            ),
        )
