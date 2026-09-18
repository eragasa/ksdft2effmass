#!/usr/bin/env python3
"""Plot retained optimizer-basin and convergence diagnostics."""

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


class OptimizerBasinPlotter:
    """Render start outcomes and best/median convergence sequences."""

    __slots__ = ()

    def execute(self, result_path: Path, output_path: Path) -> None:
        result = self._mapping(
            cast(JsonValue, json.loads(result_path.read_text(encoding="utf-8")))
        )
        configurations = [
            self._mapping(value) for value in self._array(result["configurations"])
        ]
        figure, axes = plt.subplots(2, 2, figsize=(13.5, 9.0), constrained_layout=True)
        self._all_starts(axes[0, 0], configurations)
        self._sequence(
            axes[0, 1],
            configurations,
            axis_name="mesh",
            parameter="reciprocal_mesh_size",
            title="Mesh sequence at $P=4$, $c=N$",
            x_label="mesh size $N$",
        )
        self._sequence(
            axes[1, 0],
            configurations,
            axis_name="cutoff",
            parameter="plane_wave_cutoff",
            title="Cutoff sequence at $N=c=19$",
            x_label="plane-wave cutoff $P$",
        )
        self._counts(axes[1, 1], configurations)
        figure.suptitle(
            "Periodic-2D deterministic multi-initialization study\n"
            "Synthetic non-DFT numerical verification; 21/72 starts did not converge",
            fontsize=14,
        )
        figure.savefig(output_path, dpi=220)
        plt.close(figure)

    def _all_starts(
        self, axis: Axes, configurations: list[dict[str, JsonValue]]
    ) -> None:
        for index, configuration in enumerate(configurations):
            starts = [
                self._mapping(value) for value in self._array(configuration["starts"])
            ]
            for offset, start in enumerate(starts):
                converged = start["convergence_criterion_satisfied"] is True
                axis.scatter(
                    index + (offset - 3.5) * 0.035,
                    self._real(start["native_total_spread_cell_squared"]),
                    marker="o" if converged else "x",
                    s=34 if converged else 42,
                    color="#1f77b4" if converged else "#d62728",
                    linewidth=1.2,
                    alpha=0.9,
                )
        labels = [self._short_label(value) for value in configurations]
        axis.set_xticks(range(len(labels)), labels, rotation=38, ha="right")
        axis.set_yscale("log")
        axis.set_ylabel("native Wannier90 total spread ($a^2$)")
        axis.set_title("All deterministic starts")
        axis.grid(alpha=0.25, which="both")
        axis.scatter([], [], marker="o", color="#1f77b4", label="converged")
        axis.scatter([], [], marker="x", color="#d62728", label="5000-step stop")
        axis.legend(frameon=False)

    def _sequence(
        self,
        plot_axis: Axes,
        configurations: list[dict[str, JsonValue]],
        *,
        axis_name: str,
        parameter: str,
        title: str,
        x_label: str,
    ) -> None:
        selected = [
            value
            for value in configurations
            if axis_name in self._strings(value["study_axes"])
        ]
        selected.sort(key=lambda value: self._integer(value[parameter]))
        x_values = [self._integer(value[parameter]) for value in selected]
        best = [
            self._real(
                self._mapping(value["best_observed_converged"])[
                    "native_total_spread_cell_squared"
                ]
            )
            for value in selected
        ]
        median = [
            self._real(
                self._mapping(value["median_across_converged_starts"])[
                    "native_total_spread_cell_squared"
                ]
            )
            for value in selected
        ]
        plot_axis.plot(x_values, best, "o-", label="best observed converged")
        plot_axis.plot(x_values, median, "s--", label="median converged start")
        plot_axis.set_xlabel(x_label)
        plot_axis.set_ylabel("native total spread ($a^2$)")
        plot_axis.set_title(title)
        plot_axis.grid(alpha=0.25)
        plot_axis.legend(frameon=False)

    def _counts(self, axis: Axes, configurations: list[dict[str, JsonValue]]) -> None:
        positions = list(range(len(configurations)))
        converged = [
            self._integer(value["converged_start_count"]) for value in configurations
        ]
        nonconverged = [8 - value for value in converged]
        basins = [
            self._integer(value["observed_converged_basin_count"])
            for value in configurations
        ]
        axis.bar(positions, converged, color="#2ca02c", label="converged starts")
        axis.bar(
            positions,
            nonconverged,
            bottom=converged,
            color="#d62728",
            label="5000-step stops",
        )
        axis.plot(
            positions,
            basins,
            "D-",
            color="#111111",
            linewidth=1.2,
            markersize=4,
            label="observed converged basins",
        )
        labels = [self._short_label(value) for value in configurations]
        axis.set_xticks(positions, labels, rotation=38, ha="right")
        axis.set_ylim(0, 8.6)
        axis.set_ylabel("count out of eight starts")
        axis.set_title("Convergence and basin multiplicity")
        axis.grid(alpha=0.2, axis="y")
        axis.legend(frameon=False, fontsize=8)

    def _short_label(self, configuration: dict[str, JsonValue]) -> str:
        return (
            f"P{self._integer(configuration['plane_wave_cutoff'])}/"
            f"N{self._integer(configuration['reciprocal_mesh_size'])}/"
            f"c{self._real(configuration['transverse_lattice_length']):g}"
        )

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
    def _integer(value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("expected an integer")
        return value

    @staticmethod
    def _real(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("expected a real number")
        return float(value)

    def _strings(self, value: JsonValue) -> tuple[str, ...]:
        result: list[str] = []
        for item in self._array(value):
            if not isinstance(item, str):
                raise TypeError("expected string array entries")
            result.append(item)
        return tuple(result)


class CommandAdapter:
    """Adapt CLI paths to the plot action."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("result", type=Path)
        parser.add_argument("output", type=Path)
        arguments = parser.parse_args(argv)
        OptimizerBasinPlotter().execute(
            cast(Path, arguments.result).resolve(),
            cast(Path, arguments.output).resolve(),
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
