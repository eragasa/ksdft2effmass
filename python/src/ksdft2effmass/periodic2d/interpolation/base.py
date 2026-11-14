"""Periodic two-dimensional specialization of interpolation."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.interpolation import (
    PeriodicInterpolation,
    PeriodicInterpolationAnalysis,
    PeriodicInterpolationAnalysisRequest,
    PeriodicInterpolationAnalyzer,
)
from ksdft2effmass.periodic2d.base import Periodic2DCapability


class Periodic2DInterpolation(
    PeriodicInterpolation,
    Periodic2DCapability,
):  # noqa: B024 - intentionally nominal marker
    """Identify interpolation on an explicit periodic-2D mesh topology."""

    __slots__ = ()


class Periodic2DInterpolationAnalysisRequest(
    PeriodicInterpolationAnalysisRequest,
    Periodic2DInterpolation,
    ABC,
):
    """Bind one periodic-2D interpolation request."""

    __slots__ = ()


class Periodic2DInterpolationAnalysis(
    PeriodicInterpolationAnalysis,
    Periodic2DInterpolation,
    ABC,
):
    """Retain one periodic-2D interpolation analysis."""

    __slots__ = ()


class Periodic2DInterpolationAnalyzer[
    RequestT: Periodic2DInterpolationAnalysisRequest,
    AnalysisT: Periodic2DInterpolationAnalysis,
](
    PeriodicInterpolationAnalyzer[RequestT, AnalysisT],
    Periodic2DInterpolation,
    ABC,
):
    """Execute one periodic-2D interpolation request."""

    __slots__ = ()


__all__ = [
    "Periodic2DInterpolation",
    "Periodic2DInterpolationAnalysis",
    "Periodic2DInterpolationAnalysisRequest",
    "Periodic2DInterpolationAnalyzer",
]
