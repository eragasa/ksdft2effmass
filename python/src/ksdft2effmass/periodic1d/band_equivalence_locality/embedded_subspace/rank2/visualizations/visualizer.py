"""Authenticated renderers for embedded rank-two analyses."""

from __future__ import annotations

from ksdft2effmass.visualizations import (
    BaseVisualizer,
    PngFigureRenderer,
    PngVisualization,
)

from ..retention.calculation_verification import (
    Periodic1DRank2CalculationVerification,
)
from ..retention.verification import (
    Periodic1DRank2ParentFamilyVerification,
    Periodic1DRank2Verification,
)
from ..retention.visualization_data import (
    Periodic1DRank2CalculationVisualizationData,
    Periodic1DRank2ParentFamilyVisualizationData,
    Periodic1DRank2VisualizationData,
)
from .figures import (
    _AdaptiveAmplitudeRefinementFigure,
    _BandAndAlignmentFigure,
    _FamilyAlignmentLandscapeFigure,
    _FamilyLocalityLandscapeFigure,
    _FamilyQualificationFigure,
    _LocalityFigure,
    _MomentumRefinementFigure,
    _NumericalResidualFigure,
    _TruncationConsequencesFigure,
)
from .inventory import (
    Periodic1DRank2CalculationVisualizationPlot,
    Periodic1DRank2ParentFamilyVisualizationPlot,
    Periodic1DRank2VisualizationPlot,
)


class Periodic1DRank2CalculationVisualizer(
    BaseVisualizer[
        Periodic1DRank2CalculationVisualizationData,
        Periodic1DRank2CalculationVerification,
        Periodic1DRank2CalculationVisualizationPlot,
    ]
):
    """Render aggregate refinement and truncation channels."""

    __slots__ = ("_dpi",)

    def __init__(
        self,
        *,
        data: Periodic1DRank2CalculationVisualizationData,
        verification: Periodic1DRank2CalculationVerification,
        dpi: int = 180,
    ) -> None:
        if type(data) is not (Periodic1DRank2CalculationVisualizationData):
            raise TypeError("data must be calculation visualization data")
        if type(verification) is not (Periodic1DRank2CalculationVerification):
            raise TypeError("verification must be calculation verification")
        if type(dpi) is not int:
            raise TypeError("dpi must be a built-in int")
        if dpi <= 0:
            raise ValueError("dpi must be positive")
        if not all(
            (
                data.momentum_fine_mesh_sizes,
                data.adaptive_level_indices,
                data.truncation_maximum_ranges,
                data.truncation_amplitudes,
            )
        ):
            raise ValueError("rendering requires complete aggregate channels")
        super().__init__(
            data=data,
            verification=verification,
            plots=tuple(Periodic1DRank2CalculationVisualizationPlot),
        )
        self._dpi = dpi

    def _render(
        self,
    ) -> frozenset[PngVisualization[Periodic1DRank2CalculationVisualizationPlot]]:
        plot = Periodic1DRank2CalculationVisualizationPlot
        return frozenset(
            {
                PngFigureRenderer(
                    plot.MOMENTUM_REFINEMENT,
                    _MomentumRefinementFigure(self.data),
                    self._dpi,
                ).visualize(),
                PngFigureRenderer(
                    plot.ADAPTIVE_AMPLITUDE_REFINEMENT,
                    _AdaptiveAmplitudeRefinementFigure(self.data),
                    self._dpi,
                ).visualize(),
                PngFigureRenderer(
                    plot.TRUNCATION_CONSEQUENCES,
                    _TruncationConsequencesFigure(self.data),
                    self._dpi,
                ).visualize(),
            }
        )


class Periodic1DRank2Visualizer(
    BaseVisualizer[
        Periodic1DRank2VisualizationData,
        Periodic1DRank2Verification,
        Periodic1DRank2VisualizationPlot,
    ]
):
    """Render the closed single-parent inventory from authenticated data."""

    __slots__ = ("_dpi",)

    def __init__(
        self,
        *,
        data: Periodic1DRank2VisualizationData,
        verification: Periodic1DRank2Verification,
        dpi: int = 180,
    ) -> None:
        if type(dpi) is not int:
            raise TypeError("dpi must be a built-in int")
        if dpi <= 0:
            raise ValueError("dpi must be positive")
        if not data.amplitudes:
            raise ValueError("rendering requires a qualified embedded projection")
        super().__init__(
            data=data,
            verification=verification,
            plots=tuple(Periodic1DRank2VisualizationPlot),
        )
        self._dpi = dpi

    def _render(
        self,
    ) -> frozenset[PngVisualization[Periodic1DRank2VisualizationPlot]]:
        plot = Periodic1DRank2VisualizationPlot
        return frozenset(
            {
                PngFigureRenderer(
                    plot.BAND_AND_ALIGNMENT,
                    _BandAndAlignmentFigure(self.data),
                    self._dpi,
                ).visualize(),
                PngFigureRenderer(
                    plot.LOCALITY,
                    _LocalityFigure(self.data),
                    self._dpi,
                ).visualize(),
                PngFigureRenderer(
                    plot.NUMERICAL_RESIDUALS,
                    _NumericalResidualFigure(self.data),
                    self._dpi,
                ).visualize(),
            }
        )


class Periodic1DRank2ParentFamilyVisualizer(
    BaseVisualizer[
        Periodic1DRank2ParentFamilyVisualizationData,
        Periodic1DRank2ParentFamilyVerification,
        Periodic1DRank2ParentFamilyVisualizationPlot,
    ]
):
    """Render the closed parent-family inventory from authenticated data."""

    __slots__ = ("_dpi",)

    def __init__(
        self,
        *,
        data: Periodic1DRank2ParentFamilyVisualizationData,
        verification: Periodic1DRank2ParentFamilyVerification,
        dpi: int = 180,
    ) -> None:
        if type(dpi) is not int:
            raise TypeError("dpi must be a built-in int")
        if dpi <= 0:
            raise ValueError("dpi must be positive")
        super().__init__(
            data=data,
            verification=verification,
            plots=tuple(Periodic1DRank2ParentFamilyVisualizationPlot),
        )
        self._dpi = dpi

    def _render(
        self,
    ) -> frozenset[PngVisualization[Periodic1DRank2ParentFamilyVisualizationPlot]]:
        plot = Periodic1DRank2ParentFamilyVisualizationPlot
        return frozenset(
            {
                PngFigureRenderer(
                    plot.ALIGNMENT_LANDSCAPE,
                    _FamilyAlignmentLandscapeFigure(self.data),
                    self._dpi,
                ).visualize(),
                PngFigureRenderer(
                    plot.LOCALITY_LANDSCAPE,
                    _FamilyLocalityLandscapeFigure(self.data),
                    self._dpi,
                ).visualize(),
                PngFigureRenderer(
                    plot.QUALIFICATION,
                    _FamilyQualificationFigure(self.data),
                    self._dpi,
                ).visualize(),
            }
        )


__all__ = [
    "Periodic1DRank2CalculationVisualizer",
    "Periodic1DRank2ParentFamilyVisualizer",
    "Periodic1DRank2Visualizer",
]
