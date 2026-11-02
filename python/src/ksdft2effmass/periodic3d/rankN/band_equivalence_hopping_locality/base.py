"""Periodic-3D rank-N aggregate ownership guardrails."""

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
from ksdft2effmass.periodic3d.band_equivalence_hopping_locality.base import (
    Periodic3DBandEquivalenceHoppingLocality,
    Periodic3DBandEquivalenceHoppingLocalityAction,
    Periodic3DBandEquivalenceHoppingLocalityAnalysis,
    Periodic3DBandEquivalenceHoppingLocalityAnalyzer,
    Periodic3DBandEquivalenceHoppingLocalityRequest,
    Periodic3DBandEquivalenceHoppingLocalityValue,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence.base import (
    Periodic3DRankNBandEquivalence,
    Periodic3DRankNBandEquivalenceAnalysis,
    Periodic3DRankNBandEquivalenceAnalyzer,
    Periodic3DRankNBandEquivalenceRequest,
)


class Periodic3DRankNBandEquivalenceHoppingLocalityCapability(
    Periodic3DRankNBandEquivalence,
    Periodic3DBandEquivalenceHoppingLocality,
    PeriodicRankNBandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Coordinate one periodic-3D arbitrary-rank aggregate study family."""

    __slots__ = ()


class Periodic3DRankNBandEquivalenceHoppingLocalityCaseCapability(
    Periodic3DBandEquivalenceHoppingLocality,
    PeriodicRankNBandEquivalenceHoppingLocalityCaseCapability,
    ABC,
):
    """Identify one concrete finite-rank case in the rank-N family."""

    __slots__ = ()


class Periodic3DRankNBandEquivalenceHoppingLocalityCaseRequest(
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseCapability,
    PeriodicRankNBandEquivalenceHoppingLocalityCaseRequest,
    ABC,
):  # noqa: B024
    """Bind one rank-N aggregate case supporting request."""

    __slots__ = ()


class Periodic3DRankNBandEquivalenceHoppingLocalityCaseValue(
    Periodic3DBandEquivalenceHoppingLocalityValue,
    PeriodicRankNBandEquivalenceHoppingLocalityCaseValue,
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseCapability,
    ABC,
):
    """Retain one standalone rank-N aggregate case value."""

    __slots__ = ()


class Periodic3DRankNBandEquivalenceHoppingLocalityCaseAction(
    Periodic3DBandEquivalenceHoppingLocalityAction,
    PeriodicRankNBandEquivalenceHoppingLocalityCaseAction,
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseCapability,
    ABC,
):
    """Perform one supporting rank-N aggregate case action."""

    __slots__ = ()


class Periodic3DRankNBandEquivalenceHoppingLocalityRequestRole(
    Periodic3DRankNBandEquivalenceRequest,
    Periodic3DBandEquivalenceHoppingLocalityRequest,
    PeriodicRankNBandEquivalenceHoppingLocalityRequestRole,
    Periodic3DRankNBandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Bind one periodic-3D rank-N aggregate request."""

    __slots__ = ()


class Periodic3DRankNBandEquivalenceHoppingLocalityAnalysisRole[
    RequestT: Periodic3DRankNBandEquivalenceHoppingLocalityRequestRole,
](
    Periodic3DRankNBandEquivalenceAnalysis[RequestT],
    Periodic3DBandEquivalenceHoppingLocalityAnalysis[RequestT],
    PeriodicRankNBandEquivalenceHoppingLocalityAnalysisRole[RequestT],
    Periodic3DRankNBandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Retain one periodic-3D rank-N aggregate analysis."""

    __slots__ = ()


class Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzerRole[
    RequestT: Periodic3DRankNBandEquivalenceHoppingLocalityRequestRole,
](
    Periodic3DRankNBandEquivalenceAnalyzer[RequestT],
    Periodic3DBandEquivalenceHoppingLocalityAnalyzer[RequestT],
    PeriodicRankNBandEquivalenceHoppingLocalityAnalyzerRole[RequestT],
    Periodic3DRankNBandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Execute one periodic-3D rank-N aggregate request."""

    __slots__ = ()

    @property
    @final
    def band_subspace_ranks(self) -> tuple[int, ...]:
        """Return the bound request's band-subspace rank inventory."""
        return self.request.band_subspace_ranks

    @abstractmethod
    def execute(
        self,
    ) -> Periodic3DRankNBandEquivalenceHoppingLocalityAnalysisRole[RequestT]:
        """Execute the bound rank-N aggregate."""


class Periodic3DRankNBandEquivalenceHoppingLocalityValue(
    Periodic3DBandEquivalenceHoppingLocalityValue,
    PeriodicRankNBandEquivalenceHoppingLocalityValue,
    Periodic3DRankNBandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Retain one standalone rank-N aggregate-family value."""

    __slots__ = ()


class Periodic3DRankNBandEquivalenceHoppingLocalityAction(
    Periodic3DBandEquivalenceHoppingLocalityAction,
    PeriodicRankNBandEquivalenceHoppingLocalityAction,
    Periodic3DRankNBandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Perform one supporting rank-N aggregate-family action."""

    __slots__ = ()


__all__ = [
    "Periodic3DRankNBandEquivalenceHoppingLocalityAction",
    "Periodic3DRankNBandEquivalenceHoppingLocalityCaseAction",
    "Periodic3DRankNBandEquivalenceHoppingLocalityCaseCapability",
    "Periodic3DRankNBandEquivalenceHoppingLocalityCaseRequest",
    "Periodic3DRankNBandEquivalenceHoppingLocalityCaseValue",
    "Periodic3DRankNBandEquivalenceHoppingLocalityAnalysisRole",
    "Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzerRole",
    "Periodic3DRankNBandEquivalenceHoppingLocalityCapability",
    "Periodic3DRankNBandEquivalenceHoppingLocalityRequestRole",
    "Periodic3DRankNBandEquivalenceHoppingLocalityValue",
]
