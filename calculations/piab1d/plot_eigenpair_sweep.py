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
    figure, axes = plt.subplots(1, 2, figsize=(11.8, 4.5), constrained_layout=True)
    energy_axis, vector_axis = axes
    colors = plt.colormaps["viridis"](np.linspace(0.08, 0.9, len(grids)))
    floor = np.finfo(np.float64).eps

    for grid, color in zip(grids, colors, strict=True):
        fraction = [record["fractional_mode_index"] for record in grid["eigenpairs"]]
        energy_error = [
            record["relative_energy_error"] for record in grid["eigenpairs"]
        ]
        overlap_error = [
            max(record["nodal_overlap_defect"], floor) for record in grid["eigenpairs"]
        ]
        label = rf"$N={grid['interior_points']}$"
        energy_axis.semilogy(fraction, energy_error, "-", color=color, label=label)
        vector_axis.semilogy(fraction, overlap_error, ".", color=color, label=label)

    energy_axis.set(
        title="Eigenvalue dispersion across the spectrum",
        xlabel=r"fractional mode index $n/(N+1)$",
        ylabel="relative energy error",
    )
    vector_axis.set(
        title="Agreement with continuum sine at grid nodes",
        xlabel=r"fractional mode index $n/(N+1)$",
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
    point_counts = [grid["interior_points"] for grid in grids]
    fixed = payload["fixed_higher_mode_series"]
    fixed_modes = payload["input"]["grid_series"]["fixed_higher_modes"]
    colors = ["#0072B2", "#D55E00", "#009E73"]
    order_positions = {
        points: index for index, points in enumerate(point_counts[1:], start=1)
    }
    figure, axes = plt.subplots(1, 2, figsize=(11.5, 4.5), constrained_layout=True)
    error_axis, order_axis = axes

    for mode, color in zip(fixed_modes, colors, strict=True):
        record = fixed[str(mode)]
        spacings = np.asarray(record["spacings"], dtype=float)
        errors = np.asarray(record["relative_energy_errors"], dtype=float)
        orders = np.asarray(record["observed_orders"][1:], dtype=float)
        error_axis.loglog(spacings, errors, "o-", color=color, label=rf"$n={mode}$")
        order_axis.plot(
            [order_positions[points] for points in record["interior_points"][1:]],
            orders,
            "o-",
            color=color,
            label=rf"$n={mode}$",
        )

    reference_spacings = np.asarray([grid["spacing"] for grid in grids], dtype=float)
    reference = reference_spacings**2
    reference *= 0.8 * error_axis.get_ylim()[1] / reference[0]
    error_axis.loglog(
        reference_spacings, reference, "k--", alpha=0.65, label=r"$O(h^2)$"
    )
    error_axis.invert_xaxis()
    error_axis.set(
        title="Fixed higher-mode refinement",
        xlabel="grid spacing $h$",
        ylabel="relative energy error",
    )
    order_axis.axhline(2.0, color="black", linestyle="--", alpha=0.65)
    order_axis.set(
        title="Observed order between refinements",
        xlabel="interior points on finer grid",
        ylabel="observed order",
        xticks=list(order_positions.values()),
    )
    order_axis.set_xticklabels([str(points) for points in point_counts[1:]])
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
