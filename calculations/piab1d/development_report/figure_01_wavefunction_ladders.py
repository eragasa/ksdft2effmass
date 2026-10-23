#!/usr/bin/env python3
"""Generate the continuum and finite PIAB1D wavefunction ladders."""

from __future__ import annotations

import json
from pathlib import Path
from typing import cast

import matplotlib.pyplot as plt
import numpy as np
from ksdft2effmass.model_systems.piab1d import Piab1dResultVerifier

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


def style_axis(axis: plt.Axes) -> None:
    """Apply the common journal-figure axis style."""
    axis.set_xlim(-0.04, 1.04)
    axis.set_xlabel(r"position $x/L$")
    axis.set_ylabel("energy")
    axis.spines[["top", "right"]].set_visible(False)


def continuum_ladder(output: Path) -> None:
    """Plot the first three continuum eigenfunctions around their energies."""
    coordinates = np.linspace(0.0, 1.0, 800)
    colors = ("#0072B2", "#D55E00", "#009E73")
    figure, axis = plt.subplots(figsize=(5.2, 5.0), constrained_layout=True)
    amplitude_scale = 2.4
    for mode, color in zip(range(1, 4), colors, strict=True):
        energy = 0.5 * np.pi**2 * mode**2
        wavefunction = np.sqrt(2.0) * np.sin(mode * np.pi * coordinates)
        axis.axhline(energy, color=color, linewidth=0.8, alpha=0.45)
        axis.plot(
            coordinates,
            energy + amplitude_scale * wavefunction,
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
    axis.axvline(0.0, color="black", linewidth=1.2)
    axis.axvline(1.0, color="black", linewidth=1.2)
    axis.set_title("Continuum eigenfunctions")
    style_axis(axis)
    figure.savefig(output, dpi=220)
    plt.close(figure)


def discrete_ladder(output: Path, result_path: Path) -> None:
    """Plot retained quadrature-normalized amplitudes from verified evidence."""
    payload = cast(
        dict[str, JsonValue],
        json.loads(result_path.read_text(encoding="utf-8")),
    )
    quadrature = cast(dict[str, JsonValue], payload["quadrature"])
    if quadrature.get("enabled") is not True:
        raise ValueError("the report requires enabled quadrature evidence")
    interval = np.asarray(quadrature["interval"], dtype=np.float64)
    spacing = float(cast(float, quadrature["spacing"]))
    node_indices = np.asarray(
        quadrature["interior_full_grid_indices"],
        dtype=np.float64,
    )
    coordinates = interval[0] + node_indices * spacing
    plotted_coordinates = np.concatenate(([interval[0]], coordinates, [interval[1]]))
    matrices = cast(dict[str, JsonValue], payload["matrices"])
    nodal_amplitudes = np.asarray(
        matrices["retained_nodal_amplitudes_quadrature_normalized"],
        dtype=np.float64,
    )
    spectra = cast(dict[str, JsonValue], payload["spectra"])
    energies = np.asarray(spectra["computed_discrete"], dtype=np.float64)
    total_points = node_indices.size + 2
    colors = ("#0072B2", "#D55E00", "#009E73")
    figure, axis = plt.subplots(figsize=(5.2, 5.0), constrained_layout=True)
    amplitude_scale = 2.4
    for mode, color in zip(range(1, 4), colors, strict=True):
        energy = float(energies[mode - 1])
        plotted_values = np.concatenate(([0.0], nodal_amplitudes[:, mode - 1], [0.0]))
        axis.axhline(energy, color=color, linewidth=0.8, alpha=0.45)
        axis.plot(
            plotted_coordinates,
            energy + amplitude_scale * plotted_values,
            color=color,
            linewidth=1.2,
            alpha=0.65,
        )
        axis.scatter(
            plotted_coordinates,
            energy + amplitude_scale * plotted_values,
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
    axis.set_title(rf"Finite-grid wavefunctions ($N={total_points}$)")
    style_axis(axis)
    figure.savefig(output, dpi=220)
    plt.close(figure)


def main() -> int:
    """Generate both Figure 1 panels beside the report source."""
    root = Path(__file__).resolve().parent
    repository_root = root.parents[2]
    result_path = root.parent / "result.json"
    Piab1dResultVerifier().execute(result_path, repository_root)
    continuum_ladder(root / "figure_01a_continuum_wavefunction_ladder.png")
    discrete_ladder(
        root / "figure_01b_discrete_wavefunction_ladder.png",
        result_path,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
