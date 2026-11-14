"""Periodic-1D arbitrary-rank hopping-locality ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.hopping_locality.base import PeriodicRankNHoppingLocalityCapability
from ksdft2effmass.periodic1d.hopping_locality.base import (
    Periodic1DHoppingLocality,
    Periodic1DHoppingLocalityAnalysis,
    Periodic1DHoppingLocalityAnalysisRequest,
    Periodic1DHoppingLocalityAnalyzer,
)


class Periodic1DRankNHoppingLocalityCapability(
    Periodic1DHoppingLocality,
    PeriodicRankNHoppingLocalityCapability,
    ABC,
):
    """Identify unchanged periodic-1D finite-rank hopping coefficients."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the unchanged hopping-block rank."""


class Periodic1DRankNHoppingLocalityAnalysisRequestRole(
    Periodic1DHoppingLocalityAnalysisRequest,
    Periodic1DRankNHoppingLocalityCapability,
    ABC,
):
    """Bind one periodic-1D arbitrary-rank hopping-locality request."""

    __slots__ = ()


class Periodic1DRankNHoppingLocalityAnalysisRole(
    Periodic1DHoppingLocalityAnalysis,
    Periodic1DRankNHoppingLocalityCapability,
    ABC,
):
    """Retain one periodic-1D arbitrary-rank hopping-locality analysis."""

    __slots__ = ()


class Periodic1DRankNHoppingLocalityAnalyzerRole[
    RequestT: Periodic1DRankNHoppingLocalityAnalysisRequestRole,
    AnalysisT: Periodic1DRankNHoppingLocalityAnalysisRole,
](
    Periodic1DHoppingLocalityAnalyzer[RequestT, AnalysisT],
    Periodic1DRankNHoppingLocalityCapability,
    ABC,
):
    """Execute one periodic-1D arbitrary-rank hopping-locality request."""

    __slots__ = ()

    @property
    def band_subspace_rank(self) -> int:
        """Return the unchanged hopping-block rank."""
        return self.request.band_subspace_rank


class Periodic1DRankNHoppingLocalityValue(
    Periodic1DRankNHoppingLocalityCapability,
    ABC,
):
    """Retain one standalone arbitrary-rank hopping-locality value."""

    __slots__ = ()


__all__ = [
    "Periodic1DRankNHoppingLocalityAnalysisRequestRole",
    "Periodic1DRankNHoppingLocalityAnalysisRole",
    "Periodic1DRankNHoppingLocalityAnalyzerRole",
    "Periodic1DRankNHoppingLocalityCapability",
    "Periodic1DRankNHoppingLocalityValue",
]
