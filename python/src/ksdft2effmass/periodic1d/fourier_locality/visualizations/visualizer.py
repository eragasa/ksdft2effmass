"""Authenticated rank-one Fourier-locality visualization action."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ksdft2effmass.verification import VisualizationVerification
from ksdft2effmass.visualizations import (
    BaseVisualizer,
    PngFigureRenderer,
    PngVisualization,
)

if TYPE_CHECKING:
    from ..verification import Periodic1DFourierLocalityVerification

from .data import Periodic1DFourierLocalityVisualizationData
from .figures import (
    Periodic1DFourierLocalityFigure,
    Periodic1DFourierRouteAgreementFigure,
)
from .inventory import Periodic1DFourierLocalityVisualizationPlotEnum


class Periodic1DFourierLocalityVisualizer(
    BaseVisualizer[
        Periodic1DFourierLocalityVisualizationData,
        VisualizationVerification,
        Periodic1DFourierLocalityVisualizationPlotEnum,
    ]
):
    """Authenticate and render the closed two-figure Fourier-locality inventory."""

    __slots__ = ()

    def __init__(
        self,
        *,
        data: Periodic1DFourierLocalityVisualizationData,
        verification: Periodic1DFourierLocalityVerification,
    ) -> None:
        if not isinstance(data, Periodic1DFourierLocalityVisualizationData):
            raise TypeError("data must be Periodic1DFourierLocalityVisualizationData")
        from ..verification import Periodic1DFourierLocalityVerification

        if not isinstance(verification, Periodic1DFourierLocalityVerification):
            raise TypeError(
                "verification must be Periodic1DFourierLocalityVerification"
            )
        super().__init__(
            data=data,
            verification=verification,
            plots=tuple(Periodic1DFourierLocalityVisualizationPlotEnum),
        )

    def _render(
        self,
    ) -> frozenset[PngVisualization[Periodic1DFourierLocalityVisualizationPlotEnum]]:
        return frozenset(
            {
                PngFigureRenderer(
                    plot=(
                        Periodic1DFourierLocalityVisualizationPlotEnum.fourier_locality
                    ),
                    figure=Periodic1DFourierLocalityFigure(self.data),
                    dpi=160,
                ).visualize(),
                PngFigureRenderer(
                    plot=(
                        Periodic1DFourierLocalityVisualizationPlotEnum.route_agreement
                    ),
                    figure=Periodic1DFourierRouteAgreementFigure(self.data),
                    dpi=160,
                ).visualize(),
            }
        )
