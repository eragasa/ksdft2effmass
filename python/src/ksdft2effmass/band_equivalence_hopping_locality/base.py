"""Scientific ownership roles for the band-equivalence/locality aggregate."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.analysis.model_adequacy.band_equivalence.base import (
    BandEquivalence,
    BandEquivalenceAnalysis,
    BandEquivalenceAnalyzer,
    BandEquivalenceRequest,
    PeriodicBandEquivalence,
    PeriodicBandEquivalenceAnalysis,
    PeriodicBandEquivalenceAnalyzer,
    PeriodicBandEquivalenceRequest,
)


class BandEquivalenceHoppingLocality(BandEquivalence, ABC):  # noqa: B024
    """Coordinate distinct band-equivalence and locality operations.

    This aggregate remains founded on band equivalence. Membership does not transfer
    ownership of gauge alignment, frame transport, hopping locality, or irreversible
    support truncation from their dedicated capability hierarchies.
    """

    __slots__ = ()

    @property
    @final
    def aggregate_operation_identifier(self) -> str:
        """Return the stable aggregate-operation identity."""
        return "band-equivalence-hopping-locality"


class BandEquivalenceHoppingLocalityRequest(
    BandEquivalenceRequest,
    BandEquivalenceHoppingLocality,
    ABC,
):
    """Bind one aggregate request without absorbing suboperation ownership."""

    __slots__ = ()


class BandEquivalenceHoppingLocalityAnalysis[
    RequestT: BandEquivalenceHoppingLocalityRequest,
](
    BandEquivalenceAnalysis[RequestT],
    BandEquivalenceHoppingLocality,
    ABC,
):
    """Retain one request-bound aggregate analysis."""

    __slots__ = ()


class BandEquivalenceHoppingLocalityAnalyzer[
    RequestT: BandEquivalenceHoppingLocalityRequest,
](
    BandEquivalenceAnalyzer[RequestT],
    BandEquivalenceHoppingLocality,
    ABC,
):
    """Execute one bound aggregate request."""

    __slots__ = ()

    @abstractmethod
    def execute(self) -> BandEquivalenceHoppingLocalityAnalysis[RequestT]:
        """Execute the aggregate without additional arguments."""


class BandEquivalenceHoppingLocalityValue(
    BandEquivalenceHoppingLocality,
    ABC,
):  # noqa: B024
    """Retain one standalone aggregate-owned scientific value."""

    __slots__ = ()


class BandEquivalenceHoppingLocalityAction(
    BandEquivalenceHoppingLocality,
    ABC,
):  # noqa: B024
    """Perform one supporting aggregate action outside the main analyzer role."""

    __slots__ = ()


class PeriodicBandEquivalenceHoppingLocality(
    PeriodicBandEquivalence,
    BandEquivalenceHoppingLocality,
    ABC,
):  # noqa: B024
    """Coordinate the aggregate under periodic boundary conditions."""

    __slots__ = ()


class PeriodicBandEquivalenceHoppingLocalityRequest(
    PeriodicBandEquivalenceRequest,
    BandEquivalenceHoppingLocalityRequest,
    PeriodicBandEquivalenceHoppingLocality,
    ABC,
):
    """Bind one periodic aggregate request."""

    __slots__ = ()


class PeriodicBandEquivalenceHoppingLocalityAnalysis[
    RequestT: PeriodicBandEquivalenceHoppingLocalityRequest,
](
    PeriodicBandEquivalenceAnalysis[RequestT],
    BandEquivalenceHoppingLocalityAnalysis[RequestT],
    PeriodicBandEquivalenceHoppingLocality,
    ABC,
):
    """Retain one periodic aggregate analysis."""

    __slots__ = ()


class PeriodicBandEquivalenceHoppingLocalityAnalyzer[
    RequestT: PeriodicBandEquivalenceHoppingLocalityRequest,
](
    PeriodicBandEquivalenceAnalyzer[RequestT],
    BandEquivalenceHoppingLocalityAnalyzer[RequestT],
    PeriodicBandEquivalenceHoppingLocality,
    ABC,
):
    """Execute one periodic aggregate request."""

    __slots__ = ()

    @abstractmethod
    def execute(self) -> PeriodicBandEquivalenceHoppingLocalityAnalysis[RequestT]:
        """Execute the bound periodic aggregate."""


class PeriodicBandEquivalenceHoppingLocalityValue(
    BandEquivalenceHoppingLocalityValue,
    PeriodicBandEquivalenceHoppingLocality,
    ABC,
):  # noqa: B024
    """Retain one standalone periodic aggregate value."""

    __slots__ = ()


class PeriodicBandEquivalenceHoppingLocalityAction(
    BandEquivalenceHoppingLocalityAction,
    PeriodicBandEquivalenceHoppingLocality,
    ABC,
):  # noqa: B024
    """Perform one supporting periodic aggregate action."""

    __slots__ = ()


__all__ = [
    "BandEquivalenceHoppingLocality",
    "BandEquivalenceHoppingLocalityAction",
    "BandEquivalenceHoppingLocalityAnalysis",
    "BandEquivalenceHoppingLocalityAnalyzer",
    "BandEquivalenceHoppingLocalityRequest",
    "BandEquivalenceHoppingLocalityValue",
    "PeriodicBandEquivalenceHoppingLocality",
    "PeriodicBandEquivalenceHoppingLocalityAction",
    "PeriodicBandEquivalenceHoppingLocalityAnalysis",
    "PeriodicBandEquivalenceHoppingLocalityAnalyzer",
    "PeriodicBandEquivalenceHoppingLocalityRequest",
    "PeriodicBandEquivalenceHoppingLocalityValue",
]
