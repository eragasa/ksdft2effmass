"""Periodic one-dimensional specialization of interpolation."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.interpolation import (
    PeriodicInterpolation,
    PeriodicInterpolationAnalysis,
    PeriodicInterpolationAnalysisRequest,
    PeriodicInterpolationAnalyzer,
)
from ksdft2effmass.periodic1d.base import Periodic1DCapability


class Periodic1DInterpolation(
    PeriodicInterpolation,
    Periodic1DCapability,
):  # noqa: B024 - intentionally nominal marker
    """Identify interpolation on an explicit periodic-1D coordinate inventory."""

    __slots__ = ()


class Periodic1DInterpolationAnalysisRequest(
    PeriodicInterpolationAnalysisRequest,
    Periodic1DInterpolation,
    ABC,
):
    """Bind one periodic-1D interpolation-analysis request."""

    __slots__ = ()


class Periodic1DInterpolationAnalysis(
    PeriodicInterpolationAnalysis,
    Periodic1DInterpolation,
    ABC,
):
    """Retain one periodic-1D interpolation analysis."""

    __slots__ = ()


class Periodic1DInterpolationAnalyzer[
    RequestT: Periodic1DInterpolationAnalysisRequest,
    AnalysisT: Periodic1DInterpolationAnalysis,
](
    PeriodicInterpolationAnalyzer[RequestT, AnalysisT],
    Periodic1DInterpolation,
    ABC,
):
    """Execute one periodic-1D interpolation-analysis request."""

    __slots__ = ()


__all__ = [
    "Periodic1DInterpolation",
    "Periodic1DInterpolationAnalysis",
    "Periodic1DInterpolationAnalysisRequest",
    "Periodic1DInterpolationAnalyzer",
]
