"""Periodic-2D rank-N aggregate ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.band_equivalence_hopping_locality.rankN.base import (
    PeriodicRankNBandEquivalenceHoppingLocalityAction,
    PeriodicRankNBandEquivalenceHoppingLocalityAnalysisRole,
    PeriodicRankNBandEquivalenceHoppingLocalityAnalyzerRole,
    PeriodicRankNBandEquivalenceHoppingLocalityCapability,
    PeriodicRankNBandEquivalenceHoppingLocalityCaseAction,
    PeriodicRankNBandEquivalenceHoppingLocalityCaseCapability,
    PeriodicRankNBandEquivalenceHoppingLocalityCaseRequest,
    PeriodicRankNBandEquivalenceHoppingLocalityCaseValue,
    PeriodicRankNBandEquivalenceHoppingLocalityRequestRole,
    PeriodicRankNBandEquivalenceHoppingLocalityValue,
)
from ksdft2effmass.periodic2d.band_equivalence_hopping_locality.base import (
    Periodic2DBandEquivalenceHoppingLocality,
    Periodic2DBandEquivalenceHoppingLocalityAction,
    Periodic2DBandEquivalenceHoppingLocalityAnalysis,
    Periodic2DBandEquivalenceHoppingLocalityAnalyzer,
    Periodic2DBandEquivalenceHoppingLocalityRequest,
    Periodic2DBandEquivalenceHoppingLocalityValue,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence.base import (
    Periodic2DRankNBandEquivalence,
    Periodic2DRankNBandEquivalenceAnalysis,
    Periodic2DRankNBandEquivalenceAnalyzer,
    Periodic2DRankNBandEquivalenceRequest,
)


class Periodic2DRankNBandEquivalenceHoppingLocalityCapability(
    Periodic2DRankNBandEquivalence,
    Periodic2DBandEquivalenceHoppingLocality,
    PeriodicRankNBandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Coordinate one periodic-2D arbitrary-rank aggregate study family."""

    __slots__ = ()


class Periodic2DRankNBandEquivalenceHoppingLocalityCaseCapability(
    Periodic2DBandEquivalenceHoppingLocality,
    PeriodicRankNBandEquivalenceHoppingLocalityCaseCapability,
    ABC,
):
    """Identify one concrete finite-rank case in the rank-N family."""

    __slots__ = ()


class Periodic2DRankNBandEquivalenceHoppingLocalityCaseRequest(
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseCapability,
    PeriodicRankNBandEquivalenceHoppingLocalityCaseRequest,
    ABC,
):  # noqa: B024
    """Bind one rank-N aggregate case supporting request."""

    __slots__ = ()


class Periodic2DRankNBandEquivalenceHoppingLocalityCaseValue(
    Periodic2DBandEquivalenceHoppingLocalityValue,
    PeriodicRankNBandEquivalenceHoppingLocalityCaseValue,
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseCapability,
    ABC,
):
    """Retain one standalone rank-N aggregate case value."""

    __slots__ = ()


class Periodic2DRankNBandEquivalenceHoppingLocalityCaseAction(
    Periodic2DBandEquivalenceHoppingLocalityAction,
    PeriodicRankNBandEquivalenceHoppingLocalityCaseAction,
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseCapability,
    ABC,
):
    """Perform one supporting rank-N aggregate case action."""

    __slots__ = ()


class Periodic2DRankNBandEquivalenceHoppingLocalityRequestRole(
    Periodic2DRankNBandEquivalenceRequest,
    Periodic2DBandEquivalenceHoppingLocalityRequest,
    PeriodicRankNBandEquivalenceHoppingLocalityRequestRole,
    Periodic2DRankNBandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Bind one periodic-2D rank-N aggregate request."""

    __slots__ = ()


class Periodic2DRankNBandEquivalenceHoppingLocalityAnalysisRole[
    RequestT: Periodic2DRankNBandEquivalenceHoppingLocalityRequestRole,
](
    Periodic2DRankNBandEquivalenceAnalysis[RequestT],
    Periodic2DBandEquivalenceHoppingLocalityAnalysis[RequestT],
    PeriodicRankNBandEquivalenceHoppingLocalityAnalysisRole[RequestT],
    Periodic2DRankNBandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Retain one periodic-2D rank-N aggregate analysis."""

    __slots__ = ()


class Periodic2DRankNBandEquivalenceHoppingLocalityAnalyzerRole[
    RequestT: Periodic2DRankNBandEquivalenceHoppingLocalityRequestRole,
](
    Periodic2DRankNBandEquivalenceAnalyzer[RequestT],
    Periodic2DBandEquivalenceHoppingLocalityAnalyzer[RequestT],
    PeriodicRankNBandEquivalenceHoppingLocalityAnalyzerRole[RequestT],
    Periodic2DRankNBandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Execute one periodic-2D rank-N aggregate request."""

    __slots__ = ()

    @property
    @final
    def band_subspace_ranks(self) -> tuple[int, ...]:
        """Return the bound request's band-subspace rank inventory."""
        return self.request.band_subspace_ranks

    @abstractmethod
    def execute(
        self,
    ) -> Periodic2DRankNBandEquivalenceHoppingLocalityAnalysisRole[RequestT]:
        """Execute the bound rank-N aggregate."""


class Periodic2DRankNBandEquivalenceHoppingLocalityValue(
    Periodic2DBandEquivalenceHoppingLocalityValue,
    PeriodicRankNBandEquivalenceHoppingLocalityValue,
    Periodic2DRankNBandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Retain one standalone rank-N aggregate-family value."""

    __slots__ = ()


class Periodic2DRankNBandEquivalenceHoppingLocalityAction(
    Periodic2DBandEquivalenceHoppingLocalityAction,
    PeriodicRankNBandEquivalenceHoppingLocalityAction,
    Periodic2DRankNBandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Perform one supporting rank-N aggregate-family action."""

    __slots__ = ()


__all__ = [
    "Periodic2DRankNBandEquivalenceHoppingLocalityAction",
    "Periodic2DRankNBandEquivalenceHoppingLocalityCaseAction",
    "Periodic2DRankNBandEquivalenceHoppingLocalityCaseCapability",
    "Periodic2DRankNBandEquivalenceHoppingLocalityCaseRequest",
    "Periodic2DRankNBandEquivalenceHoppingLocalityCaseValue",
    "Periodic2DRankNBandEquivalenceHoppingLocalityAnalysisRole",
    "Periodic2DRankNBandEquivalenceHoppingLocalityAnalyzerRole",
    "Periodic2DRankNBandEquivalenceHoppingLocalityCapability",
    "Periodic2DRankNBandEquivalenceHoppingLocalityRequestRole",
    "Periodic2DRankNBandEquivalenceHoppingLocalityValue",
]
