"""QHO1D scientific figure composition."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ksdft2effmass.visualizations import BaseFigure, BasePlot, BaseSubplot

from ..result import Qho1dCaseResult, Qho1dStateComparisonResult
from .data import Qho1dVisualizationData


class _Qho1dEigenstatePlot(BasePlot):
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


class _Qho1dEigenstateSubplot(BaseSubplot):
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


class _Qho1dStateDistortionPlot(BasePlot):
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


class _Qho1dStateDistortionSubplot(BaseSubplot):
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


class _Qho1dEnergyDistortionPlot(BasePlot):
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


class _Qho1dEnergyDistortionSubplot(BaseSubplot):
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


class _Qho1dSpatialRefinementPlot(BasePlot):
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


class _Qho1dSpatialRefinementSubplot(BaseSubplot):
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


class _Qho1dGramDefectPlot(BasePlot):
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


class _Qho1dGramDefectSubplot(BaseSubplot):
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


class _Qho1dDiscrepancyComponentsPlot(BasePlot):
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


class _Qho1dDiscrepancyComponentsSubplot(BaseSubplot):
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


class _Qho1dResidualDiagnosticPlot(BasePlot):
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


class _Qho1dResidualDiagnosticSubplot(BaseSubplot):
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


class _Qho1dFigure(BaseFigure):
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
