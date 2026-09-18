#!/usr/bin/env python3
"""Plot the retained two-dimensional periodic-reduction diagnostics."""

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
        raise TypeError("expected JSON object")
    return value


def records(value: JsonValue) -> list[dict[str, JsonValue]]:
    if not isinstance(value, list):
        raise TypeError("expected JSON array")
    return [mapping(item) for item in value]


def real(value: JsonValue) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise TypeError("expected number")
    return float(value)


def integer(value: JsonValue) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("expected integer")
    return value


def reals(value: JsonValue) -> list[float]:
    if not isinstance(value, list):
        raise TypeError("expected array")
    return [real(item) for item in value]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    result = mapping(cast(JsonValue, json.loads(arguments.result.read_text())))
    parent = mapping(result["parent_representation_verification"])
    continuation = records(result["coupling_continuation"])

    figure, axes = plt.subplots(2, 3, figsize=(13.2, 8.0), constrained_layout=True)

    pw = records(parent["plane_wave_cutoff_study"])
    fd = records(parent["finite_difference_grid_study"])
    axes[0, 0].semilogy(
        [integer(item["represented_dimension"]) for item in pw],
        [real(item["maximum_low_band_absolute_error"]) for item in pw],
        "o-",
        label="plane wave",
    )
    axes[0, 0].semilogy(
        [integer(item["represented_dimension"]) for item in fd],
        [real(item["maximum_low_band_absolute_error"]) for item in fd],
        "s-",
        label="finite difference",
    )
    axes[0, 0].set(
        xlabel="represented dimension",
        ylabel="low-band error ($E_G$)",
        title="Independent parent refinement",
    )
    axes[0, 0].legend()
    axes[0, 0].grid(alpha=0.25)

    strongest = continuation[-1]
    mesh = np.asarray(reals(strongest["reciprocal_mesh"]))
    energy_value = strongest["lowest_band_energies"]
    if not isinstance(energy_value, list):
        raise TypeError("energy surface must be an array")
    energies = np.asarray(
        [[real(item) for item in cast(list[JsonValue], row)] for row in energy_value]
    )
    contour = axes[0, 1].contourf(mesh, mesh, energies.T, levels=18, cmap="viridis")
    figure.colorbar(contour, ax=axes[0, 1], label="$E_0/E_G$")
    axes[0, 1].set(
        xlabel="$k_x/G$",
        ylabel="$k_y/G$",
        title=(
            f"Coupled lowest band, $\\lambda_{{xy}}={real(strongest['lambda_xy']):.2f}$"
        ),
    )
    axes[0, 1].set_aspect("equal")

    for case in continuation:
        topology = mapping(case["topology_and_gauge"])
        axes[0, 2].plot(
            mesh,
            np.unwrap(np.asarray(reals(topology["wilson_loop_x_phases"]))) / np.pi,
            marker=".",
            label=f"{real(case['lambda_xy']):.2f}",
        )
    axes[0, 2].set(
        xlabel="$k_y/G$",
        ylabel="$x$ Wilson phase / $\\pi$",
        title="Gauge-invariant loop phases",
    )
    axes[0, 2].grid(alpha=0.25)
    axes[0, 2].legend(title="$\\lambda_{xy}$", ncol=2)

    hopping = records(strongest["hopping_coefficients"])
    half = int(round(np.sqrt(len(hopping)))) // 2
    hopping_map = np.full((2 * half + 1, 2 * half + 1), np.nan)
    for item in hopping:
        rx = integer(item["rx"])
        ry = integer(item["ry"])
        hopping_map[rx + half, ry + half] = max(real(item["magnitude"]), 1.0e-18)
    image = axes[1, 0].imshow(
        np.log10(hopping_map.T),
        origin="lower",
        extent=(-half - 0.5, half + 0.5, -half - 0.5, half + 0.5),
        cmap="magma",
    )
    figure.colorbar(image, ax=axes[1, 0], label="$\\log_{10}|t_{R_x,R_y}/E_G|$")
    axes[1, 0].set(xlabel="$R_x/a$", ylabel="$R_y/a$", title="Coupled hopping map")

    for case in continuation:
        shells = records(case["shell_study"])
        axes[1, 1].semilogy(
            [integer(item["retained_coefficient_count"]) for item in shells],
            [real(item["withheld_root_mean_square_error"]) for item in shells],
            "o-",
            label=f"{real(case['lambda_xy']):.2f}",
        )
    axes[1, 1].set(
        xlabel="retained hopping coefficients",
        ylabel="withheld RMSE ($E_G$)",
        title="Symmetry-shell convergence",
    )
    axes[1, 1].grid(alpha=0.25)
    axes[1, 1].legend(title="$\\lambda_{xy}$", ncol=2)

    couplings = np.asarray([real(case["lambda_xy"]) for case in continuation])
    separability = np.asarray(
        [
            real(case["maximum_lowest_band_separability_residual"])
            for case in continuation
        ]
    )
    mixed = np.asarray(
        [real(case["mixed_to_total_nonlocal_hopping_ratio"]) for case in continuation]
    )
    axes[1, 2].plot(
        couplings, separability, "o-", label="separability residual ($E_G$)"
    )
    axes[1, 2].plot(couplings, mixed, "s-", label="mixed-hopping ratio")
    axes[1, 2].set(
        xlabel="$\\lambda_{xy}$",
        ylabel="diagnostic",
        title="Controlled loss of separability",
    )
    axes[1, 2].grid(alpha=0.25)
    axes[1, 2].legend()

    figure.suptitle(
        "Two-dimensional separable-to-coupled reduction — "
        "illustrative numerical verification",
        fontsize=13,
    )
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(arguments.output, dpi=180)


if __name__ == "__main__":
    main()
