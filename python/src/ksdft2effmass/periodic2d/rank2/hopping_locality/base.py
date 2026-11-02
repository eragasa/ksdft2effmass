"""Periodic-2D rank-two hopping-locality ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic2d.hopping_locality.base import (
    Periodic2DHoppingLocality,
    Periodic2DHoppingLocalityAnalysis,
    Periodic2DHoppingLocalityAnalysisRequest,
    Periodic2DHoppingLocalityAnalyzer,
)


class _Periodic2DRank2BandSubspace:
    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the unchanged hopping-block rank."""
        return 2


class Periodic2DRank2HoppingLocalityCapability(Periodic2DHoppingLocality, ABC):
    """Identify unchanged periodic-2D rank-two hopping coefficients."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the unchanged hopping-block rank."""


class Periodic2DRank2HoppingLocalityAnalysisRequestRole(
    _Periodic2DRank2BandSubspace,
    Periodic2DHoppingLocalityAnalysisRequest,
    Periodic2DRank2HoppingLocalityCapability,
    ABC,
):
    """Bind one periodic-2D rank-two hopping-locality request."""

    __slots__ = ()


class Periodic2DRank2HoppingLocalityAnalysisRole(
    _Periodic2DRank2BandSubspace,
    Periodic2DHoppingLocalityAnalysis,
    Periodic2DRank2HoppingLocalityCapability,
    ABC,
):
    """Retain one periodic-2D rank-two hopping-locality analysis."""

    __slots__ = ()


class Periodic2DRank2HoppingLocalityAnalyzerRole[
    RequestT: Periodic2DRank2HoppingLocalityAnalysisRequestRole,
    AnalysisT: Periodic2DRank2HoppingLocalityAnalysisRole,
](
    _Periodic2DRank2BandSubspace,
    Periodic2DHoppingLocalityAnalyzer[RequestT, AnalysisT],
    Periodic2DRank2HoppingLocalityCapability,
    ABC,
):
    """Execute one periodic-2D rank-two hopping-locality request."""

    __slots__ = ()


__all__ = [
    "Periodic2DRank2HoppingLocalityAnalysisRequestRole",
    "Periodic2DRank2HoppingLocalityAnalysisRole",
    "Periodic2DRank2HoppingLocalityAnalyzerRole",
    "Periodic2DRank2HoppingLocalityCapability",
]
