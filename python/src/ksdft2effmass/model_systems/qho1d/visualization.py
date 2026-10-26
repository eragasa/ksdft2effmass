"""Authenticated visualization of direct QHO1D results."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from typing import Self

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ksdft2effmass.model_systems.visualization import (
    BaseModelAnalysisFigure,
    BaseModelAnalysisPlot,
    BaseModelAnalysisSubplot,
    BaseModelAnalysisVisualizationData,
    BaseModelAnalysisVisualizer,
    ModelAnalysisPngFigureRenderer,
    ModelAnalysisPngVisualization,
)
from ksdft2effmass.serialization import SerializableValue

from .configuration import Qho1dConfiguration
from .result import Qho1dCaseResult, Qho1dStateComparisonResult
from .verification_values import Qho1dVerification


class Qho1dVisualizationPlotEnum(Enum):
    """Enumerate the closed direct QHO1D figure inventory."""

    eigenstates = "qho1d-eigenstates.png"
    eigenstate_distortion = "qho1d-eigenstate-distortion.png"
    diagnostics = "qho1d-diagnostics.png"


@dataclass(frozen=True, slots=True, eq=False)
class Qho1dVisualizationData(BaseModelAnalysisVisualizationData):
    """Retain the verifier-derived QHO1D rendering projection.

    Parameters
    ----------
    configuration
        Exact sweep and selected-state configuration.
    cases
        Ordered typed cases supplying diagnostic curves.
    selected_state_comparison
        State-resolved selected-case values.

    Raises
    ------
    TypeError
        A field has the wrong domain type.
    ValueError
        Cases do not equal the configured sweep or selected values disagree.
    """

    configuration: Qho1dConfiguration
    cases: tuple[Qho1dCaseResult, ...]
    selected_state_comparison: Qho1dStateComparisonResult

    def __post_init__(self) -> None:
        if not isinstance(self.configuration, Qho1dConfiguration):
            raise TypeError("configuration must be Qho1dConfiguration")
        if not isinstance(self.cases, tuple) or any(
            not isinstance(case, Qho1dCaseResult) for case in self.cases
        ):
            raise TypeError("cases must be a tuple of Qho1dCaseResult")
        expected = tuple(
            (box, spacing, retained)
            for box in self.configuration.box_half_widths
            for spacing in self.configuration.grid_spacings
            for retained in self.configuration.retained_dimensions
        )
        if tuple(case.key for case in self.cases) != expected:
            raise ValueError("visualization cases differ from the configured sweep")
        if not isinstance(self.selected_state_comparison, Qho1dStateComparisonResult):
            raise TypeError(
                "selected_state_comparison must be Qho1dStateComparisonResult"
            )
        selected = self.selected_state_comparison
        if (
            selected.box_half_width.magnitude
            != self.configuration.selected_box_half_width
            or selected.retained_dimension
            != self.configuration.selected_retained_dimension
            or selected.displayed_states != self.configuration.displayed_states
        ):
            raise ValueError("selected visualization data differs from configuration")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "configuration": self.configuration,
            "cases": self.cases,
            "selected_state_comparison": self.selected_state_comparison,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "configuration",
            "cases",
            "selected_state_comparison",
        }:
            raise ValueError("QHO1D visualization fields do not match")
        configuration_value = values["configuration"]
        cases_value = values["cases"]
        selected_value = values["selected_state_comparison"]
        if not isinstance(configuration_value, Mapping):
            raise TypeError("configuration must decode to a mapping")
        if not isinstance(cases_value, tuple) or any(
            not isinstance(case, Mapping) for case in cases_value
        ):
            raise TypeError("cases must decode to a tuple of mappings")
        if not isinstance(selected_value, Mapping):
            raise TypeError("selected_state_comparison must decode to a mapping")
        return cls(
            configuration=Qho1dConfiguration.from_dict(configuration_value),
            cases=tuple(Qho1dCaseResult.from_dict(case) for case in cases_value),
            selected_state_comparison=Qho1dStateComparisonResult.from_dict(
                selected_value
            ),
        )


class _Qho1dEigenstatePlot(BaseModelAnalysisPlot):
    """Draw exact, finite-grid, and boundary values for one selected state."""

    __slots__ = ("_state", "_index")

    def __init__(self, state: Qho1dStateComparisonResult, index: int) -> None:
        self._state = state
        self._index = index

    def draw(self, axis: Axes) -> None:
        state = self._state
        index = self._index
        coordinates = state.coordinates.magnitude
        axis.plot(
            coordinates,
            state.analytical_wavefunctions.magnitude[:, index],
            label="real-line Hermite",
            linewidth=2,
        )
        axis.plot(
            coordinates,
            state.finite_wavefunctions.magnitude[:, index],
            "--",
            label="finite Dirichlet grid",
            linewidth=1.5,
        )
        axis.scatter(
            (-state.box_half_width.magnitude, state.box_half_width.magnitude),
            (0.0, 0.0),
            color="black",
            marker="x",
            label="Dirichlet boundary" if index == 0 else None,
        )


class _Qho1dEigenstateSubplot(BaseModelAnalysisSubplot):
    """Compose one state plot with state-specific axis presentation."""

    __slots__ = ("_index", "_plot")

    def __init__(self, state: Qho1dStateComparisonResult, index: int) -> None:
        self._index = index
        self._plot = _Qho1dEigenstatePlot(state, index)

    def draw(self, axis: Axes) -> None:
        self._plot.draw(axis)
        axis.set_title(f"state n={self._index}")
        axis.set_ylabel("wavefunction")
        axis.grid(alpha=0.25)


class _Qho1dStateDistortionPlot(BaseModelAnalysisPlot):
    """Draw pointwise finite-minus-analytical state differences."""

    __slots__ = ("_state",)

    def __init__(self, state: Qho1dStateComparisonResult) -> None:
        self._state = state

    def draw(self, axis: Axes) -> None:
        state = self._state
        for index in range(state.displayed_states):
            axis.plot(
                state.coordinates.magnitude,
                state.finite_wavefunctions.magnitude[:, index]
                - state.analytical_wavefunctions.magnitude[:, index],
                label=f"n={index}",
            )


class _Qho1dStateDistortionSubplot(BaseModelAnalysisSubplot):
    """Compose pointwise state differences and local presentation."""

    __slots__ = ("_plot",)

    def __init__(self, state: Qho1dStateComparisonResult) -> None:
        self._plot = _Qho1dStateDistortionPlot(state)

    def draw(self, axis: Axes) -> None:
        self._plot.draw(axis)
        axis.axhline(0.0, color="black", linewidth=0.8)
        axis.set_ylabel("grid state minus Hermite state")
        axis.set_xlabel(r"dimensionless coordinate $x/\ell$")
        axis.set_title("Pointwise eigenstate distortion on interior coordinates")
        axis.legend(ncol=4)
        axis.grid(alpha=0.25)


class _Qho1dEnergyDistortionPlot(BaseModelAnalysisPlot):
    """Draw finite-minus-analytical retained-state energy differences."""

    __slots__ = ("_state",)

    def __init__(self, state: Qho1dStateComparisonResult) -> None:
        self._state = state

    def draw(self, axis: Axes) -> None:
        state = self._state
        axis.bar(
            np.arange(state.retained_dimension),
            state.finite_energies.magnitude - state.analytical_energies.magnitude,
        )


class _Qho1dEnergyDistortionSubplot(BaseModelAnalysisSubplot):
    """Compose retained-state energy differences and local presentation."""

    __slots__ = ("_plot",)

    def __init__(self, state: Qho1dStateComparisonResult) -> None:
        self._plot = _Qho1dEnergyDistortionPlot(state)

    def draw(self, axis: Axes) -> None:
        self._plot.draw(axis)
        axis.axhline(0.0, color="black", linewidth=0.8)
        axis.set_xlabel("state index n")
        axis.set_ylabel(r"$E_{n,h,X}-E_n$")
        axis.set_title("Finite-grid eigenvalue distortion")
        axis.grid(axis="y", alpha=0.25)


class _Qho1dSpatialRefinementPlot(BaseModelAnalysisPlot):
    """Draw relative discrepancies across selected-box grid refinements."""

    __slots__ = ("_data",)

    def __init__(self, data: Qho1dVisualizationData) -> None:
        self._data = data

    def draw(self, axis: Axes) -> None:
        configuration = self._data.configuration
        for retained in configuration.retained_dimensions:
            selected = tuple(
                case
                for case in self._data.cases
                if case.box_half_width.magnitude
                == configuration.selected_box_half_width
                and case.retained_dimension == retained
            )
            axis.loglog(
                [case.grid_spacing.magnitude for case in selected],
                [case.relative_discrepancy.magnitude for case in selected],
                marker="o",
                label=f"K={retained}",
            )


class _Qho1dSpatialRefinementSubplot(BaseModelAnalysisSubplot):
    """Compose spatial-refinement marks and local presentation."""

    __slots__ = ("_configuration", "_plot")

    def __init__(self, data: Qho1dVisualizationData) -> None:
        self._configuration = data.configuration
        self._plot = _Qho1dSpatialRefinementPlot(data)

    def draw(self, axis: Axes) -> None:
        self._plot.draw(axis)
        axis.invert_xaxis()
        axis.set_xlabel("grid spacing h")
        axis.set_ylabel("relative Frobenius discrepancy")
        axis.set_title(
            f"Spatial refinement at b={self._configuration.selected_box_half_width:g}"
        )
        axis.legend()
        axis.grid(alpha=0.25)


class _Qho1dGramDefectPlot(BaseModelAnalysisPlot):
    """Draw sampled-state Gram defects across finite-domain widths."""

    __slots__ = ("_data",)

    def __init__(self, data: Qho1dVisualizationData) -> None:
        self._data = data

    def draw(self, axis: Axes) -> None:
        configuration = self._data.configuration
        for retained in configuration.retained_dimensions:
            selected = tuple(
                case
                for case in self._data.cases
                if case.requested_grid_spacing.magnitude
                == configuration.selected_grid_spacing
                and case.retained_dimension == retained
            )
            axis.semilogy(
                [case.box_half_width.magnitude for case in selected],
                [case.gram_deviation.magnitude for case in selected],
                marker="o",
                label=f"K={retained}",
            )


class _Qho1dGramDefectSubplot(BaseModelAnalysisSubplot):
    """Compose sampled-state Gram-defect marks and local presentation."""

    __slots__ = ("_configuration", "_plot")

    def __init__(self, data: Qho1dVisualizationData) -> None:
        self._configuration = data.configuration
        self._plot = _Qho1dGramDefectPlot(data)

    def draw(self, axis: Axes) -> None:
        self._plot.draw(axis)
        axis.set_xlabel("box half-width b")
        axis.set_ylabel(r"$\|G-I\|_F$")
        spacing = self._configuration.selected_grid_spacing
        axis.set_title(f"Sampled Gram defect at requested h={spacing:g}")
        axis.legend()
        axis.grid(alpha=0.25)


class _Qho1dDiscrepancyComponentsPlot(BaseModelAnalysisPlot):
    """Draw diagonal and off-diagonal discrepancy components."""

    __slots__ = ("_data",)

    def __init__(self, data: Qho1dVisualizationData) -> None:
        self._data = data

    def draw(self, axis: Axes) -> None:
        configuration = self._data.configuration
        selected = tuple(
            case
            for case in self._data.cases
            if case.requested_grid_spacing.magnitude
            == configuration.selected_grid_spacing
            and case.box_half_width.magnitude == configuration.selected_box_half_width
        )
        retained_dimensions = np.asarray(
            [case.retained_dimension for case in selected], dtype=np.float64
        )
        width = 0.32
        axis.bar(
            retained_dimensions - width / 2.0,
            [case.diagonal_discrepancy.magnitude for case in selected],
            width=width,
            label="diagonal",
        )
        axis.bar(
            retained_dimensions + width / 2.0,
            [case.off_diagonal_discrepancy.magnitude for case in selected],
            width=width,
            label="off-diagonal",
        )


class _Qho1dDiscrepancyComponentsSubplot(BaseModelAnalysisSubplot):
    """Compose discrepancy-component marks and local presentation."""

    __slots__ = ("_plot", "_retained_dimensions")

    def __init__(self, data: Qho1dVisualizationData) -> None:
        self._plot = _Qho1dDiscrepancyComponentsPlot(data)
        configuration = data.configuration
        self._retained_dimensions = np.asarray(
            [
                case.retained_dimension
                for case in data.cases
                if case.requested_grid_spacing.magnitude
                == configuration.selected_grid_spacing
                and case.box_half_width.magnitude
                == configuration.selected_box_half_width
            ],
            dtype=np.float64,
        )

    def draw(self, axis: Axes) -> None:
        self._plot.draw(axis)
        axis.set_xticks(self._retained_dimensions)
        axis.set_xlabel("retained dimension K")
        axis.set_ylabel("Frobenius component")
        axis.set_title("Reusable discrepancy decomposition")
        axis.legend()
        axis.grid(axis="y", alpha=0.25)


class _Qho1dResidualDiagnosticPlot(BaseModelAnalysisPlot):
    """Draw full-space residuals against pulled-back discrepancies."""

    __slots__ = ("_cases",)

    def __init__(self, cases: tuple[Qho1dCaseResult, ...]) -> None:
        self._cases = cases

    def draw(self, axis: Axes) -> None:
        residuals = np.asarray(
            [case.residual_frobenius.magnitude for case in self._cases],
            dtype=np.float64,
        )
        discrepancies = np.asarray(
            [case.absolute_discrepancy.magnitude for case in self._cases],
            dtype=np.float64,
        )
        axis.loglog(residuals, discrepancies, "o", alpha=0.75)
        lower = float(min(np.min(residuals), np.min(discrepancies)))
        upper = float(max(np.max(residuals), np.max(discrepancies)))
        axis.loglog((lower, upper), (lower, upper), "--", label="equality")


class _Qho1dResidualDiagnosticSubplot(BaseModelAnalysisSubplot):
    """Compose residual-diagnostic marks and local presentation."""

    __slots__ = ("_plot",)

    def __init__(self, cases: tuple[Qho1dCaseResult, ...]) -> None:
        self._plot = _Qho1dResidualDiagnosticPlot(cases)

    def draw(self, axis: Axes) -> None:
        self._plot.draw(axis)
        axis.set_xlabel(r"$\|H_{X,h}J-JH_K\|_F$")
        axis.set_ylabel(r"$\|J^T H_{X,h}J-H_K\|_F$")
        axis.set_title("A-posteriori residual diagnostic")
        axis.legend()
        axis.grid(alpha=0.25)


class _Qho1dFigure(BaseModelAnalysisFigure):
    __slots__ = ("data",)

    def __init__(self, data: Qho1dVisualizationData) -> None:
        self.data = data


class _Qho1dEigenstateFigure(_Qho1dFigure):
    def draw(self) -> Figure:
        state = self.data.selected_state_comparison
        figure, axes = plt.subplots(2, 2, figsize=(10.0, 7.0), sharex=True)
        flat_axes = axes.ravel()
        for index in range(state.displayed_states):
            _Qho1dEigenstateSubplot(state, index).draw(flat_axes[index])
        for axis in flat_axes[-2:]:
            axis.set_xlabel(r"dimensionless coordinate $x/\ell$")
        handles, labels = flat_axes[0].get_legend_handles_labels()
        figure.suptitle(
            "QHO1D exact and finite-grid eigenstates "
            f"(b={state.box_half_width.magnitude:g}, "
            f"h={state.grid_spacing.magnitude:g})",
            y=0.995,
        )
        figure.legend(
            handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.955), ncol=3
        )
        figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.89))
        return figure


class _Qho1dEigenstateDistortionFigure(_Qho1dFigure):
    def draw(self) -> Figure:
        state = self.data.selected_state_comparison
        figure, axes = plt.subplots(2, 1, figsize=(9.0, 8.0))
        state_axis, energy_axis = axes
        _Qho1dStateDistortionSubplot(state).draw(state_axis)
        _Qho1dEnergyDistortionSubplot(state).draw(energy_axis)
        figure.tight_layout()
        return figure


class _Qho1dDiagnosticFigure(_Qho1dFigure):
    def draw(self) -> Figure:
        figure, axes = plt.subplots(2, 2, figsize=(11.0, 8.5))
        convergence_axis, gram_axis, components_axis, residual_axis = axes.ravel()
        _Qho1dSpatialRefinementSubplot(self.data).draw(convergence_axis)
        _Qho1dGramDefectSubplot(self.data).draw(gram_axis)
        _Qho1dDiscrepancyComponentsSubplot(self.data).draw(components_axis)
        _Qho1dResidualDiagnosticSubplot(self.data.cases).draw(residual_axis)
        figure.tight_layout()
        return figure


class Qho1dVisualizer(BaseModelAnalysisVisualizer):
    """Render the closed QHO1D figure inventory from authenticated data.

    Parameters
    ----------
    data
        Verifier-derived immutable visualization projection.
    verification
        Passing aggregate bound to the exact projection digest.

    Raises
    ------
    TypeError
        Either argument has the wrong domain type.
    ValueError
        Verification failed or authenticates different projection bytes.
    """

    __slots__ = ("data", "verification")

    plots = tuple(Qho1dVisualizationPlotEnum)

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
        self._authenticate(data, verification)
        self.data = data
        self.verification = verification

    def visualize(
        self,
    ) -> frozenset[ModelAnalysisPngVisualization[Qho1dVisualizationPlotEnum]]:
        """Render every declared QHO1D plot exactly once.

        Returns
        -------
        frozenset[ModelAnalysisPngVisualization[Qho1dVisualizationPlotEnum]]
            Three validated PNG values indexed by the closed plot enum.

        Raises
        ------
        RuntimeError
            Concrete renderer ownership differs from the declared enum inventory.
        """
        renderers = (
            ModelAnalysisPngFigureRenderer(
                plot=Qho1dVisualizationPlotEnum.eigenstates,
                figure=_Qho1dEigenstateFigure(self.data),
                dpi=180,
            ),
            ModelAnalysisPngFigureRenderer(
                plot=Qho1dVisualizationPlotEnum.eigenstate_distortion,
                figure=_Qho1dEigenstateDistortionFigure(self.data),
                dpi=180,
            ),
            ModelAnalysisPngFigureRenderer(
                plot=Qho1dVisualizationPlotEnum.diagnostics,
                figure=_Qho1dDiagnosticFigure(self.data),
                dpi=180,
            ),
        )
        visualizations = frozenset(renderer.visualize() for renderer in renderers)
        self._require_complete_inventory(
            visualizations,
            frozenset(self.plots),
        )
        return visualizations
