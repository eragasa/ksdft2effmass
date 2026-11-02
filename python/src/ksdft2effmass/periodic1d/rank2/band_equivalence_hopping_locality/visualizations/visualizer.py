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
    from ..verification import Periodic1DRank2BandEquivalenceHoppingLocalityVerification

from .data import Periodic1DRank2BandEquivalenceHoppingLocalityVisualizationData
from .figures import _AlignmentFigure, _ErrorChannelFigure, _LocalityFigure
from .inventory import (
    Periodic1DRank2BandEquivalenceHoppingLocalityVisualizationPlotEnum,
)


class Periodic1DRank2BandEquivalenceHoppingLocalityVisualizer(
    BaseVisualizer[
        Periodic1DRank2BandEquivalenceHoppingLocalityVisualizationData,
        VisualizationVerification,
        Periodic1DRank2BandEquivalenceHoppingLocalityVisualizationPlotEnum,
    ]
):
    """Authenticate one projection and render the closed figure inventory."""

    __slots__ = ("_dpi",)

    def __init__(
        self,
        *,
        data: Periodic1DRank2BandEquivalenceHoppingLocalityVisualizationData,
        verification: Periodic1DRank2BandEquivalenceHoppingLocalityVerification,
        dpi: int = 180,
    ) -> None:
        if (
            type(data)
            is not Periodic1DRank2BandEquivalenceHoppingLocalityVisualizationData
        ):
            raise TypeError(
                "data must be Periodic1DRank2BandEquivalenceHoppingLocalityVisualizationData"  # noqa: E501
            )
        from ..verification import (
            Periodic1DRank2BandEquivalenceHoppingLocalityVerification,
        )

        if (
            type(verification)
            is not Periodic1DRank2BandEquivalenceHoppingLocalityVerification
        ):
            raise TypeError(
                "verification must be Periodic1DRank2BandEquivalenceHoppingLocalityVerification"  # noqa: E501
            )
        if type(dpi) is not int:
            raise TypeError("dpi must be a built-in int")
        if dpi <= 0:
            raise ValueError("dpi must be positive")
        super().__init__(
            data=data,
            verification=verification,
            plots=tuple(
                Periodic1DRank2BandEquivalenceHoppingLocalityVisualizationPlotEnum
            ),
        )
        self._dpi = dpi

    def _render(
        self,
    ) -> frozenset[
        PngVisualization[
            Periodic1DRank2BandEquivalenceHoppingLocalityVisualizationPlotEnum
        ]
    ]:
        return frozenset(
            {
                PngFigureRenderer(
                    Periodic1DRank2BandEquivalenceHoppingLocalityVisualizationPlotEnum.ALIGNMENT,
                    _AlignmentFigure(self.data),
                    self._dpi,
                ).visualize(),
                PngFigureRenderer(
                    Periodic1DRank2BandEquivalenceHoppingLocalityVisualizationPlotEnum.LOCALITY,
                    _LocalityFigure(self.data),
                    self._dpi,
                ).visualize(),
                PngFigureRenderer(
                    Periodic1DRank2BandEquivalenceHoppingLocalityVisualizationPlotEnum.ERROR_CHANNELS,
                    _ErrorChannelFigure(self.data),
                    self._dpi,
                ).visualize(),
            }
        )


__all__ = ["Periodic1DRank2BandEquivalenceHoppingLocalityVisualizer"]
