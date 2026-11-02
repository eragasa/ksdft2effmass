"""Periodic one-dimensional specialization of frame transport."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.frame_transport.base import (
    PeriodicFrameTransport,
    PeriodicFrameTransportAnalysis,
    PeriodicFrameTransportAnalysisRequest,
    PeriodicFrameTransportAnalyzer,
)
from ksdft2effmass.periodic1d.base import Periodic1DCapability


class Periodic1DFrameTransport(
    PeriodicFrameTransport,
    Periodic1DCapability,
    ABC,
):
    """Identify frame transport on a one-dimensional periodic lattice."""

    __slots__ = ()


class Periodic1DFrameTransportAnalysisRequest(
    PeriodicFrameTransportAnalysisRequest,
    Periodic1DFrameTransport,
    ABC,
):
    """Bind one periodic-1D frame-transport request."""

    __slots__ = ()


class Periodic1DFrameTransportAnalysis(
    PeriodicFrameTransportAnalysis,
    Periodic1DFrameTransport,
    ABC,
):
    """Retain one periodic-1D frame-transport outcome."""

    __slots__ = ()


class Periodic1DFrameTransportAnalyzer[
    RequestT: Periodic1DFrameTransportAnalysisRequest,
    AnalysisT: Periodic1DFrameTransportAnalysis,
](
    PeriodicFrameTransportAnalyzer[RequestT, AnalysisT],
    Periodic1DFrameTransport,
    ABC,
):
    """Execute one periodic-1D frame-transport request."""

    __slots__ = ()


__all__ = [
    "Periodic1DFrameTransport",
    "Periodic1DFrameTransportAnalysis",
    "Periodic1DFrameTransportAnalysisRequest",
    "Periodic1DFrameTransportAnalyzer",
]
