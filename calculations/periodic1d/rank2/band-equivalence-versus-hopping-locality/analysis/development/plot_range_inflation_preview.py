"""Plot exploratory sampled cutoff inflation from the truncation analysis."""

from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from matplotlib.colors import BoundaryNorm

DEVELOPMENT = Path(__file__).resolve().parent
CALCULATION = DEVELOPMENT.parents[1]
INPUTS = CALCULATION / "simulations" / "development" / "inputs"
RESULTS = CALCULATION / "simulations" / "development" / "results"
FIGURES = DEVELOPMENT / "figures"
INPUT = RESULTS / "truncation-consequences.csv"
OUTPUT = FIGURES / "range-inflation-preview"
TARGETS = (1.0e-6, 1.0e-8, 1.0e-10, 1.0e-12)


def _rows() -> list[dict[str, float]]:
    with INPUT.open(encoding="utf-8", newline="") as stream:
        return [
            {name: float(value) for name, value in row.items()}
            for row in csv.DictReader(stream)
        ]


def _first_passing_cutoff(
    rows: list[dict[str, float]], channel: str, target: float
) -> int | None:
    for row in sorted(rows, key=lambda item: item["maximum_range"]):
        if row[channel] <= target:
            return int(row["maximum_range"])
    return None


def _inflation_grid(
    rows: list[dict[str, float]], target: float
) -> tuple[npt.NDArray[np.float64], tuple[float, ...], tuple[float, ...]]:
    grouped: defaultdict[tuple[float, float], list[dict[str, float]]] = defaultdict(
        list
    )
    for row in rows:
        grouped[(row["parent_hopping_scale"], row["amplitude"])].append(row)
    parent_scales = tuple(sorted({key[0] for key in grouped}))
    amplitudes = tuple(sorted({key[1] for key in grouped}))
    grid = np.empty((len(parent_scales), len(amplitudes)), dtype=np.float64)
    for parent_index, parent_scale in enumerate(parent_scales):
        for amplitude_index, amplitude in enumerate(amplitudes):
            group = grouped[(parent_scale, amplitude)]
            reference = _first_passing_cutoff(
                group, "reference_maximum_band_error", target
            )
            comparison = _first_passing_cutoff(
                group, "comparison_maximum_total_band_error", target
            )
            if reference is None or comparison is None:
                grid[parent_index, amplitude_index] = np.nan
            else:
                grid[parent_index, amplitude_index] = comparison - reference
    return grid, parent_scales, amplitudes


def _edges(values: tuple[float, ...]) -> npt.NDArray[np.float64]:
    array = np.asarray(values, dtype=np.float64)
    if array.size < 2:
        raise ValueError("at least two sampled values are required")
    midpoints = 0.5 * (array[:-1] + array[1:])
    return np.concatenate(
        (
            np.asarray([array[0] - 0.5 * (array[1] - array[0])]),
            midpoints,
            np.asarray([array[-1] + 0.5 * (array[-1] - array[-2])]),
        )
    )


def main() -> None:
    """Write four discrete maps of first-passing sampled-cutoff inflation."""
    rows = _rows()
    grids = tuple(_inflation_grid(rows, target) for target in TARGETS)
    maximum = int(max(float(np.nanmax(grid)) for grid, _, _ in grids))
    boundaries = np.arange(-0.5, maximum + 1.5, 1.0)
    normalization = BoundaryNorm(boundaries, ncolors=256)
    figure, axes = plt.subplots(
        2,
        2,
        figsize=(10.8, 7.8),
        sharex=True,
        sharey=True,
        constrained_layout=True,
    )
    image = None
    for axis, target, (grid, parent_scales, amplitudes) in zip(
        axes.flat, TARGETS, grids, strict=True
    ):
        normalized_amplitudes = tuple(4.0 * value / math.pi for value in amplitudes)
        image = axis.pcolormesh(
            _edges(normalized_amplitudes),
            _edges(parent_scales),
            grid,
            cmap="viridis",
            norm=normalization,
            shading="flat",
        )
        endpoint = int(grid[-1, -1])
        axis.text(
            0.97,
            0.93,
            rf"endpoint $\Delta\widehat{{R}}_c^\star={endpoint}$",
            transform=axis.transAxes,
            ha="right",
            va="top",
            color="black",
            fontsize=9,
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.82},
        )
        exponent = round(math.log10(target))
        axis.set_title(rf"sampled target $\tau=10^{{{exponent}}}$")
        axis.set_xticks((0.0, 0.5, 1.0), ("0", r"$\pi/8$", r"$\pi/4$"))
        axis.set_yticks(parent_scales)
        axis.grid(False)
    if image is None:
        raise RuntimeError("no range-inflation panels were constructed")
    for axis in axes[-1, :]:
        axis.set_xlabel(r"rotation amplitude $a$")
    for axis in axes[:, 0]:
        axis.set_ylabel(r"sampled parent scale $\rho$")
    colorbar = figure.colorbar(
        image,
        ax=axes,
        ticks=np.arange(0, maximum + 1, 2),
        shrink=0.94,
    )
    colorbar.set_label(
        r"additional range $\Delta\widehat{R}_c^\star$ "
        "(first sampled passing cutoff)"
    )
    figure.suptitle(
        "Exploratory sampled range inflation for equal band-error targets",
        fontsize=15,
    )
    figure.savefig(OUTPUT.with_suffix(".pdf"), bbox_inches="tight")
    figure.savefig(OUTPUT.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    main()
