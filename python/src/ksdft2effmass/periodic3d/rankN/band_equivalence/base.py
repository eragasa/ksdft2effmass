"""Periodic-3D rank-N band-equivalence ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.periodic3d.band_equivalence.base import (
    Periodic3DBandEquivalence,
    Periodic3DBandEquivalenceAnalysis,
    Periodic3DBandEquivalenceAnalyzer,
    Periodic3DBandEquivalenceRequest,
)


class Periodic3DRankNBandEquivalence(Periodic3DBandEquivalence, ABC):
    """Identify arbitrary-rank band equivalence on a periodic 3D lattice."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_ranks(self) -> tuple[int, ...]:
        """Return the represented band-subspace rank inventory."""


class Periodic3DRankNBandEquivalenceRequest(
    Periodic3DBandEquivalenceRequest,
    Periodic3DRankNBandEquivalence,
    ABC,
):
    """Require rank-N ownership for periodic-3D requests."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_ranks(self) -> tuple[int, ...]:
        """Return the requested band-subspace rank inventory."""


class Periodic3DRankNBandEquivalenceAnalysis[
    RequestT: Periodic3DRankNBandEquivalenceRequest,
](
    Periodic3DBandEquivalenceAnalysis[RequestT],
    Periodic3DRankNBandEquivalence,
    ABC,
):
    """Require rank-N ownership for periodic-3D analyses."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_ranks(self) -> tuple[int, ...]:
        """Return the analyzed band-subspace rank inventory."""


class Periodic3DRankNBandEquivalenceAnalyzer[
    RequestT: Periodic3DRankNBandEquivalenceRequest,
](
    Periodic3DBandEquivalenceAnalyzer[RequestT],
    Periodic3DRankNBandEquivalence,
    ABC,
):
    """Require one concrete periodic-3D arbitrary-rank analysis action."""

    __slots__ = ()

    @property
    def band_subspace_ranks(self) -> tuple[int, ...]:
        """Return the bound request's band-subspace rank inventory."""
        return self.request.band_subspace_ranks

    @abstractmethod
    def execute(self) -> Periodic3DRankNBandEquivalenceAnalysis[RequestT]:
        """Execute the bound arbitrary-rank analysis."""


__all__ = [
    "Periodic3DRankNBandEquivalence",
    "Periodic3DRankNBandEquivalenceAnalysis",
    "Periodic3DRankNBandEquivalenceAnalyzer",
    "Periodic3DRankNBandEquivalenceRequest",
]
