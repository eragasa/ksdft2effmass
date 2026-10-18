"""Create publication-format plots for the exploratory flat-parent analysis."""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = Path(__file__).resolve().parent
PNG_OUTPUT = ANALYSIS / "band-equivalence-versus-hopping-locality.png"
PDF_OUTPUT = ANALYSIS / "band-equivalence-versus-hopping-locality.pdf"

BLUE = "#0072B2"
VERMILION = "#D55E00"
GREEN = "#009E73"
PURPLE = "#CC79A7"
BLACK = "#202020"


def _panel_label(axis: plt.Axes, label: str) -> None:
    """Place a journal-style panel label outside the upper-left corner."""
    axis.text(
        -0.13,
        1.04,
        label,
        transform=axis.transAxes,
        fontsize=9,
        fontweight="bold",
        va="bottom",
        ha="left",
    )


def main() -> int:
    """Create vector PDF and 600-dpi PNG versions of the five-panel figure."""
    threshold_data = np.genfromtxt(
        ROOT / "smooth-threshold-continuum.csv", delimiter=",", names=True
    )
    amplitude_data = np.genfromtxt(
        ANALYSIS / "amplitude-resolution.csv", delimiter=",", names=True
    )
    hopping_data = np.genfromtxt(
        ANALYSIS / "selected-hopping-tails.csv", delimiter=",", names=True
    )
    hopping_map_data = np.genfromtxt(
        ANALYSIS / "hopping-power-map.csv", delimiter=",", names=True
    )

    style = {
        "font.family": "DejaVu Sans",
        "font.size": 7.5,
        "axes.titlesize": 8.5,
        "axes.labelsize": 8,
        "axes.linewidth": 0.7,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "xtick.major.width": 0.7,
        "ytick.major.width": 0.7,
        "legend.fontsize": 6.5,
        "lines.linewidth": 1.4,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "savefig.transparent": False,
    }
    with mpl.rc_context(style):  # type: ignore[arg-type]
        figure = plt.figure(figsize=(7.2, 6.8), constrained_layout=True)
        grid = figure.add_gridspec(2, 6, height_ratios=(1.0, 1.08))
        axes = (
            figure.add_subplot(grid[0, 0:2]),
            figure.add_subplot(grid[0, 2:4]),
            figure.add_subplot(grid[0, 4:6]),
            figure.add_subplot(grid[1, 0:3]),
            figure.add_subplot(grid[1, 3:6]),
        )

        amplitude = np.asarray(threshold_data["a"], dtype=np.float64)
        axes[0].plot(
            amplitude,
            threshold_data["operator_threshold_over_sqrt_kappa"],
            color=BLUE,
            label="minimum operator",
        )
        axes[0].plot(
            amplitude,
            threshold_data["joint_threshold_over_sqrt_kappa"],
            color=VERMILION,
            linestyle="--",
            label="exact-spectrum joint",
        )
        axes[0].set_xticks(
            (0.0, math.pi / 8.0, math.pi / 4.0),
            ("0", r"$\pi/8$", r"$\pi/4$"),
        )
        axes[0].set_xlabel("rotation amplitude $a$")
        axes[0].set_ylabel(r"threshold$/\sqrt{\kappa}$")
        axes[0].set_title("Acceptance thresholds")
        axes[0].legend(frameon=False, loc="upper left")
        axes[0].grid(alpha=0.2, linewidth=0.5)
        _panel_label(axes[0], "(a)")

        intervals = np.asarray(amplitude_data["amplitude_intervals"], dtype=np.float64)
        axes[1].loglog(
            intervals,
            amplitude_data["maximum_operator_threshold_midpoint_interpolation_defect"],
            marker="o",
            markersize=3.2,
            color=BLUE,
            label="operator",
        )
        axes[1].loglog(
            intervals,
            amplitude_data["maximum_joint_threshold_midpoint_interpolation_defect"],
            marker="s",
            markersize=3.0,
            color=VERMILION,
            label="joint",
        )
        axes[1].axhline(
            1.01e-8,
            color="#555555",
            linestyle=":",
            linewidth=1.0,
            label=r"draft $1.01\times10^{-8}$",
        )
        axes[1].axvspan(8, 64, color="#999999", alpha=0.12)
        axes[1].set_xlabel("amplitude intervals $N_a$")
        axes[1].set_ylabel("midpoint interpolation defect")
        axes[1].set_title("Amplitude resolution")
        axes[1].legend(frameon=False, loc="upper right")
        axes[1].grid(which="both", alpha=0.2, linewidth=0.5)
        _panel_label(axes[1], "(b)")

        selected = (
            (math.pi / 8.0, r"$a=\pi/8$", GREEN, "o"),
            (math.pi / 4.0, r"$a=\pi/4$", PURPLE, "s"),
        )
        for value, label, color, marker in selected:
            mask = np.isclose(hopping_data["amplitude"], value, rtol=0.0, atol=1.0e-15)
            axes[2].semilogy(
                hopping_data["maximum_range"][mask],
                hopping_data["normalized_tail_weight"][mask],
                marker=marker,
                markersize=3.2,
                color=color,
                label=label,
            )
        axes[2].set_xlabel(r"retained range $R_{\max}$")
        axes[2].set_ylabel(r"weight outside $|R|\leq R_{\max}$")
        axes[2].set_title("Cumulative hopping tails")
        axes[2].legend(frameon=False, loc="upper right")
        axes[2].grid(which="both", alpha=0.2, linewidth=0.5)
        _panel_label(axes[2], "(c)")

        coordinate = np.linspace(-0.5, 0.5, 257, endpoint=False)
        axes[3].plot(
            coordinate,
            np.ones_like(coordinate),
            color=BLACK,
            linewidth=1.8,
            label="reference",
        )
        axes[3].plot(coordinate, -np.ones_like(coordinate), color=BLACK, linewidth=1.8)
        marker_coordinates = coordinate[::16]
        for value, label, color, marker in selected:
            theta = value * np.sin(2.0 * np.pi * marker_coordinates)
            cosine = np.cos(2.0 * theta)
            sine = np.sin(2.0 * theta)
            attacked = np.empty((marker_coordinates.size, 2, 2), dtype=np.float64)
            attacked[:, 0, 0] = cosine
            attacked[:, 0, 1] = -sine
            attacked[:, 1, 0] = -sine
            attacked[:, 1, 1] = -cosine
            bands = np.linalg.eigvalsh(attacked)
            axes[3].plot(
                marker_coordinates,
                bands[:, 0],
                linestyle="none",
                marker=marker,
                markerfacecolor="none",
                markeredgecolor=color,
                markeredgewidth=0.8,
                markersize=3.2,
                label=label,
            )
            axes[3].plot(
                marker_coordinates,
                bands[:, 1],
                linestyle="none",
                marker=marker,
                markerfacecolor="none",
                markeredgecolor=color,
                markeredgewidth=0.8,
                markersize=3.2,
            )
        axes[3].text(
            0.02,
            0.50,
            r"maximum defect $2.22\times10^{-16}$",
            transform=axes[3].transAxes,
            fontsize=7,
            va="center",
        )
        axes[3].set_xlabel("reduced coordinate $q$")
        axes[3].set_ylabel("normalized band energy")
        axes[3].set_title("Bloch bands")
        axes[3].set_ylim(-1.18, 1.18)
        axes[3].legend(frameon=False, ncol=3, loc="lower center")
        axes[3].grid(alpha=0.2, linewidth=0.5)
        _panel_label(axes[3], "(d)")

        map_amplitudes = np.unique(hopping_map_data["amplitude"])
        map_displacements = np.unique(hopping_map_data["absolute_displacement"])
        hopping_map = np.empty((map_displacements.size, map_amplitudes.size))
        for row_index, displacement in enumerate(map_displacements):
            mask = hopping_map_data["absolute_displacement"] == displacement
            hopping_map[row_index] = hopping_map_data["normalized_hopping_weight"][mask]
        color_mesh = axes[4].pcolormesh(
            map_amplitudes,
            map_displacements,
            hopping_map,
            shading="nearest",
            cmap="magma",
            norm=LogNorm(vmin=1.0e-16, vmax=float(np.max(hopping_map))),
            rasterized=True,
        )
        axes[4].set_xticks(
            (0.0, math.pi / 8.0, math.pi / 4.0),
            ("0", r"$\pi/8$", r"$\pi/4$"),
        )
        axes[4].set_xlabel("rotation amplitude $a$")
        axes[4].set_ylabel(r"absolute displacement $|R|$")
        axes[4].set_title("Range-resolved hopping weight")
        colorbar = figure.colorbar(color_mesh, ax=axes[4], pad=0.02, aspect=25)
        colorbar.set_label("normalized hopping weight", fontsize=8)
        colorbar.ax.tick_params(labelsize=7, width=0.7)
        _panel_label(axes[4], "(e)")

        metadata = {
            "Title": "Band Equivalence versus Hopping Locality",
            "Subject": "Exploratory flat-parent continuum analysis",
        }
        figure.savefig(PDF_OUTPUT, bbox_inches="tight", metadata=metadata)
        figure.savefig(PNG_OUTPUT, dpi=600, bbox_inches="tight", metadata=metadata)
        plt.close(figure)

    print(f"output={PDF_OUTPUT}")
    print(f"output={PNG_OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
