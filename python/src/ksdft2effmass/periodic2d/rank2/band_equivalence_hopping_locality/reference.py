"""Periodic-2D rank-two independent band-equivalence/locality reference."""

from __future__ import annotations

from dataclasses import dataclass
from typing import override

from ksdft2effmass.band_equivalence_hopping_locality.reference import (
    BandEquivalenceHoppingLocalityIndependentShellPowerAnalyzer,
    BandEquivalenceHoppingLocalityIndependentShellPowerPoint,
    BandEquivalenceHoppingLocalityIndependentShellPowerReference,
)

from .base import (
    Periodic2DRank2BandEquivalenceHoppingLocalityAction,
    Periodic2DRank2BandEquivalenceHoppingLocalityValue,
)
from .request import Periodic2DRank2BandEquivalenceHoppingLocalityRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic2DRank2BandEquivalenceHoppingLocalityIndependentShellPowerReference(
    BandEquivalenceHoppingLocalityIndependentShellPowerReference,
    Periodic2DRank2BandEquivalenceHoppingLocalityValue,
):
    """Retain the independent shell-power reference for one periodic-2D request."""

    request: Periodic2DRank2BandEquivalenceHoppingLocalityRequest
    points: tuple[BandEquivalenceHoppingLocalityIndependentShellPowerPoint, ...]

    def __post_init__(self) -> None:
        if (
            type(self.request)
            is not Periodic2DRank2BandEquivalenceHoppingLocalityRequest
        ):
            raise TypeError(
                "request must be Periodic2DRank2BandEquivalenceHoppingLocalityRequest"
            )
        super().__post_init__()


class Periodic2DRank2BandEquivalenceHoppingLocalityIndependentShellPowerAnalyzer(
    BandEquivalenceHoppingLocalityIndependentShellPowerAnalyzer,
    Periodic2DRank2BandEquivalenceHoppingLocalityAction,
):
    """Execute the independent finite-sum route for one periodic-2D request."""

    __slots__ = ()

    def __init__(
        self,
        *,
        request: Periodic2DRank2BandEquivalenceHoppingLocalityRequest,
    ) -> None:
        if type(request) is not Periodic2DRank2BandEquivalenceHoppingLocalityRequest:
            raise TypeError(
                "request must be Periodic2DRank2BandEquivalenceHoppingLocalityRequest"
            )
        super().__init__(request=request)

    @property
    @override
    def request(self) -> Periodic2DRank2BandEquivalenceHoppingLocalityRequest:
        """Return the exact periodic-2D request bound to this action."""
        request = super().request
        if type(request) is not Periodic2DRank2BandEquivalenceHoppingLocalityRequest:
            raise TypeError("stored request lost periodic-2D rank-two ownership")
        return request

    @override
    def execute(
        self,
    ) -> Periodic2DRank2BandEquivalenceHoppingLocalityIndependentShellPowerReference:
        """Return the dimension- and rank-qualified independent reference."""
        reference = super().execute()
        return (
            Periodic2DRank2BandEquivalenceHoppingLocalityIndependentShellPowerReference(
                request=self.request,
                points=reference.points,
            )
        )


__all__ = [
    "Periodic2DRank2BandEquivalenceHoppingLocalityIndependentShellPowerAnalyzer",
    "Periodic2DRank2BandEquivalenceHoppingLocalityIndependentShellPowerReference",
]
