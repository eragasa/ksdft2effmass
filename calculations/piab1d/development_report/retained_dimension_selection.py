"""Reproduce the retained-dimension calculation reported in the PIAB1D tutorial."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import cast

import matplotlib.pyplot as plt
import numpy as np

TOTAL_POINTS = 10
BETA = 0.1
OMITTED_PROBABILITY_TOLERANCE = 0.01


def represented_energy(mode: int, total_points: int) -> float:
    """Return the nondimensional centered-difference box energy."""
    spacing = 1.0 / (total_points - 1)
    return (
        2.0
        / spacing**2
        * math.sin(mode * math.pi / (2.0 * (total_points - 1))) ** 2
    )


def calculate_selection() -> dict[str, object]:
    """Return canonical weights and the first dimension meeting the tolerance."""
    energies = [
        represented_energy(mode, TOTAL_POINTS)
        for mode in range(1, TOTAL_POINTS - 1)
    ]
    boltzmann_factors = [math.exp(-BETA * energy) for energy in energies]
    partition_function = math.fsum(boltzmann_factors)

    candidates: list[dict[str, float | int | bool]] = []
    selected_dimension: int | None = None
    for retained_dimension in range(1, TOTAL_POINTS - 1):
        omitted_probability = (
            math.fsum(boltzmann_factors[retained_dimension:])
            / partition_function
        )
        passes = omitted_probability <= OMITTED_PROBABILITY_TOLERANCE
        candidates.append(
            {
                "retained_dimension": retained_dimension,
                "omitted_probability": omitted_probability,
                "passes": passes,
            }
        )
        if passes and selected_dimension is None:
            selected_dimension = retained_dimension

    if selected_dimension is None:
        raise RuntimeError("no retained dimension satisfies the declared tolerance")

    return {
        "beta": BETA,
        "candidates": candidates,
        "omitted_probability_tolerance": OMITTED_PROBABILITY_TOLERANCE,
        "partition_function": partition_function,
        "selected_dimension": selected_dimension,
        "total_points": TOTAL_POINTS,
    }


def plot_selection(payload: dict[str, object], output: Path) -> None:
    """Plot omitted canonical probability and the selected retained dimension."""
    candidates = payload["candidates"]
    if not isinstance(candidates, list):
        raise TypeError("candidates must be a list")
    candidate_records = cast(list[dict[str, float | int | bool]], candidates)
    selected_dimension = payload["selected_dimension"]
    tolerance = payload["omitted_probability_tolerance"]
    if not isinstance(selected_dimension, int):
        raise TypeError("selected_dimension must be an integer")
    if not isinstance(tolerance, float):
        raise TypeError("omitted_probability_tolerance must be a float")

    dimensions = np.asarray(
        [candidate["retained_dimension"] for candidate in candidate_records], dtype=int
    )
    omitted = np.asarray(
        [candidate["omitted_probability"] for candidate in candidate_records],
        dtype=float,
    )
    tolerance_axis = np.logspace(-8.0, math.log10(0.35), 2000)
    required_dimensions = np.asarray(
        [
            dimensions[np.flatnonzero(omitted <= candidate_tolerance)[0]]
            for candidate_tolerance in tolerance_axis
        ],
        dtype=int,
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
        rf"$\tau={tolerance:.2f}\;\Longrightarrow\;M_\star={selected_dimension}$",
        xy=(tolerance, selected_dimension),
        xytext=(tolerance * 2.0, selected_dimension + 0.65),
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
    figure.savefig(output, dpi=180)
    plt.close(figure)


def main() -> None:
    """Print the calculation and optionally write its tutorial figure."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--plot-output", type=Path)
    args = parser.parse_args()

    payload = calculate_selection()
    if args.plot_output is not None:
        plot_selection(payload, args.plot_output)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
