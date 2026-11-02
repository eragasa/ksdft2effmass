"""Periodic-3D rank-two frame-transport result."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.band_equivalence_hopping_locality.alignment import (
    FrameTransportDiagnostic,
)
from ksdft2effmass.periodic3d.base import Periodic3DCapability

from .request import Periodic3DRank2TransportAnalysisRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic3DRank2TransportDiagnosticAnalysis(
    FrameTransportDiagnostic,
    Periodic3DCapability,
):
    """Retain neighbor-link, closure, and plaquette transport diagnostics."""

    request: Periodic3DRank2TransportAnalysisRequest

    def __post_init__(self) -> None:
        FrameTransportDiagnostic.__post_init__(self)
        if type(self.request) is not Periodic3DRank2TransportAnalysisRequest:
            raise TypeError("request must be the exact periodic-3D transport request")


__all__ = ["Periodic3DRank2TransportDiagnosticAnalysis"]
