"""Create publication-format exploratory plots for the non-flat realization."""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

CALCULATION = Path(__file__).resolve().parents[2]
RESULTS = CALCULATION / "simulations" / "development" / "results"
FIGURES = Path(__file__).resolve().parent / "figures"
PDF_OUTPUT = FIGURES / "nonflat-four-state-exploratory.pdf"
PNG_OUTPUT = FIGURES / "nonflat-four-state-exploratory.png"
BLUE = "#0072B2"
VERMILION = "#D55E00"
GREEN = "#009E73"
PURPLE = "#CC79A7"
BLACK = "#202020"


def _panel_label(axis: plt.Axes, label: str) -> None:
    axis.text(
        -0.14,
        1.08,
        label,
        transform=axis.transAxes,
        fontsize=9,
        fontweight="bold",
        va="bottom",
    )


def _amplitude_ticks(axis: plt.Axes) -> None:
    axis.set_xticks(
        (0.0, math.pi / 8.0, math.pi / 4.0),
        ("0", r"$\pi/8$", r"$\pi/4$"),
    )


def main() -> int:
    """Plot the full non-flat amplitude family and unresolved controls."""
    continuum = np.genfromtxt(
        RESULTS / "nonflat-continuum.csv", delimiter=",", names=True
    )
    power_map = np.genfromtxt(
        RESULTS / "nonflat-hopping-power-map.csv", delimiter=",", names=True
    )
    tails = np.genfromtxt(
        RESULTS / "nonflat-selected-hopping-tails.csv", delimiter=",", names=True
    )
    momentum = np.genfromtxt(
        RESULTS / "nonflat-momentum-refinement.csv", delimiter=",", names=True
    )
    amplitude_resolution = np.genfromtxt(
        RESULTS / "nonflat-amplitude-resolution.csv", delimiter=",", names=True
    )
    style = {
        "font.family": "DejaVu Sans",
        "font.size": 7.3,
        "axes.titlesize": 8.3,
        "axes.labelsize": 7.7,
        "axes.linewidth": 0.7,
        "xtick.labelsize": 6.8,
        "ytick.labelsize": 6.8,
        "legend.fontsize": 6.2,
        "lines.linewidth": 1.35,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
    with mpl.rc_context(style):  # type: ignore[arg-type]
        figure, axes = plt.subplots(2, 3, figsize=(7.2, 5.15), constrained_layout=True)
        flat_axes = axes.ravel()
        amplitude = continuum["amplitude"]

        flat_axes[0].plot(
            amplitude,
            continuum["minimum_operator_threshold"],
            color=BLUE,
            marker="o",
            markevery=8,
            markersize=2.5,
            label="minimum operator",
        )
        flat_axes[0].plot(
            amplitude,
            continuum["exact_spectrum_joint_operator_threshold"],
            color=VERMILION,
            linestyle="--",
            marker="s",
            markevery=8,
            markersize=2.5,
            label="exact-spectrum joint",
        )
        _amplitude_ticks(flat_axes[0])
        flat_axes[0].set_xlabel("rotation amplitude $a$")
        flat_axes[0].set_ylabel("normalized threshold")
        flat_axes[0].set_title("Sampled thresholds")
        flat_axes[0].legend(frameon=False)
        flat_axes[0].grid(alpha=0.2, linewidth=0.5)
        _panel_label(flat_axes[0], "(a)")

        flat_axes[1].plot(
            amplitude,
            continuum["reference_nonzero_hopping_weight"],
            color=BLACK,
            linestyle=":",
            marker="^",
            markevery=8,
            markersize=2.5,
            label="reference",
        )
        flat_axes[1].plot(
            amplitude,
            continuum["comparison_nonzero_hopping_weight"],
            color=GREEN,
            marker="o",
            markevery=8,
            markersize=2.5,
            label="comparison",
        )
        _amplitude_ticks(flat_axes[1])
        flat_axes[1].set_xlabel("rotation amplitude $a$")
        flat_axes[1].set_ylabel("non-onsite weight")
        flat_axes[1].set_title("Sampled non-onsite weights")
        flat_axes[1].legend(frameon=False)
        flat_axes[1].grid(alpha=0.2, linewidth=0.5)
        _panel_label(flat_axes[1], "(b)")

        map_amplitudes = np.unique(power_map["amplitude"])
        map_ranges = np.unique(power_map["absolute_displacement"])
        comparison_grid = np.empty((map_ranges.size, map_amplitudes.size))
        for index, value in enumerate(map_amplitudes):
            mask = np.isclose(power_map["amplitude"], value, rtol=0.0, atol=1.0e-15)
            ordered = np.argsort(power_map["absolute_displacement"][mask])
            comparison_grid[:, index] = power_map[
                "comparison_normalized_hopping_weight"
            ][mask][ordered]
        image = flat_axes[2].pcolormesh(
            map_amplitudes,
            map_ranges,
            np.log10(np.maximum(comparison_grid, 1.0e-20)),
            shading="nearest",
            cmap="viridis",
            vmin=-18.0,
            vmax=0.0,
        )
        _amplitude_ticks(flat_axes[2])
        flat_axes[2].set_xlabel("rotation amplitude $a$")
        flat_axes[2].set_ylabel(r"absolute displacement $|R|$")
        flat_axes[2].set_title("Sampled range redistribution")
        colorbar = figure.colorbar(image, ax=flat_axes[2], pad=0.02)
        colorbar.set_label(r"$\log_{10}$ normalized weight", fontsize=7)
        colorbar.ax.tick_params(labelsize=6.5)
        _panel_label(flat_axes[2], "(c)")

        selected = (
            (0.0, "reference", BLACK, "^"),
            (math.pi / 8.0, r"comparison, $a=\pi/8$", GREEN, "o"),
            (math.pi / 4.0, r"comparison, $a=\pi/4$", PURPLE, "s"),
        )
        for value, label, color, marker in selected:
            mask = np.isclose(tails["amplitude"], value, rtol=0.0, atol=1.0e-15)
            field = (
                "reference_normalized_tail_weight"
                if value == 0.0
                else "comparison_normalized_tail_weight"
            )
            flat_axes[3].semilogy(
                tails["maximum_range"][mask],
                tails[field][mask],
                color=color,
                marker=marker,
                markersize=3.0,
                label=label,
            )
        flat_axes[3].set_xlabel(r"retained range $R_{\max}$")
        flat_axes[3].set_ylabel(r"weight outside $|R|\leq R_{\max}$")
        flat_axes[3].set_title("Selected cumulative tails")
        flat_axes[3].legend(frameon=False)
        flat_axes[3].grid(which="both", alpha=0.2, linewidth=0.5)
        _panel_label(flat_axes[3], "(d)")

        fine_mesh = momentum["fine_mesh_size"]
        physical_change = np.maximum.reduce(
            [
                momentum["maximum_correlation_change"],
                momentum["maximum_threshold_change"],
                momentum["maximum_hopping_weight_change"],
                momentum["maximum_hopping_block_power_change"],
            ]
        )
        flat_axes[4].loglog(
            fine_mesh,
            momentum["maximum_parent_diagnostic_change"],
            color=VERMILION,
            marker="s",
            markersize=3.0,
            label="largest parent-invariant change",
        )
        flat_axes[4].loglog(
            fine_mesh,
            physical_change,
            color=BLUE,
            marker="o",
            markersize=3.0,
            label="largest outcome change",
        )
        flat_axes[4].axhline(
            1.01e-8,
            color="#555555",
            linestyle=":",
            linewidth=1.0,
            label=r"draft $1.01\times10^{-8}$",
        )
        flat_axes[4].set_xticks(
            fine_mesh, tuple(str(int(value)) for value in fine_mesh)
        )
        flat_axes[4].xaxis.set_minor_locator(mpl.ticker.NullLocator())
        flat_axes[4].set_xlabel("fine momentum mesh $N$")
        flat_axes[4].set_ylabel("maximum refinement change")
        flat_axes[4].set_title("Momentum: converged")
        flat_axes[4].legend(frameon=False, loc="center right")
        flat_axes[4].grid(which="both", alpha=0.2, linewidth=0.5)
        _panel_label(flat_axes[4], "(e)")

        intervals = amplitude_resolution["amplitude_intervals"]
        amplitude_fields = (
            ("maximum_operator_threshold_midpoint_defect", BLUE, "operator"),
            ("maximum_joint_threshold_midpoint_defect", VERMILION, "joint"),
            (
                "maximum_hopping_block_power_midpoint_defect",
                PURPLE,
                "hopping block",
            ),
        )
        for field, color, label in amplitude_fields:
            flat_axes[5].loglog(
                intervals,
                amplitude_resolution[field],
                color=color,
                marker="o",
                markersize=3.0,
                label=label,
            )
        flat_axes[5].axhline(
            1.01e-8,
            color="#555555",
            linestyle=":",
            linewidth=1.0,
            label=r"draft $1.01\times10^{-8}$",
        )
        flat_axes[5].set_xticks(
            intervals, tuple(str(int(value)) for value in intervals)
        )
        flat_axes[5].xaxis.set_minor_locator(mpl.ticker.NullLocator())
        flat_axes[5].set_xlabel("amplitude intervals $N_a$")
        flat_axes[5].set_ylabel("maximum midpoint defect")
        flat_axes[5].set_title("Amplitude: unresolved")
        flat_axes[5].legend(frameon=False, loc="lower left")
        flat_axes[5].grid(which="both", alpha=0.2, linewidth=0.5)
        _panel_label(flat_axes[5], "(f)")

        metadata = {
            "Title": "Exploratory smooth non-flat four-state realization",
            "Subject": "Unresolved pre-version numerical analysis",
        }
        figure.savefig(PDF_OUTPUT, bbox_inches="tight", metadata=metadata)
        figure.savefig(PNG_OUTPUT, dpi=600, bbox_inches="tight", metadata=metadata)
        plt.close(figure)
    print(f"output={PDF_OUTPUT}")
    print(f"output={PNG_OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
