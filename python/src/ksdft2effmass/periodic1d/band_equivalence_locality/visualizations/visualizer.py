"""Authenticated flat-parent band-equivalence visualization action."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ksdft2effmass.verification import VisualizationVerification
from ksdft2effmass.visualizations import (
    BaseVisualizer,
    PngFigureRenderer,
    PngVisualization,
)

if TYPE_CHECKING:
    from ..verification import Periodic1DBandEquivalenceLocalityVerification

from .data import Periodic1DBandEquivalenceLocalityVisualizationData
from .figures import _AlignmentFigure, _ErrorChannelFigure, _LocalityFigure
from .inventory import Periodic1DBandEquivalenceLocalityVisualizationPlotEnum


class Periodic1DBandEquivalenceLocalityVisualizer(
    BaseVisualizer[
        Periodic1DBandEquivalenceLocalityVisualizationData,
        VisualizationVerification,
        Periodic1DBandEquivalenceLocalityVisualizationPlotEnum,
    ]
):
    """Authenticate one projection and render the closed figure inventory."""

    __slots__ = ("_dpi",)

    def __init__(
        self,
        *,
        data: Periodic1DBandEquivalenceLocalityVisualizationData,
        verification: Periodic1DBandEquivalenceLocalityVerification,
        dpi: int = 180,
    ) -> None:
        if type(data) is not Periodic1DBandEquivalenceLocalityVisualizationData:
            raise TypeError(
                "data must be Periodic1DBandEquivalenceLocalityVisualizationData"
            )
        from ..verification import Periodic1DBandEquivalenceLocalityVerification

        if type(verification) is not Periodic1DBandEquivalenceLocalityVerification:
            raise TypeError(
                "verification must be Periodic1DBandEquivalenceLocalityVerification"
            )
        if type(dpi) is not int:
            raise TypeError("dpi must be a built-in int")
        if dpi <= 0:
            raise ValueError("dpi must be positive")
        super().__init__(
            data=data,
            verification=verification,
            plots=tuple(Periodic1DBandEquivalenceLocalityVisualizationPlotEnum),
        )
        self._dpi = dpi

    def _render(
        self,
    ) -> frozenset[
        PngVisualization[Periodic1DBandEquivalenceLocalityVisualizationPlotEnum]
    ]:
        return frozenset(
            {
                PngFigureRenderer(
                    Periodic1DBandEquivalenceLocalityVisualizationPlotEnum.ALIGNMENT,
                    _AlignmentFigure(self.data),
                    self._dpi,
                ).visualize(),
                PngFigureRenderer(
                    Periodic1DBandEquivalenceLocalityVisualizationPlotEnum.LOCALITY,
                    _LocalityFigure(self.data),
                    self._dpi,
                ).visualize(),
                PngFigureRenderer(
                    Periodic1DBandEquivalenceLocalityVisualizationPlotEnum.ERROR_CHANNELS,
                    _ErrorChannelFigure(self.data),
                    self._dpi,
                ).visualize(),
            }
        )


__all__ = ["Periodic1DBandEquivalenceLocalityVisualizer"]
