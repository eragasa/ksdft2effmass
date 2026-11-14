"""Periodic three-dimensional specialization of Fourier analysis."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.fourier_analysis import (
    PeriodicFourierAnalysis,
    PeriodicFourierAnalysisRequest,
    PeriodicFourierAnalysisResult,
    PeriodicFourierAnalyzer,
)
from ksdft2effmass.periodic3d.base import Periodic3DCapability


class Periodic3DFourierAnalysis(
    PeriodicFourierAnalysis,
    Periodic3DCapability,
):  # noqa: B024 - intentionally nominal marker
    """Identify Fourier analysis on an explicit periodic-3D mesh topology."""

    __slots__ = ()


class Periodic3DFourierAnalysisRequest(
    PeriodicFourierAnalysisRequest,
    Periodic3DFourierAnalysis,
    ABC,
):
    """Bind one periodic-3D Fourier-analysis request."""

    __slots__ = ()


class Periodic3DFourierAnalysisResult(
    PeriodicFourierAnalysisResult,
    Periodic3DFourierAnalysis,
    ABC,
):
    """Retain one periodic-3D Fourier analysis."""

    __slots__ = ()


class Periodic3DFourierAnalyzer[
    RequestT: Periodic3DFourierAnalysisRequest,
    ResultT: Periodic3DFourierAnalysisResult,
](
    PeriodicFourierAnalyzer[RequestT, ResultT],
    Periodic3DFourierAnalysis,
    ABC,
):
    """Execute one periodic-3D Fourier-analysis request."""

    __slots__ = ()


__all__ = [
    "Periodic3DFourierAnalysis",
    "Periodic3DFourierAnalysisRequest",
    "Periodic3DFourierAnalysisResult",
    "Periodic3DFourierAnalyzer",
]
