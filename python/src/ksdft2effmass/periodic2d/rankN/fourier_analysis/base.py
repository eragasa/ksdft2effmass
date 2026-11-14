"""Periodic-2D finite-rank Fourier-analysis ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.fourier_analysis import PeriodicRankNFourierAnalysisCapability
from ksdft2effmass.periodic2d.fourier_analysis import (
    Periodic2DFourierAnalysis,
    Periodic2DFourierAnalysisRequest,
    Periodic2DFourierAnalysisResult,
    Periodic2DFourierAnalyzer,
)


class Periodic2DRankNFourierAnalysisCapability(
    Periodic2DFourierAnalysis,
    PeriodicRankNFourierAnalysisCapability,
    ABC,
):
    """Identify Fourier analysis of periodic-2D finite-rank matrix fields."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the finite represented matrix rank."""


class Periodic2DRankNFourierAnalysisRequestRole(
    Periodic2DFourierAnalysisRequest,
    Periodic2DRankNFourierAnalysisCapability,
    ABC,
):
    """Bind one periodic-2D finite-rank Fourier-analysis request."""

    __slots__ = ()


class Periodic2DRankNFourierAnalysisRole(
    Periodic2DFourierAnalysisResult,
    Periodic2DRankNFourierAnalysisCapability,
    ABC,
):
    """Retain one periodic-2D finite-rank Fourier analysis."""

    __slots__ = ()


class Periodic2DRankNFourierAnalyzerRole[
    RequestT: Periodic2DRankNFourierAnalysisRequestRole,
    ResultT: Periodic2DRankNFourierAnalysisRole,
](
    Periodic2DFourierAnalyzer[RequestT, ResultT],
    Periodic2DRankNFourierAnalysisCapability,
    ABC,
):
    """Execute one periodic-2D finite-rank Fourier-analysis request."""

    __slots__ = ()

    @property
    def band_subspace_rank(self) -> int:
        """Return the finite represented matrix rank."""
        return self.request.band_subspace_rank


__all__ = [
    "Periodic2DRankNFourierAnalysisCapability",
    "Periodic2DRankNFourierAnalysisRequestRole",
    "Periodic2DRankNFourierAnalysisRole",
    "Periodic2DRankNFourierAnalyzerRole",
]
