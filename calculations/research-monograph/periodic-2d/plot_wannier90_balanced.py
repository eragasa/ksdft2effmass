#!/usr/bin/env python3
"""Plot the corrected periodic-2D Wannier90 comparison."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import cast

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


class CorrectedWannier90Plotter:
    """Render localization, centers, hopping tails, and operator defects."""

    __slots__ = ("_result", "_composite")

    def __init__(self, result_payload: bytes, composite_payload: bytes) -> None:
        self._result = self._mapping(
            cast(JsonValue, json.loads(result_payload.decode("utf-8")))
        )
        self._composite = self._mapping(
            cast(JsonValue, json.loads(composite_payload.decode("utf-8")))
        )

    def execute(self) -> Figure:
        figure, axes = plt.subplots(2, 2, figsize=(9.5, 7.5), constrained_layout=True)
        localization = self._mapping(self._result["localization"])
        common_localization = self._array(
            localization["common_finite_supercell_estimator"]
        )
        w90_spreads = [
            self._real(self._mapping(value)["spread_cell_squared"])
            for value in common_localization
        ]
        smooth = self._mapping(self._composite["smooth_projected_gauge"])
        direct_localization = self._array(
            localization["direct_projected_common_finite_supercell_estimator"]
        )
        direct_spreads = [
            self._real(self._mapping(value)["spread_cell_squared"])
            for value in direct_localization
        ]
        positions = np.arange(3, dtype=np.float64)
        width = 0.36
        axes[0, 0].bar(
            positions - width / 2,
            direct_spreads,
            width,
            label="direct projected",
            color="#56B4E9",
        )
        axes[0, 0].bar(
            positions + width / 2,
            w90_spreads,
            width,
            label="Wannier90",
            color="#D55E00",
        )
        axes[0, 0].set_xticks(positions, ("orbital 1", "orbital 2", "orbital 3"))
        axes[0, 0].set_ylabel("active-plane spread / cell$^2$")
        axes[0, 0].set_title("Common finite-supercell estimator")
        axes[0, 0].legend()
        axes[0, 0].grid(axis="y", alpha=0.25)

        represented = self._mapping(self._result["represented_comparison"])
        w90_shells = self._array(represented["shell_study"])
        direct_reduction = self._mapping(smooth["reduction"])
        direct_shells = self._array(direct_reduction["shell_study"])
        shell_radii = [
            self._integer(self._mapping(value)["maximum_squared_radius"])
            for value in w90_shells
        ]
        w90_tail = [
            self._real(self._mapping(value)["omitted_block_frobenius_l2_norm"])
            for value in w90_shells
        ]
        direct_tail = [
            self._real(self._mapping(value)["omitted_block_frobenius_l2_norm"])
            for value in direct_shells
        ]
        nonzero = slice(0, -1)
        axes[0, 1].semilogy(
            np.asarray(shell_radii)[nonzero],
            np.asarray(direct_tail)[nonzero],
            "o-",
            label="direct projected",
            color="#56B4E9",
        )
        axes[0, 1].semilogy(
            np.asarray(shell_radii)[nonzero],
            np.asarray(w90_tail)[nonzero],
            "s-",
            label="Wannier90",
            color="#D55E00",
        )
        axes[0, 1].set_xlabel("maximum squared hopping radius")
        axes[0, 1].set_ylabel("omitted block $L^2$ norm")
        axes[0, 1].set_title("Matrix-valued hopping tail")
        axes[0, 1].legend()
        axes[0, 1].grid(alpha=0.25, which="both")

        for index, center_value in enumerate(common_localization):
            center = self._mapping(center_value)
            coordinates = self._reals(center["center_modulo_cell"])
            axes[1, 0].scatter(
                coordinates[0],
                coordinates[1],
                s=75,
                label=f"Wannier90 {index + 1}",
            )
        axes[1, 0].scatter(
            0.5,
            0.5,
            marker="x",
            s=100,
            linewidths=2.0,
            color="black",
            label="direct projected centers",
        )
        axes[1, 0].set_xlim(0.0, 1.0)
        axes[1, 0].set_ylim(0.0, 1.0)
        axes[1, 0].set_aspect("equal")
        axes[1, 0].set_xlabel("fractional $x$")
        axes[1, 0].set_ylabel("fractional $y$")
        axes[1, 0].set_title("Active-plane centers modulo a cell")
        axes[1, 0].legend(fontsize=8)
        axes[1, 0].grid(alpha=0.25)

        defect_labels = (
            "projector",
            "$k$-aligned\noperator",
            "HR operator",
            "HR spectrum",
        )
        defect_values = (
            self._real(represented["direct_w90_projector_maximum_frobenius_defect"]),
            self._real(
                represented[
                    "k_dependent_exact_alignment_operator_maximum_frobenius_defect"
                ]
            ),
            self._real(represented["hr_mesh_operator_maximum_frobenius_defect"]),
            self._real(represented["hr_mesh_spectrum_maximum_absolute_defect"]),
        )
        axes[1, 1].bar(defect_labels, defect_values, color="#009E73")
        axes[1, 1].set_yscale("log")
        axes[1, 1].set_ylabel("maximum defect")
        axes[1, 1].set_title("Represented comparison")
        axes[1, 1].grid(axis="y", alpha=0.25, which="both")
        figure.suptitle("Corrected independent Wannier90 rank-three comparison")
        return figure

    def _mapping(self, value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("expected a mapping")
        return value

    def _array(self, value: JsonValue) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError("expected an array")
        return value

    def _integer(self, value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("expected an integer")
        return value

    def _real(self, value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("expected a real number")
        return float(value)

    def _reals(self, value: JsonValue) -> tuple[float, ...]:
        return tuple(self._real(item) for item in self._array(value))


def main() -> None:
    """CLI entry point required by the script boundary."""
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    plotter = CorrectedWannier90Plotter(
        arguments.result.read_bytes(),
        arguments.result.with_name("composite-result.json").read_bytes(),
    )
    figure = plotter.execute()
    figure.savefig(arguments.output, dpi=220)
    plt.close(figure)


if __name__ == "__main__":
    main()
