"""Periodic two-dimensional specialization of frame transport."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.frame_transport.base import (
    PeriodicFrameTransport,
    PeriodicFrameTransportAnalysis,
    PeriodicFrameTransportAnalysisRequest,
    PeriodicFrameTransportAnalyzer,
)
from ksdft2effmass.periodic2d.base import Periodic2DCapability


class Periodic2DFrameTransport(
    PeriodicFrameTransport,
    Periodic2DCapability,
    ABC,
):
    """Identify frame transport on a two-dimensional periodic lattice."""

    __slots__ = ()


class Periodic2DFrameTransportAnalysisRequest(
    PeriodicFrameTransportAnalysisRequest,
    Periodic2DFrameTransport,
    ABC,
):
    """Bind one periodic-2D frame-transport request."""

    __slots__ = ()


class Periodic2DFrameTransportAnalysis(
    PeriodicFrameTransportAnalysis,
    Periodic2DFrameTransport,
    ABC,
):
    """Retain one periodic-2D frame-transport outcome."""

    __slots__ = ()


class Periodic2DFrameTransportAnalyzer[
    RequestT: Periodic2DFrameTransportAnalysisRequest,
    AnalysisT: Periodic2DFrameTransportAnalysis,
](
    PeriodicFrameTransportAnalyzer[RequestT, AnalysisT],
    Periodic2DFrameTransport,
    ABC,
):
    """Execute one periodic-2D frame-transport request."""

    __slots__ = ()


__all__ = [
    "Periodic2DFrameTransport",
    "Periodic2DFrameTransportAnalysis",
    "Periodic2DFrameTransportAnalysisRequest",
    "Periodic2DFrameTransportAnalyzer",
]
