"""Periodic-3D rank-two band-equivalence ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic3d.rankN.band_equivalence.base import (
    Periodic3DRankNBandEquivalence,
    Periodic3DRankNBandEquivalenceAnalysis,
    Periodic3DRankNBandEquivalenceAnalyzer,
    Periodic3DRankNBandEquivalenceRequest,
)


class _Periodic3DRank2BandSubspace:
    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the represented band subspace at each momentum."""
        return 2


class Periodic3DRank2BandEquivalence(
    Periodic3DRankNBandEquivalence,
    ABC,
):
    """Identify rank-two band equivalence on a periodic 3D lattice."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the represented band subspace at each momentum."""

    @property
    def band_subspace_ranks(self) -> tuple[int, ...]:
        """Return the one-entry represented rank inventory."""
        return (self.band_subspace_rank,)


class Periodic3DRank2BandEquivalenceRequest(
    _Periodic3DRank2BandSubspace,
    Periodic3DRankNBandEquivalenceRequest,
    Periodic3DRank2BandEquivalence,
    ABC,
):
    """Require rank-two ownership for periodic-3D requests."""

    __slots__ = ()


class Periodic3DRank2BandEquivalenceAnalysis[
    RequestT: Periodic3DRank2BandEquivalenceRequest,
](
    _Periodic3DRank2BandSubspace,
    Periodic3DRankNBandEquivalenceAnalysis[RequestT],
    Periodic3DRank2BandEquivalence,
    ABC,
):
    """Require rank-two ownership for periodic-3D analyses."""

    __slots__ = ()


class Periodic3DRank2BandEquivalenceAnalyzer[
    RequestT: Periodic3DRank2BandEquivalenceRequest,
](
    _Periodic3DRank2BandSubspace,
    Periodic3DRankNBandEquivalenceAnalyzer[RequestT],
    Periodic3DRank2BandEquivalence,
    ABC,
):
    """Require one concrete periodic-3D rank-two analysis action."""

    __slots__ = ()

    @abstractmethod
    def execute(self) -> Periodic3DRank2BandEquivalenceAnalysis[RequestT]:
        """Execute the bound rank-two analysis."""


__all__ = [
    "Periodic3DRank2BandEquivalence",
    "Periodic3DRank2BandEquivalenceAnalysis",
    "Periodic3DRank2BandEquivalenceAnalyzer",
    "Periodic3DRank2BandEquivalenceRequest",
]
