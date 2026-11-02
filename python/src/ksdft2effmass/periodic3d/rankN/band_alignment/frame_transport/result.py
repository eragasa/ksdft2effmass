"""Periodic-3D arbitrary-rank frame-transport result."""

from __future__ import annotations

from dataclasses import dataclass
from typing import final

from ksdft2effmass.band_equivalence_hopping_locality.alignment import (
    FrameTransportDiagnostic,
)

from .base import Periodic3DRankNFrameTransportAnalysis
from .request import Periodic3DRankNTransportAnalysisRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic3DRankNTransportDiagnosticAnalysis(
    FrameTransportDiagnostic,
    Periodic3DRankNFrameTransportAnalysis,
):
    """Retain finite-rank neighbor-link, closure, and plaquette diagnostics."""

    request: Periodic3DRankNTransportAnalysisRequest

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the transported band frame."""
        return self.request.band_subspace_rank

    def __post_init__(self) -> None:
        FrameTransportDiagnostic.__post_init__(self)
        if type(self.request) is not Periodic3DRankNTransportAnalysisRequest:
            raise TypeError("request must be the exact periodic-3D rank-N request")


__all__ = ["Periodic3DRankNTransportDiagnosticAnalysis"]
