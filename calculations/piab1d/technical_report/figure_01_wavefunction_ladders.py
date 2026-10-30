#!/usr/bin/env python3
"""Generate the continuum and finite PIAB1D wavefunction ladders."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ksdft2effmass.model_systems.piab1d import (
    Piab1dCalculationResult,
    Piab1dVerification,
)
from ksdft2effmass.serialization import TypedJsonValueCodec


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


def discrete_ladder(output: Path, result: Piab1dCalculationResult) -> None:
    """Plot retained quadrature-normalized amplitudes from verified evidence."""
    total_points = result.configuration.interior_points + 2
    spacing = result.configuration.length / (total_points - 1)
    coordinates = spacing * np.arange(1, total_points - 1, dtype=np.float64)
    plotted_coordinates = np.concatenate(
        ((0.0,), coordinates, (result.configuration.length,))
    )
    nodal_amplitudes = result.eigensystem.matrix("quadrature_normalized").magnitude[
        :, : result.configuration.retained_dimension
    ]
    energies = result.eigensystem.vector("computed_discrete").magnitude
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
    execution = root.parent / "executions" / "direct-core-n8-m3"
    result_bytes = (execution / "results" / "result.json").read_bytes()
    verification_document = TypedJsonValueCodec().deserialize_bytes(
        (execution / "verification" / "verification.json").read_bytes()
    )
    if not isinstance(verification_document, Mapping):
        raise TypeError("verification document must decode to a mapping")
    verification_value = verification_document.get("verification")
    if not isinstance(verification_value, Mapping):
        raise TypeError("verification aggregate must decode to a mapping")
    verification = Piab1dVerification.from_dict(verification_value)
    if not verification.passed:
        raise ValueError("the report requires passing typed verification")
    if verification.subject_sha256 != hashlib.sha256(result_bytes).hexdigest():
        raise ValueError("verification does not authenticate the direct result bytes")
    result = Piab1dCalculationResult.from_json(result_bytes)
    continuum_ladder(root / "figure_01a_continuum_wavefunction_ladder.png")
    discrete_ladder(
        root / "figure_01b_discrete_wavefunction_ladder.png",
        result,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
