"""Periodic-2D arbitrary-rank frame-transport result."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.band_equivalence_hopping_locality.alignment import (
    FrameTransportDiagnostic,
)
from ksdft2effmass.periodic2d.base import Periodic2DCapability

from .request import Periodic2DRankNTransportAnalysisRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic2DRankNTransportDiagnosticAnalysis(
    FrameTransportDiagnostic,
    Periodic2DCapability,
):
    """Retain finite-rank neighbor-link, closure, and plaquette diagnostics."""

    request: Periodic2DRankNTransportAnalysisRequest

    def __post_init__(self) -> None:
        FrameTransportDiagnostic.__post_init__(self)
        if type(self.request) is not Periodic2DRankNTransportAnalysisRequest:
            raise TypeError("request must be the exact periodic-2D rank-N request")


__all__ = ["Periodic2DRankNTransportDiagnosticAnalysis"]
