"""Periodic-2D rank-one band-equivalence ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic2d.band_equivalence.base import (
    Periodic2DBandEquivalence,
    Periodic2DBandEquivalenceAnalysis,
    Periodic2DBandEquivalenceAnalyzer,
    Periodic2DBandEquivalenceRequest,
)


class _Periodic2DRank1BandSubspace:
    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the represented band subspace at each momentum."""
        return 1


class Periodic2DRank1BandEquivalence(Periodic2DBandEquivalence, ABC):
    """Identify scalar band equivalence on a periodic 2D lattice."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the represented band subspace at each momentum."""


class Periodic2DRank1BandEquivalenceRequest(
    Periodic2DBandEquivalenceRequest,
    Periodic2DRank1BandEquivalence,
    ABC,
):
    """Own the currently study-independent periodic-2D rank-one request role."""

    __slots__ = ()


class Periodic2DRank1BandEquivalenceAnalysis[
    RequestT: Periodic2DRank1BandEquivalenceRequest,
](
    Periodic2DBandEquivalenceAnalysis[RequestT],
    Periodic2DRank1BandEquivalence,
    ABC,
):
    """Own the currently study-independent periodic-2D rank-one analysis role."""

    __slots__ = ()


class Periodic2DRank1BandEquivalenceAnalyzer[
    RequestT: Periodic2DRank1BandEquivalenceRequest,
](
    _Periodic2DRank1BandSubspace,
    Periodic2DBandEquivalenceAnalyzer[RequestT],
    Periodic2DRank1BandEquivalence,
    ABC,
):
    """Reserve the rank-one action role without installing a scientific study."""

    __slots__ = ()

    @abstractmethod
    def execute(self) -> Periodic2DRank1BandEquivalenceAnalysis[RequestT]:
        """Execute a separately installed rank-one study."""


__all__ = [
    "Periodic2DRank1BandEquivalence",
    "Periodic2DRank1BandEquivalenceAnalysis",
    "Periodic2DRank1BandEquivalenceAnalyzer",
    "Periodic2DRank1BandEquivalenceRequest",
]
