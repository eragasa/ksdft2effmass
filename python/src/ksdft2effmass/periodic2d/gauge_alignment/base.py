"""Periodic two-dimensional specialization of gauge alignment."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.gauge_alignment.base import (
    GaugeAlignmentAnalysis,
    GaugeAlignmentAnalysisRequest,
    GaugeAlignmentAnalyzer,
    PeriodicGaugeAlignment,
)
from ksdft2effmass.periodic2d.base import Periodic2DCapability


class Periodic2DGaugeAlignment(
    PeriodicGaugeAlignment,
    Periodic2DCapability,
):  # noqa: B024 - nominal owner
    """Identify a periodic-2D retained-space gauge-alignment capability.

    Concrete subclasses must declare the retained rank, gauge group, action
    convention, reciprocal-coordinate domain, and applicability. The lattice
    dimension is fixed without selecting a direct lattice, mesh, transport route,
    solver, threshold, locality policy, or serialization format.
    """

    __slots__ = ()


class Periodic2DGaugeAlignmentAnalysisRequest(
    GaugeAlignmentAnalysisRequest,
    Periodic2DGaugeAlignment,
    ABC,
):
    """Bind one periodic-2D gauge-alignment analysis request."""

    __slots__ = ()


class Periodic2DGaugeAlignmentAnalysis(
    GaugeAlignmentAnalysis,
    Periodic2DGaugeAlignment,
    ABC,
):
    """Retain one periodic-2D gauge-alignment analysis."""

    __slots__ = ()


class Periodic2DGaugeAlignmentAnalyzer[
    Periodic2DGaugeAlignmentAnalysisRequestT: Periodic2DGaugeAlignmentAnalysisRequest,
    Periodic2DGaugeAlignmentAnalysisT: Periodic2DGaugeAlignmentAnalysis,
](
    GaugeAlignmentAnalyzer[
        Periodic2DGaugeAlignmentAnalysisRequestT,
        Periodic2DGaugeAlignmentAnalysisT,
    ],
    Periodic2DGaugeAlignment,
    ABC,
):
    """Execute one periodic-2D gauge-alignment analysis request."""

    __slots__ = ()


__all__ = [
    "Periodic2DGaugeAlignment",
    "Periodic2DGaugeAlignmentAnalysis",
    "Periodic2DGaugeAlignmentAnalysisRequest",
    "Periodic2DGaugeAlignmentAnalyzer",
]
