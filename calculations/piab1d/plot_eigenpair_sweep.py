#!/usr/bin/env python3
"""Plot the retained higher-index eigenpair sweep."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np


def plot_full_spectrum(payload: dict[str, Any], output: Path) -> None:
    """Plot energy dispersion and nodal eigenvector agreement across the spectrum."""
    grids = payload["grids"]
    selected_indices = np.unique(np.linspace(0, len(grids) - 1, 7, dtype=int))
    selected = [grids[index] for index in selected_indices]
    figure, axes = plt.subplots(1, 2, figsize=(11.8, 4.5), constrained_layout=True)
    energy_axis, vector_axis = axes
    colors = plt.colormaps["viridis"](np.linspace(0.08, 0.9, len(selected)))
    floor = np.finfo(np.float64).eps

    for grid, color in zip(selected, colors, strict=True):
        fraction = [record["fractional_mode_index"] for record in grid["eigenpairs"]]
        energy_error = [
            record["relative_energy_error"] for record in grid["eigenpairs"]
        ]
        overlap_error = [
            max(record["nodal_overlap_defect"], floor) for record in grid["eigenpairs"]
        ]
        label = rf"$N={grid['interior_points'] + 2}$"
        energy_axis.semilogy(fraction, energy_error, "-", color=color, label=label)
        vector_axis.semilogy(fraction, overlap_error, ".", color=color, label=label)

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
    figure.savefig(output, dpi=180)
    plt.close(figure)


def plot_fixed_modes(payload: dict[str, Any], output: Path) -> None:
    """Plot refinement errors and observed orders for fixed higher modes."""
    grids = payload["grids"]
    fixed = payload["fixed_higher_mode_series"]
    fixed_modes = payload["input"]["grid_series"]["fixed_higher_modes"]
    colors = ["#0072B2", "#D55E00", "#009E73"]
    figure, axes = plt.subplots(1, 2, figsize=(11.5, 4.5), constrained_layout=True)
    error_axis, order_axis = axes

    for mode, color in zip(fixed_modes, colors, strict=True):
        record = fixed[str(mode)]
        spacings = np.asarray(record["spacings"], dtype=float)
        errors = np.asarray(record["relative_energy_errors"], dtype=float)
        orders = np.asarray(record["observed_orders"][1:], dtype=float)
        total_points = np.asarray(record["interior_points"], dtype=int) + 2
        marker_interval = max(len(total_points) // 12, 1)
        error_axis.loglog(
            spacings,
            errors,
            "-",
            color=color,
            marker="o",
            markevery=marker_interval,
            markersize=4,
            label=rf"$n={mode}$",
        )
        order_axis.plot(
            total_points[1:],
            orders,
            "-",
            color=color,
            marker="o",
            markevery=marker_interval,
            markersize=4,
            label=rf"$n={mode}$",
        )

    reference_spacings = np.asarray([grid["spacing"] for grid in grids], dtype=float)
    reference = reference_spacings**2
    reference *= 0.8 * error_axis.get_ylim()[1] / reference[0]
    error_axis.loglog(
        reference_spacings, reference, "k--", alpha=0.65, label=r"$O((\Delta x)^2)$"
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
    figure.savefig(output, dpi=180)
    plt.close(figure)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--spectrum-output", type=Path, required=True)
    parser.add_argument("--fixed-mode-output", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.result.read_text(encoding="utf-8"))
    plot_full_spectrum(payload, args.spectrum_output)
    plot_fixed_modes(payload, args.fixed_mode_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
