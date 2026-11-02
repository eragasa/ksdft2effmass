"""Periodic-2D rank-two band-equivalence/locality request."""

from __future__ import annotations

from projectkoios.physkit.periodic.lattice import DirectLattice2D

from ksdft2effmass.band_equivalence_hopping_locality.definitions import (
    BandEquivalenceHoppingLocalityFamilyEnum,
    BandEquivalenceHoppingLocalityRequest,
)

from .base import Periodic2DRank2BandEquivalenceHoppingLocalityRequestRole


class Periodic2DRank2BandEquivalenceHoppingLocalityRequest(
    Periodic2DRank2BandEquivalenceHoppingLocalityRequestRole,
    BandEquivalenceHoppingLocalityRequest,
):
    """Bind one rank-two study to exact periodic-2D PhysKit lattice geometry."""

    __slots__ = ()

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.dimension != 2:
            raise ValueError("all cases must have spatial dimension two")
        if self.family not in (
            BandEquivalenceHoppingLocalityFamilyEnum.SQUARE,
            BandEquivalenceHoppingLocalityFamilyEnum.GRAPHENE_INSPIRED,
        ):
            raise ValueError("family must identify a periodic-2D study")
        if self.synthetic_model.retained_rank != 2:
            raise ValueError("synthetic model must retain rank two")
        if any(
            type(case.direct_metric.direct_lattice) is not DirectLattice2D
            for case in self.cases
        ):
            raise TypeError("every case must use the exact PhysKit DirectLattice2D")


__all__ = ["Periodic2DRank2BandEquivalenceHoppingLocalityRequest"]
