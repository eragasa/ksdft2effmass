#!/usr/bin/env python3
"""Plot the retained particle-in-a-box experiment result."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from matplotlib.colors import TwoSlopeNorm

RealMatrix = npt.NDArray[np.float64]


def _matrix(payload: dict[str, Any], name: str) -> RealMatrix:
    return np.asarray(payload["matrices"][name], dtype=np.float64)


def _residual(payload: dict[str, Any], name: str) -> RealMatrix:
    return np.asarray(payload["residuals"][name]["matrix"], dtype=np.float64)


def plot_summary(payload: dict[str, Any], output: Path) -> None:
    """Write a summary graphic for the retained result."""
    parameters = payload["input"]["dimensionless_parameters"]
    points = int(parameters["interior_points"])
    retained = int(parameters["retained_dimension"])
    length = float(parameters["length"])

    positions = np.linspace(0.0, length, points + 2)
    vectors = _matrix(payload, "retained_eigenvectors")
    discrete = np.asarray(payload["spectra"]["computed_discrete"], dtype=np.float64)
    continuum = np.asarray(
        payload["spectra"]["continuum_closed_form"], dtype=np.float64
    )
    levels = np.arange(1, points + 1)

    figure, axes = plt.subplots(1, 2, figsize=(11.5, 4.4), constrained_layout=True)

    state_axis = axes[0]
    for index in range(retained):
        state = np.zeros(points + 2)
        state[1:-1] = vectors[:, index]
        sign = 1.0 if state[1] >= 0.0 else -1.0
        state_axis.plot(
            positions,
            sign * state,
            marker="o",
            label=rf"$n={index + 1}$, $E={discrete[index]:.3f}$",
        )
    state_axis.axhline(0.0, color="0.75", linewidth=0.8)
    state_axis.set(
        title="Three retained discrete eigenstates",
        xlabel=rf"position $x$ ($L={length:g}$)",
        ylabel="grid-normalized amplitude",
    )
    state_axis.legend(frameon=False)

    spectrum_axis = axes[1]
    spectrum_axis.plot(
        levels,
        continuum,
        "o--",
        color="#777777",
        label="continuum closed form",
    )
    spectrum_axis.plot(
        levels,
        discrete,
        "o-",
        color="#0072B2",
        label="finite difference",
    )
    spectrum_axis.axvspan(0.5, retained + 0.5, color="#009E73", alpha=0.12)
    spectrum_axis.text(
        0.04,
        0.92,
        f"retained: n = 1…{retained}",
        transform=spectrum_axis.transAxes,
        color="#006B50",
    )
    spectrum_axis.set(
        title="Discrete and continuum energy levels",
        xlabel="level index $n$",
        ylabel="dimensionless energy",
        xticks=levels,
    )
    spectrum_axis.legend(frameon=False)

    figure.suptitle(
        "Particle-in-a-box illustrative experiment",
        fontsize=14,
        fontweight="bold",
    )
    figure.savefig(output, dpi=180)
    plt.close(figure)


def plot_residuals(payload: dict[str, Any], output: Path) -> None:
    """Write heat maps of the three residual constructions."""
    residuals = [
        _residual(payload, "consistently_compressed_physical_potential"),
        _residual(payload, "projected_hamiltonian_minus_unprojected_kinetic"),
        _residual(payload, "dirichlet_minus_cyclic_reference"),
    ]
    titles = [
        "Consistent compression\n$P H P - P T P$",
        "Unmatched compression\n$P H P - T$",
        "Boundary realization\n$H_{D} - H_{cyclic}$",
    ]

    figure, axes = plt.subplots(1, 3, figsize=(12.5, 4.1), constrained_layout=True)
    for axis, matrix, title in zip(axes, residuals, titles, strict=True):
        maximum = float(np.max(np.abs(matrix)))
        if maximum == 0.0:
            maximum = 1.0
        image = axis.imshow(
            matrix,
            cmap="RdBu_r",
            norm=TwoSlopeNorm(vmin=-maximum, vcenter=0.0, vmax=maximum),
            interpolation="nearest",
        )
        norm = float(np.linalg.norm(matrix, ord="fro"))
        axis.set(
            title=rf"{title}" + "\n" + rf"$\|R\|_F={norm:.3f}$",
            xlabel="column index",
            ylabel="row index",
            xticks=np.arange(matrix.shape[1]),
            yticks=np.arange(matrix.shape[0]),
        )
        colorbar = figure.colorbar(image, ax=axis, shrink=0.78)
        colorbar.ax.set_ylabel("matrix value", rotation=270, labelpad=13)

    figure.suptitle(
        "Different subtractions produce different residual operators",
        fontsize=14,
        fontweight="bold",
    )
    figure.savefig(output, dpi=180)
    plt.close(figure)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--summary-output", type=Path, required=True)
    parser.add_argument("--residual-output", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.result.read_text(encoding="utf-8"))
    plot_summary(payload, args.summary_output)
    plot_residuals(payload, args.residual_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
