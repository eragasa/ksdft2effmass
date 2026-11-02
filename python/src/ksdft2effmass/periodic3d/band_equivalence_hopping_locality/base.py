"""Periodic-3D ownership roles for the band-equivalence/locality aggregate."""

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
from ksdft2effmass.periodic3d.band_equivalence.base import (
    Periodic3DBandEquivalence,
    Periodic3DBandEquivalenceAnalysis,
    Periodic3DBandEquivalenceAnalyzer,
    Periodic3DBandEquivalenceRequest,
)


class Periodic3DBandEquivalenceHoppingLocality(
    Periodic3DBandEquivalence,
    PeriodicBandEquivalenceHoppingLocality,
    ABC,
):  # noqa: B024
    """Coordinate the aggregate on a periodic three-dimensional lattice."""

    __slots__ = ()


class Periodic3DBandEquivalenceHoppingLocalityRequest(
    Periodic3DBandEquivalenceRequest,
    PeriodicBandEquivalenceHoppingLocalityRequest,
    Periodic3DBandEquivalenceHoppingLocality,
    ABC,
):
    """Bind one periodic-3D aggregate request."""

    __slots__ = ()


class Periodic3DBandEquivalenceHoppingLocalityAnalysis[
    RequestT: Periodic3DBandEquivalenceHoppingLocalityRequest,
](
    Periodic3DBandEquivalenceAnalysis[RequestT],
    PeriodicBandEquivalenceHoppingLocalityAnalysis[RequestT],
    Periodic3DBandEquivalenceHoppingLocality,
    ABC,
):
    """Retain one periodic-3D aggregate analysis."""

    __slots__ = ()


class Periodic3DBandEquivalenceHoppingLocalityAnalyzer[
    RequestT: Periodic3DBandEquivalenceHoppingLocalityRequest,
](
    Periodic3DBandEquivalenceAnalyzer[RequestT],
    PeriodicBandEquivalenceHoppingLocalityAnalyzer[RequestT],
    Periodic3DBandEquivalenceHoppingLocality,
    ABC,
):
    """Execute one periodic-3D aggregate request."""

    __slots__ = ()

    @abstractmethod
    def execute(self) -> Periodic3DBandEquivalenceHoppingLocalityAnalysis[RequestT]:
        """Execute the bound periodic-3D aggregate."""


class Periodic3DBandEquivalenceHoppingLocalityValue(
    PeriodicBandEquivalenceHoppingLocalityValue,
    Periodic3DBandEquivalenceHoppingLocality,
    ABC,
):  # noqa: B024
    """Retain one standalone periodic-3D aggregate value."""

    __slots__ = ()


class Periodic3DBandEquivalenceHoppingLocalityAction(
    PeriodicBandEquivalenceHoppingLocalityAction,
    Periodic3DBandEquivalenceHoppingLocality,
    ABC,
):  # noqa: B024
    """Perform one supporting periodic-3D aggregate action."""

    __slots__ = ()


__all__ = [
    "Periodic3DBandEquivalenceHoppingLocality",
    "Periodic3DBandEquivalenceHoppingLocalityAction",
    "Periodic3DBandEquivalenceHoppingLocalityAnalysis",
    "Periodic3DBandEquivalenceHoppingLocalityAnalyzer",
    "Periodic3DBandEquivalenceHoppingLocalityRequest",
    "Periodic3DBandEquivalenceHoppingLocalityValue",
]
