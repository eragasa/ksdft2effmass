"""Periodic-2D arbitrary-rank frame-transport ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic2d.frame_transport.base import (
    Periodic2DFrameTransport,
    Periodic2DFrameTransportAnalysis,
    Periodic2DFrameTransportAnalysisRequest,
    Periodic2DFrameTransportAnalyzer,
)


class Periodic2DRankNFrameTransportCapability(Periodic2DFrameTransport, ABC):
    """Identify frame transport on a periodic-2D finite-rank band subspace."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the transported band frame."""


class Periodic2DRankNFrameTransportAnalysisRequest(
    Periodic2DFrameTransportAnalysisRequest,
    Periodic2DRankNFrameTransportCapability,
    ABC,
):
    """Bind one periodic-2D arbitrary-rank frame-transport analysis."""

    __slots__ = ()

    @property
    @abstractmethod
    def retained_rank(self) -> int:
        """Return the request's historical retained-rank field."""

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the transported band frame."""
        return self.retained_rank


class Periodic2DRankNFrameTransportAnalysis(
    Periodic2DFrameTransportAnalysis,
    Periodic2DRankNFrameTransportCapability,
    ABC,
):
    """Retain one periodic-2D arbitrary-rank frame-transport analysis."""

    __slots__ = ()


class Periodic2DRankNFrameTransportAnalyzer[
    RequestT: Periodic2DRankNFrameTransportAnalysisRequest,
    AnalysisT: Periodic2DRankNFrameTransportAnalysis,
](
    Periodic2DFrameTransportAnalyzer[RequestT, AnalysisT],
    Periodic2DRankNFrameTransportCapability,
    ABC,
):
    """Execute one periodic-2D arbitrary-rank frame-transport request."""

    __slots__ = ()

    @property
    @abstractmethod
    def request(self) -> RequestT:
        """Return the immutable request bound to this action."""

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the transported band frame."""
        return self.request.band_subspace_rank

    @abstractmethod
    def execute(self) -> AnalysisT:
        """Execute the bound frame-transport analysis."""


__all__ = [
    "Periodic2DRankNFrameTransportAnalysis",
    "Periodic2DRankNFrameTransportAnalysisRequest",
    "Periodic2DRankNFrameTransportAnalyzer",
    "Periodic2DRankNFrameTransportCapability",
]
