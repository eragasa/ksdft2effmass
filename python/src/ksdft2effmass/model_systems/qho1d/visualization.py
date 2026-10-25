"""Authenticated visualization of direct QHO1D results."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from io import BytesIO
from typing import Self

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from ksdft2effmass.model_systems.visualization import (
    BaseModelAnalysisVisualizationData,
    BaseModelAnalysisVisualizationPlotter,
    BaseModelAnalysisVisualizer,
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


class _Qho1dPlotter(BaseModelAnalysisVisualizationPlotter):
    __slots__ = ("data",)

    plot: Qho1dVisualizationPlotEnum

    def __init__(self, data: Qho1dVisualizationData) -> None:
        self.data = data

    def _value(
        self, figure: Figure
    ) -> ModelAnalysisPngVisualization[Qho1dVisualizationPlotEnum]:
        output = BytesIO()
        figure.savefig(output, format="png", dpi=180)
        plt.close(figure)
        return ModelAnalysisPngVisualization(plot=self.plot, png=output.getvalue())


class _Qho1dEigenstatePlotter(_Qho1dPlotter):
    plot = Qho1dVisualizationPlotEnum.eigenstates

    def visualize(self) -> ModelAnalysisPngVisualization[Qho1dVisualizationPlotEnum]:
        state = self.data.selected_state_comparison
        figure, axes = plt.subplots(2, 2, figsize=(10.0, 7.0), sharex=True)
        flat_axes = axes.ravel()
        coordinates = state.coordinates.magnitude
        for index in range(state.displayed_states):
            axis = flat_axes[index]
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
            axis.set_title(f"state n={index}")
            axis.set_ylabel("wavefunction")
            axis.grid(alpha=0.25)
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
        return self._value(figure)


class _Qho1dEigenstateDistortionPlotter(_Qho1dPlotter):
    plot = Qho1dVisualizationPlotEnum.eigenstate_distortion

    def visualize(self) -> ModelAnalysisPngVisualization[Qho1dVisualizationPlotEnum]:
        state = self.data.selected_state_comparison
        figure, axes = plt.subplots(2, 1, figsize=(9.0, 8.0))
        state_axis, energy_axis = axes
        for index in range(state.displayed_states):
            state_axis.plot(
                state.coordinates.magnitude,
                state.finite_wavefunctions.magnitude[:, index]
                - state.analytical_wavefunctions.magnitude[:, index],
                label=f"n={index}",
            )
        state_axis.axhline(0.0, color="black", linewidth=0.8)
        state_axis.set_ylabel("grid state minus Hermite state")
        state_axis.set_xlabel(r"dimensionless coordinate $x/\ell$")
        state_axis.set_title("Pointwise eigenstate distortion on interior coordinates")
        state_axis.legend(ncol=4)
        state_axis.grid(alpha=0.25)
        states = np.arange(state.retained_dimension)
        energy_axis.bar(
            states,
            state.finite_energies.magnitude - state.analytical_energies.magnitude,
        )
        energy_axis.axhline(0.0, color="black", linewidth=0.8)
        energy_axis.set_xlabel("state index n")
        energy_axis.set_ylabel(r"$E_{n,h,X}-E_n$")
        energy_axis.set_title("Finite-grid eigenvalue distortion")
        energy_axis.grid(axis="y", alpha=0.25)
        figure.tight_layout()
        return self._value(figure)


class _Qho1dDiagnosticPlotter(_Qho1dPlotter):
    plot = Qho1dVisualizationPlotEnum.diagnostics

    def visualize(self) -> ModelAnalysisPngVisualization[Qho1dVisualizationPlotEnum]:
        configuration = self.data.configuration
        cases = self.data.cases
        figure, axes = plt.subplots(2, 2, figsize=(11.0, 8.5))
        convergence_axis, gram_axis, components_axis, residual_axis = axes.ravel()
        for retained in configuration.retained_dimensions:
            selected = tuple(
                case
                for case in cases
                if case.box_half_width.magnitude
                == configuration.selected_box_half_width
                and case.retained_dimension == retained
            )
            convergence_axis.loglog(
                [case.grid_spacing.magnitude for case in selected],
                [case.relative_discrepancy.magnitude for case in selected],
                marker="o",
                label=f"K={retained}",
            )
        convergence_axis.invert_xaxis()
        convergence_axis.set_xlabel("grid spacing h")
        convergence_axis.set_ylabel("relative Frobenius discrepancy")
        convergence_axis.set_title(
            f"Spatial refinement at b={configuration.selected_box_half_width:g}"
        )
        convergence_axis.legend()
        convergence_axis.grid(alpha=0.25)
        for retained in configuration.retained_dimensions:
            selected = tuple(
                case
                for case in cases
                if case.requested_grid_spacing.magnitude
                == configuration.selected_grid_spacing
                and case.retained_dimension == retained
            )
            gram_axis.semilogy(
                [case.box_half_width.magnitude for case in selected],
                [case.gram_deviation.magnitude for case in selected],
                marker="o",
                label=f"K={retained}",
            )
        gram_axis.set_xlabel("box half-width b")
        gram_axis.set_ylabel(r"$\|G-I\|_F$")
        selected_spacing = configuration.selected_grid_spacing
        gram_axis.set_title(f"Sampled Gram defect at requested h={selected_spacing:g}")
        gram_axis.legend()
        gram_axis.grid(alpha=0.25)
        selected_components = tuple(
            case
            for case in cases
            if case.requested_grid_spacing.magnitude
            == configuration.selected_grid_spacing
            and case.box_half_width.magnitude == configuration.selected_box_half_width
        )
        retained_dimensions = np.asarray(
            [case.retained_dimension for case in selected_components], dtype=np.float64
        )
        width = 0.32
        components_axis.bar(
            retained_dimensions - width / 2.0,
            [case.diagonal_discrepancy.magnitude for case in selected_components],
            width=width,
            label="diagonal",
        )
        components_axis.bar(
            retained_dimensions + width / 2.0,
            [case.off_diagonal_discrepancy.magnitude for case in selected_components],
            width=width,
            label="off-diagonal",
        )
        components_axis.set_xticks(retained_dimensions)
        components_axis.set_xlabel("retained dimension K")
        components_axis.set_ylabel("Frobenius component")
        components_axis.set_title("Reusable discrepancy decomposition")
        components_axis.legend()
        components_axis.grid(axis="y", alpha=0.25)
        residuals = np.asarray(
            [case.residual_frobenius.magnitude for case in cases], dtype=np.float64
        )
        discrepancies = np.asarray(
            [case.absolute_discrepancy.magnitude for case in cases], dtype=np.float64
        )
        residual_axis.loglog(residuals, discrepancies, "o", alpha=0.75)
        lower = float(min(np.min(residuals), np.min(discrepancies)))
        upper = float(max(np.max(residuals), np.max(discrepancies)))
        residual_axis.loglog((lower, upper), (lower, upper), "--", label="equality")
        residual_axis.set_xlabel(r"$\|H_{X,h}J-JH_K\|_F$")
        residual_axis.set_ylabel(r"$\|J^T H_{X,h}J-H_K\|_F$")
        residual_axis.set_title("A-posteriori residual diagnostic")
        residual_axis.legend()
        residual_axis.grid(alpha=0.25)
        figure.tight_layout()
        return self._value(figure)


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
        if not verification.passed:
            raise ValueError("visualization requires passing QHO1D verification")
        digest = hashlib.sha256(data.to_json()).hexdigest()
        if verification.visualization_data_sha256 != digest:
            raise ValueError("verification authenticates different visualization data")
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
            Concrete plotter ownership differs from the declared enum inventory.
        """
        visualizations = frozenset(
            (
                _Qho1dEigenstatePlotter(self.data).visualize(),
                _Qho1dEigenstateDistortionPlotter(self.data).visualize(),
                _Qho1dDiagnosticPlotter(self.data).visualize(),
            )
        )
        if {visualization.plot for visualization in visualizations} != set(self.plots):
            raise RuntimeError("QHO1D plotter inventory differs from declared plots")
        return visualizations
