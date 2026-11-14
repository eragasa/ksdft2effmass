"""Periodic-2D finite-rank interpolation ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.interpolation import PeriodicRankNInterpolationCapability
from ksdft2effmass.periodic2d.interpolation import (
    Periodic2DInterpolation,
    Periodic2DInterpolationAnalysis,
    Periodic2DInterpolationAnalysisRequest,
    Periodic2DInterpolationAnalyzer,
)


class Periodic2DRankNInterpolationCapability(
    Periodic2DInterpolation,
    PeriodicRankNInterpolationCapability,
    ABC,
):
    """Identify interpolation of periodic-2D finite-rank matrix fields."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the finite represented matrix rank."""


class Periodic2DRankNInterpolationAnalysisRequestRole(
    Periodic2DInterpolationAnalysisRequest,
    Periodic2DRankNInterpolationCapability,
    ABC,
):
    """Bind one periodic-2D finite-rank interpolation request."""

    __slots__ = ()


class Periodic2DRankNInterpolationAnalysisRole(
    Periodic2DInterpolationAnalysis,
    Periodic2DRankNInterpolationCapability,
    ABC,
):
    """Retain one periodic-2D finite-rank interpolation analysis."""

    __slots__ = ()


class Periodic2DRankNInterpolationAnalyzerRole[
    RequestT: Periodic2DRankNInterpolationAnalysisRequestRole,
    AnalysisT: Periodic2DRankNInterpolationAnalysisRole,
](
    Periodic2DInterpolationAnalyzer[RequestT, AnalysisT],
    Periodic2DRankNInterpolationCapability,
    ABC,
):
    """Execute one periodic-2D finite-rank interpolation request."""

    __slots__ = ()

    @property
    def band_subspace_rank(self) -> int:
        """Return the finite represented matrix rank."""
        return self.request.band_subspace_rank


__all__ = [
    "Periodic2DRankNInterpolationAnalysisRequestRole",
    "Periodic2DRankNInterpolationAnalysisRole",
    "Periodic2DRankNInterpolationAnalyzerRole",
    "Periodic2DRankNInterpolationCapability",
]
