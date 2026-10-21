"""Plot QHO1D eigenstates, distortions, and reusable development diagnostics."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ksdft2effmass.model_systems.qho1d import (
    Qho1dComparisonResult,
    Qho1dResultVerifier,
    Qho1dStudyEvaluator,
    Qho1dStudyInputDeserializer,
    Qho1dStudyResult,
    Unitless,
    VectorQuantity,
)

CALCULATION_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = CALCULATION_ROOT.parents[1]
INPUT_PATH = CALCULATION_ROOT / "input.json"
DEVELOPMENT_ROOT = CALCULATION_ROOT / "analysis" / "development"
RESULT_PATH = DEVELOPMENT_ROOT / "qho1d-result.json"
EIGENSTATE_OUTPUT_PATH = DEVELOPMENT_ROOT / "qho1d-eigenstates.png"
DISTORTION_OUTPUT_PATH = DEVELOPMENT_ROOT / "qho1d-eigenstate-distortion.png"
DIAGNOSTIC_OUTPUT_PATH = DEVELOPMENT_ROOT / "qho1d-diagnostics.png"
SELECTED_BOX_HALF_WIDTH = 8.0
SELECTED_GRID_SPACING = 0.05
SELECTED_RETAINED_DIMENSION = 6
DISPLAYED_STATES = 4


def selected_comparison(result: Qho1dStudyResult) -> Qho1dComparisonResult:
    """Return the fixed fine-grid comparison used by the state plots."""
    selected = tuple(
        comparison
        for comparison in result.comparisons
        if comparison.request.box_half_width.magnitude == SELECTED_BOX_HALF_WIDTH
        and comparison.grid_spacing.magnitude == SELECTED_GRID_SPACING
        and comparison.request.retained_dimension == SELECTED_RETAINED_DIMENSION
    )
    if len(selected) != 1:
        raise ValueError("selected QHO1D comparison must be unique")
    return selected[0]


def aligned_eigenstates(
    comparison: Qho1dComparisonResult,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return coordinates, exact states, aligned grid states, and grid eigenvalues."""
    request = comparison.request
    coordinates = comparison.grid_coordinates.magnitude
    spacing = comparison.grid_spacing.magnitude
    oscillator_length = request.parameters.oscillator_length.magnitude
    exact = request.analytical.number_state_wavefunctions(
        VectorQuantity(coordinates / oscillator_length, Unitless()),
        request.retained_dimension,
    ).magnitude
    hamiltonian = request.finite_difference.hamiltonian().to_dense().magnitude
    eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian)
    grid_states = eigenvectors[:, : request.retained_dimension] / np.sqrt(spacing)
    for state in range(request.retained_dimension):
        overlap = spacing * np.dot(exact[:, state], grid_states[:, state])
        if overlap < 0.0:
            grid_states[:, state] *= -1.0
    return (
        coordinates,
        exact,
        grid_states,
        eigenvalues[: request.retained_dimension],
    )


def state_axes() -> tuple[Figure, np.ndarray]:
    """Create the fixed two-by-two state-plot layout."""
    figure, axes = plt.subplots(2, 2, figsize=(10.0, 7.0), sharex=True)
    return figure, np.asarray(axes, dtype=object)


def plot_eigenstates(comparison: Qho1dComparisonResult, output: Path) -> None:
    """Plot exact Hermite states and aligned finite-grid eigenvectors."""
    coordinates, exact, grid_states, _ = aligned_eigenstates(comparison)
    figure, axes = state_axes()
    flat_axes = axes.ravel()
    for state in range(DISPLAYED_STATES):
        axis = flat_axes[state]
        if not isinstance(axis, Axes):
            raise TypeError("state subplot must be a matplotlib Axes")
        axis.plot(coordinates, exact[:, state], label="real-line Hermite", linewidth=2)
        axis.plot(
            coordinates,
            grid_states[:, state],
            "--",
            label="finite Dirichlet grid",
            linewidth=1.5,
        )
        axis.scatter(
            (-SELECTED_BOX_HALF_WIDTH, SELECTED_BOX_HALF_WIDTH),
            (0.0, 0.0),
            color="black",
            marker="x",
            label="Dirichlet boundary" if state == 0 else None,
        )
        axis.set_title(f"state n={state}")
        axis.set_ylabel(r"wavefunction")
        axis.grid(alpha=0.25)
    for axis in flat_axes[-2:]:
        if isinstance(axis, Axes):
            axis.set_xlabel(r"dimensionless coordinate $x/\ell$")
    handles, labels = flat_axes[0].get_legend_handles_labels()
    figure.suptitle(
        "QHO1D exact and finite-grid eigenstates "
        f"(b={SELECTED_BOX_HALF_WIDTH:g}, h={SELECTED_GRID_SPACING:g})",
        y=0.995,
    )
    figure.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.955),
        ncol=3,
    )
    figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.89))
    figure.savefig(output, dpi=180)
    plt.close(figure)


