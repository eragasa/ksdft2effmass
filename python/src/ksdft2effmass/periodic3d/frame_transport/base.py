"""Periodic three-dimensional specialization of frame transport."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.frame_transport.base import (
    PeriodicFrameTransport,
    PeriodicFrameTransportAnalysis,
    PeriodicFrameTransportAnalysisRequest,
    PeriodicFrameTransportAnalyzer,
)
from ksdft2effmass.periodic3d.base import Periodic3DCapability


class Periodic3DFrameTransport(
    PeriodicFrameTransport,
    Periodic3DCapability,
    ABC,
):
    """Identify frame transport on a three-dimensional periodic lattice."""

    __slots__ = ()


class Periodic3DFrameTransportAnalysisRequest(
    PeriodicFrameTransportAnalysisRequest,
    Periodic3DFrameTransport,
    ABC,
):
    """Bind one periodic-3D frame-transport request."""

    __slots__ = ()


class Periodic3DFrameTransportAnalysis(
    PeriodicFrameTransportAnalysis,
    Periodic3DFrameTransport,
    ABC,
):
    """Retain one periodic-3D frame-transport outcome."""

    __slots__ = ()


class Periodic3DFrameTransportAnalyzer[
    RequestT: Periodic3DFrameTransportAnalysisRequest,
    AnalysisT: Periodic3DFrameTransportAnalysis,
](
    PeriodicFrameTransportAnalyzer[RequestT, AnalysisT],
    Periodic3DFrameTransport,
    ABC,
):
    """Execute one periodic-3D frame-transport request."""

    __slots__ = ()


__all__ = [
    "Periodic3DFrameTransport",
    "Periodic3DFrameTransportAnalysis",
    "Periodic3DFrameTransportAnalysisRequest",
    "Periodic3DFrameTransportAnalyzer",
]
