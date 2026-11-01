"""Verified rank-two composite-alignment visualization action."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ksdft2effmass.verification import VisualizationVerification
from ksdft2effmass.visualizations import (
    BaseVisualizer,
    PngFigureRenderer,
    PngVisualization,
)

if TYPE_CHECKING:
    from ..verification import Periodic1DCompositeBandAlignmentVerification

from .data import Periodic1DCompositeBandAlignmentVisualizationData
from .figures import (
    _AlignmentFigure,
    _ErrorChannelFigure,
    _ErrorTrajectoryFigure,
    _HoppingDiagnosticFigure,
    _LocalityFigure,
    _RecoveryControlFigure,
)
from .inventory import Periodic1DCompositeBandAlignmentVisualizationPlotEnum


class Periodic1DCompositeBandAlignmentVisualizer(
    BaseVisualizer[
        Periodic1DCompositeBandAlignmentVisualizationData,
        VisualizationVerification,
        Periodic1DCompositeBandAlignmentVisualizationPlotEnum,
    ]
):
    """Admit verified visualization data and render the closed figure inventory."""

    __slots__ = ("_dpi",)

    def __init__(
        self,
        *,
        data: Periodic1DCompositeBandAlignmentVisualizationData,
        verification: Periodic1DCompositeBandAlignmentVerification,
        dpi: int = 180,
    ) -> None:
        if not isinstance(data, Periodic1DCompositeBandAlignmentVisualizationData):
            raise TypeError(
                "data must be Periodic1DCompositeBandAlignmentVisualizationData"
            )
        from ..verification import Periodic1DCompositeBandAlignmentVerification

        if not isinstance(verification, Periodic1DCompositeBandAlignmentVerification):
            raise TypeError(
                "verification must be Periodic1DCompositeBandAlignmentVerification"
            )
        if type(dpi) is not int:
            raise TypeError("dpi must be a built-in int")
        if dpi <= 0:
            raise ValueError("dpi must be positive")
        super().__init__(
            data=data,
            verification=verification,
            plots=tuple(Periodic1DCompositeBandAlignmentVisualizationPlotEnum),
        )
        self._dpi = dpi

    @property
    def dpi(self) -> int:
        """Return the constructor-bound PNG resolution."""
        return self._dpi

    def _render(
        self,
    ) -> frozenset[
        PngVisualization[Periodic1DCompositeBandAlignmentVisualizationPlotEnum]
    ]:
        return frozenset(
            {
                PngFigureRenderer(
                    Periodic1DCompositeBandAlignmentVisualizationPlotEnum.ALIGNMENT,
                    _AlignmentFigure(self.data),
                    self.dpi,
                ).visualize(),
                PngFigureRenderer(
                    Periodic1DCompositeBandAlignmentVisualizationPlotEnum.RECOVERY_CONTROLS,
                    _RecoveryControlFigure(self.data),
                    self.dpi,
                ).visualize(),
                PngFigureRenderer(
                    Periodic1DCompositeBandAlignmentVisualizationPlotEnum.HOPPING_DIAGNOSTICS,
                    _HoppingDiagnosticFigure(self.data),
                    self.dpi,
                ).visualize(),
                PngFigureRenderer(
                    Periodic1DCompositeBandAlignmentVisualizationPlotEnum.LOCALITY,
                    _LocalityFigure(self.data),
                    self.dpi,
                ).visualize(),
                PngFigureRenderer(
                    Periodic1DCompositeBandAlignmentVisualizationPlotEnum.ERROR_CHANNELS,
                    _ErrorChannelFigure(self.data),
                    self.dpi,
                ).visualize(),
                PngFigureRenderer(
                    Periodic1DCompositeBandAlignmentVisualizationPlotEnum.ERROR_TRAJECTORIES,
                    _ErrorTrajectoryFigure(self.data),
                    self.dpi,
                ).visualize(),
            }
        )
