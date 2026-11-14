"""Periodic one-dimensional specialization of Fourier analysis."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.fourier_analysis import (
    PeriodicFourierAnalysis,
    PeriodicFourierAnalysisRequest,
    PeriodicFourierAnalysisResult,
    PeriodicFourierAnalyzer,
)
from ksdft2effmass.periodic1d.base import Periodic1DCapability


class Periodic1DFourierAnalysis(
    PeriodicFourierAnalysis,
    Periodic1DCapability,
):  # noqa: B024 - intentionally nominal marker
    """Identify Fourier analysis on an explicit periodic-1D sample inventory."""

    __slots__ = ()


class Periodic1DFourierAnalysisRequest(
    PeriodicFourierAnalysisRequest,
    Periodic1DFourierAnalysis,
    ABC,
):
    """Bind one periodic-1D Fourier-analysis request."""

    __slots__ = ()


class Periodic1DFourierAnalysisResult(
    PeriodicFourierAnalysisResult,
    Periodic1DFourierAnalysis,
    ABC,
):
    """Retain one periodic-1D Fourier analysis."""

    __slots__ = ()


class Periodic1DFourierAnalyzer[
    RequestT: Periodic1DFourierAnalysisRequest,
    ResultT: Periodic1DFourierAnalysisResult,
](
    PeriodicFourierAnalyzer[RequestT, ResultT],
    Periodic1DFourierAnalysis,
    ABC,
):
    """Execute one periodic-1D Fourier-analysis request."""

    __slots__ = ()


__all__ = [
    "Periodic1DFourierAnalysis",
    "Periodic1DFourierAnalysisRequest",
    "Periodic1DFourierAnalysisResult",
    "Periodic1DFourierAnalyzer",
]
