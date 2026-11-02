"""Periodic-1D ownership roles for the band-equivalence/locality aggregate."""

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
from ksdft2effmass.periodic1d.band_equivalence.base import (
    Periodic1DBandEquivalence,
    Periodic1DBandEquivalenceAnalysis,
    Periodic1DBandEquivalenceAnalyzer,
    Periodic1DBandEquivalenceRequest,
)


class Periodic1DBandEquivalenceHoppingLocality(
    Periodic1DBandEquivalence,
    PeriodicBandEquivalenceHoppingLocality,
    ABC,
):  # noqa: B024
    """Coordinate the aggregate on a periodic one-dimensional lattice."""

    __slots__ = ()


class Periodic1DBandEquivalenceHoppingLocalityRequest(
    Periodic1DBandEquivalenceRequest,
    PeriodicBandEquivalenceHoppingLocalityRequest,
    Periodic1DBandEquivalenceHoppingLocality,
    ABC,
):
    """Bind one periodic-1D aggregate request."""

    __slots__ = ()


class Periodic1DBandEquivalenceHoppingLocalityAnalysis[
    RequestT: Periodic1DBandEquivalenceHoppingLocalityRequest,
](
    Periodic1DBandEquivalenceAnalysis[RequestT],
    PeriodicBandEquivalenceHoppingLocalityAnalysis[RequestT],
    Periodic1DBandEquivalenceHoppingLocality,
    ABC,
):
    """Retain one periodic-1D aggregate analysis."""

    __slots__ = ()


class Periodic1DBandEquivalenceHoppingLocalityAnalyzer[
    RequestT: Periodic1DBandEquivalenceHoppingLocalityRequest,
](
    Periodic1DBandEquivalenceAnalyzer[RequestT],
    PeriodicBandEquivalenceHoppingLocalityAnalyzer[RequestT],
    Periodic1DBandEquivalenceHoppingLocality,
    ABC,
):
    """Execute one periodic-1D aggregate request."""

    __slots__ = ()

    @abstractmethod
    def execute(self) -> Periodic1DBandEquivalenceHoppingLocalityAnalysis[RequestT]:
        """Execute the bound periodic-1D aggregate."""


class Periodic1DBandEquivalenceHoppingLocalityValue(
    PeriodicBandEquivalenceHoppingLocalityValue,
    Periodic1DBandEquivalenceHoppingLocality,
    ABC,
):  # noqa: B024
    """Retain one standalone periodic-1D aggregate value."""

    __slots__ = ()


class Periodic1DBandEquivalenceHoppingLocalityAction(
    PeriodicBandEquivalenceHoppingLocalityAction,
    Periodic1DBandEquivalenceHoppingLocality,
    ABC,
):  # noqa: B024
    """Perform one supporting periodic-1D aggregate action."""

    __slots__ = ()


__all__ = [
    "Periodic1DBandEquivalenceHoppingLocality",
    "Periodic1DBandEquivalenceHoppingLocalityAction",
    "Periodic1DBandEquivalenceHoppingLocalityAnalysis",
    "Periodic1DBandEquivalenceHoppingLocalityAnalyzer",
    "Periodic1DBandEquivalenceHoppingLocalityRequest",
    "Periodic1DBandEquivalenceHoppingLocalityValue",
]
