"""Periodic-2D rank-two frame-transport ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic2d.frame_transport.base import (
    Periodic2DFrameTransport,
    Periodic2DFrameTransportAnalysis,
    Periodic2DFrameTransportAnalysisRequest,
    Periodic2DFrameTransportAnalyzer,
)


class _Periodic2DRank2BandSubspace:
    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the transported band frame."""
        return 2


class Periodic2DRank2FrameTransport(Periodic2DFrameTransport, ABC):
    """Identify frame transport on a periodic-2D rank-two band subspace."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the transported band frame."""


class Periodic2DRank2FrameTransportAnalysisRequest(
    _Periodic2DRank2BandSubspace,
    Periodic2DFrameTransportAnalysisRequest,
    Periodic2DRank2FrameTransport,
    ABC,
):
    """Bind one periodic-2D rank-two frame-transport analysis."""

    __slots__ = ()


class Periodic2DRank2FrameTransportAnalysis(
    _Periodic2DRank2BandSubspace,
    Periodic2DFrameTransportAnalysis,
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
    Periodic2DFrameTransportAnalyzer[RequestT, AnalysisT],
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
