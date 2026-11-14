"""Periodic-3D finite-rank Fourier-analysis ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.fourier_analysis import PeriodicRankNFourierAnalysisCapability
from ksdft2effmass.periodic3d.fourier_analysis import (
    Periodic3DFourierAnalysis,
    Periodic3DFourierAnalysisRequest,
    Periodic3DFourierAnalysisResult,
    Periodic3DFourierAnalyzer,
)


class Periodic3DRankNFourierAnalysisCapability(
    Periodic3DFourierAnalysis,
    PeriodicRankNFourierAnalysisCapability,
    ABC,
):
    """Identify Fourier analysis of periodic-3D finite-rank matrix fields."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the finite represented matrix rank."""


class Periodic3DRankNFourierAnalysisRequestRole(
    Periodic3DFourierAnalysisRequest,
    Periodic3DRankNFourierAnalysisCapability,
    ABC,
):
    """Bind one periodic-3D finite-rank Fourier-analysis request."""

    __slots__ = ()


class Periodic3DRankNFourierAnalysisRole(
    Periodic3DFourierAnalysisResult,
    Periodic3DRankNFourierAnalysisCapability,
    ABC,
):
    """Retain one periodic-3D finite-rank Fourier analysis."""

    __slots__ = ()


class Periodic3DRankNFourierAnalyzerRole[
    RequestT: Periodic3DRankNFourierAnalysisRequestRole,
    ResultT: Periodic3DRankNFourierAnalysisRole,
](
    Periodic3DFourierAnalyzer[RequestT, ResultT],
    Periodic3DRankNFourierAnalysisCapability,
    ABC,
):
    """Execute one periodic-3D finite-rank Fourier-analysis request."""

    __slots__ = ()

    @property
    def band_subspace_rank(self) -> int:
        """Return the finite represented matrix rank."""
        return self.request.band_subspace_rank


__all__ = [
    "Periodic3DRankNFourierAnalysisCapability",
    "Periodic3DRankNFourierAnalysisRequestRole",
    "Periodic3DRankNFourierAnalysisRole",
    "Periodic3DRankNFourierAnalyzerRole",
]
