"""Authenticated constrained-admissible-set visualization action."""

from ksdft2effmass.visualizations import (
    BaseVisualizer,
    PngFigureRenderer,
    PngVisualization,
)

from ..verification import Periodic1DConstrainedAdmissibleSetVerification
from .data import Periodic1DConstrainedAdmissibleSetVisualizationData
from .figures import _AdmissibilityFigure, _LocalityChannelsFigure
from .inventory import Periodic1DConstrainedAdmissibleSetVisualizationPlotEnum


class Periodic1DConstrainedAdmissibleSetVisualizer(
    BaseVisualizer[
        Periodic1DConstrainedAdmissibleSetVisualizationData,
        Periodic1DConstrainedAdmissibleSetVerification,
        Periodic1DConstrainedAdmissibleSetVisualizationPlotEnum,
    ]
):
    """Render the closed authenticated constrained-admissible-set inventory."""

    __slots__ = ("_renderers",)

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
        if type(verification) is not Periodic1DConstrainedAdmissibleSetVerification:
            raise TypeError(
                "verification must be Periodic1DConstrainedAdmissibleSetVerification"
            )
        if type(dpi) is not int:
            raise TypeError("dpi must be a built-in int")
        if dpi <= 0:
            raise ValueError("dpi must be positive")
        plots = tuple(Periodic1DConstrainedAdmissibleSetVisualizationPlotEnum)
        super().__init__(data=data, verification=verification, plots=plots)
        plot = Periodic1DConstrainedAdmissibleSetVisualizationPlotEnum
        self._renderers = frozenset(
            {
                PngFigureRenderer(
                    plot=plot.ADMISSIBILITY,
                    figure=_AdmissibilityFigure(data),
                    dpi=dpi,
                ),
                PngFigureRenderer(
                    plot=plot.LOCALITY_CHANNELS,
                    figure=_LocalityChannelsFigure(data),
                    dpi=dpi,
                ),
            }
        )
        if {renderer.plot for renderer in self._renderers} != set(self.plots):
            raise RuntimeError(
                "constrained-admissible-set renderers must cover the closed inventory"
            )

    def _render(
        self,
    ) -> frozenset[
        PngVisualization[Periodic1DConstrainedAdmissibleSetVisualizationPlotEnum]
    ]:
        return frozenset(renderer.visualize() for renderer in self._renderers)


__all__ = ["Periodic1DConstrainedAdmissibleSetVisualizer"]
