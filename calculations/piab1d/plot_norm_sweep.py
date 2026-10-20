#!/usr/bin/env python3
"""Plot retained multi-norm particle-in-a-box diagnostics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np


def plot_operator_norms(payload: dict[str, Any], output: Path) -> None:
    """Plot raw and same-grid-normalized operator residual norms."""
    grids = payload["grids"]
    points = np.asarray([grid["interior_points"] for grid in grids])
    residual_names = ["unmatched_compression", "boundary_realization"]
    residual_labels = {
        "unmatched_compression": "unmatched compression",
        "boundary_realization": "boundary realization",
    }
    colors = {"unmatched_compression": "#D55E00", "boundary_realization": "#0072B2"}
    norm_names = ["frobenius", "spectral", "maximum_entry"]
    norm_labels = {
        "frobenius": r"Frobenius $\|R\|_F/\|H\|_F$",
        "spectral": r"spectral $\|R\|_2/\|H\|_2$",
        "maximum_entry": r"maximum entry $\|R\|_{\max}/\|H\|_{\max}$",
    }

    figure, axes = plt.subplots(2, 2, figsize=(11.8, 8.0), constrained_layout=True)
    raw_axis = axes[0, 0]
    for name in residual_names:
        values = [
            grid["operator_residuals"][name]["raw"]["frobenius"] for grid in grids
        ]
        raw_axis.loglog(
            points,
            values,
            "o-",
            color=colors[name],
            label=residual_labels[name],
        )
    raw_axis.set(
        title="Raw Frobenius norms (not convergence metrics)",
        xlabel="interior points $N$",
        ylabel=r"$\|R\|_F$",
    )
    raw_axis.legend(frameon=False)

    for axis, norm_name in zip(axes.flat[1:], norm_names, strict=True):
        for name in residual_names:
            values = [
                grid["operator_residuals"][name]["relative_to_hamiltonian"][norm_name]
                for grid in grids
            ]
            axis.semilogx(
                points,
                values,
                "o-",
                color=colors[name],
                label=residual_labels[name],
            )
        axis.set(
            title=norm_labels[norm_name],
            xlabel="interior points $N$",
            ylabel="same-grid norm ratio",
            xticks=points,
        )
        axis.set_xticklabels([str(point) for point in points])
        axis.legend(frameon=False)

    for axis in axes.flat:
        axis.grid(True, which="both", alpha=0.25)
    figure.suptitle(
        "Operator residuals under different matrix norms",
        fontsize=15,
        fontweight="bold",
    )
    figure.savefig(output, dpi=180)
    plt.close(figure)


def plot_algebraic_norms(payload: dict[str, Any], output: Path) -> None:
    """Plot full-eigensystem algebraic residual ratios under three norms."""
    grids = payload["grids"]
    points = np.asarray([grid["interior_points"] for grid in grids])
    labels = {
        "frobenius": r"$\|HV-V\Lambda\|_F/\|H\|_F$",
        "spectral": r"$\|HV-V\Lambda\|_2/\|H\|_2$",
        "maximum_entry": r"$\|HV-V\Lambda\|_{\max}/\|H\|_{\max}$",
    }
    colors = ["#0072B2", "#D55E00", "#009E73"]
    figure, axis = plt.subplots(figsize=(8.0, 4.8), constrained_layout=True)
    for (norm_name, label), color in zip(labels.items(), colors, strict=True):
        values = [
            grid["full_eigenpair_algebraic_residual"]["relative_to_hamiltonian"][
                norm_name
            ]
            for grid in grids
        ]
        axis.loglog(points, values, "o-", color=color, label=label)
    axis.set(
        title="Discrete eigensolver residuals under multiple norms",
        xlabel="interior points $N$",
        ylabel="same-grid norm ratio",
        xticks=points,
    )
    axis.set_xticklabels([str(point) for point in points])
    axis.grid(True, which="both", alpha=0.25)
    axis.legend(frameon=False, loc="upper left")
    axis.text(
        0.50,
        0.05,
        "Solver diagnostic only—not continuum error",
        transform=axis.transAxes,
        fontsize=10,
    )
    figure.savefig(output, dpi=180)
    plt.close(figure)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--operator-output", type=Path, required=True)
    parser.add_argument("--algebraic-output", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.result.read_text(encoding="utf-8"))
    plot_operator_norms(payload, args.operator_output)
    plot_algebraic_norms(payload, args.algebraic_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
