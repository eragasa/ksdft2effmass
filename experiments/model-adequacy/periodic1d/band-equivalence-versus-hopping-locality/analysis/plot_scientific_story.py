"""Plot the main scientific story across the sampled parent family."""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

ANALYSIS = Path(__file__).resolve().parent
PDF_OUTPUT = ANALYSIS / "band-equivalence-locality-scientific-story.pdf"
PNG_OUTPUT = ANALYSIS / "band-equivalence-locality-scientific-story.png"
BLACK = "#202020"


def _panel_label(axis: plt.Axes, label: str) -> None:
    axis.text(
        -0.13,
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


def _family_rows(data: np.ndarray, scale: float) -> np.ndarray:
    mask = np.isclose(data["parent_hopping_scale"], scale, rtol=0.0, atol=1.0e-15)
    return data[mask][np.argsort(data["amplitude"][mask])]


def main() -> int:
    """Create the sampled theorem-to-robustness comparison figure."""
    family = np.genfromtxt(
        ANALYSIS / "parent-family-continuum.csv", delimiter=",", names=True
    )
    analytic = np.genfromtxt(
        ANALYSIS.parent / "smooth-threshold-continuum.csv",
        delimiter=",",
        names=True,
    )
    tails = np.genfromtxt(
        ANALYSIS / "nonflat-selected-hopping-tails.csv", delimiter=",", names=True
    )
    scales = np.unique(family["parent_hopping_scale"])
    colors = plt.get_cmap("viridis")(np.linspace(0.08, 0.92, scales.size))
    style = {
        "font.family": "DejaVu Sans",
        "font.size": 7.2,
        "axes.titlesize": 8.2,
        "axes.labelsize": 7.7,
        "axes.linewidth": 0.7,
        "xtick.labelsize": 6.8,
        "ytick.labelsize": 6.8,
        "legend.fontsize": 5.9,
        "lines.linewidth": 1.3,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
    with mpl.rc_context(style):  # type: ignore[arg-type]
        figure, axes = plt.subplots(2, 3, figsize=(7.2, 5.15), constrained_layout=True)
        flat_axes = axes.ravel()

        for scale, color in zip(scales, colors, strict=True):
            rows = _family_rows(family, float(scale))
            label = rf"$\rho={scale:g}$"
            flat_axes[0].semilogy(
                rows["amplitude"],
                np.maximum(rows["maximum_band_defect"], 1.0e-18),
                color=color,
                marker="o",
                markevery=4,
                markersize=2.2,
                label=label,
            )
        _amplitude_ticks(flat_axes[0])
        flat_axes[0].set_xlabel("rotation amplitude $a$")
        flat_axes[0].set_ylabel("maximum band defect")
        flat_axes[0].set_title("Band blindness")
        flat_axes[0].legend(frameon=False, ncol=2)
        flat_axes[0].grid(which="both", alpha=0.2, linewidth=0.5)
        _panel_label(flat_axes[0], "(a)")

        flat_axes[1].plot(
            analytic["a"],
            analytic["operator_threshold_over_sqrt_kappa"],
            color=BLACK,
            linestyle="--",
            linewidth=1.0,
            label="flat analytic",
        )
        for scale, color in zip(scales, colors, strict=True):
            rows = _family_rows(family, float(scale))
            flat_axes[1].plot(
                rows["amplitude"],
                rows["minimum_operator_threshold_over_sqrt_kappa"],
                color=color,
                marker="o",
                markevery=4,
                markersize=2.2,
                label=rf"$\rho={scale:g}$",
            )
        _amplitude_ticks(flat_axes[1])
        flat_axes[1].set_xlabel("rotation amplitude $a$")
        flat_axes[1].set_ylabel(r"$\epsilon_{\min}/\sqrt{\kappa}$")
        flat_axes[1].set_title("Restricted mismatch")
        flat_axes[1].grid(alpha=0.2, linewidth=0.5)
        _panel_label(flat_axes[1], "(b)")

        flat_axes[2].plot(
            analytic["a"],
            analytic["operator_threshold_over_sqrt_kappa"] ** 2,
            color=BLACK,
            linestyle="--",
            linewidth=1.0,
            label="flat analytic identity",
        )
        for scale, color in zip(scales, colors, strict=True):
            rows = _family_rows(family, float(scale))
            flat_axes[2].plot(
                rows["amplitude"],
                rows["normalized_excess_nonzero_hopping_weight"],
                color=color,
                marker="o",
                markevery=4,
                markersize=2.2,
                label=rf"$\rho={scale:g}$",
            )
        _amplitude_ticks(flat_axes[2])
        flat_axes[2].set_xlabel("rotation amplitude $a$")
        flat_axes[2].set_ylabel(r"$(P_{>0}^{A}-P_{>0}^{H})/\kappa$")
        flat_axes[2].set_title("Excess hopping")
        flat_axes[2].grid(alpha=0.2, linewidth=0.5)
        _panel_label(flat_axes[2], "(c)")

        diagonal = np.linspace(0.0, 0.8, 101)
        flat_axes[3].plot(
            diagonal,
            diagonal,
            color=BLACK,
            linestyle="--",
            linewidth=1.0,
            label="flat identity $y=x$",
        )
        for scale, color in zip(scales, colors, strict=True):
            rows = _family_rows(family, float(scale))
            flat_axes[3].plot(
                rows["normalized_squared_operator_residual"],
                rows["normalized_excess_nonzero_hopping_weight"],
                color=color,
                marker="o",
                markevery=4,
                markersize=2.2,
                label="_nolegend_",
            )
        flat_axes[3].set_xlabel(r"$x=\epsilon_{\min}^2/\kappa$")
        flat_axes[3].set_ylabel(r"$y=(P_{>0}^{A}-P_{>0}^{H})/\kappa$")
        flat_axes[3].set_title("Residual--locality relation")
        flat_axes[3].legend(frameon=False, loc="upper left")
        flat_axes[3].grid(alpha=0.2, linewidth=0.5)
        _panel_label(flat_axes[3], "(d)")

        amplitudes = np.unique(family["amplitude"])
        departure = np.empty((scales.size, amplitudes.size))
        for row_index, scale in enumerate(scales):
            rows = _family_rows(family, float(scale))
            departure[row_index] = rows["flat_identity_departure"]
        image = flat_axes[4].pcolormesh(
            amplitudes,
            scales,
            departure,
            shading="nearest",
            cmap="magma",
            vmin=float(np.min(departure)),
            vmax=0.0,
        )
        _amplitude_ticks(flat_axes[4])
        flat_axes[4].set_yticks(scales)
        flat_axes[4].set_xlabel("rotation amplitude $a$")
        flat_axes[4].set_ylabel(r"parent hopping scale $\rho$")
        flat_axes[4].set_title("Departure from flat identity")
        colorbar = figure.colorbar(image, ax=flat_axes[4], pad=0.02)
        colorbar.set_label("normalized departure", fontsize=7)
        colorbar.ax.tick_params(labelsize=6.3)
        _panel_label(flat_axes[4], "(e)")

        selected = (
            (0.0, "reference", BLACK, "^"),
            (math.pi / 8.0, r"comparison, $a=\pi/8$", colors[2], "o"),
            (math.pi / 4.0, r"comparison, $a=\pi/4$", colors[-1], "s"),
        )
        for value, label, color, marker in selected:
            mask = np.isclose(tails["amplitude"], value, rtol=0.0, atol=1.0e-15)
            field = (
                "reference_normalized_tail_weight"
                if value == 0.0
                else "comparison_normalized_tail_weight"
            )
            flat_axes[5].semilogy(
                tails["maximum_range"][mask],
                tails[field][mask],
                color=color,
                marker=marker,
                markersize=2.8,
                label=label,
            )
        flat_axes[5].set_xlabel(r"retained range $R_{\max}$")
        flat_axes[5].set_ylabel(r"weight outside $|R|\leq R_{\max}$")
        flat_axes[5].set_title(r"Full-parent tails ($\rho=1$)")
        flat_axes[5].legend(frameon=False)
        flat_axes[5].grid(which="both", alpha=0.2, linewidth=0.5)
        _panel_label(flat_axes[5], "(f)")

        metadata = {
            "Title": "Band equivalence and locality across a parent family",
            "Subject": "Sampled theorem-to-robustness comparison",
        }
        figure.savefig(PDF_OUTPUT, bbox_inches="tight", metadata=metadata)
        figure.savefig(PNG_OUTPUT, dpi=600, bbox_inches="tight", metadata=metadata)
        plt.close(figure)
    print(f"output={PDF_OUTPUT}")
    print(f"output={PNG_OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
