"""Periodic-1D rank-N band-equivalence ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.periodic1d.band_equivalence.base import (
    Periodic1DBandEquivalence,
    Periodic1DBandEquivalenceAnalysis,
    Periodic1DBandEquivalenceAnalyzer,
    Periodic1DBandEquivalenceRequest,
)


class Periodic1DRankNBandEquivalence(Periodic1DBandEquivalence, ABC):
    """Identify arbitrary-rank band equivalence on a periodic 1D lattice."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_ranks(self) -> tuple[int, ...]:
        """Return the represented band-subspace rank inventory."""


class Periodic1DRankNBandEquivalenceRequest(
    Periodic1DBandEquivalenceRequest,
    Periodic1DRankNBandEquivalence,
    ABC,
):
    """Require rank-N ownership for periodic-1D band-equivalence requests."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_ranks(self) -> tuple[int, ...]:
        """Return the requested band-subspace rank inventory."""


class Periodic1DRankNBandEquivalenceAnalysis[
    RequestT: Periodic1DRankNBandEquivalenceRequest,
](
    Periodic1DBandEquivalenceAnalysis[RequestT],
    Periodic1DRankNBandEquivalence,
    ABC,
):
    """Require rank-N ownership for periodic-1D band-equivalence analyses."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_ranks(self) -> tuple[int, ...]:
        """Return the analyzed band-subspace rank inventory."""


class Periodic1DRankNBandEquivalenceAnalyzer[
    RequestT: Periodic1DRankNBandEquivalenceRequest,
](
    Periodic1DBandEquivalenceAnalyzer[RequestT],
    Periodic1DRankNBandEquivalence,
    ABC,
):
    """Require one concrete arbitrary-rank analysis action."""

    __slots__ = ()

    @property
    def band_subspace_ranks(self) -> tuple[int, ...]:
        """Return the bound request's band-subspace rank inventory."""
        return self.request.band_subspace_ranks

    @abstractmethod
    def execute(self) -> Periodic1DRankNBandEquivalenceAnalysis[RequestT]:
        """Execute the bound arbitrary-rank analysis."""


__all__ = [
    "Periodic1DRankNBandEquivalence",
    "Periodic1DRankNBandEquivalenceAnalysis",
    "Periodic1DRankNBandEquivalenceAnalyzer",
    "Periodic1DRankNBandEquivalenceRequest",
]
