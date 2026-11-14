"""Periodic-1D rank-two band-equivalence ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic1d.rankN.band_equivalence.base import (
    Periodic1DRankNBandEquivalence,
    Periodic1DRankNBandEquivalenceAnalysis,
    Periodic1DRankNBandEquivalenceAnalyzer,
    Periodic1DRankNBandEquivalenceRequest,
)


class _Periodic1DRank2BandSubspace:
    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the represented band subspace at each momentum."""
        return 2


class Periodic1DRank2BandEquivalence(
    Periodic1DRankNBandEquivalence,
    ABC,
):
    """Identify rank-two band equivalence on a periodic one-dimensional lattice."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the represented band subspace at each momentum."""

    @property
    def band_subspace_ranks(self) -> tuple[int, ...]:
        """Return the one-entry represented rank inventory."""
        return (self.band_subspace_rank,)


class Periodic1DRank2BandEquivalenceRequest(
    _Periodic1DRank2BandSubspace,
    Periodic1DRankNBandEquivalenceRequest,
    Periodic1DRank2BandEquivalence,
    ABC,
):
    """Require rank-two ownership for periodic-1D band-equivalence requests."""

    __slots__ = ()


class Periodic1DRank2BandEquivalenceAnalysis[
    RequestT: Periodic1DRank2BandEquivalenceRequest,
](
    _Periodic1DRank2BandSubspace,
    Periodic1DRankNBandEquivalenceAnalysis[RequestT],
    Periodic1DRank2BandEquivalence,
    ABC,
):
    """Require rank-two ownership for periodic-1D band-equivalence analyses."""

    __slots__ = ()


class Periodic1DRank2BandEquivalenceAnalyzer[
    RequestT: Periodic1DRank2BandEquivalenceRequest,
](
    _Periodic1DRank2BandSubspace,
    Periodic1DRankNBandEquivalenceAnalyzer[RequestT],
    Periodic1DRank2BandEquivalence,
    ABC,
):
    """Require one concrete rank-two analysis action."""

    __slots__ = ()

    @abstractmethod
    def execute(self) -> Periodic1DRank2BandEquivalenceAnalysis[RequestT]:
        """Execute the bound rank-two analysis."""


__all__ = [
    "Periodic1DRank2BandEquivalence",
    "Periodic1DRank2BandEquivalenceAnalysis",
    "Periodic1DRank2BandEquivalenceAnalyzer",
    "Periodic1DRank2BandEquivalenceRequest",
]
