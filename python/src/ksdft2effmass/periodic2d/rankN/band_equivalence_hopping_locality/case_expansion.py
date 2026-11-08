"""Periodic-2D arbitrary-rank analytic case-expansion action."""

from __future__ import annotations

from itertools import product

from ksdft2effmass.periodic.models import PeriodicModelRole
from ksdft2effmass.periodic.operators import PeriodicBasisInventory
from ksdft2effmass.periodic.periodic2d.operators import Periodic2DBasisIdentity
from ksdft2effmass.periodic.periodic2d.rankN.models import (
    Periodic2DRankNAnalyticParentModel,
)
from ksdft2effmass.periodic2d.rankN.gauge_alignment.transformation import (
    Periodic2DRankNGivensGaugeTransformation,
)

from .base import Periodic2DRankNBandEquivalenceHoppingLocalityAction
from .case import Periodic2DRankNAnalyticCase
from .request import Periodic2DRankNBandEquivalenceHoppingLocalityRequest


class Periodic2DRankNBandEquivalenceHoppingLocalityCaseExpander(
    Periodic2DRankNBandEquivalenceHoppingLocalityAction
):
    """Expand one typed request using an explicitly supplied basis inventory."""

    __slots__ = ("_request", "_basis_inventory")

    def __init__(
        self,
        *,
        request: Periodic2DRankNBandEquivalenceHoppingLocalityRequest,
        basis_inventory: PeriodicBasisInventory[Periodic2DBasisIdentity],
    ) -> None:
        if type(request) is not Periodic2DRankNBandEquivalenceHoppingLocalityRequest:
            raise TypeError("request must be the exact periodic-2D rank-N request")
        if type(basis_inventory) is not PeriodicBasisInventory:
            raise TypeError("basis_inventory must be the exact PeriodicBasisInventory")
        if basis_inventory.retained_ranks != request.retained_ranks:
            raise ValueError("basis inventory ranks must match the requested ranks")
        if any(
            type(entry.basis_identity) is not Periodic2DBasisIdentity
            for entry in basis_inventory.entries
        ):
            raise TypeError(
                "basis inventory must contain Periodic2DBasisIdentity values"
            )
        self._request = request
        self._basis_inventory = basis_inventory

    @property
    def request(self) -> Periodic2DRankNBandEquivalenceHoppingLocalityRequest:
        """Return the immutable aggregate request bound to this action."""
        return self._request

    @property
    def basis_inventory(self) -> PeriodicBasisInventory[Periodic2DBasisIdentity]:
        """Return the explicit calculation-composed basis inventory."""
        return self._basis_inventory

    @property
    def band_subspace_ranks(self) -> tuple[int, ...]:
        """Return the expanded band-subspace rank inventory."""
        return self.request.band_subspace_ranks

    def execute(self) -> tuple[Periodic2DRankNAnalyticCase, ...]:
        """Return the ordered geometry/rank/depth/scale/transformation cross product."""
        inventory = product(
            self._request.cases,
            self._request.retained_ranks,
            self._request.circuit_depths,
            self._request.parent_scales,
            self._request.transformation_coefficients,
        )
        return tuple(
            Periodic2DRankNAnalyticCase(
                case_identifier=values[0].identifier,
                parent_model=Periodic2DRankNAnalyticParentModel(
                    retained_rank=values[1],
                    positive_bonds=values[0].positive_bonds,
                    parent_scale=values[3],
                    basis=self._basis_inventory.basis_identity_for_rank(values[1]),
                    role=PeriodicModelRole.CONTROL_MODEL,
                ),
                gauge_transformation=Periodic2DRankNGivensGaugeTransformation(
                    retained_rank=values[1],
                    circuit_depth=values[2],
                    harmonic_bonds=values[0].positive_bonds,
                    normalization=values[0].gauge_normalization,
                    coefficient=values[4],
                ),
            )
            for values in inventory
        )


__all__ = ["Periodic2DRankNBandEquivalenceHoppingLocalityCaseExpander"]
