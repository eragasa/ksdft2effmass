"""Periodic-3D rank-two authenticated visualization action."""

from __future__ import annotations

from ksdft2effmass.band_equivalence_hopping_locality.verification import (
    BandEquivalenceHoppingLocalityVerification,
)
from ksdft2effmass.band_equivalence_hopping_locality.visualizations.visualizer import (
    BandEquivalenceHoppingLocalityVisualizer,
)

from ..base import Periodic3DRank2BandEquivalenceHoppingLocalityAction
from .data import Periodic3DRank2BandEquivalenceHoppingLocalityVisualizationData


class Periodic3DRank2BandEquivalenceHoppingLocalityVisualizer(
    BandEquivalenceHoppingLocalityVisualizer,
    Periodic3DRank2BandEquivalenceHoppingLocalityAction,
):
    """Render one authenticated periodic-3D rank-two projection."""

    __slots__ = ()

    def __init__(
        self,
        *,
        data: Periodic3DRank2BandEquivalenceHoppingLocalityVisualizationData,
        verification: BandEquivalenceHoppingLocalityVerification,
        dpi: int = 180,
    ) -> None:
        if (
            type(data)
            is not Periodic3DRank2BandEquivalenceHoppingLocalityVisualizationData
        ):
            raise TypeError(
                "data must be Periodic3DRank2BandEquivalenceHoppingLocalityVisualizationData"  # noqa: E501
            )
        super().__init__(data=data, verification=verification, dpi=dpi)


__all__ = ["Periodic3DRank2BandEquivalenceHoppingLocalityVisualizer"]
