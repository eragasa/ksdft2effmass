"""Periodic-3D rank-two aggregate ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic3d.band_equivalence_hopping_locality.base import (
    Periodic3DBandEquivalenceHoppingLocality,
    Periodic3DBandEquivalenceHoppingLocalityAction,
    Periodic3DBandEquivalenceHoppingLocalityAnalysis,
    Periodic3DBandEquivalenceHoppingLocalityAnalyzer,
    Periodic3DBandEquivalenceHoppingLocalityRequest,
    Periodic3DBandEquivalenceHoppingLocalityValue,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence.base import (
    Periodic3DRank2BandEquivalence,
    Periodic3DRank2BandEquivalenceAnalysis,
    Periodic3DRank2BandEquivalenceAnalyzer,
    Periodic3DRank2BandEquivalenceRequest,
)


class _Periodic3DRank2BandSubspace:
    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the fixed represented band-subspace rank."""
        return 2


class Periodic3DRank2BandEquivalenceHoppingLocalityCapability(
    Periodic3DRank2BandEquivalence,
    Periodic3DBandEquivalenceHoppingLocality,
    ABC,
):
    """Coordinate one periodic-3D rank-two aggregate study."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the represented band-subspace rank."""


class Periodic3DRank2BandEquivalenceHoppingLocalityRequestRole(
    Periodic3DRank2BandEquivalenceRequest,
    Periodic3DBandEquivalenceHoppingLocalityRequest,
    Periodic3DRank2BandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Bind one periodic-3D rank-two aggregate request."""

    __slots__ = ()


class Periodic3DRank2BandEquivalenceHoppingLocalityAnalysisRole[
    RequestT: Periodic3DRank2BandEquivalenceHoppingLocalityRequestRole,
](
    Periodic3DRank2BandEquivalenceAnalysis[RequestT],
    Periodic3DBandEquivalenceHoppingLocalityAnalysis[RequestT],
    Periodic3DRank2BandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Retain one periodic-3D rank-two aggregate analysis."""

    __slots__ = ()


class Periodic3DRank2BandEquivalenceHoppingLocalityAnalyzerRole[
    RequestT: Periodic3DRank2BandEquivalenceHoppingLocalityRequestRole,
](
    Periodic3DRank2BandEquivalenceAnalyzer[RequestT],
    Periodic3DBandEquivalenceHoppingLocalityAnalyzer[RequestT],
    Periodic3DRank2BandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Execute one periodic-3D rank-two aggregate request."""

    __slots__ = ()

    @abstractmethod
    def execute(
        self,
    ) -> Periodic3DRank2BandEquivalenceHoppingLocalityAnalysisRole[RequestT]:
        """Execute the bound rank-two aggregate."""


class Periodic3DRank2BandEquivalenceHoppingLocalityValue(
    _Periodic3DRank2BandSubspace,
    Periodic3DBandEquivalenceHoppingLocalityValue,
    Periodic3DRank2BandEquivalenceHoppingLocalityCapability,
    ABC,
):  # noqa: B024
    """Retain one standalone rank-two aggregate value."""

    __slots__ = ()


class Periodic3DRank2BandEquivalenceHoppingLocalityAction(
    _Periodic3DRank2BandSubspace,
    Periodic3DBandEquivalenceHoppingLocalityAction,
    Periodic3DRank2BandEquivalenceHoppingLocalityCapability,
    ABC,
):  # noqa: B024
    """Perform one supporting rank-two aggregate action."""

    __slots__ = ()


__all__ = [
    "Periodic3DRank2BandEquivalenceHoppingLocalityAction",
    "Periodic3DRank2BandEquivalenceHoppingLocalityAnalysisRole",
    "Periodic3DRank2BandEquivalenceHoppingLocalityAnalyzerRole",
    "Periodic3DRank2BandEquivalenceHoppingLocalityCapability",
    "Periodic3DRank2BandEquivalenceHoppingLocalityRequestRole",
    "Periodic3DRank2BandEquivalenceHoppingLocalityValue",
]
