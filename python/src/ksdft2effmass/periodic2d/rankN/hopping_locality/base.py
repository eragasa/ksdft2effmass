"""Periodic-2D arbitrary-rank hopping-locality ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic2d.hopping_locality.base import (
    Periodic2DHoppingLocality,
    Periodic2DHoppingLocalityAnalysis,
    Periodic2DHoppingLocalityAnalysisRequest,
    Periodic2DHoppingLocalityAnalyzer,
)


class Periodic2DRankNHoppingLocalityCapability(Periodic2DHoppingLocality, ABC):
    """Identify unchanged periodic-2D finite-rank hopping coefficients."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the unchanged hopping-block rank."""


class Periodic2DRankNHoppingLocalityAnalysisRequestRole(
    Periodic2DHoppingLocalityAnalysisRequest,
    Periodic2DRankNHoppingLocalityCapability,
    ABC,
):
    """Bind one periodic-2D arbitrary-rank hopping-locality request."""

    __slots__ = ()


class Periodic2DRankNHoppingLocalityAnalysisRole(
    Periodic2DHoppingLocalityAnalysis,
    Periodic2DRankNHoppingLocalityCapability,
    ABC,
):
    """Retain one periodic-2D arbitrary-rank hopping-locality analysis."""

    __slots__ = ()


class Periodic2DRankNHoppingLocalityAnalyzerRole[
    RequestT: Periodic2DRankNHoppingLocalityAnalysisRequestRole,
    AnalysisT: Periodic2DRankNHoppingLocalityAnalysisRole,
](
    Periodic2DHoppingLocalityAnalyzer[RequestT, AnalysisT],
    Periodic2DRankNHoppingLocalityCapability,
    ABC,
):
    """Execute one periodic-2D arbitrary-rank hopping-locality request."""

    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the unchanged hopping-block rank."""
        return self.request.band_subspace_rank


__all__ = [
    "Periodic2DRankNHoppingLocalityAnalysisRequestRole",
    "Periodic2DRankNHoppingLocalityAnalysisRole",
    "Periodic2DRankNHoppingLocalityAnalyzerRole",
    "Periodic2DRankNHoppingLocalityCapability",
]
