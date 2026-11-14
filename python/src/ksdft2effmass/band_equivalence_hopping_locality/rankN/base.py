"""Dimension-neutral periodic rank-N aggregate ownership roles."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.band_equivalence_hopping_locality.base import (
    PeriodicBandEquivalenceHoppingLocality,
    PeriodicBandEquivalenceHoppingLocalityAction,
    PeriodicBandEquivalenceHoppingLocalityAnalysis,
    PeriodicBandEquivalenceHoppingLocalityAnalyzer,
    PeriodicBandEquivalenceHoppingLocalityRequest,
    PeriodicBandEquivalenceHoppingLocalityValue,
)


class PeriodicRankNBandEquivalenceHoppingLocalityCapability(
    PeriodicBandEquivalenceHoppingLocality,
    ABC,
):
    """Coordinate one dimension-qualified periodic rank-N aggregate family."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_ranks(self) -> tuple[int, ...]:
        """Return the represented band-subspace rank inventory."""


class PeriodicRankNBandEquivalenceHoppingLocalityCaseCapability(
    PeriodicBandEquivalenceHoppingLocality,
    ABC,
):
    """Identify one dimension-qualified finite-rank aggregate case."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the represented band-subspace rank for this case."""


class PeriodicRankNBandEquivalenceHoppingLocalityCaseRequest(
    PeriodicRankNBandEquivalenceHoppingLocalityCaseCapability,
    ABC,
):  # noqa: B024
    """Bind one supporting request for a dimension-qualified rank-N case."""

    __slots__ = ()


class PeriodicRankNBandEquivalenceHoppingLocalityCaseValue(
    PeriodicBandEquivalenceHoppingLocalityValue,
    PeriodicRankNBandEquivalenceHoppingLocalityCaseCapability,
    ABC,
):
    """Retain one standalone dimension-qualified rank-N case value."""

    __slots__ = ()


class PeriodicRankNBandEquivalenceHoppingLocalityCaseAction(
    PeriodicBandEquivalenceHoppingLocalityAction,
    PeriodicRankNBandEquivalenceHoppingLocalityCaseCapability,
    ABC,
):
    """Perform one supporting dimension-qualified rank-N case action."""

    __slots__ = ()


class PeriodicRankNBandEquivalenceHoppingLocalityRequestRole(
    PeriodicBandEquivalenceHoppingLocalityRequest,
    PeriodicRankNBandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Bind one dimension-qualified periodic rank-N aggregate request."""

    __slots__ = ()


class PeriodicRankNBandEquivalenceHoppingLocalityAnalysisRole[
    RequestT: PeriodicRankNBandEquivalenceHoppingLocalityRequestRole,
](
    PeriodicBandEquivalenceHoppingLocalityAnalysis[RequestT],
    PeriodicRankNBandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Retain one dimension-qualified periodic rank-N aggregate analysis."""

    __slots__ = ()


class PeriodicRankNBandEquivalenceHoppingLocalityAnalyzerRole[
    RequestT: PeriodicRankNBandEquivalenceHoppingLocalityRequestRole,
](
    PeriodicBandEquivalenceHoppingLocalityAnalyzer[RequestT],
    PeriodicRankNBandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Execute one dimension-qualified periodic rank-N aggregate request."""

    __slots__ = ()

    @abstractmethod
    def execute(
        self,
    ) -> PeriodicRankNBandEquivalenceHoppingLocalityAnalysisRole[RequestT]:
        """Execute the bound rank-N aggregate."""


class PeriodicRankNBandEquivalenceHoppingLocalityValue(
    PeriodicBandEquivalenceHoppingLocalityValue,
    PeriodicRankNBandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Retain one standalone dimension-qualified rank-N aggregate value."""

    __slots__ = ()


class PeriodicRankNBandEquivalenceHoppingLocalityAction(
    PeriodicBandEquivalenceHoppingLocalityAction,
    PeriodicRankNBandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Perform one supporting dimension-qualified rank-N aggregate action."""

    __slots__ = ()


__all__ = [
    "PeriodicRankNBandEquivalenceHoppingLocalityAction",
    "PeriodicRankNBandEquivalenceHoppingLocalityAnalysisRole",
    "PeriodicRankNBandEquivalenceHoppingLocalityAnalyzerRole",
    "PeriodicRankNBandEquivalenceHoppingLocalityCapability",
    "PeriodicRankNBandEquivalenceHoppingLocalityCaseAction",
    "PeriodicRankNBandEquivalenceHoppingLocalityCaseCapability",
    "PeriodicRankNBandEquivalenceHoppingLocalityCaseRequest",
    "PeriodicRankNBandEquivalenceHoppingLocalityCaseValue",
    "PeriodicRankNBandEquivalenceHoppingLocalityRequestRole",
    "PeriodicRankNBandEquivalenceHoppingLocalityValue",
]
