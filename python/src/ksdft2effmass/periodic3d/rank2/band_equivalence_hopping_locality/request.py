"""Periodic-3D rank-two band-equivalence/locality request."""

from __future__ import annotations

from projectkoios.physkit.periodic.lattice import DirectLattice3D

from ksdft2effmass.band_equivalence_hopping_locality.definitions import (
    BandEquivalenceHoppingLocalityFamilyEnum,
    BandEquivalenceHoppingLocalityRequest,
)

from .base import Periodic3DRank2BandEquivalenceHoppingLocalityRequestRole


class Periodic3DRank2BandEquivalenceHoppingLocalityRequest(
    Periodic3DRank2BandEquivalenceHoppingLocalityRequestRole,
    BandEquivalenceHoppingLocalityRequest,
):
    """Bind one rank-two study to exact periodic-3D PhysKit lattice geometry."""

    __slots__ = ()

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.dimension != 3:
            raise ValueError("all cases must have spatial dimension three")
        if self.family not in (
            BandEquivalenceHoppingLocalityFamilyEnum.SIMPLE_CUBIC,
            BandEquivalenceHoppingLocalityFamilyEnum.SILICON_INSPIRED,
        ):
            raise ValueError("family must identify a periodic-3D study")
        if self.synthetic_model.retained_rank != 2:
            raise ValueError("synthetic model must retain rank two")
        if any(
            type(case.direct_metric.direct_lattice) is not DirectLattice3D
            for case in self.cases
        ):
            raise TypeError("every case must use the exact PhysKit DirectLattice3D")


__all__ = ["Periodic3DRank2BandEquivalenceHoppingLocalityRequest"]
