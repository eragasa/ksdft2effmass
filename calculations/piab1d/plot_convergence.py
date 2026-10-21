#!/usr/bin/env python3
"""Plot retained particle-in-a-box grid-convergence series."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np


def plot_convergence(payload: dict[str, Any], output: Path) -> None:
    """Plot fixed-mode relative errors and observed refinement orders."""
    refinements = payload["refinements"]
    spacings = np.asarray([item["spacing"] for item in refinements], dtype=float)
    point_counts = np.asarray(
        [item["interior_points"] + 2 for item in refinements], dtype=int
    )
    order_modes = payload["input"]["grid_series"]["order_modes"]
    marker_interval = max(len(point_counts) // 12, 1)

    figure, axes = plt.subplots(1, 2, figsize=(11.5, 4.5), constrained_layout=True)
    error_axis, order_axis = axes
    colors = ["#0072B2", "#D55E00", "#009E73"]

    for mode, color in zip(order_modes, colors, strict=True):
        errors = np.asarray(
            [item["modes"][mode - 1]["relative_error"] for item in refinements],
            dtype=float,
        )
        orders = payload["observed_relative_error_orders"][str(mode)]
        error_axis.loglog(
            spacings,
            errors,
            "-",
            color=color,
            marker="o",
            markevery=marker_interval,
            markersize=4,
            label=rf"mode $n={mode}$",
        )
        order_axis.plot(
            point_counts[1:],
            np.asarray(orders[1:], dtype=float),
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
    figure.savefig(output, dpi=180)
    plt.close(figure)


def plot_mode_sweep(payload: dict[str, Any], output: Path) -> None:
    """Plot mode-wise relative errors for every retained grid refinement."""
    refinements = payload["refinements"]
    selected_indices = np.unique(
        np.linspace(0, len(refinements) - 1, 7, dtype=int)
    )
    selected = [refinements[index] for index in selected_indices]
    figure, axis = plt.subplots(figsize=(7.6, 4.8), constrained_layout=True)
    colors = plt.colormaps["viridis"](np.linspace(0.08, 0.9, len(selected)))
    for item, color in zip(selected, colors, strict=True):
        modes = [mode["mode"] for mode in item["modes"]]
        errors = [mode["relative_error"] for mode in item["modes"]]
        axis.semilogy(
            modes,
            errors,
            "o-",
            color=color,
            label=rf"$N={item['interior_points'] + 2}$",
        )
    axis.set(
        title="Error across mode index and grid resolution",
        xlabel="fixed continuum mode index $n$",
        ylabel="relative energy error",
        xticks=modes,
    )
    axis.grid(True, which="both", alpha=0.25)
    axis.legend(frameon=False, ncol=2)
    figure.savefig(output, dpi=180)
    plt.close(figure)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--convergence-output", type=Path, required=True)
    parser.add_argument("--mode-sweep-output", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.result.read_text(encoding="utf-8"))
    plot_convergence(payload, args.convergence_output)
    plot_mode_sweep(payload, args.mode_sweep_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
