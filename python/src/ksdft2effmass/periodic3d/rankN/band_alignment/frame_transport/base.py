"""Periodic-3D arbitrary-rank frame-transport ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic3d.frame_transport.base import (
    Periodic3DFrameTransport,
    Periodic3DFrameTransportAnalysis,
    Periodic3DFrameTransportAnalysisRequest,
    Periodic3DFrameTransportAnalyzer,
)


class Periodic3DRankNFrameTransportCapability(Periodic3DFrameTransport, ABC):
    """Identify frame transport on a periodic-3D finite-rank band subspace."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the transported band frame."""


class Periodic3DRankNFrameTransportAnalysisRequest(
    Periodic3DFrameTransportAnalysisRequest,
    Periodic3DRankNFrameTransportCapability,
    ABC,
):
    """Bind one periodic-3D arbitrary-rank frame-transport analysis."""

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


class Periodic3DRankNFrameTransportAnalysis(
    Periodic3DFrameTransportAnalysis,
    Periodic3DRankNFrameTransportCapability,
    ABC,
):
    """Retain one periodic-3D arbitrary-rank frame-transport analysis."""

    __slots__ = ()


class Periodic3DRankNFrameTransportAnalyzer[
    RequestT: Periodic3DRankNFrameTransportAnalysisRequest,
    AnalysisT: Periodic3DRankNFrameTransportAnalysis,
](
    Periodic3DFrameTransportAnalyzer[RequestT, AnalysisT],
    Periodic3DRankNFrameTransportCapability,
    ABC,
):
    """Execute one periodic-3D arbitrary-rank frame-transport request."""

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
    "Periodic3DRankNFrameTransportAnalysis",
    "Periodic3DRankNFrameTransportAnalysisRequest",
    "Periodic3DRankNFrameTransportAnalyzer",
    "Periodic3DRankNFrameTransportCapability",
]
