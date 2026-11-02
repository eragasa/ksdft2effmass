"""Periodic-1D rank-one band-equivalence ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic1d.band_equivalence.base import (
    Periodic1DBandEquivalence,
    Periodic1DBandEquivalenceAnalysis,
    Periodic1DBandEquivalenceAnalyzer,
    Periodic1DBandEquivalenceRequest,
)


class _Periodic1DRank1BandSubspace:
    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the represented band subspace at each momentum."""
        return 1


class Periodic1DRank1BandEquivalence(Periodic1DBandEquivalence, ABC):
    """Identify scalar band equivalence on a periodic one-dimensional lattice."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the represented band subspace at each momentum."""


class Periodic1DRank1BandEquivalenceRequest(
    _Periodic1DRank1BandSubspace,
    Periodic1DBandEquivalenceRequest,
    Periodic1DRank1BandEquivalence,
    ABC,
):
    """Require rank-one ownership for periodic-1D band-equivalence requests."""

    __slots__ = ()


class Periodic1DRank1BandEquivalenceAnalysis[
    RequestT: Periodic1DRank1BandEquivalenceRequest,
](
    _Periodic1DRank1BandSubspace,
    Periodic1DBandEquivalenceAnalysis[RequestT],
    Periodic1DRank1BandEquivalence,
    ABC,
):
    """Require rank-one ownership for periodic-1D band-equivalence analyses."""

    __slots__ = ()


class Periodic1DRank1BandEquivalenceAnalyzer[
    RequestT: Periodic1DRank1BandEquivalenceRequest,
](
    _Periodic1DRank1BandSubspace,
    Periodic1DBandEquivalenceAnalyzer[RequestT],
    Periodic1DRank1BandEquivalence,
    ABC,
):
    """Require one concrete rank-one analysis action."""

    __slots__ = ()

    @abstractmethod
    def execute(self) -> Periodic1DRank1BandEquivalenceAnalysis[RequestT]:
        """Execute the bound rank-one analysis."""


__all__ = [
    "Periodic1DRank1BandEquivalence",
    "Periodic1DRank1BandEquivalenceAnalysis",
    "Periodic1DRank1BandEquivalenceAnalyzer",
    "Periodic1DRank1BandEquivalenceRequest",
]
