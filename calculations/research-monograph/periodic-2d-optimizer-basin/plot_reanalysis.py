#!/usr/bin/env python3
"""Plot spread-component, trace, symmetry, and estimator reanalysis."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import cast

import matplotlib.pyplot as plt
from matplotlib.axes import Axes

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


class ReanalysisPlotter:
    """Render the principal offline reanalysis diagnostics."""

    __slots__ = ()

    def execute(self, result_path: Path, output_path: Path) -> None:
        result = self._mapping(
            cast(JsonValue, json.loads(result_path.read_text(encoding="utf-8")))
        )
        configurations = [
            self._mapping(value) for value in self._array(result["configurations"])
        ]
        figure, axes = plt.subplots(2, 2, figsize=(13.5, 9.0), constrained_layout=True)
        self._spread_sequence(
            axes[0, 0], configurations[:4], "reciprocal_mesh_size", "mesh size $N$"
        )
        cutoff = [configurations[index] for index in (4, 5, 2, 6)]
        cutoff.sort(key=lambda value: self._integer(value["plane_wave_cutoff"]))
        self._spread_sequence(
            axes[0, 1], cutoff, "plane_wave_cutoff", "plane-wave cutoff $P$"
        )
        self._trace_and_basins(axes[1, 0], result, configurations)
        self._estimator_refinement(axes[1, 1], result)
        figure.suptitle(
            "Periodic-2D offline optimizer-basin reanalysis\n"
            "Spread components, terminal traces, D4-aware basins, and FFT refinement",
            fontsize=14,
        )
        figure.savefig(output_path, dpi=220)
        plt.close(figure)

    def _spread_sequence(
        self,
        axis: Axes,
        configurations: list[dict[str, JsonValue]],
        parameter: str,
        x_label: str,
    ) -> None:
        x_values = [self._integer(value[parameter]) for value in configurations]
        best = [
            self._mapping(value["best_observed_converged_by_omega_tilde"])
            for value in configurations
        ]
        omega_i = [
            self._real(
                self._mapping(value["spread_components"])["omega_i_cell_squared"]
            )
            for value in best
        ]
        omega_tilde = [
            self._real(
                self._mapping(value["spread_components"])["omega_tilde_cell_squared"]
            )
            for value in best
        ]
        axis.plot(x_values, omega_i, "o-", label="$\\Omega_I$")
        axis.plot(x_values, omega_tilde, "s--", label="$\\widetilde{\\Omega}$")
        axis.set_xlabel(x_label)
        axis.set_ylabel("spread component ($a^2$)")
        axis.set_title(f"Best converged components versus {x_label}")
        axis.grid(alpha=0.25)
        axis.legend(frameon=False)

    def _trace_and_basins(
        self,
        axis: Axes,
        result: dict[str, JsonValue],
        configurations: list[dict[str, JsonValue]],
    ) -> None:
        counts = self._mapping(result["diagnostic_classification_counts"])
        labels = [
            "converged",
            "still descending",
            "near stationary",
            "oscillatory/stalled",
        ]
        keys = [
            "native_converged",
            "continuing_descent_at_iteration_limit",
            "near_stationary_without_window_convergence",
            "oscillatory_or_stalled",
        ]
        values = [self._integer(counts[key]) for key in keys]
        positions = list(range(len(labels)))
        axis.bar(positions, values, color=["#2ca02c", "#ff7f0e", "#1f77b4", "#d62728"])
        axis.set_xticks(positions, labels, rotation=25, ha="right")
        axis.set_ylabel("start count")
        axis.set_title("Terminal trace classifications")
        axis.grid(alpha=0.2, axis="y")
        inset = axis.inset_axes([0.60, 0.46, 0.37, 0.48])
        basin_counts = [
            self._integer(value["symmetry_aware_observed_basin_count"])
            for value in configurations
        ]
        inset.plot(range(len(basin_counts)), basin_counts, "D-", color="black")
        inset.set_ylim(0, 8.5)
        inset.set_title("D4-aware basins", fontsize=9)
        inset.set_xlabel("configuration", fontsize=8)
        inset.tick_params(labelsize=8)
        inset.grid(alpha=0.2)

    def _estimator_refinement(self, axis: Axes, result: dict[str, JsonValue]) -> None:
        records = [
            self._mapping(value)
            for value in self._array(result["common_estimator_refinement"])
        ]
        for record in records:
            sizes = [self._mapping(value) for value in self._array(record["sizes"])]
            reference = self._real(sizes[-1]["common_total_spread_cell_squared"])
            axis.plot(
                [self._integer(value["fft_size"]) for value in sizes],
                [
                    abs(
                        self._real(value["common_total_spread_cell_squared"])
                        - reference
                    )
                    / max(abs(reference), 1.0e-15)
                    for value in sizes
                ],
                "o-",
                label=self._string(record["case_id"]).replace("_", " "),
            )
        axis.set_yscale("symlog", linthresh=1.0e-10)
        axis.set_xlabel("common-estimator FFT size")
        axis.set_ylabel("relative difference from $1024^2$")
        axis.set_title("Common-estimator refinement")
        axis.grid(alpha=0.25, which="both")
        axis.legend(frameon=False, fontsize=7)

    @staticmethod
    def _mapping(value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("expected an object")
        return value

    @staticmethod
    def _array(value: JsonValue) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError("expected an array")
        return value

    @staticmethod
    def _string(value: JsonValue) -> str:
        if not isinstance(value, str):
            raise TypeError("expected a string")
        return value

    @staticmethod
    def _integer(value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("expected an integer")
        return value

    @staticmethod
    def _real(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("expected a real number")
        return float(value)


class CommandAdapter:
    """Adapt CLI paths to the reanalysis plotter."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("result", type=Path)
        parser.add_argument("output", type=Path)
        arguments = parser.parse_args(argv)
        ReanalysisPlotter().execute(
            cast(Path, arguments.result).resolve(),
            cast(Path, arguments.output).resolve(),
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
