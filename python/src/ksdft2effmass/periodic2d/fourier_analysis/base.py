"""Periodic two-dimensional specialization of Fourier analysis."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.fourier_analysis import (
    PeriodicFourierAnalysis,
    PeriodicFourierAnalysisRequest,
    PeriodicFourierAnalysisResult,
    PeriodicFourierAnalyzer,
)
from ksdft2effmass.periodic2d.base import Periodic2DCapability


class Periodic2DFourierAnalysis(
    PeriodicFourierAnalysis,
    Periodic2DCapability,
):  # noqa: B024 - intentionally nominal marker
    """Identify Fourier analysis on an explicit periodic-2D mesh topology."""

    __slots__ = ()


class Periodic2DFourierAnalysisRequest(
    PeriodicFourierAnalysisRequest,
    Periodic2DFourierAnalysis,
    ABC,
):
    """Bind one periodic-2D Fourier-analysis request."""

    __slots__ = ()


class Periodic2DFourierAnalysisResult(
    PeriodicFourierAnalysisResult,
    Periodic2DFourierAnalysis,
    ABC,
):
    """Retain one periodic-2D Fourier analysis."""

    __slots__ = ()


class Periodic2DFourierAnalyzer[
    RequestT: Periodic2DFourierAnalysisRequest,
    ResultT: Periodic2DFourierAnalysisResult,
](
    PeriodicFourierAnalyzer[RequestT, ResultT],
    Periodic2DFourierAnalysis,
    ABC,
):
    """Execute one periodic-2D Fourier-analysis request."""

    __slots__ = ()


__all__ = [
    "Periodic2DFourierAnalysis",
    "Periodic2DFourierAnalysisRequest",
    "Periodic2DFourierAnalysisResult",
    "Periodic2DFourierAnalyzer",
]
