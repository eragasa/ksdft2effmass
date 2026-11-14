"""Periodic-3D finite-rank interpolation ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.interpolation import PeriodicRankNInterpolationCapability
from ksdft2effmass.periodic3d.interpolation import (
    Periodic3DInterpolation,
    Periodic3DInterpolationAnalysis,
    Periodic3DInterpolationAnalysisRequest,
    Periodic3DInterpolationAnalyzer,
)


class Periodic3DRankNInterpolationCapability(
    Periodic3DInterpolation,
    PeriodicRankNInterpolationCapability,
    ABC,
):
    """Identify interpolation of periodic-3D finite-rank matrix fields."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the finite represented matrix rank."""


class Periodic3DRankNInterpolationAnalysisRequestRole(
    Periodic3DInterpolationAnalysisRequest,
    Periodic3DRankNInterpolationCapability,
    ABC,
):
    """Bind one periodic-3D finite-rank interpolation request."""

    __slots__ = ()


class Periodic3DRankNInterpolationAnalysisRole(
    Periodic3DInterpolationAnalysis,
    Periodic3DRankNInterpolationCapability,
    ABC,
):
    """Retain one periodic-3D finite-rank interpolation analysis."""

    __slots__ = ()


class Periodic3DRankNInterpolationAnalyzerRole[
    RequestT: Periodic3DRankNInterpolationAnalysisRequestRole,
    AnalysisT: Periodic3DRankNInterpolationAnalysisRole,
](
    Periodic3DInterpolationAnalyzer[RequestT, AnalysisT],
    Periodic3DRankNInterpolationCapability,
    ABC,
):
    """Execute one periodic-3D finite-rank interpolation request."""

    __slots__ = ()

    @property
    def band_subspace_rank(self) -> int:
        """Return the finite represented matrix rank."""
        return self.request.band_subspace_rank


__all__ = [
    "Periodic3DRankNInterpolationAnalysisRequestRole",
    "Periodic3DRankNInterpolationAnalysisRole",
    "Periodic3DRankNInterpolationAnalyzerRole",
    "Periodic3DRankNInterpolationCapability",
]
