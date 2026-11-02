"""Periodic-2D rank-two frame-transport result."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.band_equivalence_hopping_locality.alignment import (
    FrameTransportDiagnostic,
)

from .base import Periodic2DRank2FrameTransportAnalysis
from .request import Periodic2DRank2TransportAnalysisRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic2DRank2TransportDiagnosticAnalysis(
    FrameTransportDiagnostic,
    Periodic2DRank2FrameTransportAnalysis,
):
    """Retain neighbor-link, closure, and plaquette transport diagnostics."""

    request: Periodic2DRank2TransportAnalysisRequest

    def __post_init__(self) -> None:
        FrameTransportDiagnostic.__post_init__(self)
        if type(self.request) is not Periodic2DRank2TransportAnalysisRequest:
            raise TypeError("request must be the exact periodic-2D transport request")


__all__ = ["Periodic2DRank2TransportDiagnosticAnalysis"]
