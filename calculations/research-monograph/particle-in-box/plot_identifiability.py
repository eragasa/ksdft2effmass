#!/usr/bin/env python3
"""Plot the retained-space model-class identifiability demonstration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm


def plot_identifiability(payload: dict[str, Any], output: Path) -> None:
    """Plot the illustrative shift and unexplained model-class residuals."""
    shift = np.asarray(payload["illustrative_shift"], dtype=np.float64)
    fits = payload["model_class_fits"]
    class_names = payload["input"]["admissible_model_classes"]
    labels = ["scalar", "diagonal", "tridiagonal", "arbitrary\nHermitian"]
    values = [fits[name]["unexplained_frobenius_norm"] for name in class_names]

    figure, axes = plt.subplots(1, 2, figsize=(10.8, 4.4), constrained_layout=True)
    matrix_axis, fit_axis = axes
    maximum = float(np.max(np.abs(shift)))
    image = matrix_axis.imshow(
        shift,
        cmap="RdBu_r",
        norm=TwoSlopeNorm(vmin=-maximum, vcenter=0.0, vmax=maximum),
        interpolation="nearest",
    )
    matrix_axis.set(
        title="Illustrative decomposition shift $K$",
        xlabel="retained-coordinate column",
        ylabel="retained-coordinate row",
        xticks=np.arange(shift.shape[1]),
        yticks=np.arange(shift.shape[0]),
    )
    figure.colorbar(image, ax=matrix_axis, shrink=0.82)

    bars = fit_axis.bar(
        labels, values, color=["#CC79A7", "#E69F00", "#56B4E9", "#009E73"]
    )
    fit_axis.set(
        title="Unexplained residual after model-class fit",
        xlabel="admissible model class",
        ylabel=r"$\|K-V_{\mathcal{M}}^{\star}\|_F$",
    )
    fit_axis.grid(True, axis="y", alpha=0.25)
    for bar, value in zip(bars, values, strict=True):
        fit_axis.text(
            bar.get_x() + bar.get_width() / 2.0,
            value + 0.025 * max(values),
            f"{value:.3f}",
            ha="center",
            va="bottom",
        )
    fit_axis.text(
        0.98,
        0.75,
        "Illustrative fit—not a physical potential",
        transform=fit_axis.transAxes,
        ha="right",
        va="top",
        fontsize=9,
    )

    figure.suptitle(
        "Reduced Hamiltonian decomposition is not identifiable without a model class",
        fontsize=13,
        fontweight="bold",
    )
    figure.savefig(output, dpi=180)
    plt.close(figure)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.result.read_text(encoding="utf-8"))
    plot_identifiability(payload, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
