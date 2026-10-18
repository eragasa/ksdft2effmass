"""Plot the exploratory parent-dispersion and representation-amplitude study."""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

ANALYSIS = Path(__file__).resolve().parent
PDF_OUTPUT = ANALYSIS / "parent-family-robustness-exploratory.pdf"
PNG_OUTPUT = ANALYSIS / "parent-family-robustness-exploratory.png"
BLUE = "#0072B2"
VERMILION = "#D55E00"


def _panel_label(axis: plt.Axes, label: str) -> None:
    axis.text(
        -0.12,
        1.05,
        label,
        transform=axis.transAxes,
        fontsize=9,
        fontweight="bold",
        va="bottom",
    )


def _grid(data: np.ndarray, field: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    parent_scales = np.unique(data["parent_hopping_scale"])
    amplitudes = np.unique(data["amplitude"])
    values = np.empty((parent_scales.size, amplitudes.size))
    for row, scale in enumerate(parent_scales):
        mask = np.isclose(data["parent_hopping_scale"], scale, rtol=0.0, atol=1.0e-15)
        ordered = np.argsort(data["amplitude"][mask])
        values[row] = data[field][mask][ordered]
    return parent_scales, amplitudes, values


def _heatmap(
    figure: plt.Figure,
    axis: plt.Axes,
    parent_scales: np.ndarray,
    amplitudes: np.ndarray,
    values: np.ndarray,
    *,
    title: str,
    colorbar_label: str,
    cmap: str,
) -> None:
    image = axis.pcolormesh(
        amplitudes,
        parent_scales,
        values,
        shading="nearest",
        cmap=cmap,
    )
    axis.set_xticks(
        (0.0, math.pi / 8.0, math.pi / 4.0),
        ("0", r"$\pi/8$", r"$\pi/4$"),
    )
    axis.set_yticks((0.0, 0.25, 0.5, 0.75, 1.0))
    axis.set_xlabel("rotation amplitude $a$")
    axis.set_ylabel(r"parent hopping scale $\rho$")
    axis.set_title(title)
    colorbar = figure.colorbar(image, ax=axis, pad=0.02)
    colorbar.set_label(colorbar_label, fontsize=7)
    colorbar.ax.tick_params(labelsize=6.5)


def main() -> int:
    """Create a bounded visualization of the sampled two-parameter family."""
    continuum = np.genfromtxt(
        ANALYSIS / "parent-family-continuum.csv", delimiter=",", names=True
    )
    summary = np.genfromtxt(
        ANALYSIS / "parent-family-summary.csv", delimiter=",", names=True
    )
    parent_scales, amplitudes, correlation = _grid(continuum, "maximum_correlation")
    _, _, threshold = _grid(continuum, "minimum_operator_threshold_over_sqrt_kappa")
    _, _, excess_weight = _grid(continuum, "excess_nonzero_hopping_weight")
    style = {
        "font.family": "DejaVu Sans",
        "font.size": 7.5,
        "axes.titlesize": 8.5,
        "axes.labelsize": 8,
        "axes.linewidth": 0.7,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "legend.fontsize": 6.5,
        "lines.linewidth": 1.4,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
    with mpl.rc_context(style):  # type: ignore[arg-type]
        figure, axes = plt.subplots(2, 2, figsize=(7.2, 5.7), constrained_layout=True)
        flat_axes = axes.ravel()
        _heatmap(
            figure,
            flat_axes[0],
            parent_scales,
            amplitudes,
            correlation,
            title="Sampled restricted correlation",
            colorbar_label=r"$\mu_{N,\max}$",
            cmap="viridis",
        )
        _panel_label(flat_axes[0], "(a)")
        _heatmap(
            figure,
            flat_axes[1],
            parent_scales,
            amplitudes,
            threshold,
            title="Sampled normalized operator threshold",
            colorbar_label=r"$\epsilon_{\min}/\sqrt{\kappa}$",
            cmap="magma",
        )
        _panel_label(flat_axes[1], "(b)")
        _heatmap(
            figure,
            flat_axes[2],
            parent_scales,
            amplitudes,
            excess_weight,
            title="Sampled excess non-onsite weight",
            colorbar_label=r"$P_{>0}^{A}-P_{>0}^{H}$",
            cmap="cividis",
        )
        _panel_label(flat_axes[2], "(c)")

        scale = summary["parent_hopping_scale"]
        flat_axes[3].plot(
            scale,
            summary["minimum_sampled_external_gap"],
            color=BLUE,
            marker="o",
            markersize=3.5,
            label="sampled external gap",
        )
        flat_axes[3].set_xlabel(r"parent hopping scale $\rho$")
        flat_axes[3].set_ylabel(r"sampled gap ($E_G$)", color=BLUE)
        flat_axes[3].tick_params(axis="y", colors=BLUE)
        companion = flat_axes[3].twinx()
        reference_weight = np.asarray(
            [
                continuum["reference_nonzero_hopping_weight"][
                    np.isclose(
                        continuum["parent_hopping_scale"],
                        value,
                        rtol=0.0,
                        atol=1.0e-15,
                    )
                ][0]
                for value in scale
            ]
        )
        companion.plot(
            scale,
            reference_weight,
            color=VERMILION,
            marker="s",
            markersize=3.5,
            label="reference non-onsite weight",
        )
        companion.set_ylabel("reference non-onsite weight", color=VERMILION)
        companion.tick_params(axis="y", colors=VERMILION)
        flat_axes[3].set_title("Parent-family qualification channels")
        flat_axes[3].grid(alpha=0.2, linewidth=0.5)
        lines = flat_axes[3].lines + companion.lines
        flat_axes[3].legend(
            lines,
            [line.get_label() for line in lines],
            frameon=False,
            loc="center left",
        )
        _panel_label(flat_axes[3], "(d)")

        metadata = {
            "Title": "Exploratory robustness across a four-state parent family",
            "Subject": (
                "Finite sampling of parent dispersion and representation amplitude"
            ),
        }
        figure.savefig(PDF_OUTPUT, bbox_inches="tight", metadata=metadata)
        figure.savefig(PNG_OUTPUT, dpi=600, bbox_inches="tight", metadata=metadata)
        plt.close(figure)
    print(f"output={PDF_OUTPUT}")
    print(f"output={PNG_OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
