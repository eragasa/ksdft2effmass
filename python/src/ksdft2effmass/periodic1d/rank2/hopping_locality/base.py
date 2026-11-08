"""Periodic-1D rank-two hopping-locality ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic1d.rankN.hopping_locality.base import (
    Periodic1DRankNHoppingLocalityAnalysisRequestRole,
    Periodic1DRankNHoppingLocalityAnalysisRole,
    Periodic1DRankNHoppingLocalityAnalyzerRole,
    Periodic1DRankNHoppingLocalityCapability,
    Periodic1DRankNHoppingLocalityValue,
)


class _Periodic1DRank2BandSubspace:
    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the unchanged hopping-block rank."""
        return 2


class Periodic1DRank2HoppingLocalityCapability(
    Periodic1DRankNHoppingLocalityCapability,
    ABC,
):
    """Identify unchanged periodic-1D rank-two hopping coefficients."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the unchanged hopping-block rank."""


class Periodic1DRank2HoppingLocalityAnalysisRequestRole(
    _Periodic1DRank2BandSubspace,
    Periodic1DRankNHoppingLocalityAnalysisRequestRole,
    Periodic1DRank2HoppingLocalityCapability,
    ABC,
):
    """Bind one periodic-1D rank-two hopping-locality request."""

    __slots__ = ()


class Periodic1DRank2HoppingLocalityAnalysisRole(
    _Periodic1DRank2BandSubspace,
    Periodic1DRankNHoppingLocalityAnalysisRole,
    Periodic1DRank2HoppingLocalityCapability,
    ABC,
):
    """Retain one periodic-1D rank-two hopping-locality analysis."""

    __slots__ = ()


class Periodic1DRank2HoppingLocalityAnalyzerRole[
    RequestT: Periodic1DRank2HoppingLocalityAnalysisRequestRole,
    AnalysisT: Periodic1DRank2HoppingLocalityAnalysisRole,
](
    _Periodic1DRank2BandSubspace,
    Periodic1DRankNHoppingLocalityAnalyzerRole[RequestT, AnalysisT],
    Periodic1DRank2HoppingLocalityCapability,
    ABC,
):
    """Execute one periodic-1D rank-two hopping-locality request."""

    __slots__ = ()


class Periodic1DRank2HoppingLocalityValue(
    _Periodic1DRank2BandSubspace,
    Periodic1DRankNHoppingLocalityValue,
    Periodic1DRank2HoppingLocalityCapability,
    ABC,
):
    """Retain one standalone rank-two hopping-locality value."""

    __slots__ = ()


__all__ = [
    "Periodic1DRank2HoppingLocalityAnalysisRequestRole",
    "Periodic1DRank2HoppingLocalityAnalysisRole",
    "Periodic1DRank2HoppingLocalityAnalyzerRole",
    "Periodic1DRank2HoppingLocalityCapability",
    "Periodic1DRank2HoppingLocalityValue",
]
