"""Authenticated constrained-admissible-set visualization action."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ksdft2effmass.verification import VisualizationVerification
from ksdft2effmass.visualizations import (
    BaseVisualizer,
    PngFigureRenderer,
    PngVisualization,
)

if TYPE_CHECKING:
    from ..verify import Periodic1DConstrainedAdmissibleSetVerification

from .data import Periodic1DConstrainedAdmissibleSetVisualizationData
from .figures import _AdmissibilityFigure, _LocalityChannelsFigure
from .inventory import Periodic1DConstrainedAdmissibleSetVisualizationPlotEnum


class Periodic1DConstrainedAdmissibleSetVisualizer(
    BaseVisualizer[
        Periodic1DConstrainedAdmissibleSetVisualizationData,
        VisualizationVerification,
        Periodic1DConstrainedAdmissibleSetVisualizationPlotEnum,
    ]
):
    """Authenticate one projection and render its closed two-figure inventory."""

    __slots__ = ("_dpi",)

    def __init__(
        self,
        *,
        data: Periodic1DConstrainedAdmissibleSetVisualizationData,
        verification: Periodic1DConstrainedAdmissibleSetVerification,
        dpi: int = 180,
    ) -> None:
        if type(data) is not Periodic1DConstrainedAdmissibleSetVisualizationData:
            raise TypeError(
                "data must be Periodic1DConstrainedAdmissibleSetVisualizationData"
            )
        from ..verify import Periodic1DConstrainedAdmissibleSetVerification

        if type(verification) is not Periodic1DConstrainedAdmissibleSetVerification:
            raise TypeError(
                "verification must be Periodic1DConstrainedAdmissibleSetVerification"
            )
        if type(dpi) is not int:
            raise TypeError("dpi must be a built-in int")
        if dpi <= 0:
            raise ValueError("dpi must be positive")
        super().__init__(
            data=data,
            verification=verification,
            plots=tuple(Periodic1DConstrainedAdmissibleSetVisualizationPlotEnum),
        )
        self._dpi = dpi

    @property
    def dpi(self) -> int:
        """Return the constructor-bound PNG resolution."""
        return self._dpi

    def _render(
        self,
    ) -> frozenset[
        PngVisualization[Periodic1DConstrainedAdmissibleSetVisualizationPlotEnum]
    ]:
        plot = Periodic1DConstrainedAdmissibleSetVisualizationPlotEnum
        return frozenset(
            {
                PngFigureRenderer(
                    plot.ADMISSIBILITY,
                    _AdmissibilityFigure(self.data),
                    self.dpi,
                ).visualize(),
                PngFigureRenderer(
                    plot.LOCALITY_CHANNELS,
                    _LocalityChannelsFigure(self.data),
                    self.dpi,
                ).visualize(),
            }
        )


__all__ = ["Periodic1DConstrainedAdmissibleSetVisualizer"]
