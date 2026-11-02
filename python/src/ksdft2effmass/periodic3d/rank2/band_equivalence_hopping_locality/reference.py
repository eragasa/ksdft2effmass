"""Periodic-3D rank-two independent band-equivalence/locality reference."""

from __future__ import annotations

from dataclasses import dataclass
from typing import override

from ksdft2effmass.band_equivalence_hopping_locality.reference import (
    BandEquivalenceHoppingLocalityIndependentShellPowerAnalyzer,
    BandEquivalenceHoppingLocalityIndependentShellPowerPoint,
    BandEquivalenceHoppingLocalityIndependentShellPowerReference,
)

from .base import (
    Periodic3DRank2BandEquivalenceHoppingLocalityAction,
    Periodic3DRank2BandEquivalenceHoppingLocalityValue,
)
from .request import Periodic3DRank2BandEquivalenceHoppingLocalityRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic3DRank2BandEquivalenceHoppingLocalityIndependentShellPowerReference(
    BandEquivalenceHoppingLocalityIndependentShellPowerReference,
    Periodic3DRank2BandEquivalenceHoppingLocalityValue,
):
    """Retain the independent shell-power reference for one periodic-3D request."""

    request: Periodic3DRank2BandEquivalenceHoppingLocalityRequest
    points: tuple[BandEquivalenceHoppingLocalityIndependentShellPowerPoint, ...]

    def __post_init__(self) -> None:
        if (
            type(self.request)
            is not Periodic3DRank2BandEquivalenceHoppingLocalityRequest
        ):
            raise TypeError(
                "request must be Periodic3DRank2BandEquivalenceHoppingLocalityRequest"
            )
        super().__post_init__()


class Periodic3DRank2BandEquivalenceHoppingLocalityIndependentShellPowerAnalyzer(
    BandEquivalenceHoppingLocalityIndependentShellPowerAnalyzer,
    Periodic3DRank2BandEquivalenceHoppingLocalityAction,
):
    """Execute the independent finite-sum route for one periodic-3D request."""

    __slots__ = ()

    def __init__(
        self,
        *,
        request: Periodic3DRank2BandEquivalenceHoppingLocalityRequest,
    ) -> None:
        if type(request) is not Periodic3DRank2BandEquivalenceHoppingLocalityRequest:
            raise TypeError(
                "request must be Periodic3DRank2BandEquivalenceHoppingLocalityRequest"
            )
        super().__init__(request=request)

    @property
    @override
    def request(self) -> Periodic3DRank2BandEquivalenceHoppingLocalityRequest:
        """Return the exact periodic-3D request bound to this action."""
        request = super().request
        if type(request) is not Periodic3DRank2BandEquivalenceHoppingLocalityRequest:
            raise TypeError("stored request lost periodic-3D rank-two ownership")
        return request

    @override
    def execute(
        self,
    ) -> Periodic3DRank2BandEquivalenceHoppingLocalityIndependentShellPowerReference:
        """Return the dimension- and rank-qualified independent reference."""
        reference = super().execute()
        return (
            Periodic3DRank2BandEquivalenceHoppingLocalityIndependentShellPowerReference(
                request=self.request,
                points=reference.points,
            )
        )


__all__ = [
    "Periodic3DRank2BandEquivalenceHoppingLocalityIndependentShellPowerAnalyzer",
    "Periodic3DRank2BandEquivalenceHoppingLocalityIndependentShellPowerReference",
]
