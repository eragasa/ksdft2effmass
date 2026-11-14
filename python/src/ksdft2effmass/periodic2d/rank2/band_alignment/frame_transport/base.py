"""Periodic-2D rank-two frame-transport ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic2d.rankN.band_alignment.frame_transport.base import (
    Periodic2DRankNFrameTransportAnalysis,
    Periodic2DRankNFrameTransportAnalysisRequest,
    Periodic2DRankNFrameTransportAnalyzer,
    Periodic2DRankNFrameTransportCapability,
)


class _Periodic2DRank2BandSubspace:
    __slots__ = ()

    @property
    @final
    def retained_rank(self) -> int:
        """Return the fixed historical retained-rank value."""
        return 2

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the transported band frame."""
        return self.retained_rank


class Periodic2DRank2FrameTransport(
    Periodic2DRankNFrameTransportCapability,
    ABC,
):
    """Refine finite-rank periodic-2D frame transport to rank two."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the transported band frame."""


class Periodic2DRank2FrameTransportAnalysisRequest(
    _Periodic2DRank2BandSubspace,
    Periodic2DRankNFrameTransportAnalysisRequest,
    Periodic2DRank2FrameTransport,
    ABC,
):
    """Bind one periodic-2D rank-two frame-transport analysis."""

    __slots__ = ()


class Periodic2DRank2FrameTransportAnalysis(
    _Periodic2DRank2BandSubspace,
    Periodic2DRankNFrameTransportAnalysis,
    Periodic2DRank2FrameTransport,
    ABC,
):
    """Retain one periodic-2D rank-two frame-transport analysis."""

    __slots__ = ()


class Periodic2DRank2FrameTransportAnalyzer[
    RequestT: Periodic2DRank2FrameTransportAnalysisRequest,
    AnalysisT: Periodic2DRank2FrameTransportAnalysis,
](
    _Periodic2DRank2BandSubspace,
    Periodic2DRankNFrameTransportAnalyzer[RequestT, AnalysisT],
    Periodic2DRank2FrameTransport,
    ABC,
):
    """Execute one periodic-2D rank-two frame-transport request."""

    __slots__ = ()

    @property
    @abstractmethod
    def request(self) -> RequestT:
        """Return the immutable request bound to this action."""

    @abstractmethod
    def execute(self) -> AnalysisT:
        """Execute the bound frame-transport analysis."""


__all__ = [
    "Periodic2DRank2FrameTransport",
    "Periodic2DRank2FrameTransportAnalysis",
    "Periodic2DRank2FrameTransportAnalysisRequest",
    "Periodic2DRank2FrameTransportAnalyzer",
]
