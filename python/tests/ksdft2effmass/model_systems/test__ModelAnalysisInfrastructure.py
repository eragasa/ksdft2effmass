"""Software verification of shared model-analysis lifecycle infrastructure."""

from __future__ import annotations

from enum import Enum

import matplotlib.pyplot as plt
import pytest
from matplotlib.axes import Axes
from matplotlib.figure import Figure

import ksdft2effmass.model_systems as model_systems
from ksdft2effmass.model_systems import (
    BaseModelAnalysisFigure,
    BaseModelAnalysisPlot,
    BaseModelAnalysisSubplot,
    BaseModelAnalysisVerification,
    BaseModelAnalysisVerifier,
    ModelAnalysisPngFigureRenderer,
)
from ksdft2effmass.model_systems.piab1d import (
    Piab1dAnalyzer,
    Piab1dCalculationResult,
    Piab1dVerification,
    Piab1dVerifier,
)
from ksdft2effmass.model_systems.qho1d import (
    Qho1dAnalyzer,
    Qho1dCalculationResult,
    Qho1dVerification,
    Qho1dVerifier,
)


class _Plot(Enum):
    line = "line.png"


class _LinePlot(BaseModelAnalysisPlot):
    def draw(self, axis: Axes) -> None:
        axis.plot((0.0, 1.0), (0.0, 1.0), label="line")


class _LineSubplot(BaseModelAnalysisSubplot):
    def __init__(self, plot: BaseModelAnalysisPlot) -> None:
        self._plot = plot

    def draw(self, axis: Axes) -> None:
        self._plot.draw(axis)
        axis.set_xlabel("x")
        axis.set_ylabel("y")
        axis.legend()


class _LineFigure(BaseModelAnalysisFigure):
    def __init__(self, subplot: BaseModelAnalysisSubplot) -> None:
        self._subplot = subplot

    def draw(self) -> Figure:
        figure, axis = plt.subplots(figsize=(3.0, 2.0))
        self._subplot.draw(axis)
        figure.tight_layout()
        return figure


class TestModelAnalysisInfrastructure:
    """Verify shared boundaries without imposing model-specific science."""

    def test_analyzers__nominal_common_base__is_absent(self) -> None:
        """Model analyzers remain concrete when they share no executed behavior."""
        assert not hasattr(model_systems, "BaseModelSystemAnalyzer")
        assert Piab1dAnalyzer.__bases__ == (object,)
        assert Qho1dAnalyzer.__bases__ == (object,)

    def test_verification__aggregate_behavior__is_owned_once(self) -> None:
        """Concrete aggregates inherit common reporting and authentication behavior."""
        for verification_type in (Piab1dVerification, Qho1dVerification):
            assert verification_type.passed is BaseModelAnalysisVerification.passed
            assert verification_type.checks is BaseModelAnalysisVerification.checks
            assert (
                verification_type.check_tolerances
                is BaseModelAnalysisVerification.check_tolerances
            )
            assert (
                verification_type.authenticated_visualization_data_sha256
                is BaseModelAnalysisVerification.authenticated_visualization_data_sha256
            )

    def test_verifier__subject_boundary__is_owned_once(self) -> None:
        """Both concrete verifiers inherit the final shared subject constructor."""
        assert Piab1dVerifier.__init__ is BaseModelAnalysisVerifier.__init__
        assert Qho1dVerifier.__init__ is BaseModelAnalysisVerifier.__init__
        assert Piab1dVerifier.admit_stored is BaseModelAnalysisVerifier.admit_stored
        assert Qho1dVerifier.admit_stored is BaseModelAnalysisVerifier.admit_stored
        assert Piab1dVerifier._result_type() is Piab1dCalculationResult
        assert Qho1dVerifier._result_type() is Qho1dCalculationResult
        for verifier_type in (Piab1dVerifier, Qho1dVerifier):
            with pytest.raises(TypeError, match="result_wire must be built-in bytes"):
                verifier_type(result_wire=bytearray())  # type: ignore[arg-type]

    def test_renderer__plot_subplot_and_figure__remain_independently_composable(
        self,
    ) -> None:
        """Common PNG encoding accepts an independently composed figure action."""
        renderer = ModelAnalysisPngFigureRenderer(
            plot=_Plot.line,
            figure=_LineFigure(_LineSubplot(_LinePlot())),
            dpi=100,
        )
        open_figures = tuple(plt.get_fignums())

        visualization = renderer.visualize()

        assert tuple(plt.get_fignums()) == open_figures
        assert visualization.plot is _Plot.line
        assert visualization.filename == "line.png"
        assert visualization.png.startswith(b"\x89PNG\r\n\x1a\n")

    def test_renderer__dpi__rejects_boolean_and_nonpositive_values(self) -> None:
        """The shared encoder requires a positive built-in integer resolution."""
        figure = _LineFigure(_LineSubplot(_LinePlot()))
        with pytest.raises(TypeError, match="dpi must be a built-in int"):
            ModelAnalysisPngFigureRenderer(
                plot=_Plot.line,
                figure=figure,
                dpi=True,
            )
        with pytest.raises(ValueError, match="dpi must be positive"):
            ModelAnalysisPngFigureRenderer(
                plot=_Plot.line,
                figure=figure,
                dpi=0,
            )
