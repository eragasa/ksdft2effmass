"""Periodic-3D arbitrary-rank frame-transport result."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.band_equivalence_hopping_locality.alignment import (
    FrameTransportDiagnostic,
)
from ksdft2effmass.periodic3d.base import Periodic3DCapability

from .request import Periodic3DRankNTransportAnalysisRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic3DRankNTransportDiagnosticAnalysis(
    FrameTransportDiagnostic,
    Periodic3DCapability,
):
    """Retain finite-rank neighbor-link, closure, and plaquette diagnostics."""

    request: Periodic3DRankNTransportAnalysisRequest

    def __post_init__(self) -> None:
        FrameTransportDiagnostic.__post_init__(self)
        if type(self.request) is not Periodic3DRankNTransportAnalysisRequest:
            raise TypeError("request must be the exact periodic-3D rank-N request")


__all__ = ["Periodic3DRankNTransportDiagnosticAnalysis"]
