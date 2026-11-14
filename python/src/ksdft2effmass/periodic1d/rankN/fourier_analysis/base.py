"""Periodic-1D finite-rank Fourier-analysis ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.fourier_analysis import PeriodicRankNFourierAnalysisCapability
from ksdft2effmass.periodic1d.fourier_analysis import (
    Periodic1DFourierAnalysis,
    Periodic1DFourierAnalysisRequest,
    Periodic1DFourierAnalysisResult,
    Periodic1DFourierAnalyzer,
)


class Periodic1DRankNFourierAnalysisCapability(
    Periodic1DFourierAnalysis,
    PeriodicRankNFourierAnalysisCapability,
    ABC,
):
    """Identify Fourier analysis of periodic-1D finite-rank matrix fields."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the finite represented matrix rank."""


class Periodic1DRankNFourierAnalysisRequestRole(
    Periodic1DFourierAnalysisRequest,
    Periodic1DRankNFourierAnalysisCapability,
    ABC,
):
    """Bind one periodic-1D finite-rank Fourier-analysis request."""

    __slots__ = ()


class Periodic1DRankNFourierAnalysisRole(
    Periodic1DFourierAnalysisResult,
    Periodic1DRankNFourierAnalysisCapability,
    ABC,
):
    """Retain one periodic-1D finite-rank Fourier analysis."""

    __slots__ = ()


class Periodic1DRankNFourierAnalyzerRole[
    RequestT: Periodic1DRankNFourierAnalysisRequestRole,
    ResultT: Periodic1DRankNFourierAnalysisRole,
](
    Periodic1DFourierAnalyzer[RequestT, ResultT],
    Periodic1DRankNFourierAnalysisCapability,
    ABC,
):
    """Execute one periodic-1D finite-rank Fourier-analysis request."""

    __slots__ = ()

    @property
    def band_subspace_rank(self) -> int:
        """Return the finite represented matrix rank."""
        return self.request.band_subspace_rank


__all__ = [
    "Periodic1DRankNFourierAnalysisCapability",
    "Periodic1DRankNFourierAnalysisRequestRole",
    "Periodic1DRankNFourierAnalysisRole",
    "Periodic1DRankNFourierAnalyzerRole",
]
