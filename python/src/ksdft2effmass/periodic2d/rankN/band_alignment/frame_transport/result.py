"""Periodic-2D arbitrary-rank frame-transport result."""

from __future__ import annotations

from dataclasses import dataclass
from typing import final

from ksdft2effmass.band_equivalence_hopping_locality.alignment import (
    FrameTransportDiagnostic,
)

from .base import Periodic2DRankNFrameTransportAnalysis
from .request import Periodic2DRankNTransportAnalysisRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic2DRankNTransportDiagnosticAnalysis(
    FrameTransportDiagnostic,
    Periodic2DRankNFrameTransportAnalysis,
):
    """Retain finite-rank neighbor-link, closure, and plaquette diagnostics."""

    request: Periodic2DRankNTransportAnalysisRequest

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the transported band frame."""
        return self.request.band_subspace_rank

    def __post_init__(self) -> None:
        FrameTransportDiagnostic.__post_init__(self)
        if type(self.request) is not Periodic2DRankNTransportAnalysisRequest:
            raise TypeError("request must be the exact periodic-2D rank-N request")


__all__ = ["Periodic2DRankNTransportDiagnosticAnalysis"]
