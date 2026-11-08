"""Periodic-1D finite-rank interpolation ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.interpolation import PeriodicRankNInterpolationCapability
from ksdft2effmass.periodic1d.interpolation import (
    Periodic1DInterpolation,
    Periodic1DInterpolationAnalysis,
    Periodic1DInterpolationAnalysisRequest,
    Periodic1DInterpolationAnalyzer,
)


class Periodic1DRankNInterpolationCapability(
    Periodic1DInterpolation,
    PeriodicRankNInterpolationCapability,
    ABC,
):
    """Identify interpolation of periodic-1D finite-rank matrix fields."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the finite represented matrix rank."""


class Periodic1DRankNInterpolationAnalysisRequestRole(
    Periodic1DInterpolationAnalysisRequest,
    Periodic1DRankNInterpolationCapability,
    ABC,
):
    """Bind one periodic-1D finite-rank interpolation request."""

    __slots__ = ()


class Periodic1DRankNInterpolationAnalysisRole(
    Periodic1DInterpolationAnalysis,
    Periodic1DRankNInterpolationCapability,
    ABC,
):
    """Retain one periodic-1D finite-rank interpolation analysis."""

    __slots__ = ()


class Periodic1DRankNInterpolationAnalyzerRole[
    RequestT: Periodic1DRankNInterpolationAnalysisRequestRole,
    AnalysisT: Periodic1DRankNInterpolationAnalysisRole,
](
    Periodic1DInterpolationAnalyzer[RequestT, AnalysisT],
    Periodic1DRankNInterpolationCapability,
    ABC,
):
    """Execute one periodic-1D finite-rank interpolation request."""

    __slots__ = ()

    @property
    def band_subspace_rank(self) -> int:
        """Return the finite represented matrix rank."""
        return self.request.band_subspace_rank


__all__ = [
    "Periodic1DRankNInterpolationAnalysisRequestRole",
    "Periodic1DRankNInterpolationAnalysisRole",
    "Periodic1DRankNInterpolationAnalyzerRole",
    "Periodic1DRankNInterpolationCapability",
]
