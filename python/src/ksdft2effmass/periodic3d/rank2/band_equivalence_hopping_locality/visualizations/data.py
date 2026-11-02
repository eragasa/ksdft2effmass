"""Periodic-3D rank-two authenticated visualization data."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.band_equivalence_hopping_locality.definitions import (
    BandEquivalenceHoppingLocalityFamilyEnum,
)
from ksdft2effmass.band_equivalence_hopping_locality.visualizations.data import (
    BandEquivalenceHoppingLocalityVisualizationData,
)

from ..base import Periodic3DRank2BandEquivalenceHoppingLocalityValue


@dataclass(frozen=True, slots=True, eq=False)
class Periodic3DRank2BandEquivalenceHoppingLocalityVisualizationData(
    BandEquivalenceHoppingLocalityVisualizationData,
    Periodic3DRank2BandEquivalenceHoppingLocalityValue,
):
    """Retain authenticated scalar projection data for a periodic-3D family."""

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.family not in (
            BandEquivalenceHoppingLocalityFamilyEnum.SIMPLE_CUBIC,
            BandEquivalenceHoppingLocalityFamilyEnum.SILICON_INSPIRED,
        ):
            raise ValueError("family must identify a periodic-3D study")


__all__ = ["Periodic3DRank2BandEquivalenceHoppingLocalityVisualizationData"]
