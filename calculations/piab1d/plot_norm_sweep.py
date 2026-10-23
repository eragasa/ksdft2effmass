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
    points = np.asarray([grid["interior_points"] + 2 for grid in grids])
    marker_interval = max(len(points) // 12, 1)
    residual_names = ["unmatched_compression", "boundary_realization"]
    residual_labels = {
        "unmatched_compression": "unmatched compression",
        "boundary_realization": "boundary realization",
    }
    colors = {"unmatched_compression": "#D55E00", "boundary_realization": "#0072B2"}
    norm_names = ["frobenius", "spectral", "maximum_entry"]
    norm_labels = {
        "frobenius": r"Frobenius $\|\mathsf{R}\|_F/\|\mathsf{H}\|_F$",
        "spectral": r"spectral $\|\mathsf{R}\|_2/\|\mathsf{H}\|_2$",
        "maximum_entry": (
            r"maximum entry $\|\mathsf{R}\|_{\max}/\|\mathsf{H}\|_{\max}$"
        ),
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
            "-",
            color=colors[name],
            marker="o",
            markevery=marker_interval,
            markersize=4,
            label=residual_labels[name],
        )
    raw_axis.set(
        title="Raw Frobenius norms (not convergence metrics)",
        xlabel=r"closed-interval grid points $N$",
        ylabel=r"$\|\mathsf{R}\|_F$",
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
                "-",
                color=colors[name],
                marker="o",
                markevery=marker_interval,
                markersize=4,
                label=residual_labels[name],
            )
        axis.set(
            title=norm_labels[norm_name],
            xlabel=r"closed-interval grid points $N$",
            ylabel="same-grid norm ratio",
        )
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
    points = np.asarray([grid["interior_points"] + 2 for grid in grids])
    marker_interval = max(len(points) // 12, 1)
    labels = {
        "frobenius": (
            r"$\|\mathsf{H}\mathsf{U}-\mathsf{U}\mathsf{D}\|_F/"
            r"\|\mathsf{H}\|_F$"
        ),
        "spectral": (
            r"$\|\mathsf{H}\mathsf{U}-\mathsf{U}\mathsf{D}\|_2/"
            r"\|\mathsf{H}\|_2$"
        ),
        "maximum_entry": (
            r"$\|\mathsf{H}\mathsf{U}-\mathsf{U}\mathsf{D}\|_{\max}/"
            r"\|\mathsf{H}\|_{\max}$"
        ),
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
        axis.loglog(
            points,
            values,
            "-",
            color=color,
            marker="o",
            markevery=marker_interval,
            markersize=4,
            label=label,
        )
    axis.set(
        title="Discrete eigensolver residuals under multiple norms",
        xlabel=r"closed-interval grid points $N$",
        ylabel="same-grid norm ratio",
    )
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


def plot_finite_identity_diagnostics(payload: dict[str, Any], output: Path) -> None:
    """Plot the six finite-identity diagnostics defined in the report."""
    grids = payload["grids"]
    points = np.asarray([grid["interior_points"] + 2 for grid in grids])
    panels = (
        (
            "Spectral consistency",
            "energy-valued diagnostic",
            (
                (
                    "discrete_spectrum_maximum_absolute_error",
                    r"$\delta_E$",
                    "#0072B2",
                ),
                (
                    "spectral_reconstruction_frobenius_error",
                    r"$\delta_{\mathrm{rec}}$",
                    "#D55E00",
                ),
            ),
        ),
        (
            "Retained-operator identities",
            "energy-valued diagnostic",
            (
                (
                    "retained_coordinate_frobenius_error",
                    r"$\delta_{\mathrm{coord}}$",
                    "#009E73",
                ),
                (
                    "retained_embedding_frobenius_error",
                    r"$\delta_{\mathrm{embed}}$",
                    "#CC79A7",
                ),
                (
                    "spectral_leakage_frobenius_norm",
                    r"$\delta_{\mathrm{leak}}$",
                    "#E69F00",
                ),
            ),
        ),
        (
            "Projector identity",
            "dimensionless diagnostic",
            (
                (
                    "projector_idempotency_frobenius_error",
                    r"$\delta_{\mathrm{idem}}$",
                    "#56B4E9",
                ),
            ),
        ),
    )
    figure, axes = plt.subplots(3, 1, figsize=(8.2, 9.2), constrained_layout=True)
    for axis, (title, ylabel, series) in zip(axes, panels, strict=True):
        for key, label, color in series:
            values = np.asarray(
                [grid["finite_identity_diagnostics"][key] for grid in grids]
            )
            axis.loglog(points, values, color=color, linewidth=1.8, label=label)
        axis.set(
            title=title,
            xlabel=r"closed-interval grid points $N$",
            ylabel=ylabel,
        )
        axis.grid(True, which="both", alpha=0.25)
        axis.legend(frameon=False)
    figure.suptitle(
        "Finite spectral and reduction diagnostics",
        fontsize=15,
        fontweight="bold",
    )
    figure.savefig(output, dpi=180)
    plt.close(figure)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--operator-output", type=Path, required=True)
    parser.add_argument("--algebraic-output", type=Path, required=True)
    parser.add_argument("--identity-output", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.result.read_text(encoding="utf-8"))
    plot_operator_norms(payload, args.operator_output)
    plot_algebraic_norms(payload, args.algebraic_output)
    plot_finite_identity_diagnostics(payload, args.identity_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
