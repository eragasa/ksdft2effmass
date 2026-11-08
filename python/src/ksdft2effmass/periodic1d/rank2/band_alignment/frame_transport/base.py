"""Periodic-1D rank-two frame-transport ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic1d.rankN.band_alignment.frame_transport.base import (
    Periodic1DRankNFrameTransportAnalysis,
    Periodic1DRankNFrameTransportAnalysisRequest,
    Periodic1DRankNFrameTransportAnalyzer,
    Periodic1DRankNFrameTransportCapability,
)


class _Periodic1DRank2BandSubspace:
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


class Periodic1DRank2FrameTransport(
    Periodic1DRankNFrameTransportCapability,
    ABC,
):
    """Refine finite-rank periodic-1D frame transport to rank two."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the transported band frame."""


class Periodic1DRank2FrameTransportAnalysisRequest(
    _Periodic1DRank2BandSubspace,
    Periodic1DRankNFrameTransportAnalysisRequest,
    Periodic1DRank2FrameTransport,
    ABC,
):
    """Bind one periodic-1D rank-two frame-transport analysis."""

    __slots__ = ()


class Periodic1DRank2FrameTransportAnalysis(
    _Periodic1DRank2BandSubspace,
    Periodic1DRankNFrameTransportAnalysis,
    Periodic1DRank2FrameTransport,
    ABC,
):
    """Retain one periodic-1D rank-two frame-transport analysis."""

    __slots__ = ()


class Periodic1DRank2FrameTransportAnalyzer[
    RequestT: Periodic1DRank2FrameTransportAnalysisRequest,
    AnalysisT: Periodic1DRank2FrameTransportAnalysis,
](
    _Periodic1DRank2BandSubspace,
    Periodic1DRankNFrameTransportAnalyzer[RequestT, AnalysisT],
    Periodic1DRank2FrameTransport,
    ABC,
):
    """Execute one periodic-1D rank-two frame-transport request."""

    __slots__ = ()

    @property
    @abstractmethod
    def request(self) -> RequestT:
        """Return the immutable request bound to this action."""

    @abstractmethod
    def execute(self) -> AnalysisT:
        """Execute the bound frame-transport analysis."""


__all__ = [
    "Periodic1DRank2FrameTransport",
    "Periodic1DRank2FrameTransportAnalysis",
    "Periodic1DRank2FrameTransportAnalysisRequest",
    "Periodic1DRank2FrameTransportAnalyzer",
]
