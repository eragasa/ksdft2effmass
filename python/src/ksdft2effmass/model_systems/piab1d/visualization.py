"""Verified visualization of successor PIAB1D analysis results."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from typing import Self

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.colors import TwoSlopeNorm
from matplotlib.figure import Figure
from projectkoios.physkit.units import (
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.analysis import (
    RelativeErrorConvergenceResult,
    TailProbabilitySelection,
)
from ksdft2effmass.analysis.operators import KineticPotentialDecompositionResult
from ksdft2effmass.model_systems.visualization import (
    BaseModelAnalysisFigure,
    BaseModelAnalysisFigureRenderer,
    BaseModelAnalysisPlot,
    BaseModelAnalysisSubplot,
    BaseModelAnalysisVisualizationData,
    BaseModelAnalysisVisualizer,
    ModelAnalysisPngVisualization,
)
from ksdft2effmass.serialization import SerializableValue

from .analysis.finite_algebraic_diagnostics import Piab1dFiniteAlgebraicDiagnostics
from .analysis.grid_sweep import Piab1dEigenpairSweepResult
from .analysis.residual_norms import Piab1dResidualNormSweepResult
from .analysis.verification.values import Piab1dVerification


class Piab1dVisualizationPlotEnum(Enum):
    """Enumerate the complete maintained PIAB1D plot migration target."""

    spectrum_and_states = "spectrum-and-states.png"
    residual_matrices = "residual-matrices.png"
    continuum_wavefunction_ladder = "figure_01a_continuum_wavefunction_ladder.png"
    discrete_wavefunction_ladder = "figure_01b_discrete_wavefunction_ladder.png"
    retained_dimension_selection = "figure_02_retained_dimension_selection.png"
    convergence_series = "convergence-series.png"
    convergence_mode_sweep = "convergence-mode-sweep.png"
    higher_eigenpair_sweep = "higher-eigenpair-sweep.png"
    higher_mode_convergence = "higher-mode-convergence.png"
    operator_residual_norms = "operator-residual-norms.png"
    eigensolver_residual_norms = "eigensolver-residual-norms.png"
    finite_algebraic_diagnostics = "finite-algebraic-diagnostics.png"
    kinetic_potential_decomposition = "kinetic-potential-decomposition.png"


@dataclass(frozen=True, slots=True, eq=False)
class Piab1dVisualizationData(BaseModelAnalysisVisualizationData):
    """Retain immutable typed PIAB1D data projected by the verifier.

    Parameters
    ----------
    length
        Positive box length quantity.
    retained_dimension
        Positive number of retained low-energy states.
    computed_energies, continuum_energies
        Represented and analytical full-spectrum energy vectors.
    eigenvectors, quadrature_eigenvectors
        Euclidean and quadrature-normalized eigenvector matrices.
    consistent, unmatched, boundary
        Distinct full-space Hamiltonian analysis matrices.
    continuum_coordinates, continuum_wavefunctions
        Analytical sampling grid and retained-mode wavefunctions.
    selection
        Tail-probability retained-dimension selection.
    convergence_interior_points, convergence_modes, convergence
        Low-mode refinement inventory and values.
    eigenpair_sweep
        Full-spectrum dispersion and eigenpair observations.
    residual_norm_sweep
        Canonical grid-indexed operator and residual norms.
    finite_algebraic_diagnostics
        Grid-indexed finite matrix-identity discrepancies.
    kinetic_potential_decomposition
        Retained-space component pairs and model-class fits.

    Raises
    ------
    TypeError
        A field has the wrong domain type or inventory element type.
    ValueError
        Units, shapes, dimensions, grids, modes, or cross-field conventions disagree.

    Notes
    -----
    This record is derived from the authoritative calculation result by the verifier.
    Its canonical JSON digest is stored in ``Piab1dVerification`` before rendering.
    """

    length: ScalarQuantity
    retained_dimension: int
    computed_energies: VectorQuantity
    continuum_energies: VectorQuantity
    eigenvectors: MatrixQuantity
    quadrature_eigenvectors: MatrixQuantity
    consistent: MatrixQuantity
    unmatched: MatrixQuantity
    boundary: MatrixQuantity
    continuum_coordinates: VectorQuantity
    continuum_wavefunctions: MatrixQuantity
    selection: TailProbabilitySelection
    convergence_interior_points: tuple[int, ...]
    convergence_modes: tuple[int, ...]
    convergence: RelativeErrorConvergenceResult
    eigenpair_sweep: Piab1dEigenpairSweepResult
    residual_norm_sweep: Piab1dResidualNormSweepResult
    finite_algebraic_diagnostics: Piab1dFiniteAlgebraicDiagnostics
    kinetic_potential_decomposition: KineticPotentialDecompositionResult

    def __post_init__(self) -> None:
        if not isinstance(self.length, ScalarQuantity):
            raise TypeError("length must be ScalarQuantity")
        if self.length.magnitude <= 0.0:
            raise ValueError("length must be positive")
        if type(self.retained_dimension) is not int or self.retained_dimension <= 0:
            raise TypeError("retained_dimension must be a positive built-in integer")
        for name, value, expected_type in (
            ("computed_energies", self.computed_energies, VectorQuantity),
            ("continuum_energies", self.continuum_energies, VectorQuantity),
            ("eigenvectors", self.eigenvectors, MatrixQuantity),
            (
                "quadrature_eigenvectors",
                self.quadrature_eigenvectors,
                MatrixQuantity,
            ),
            ("consistent", self.consistent, MatrixQuantity),
            ("unmatched", self.unmatched, MatrixQuantity),
            ("boundary", self.boundary, MatrixQuantity),
            ("continuum_coordinates", self.continuum_coordinates, VectorQuantity),
            ("continuum_wavefunctions", self.continuum_wavefunctions, MatrixQuantity),
        ):
            if not isinstance(value, expected_type):
                raise TypeError(f"{name} must be {expected_type.__name__}")
        if self.computed_energies.unit != self.continuum_energies.unit:
            raise ValueError("computed and continuum energy units must agree")
        energy_unit = self.computed_energies.unit
        if any(
            matrix.unit != energy_unit
            for matrix in (self.consistent, self.unmatched, self.boundary)
        ):
            raise ValueError("visualized Hamiltonian matrices must use the energy unit")
        if not isinstance(self.eigenvectors.unit, Unitless):
            raise ValueError("Euclidean eigenvectors must be unitless")
        if self.continuum_coordinates.unit != self.length.unit:
            raise ValueError("continuum coordinates and box length units must agree")
        if self.continuum_wavefunctions.unit != self.quadrature_eigenvectors.unit:
            raise ValueError("analytical and quadrature wavefunction units must agree")
        if not isinstance(self.selection, TailProbabilitySelection):
            raise TypeError("selection must be TailProbabilitySelection")
        if not isinstance(self.convergence, RelativeErrorConvergenceResult):
            raise TypeError("convergence must be RelativeErrorConvergenceResult")
        if not isinstance(self.eigenpair_sweep, Piab1dEigenpairSweepResult):
            raise TypeError("eigenpair_sweep must be Piab1dEigenpairSweepResult")
        if not isinstance(self.residual_norm_sweep, Piab1dResidualNormSweepResult):
            raise TypeError("residual_norm_sweep must be Piab1dResidualNormSweepResult")
        if not isinstance(
            self.finite_algebraic_diagnostics, Piab1dFiniteAlgebraicDiagnostics
        ):
            raise TypeError(
                "finite_algebraic_diagnostics must be Piab1dFiniteAlgebraicDiagnostics"
            )
        if not isinstance(
            self.kinetic_potential_decomposition,
            KineticPotentialDecompositionResult,
        ):
            raise TypeError("kinetic-potential decomposition has the wrong result type")
        if not (
            self.eigenpair_sweep.definition
            == self.residual_norm_sweep.definition
            == self.finite_algebraic_diagnostics.definition
        ):
            raise ValueError("visualization grid-sweep sections must agree")
        for name, values in (
            ("convergence_interior_points", self.convergence_interior_points),
            ("convergence_modes", self.convergence_modes),
        ):
            if not isinstance(values, tuple) or any(
                type(value) is not int or value <= 0 for value in values
            ):
                raise TypeError(f"{name} must contain positive built-in integers")
        points = self.computed_energies.magnitude.size
        retained = self.retained_dimension
        if points <= 0 or retained > points:
            raise ValueError("retained_dimension must not exceed the parent dimension")
        if self.continuum_energies.magnitude.shape != (points,):
            raise ValueError("continuum_energies must match the parent dimension")
        for name, matrix in (
            ("eigenvectors", self.eigenvectors),
            ("quadrature_eigenvectors", self.quadrature_eigenvectors),
            ("consistent", self.consistent),
            ("unmatched", self.unmatched),
            ("boundary", self.boundary),
        ):
            if matrix.magnitude.shape != (points, points):
                raise ValueError(f"{name} must match the parent matrix shape")
        samples = self.continuum_coordinates.magnitude.size
        if self.continuum_wavefunctions.magnitude.shape != (samples, retained):
            raise ValueError(
                "continuum wavefunctions must match samples and retained modes"
            )
        if self.selection.probabilities.magnitude.shape != (points,):
            raise ValueError("selection probabilities must cover the parent dimension")
        levels, modes = self.convergence.relative_errors.magnitude.shape
        if len(self.convergence_interior_points) != levels:
            raise ValueError("convergence points must cover every refinement level")
        if len(self.convergence_modes) != modes:
            raise ValueError("convergence modes must label every error series")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        """Compose reusable scientific values without JSON normalization."""
        return {
            "length": self.length,
            "retained_dimension": self.retained_dimension,
            "computed_energies": self.computed_energies,
            "continuum_energies": self.continuum_energies,
            "eigenvectors": self.eigenvectors,
            "quadrature_eigenvectors": self.quadrature_eigenvectors,
            "consistent": self.consistent,
            "unmatched": self.unmatched,
            "boundary": self.boundary,
            "continuum_coordinates": self.continuum_coordinates,
            "continuum_wavefunctions": self.continuum_wavefunctions,
            "selection": self.selection,
            "convergence_interior_points": self.convergence_interior_points,
            "convergence_modes": self.convergence_modes,
            "convergence": self.convergence,
            "eigenpair_sweep": self.eigenpair_sweep,
            "residual_norm_sweep": self.residual_norm_sweep,
            "finite_algebraic_diagnostics": self.finite_algebraic_diagnostics,
            "kinetic_potential_decomposition": self.kinetic_potential_decomposition,
        }

    @classmethod
    def _from_mapping(
        cls,
        values: Mapping[str, SerializableValue],
    ) -> Self:
        """Recompose reusable values restored by the generic JSON codec."""
        expected = {
            "length",
            "retained_dimension",
            "computed_energies",
            "continuum_energies",
            "eigenvectors",
            "quadrature_eigenvectors",
            "consistent",
            "unmatched",
            "boundary",
            "continuum_coordinates",
            "continuum_wavefunctions",
            "selection",
            "convergence_interior_points",
            "convergence_modes",
            "convergence",
            "eigenpair_sweep",
            "residual_norm_sweep",
            "finite_algebraic_diagnostics",
            "kinetic_potential_decomposition",
        }
        if set(values) != expected:
            raise ValueError("visualization data fields do not match the contract")
        length = values["length"]
        retained_dimension = values["retained_dimension"]
        computed_energies = values["computed_energies"]
        continuum_energies = values["continuum_energies"]
        eigenvectors = values["eigenvectors"]
        quadrature_eigenvectors = values["quadrature_eigenvectors"]
        consistent = values["consistent"]
        unmatched = values["unmatched"]
        boundary = values["boundary"]
        continuum_coordinates = values["continuum_coordinates"]
        continuum_wavefunctions = values["continuum_wavefunctions"]
        selection = values["selection"]
        convergence_points = values["convergence_interior_points"]
        convergence_modes = values["convergence_modes"]
        convergence = values["convergence"]
        eigenpair_sweep = values["eigenpair_sweep"]
        residual_norm_sweep = values["residual_norm_sweep"]
        algebraic_diagnostics = values["finite_algebraic_diagnostics"]
        decomposition = values["kinetic_potential_decomposition"]
        if not isinstance(length, ScalarQuantity):
            raise TypeError("length must decode to ScalarQuantity")
        if type(retained_dimension) is not int:
            raise TypeError("retained_dimension must decode to a built-in integer")
        if not isinstance(computed_energies, VectorQuantity):
            raise TypeError("computed_energies must decode to VectorQuantity")
        if not isinstance(continuum_energies, VectorQuantity):
            raise TypeError("continuum_energies must decode to VectorQuantity")
        if not isinstance(eigenvectors, MatrixQuantity):
            raise TypeError("eigenvectors must decode to MatrixQuantity")
        if not isinstance(quadrature_eigenvectors, MatrixQuantity):
            raise TypeError("quadrature_eigenvectors must decode to MatrixQuantity")
        if not isinstance(consistent, MatrixQuantity):
            raise TypeError("consistent must decode to MatrixQuantity")
        if not isinstance(unmatched, MatrixQuantity):
            raise TypeError("unmatched must decode to MatrixQuantity")
        if not isinstance(boundary, MatrixQuantity):
            raise TypeError("boundary must decode to MatrixQuantity")
        if not isinstance(continuum_coordinates, VectorQuantity):
            raise TypeError("continuum_coordinates must decode to VectorQuantity")
        if not isinstance(continuum_wavefunctions, MatrixQuantity):
            raise TypeError("continuum_wavefunctions must decode to MatrixQuantity")
        if not isinstance(selection, Mapping):
            raise TypeError("selection must decode to a mapping")
        if not isinstance(convergence, Mapping):
            raise TypeError("convergence must decode to a mapping")
        if not isinstance(eigenpair_sweep, Mapping):
            raise TypeError("eigenpair_sweep must decode to a mapping")
        if not isinstance(residual_norm_sweep, Mapping):
            raise TypeError("residual_norm_sweep must decode to a mapping")
        if not isinstance(algebraic_diagnostics, Mapping):
            raise TypeError("finite_algebraic_diagnostics must decode to a mapping")
        if not isinstance(decomposition, Mapping):
            raise TypeError("kinetic_potential_decomposition must decode to a mapping")
        if not isinstance(convergence_points, tuple) or any(
            type(item) is not int for item in convergence_points
        ):
            raise TypeError(
                "convergence_interior_points must decode to an integer tuple"
            )
        if not isinstance(convergence_modes, tuple) or any(
            type(item) is not int for item in convergence_modes
        ):
            raise TypeError("convergence_modes must decode to an integer tuple")
        return cls(
            length=length,
            retained_dimension=retained_dimension,
            computed_energies=computed_energies,
            continuum_energies=continuum_energies,
            eigenvectors=eigenvectors,
            quadrature_eigenvectors=quadrature_eigenvectors,
            consistent=consistent,
            unmatched=unmatched,
            boundary=boundary,
            continuum_coordinates=continuum_coordinates,
            continuum_wavefunctions=continuum_wavefunctions,
            selection=TailProbabilitySelection.from_dict(selection),
            convergence_interior_points=convergence_points,
            convergence_modes=convergence_modes,
            convergence=RelativeErrorConvergenceResult.from_dict(convergence),
            eigenpair_sweep=Piab1dEigenpairSweepResult.from_dict(eigenpair_sweep),
            residual_norm_sweep=Piab1dResidualNormSweepResult.from_dict(
                residual_norm_sweep
            ),
            finite_algebraic_diagnostics=Piab1dFiniteAlgebraicDiagnostics.from_dict(
                algebraic_diagnostics
            ),
            kinetic_potential_decomposition=KineticPotentialDecompositionResult.from_dict(
                decomposition
            ),
        )


class Piab1dVisualization(ModelAnalysisPngVisualization[Piab1dVisualizationPlotEnum]):
    """Associate a reusable PNG value with the PIAB1D plot inventory."""

    __slots__ = ()

    def __post_init__(self) -> None:
        if not isinstance(self.plot, Piab1dVisualizationPlotEnum):
            raise TypeError("plot must be Piab1dVisualizationPlotEnum")
        super().__post_init__()


@dataclass(frozen=True, slots=True)
class _Piab1dPngFigureRenderer(BaseModelAnalysisFigureRenderer):
    """Encode one independently composed PIAB1D figure as a PNG value."""

    plot: Piab1dVisualizationPlotEnum
    figure: BaseModelAnalysisFigure
    dpi: int

    def __post_init__(self) -> None:
        if not isinstance(self.plot, Piab1dVisualizationPlotEnum):
            raise TypeError("plot must be Piab1dVisualizationPlotEnum")
        if not isinstance(self.figure, BaseModelAnalysisFigure):
            raise TypeError("figure must be BaseModelAnalysisFigure")
        if type(self.dpi) is not int:
            raise TypeError("dpi must be a built-in integer")
        if self.dpi <= 0:
            raise ValueError("dpi must be positive")

    def visualize(self) -> Piab1dVisualization:
        """Draw, encode, close, and admit the owned PIAB1D figure."""
        return Piab1dVisualization(
            plot=self.plot,
            png=self._encode_png(self.figure.draw(), self.dpi),
        )


class _Piab1dSpectrumPlot(BaseModelAnalysisPlot):
    """Draw continuum and represented energies with the retained cutoff."""

    __slots__ = ("_data",)

    def __init__(self, data: Piab1dVisualizationData) -> None:
        self._data = data

    def draw(self, axis: Axes) -> None:
        data = self._data
        points = data.computed_energies.magnitude.size
        mode_numbers = np.arange(1, points + 1)
        axis.plot(
            mode_numbers,
            data.continuum_energies.magnitude,
            "o-",
            label="continuum",
        )
        axis.plot(
            mode_numbers,
            data.computed_energies.magnitude,
            "s--",
            label="finite difference",
        )
        axis.axvline(
            data.retained_dimension + 0.5,
            color="black",
            linewidth=0.8,
            linestyle=":",
        )


class _Piab1dSpectrumSubplot(BaseModelAnalysisSubplot):
    """Compose the spectrum plot with energy-axis presentation."""

    __slots__ = ("_plot",)

    def __init__(self, data: Piab1dVisualizationData) -> None:
        self._plot = _Piab1dSpectrumPlot(data)

    def draw(self, axis: Axes) -> None:
        self._plot.draw(axis)
        axis.set_xlabel("mode index")
        axis.set_ylabel("nondimensional energy")
        axis.set_title("PIAB1D spectrum")
        axis.legend()


class _Piab1dRetainedStatesPlot(BaseModelAnalysisPlot):
    """Draw normalized retained eigenvectors at vertically offset levels."""

    __slots__ = ("_data",)

    def __init__(self, data: Piab1dVisualizationData) -> None:
        self._data = data

    def draw(self, axis: Axes) -> None:
        data = self._data
        points = data.computed_energies.magnitude.size
        coordinates = np.linspace(0.0, data.length.magnitude, points + 2)[1:-1]
        for mode in range(data.retained_dimension):
            vector = data.eigenvectors.magnitude[:, mode]
            amplitude = vector / np.max(np.abs(vector))
            axis.plot(coordinates, amplitude + 2.0 * mode, label=f"mode {mode + 1}")


class _Piab1dRetainedStatesSubplot(BaseModelAnalysisSubplot):
    """Compose retained-state curves with position-axis presentation."""

    __slots__ = ("_plot",)

    def __init__(self, data: Piab1dVisualizationData) -> None:
        self._plot = _Piab1dRetainedStatesPlot(data)

    def draw(self, axis: Axes) -> None:
        self._plot.draw(axis)
        axis.set_xlabel("position")
        axis.set_ylabel("normalized amplitude + offset")
        axis.set_title("Retained discrete states")
        axis.legend()


class _Piab1dSpectrumAndStatesFigure(BaseModelAnalysisFigure):
    """Compose independently owned spectrum and retained-state subplots."""

    __slots__ = ("_data",)

    def __init__(self, data: Piab1dVisualizationData) -> None:
        self._data = data

    def draw(self) -> Figure:
        figure, axes = plt.subplots(
            1,
            2,
            figsize=(10.0, 4.0),
            constrained_layout=True,
        )
        _Piab1dSpectrumSubplot(self._data).draw(axes[0])
        _Piab1dRetainedStatesSubplot(self._data).draw(axes[1])
        return figure


class _Piab1dFigure(BaseModelAnalysisFigure):
    """Bind authenticated PIAB1D data to one model-specific figure action."""

    __slots__ = ("_data",)

    def __init__(self, data: Piab1dVisualizationData) -> None:
        if not isinstance(data, Piab1dVisualizationData):
            raise TypeError("data must be Piab1dVisualizationData")
        self._data = data


class _ResidualMatricesFigure(_Piab1dFigure):
    def draw(self) -> Figure:
        residuals = (
            ("consistent reduction", self._data.consistent.magnitude),
            ("embedded minus parent", self._data.unmatched.magnitude),
            ("Dirichlet minus cyclic", self._data.boundary.magnitude),
        )
        maximum = max(float(np.max(np.abs(matrix))) for _, matrix in residuals)
        if maximum == 0.0:
            raise ValueError("residual rendering requires a nonzero matrix")
        normalization = TwoSlopeNorm(vmin=-maximum, vcenter=0.0, vmax=maximum)
        figure, axes = plt.subplots(1, 3, figsize=(12.0, 3.8), constrained_layout=True)
        image = None
        for axis, (title, matrix) in zip(axes, residuals, strict=True):
            image = axis.imshow(matrix, cmap="coolwarm", norm=normalization)
            axis.set_title(title)
            axis.set_xlabel("column")
            axis.set_ylabel("row")
        if image is None:
            raise RuntimeError("no residual matrix was rendered")
        figure.colorbar(image, ax=axes, shrink=0.8, label="matrix entry")
        return figure


class _ContinuumWavefunctionLadderFigure(_Piab1dFigure):
    def draw(self) -> Figure:
        data = self._data
        if data.retained_dimension != 3:
            raise ValueError("the ladder plot requires exactly three retained states")
        colors = ("#0072B2", "#D55E00", "#009E73")
        figure, axis = plt.subplots(figsize=(5.2, 5.0), constrained_layout=True)
        for mode, color in zip(range(1, 4), colors, strict=True):
            energy = data.continuum_energies.magnitude[mode - 1]
            wavefunction = data.continuum_wavefunctions.magnitude[:, mode - 1]
            axis.axhline(energy, color=color, linewidth=0.8, alpha=0.45)
            axis.plot(
                data.continuum_coordinates.magnitude,
                energy + 2.4 * wavefunction,
                color=color,
                linewidth=2.0,
            )
            axis.text(
                1.015,
                energy,
                rf"$E_{mode}$",
                color=color,
                va="center",
                ha="left",
            )
        self._style_axis(axis, "Continuum eigenfunctions")
        return figure

    def _style_axis(self, axis: plt.Axes, title: str) -> None:
        axis.axvline(0.0, color="black", linewidth=1.2)
        axis.axvline(1.0, color="black", linewidth=1.2)
        axis.set_xlim(-0.04, 1.04)
        axis.set_xlabel(r"position $x/L$")
        axis.set_ylabel("energy")
        axis.set_title(title)
        axis.spines[["top", "right"]].set_visible(False)


class _DiscreteWavefunctionLadderFigure(_Piab1dFigure):
    def draw(self) -> Figure:
        data = self._data
        if data.retained_dimension != 3:
            raise ValueError("the ladder plot requires exactly three retained states")
        points = data.computed_energies.magnitude.size
        length = data.length.magnitude
        coordinates = np.linspace(0.0, length, points + 2)[1:-1]
        plotted_coordinates = np.concatenate(([0.0], coordinates / length, [1.0]))
        colors = ("#0072B2", "#D55E00", "#009E73")
        figure, axis = plt.subplots(figsize=(5.2, 5.0), constrained_layout=True)
        for mode, color in zip(range(1, 4), colors, strict=True):
            energy = data.computed_energies.magnitude[mode - 1]
            values = np.concatenate(
                (
                    [0.0],
                    data.quadrature_eigenvectors.magnitude[:, mode - 1],
                    [0.0],
                )
            )
            axis.axhline(energy, color=color, linewidth=0.8, alpha=0.45)
            axis.plot(
                plotted_coordinates,
                energy + 2.4 * values,
                color=color,
                linewidth=1.2,
                alpha=0.65,
            )
            axis.scatter(
                plotted_coordinates,
                energy + 2.4 * values,
                color=color,
                s=23,
                zorder=3,
            )
            axis.text(
                1.015,
                energy,
                rf"$E_{{{mode},\Delta x}}$",
                color=color,
                va="center",
                ha="left",
            )
        axis.axvline(0.0, color="black", linewidth=1.2)
        axis.axvline(1.0, color="black", linewidth=1.2)
        axis.set_xlim(-0.04, 1.04)
        axis.set_xlabel(r"position $x/L$")
        axis.set_ylabel("energy")
        axis.set_title(rf"Finite-grid wavefunctions ($N={points + 2}$)")
        axis.spines[["top", "right"]].set_visible(False)
        return figure


class _RetainedDimensionSelectionFigure(_Piab1dFigure):
    def draw(self) -> Figure:
        data = self._data
        dimensions = np.arange(
            1,
            data.selection.probabilities.magnitude.size + 1,
            dtype=np.int64,
        )
        tolerance_axis = np.logspace(-8.0, np.log10(0.35), 2000)
        required_dimensions = np.asarray(
            [
                dimensions[
                    np.flatnonzero(
                        data.selection.omitted_probabilities.magnitude
                        <= candidate_tolerance
                    )[0]
                ]
                for candidate_tolerance in tolerance_axis
            ],
            dtype=np.int64,
        )
        figure, axis = plt.subplots(figsize=(7.6, 4.8), constrained_layout=True)
        axis.step(
            tolerance_axis,
            required_dimensions,
            where="post",
            color="#0072B2",
            linewidth=2.2,
            label=r"required dimension $M_\star(\tau)$",
        )
        axis.annotate(
            rf"$\tau={data.selection.tolerance:.2f}\;\Longrightarrow\;"
            rf"M_\star={data.selection.selected_count}$",
            xy=(data.selection.tolerance, data.selection.selected_count),
            xytext=(
                data.selection.tolerance * 2.0,
                data.selection.selected_count + 0.65,
            ),
            arrowprops={"arrowstyle": "->", "color": "black"},
        )
        axis.set(
            title="Required retained dimension versus a priori tolerance",
            xlabel=r"omitted-probability tolerance $\tau$",
            ylabel=r"minimum retained dimension $M_\star(\tau)$",
            yticks=dimensions,
            xscale="log",
        )
        axis.grid(True, which="both", alpha=0.25)
        axis.legend(frameon=False, loc="upper right")
        return figure


class _ConvergenceSeriesFigure(_Piab1dFigure):
    def draw(self) -> Figure:
        data = self._data
        convergence = data.convergence
        spacings = convergence.spacings.magnitude
        point_counts = np.asarray(data.convergence_interior_points, dtype=np.int64) + 2
        marker_interval = max(point_counts.size // 12, 1)
        colors = ("#0072B2", "#D55E00", "#009E73")
        figure, axes = plt.subplots(1, 2, figsize=(11.5, 4.5), constrained_layout=True)
        error_axis, order_axis = axes
        order_modes = tuple(
            data.convergence_modes[column] for column in convergence.order_columns
        )
        for column, (mode, color) in enumerate(zip(order_modes, colors, strict=True)):
            mode_column = data.convergence_modes.index(mode)
            error_axis.loglog(
                spacings,
                convergence.relative_errors.magnitude[:, mode_column],
                "-",
                color=color,
                marker="o",
                markevery=marker_interval,
                markersize=4,
                label=rf"mode $n={mode}$",
            )
            order_axis.plot(
                point_counts[1:],
                convergence.observed_orders.magnitude[:, column],
                "-",
                color=color,
                marker="o",
                markevery=marker_interval,
                markersize=4,
                label=rf"mode $n={mode}$",
            )
        reference = spacings**2
        reference *= 0.8 * error_axis.get_ylim()[1] / reference[0]
        error_axis.loglog(
            spacings,
            reference,
            "k--",
            alpha=0.65,
            label=r"$O((\Delta x)^2)$",
        )
        error_axis.invert_xaxis()
        error_axis.set(
            title="Fixed-mode eigenvalue convergence",
            xlabel=r"grid spacing $\Delta x$",
            ylabel="relative energy error",
        )
        error_axis.grid(True, which="both", alpha=0.25)
        error_axis.legend(frameon=False)
        order_axis.axhline(2.0, color="black", linestyle="--", alpha=0.65)
        order_axis.set(
            title="Observed order between refinements",
            xlabel=r"closed-interval grid points $N$",
            ylabel="observed order",
        )
        order_axis.grid(True, alpha=0.25)
        order_axis.legend(frameon=False)
        figure.suptitle(
            "Particle-in-a-box grid-refinement series",
            fontsize=14,
            fontweight="bold",
        )
        return figure


class _ConvergenceModeSweepFigure(_Piab1dFigure):
    def draw(self) -> Figure:
        data = self._data
        convergence = data.convergence
        selected_indices = np.unique(
            np.linspace(
                0,
                len(data.convergence_interior_points) - 1,
                7,
                dtype=np.int64,
            )
        )
        figure, axis = plt.subplots(figsize=(7.6, 4.8), constrained_layout=True)
        colors = plt.colormaps["viridis"](np.linspace(0.08, 0.9, selected_indices.size))
        for index, color in zip(selected_indices, colors, strict=True):
            axis.semilogy(
                data.convergence_modes,
                convergence.relative_errors.magnitude[index],
                "o-",
                color=color,
                label=rf"$N={data.convergence_interior_points[index] + 2}$",
            )
        axis.set(
            title="Error across mode index and grid resolution",
            xlabel="fixed continuum mode index $n$",
            ylabel="relative energy error",
            xticks=data.convergence_modes,
        )
        axis.grid(True, which="both", alpha=0.25)
        axis.legend(frameon=False, ncol=2)
        return figure


class _HigherEigenpairSweepFigure(_Piab1dFigure):
    def draw(self) -> Figure:
        sweep = self._data.eigenpair_sweep
        dimensions = sweep.definition.interior_points
        selected = np.unique(np.linspace(0, len(dimensions) - 1, 7, dtype=np.int64))
        colors = plt.colormaps["viridis"](np.linspace(0.08, 0.9, selected.size))
        figure, axes = plt.subplots(1, 2, figsize=(11.8, 4.5), constrained_layout=True)
        energy_axis, vector_axis = axes
        floor = np.finfo(np.float64).eps
        for grid_index, color in zip(selected, colors, strict=True):
            start = sweep.grid_offsets[int(grid_index)]
            stop = sweep.grid_offsets[int(grid_index) + 1]
            fraction = sweep.fractional_mode_indices.magnitude[start:stop]
            energy_axis.semilogy(
                fraction,
                sweep.relative_energy_errors.magnitude[start:stop],
                "-",
                color=color,
                label=rf"$N={dimensions[int(grid_index)] + 2}$",
            )
            vector_axis.semilogy(
                fraction,
                np.maximum(sweep.nodal_overlap_defects.magnitude[start:stop], floor),
                ".",
                color=color,
                label=rf"$N={dimensions[int(grid_index)] + 2}$",
            )
        energy_axis.set(
            title="Eigenvalue dispersion across the spectrum",
            xlabel=r"fractional mode index $n/(N-1)$",
            ylabel="relative energy error",
        )
        vector_axis.set(
            title="Agreement with continuum sine at grid nodes",
            xlabel=r"fractional mode index $n/(N-1)$",
            ylabel=r"nodal overlap defect $1-|\langle v,s_n\rangle|$",
        )
        for axis in axes:
            axis.grid(True, which="both", alpha=0.25)
            axis.legend(frameon=False)
        figure.suptitle(
            "Higher-index particle-in-a-box eigenpair sweep",
            fontsize=14,
            fontweight="bold",
        )
        return figure


class _HigherModeConvergenceFigure(_Piab1dFigure):
    def draw(self) -> Figure:
        sweep = self._data.eigenpair_sweep
        fixed_modes = sweep.definition.fixed_modes
        colors = plt.colormaps["tab10"](np.linspace(0.0, 0.8, len(fixed_modes)))
        figure, axes = plt.subplots(1, 2, figsize=(11.5, 4.5), constrained_layout=True)
        error_axis, order_axis = axes
        for mode, color in zip(fixed_modes, colors, strict=True):
            convergence = sweep.fixed_mode_convergence(mode)
            dimensions = np.asarray(
                tuple(
                    value for value in sweep.definition.interior_points if mode <= value
                ),
                dtype=np.int64,
            )
            marker_interval = max(dimensions.size // 12, 1)
            error_axis.loglog(
                convergence.spacings.magnitude,
                convergence.relative_errors.magnitude[:, 0],
                "-o",
                color=color,
                markevery=marker_interval,
                markersize=4,
                label=rf"$n={mode}$",
            )
            order_axis.plot(
                dimensions[1:] + 2,
                convergence.observed_orders.magnitude[:, 0],
                "-o",
                color=color,
                markevery=marker_interval,
                markersize=4,
                label=rf"$n={mode}$",
            )
        reference_spacings = sweep.spacings.magnitude
        reference = reference_spacings**2
        reference *= 0.8 * error_axis.get_ylim()[1] / reference[0]
        error_axis.loglog(
            reference_spacings,
            reference,
            "k--",
            alpha=0.65,
            label=r"$O((\Delta x)^2)$",
        )
        error_axis.invert_xaxis()
        error_axis.set(
            title="Fixed higher-mode refinement",
            xlabel=r"grid spacing $\Delta x$",
            ylabel="relative energy error",
        )
        order_axis.axhline(2.0, color="black", linestyle="--", alpha=0.65)
        order_axis.set(
            title="Observed order between refinements",
            xlabel=r"closed-interval grid points $N$",
            ylabel="observed order",
        )
        for axis in axes:
            axis.grid(True, which="both", alpha=0.25)
            axis.legend(frameon=False)
        figure.suptitle(
            "Convergence of fixed higher eigenvalues",
            fontsize=14,
            fontweight="bold",
        )
        return figure


class _OperatorResidualNormsFigure(_Piab1dFigure):
    def draw(self) -> Figure:
        result = self._data.residual_norm_sweep
        points = np.asarray(result.definition.interior_points) + 2
        marker_interval = max(points.size // 12, 1)
        figure, axes = plt.subplots(2, 2, figsize=(11.8, 8.0), constrained_layout=True)
        series = (
            (
                "unmatched compression",
                result.unmatched,
                result.unmatched_relative,
                "#D55E00",
            ),
            (
                "boundary realization",
                result.boundary,
                result.boundary_relative,
                "#0072B2",
            ),
        )
        for label, raw, _, color in series:
            axes[0, 0].loglog(
                points,
                raw.magnitude[:, 0],
                "-o",
                color=color,
                markevery=marker_interval,
                markersize=4,
                label=label,
            )
        axes[0, 0].set(title="Raw Frobenius norms", ylabel=r"$\|R\|_F$")
        norm_labels = ("Frobenius", "spectral", "maximum absolute entry")
        for column, (axis, norm_label) in enumerate(
            zip(axes.flat[1:], norm_labels, strict=True)
        ):
            for label, _, relative, color in series:
                axis.semilogx(
                    points,
                    relative.magnitude[:, column],
                    "-o",
                    color=color,
                    markevery=marker_interval,
                    markersize=4,
                    label=label,
                )
            axis.set(title=norm_label, ylabel="same-grid norm ratio")
        for axis in axes.flat:
            axis.set_xlabel("closed-interval grid points")
            axis.grid(True, which="both", alpha=0.25)
            axis.legend(frameon=False)
        figure.suptitle(
            "Operator residuals under canonical matrix norms", fontweight="bold"
        )
        return figure


class _EigensolverResidualNormsFigure(_Piab1dFigure):
    def draw(self) -> Figure:
        result = self._data.residual_norm_sweep
        points = np.asarray(result.definition.interior_points) + 2
        labels = ("Frobenius", "spectral", "maximum absolute entry")
        colors = ("#0072B2", "#D55E00", "#009E73")
        figure, axis = plt.subplots(figsize=(8.0, 4.8), constrained_layout=True)
        for column, (label, color) in enumerate(zip(labels, colors, strict=True)):
            axis.loglog(
                points,
                result.eigensolver_relative.magnitude[:, column],
                "-o",
                color=color,
                markevery=max(points.size // 12, 1),
                markersize=4,
                label=label,
            )
        axis.set(
            title="Discrete eigensolver residuals under canonical norms",
            xlabel="closed-interval grid points",
            ylabel="same-grid norm ratio",
        )
        axis.grid(True, which="both", alpha=0.25)
        axis.legend(frameon=False)
        axis.text(
            0.50,
            0.05,
            "Solver diagnostic only—not continuum error",
            transform=axis.transAxes,
        )
        return figure


class _FiniteAlgebraicDiagnosticsFigure(_Piab1dFigure):
    def draw(self) -> Figure:
        data = self._data.finite_algebraic_diagnostics
        points = np.asarray(data.definition.interior_points) + 2
        panels = (
            (
                "Spectral consistency",
                (
                    (data.discrete_spectrum, r"$\delta_E$", "#0072B2"),
                    (data.spectral_reconstruction, r"$\delta_{rec}$", "#D55E00"),
                ),
            ),
            (
                "Retained-operator consistency",
                (
                    (data.retained_coordinates, r"$\delta_{coord}$", "#009E73"),
                    (data.retained_embedding, r"$\delta_{embed}$", "#CC79A7"),
                    (data.spectral_leakage, r"$\delta_{leak}$", "#E69F00"),
                ),
            ),
            (
                "Projector idempotency",
                ((data.projector_idempotency, r"$\delta_{proj}$", "#56B4E9"),),
            ),
        )
        figure, axes = plt.subplots(3, 1, figsize=(8.2, 9.2), constrained_layout=True)
        for axis, (title, series) in zip(axes, panels, strict=True):
            positive = np.concatenate(
                tuple(
                    values.magnitude[values.magnitude > 0.0] for values, _, _ in series
                )
            )
            floor = (
                0.5 * float(np.min(positive))
                if positive.size
                else np.finfo(np.float64).eps
            )
            for values, label, color in series:
                axis.loglog(
                    points,
                    np.maximum(values.magnitude, floor),
                    color=color,
                    linewidth=1.8,
                    label=label,
                )
            axis.set(
                title=title,
                xlabel="closed-interval grid points",
                ylabel="algebraic discrepancy",
            )
            axis.grid(True, which="both", alpha=0.25)
            axis.legend(frameon=False)
        figure.suptitle(
            "Finite spectral and reduction diagnostics",
            fontsize=15,
            fontweight="bold",
        )
        return figure


class _KineticPotentialDecompositionFigure(_Piab1dFigure):
    def draw(self) -> Figure:
        result = self._data.kinetic_potential_decomposition
        shift = result.alternative_potential.magnitude
        maximum = float(np.max(np.abs(shift)))
        if maximum == 0.0:
            raise ValueError("decomposition shift must be nonzero")
        figure, axes = plt.subplots(1, 2, figsize=(10.8, 4.4), constrained_layout=True)
        matrix_axis, fit_axis = axes
        image = matrix_axis.imshow(
            shift,
            cmap="RdBu_r",
            norm=TwoSlopeNorm(vmin=-maximum, vcenter=0.0, vmax=maximum),
            interpolation="nearest",
        )
        matrix_axis.set(
            title="Illustrative decomposition shift",
            xlabel="retained-coordinate column",
            ylabel="retained-coordinate row",
            xticks=np.arange(shift.shape[1]),
            yticks=np.arange(shift.shape[0]),
        )
        figure.colorbar(image, ax=matrix_axis, shrink=0.82)
        labels = ("scalar", "diagonal", "tridiagonal", "real\nsymmetric")
        values = tuple(
            fit.unexplained_frobenius_norm.magnitude for fit in result.model_class_fits
        )
        bars = fit_axis.bar(
            labels,
            values,
            color=("#CC79A7", "#E69F00", "#56B4E9", "#009E73"),
        )
        fit_axis.set(
            title="Unexplained residual after model-class fit",
            xlabel="admissible model class",
            ylabel=r"$\|K-V_{class}\|_F$",
        )
        fit_axis.grid(True, axis="y", alpha=0.25)
        scale = max(values)
        for bar, value in zip(bars, values, strict=True):
            fit_axis.text(
                bar.get_x() + bar.get_width() / 2.0,
                value + 0.025 * scale,
                f"{value:.3f}",
                ha="center",
                va="bottom",
            )
        figure.suptitle(
            "Kinetic-potential decomposition under declared model classes",
            fontsize=13,
            fontweight="bold",
        )
        return figure


class Piab1dVisualizer(BaseModelAnalysisVisualizer):
    """Render a typed, digest-bound PIAB1D plot inventory."""

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
        """Bind authenticated typed data to the closed PIAB1D plot inventory.

        Parameters
        ----------
        data
            Verifier-derived immutable visualization projection.
        verification
            Passing aggregate that authenticates the canonical JSON digest of
            ``data``.
        summary_dpi
            Positive integer resolution for summary matrix and spectrum figures.
        ladder_dpi
            Positive integer resolution for wavefunction ladder figures.
        selection_dpi
            Positive integer resolution for convergence, selection, sweep,
            diagnostic, and decomposition figures.

        Raises
        ------
        TypeError
            Data, verification, or a DPI value has the wrong type.
        ValueError
            Verification failed, the data digest differs, or a DPI is not positive.
        RuntimeError
            Renderer ownership is duplicated or does not cover all 13 enum members.

        Notes
        -----
        Verification authenticates scientific inputs. PNG encoding remains a separate
        deterministic presentation action.
        """
        if not isinstance(data, Piab1dVisualizationData):
            raise TypeError("data must be Piab1dVisualizationData")
        if not isinstance(verification, Piab1dVerification):
            raise TypeError("verification must be Piab1dVerification")
        self._authenticate(data, verification)
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
        self._renderers: frozenset[_Piab1dPngFigureRenderer] = frozenset(
            _Piab1dPngFigureRenderer(plot=plot, figure=figure, dpi=dpi)
            for plot, figure, dpi in figure_specs
        )
        plots = {renderer.plot for renderer in self._renderers}
        if len(plots) != len(self._renderers):
            raise RuntimeError("PIAB1D renderers must own unique plot enum members")
        if plots != set(Piab1dVisualizationPlotEnum):
            raise RuntimeError("PIAB1D renderers must cover the closed plot inventory")

    @property
    def plots(self) -> frozenset[Piab1dVisualizationPlotEnum]:
        """Return the complete closed PIAB1D plot inventory.

        Returns
        -------
        frozenset[Piab1dVisualizationPlotEnum]
            Exactly the 13 uniquely owned plot identities.
        """
        return frozenset(renderer.plot for renderer in self._renderers)

    def visualize(self) -> frozenset[Piab1dVisualization]:
        """Render the complete authenticated PIAB1D figure set.

        Returns
        -------
        frozenset[Piab1dVisualization]
            Thirteen immutable validated PNG values with unique canonical filenames.

        Raises
        ------
        RuntimeError
            Rendered plot identities differ from the closed renderer inventory.
        ValueError
            A plot-specific precondition or PNG validation rule fails.

        Notes
        -----
        This method returns in-memory values. Atomic directory publication and hash
        manifest creation remain responsibilities of the rendering script.
        """
        visualizations = frozenset(renderer.visualize() for renderer in self._renderers)
        self._require_complete_inventory(
            visualizations,
            self.plots,
        )
        return visualizations
