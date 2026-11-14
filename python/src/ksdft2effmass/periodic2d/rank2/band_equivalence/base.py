"""Periodic-2D rank-two band-equivalence ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic2d.rankN.band_equivalence.base import (
    Periodic2DRankNBandEquivalence,
    Periodic2DRankNBandEquivalenceAnalysis,
    Periodic2DRankNBandEquivalenceAnalyzer,
    Periodic2DRankNBandEquivalenceRequest,
)


class _Periodic2DRank2BandSubspace:
    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the represented band subspace at each momentum."""
        return 2


class Periodic2DRank2BandEquivalence(
    Periodic2DRankNBandEquivalence,
    ABC,
):
    """Identify rank-two band equivalence on a periodic 2D lattice."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the represented band subspace at each momentum."""

    @property
    def band_subspace_ranks(self) -> tuple[int, ...]:
        """Return the one-entry represented rank inventory."""
        return (self.band_subspace_rank,)


class Periodic2DRank2BandEquivalenceRequest(
    _Periodic2DRank2BandSubspace,
    Periodic2DRankNBandEquivalenceRequest,
    Periodic2DRank2BandEquivalence,
    ABC,
):
    """Require rank-two ownership for periodic-2D requests."""

    __slots__ = ()


class Periodic2DRank2BandEquivalenceAnalysis[
    RequestT: Periodic2DRank2BandEquivalenceRequest,
](
    _Periodic2DRank2BandSubspace,
    Periodic2DRankNBandEquivalenceAnalysis[RequestT],
    Periodic2DRank2BandEquivalence,
    ABC,
):
    """Require rank-two ownership for periodic-2D analyses."""

    __slots__ = ()


class Periodic2DRank2BandEquivalenceAnalyzer[
    RequestT: Periodic2DRank2BandEquivalenceRequest,
](
    _Periodic2DRank2BandSubspace,
    Periodic2DRankNBandEquivalenceAnalyzer[RequestT],
    Periodic2DRank2BandEquivalence,
    ABC,
):
    """Require one concrete periodic-2D rank-two analysis action."""

    __slots__ = ()

    @abstractmethod
    def execute(self) -> Periodic2DRank2BandEquivalenceAnalysis[RequestT]:
        """Execute the bound rank-two analysis."""


__all__ = [
    "Periodic2DRank2BandEquivalence",
    "Periodic2DRank2BandEquivalenceAnalysis",
    "Periodic2DRank2BandEquivalenceAnalyzer",
    "Periodic2DRank2BandEquivalenceRequest",
]
