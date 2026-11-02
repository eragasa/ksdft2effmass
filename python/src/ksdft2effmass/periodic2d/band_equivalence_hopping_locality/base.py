"""Periodic-2D ownership roles for the band-equivalence/locality aggregate."""

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
from ksdft2effmass.periodic2d.band_equivalence.base import (
    Periodic2DBandEquivalence,
    Periodic2DBandEquivalenceAnalysis,
    Periodic2DBandEquivalenceAnalyzer,
    Periodic2DBandEquivalenceRequest,
)


class Periodic2DBandEquivalenceHoppingLocality(
    Periodic2DBandEquivalence,
    PeriodicBandEquivalenceHoppingLocality,
    ABC,
):  # noqa: B024
    """Coordinate the aggregate on a periodic two-dimensional lattice."""

    __slots__ = ()


class Periodic2DBandEquivalenceHoppingLocalityRequest(
    Periodic2DBandEquivalenceRequest,
    PeriodicBandEquivalenceHoppingLocalityRequest,
    Periodic2DBandEquivalenceHoppingLocality,
    ABC,
):
    """Bind one periodic-2D aggregate request."""

    __slots__ = ()


class Periodic2DBandEquivalenceHoppingLocalityAnalysis[
    RequestT: Periodic2DBandEquivalenceHoppingLocalityRequest,
](
    Periodic2DBandEquivalenceAnalysis[RequestT],
    PeriodicBandEquivalenceHoppingLocalityAnalysis[RequestT],
    Periodic2DBandEquivalenceHoppingLocality,
    ABC,
):
    """Retain one periodic-2D aggregate analysis."""

    __slots__ = ()


class Periodic2DBandEquivalenceHoppingLocalityAnalyzer[
    RequestT: Periodic2DBandEquivalenceHoppingLocalityRequest,
](
    Periodic2DBandEquivalenceAnalyzer[RequestT],
    PeriodicBandEquivalenceHoppingLocalityAnalyzer[RequestT],
    Periodic2DBandEquivalenceHoppingLocality,
    ABC,
):
    """Execute one periodic-2D aggregate request."""

    __slots__ = ()

    @abstractmethod
    def execute(self) -> Periodic2DBandEquivalenceHoppingLocalityAnalysis[RequestT]:
        """Execute the bound periodic-2D aggregate."""


class Periodic2DBandEquivalenceHoppingLocalityValue(
    PeriodicBandEquivalenceHoppingLocalityValue,
    Periodic2DBandEquivalenceHoppingLocality,
    ABC,
):  # noqa: B024
    """Retain one standalone periodic-2D aggregate value."""

    __slots__ = ()


class Periodic2DBandEquivalenceHoppingLocalityAction(
    PeriodicBandEquivalenceHoppingLocalityAction,
    Periodic2DBandEquivalenceHoppingLocality,
    ABC,
):  # noqa: B024
    """Perform one supporting periodic-2D aggregate action."""

    __slots__ = ()


__all__ = [
    "Periodic2DBandEquivalenceHoppingLocality",
    "Periodic2DBandEquivalenceHoppingLocalityAction",
    "Periodic2DBandEquivalenceHoppingLocalityAnalysis",
    "Periodic2DBandEquivalenceHoppingLocalityAnalyzer",
    "Periodic2DBandEquivalenceHoppingLocalityRequest",
    "Periodic2DBandEquivalenceHoppingLocalityValue",
]
