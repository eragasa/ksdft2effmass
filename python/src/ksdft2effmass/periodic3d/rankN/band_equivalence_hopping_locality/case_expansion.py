"""Periodic-3D arbitrary-rank synthetic case-expansion action."""

from __future__ import annotations

from itertools import product

from .base import Periodic3DRankNBandEquivalenceHoppingLocalityAction
from .model import Periodic3DRankNAnalyticCase
from .request import Periodic3DRankNBandEquivalenceHoppingLocalityRequest


class Periodic3DRankNBandEquivalenceHoppingLocalityCaseExpander(
    Periodic3DRankNBandEquivalenceHoppingLocalityAction
):
    """Expand one typed study request into its complete synthetic case inventory."""

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

    @property
    def band_subspace_ranks(self) -> tuple[int, ...]:
        """Return the expanded band-subspace rank inventory."""
        return self.request.band_subspace_ranks

    def execute(self) -> tuple[Periodic3DRankNAnalyticCase, ...]:
        """Return the ordered geometry/rank/depth/scale/transformation cross product."""
        inventory = product(
            self._request.cases,
            self._request.retained_ranks,
            self._request.circuit_depths,
            self._request.parent_scales,
            self._request.transformation_coefficients,
        )
        return tuple(
            Periodic3DRankNAnalyticCase(
                case_identifier=values[0].lattice_control.to_wire(),
                retained_rank=values[1],
                circuit_depth=values[2],
                positive_bonds=values[0].positive_bonds,
                gauge_normalization=values[0].gauge_normalization,
                parent_scale=values[3],
                transformation_coefficient=values[4],
            )
            for values in inventory
        )


__all__ = ["Periodic3DRankNBandEquivalenceHoppingLocalityCaseExpander"]
