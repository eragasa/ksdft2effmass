"""Periodic-2D rank-two authenticated visualization data."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.band_equivalence_hopping_locality.definitions import (
    BandEquivalenceHoppingLocalityFamilyEnum,
)
from ksdft2effmass.band_equivalence_hopping_locality.visualizations.data import (
    BandEquivalenceHoppingLocalityVisualizationData,
)

from ..base import Periodic2DRank2BandEquivalenceHoppingLocalityValue


@dataclass(frozen=True, slots=True, eq=False)
class Periodic2DRank2BandEquivalenceHoppingLocalityVisualizationData(
    BandEquivalenceHoppingLocalityVisualizationData,
    Periodic2DRank2BandEquivalenceHoppingLocalityValue,
):
    """Retain authenticated scalar projection data for a periodic-2D family."""

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.family not in (
            BandEquivalenceHoppingLocalityFamilyEnum.SQUARE,
            BandEquivalenceHoppingLocalityFamilyEnum.GRAPHENE_INSPIRED,
        ):
            raise ValueError("family must identify a periodic-2D study")


__all__ = ["Periodic2DRank2BandEquivalenceHoppingLocalityVisualizationData"]
