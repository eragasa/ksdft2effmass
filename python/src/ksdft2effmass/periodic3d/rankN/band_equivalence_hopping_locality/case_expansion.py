"""Periodic-3D arbitrary-rank analytic case-expansion action."""

from __future__ import annotations

from itertools import product

from ksdft2effmass.periodic3d.base import Periodic3DCapability

from .model import Periodic3DRankNAnalyticCase
from .request import Periodic3DRankNBandEquivalenceHoppingLocalityRequest


class Periodic3DRankNBandEquivalenceHoppingLocalityCaseExpander(Periodic3DCapability):
    """Expand one typed study request into its complete analytic case inventory."""

    __slots__ = ("_request",)

    def __init__(
        self,
        *,
        request: Periodic3DRankNBandEquivalenceHoppingLocalityRequest,
    ) -> None:
        if type(request) is not Periodic3DRankNBandEquivalenceHoppingLocalityRequest:
            raise TypeError("request must be the exact periodic-3D rank-N request")
        self._request = request

    @property
    def request(self) -> Periodic3DRankNBandEquivalenceHoppingLocalityRequest:
        """Return the immutable aggregate request bound to this action."""
        return self._request

    def execute(self) -> tuple[Periodic3DRankNAnalyticCase, ...]:
        """Return the ordered geometry/rank/depth/scale/attack cross product."""
        inventory = product(
            self._request.cases,
            self._request.retained_ranks,
            self._request.circuit_depths,
            self._request.parent_scales,
            self._request.attack_coefficients,
        )
        return tuple(
            Periodic3DRankNAnalyticCase(
                case_identifier=values[0].identifier,
                retained_rank=values[1],
                circuit_depth=values[2],
                positive_bonds=values[0].positive_bonds,
                gauge_normalization=values[0].gauge_normalization,
                parent_scale=values[3],
                attack_coefficient=values[4],
            )
            for values in inventory
        )


__all__ = ["Periodic3DRankNBandEquivalenceHoppingLocalityCaseExpander"]
