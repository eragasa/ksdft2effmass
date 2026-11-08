"""Periodic-1D arbitrary-rank frame-transport ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.frame_transport.base import PeriodicRankNFrameTransportCapability
from ksdft2effmass.periodic1d.frame_transport.base import (
    Periodic1DFrameTransport,
    Periodic1DFrameTransportAnalysis,
    Periodic1DFrameTransportAnalysisRequest,
    Periodic1DFrameTransportAnalyzer,
)


class Periodic1DRankNFrameTransportCapability(
    Periodic1DFrameTransport,
    PeriodicRankNFrameTransportCapability,
    ABC,
):
    """Identify frame transport on a periodic-1D finite-rank band subspace."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the transported band frame."""


class Periodic1DRankNFrameTransportAnalysisRequest(
    Periodic1DFrameTransportAnalysisRequest,
    Periodic1DRankNFrameTransportCapability,
    ABC,
):
    """Bind one periodic-1D arbitrary-rank frame-transport analysis."""

    __slots__ = ()


class Periodic1DRankNFrameTransportAnalysis(
    Periodic1DFrameTransportAnalysis,
    Periodic1DRankNFrameTransportCapability,
    ABC,
):
    """Retain one periodic-1D arbitrary-rank frame-transport analysis outcome."""

    __slots__ = ()


class Periodic1DRankNFrameTransportAnalyzer[
    RequestT: Periodic1DRankNFrameTransportAnalysisRequest,
    AnalysisT: Periodic1DRankNFrameTransportAnalysis,
](
    Periodic1DFrameTransportAnalyzer[RequestT, AnalysisT],
    Periodic1DRankNFrameTransportCapability,
    ABC,
):
    """Execute one periodic-1D arbitrary-rank frame-transport request."""

    __slots__ = ()

    @property
    @abstractmethod
    def request(self) -> RequestT:
        """Return the immutable request bound to this action."""

    @property
    def band_subspace_rank(self) -> int:
        """Return the rank of the transported band frame."""
        return self.request.band_subspace_rank

    @abstractmethod
    def execute(self) -> AnalysisT:
        """Execute the bound frame-transport analysis."""


__all__ = [
    "Periodic1DRankNFrameTransportAnalysis",
    "Periodic1DRankNFrameTransportAnalysisRequest",
    "Periodic1DRankNFrameTransportAnalyzer",
    "Periodic1DRankNFrameTransportCapability",
]
