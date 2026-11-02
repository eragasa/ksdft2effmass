"""Periodic-3D rank-two restricted gauge-alignment result."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.band_equivalence_hopping_locality.alignment import (
    RestrictedAlignmentDiagnostic,
)
from ksdft2effmass.gauge_alignment.base import GaugeAlignmentAnalysisIdentity
from ksdft2effmass.periodic3d.gauge_alignment.base import (
    Periodic3DGaugeAlignmentAnalysis,
)

from .request import Periodic3DRank2RestrictedGaugeAlignmentAnalysisRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic3DRank2RestrictedGaugeAlignmentAnalysis(
    RestrictedAlignmentDiagnostic,
    Periodic3DGaugeAlignmentAnalysis,
):
    """Retain one restricted global rank-two alignment diagnostic."""

    request: Periodic3DRank2RestrictedGaugeAlignmentAnalysisRequest

    def __post_init__(self) -> None:
        RestrictedAlignmentDiagnostic.__post_init__(self)
        if (
            type(self.request)
            is not Periodic3DRank2RestrictedGaugeAlignmentAnalysisRequest
        ):
            raise TypeError("request must be the exact periodic-3D alignment request")

    @property
    def analysis_identity(self) -> GaugeAlignmentAnalysisIdentity:
        """Return the request-bound retained-space alignment identity."""
        return self.request.analysis_identity


__all__ = ["Periodic3DRank2RestrictedGaugeAlignmentAnalysis"]
