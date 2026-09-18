#!/usr/bin/env python3
"""Plot composite-band gauge, localization, and hopping diagnostics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import cast

import matplotlib.pyplot as plt
import numpy as np

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


def mapping(value: JsonValue) -> dict[str, JsonValue]:
    if not isinstance(value, dict):
        raise TypeError("expected object")
    return value


def records(value: JsonValue) -> list[dict[str, JsonValue]]:
    if not isinstance(value, list):
        raise TypeError("expected array")
    return [mapping(item) for item in value]


def real(value: JsonValue) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise TypeError("expected number")
    return float(value)


def integer(value: JsonValue) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("expected integer")
    return value


def nested_reals(value: JsonValue) -> list[list[float]]:
    if not isinstance(value, list):
        raise TypeError("expected nested array")
    result: list[list[float]] = []
    for row in value:
        if not isinstance(row, list):
            raise TypeError("expected row")
        result.append([real(item) for item in row])
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    result = mapping(cast(JsonValue, json.loads(arguments.result.read_text())))
    smooth = mapping(result["smooth_projected_gauge"])
    rough = mapping(result["controlled_rough_gauge"])
    smooth_topology = mapping(smooth["topology"])
    smooth_reduction = mapping(smooth["reduction"])
    rough_reduction = mapping(rough["reduction"])

    figure, axes = plt.subplots(2, 2, figsize=(10.5, 8.0), constrained_layout=True)
    wilson = np.asarray(nested_reals(smooth_topology["wilson_x_phases"]))
    transverse = np.arange(wilson.shape[0]) - wilson.shape[0] // 2
    transverse = transverse / wilson.shape[0]
    for band in range(wilson.shape[1]):
        axes[0, 0].plot(transverse, wilson[:, band] / np.pi, "o-")
    axes[0, 0].set(
        xlabel="$k_y/G$",
        ylabel="Wilson eigenphase / $\\pi$",
        title="Rank-three Wilson spectrum",
    )
    axes[0, 0].grid(alpha=0.25)

    smooth_blocks = records(smooth_reduction["hopping_blocks"])
    rough_blocks = records(rough_reduction["hopping_blocks"])
    smooth_norms = np.asarray([real(item["frobenius_norm"]) for item in smooth_blocks])
    rough_norms = np.asarray([real(item["frobenius_norm"]) for item in rough_blocks])
    axes[0, 1].loglog(
        np.maximum(smooth_norms, 1.0e-18),
        np.maximum(rough_norms, 1.0e-18),
        ".",
        alpha=0.7,
    )
    limit = [1.0e-10, max(float(np.max(rough_norms)), float(np.max(smooth_norms)))]
    axes[0, 1].plot(limit, limit, "k--", linewidth=1)
    axes[0, 1].set(
        xlabel="smooth-gauge block norm ($E_G$)",
        ylabel="rough-gauge block norm ($E_G$)",
        title="Gauge-dependent hopping locality",
    )
    axes[0, 1].grid(alpha=0.25)

    for label, reduction in (("smooth", smooth_reduction), ("rough", rough_reduction)):
        shells = records(reduction["shell_study"])
        axes[1, 0].semilogy(
            [integer(item["retained_block_count"]) for item in shells],
            [real(item["omitted_block_frobenius_l2_norm"]) for item in shells],
            "o-",
            label=label,
        )
    axes[1, 0].set(
        xlabel="retained hopping blocks",
        ylabel="omitted block norm ($E_G$)",
        title="Composite shell convergence",
    )
    axes[1, 0].legend()
    axes[1, 0].grid(alpha=0.25)

    smooth_localization = records(smooth["localization"])
    rough_localization = records(rough["localization"])
    orbitals = np.arange(len(smooth_localization))
    width = 0.36
    axes[1, 1].bar(
        orbitals - width / 2,
        [real(item["spread_cell_squared"]) for item in smooth_localization],
        width,
        label="smooth",
    )
    axes[1, 1].bar(
        orbitals + width / 2,
        [real(item["spread_cell_squared"]) for item in rough_localization],
        width,
        label="rough",
    )
    axes[1, 1].set(
        xticks=orbitals,
        xticklabels=["s-like", "$p_x$-like", "$p_y$-like"],
        ylabel="finite-supercell spread ($a^2$)",
        title="Direct localization diagnostic",
    )
    axes[1, 1].legend()

    figure.suptitle(
        "Periodic-2D composite gauge comparison — illustrative numerical verification"
    )
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(arguments.output, dpi=180)


if __name__ == "__main__":
    main()
