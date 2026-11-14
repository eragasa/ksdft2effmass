"""Periodic-2D rank-N band-equivalence ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.analysis.model_adequacy.band_equivalence.base import (
    PeriodicRankNBandEquivalenceCapability,
)
from ksdft2effmass.periodic2d.band_equivalence.base import (
    Periodic2DBandEquivalence,
    Periodic2DBandEquivalenceAnalysis,
    Periodic2DBandEquivalenceAnalyzer,
    Periodic2DBandEquivalenceRequest,
)


class Periodic2DRankNBandEquivalence(
    Periodic2DBandEquivalence,
    PeriodicRankNBandEquivalenceCapability,
    ABC,
):
    """Identify arbitrary-rank band equivalence on a periodic 2D lattice."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_ranks(self) -> tuple[int, ...]:
        """Return the represented band-subspace rank inventory."""


class Periodic2DRankNBandEquivalenceRequest(
    Periodic2DBandEquivalenceRequest,
    Periodic2DRankNBandEquivalence,
    ABC,
):
    """Require rank-N ownership for periodic-2D requests."""

    __slots__ = ()


class Periodic2DRankNBandEquivalenceAnalysis[
    RequestT: Periodic2DRankNBandEquivalenceRequest,
](
    Periodic2DBandEquivalenceAnalysis[RequestT],
    Periodic2DRankNBandEquivalence,
    ABC,
):
    """Require rank-N ownership for periodic-2D analyses."""

    __slots__ = ()


class Periodic2DRankNBandEquivalenceAnalyzer[
    RequestT: Periodic2DRankNBandEquivalenceRequest,
](
    Periodic2DBandEquivalenceAnalyzer[RequestT],
    Periodic2DRankNBandEquivalence,
    ABC,
):
    """Require one concrete periodic-2D arbitrary-rank analysis action."""

    __slots__ = ()

    @property
    def band_subspace_ranks(self) -> tuple[int, ...]:
        """Return the bound request's band-subspace rank inventory."""
        return self.request.band_subspace_ranks

    @abstractmethod
    def execute(self) -> Periodic2DRankNBandEquivalenceAnalysis[RequestT]:
        """Execute the bound arbitrary-rank analysis."""


__all__ = [
    "Periodic2DRankNBandEquivalence",
    "Periodic2DRankNBandEquivalenceAnalysis",
    "Periodic2DRankNBandEquivalenceAnalyzer",
    "Periodic2DRankNBandEquivalenceRequest",
]
