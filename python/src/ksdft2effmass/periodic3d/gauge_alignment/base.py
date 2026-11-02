"""Periodic three-dimensional specialization of gauge alignment."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.gauge_alignment.base import (
    GaugeAlignment,
    GaugeAlignmentAnalysis,
    GaugeAlignmentAnalysisRequest,
    GaugeAlignmentAnalyzer,
)
from ksdft2effmass.periodic3d.base import Periodic3DCapability


class Periodic3DGaugeAlignment(
    GaugeAlignment,
    Periodic3DCapability,
):  # noqa: B024 - nominal owner
    """Identify a periodic-3D retained-space gauge-alignment capability.

    Concrete subclasses must declare the retained rank, gauge group, action
    convention, reciprocal-coordinate domain, and applicability. The lattice
    dimension is fixed without selecting a direct lattice, mesh, transport route,
    solver, threshold, locality policy, or serialization format.
    """

    __slots__ = ()


class Periodic3DGaugeAlignmentAnalysisRequest(
    GaugeAlignmentAnalysisRequest,
    Periodic3DGaugeAlignment,
    ABC,
):
    """Bind one periodic-3D gauge-alignment analysis request."""

    __slots__ = ()


class Periodic3DGaugeAlignmentAnalysis(
    GaugeAlignmentAnalysis,
    Periodic3DGaugeAlignment,
    ABC,
):
    """Retain one periodic-3D gauge-alignment analysis."""

    __slots__ = ()


class Periodic3DGaugeAlignmentAnalyzer[
    Periodic3DGaugeAlignmentAnalysisRequestT: Periodic3DGaugeAlignmentAnalysisRequest,
    Periodic3DGaugeAlignmentAnalysisT: Periodic3DGaugeAlignmentAnalysis,
](
    GaugeAlignmentAnalyzer[
        Periodic3DGaugeAlignmentAnalysisRequestT,
        Periodic3DGaugeAlignmentAnalysisT,
    ],
    Periodic3DGaugeAlignment,
    ABC,
):
    """Execute one periodic-3D gauge-alignment analysis request."""

    __slots__ = ()


__all__ = [
    "Periodic3DGaugeAlignment",
    "Periodic3DGaugeAlignmentAnalysis",
    "Periodic3DGaugeAlignmentAnalysisRequest",
    "Periodic3DGaugeAlignmentAnalyzer",
]
