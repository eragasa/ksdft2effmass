"""Periodic-2D rank-two aggregate ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic2d.band_equivalence_hopping_locality.base import (
    Periodic2DBandEquivalenceHoppingLocality,
    Periodic2DBandEquivalenceHoppingLocalityAction,
    Periodic2DBandEquivalenceHoppingLocalityAnalysis,
    Periodic2DBandEquivalenceHoppingLocalityAnalyzer,
    Periodic2DBandEquivalenceHoppingLocalityRequest,
    Periodic2DBandEquivalenceHoppingLocalityValue,
)


class _Periodic2DRank2BandSubspace:
    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the fixed represented band-subspace rank."""
        return 2


class Periodic2DRank2BandEquivalenceHoppingLocalityCapability(
    Periodic2DBandEquivalenceHoppingLocality,
    ABC,
):
    """Coordinate one periodic-2D rank-two aggregate study."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the represented band-subspace rank."""


class Periodic2DRank2BandEquivalenceHoppingLocalityRequestRole(
    _Periodic2DRank2BandSubspace,
    Periodic2DBandEquivalenceHoppingLocalityRequest,
    Periodic2DRank2BandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Bind one periodic-2D rank-two aggregate request."""

    __slots__ = ()


class Periodic2DRank2BandEquivalenceHoppingLocalityAnalysisRole[
    RequestT: Periodic2DRank2BandEquivalenceHoppingLocalityRequestRole,
](
    _Periodic2DRank2BandSubspace,
    Periodic2DBandEquivalenceHoppingLocalityAnalysis[RequestT],
    Periodic2DRank2BandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Retain one periodic-2D rank-two aggregate analysis."""

    __slots__ = ()


class Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzerRole[
    RequestT: Periodic2DRank2BandEquivalenceHoppingLocalityRequestRole,
](
    _Periodic2DRank2BandSubspace,
    Periodic2DBandEquivalenceHoppingLocalityAnalyzer[RequestT],
    Periodic2DRank2BandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Execute one periodic-2D rank-two aggregate request."""

    __slots__ = ()

    @abstractmethod
    def execute(
        self,
    ) -> Periodic2DRank2BandEquivalenceHoppingLocalityAnalysisRole[RequestT]:
        """Execute the bound rank-two aggregate."""


class Periodic2DRank2BandEquivalenceHoppingLocalityValue(
    _Periodic2DRank2BandSubspace,
    Periodic2DBandEquivalenceHoppingLocalityValue,
    Periodic2DRank2BandEquivalenceHoppingLocalityCapability,
    ABC,
):  # noqa: B024
    """Retain one standalone rank-two aggregate value."""

    __slots__ = ()


class Periodic2DRank2BandEquivalenceHoppingLocalityAction(
    _Periodic2DRank2BandSubspace,
    Periodic2DBandEquivalenceHoppingLocalityAction,
    Periodic2DRank2BandEquivalenceHoppingLocalityCapability,
    ABC,
):  # noqa: B024
    """Perform one supporting rank-two aggregate action."""

    __slots__ = ()


__all__ = [
    "Periodic2DRank2BandEquivalenceHoppingLocalityAction",
    "Periodic2DRank2BandEquivalenceHoppingLocalityAnalysisRole",
    "Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzerRole",
    "Periodic2DRank2BandEquivalenceHoppingLocalityCapability",
    "Periodic2DRank2BandEquivalenceHoppingLocalityRequestRole",
    "Periodic2DRank2BandEquivalenceHoppingLocalityValue",
]
