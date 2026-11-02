"""Periodic-3D rank-one band-equivalence ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic3d.band_equivalence.base import (
    Periodic3DBandEquivalence,
    Periodic3DBandEquivalenceAnalysis,
    Periodic3DBandEquivalenceAnalyzer,
    Periodic3DBandEquivalenceRequest,
)


class _Periodic3DRank1BandSubspace:
    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the represented band subspace at each momentum."""
        return 1


class Periodic3DRank1BandEquivalence(Periodic3DBandEquivalence, ABC):
    """Identify scalar band equivalence on a periodic 3D lattice."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the represented band subspace at each momentum."""


class Periodic3DRank1BandEquivalenceRequest(
    Periodic3DBandEquivalenceRequest,
    Periodic3DRank1BandEquivalence,
    ABC,
):
    """Own the currently study-independent periodic-3D rank-one request role."""

    __slots__ = ()


class Periodic3DRank1BandEquivalenceAnalysis[
    RequestT: Periodic3DRank1BandEquivalenceRequest,
](
    Periodic3DBandEquivalenceAnalysis[RequestT],
    Periodic3DRank1BandEquivalence,
    ABC,
):
    """Own the currently study-independent periodic-3D rank-one analysis role."""

    __slots__ = ()


class Periodic3DRank1BandEquivalenceAnalyzer[
    RequestT: Periodic3DRank1BandEquivalenceRequest,
](
    _Periodic3DRank1BandSubspace,
    Periodic3DBandEquivalenceAnalyzer[RequestT],
    Periodic3DRank1BandEquivalence,
    ABC,
):
    """Reserve the rank-one action role without installing a scientific study."""

    __slots__ = ()

    @abstractmethod
    def execute(self) -> Periodic3DRank1BandEquivalenceAnalysis[RequestT]:
        """Execute a separately installed rank-one study."""


__all__ = [
    "Periodic3DRank1BandEquivalence",
    "Periodic3DRank1BandEquivalenceAnalysis",
    "Periodic3DRank1BandEquivalenceAnalyzer",
    "Periodic3DRank1BandEquivalenceRequest",
]
