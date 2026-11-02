"""Periodic-2D rank-two band-equivalence ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic2d.band_equivalence.base import (
    Periodic2DBandEquivalence,
    Periodic2DBandEquivalenceAnalysis,
    Periodic2DBandEquivalenceAnalyzer,
    Periodic2DBandEquivalenceRequest,
)


class _Periodic2DRank2BandSubspace:
    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the represented band subspace at each momentum."""
        return 2


class Periodic2DRank2BandEquivalence(Periodic2DBandEquivalence, ABC):
    """Identify rank-two band equivalence on a periodic 2D lattice."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the represented band subspace at each momentum."""


class Periodic2DRank2BandEquivalenceRequest(
    _Periodic2DRank2BandSubspace,
    Periodic2DBandEquivalenceRequest,
    Periodic2DRank2BandEquivalence,
    ABC,
):
    """Require rank-two ownership for periodic-2D requests."""

    __slots__ = ()


class Periodic2DRank2BandEquivalenceAnalysis[
    RequestT: Periodic2DRank2BandEquivalenceRequest,
](
    _Periodic2DRank2BandSubspace,
    Periodic2DBandEquivalenceAnalysis[RequestT],
    Periodic2DRank2BandEquivalence,
    ABC,
):
    """Require rank-two ownership for periodic-2D analyses."""

    __slots__ = ()


class Periodic2DRank2BandEquivalenceAnalyzer[
    RequestT: Periodic2DRank2BandEquivalenceRequest,
](
    _Periodic2DRank2BandSubspace,
    Periodic2DBandEquivalenceAnalyzer[RequestT],
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
