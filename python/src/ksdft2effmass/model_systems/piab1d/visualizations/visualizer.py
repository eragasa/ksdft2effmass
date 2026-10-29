"""Authenticated PIAB1D visualization action."""

from ksdft2effmass.visualizations import (
    BaseVisualizer,
    PngFigureRenderer,
    PngVisualization,
)

from ..analysis.verification.values import Piab1dVerification
from .data import Piab1dVisualizationData
from .figures.algebra import (
    _FiniteAlgebraicDiagnosticsFigure,
    _KineticPotentialDecompositionFigure,
)
from .figures.convergence import (
    _ConvergenceModeSweepFigure,
    _ConvergenceSeriesFigure,
    _HigherEigenpairSweepFigure,
    _HigherModeConvergenceFigure,
    _RetainedDimensionSelectionFigure,
)
from .figures.residuals import (
    _EigensolverResidualNormsFigure,
    _OperatorResidualNormsFigure,
    _ResidualMatricesFigure,
)
from .figures.spectra import (
    _ContinuumWavefunctionLadderFigure,
    _DiscreteWavefunctionLadderFigure,
    _Piab1dSpectrumAndStatesFigure,
)
from .inventory import Piab1dVisualizationPlotEnum


class Piab1dVisualizer(
    BaseVisualizer[
        Piab1dVisualizationData,
        Piab1dVerification,
        Piab1dVisualizationPlotEnum,
    ]
):
    """Render the closed authenticated PIAB1D figure inventory."""

    __slots__ = ("_renderers",)

    def __init__(
        self,
        *,
        data: Piab1dVisualizationData,
        verification: Piab1dVerification,
        summary_dpi: int = 200,
        ladder_dpi: int = 220,
        selection_dpi: int = 180,
    ) -> None:
        if not isinstance(data, Piab1dVisualizationData):
            raise TypeError("data must be Piab1dVisualizationData")
        if not isinstance(verification, Piab1dVerification):
            raise TypeError("verification must be Piab1dVerification")
        super().__init__(
            data=data,
            verification=verification,
            plots=tuple(Piab1dVisualizationPlotEnum),
        )
        figure_specs = (
            (
                Piab1dVisualizationPlotEnum.spectrum_and_states,
                _Piab1dSpectrumAndStatesFigure(data),
                summary_dpi,
            ),
            (
                Piab1dVisualizationPlotEnum.residual_matrices,
                _ResidualMatricesFigure(data),
                summary_dpi,
            ),
            (
                Piab1dVisualizationPlotEnum.continuum_wavefunction_ladder,
                _ContinuumWavefunctionLadderFigure(data),
                ladder_dpi,
            ),
            (
                Piab1dVisualizationPlotEnum.discrete_wavefunction_ladder,
                _DiscreteWavefunctionLadderFigure(data),
                ladder_dpi,
            ),
            (
                Piab1dVisualizationPlotEnum.retained_dimension_selection,
                _RetainedDimensionSelectionFigure(data),
                selection_dpi,
            ),
            (
                Piab1dVisualizationPlotEnum.convergence_series,
                _ConvergenceSeriesFigure(data),
                selection_dpi,
            ),
            (
                Piab1dVisualizationPlotEnum.convergence_mode_sweep,
                _ConvergenceModeSweepFigure(data),
                selection_dpi,
            ),
            (
                Piab1dVisualizationPlotEnum.higher_eigenpair_sweep,
                _HigherEigenpairSweepFigure(data),
                selection_dpi,
            ),
            (
                Piab1dVisualizationPlotEnum.higher_mode_convergence,
                _HigherModeConvergenceFigure(data),
                selection_dpi,
            ),
            (
                Piab1dVisualizationPlotEnum.operator_residual_norms,
                _OperatorResidualNormsFigure(data),
                selection_dpi,
            ),
            (
                Piab1dVisualizationPlotEnum.eigensolver_residual_norms,
                _EigensolverResidualNormsFigure(data),
                selection_dpi,
            ),
            (
                Piab1dVisualizationPlotEnum.finite_algebraic_diagnostics,
                _FiniteAlgebraicDiagnosticsFigure(data),
                selection_dpi,
            ),
            (
                Piab1dVisualizationPlotEnum.kinetic_potential_decomposition,
                _KineticPotentialDecompositionFigure(data),
                selection_dpi,
            ),
        )
        self._renderers = frozenset(
            PngFigureRenderer(plot=plot, figure=figure, dpi=dpi)
            for plot, figure, dpi in figure_specs
        )
        if {renderer.plot for renderer in self._renderers} != set(self.plots):
            raise RuntimeError("PIAB1D renderers must cover the closed plot inventory")

    def _render(
        self,
    ) -> frozenset[PngVisualization[Piab1dVisualizationPlotEnum]]:
        return frozenset(renderer.visualize() for renderer in self._renderers)
