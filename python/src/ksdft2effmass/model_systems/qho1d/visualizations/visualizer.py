"""Authenticated QHO1D visualization action."""

from ksdft2effmass.visualizations import (
    BaseVisualizer,
    PngFigureRenderer,
    PngVisualization,
)

from ..verification_values import Qho1dVerification
from .data import Qho1dVisualizationData
from .figures import (
    _Qho1dDiagnosticFigure,
    _Qho1dEigenstateDistortionFigure,
    _Qho1dEigenstateFigure,
)
from .inventory import Qho1dVisualizationPlotEnum


class Qho1dVisualizer(
    BaseVisualizer[
        Qho1dVisualizationData,
        Qho1dVerification,
        Qho1dVisualizationPlotEnum,
    ]
):
    """Render the closed QHO1D figure inventory from authenticated data."""

    __slots__ = ()

    def __init__(
        self,
        *,
        data: Qho1dVisualizationData,
        verification: Qho1dVerification,
    ) -> None:
        if not isinstance(data, Qho1dVisualizationData):
            raise TypeError("data must be Qho1dVisualizationData")
        if not isinstance(verification, Qho1dVerification):
            raise TypeError("verification must be Qho1dVerification")
        super().__init__(
            data=data,
            verification=verification,
            plots=tuple(Qho1dVisualizationPlotEnum),
        )

    def _render(
        self,
    ) -> frozenset[PngVisualization[Qho1dVisualizationPlotEnum]]:
        renderers = (
            PngFigureRenderer(
                plot=Qho1dVisualizationPlotEnum.eigenstates,
                figure=_Qho1dEigenstateFigure(self.data),
                dpi=180,
            ),
            PngFigureRenderer(
                plot=Qho1dVisualizationPlotEnum.eigenstate_distortion,
                figure=_Qho1dEigenstateDistortionFigure(self.data),
                dpi=180,
            ),
            PngFigureRenderer(
                plot=Qho1dVisualizationPlotEnum.diagnostics,
                figure=_Qho1dDiagnosticFigure(self.data),
                dpi=180,
            ),
        )
        return frozenset(renderer.visualize() for renderer in renderers)
