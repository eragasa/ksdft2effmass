"""Periodic-3D rank-two frame-transport ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic3d.rankN.band_alignment.frame_transport.base import (
    Periodic3DRankNFrameTransportAnalysis,
    Periodic3DRankNFrameTransportAnalysisRequest,
    Periodic3DRankNFrameTransportAnalyzer,
    Periodic3DRankNFrameTransportCapability,
)


class _Periodic3DRank2BandSubspace:
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


class Periodic3DRank2FrameTransport(
    Periodic3DRankNFrameTransportCapability,
    ABC,
):
    """Refine finite-rank periodic-3D frame transport to rank two."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the transported band frame."""


class Periodic3DRank2FrameTransportAnalysisRequest(
    _Periodic3DRank2BandSubspace,
    Periodic3DRankNFrameTransportAnalysisRequest,
    Periodic3DRank2FrameTransport,
    ABC,
):
    """Bind one periodic-3D rank-two frame-transport analysis."""

    __slots__ = ()


class Periodic3DRank2FrameTransportAnalysis(
    _Periodic3DRank2BandSubspace,
    Periodic3DRankNFrameTransportAnalysis,
    Periodic3DRank2FrameTransport,
    ABC,
):
    """Retain one periodic-3D rank-two frame-transport analysis."""

    __slots__ = ()


class Periodic3DRank2FrameTransportAnalyzer[
    RequestT: Periodic3DRank2FrameTransportAnalysisRequest,
    AnalysisT: Periodic3DRank2FrameTransportAnalysis,
](
    _Periodic3DRank2BandSubspace,
    Periodic3DRankNFrameTransportAnalyzer[RequestT, AnalysisT],
    Periodic3DRank2FrameTransport,
    ABC,
):
    """Execute one periodic-3D rank-two frame-transport request."""

    __slots__ = ()

    @property
    @abstractmethod
    def request(self) -> RequestT:
        """Return the immutable request bound to this action."""

    @abstractmethod
    def execute(self) -> AnalysisT:
        """Execute the bound frame-transport analysis."""


__all__ = [
    "Periodic3DRank2FrameTransport",
    "Periodic3DRank2FrameTransportAnalysis",
    "Periodic3DRank2FrameTransportAnalysisRequest",
    "Periodic3DRank2FrameTransportAnalyzer",
]
