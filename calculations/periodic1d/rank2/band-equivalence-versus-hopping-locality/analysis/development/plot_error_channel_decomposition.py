"""Plot the four separated approximation channels in the truncation study."""

from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

DEVELOPMENT = Path(__file__).resolve().parent
CALCULATION = DEVELOPMENT.parents[1]
INPUTS = CALCULATION / "simulations" / "development" / "inputs"
RESULTS = CALCULATION / "simulations" / "development" / "results"
FIGURES = DEVELOPMENT / "figures"
INPUT = RESULTS / "truncation-consequences.csv"
OUTPUT = FIGURES / "truncation-error-channel-decomposition"
ENDPOINT = math.pi / 4.0
ERROR_FLOOR = 1.0e-16
POWER_FLOOR = 1.0e-34


def _rows() -> list[dict[str, float]]:
    with INPUT.open(encoding="utf-8", newline="") as stream:
        return [
            {name: float(value) for name, value in row.items()}
            for row in csv.DictReader(stream)
        ]


def _point_rows(
    rows: list[dict[str, float]], parent_scale: float
) -> list[dict[str, float]]:
    return sorted(
        (
            row
            for row in rows
            if math.isclose(row["parent_hopping_scale"], parent_scale)
            and int(row["maximum_range"]) == 0
        ),
        key=lambda row: row["amplitude"],
    )


def _endpoint_rows(
    rows: list[dict[str, float]], parent_scale: float
) -> list[dict[str, float]]:
    return sorted(
        (
            row
            for row in rows
            if math.isclose(row["parent_hopping_scale"], parent_scale)
            and math.isclose(row["amplitude"], ENDPOINT)
        ),
        key=lambda row: row["maximum_range"],
    )


def main() -> None:
    """Write a four-panel decomposition without combining scientific channels."""
    rows = _rows()
    scales = tuple(sorted({row["parent_hopping_scale"] for row in rows}))
    colors = plt.cm.viridis(np.linspace(0.05, 0.95, len(scales)))
    figure, axes = plt.subplots(
        2,
        2,
        figsize=(11.2, 8.0),
        constrained_layout=True,
    )

    reference_powers: list[float] = []
    for color, scale in zip(colors, scales, strict=True):
        selected = _point_rows(rows, scale)
        amplitudes = np.asarray([row["amplitude"] for row in selected])
        comparison_power = np.asarray(
            [row["comparison_nyquist_power"] for row in selected]
        )
        axes[0, 0].semilogy(
            amplitudes,
            np.maximum(comparison_power, POWER_FLOOR),
            "o-",
            color=color,
            markersize=3.0,
            linewidth=1.1,
            label=rf"$\rho={scale:g}$",
        )
        reference_powers.extend(row["reference_nyquist_power"] for row in selected)
    axes[0, 0].axhspan(
        min(reference_powers),
        max(reference_powers),
        color="0.35",
        alpha=0.22,
        label="reference span",
    )
    axes[0, 0].set_title("(a) centered-Nyquist conversion power")
    axes[0, 0].set_ylabel(r"$P_{\mathrm{Nyq}}/E_ref^2$")
    axes[0, 0].legend(frameon=False, fontsize=7, ncol=2)

    for color, scale in zip(colors, scales, strict=True):
        selected = _point_rows(rows, scale)
        axes[0, 1].semilogy(
            [row["amplitude"] for row in selected],
            np.maximum(
                [
                    row["comparison_maximum_interpolation_band_error"]
                    for row in selected
                ],
                ERROR_FLOOR,
            ),
            "o-",
            color=color,
            markersize=3.0,
            linewidth=1.1,
            label=rf"$\rho={scale:g}$",
        )
    axes[0, 1].set_title("(b) finite-interpolant spectral discrepancy")
    axes[0, 1].set_ylabel(r"maximum interpolation error / $E_{\mathrm{ref}}$")
    axes[0, 1].legend(frameon=False, fontsize=7, ncol=2)

    for color, scale in zip(colors, scales, strict=True):
        selected = _endpoint_rows(rows, scale)
        axes[1, 0].semilogy(
            [row["maximum_range"] for row in selected],
            np.maximum(
                [row["comparison_maximum_truncation_band_error"] for row in selected],
                ERROR_FLOOR,
            ),
            "o-",
            color=color,
            markersize=4.0,
            linewidth=1.2,
            label=rf"$\rho={scale:g}$",
        )
    axes[1, 0].set_title(r"(c) deliberate truncation, $a=\pi/4$")
    axes[1, 0].set_xlabel(r"cutoff $R_c$")
    axes[1, 0].set_ylabel(r"maximum truncation error / $E_{\mathrm{ref}}$")
    axes[1, 0].legend(frameon=False, fontsize=7, ncol=2)

    for color, scale in zip(colors, scales, strict=True):
        selected = _endpoint_rows(rows, scale)
        axes[1, 1].semilogy(
            [row["maximum_range"] for row in selected],
            np.maximum(
                [row["comparison_maximum_total_band_error"] for row in selected],
                ERROR_FLOOR,
            ),
            "o-",
            color=color,
            markersize=4.0,
            linewidth=1.2,
            label=rf"$\rho={scale:g}$",
        )
    endpoint = _endpoint_rows(rows, 1.0)
    interpolation_floor = max(
        row["comparison_maximum_interpolation_band_error"] for row in endpoint
    )
    axes[1, 1].axhline(
        interpolation_floor,
        linestyle="--",
        color="0.25",
        linewidth=1.0,
        label=r"$\rho=1$ interpolation discrepancy",
    )
    axes[1, 1].set_title(r"(d) total spectral consequence, $a=\pi/4$")
    axes[1, 1].set_xlabel(r"cutoff $R_c$")
    axes[1, 1].set_ylabel(r"maximum total band error / $E_{\mathrm{ref}}$")
    axes[1, 1].legend(frameon=False, fontsize=7, ncol=2)

    for axis in axes[0, :]:
        axis.set_xlabel(r"rotation amplitude $a$")
        axis.set_xticks((0.0, math.pi / 8.0, math.pi / 4.0))
        axis.set_xticklabels(("0", r"$\pi/8$", r"$\pi/4$"))
    for axis in axes.flat:
        axis.grid(alpha=0.22)
    figure.suptitle(
        "Separated conversion, interpolation, truncation, and total-error channels",
        fontsize=14,
    )
    figure.savefig(OUTPUT.with_suffix(".pdf"), bbox_inches="tight")
    figure.savefig(OUTPUT.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    main()
