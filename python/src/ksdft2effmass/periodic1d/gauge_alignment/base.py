"""Periodic one-dimensional specialization of gauge alignment."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.gauge_alignment import (
    GaugeAlignment,
    GaugeAlignmentAnalysis,
    GaugeAlignmentAnalysisRequest,
    GaugeAlignmentAnalyzer,
)


class Periodic1DGaugeAlignment(GaugeAlignment):  # noqa: B024 - nominal owner
    """Identify a periodic-1D retained-space gauge-alignment capability.

    Concrete subclasses must declare the retained rank, gauge group, right- or
    left-action convention, reciprocal-coordinate domain, and applicability. The
    specialization owns no mesh, transport route, alignment algorithm, threshold,
    locality policy, or serialization format.
    """

    __slots__ = ()


class Periodic1DGaugeAlignmentAnalysisRequest(
    GaugeAlignmentAnalysisRequest,
    Periodic1DGaugeAlignment,
    ABC,
):
    """Bind one periodic-1D gauge-alignment analysis request."""

    __slots__ = ()


class Periodic1DGaugeAlignmentAnalysis(
    GaugeAlignmentAnalysis,
    Periodic1DGaugeAlignment,
    ABC,
):
    """Retain one periodic-1D gauge-alignment analysis."""

    __slots__ = ()


class Periodic1DGaugeAlignmentAnalyzer[
    Periodic1DGaugeAlignmentAnalysisRequestT: Periodic1DGaugeAlignmentAnalysisRequest,
    Periodic1DGaugeAlignmentAnalysisT: Periodic1DGaugeAlignmentAnalysis,
](
    GaugeAlignmentAnalyzer[
        Periodic1DGaugeAlignmentAnalysisRequestT,
        Periodic1DGaugeAlignmentAnalysisT,
    ],
    Periodic1DGaugeAlignment,
    ABC,
):
    """Execute one periodic-1D gauge-alignment analysis request."""

    __slots__ = ()


__all__ = [
    "Periodic1DGaugeAlignment",
    "Periodic1DGaugeAlignmentAnalysis",
    "Periodic1DGaugeAlignmentAnalysisRequest",
    "Periodic1DGaugeAlignmentAnalyzer",
]
