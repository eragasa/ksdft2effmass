"""Authenticated band-equivalence locality visualization action."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ksdft2effmass.verification import VisualizationVerification
from ksdft2effmass.visualizations import (
    BaseVisualizer,
    PngFigureRenderer,
    PngVisualization,
)

if TYPE_CHECKING:
    from ..verification import BandEquivalenceLocalityVerification

from .data import BandEquivalenceLocalityVisualizationData
from .figures import _LocalityRequirementsFigure
from .inventory import BandEquivalenceLocalityVisualizationPlotEnum


class BandEquivalenceLocalityVisualizer(
    BaseVisualizer[
        BandEquivalenceLocalityVisualizationData,
        VisualizationVerification,
        BandEquivalenceLocalityVisualizationPlotEnum,
    ]
):
    """Authenticate and render the closed baseline plot inventory."""

    __slots__ = ("_dpi",)

    def __init__(
        self,
        *,
        data: BandEquivalenceLocalityVisualizationData,
        verification: BandEquivalenceLocalityVerification,
        dpi: int = 180,
    ) -> None:
        if type(data) is not BandEquivalenceLocalityVisualizationData:
            raise TypeError("data must be BandEquivalenceLocalityVisualizationData")
        from ..verification import BandEquivalenceLocalityVerification

        if type(verification) is not BandEquivalenceLocalityVerification:
            raise TypeError("verification must be BandEquivalenceLocalityVerification")
        if type(dpi) is not int:
            raise TypeError("dpi must be a built-in integer")
        if dpi <= 0:
            raise ValueError("dpi must be positive")
        super().__init__(
            data=data,
            verification=verification,
            plots=tuple(BandEquivalenceLocalityVisualizationPlotEnum),
        )
        self._dpi = dpi

    def _render(
        self,
    ) -> frozenset[PngVisualization[BandEquivalenceLocalityVisualizationPlotEnum]]:
        return frozenset(
            {
                PngFigureRenderer(
                    BandEquivalenceLocalityVisualizationPlotEnum.LOCALITY_REQUIREMENTS,
                    _LocalityRequirementsFigure(self.data),
                    self._dpi,
                ).visualize()
            }
        )
