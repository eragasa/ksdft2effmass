"""Periodic-2D rank-two restricted gauge-alignment result."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.band_equivalence_hopping_locality.alignment import (
    RestrictedAlignmentDiagnostic,
)
from ksdft2effmass.gauge_alignment.base import GaugeAlignmentAnalysisIdentity
from ksdft2effmass.periodic2d.rank2.gauge_alignment.base import (
    Periodic2DRank2GaugeAlignmentAnalysis,
)

from .request import Periodic2DRank2RestrictedGaugeAlignmentAnalysisRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic2DRank2RestrictedGaugeAlignmentAnalysis(
    RestrictedAlignmentDiagnostic,
    Periodic2DRank2GaugeAlignmentAnalysis,
):
    """Retain one restricted global rank-two alignment diagnostic."""

    request: Periodic2DRank2RestrictedGaugeAlignmentAnalysisRequest

    def __post_init__(self) -> None:
        RestrictedAlignmentDiagnostic.__post_init__(self)
        if (
            type(self.request)
            is not Periodic2DRank2RestrictedGaugeAlignmentAnalysisRequest
        ):
            raise TypeError("request must be the exact periodic-2D alignment request")

    @property
    def analysis_identity(self) -> GaugeAlignmentAnalysisIdentity:
        """Return the request-bound retained-space alignment identity."""
        return self.request.analysis_identity


__all__ = ["Periodic2DRank2RestrictedGaugeAlignmentAnalysis"]
