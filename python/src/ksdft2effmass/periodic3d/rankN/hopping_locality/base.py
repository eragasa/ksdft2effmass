"""Periodic-3D arbitrary-rank hopping-locality ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.hopping_locality.base import PeriodicRankNHoppingLocalityCapability
from ksdft2effmass.periodic3d.hopping_locality.base import (
    Periodic3DHoppingLocality,
    Periodic3DHoppingLocalityAnalysis,
    Periodic3DHoppingLocalityAnalysisRequest,
    Periodic3DHoppingLocalityAnalyzer,
)


class Periodic3DRankNHoppingLocalityCapability(
    Periodic3DHoppingLocality,
    PeriodicRankNHoppingLocalityCapability,
    ABC,
):
    """Identify unchanged periodic-3D finite-rank hopping coefficients."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the unchanged hopping-block rank."""


class Periodic3DRankNHoppingLocalityAnalysisRequestRole(
    Periodic3DHoppingLocalityAnalysisRequest,
    Periodic3DRankNHoppingLocalityCapability,
    ABC,
):
    """Bind one periodic-3D arbitrary-rank hopping-locality request."""

    __slots__ = ()


class Periodic3DRankNHoppingLocalityAnalysisRole(
    Periodic3DHoppingLocalityAnalysis,
    Periodic3DRankNHoppingLocalityCapability,
    ABC,
):
    """Retain one periodic-3D arbitrary-rank hopping-locality analysis."""

    __slots__ = ()


class Periodic3DRankNHoppingLocalityAnalyzerRole[
    RequestT: Periodic3DRankNHoppingLocalityAnalysisRequestRole,
    AnalysisT: Periodic3DRankNHoppingLocalityAnalysisRole,
](
    Periodic3DHoppingLocalityAnalyzer[RequestT, AnalysisT],
    Periodic3DRankNHoppingLocalityCapability,
    ABC,
):
    """Execute one periodic-3D arbitrary-rank hopping-locality request."""

    __slots__ = ()

    @property
    def band_subspace_rank(self) -> int:
        """Return the unchanged hopping-block rank."""
        return self.request.band_subspace_rank


__all__ = [
    "Periodic3DRankNHoppingLocalityAnalysisRequestRole",
    "Periodic3DRankNHoppingLocalityAnalysisRole",
    "Periodic3DRankNHoppingLocalityAnalyzerRole",
    "Periodic3DRankNHoppingLocalityCapability",
]
