#!/usr/bin/env python3
"""Plot the retained adversarial periodic-reduction stress result."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import cast

import matplotlib.pyplot as plt

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


class PeriodicReductionStressPlotter:
    """Render cutoff, higher-band, potential-shape, and route stress evidence."""

    __slots__ = ()

    def execute(self, result_path: Path, output_path: Path) -> None:
        result = self._mapping(
            cast(JsonValue, json.loads(result_path.read_text(encoding="utf-8")))
        )
        amplitudes = self._records(result["potential_amplitude_stress"])
        shapes = self._mapping(result["potential_shape_stress"])
        shape_cases = self._records(shapes["cases"])
        mesh = self._records(result["mesh_band_and_isolation_stress"])
        routes = self._mapping(result["route_assumption_stress"])

        figure, axes = plt.subplots(2, 2, figsize=(11.0, 8.0), constrained_layout=True)
        self._plot_cutoff_stress(axes[0, 0], amplitudes)
        self._plot_shape_gaps(axes[0, 1], shape_cases)
        self._plot_higher_bands(axes[1, 0], mesh)
        self._plot_route_attack(axes[1, 1], routes)
        figure.savefig(output_path, dpi=180)
        plt.close(figure)

    def _plot_cutoff_stress(
        self,
        axis: plt.Axes,
        amplitude_records: tuple[dict[str, JsonValue], ...],
    ) -> None:
        for record in amplitude_records:
            strength = self._real(record["potential_strength"])
            cutoff_records = self._records(record["plane_wave_cutoff_study"])
            cutoffs = [self._integer(item["cutoff"]) for item in cutoff_records]
            errors = [
                max(self._real(item["maximum_low_band_error"]), 1.0e-16)
                for item in cutoff_records
            ]
            axis.semilogy(
                cutoffs,
                errors,
                marker="o",
                label=rf"$V_0/E_G={strength:g}$",
            )
        axis.set_xlabel("plane-wave cutoff $P$")
        axis.set_ylabel(r"bands 0--7 maximum error / $E_G$")
        axis.set_title("Plane-wave cutoff convergence")
        axis.grid(True, which="both", alpha=0.3)
        axis.legend(fontsize="small", ncols=2)

    def _plot_shape_gaps(
        self,
        axis: plt.Axes,
        shape_records: tuple[dict[str, JsonValue], ...],
    ) -> None:
        for record in shape_records:
            identifier = self._string(record["id"])
            gaps = [
                max(self._real(item), 1.0e-16)
                for item in self._array(record["minimum_adjacent_gaps"])
            ]
            axis.semilogy(
                range(len(gaps)),
                gaps,
                marker="o",
                label=identifier.replace("_", " "),
            )
        axis.axhline(1.0e-8, color="black", linestyle=":", label="gap threshold")
        axis.set_xlabel("energy-ordered band index")
        axis.set_ylabel(r"minimum adjacent gap / $E_G$")
        axis.set_title("Gap sensitivity to potential shape")
        axis.grid(True, which="both", alpha=0.3)
        axis.legend(fontsize="x-small", ncols=2)

    def _plot_higher_bands(
        self,
        axis: plt.Axes,
        mesh_records: tuple[dict[str, JsonValue], ...],
    ) -> None:
        baseline = [
            record
            for record in mesh_records
            if self._real(record["potential_strength"]) == 0.5
            and self._integer(record["mesh_size"]) == 128
        ]
        baseline.sort(key=lambda record: self._integer(record["band_index"]))
        bands = [self._integer(record["band_index"]) for record in baseline]
        gaps = [self._real(record["minimum_adjacent_gap"]) for record in baseline]
        errors = [
            self._real(record["fixed_range_withheld_maximum_error"])
            for record in baseline
        ]
        axis.semilogy(bands, gaps, marker="o", label="minimum adjacent gap")
        axis.semilogy(
            bands,
            errors,
            marker="s",
            label=r"$r_c=3a$ withheld maximum error",
        )
        axis.axhline(1.0e-8, color="black", linestyle=":", label="gap threshold")
        axis.set_xlabel("energy-ordered band index")
        axis.set_ylabel(r"energy scale / $E_G$")
        axis.set_title(r"Isolation and range-$3a$ error, $V_0/E_G=0.5$")
        axis.grid(True, which="both", alpha=0.3)
        axis.legend(fontsize="small")

    def _plot_route_attack(
        self, axis: plt.Axes, route_record: dict[str, JsonValue]
    ) -> None:
        labels = ["uniform\ncomplete", "nonuniform\nweights", "restricted\nregion"]
        defects = [
            self._real(route_record["uniform_complete_coefficient_defect"]),
            self._real(route_record["nonuniform_weight_coefficient_defect"]),
            self._real(route_record["incomplete_training_coefficient_defect"]),
        ]
        axis.bar(labels, defects, color=["#4c78a8", "#f58518", "#e45756"])
        axis.set_yscale("log")
        axis.set_ylabel(r"coefficient $\ell_2$ defect")
        axis.set_title("Sensitivity to fitting objective")
        axis.grid(True, axis="y", which="both", alpha=0.3)

    @staticmethod
    def _mapping(value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("value must be a JSON object")
        return value

    @staticmethod
    def _records(value: JsonValue) -> tuple[dict[str, JsonValue], ...]:
        if not isinstance(value, list):
            raise TypeError("value must be a JSON array")
        records: list[dict[str, JsonValue]] = []
        for item in value:
            if not isinstance(item, dict):
                raise TypeError("array entries must be JSON objects")
            records.append(item)
        return tuple(records)

    @staticmethod
    def _array(value: JsonValue) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError("value must be a JSON array")
        return value

    @staticmethod
    def _real(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("value must be a number")
        return float(value)

    @staticmethod
    def _integer(value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("value must be an integer")
        return value

    @staticmethod
    def _string(value: JsonValue) -> str:
        if not isinstance(value, str):
            raise TypeError("value must be a string")
        return value


class CommandAdapter:
    """Adapt command-line paths to the owned stress plotter."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("result", type=Path)
        parser.add_argument("--output", type=Path, required=True)
        args = parser.parse_args(argv)
        PeriodicReductionStressPlotter().execute(
            cast(Path, args.result).resolve(), cast(Path, args.output).resolve()
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
