"""Plot sampled finite-range band consequences."""

from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

CALCULATION = Path(__file__).resolve().parents[2]
RESULTS = CALCULATION / "simulations" / "development" / "results"
FIGURES = Path(__file__).resolve().parent / "figures"
INPUT = RESULTS / "truncation-consequences.csv"
OUTPUT = FIGURES / "truncation-band-consequences"
ENDPOINT = math.pi / 4.0
FLOOR = 1.0e-15


def _rows() -> list[dict[str, float]]:
    with INPUT.open(encoding="utf-8", newline="") as stream:
        return [
            {name: float(value) for name, value in row.items()}
            for row in csv.DictReader(stream)
        ]


def _endpoint(
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


def main() -> int:
    """Write a three-panel sampled range-versus-accuracy figure."""
    rows = _rows()
    scales = sorted({row["parent_hopping_scale"] for row in rows})
    figure, axes = plt.subplots(1, 3, figsize=(13.0, 4.1), constrained_layout=True)

    endpoint = _endpoint(rows, 1.0)
    ranges = np.asarray([row["maximum_range"] for row in endpoint])
    axes[0].semilogy(
        ranges,
        np.maximum([row["reference_maximum_band_error"] for row in endpoint], FLOOR),
        "o-",
        label="reference",
    )
    axes[0].semilogy(
        ranges,
        np.maximum(
            [row["comparison_maximum_total_band_error"] for row in endpoint], FLOOR
        ),
        "s-",
        label="rotated comparison",
    )
    axes[0].set_title(r"(a) $\rho=1$, $a=\pi/4$")
    axes[0].set_xlabel(r"cutoff $R_c$")
    axes[0].set_ylabel(r"maximum band error / $E_G$")
    axes[0].legend(frameon=False)

    colors = plt.cm.viridis(np.linspace(0.05, 0.95, len(scales)))
    for color, scale in zip(colors, scales, strict=True):
        selected = _endpoint(rows, scale)
        axes[1].semilogy(
            [row["maximum_range"] for row in selected],
            np.maximum(
                [row["comparison_maximum_total_band_error"] for row in selected],
                FLOOR,
            ),
            "o-",
            color=color,
            label=rf"$\rho={scale:g}$",
        )
    axes[1].set_title(r"(b) sampled parent homotopy, $a=\pi/4$")
    axes[1].set_xlabel(r"cutoff $R_c$")
    axes[1].set_ylabel(r"comparison total band error / $E_G$")
    axes[1].legend(frameon=False, fontsize=8)

    for color, scale in zip(colors, scales, strict=True):
        selected = _endpoint(rows, scale)
        axes[2].loglog(
            np.maximum(
                np.sqrt([row["comparison_total_omitted_power"] for row in selected]),
                FLOOR,
            ),
            np.maximum(
                [row["comparison_maximum_total_band_error"] for row in selected],
                FLOOR,
            ),
            "o-",
            color=color,
            label=rf"$\rho={scale:g}$",
        )
    guide = np.logspace(-14, 0, 128)
    axes[2].loglog(guide, guide, "--", color="0.45", linewidth=1.0, label=r"$y=x$")
    axes[2].set_title("(c) tail power versus spectral consequence")
    axes[2].set_xlabel(r"$\sqrt{P_{>R_c}}/E_G$")
    axes[2].set_ylabel(r"comparison total band error / $E_G$")
    axes[2].legend(frameon=False, fontsize=8)

    for axis in axes:
        axis.grid(alpha=0.22)
    figure.suptitle(
        "Pointwise finite-range consequences on the disjoint evaluation mesh",
        fontsize=12,
    )
    pdf_output = OUTPUT.with_suffix(".pdf")
    png_output = OUTPUT.with_suffix(".png")
    figure.savefig(pdf_output, bbox_inches="tight")
    figure.savefig(png_output, dpi=220, bbox_inches="tight")
    plt.close(figure)
    print(f"output={pdf_output}")
    print(f"output={png_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
