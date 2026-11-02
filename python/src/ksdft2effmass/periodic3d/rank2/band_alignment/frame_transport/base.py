"""Periodic-3D rank-two frame-transport ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic3d.frame_transport.base import (
    Periodic3DFrameTransport,
    Periodic3DFrameTransportAnalysis,
    Periodic3DFrameTransportAnalysisRequest,
    Periodic3DFrameTransportAnalyzer,
)


class _Periodic3DRank2BandSubspace:
    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the transported band frame."""
        return 2


class Periodic3DRank2FrameTransport(Periodic3DFrameTransport, ABC):
    """Identify frame transport on a periodic-3D rank-two band subspace."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the transported band frame."""


class Periodic3DRank2FrameTransportAnalysisRequest(
    _Periodic3DRank2BandSubspace,
    Periodic3DFrameTransportAnalysisRequest,
    Periodic3DRank2FrameTransport,
    ABC,
):
    """Bind one periodic-3D rank-two frame-transport analysis."""

    __slots__ = ()


class Periodic3DRank2FrameTransportAnalysis(
    _Periodic3DRank2BandSubspace,
    Periodic3DFrameTransportAnalysis,
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
    Periodic3DFrameTransportAnalyzer[RequestT, AnalysisT],
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
