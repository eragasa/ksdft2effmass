"""Periodic two-dimensional specialization of interpolation."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.interpolation import (
    PeriodicInterpolation,
    PeriodicInterpolationAnalysis,
    PeriodicInterpolationAnalysisRequest,
    PeriodicInterpolationAnalyzer,
)
from ksdft2effmass.periodic3d.base import Periodic3DCapability


class Periodic3DInterpolation(
    PeriodicInterpolation,
    Periodic3DCapability,
):  # noqa: B024 - intentionally nominal marker
    """Identify interpolation on an explicit periodic-3D mesh topology."""

    __slots__ = ()


class Periodic3DInterpolationAnalysisRequest(
    PeriodicInterpolationAnalysisRequest,
    Periodic3DInterpolation,
    ABC,
):
    """Bind one periodic-3D interpolation request."""

    __slots__ = ()


class Periodic3DInterpolationAnalysis(
    PeriodicInterpolationAnalysis,
    Periodic3DInterpolation,
    ABC,
):
    """Retain one periodic-3D interpolation analysis."""

    __slots__ = ()


class Periodic3DInterpolationAnalyzer[
    RequestT: Periodic3DInterpolationAnalysisRequest,
    AnalysisT: Periodic3DInterpolationAnalysis,
](
    PeriodicInterpolationAnalyzer[RequestT, AnalysisT],
    Periodic3DInterpolation,
    ABC,
):
    """Execute one periodic-3D interpolation request."""

    __slots__ = ()


__all__ = [
    "Periodic3DInterpolation",
    "Periodic3DInterpolationAnalysis",
    "Periodic3DInterpolationAnalysisRequest",
    "Periodic3DInterpolationAnalyzer",
]