def plot_eigenstate_distortion(comparison: Qho1dComparisonResult, output: Path) -> None:
    """Plot pointwise state distortion and finite-grid eigenvalue error."""
    coordinates, exact, grid_states, grid_eigenvalues = aligned_eigenstates(comparison)
    exact_eigenvalues = comparison.request.analytical.number_state_energies(
        comparison.request.retained_dimension
    ).magnitude
    figure, axes = plt.subplots(2, 1, figsize=(9.0, 8.0))
    state_axis, energy_axis = axes
    for state in range(DISPLAYED_STATES):
        state_axis.plot(
            coordinates,
            grid_states[:, state] - exact[:, state],
            label=f"n={state}",
        )
    state_axis.axhline(0.0, color="black", linewidth=0.8)
    state_axis.set_ylabel("grid state minus Hermite state")
    state_axis.set_xlabel(r"dimensionless coordinate $x/\ell$")
    state_axis.set_title("Pointwise eigenstate distortion on interior coordinates")
    state_axis.legend(ncol=4)
    state_axis.grid(alpha=0.25)

    states = np.arange(comparison.request.retained_dimension)
    energy_axis.bar(states, grid_eigenvalues - exact_eigenvalues)
    energy_axis.axhline(0.0, color="black", linewidth=0.8)
    energy_axis.set_xlabel("state index n")
    energy_axis.set_ylabel(r"$E_{n,h,X}-E_n$")
    energy_axis.set_title("Finite-grid eigenvalue distortion")
    energy_axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(output, dpi=180)
    plt.close(figure)


def matching_results(
    result: Qho1dStudyResult,
    *,
    box_half_width: float | None = None,
    grid_spacing: float | None = None,
) -> tuple[Qho1dComparisonResult, ...]:
    """Return deterministically ordered results matching explicit controls."""
    return tuple(
        comparison
        for comparison in result.comparisons
        if (
            box_half_width is None
            or comparison.request.box_half_width.magnitude == box_half_width
        )
        and (grid_spacing is None or comparison.grid_spacing.magnitude == grid_spacing)
    )


def residual_frobenius(comparison: Qho1dComparisonResult) -> float:
    """Return the binary64 residual norm ``||H J - J H_K||_F``."""
    hamiltonian = (
        comparison.request.finite_difference.hamiltonian().to_dense().magnitude
    )
    injection = comparison.injection.magnitude
    reference = comparison.reference_hamiltonian.magnitude
    return float(
        np.linalg.norm(hamiltonian @ injection - injection @ reference, ord="fro")
    )


def plot_diagnostics(result: Qho1dStudyResult, output: Path) -> None:
    """Plot existing discrepancy channels and the reusable residual diagnostic."""
    figure, axes = plt.subplots(2, 2, figsize=(11.0, 8.5))
    convergence_axis, gram_axis, components_axis, residual_axis = axes.ravel()

    fine_box = matching_results(result, box_half_width=SELECTED_BOX_HALF_WIDTH)
    for retained in result.definition.retained_dimensions:
        cases = tuple(
            comparison
            for comparison in fine_box
            if comparison.request.retained_dimension == retained
        )
        convergence_axis.loglog(
            [case.grid_spacing.magnitude for case in cases],
            [case.relative_discrepancy.magnitude for case in cases],
            marker="o",
            label=f"K={retained}",
        )
    convergence_axis.invert_xaxis()
    convergence_axis.set_xlabel("grid spacing h")
    convergence_axis.set_ylabel("relative Frobenius discrepancy")
    convergence_axis.set_title(f"Spatial refinement at b={SELECTED_BOX_HALF_WIDTH:g}")
    convergence_axis.legend()
    convergence_axis.grid(alpha=0.25)

    fine_grid = matching_results(result, grid_spacing=SELECTED_GRID_SPACING)
    for retained in result.definition.retained_dimensions:
        cases = tuple(
            comparison
            for comparison in fine_grid
            if comparison.request.retained_dimension == retained
        )
        gram_axis.semilogy(
            [case.request.box_half_width.magnitude for case in cases],
            [case.gram_deviation.magnitude for case in cases],
            marker="o",
            label=f"K={retained}",
        )
    gram_axis.set_xlabel("box half-width b")
    gram_axis.set_ylabel(r"$\|G-I\|_F$")
    gram_axis.set_title(f"Sampled Gram defect at h={SELECTED_GRID_SPACING:g}")
    gram_axis.legend()
    gram_axis.grid(alpha=0.25)

    selected_components = tuple(
        comparison
        for comparison in fine_grid
        if comparison.request.box_half_width.magnitude == SELECTED_BOX_HALF_WIDTH
    )
    retained_dimensions = np.asarray(
        [case.request.retained_dimension for case in selected_components],
        dtype=np.float64,
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
        [residual_frobenius(case) for case in result.comparisons], dtype=np.float64
    )
    discrepancies = np.asarray(
        [case.absolute_discrepancy.magnitude for case in result.comparisons],
        dtype=np.float64,
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
    figure.savefig(output, dpi=180)
    plt.close(figure)


def main() -> int:
    """Verify the development result and write three replaceable figures."""
    Qho1dResultVerifier().execute(RESULT_PATH, REPOSITORY_ROOT)
    definition = Qho1dStudyInputDeserializer().execute(INPUT_PATH.read_bytes())
    result = Qho1dStudyEvaluator().execute(definition)
    selected = selected_comparison(result)
    DEVELOPMENT_ROOT.mkdir(parents=True, exist_ok=True)
    plot_eigenstates(selected, EIGENSTATE_OUTPUT_PATH)
    plot_eigenstate_distortion(selected, DISTORTION_OUTPUT_PATH)
    plot_diagnostics(result, DIAGNOSTIC_OUTPUT_PATH)
    print(
        "calculation=qho1d lifecycle=development plots=written "
        f"outputs={EIGENSTATE_OUTPUT_PATH},{DISTORTION_OUTPUT_PATH},"
        f"{DIAGNOSTIC_OUTPUT_PATH}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
