"""Authenticated Mathieu1D visualization action."""

from ksdft2effmass.visualizations import (
    BaseVisualizer,
    PngFigureRenderer,
    PngVisualization,
)

from ..verification_values import Mathieu1dVerification
from .data import Mathieu1dVisualizationData
from .figures import (
    Mathieu1dBandPlot,
    Mathieu1dBandSubplot,
    Mathieu1dFiniteReductionFigure,
    Mathieu1dHoppingPlot,
    Mathieu1dHoppingSubplot,
    Mathieu1dPublicationSummaryFigure,
    Mathieu1dRangePlot,
    Mathieu1dRangeSubplot,
    Mathieu1dRefinementPlot,
    Mathieu1dRefinementSubplot,
)
from .inventory import Mathieu1dVisualizationPlotEnum


class Mathieu1dVisualizer(
    BaseVisualizer[
        Mathieu1dVisualizationData,
        Mathieu1dVerification,
        Mathieu1dVisualizationPlotEnum,
    ]
):
    """Authenticate and render the closed native Mathieu1D figure inventory."""

    __slots__ = ()

    def __init__(
        self,
        *,
        data: Mathieu1dVisualizationData,
        verification: Mathieu1dVerification,
    ) -> None:
        if not isinstance(data, Mathieu1dVisualizationData):
            raise TypeError("data must be Mathieu1dVisualizationData")
        if not isinstance(verification, Mathieu1dVerification):
            raise TypeError("verification must be Mathieu1dVerification")
        super().__init__(
            data=data,
            verification=verification,
            plots=tuple(Mathieu1dVisualizationPlotEnum),
        )

    def _render(
        self,
    ) -> frozenset[PngVisualization[Mathieu1dVisualizationPlotEnum]]:
        refinement_plot = Mathieu1dRefinementPlot(self.data)
        band_plot = Mathieu1dBandPlot(self.data)
        hopping_plot = Mathieu1dHoppingPlot(self.data)
        range_plot = Mathieu1dRangePlot(self.data)
        figure = Mathieu1dFiniteReductionFigure(
            refinement=Mathieu1dRefinementSubplot(refinement_plot),
            bands=Mathieu1dBandSubplot(band_plot),
            hoppings=Mathieu1dHoppingSubplot(hopping_plot),
            ranges=Mathieu1dRangeSubplot(range_plot),
        )
        summary = Mathieu1dPublicationSummaryFigure(self.data)
        return frozenset(
            {
                PngFigureRenderer(
                    plot=Mathieu1dVisualizationPlotEnum.finite_reduction,
                    figure=figure,
                    dpi=160,
                ).visualize(),
                PngFigureRenderer(
                    plot=Mathieu1dVisualizationPlotEnum.publication_summary,
                    figure=summary,
                    dpi=200,
                ).visualize(),
            }
        )
