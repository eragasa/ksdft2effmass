#!/usr/bin/env python3
"""Plot the retained direct composite-band result."""

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


class CompositeResultPlotter:
    """Render gaps, Wilson phases, hopping locality, and truncation errors."""

    __slots__ = ()

    def execute(self, result_path: Path, output_path: Path) -> None:
        result = self._mapping(
            cast(JsonValue, json.loads(result_path.read_text(encoding="utf-8")))
        )
        groups = self._records(result["groups"])
        figure, axes = plt.subplots(2, 2, figsize=(11.0, 8.0), constrained_layout=True)
        self._plot_gaps(axes[0, 0], groups)
        self._plot_wilson_phases(axes[0, 1], groups)
        self._plot_hopping_decay(axes[1, 0], groups)
        self._plot_range_errors(axes[1, 1], groups)
        figure.savefig(output_path, dpi=180)
        plt.close(figure)

    def _plot_gaps(
        self, axis: plt.Axes, groups: tuple[dict[str, JsonValue], ...]
    ) -> None:
        labels = [self._string(group["id"]).replace("_", " ") for group in groups]
        positions = np.arange(len(labels), dtype=np.float64)
        width = 0.34
        axis.bar(
            positions - width / 2.0,
            [self._real(group["internal_minimum_gap"]) for group in groups],
            width,
            label="internal minimum gap",
        )
        axis.bar(
            positions + width / 2.0,
            [self._real(group["external_minimum_gap"]) for group in groups],
            width,
            label="external minimum gap",
        )
        axis.axhline(1.0e-8, color="black", linestyle=":", label="gap threshold")
        axis.set_xticks(positions, labels)
        axis.set_yscale("log")
        axis.set_ylabel(r"gap / $E_G$")
        axis.set_title("Retained-subspace gaps")
        axis.grid(True, axis="y", which="both", alpha=0.3)
        axis.legend(fontsize="small")

    def _plot_wilson_phases(
        self, axis: plt.Axes, groups: tuple[dict[str, JsonValue], ...]
    ) -> None:
        for index, group in enumerate(groups):
            phases = [
                self._real(value)
                for value in self._array(group["wilson_loop_eigenphases"])
            ]
            axis.scatter(
                [index] * len(phases),
                phases,
                s=70,
                label=self._string(group["id"]).replace("_", " "),
            )
        axis.axhline(0.0, color="black", linewidth=0.8)
        axis.set_xticks(
            range(len(groups)),
            [self._string(group["id"]).replace("_", " ") for group in groups],
        )
        axis.set_ylabel("Wilson-loop eigenphase / rad")
        axis.set_title("Composite closure phases")
        axis.grid(True, alpha=0.3)

    def _plot_hopping_decay(
        self, axis: plt.Axes, groups: tuple[dict[str, JsonValue], ...]
    ) -> None:
        for group in groups:
            identifier = self._string(group["id"]).replace("_", " ")
            for gauge, style in (("smooth", "-"), ("rough", "--")):
                records = self._records(group[f"{gauge}_hopping_blocks"])
                distance_to_norm: dict[int, float] = {}
                for record in records:
                    distance = abs(self._integer(record["representative_cells"]))
                    norm = self._real(record["frobenius_norm"])
                    distance_to_norm[distance] = max(
                        norm, distance_to_norm.get(distance, 0.0)
                    )
                distances = sorted(distance_to_norm)
                axis.semilogy(
                    distances,
                    [distance_to_norm[value] for value in distances],
                    linestyle=style,
                    marker="o" if gauge == "smooth" else None,
                    label=f"{identifier}, {gauge}",
                )
        axis.set_xlabel(r"block distance $|R|/a$")
        axis.set_ylabel(r"maximum $\|T_R\|_F/E_G$")
        axis.set_title("Gauge dependence of block locality")
        axis.grid(True, which="both", alpha=0.3)
        axis.legend(fontsize="small")

    def _plot_range_errors(
        self, axis: plt.Axes, groups: tuple[dict[str, JsonValue], ...]
    ) -> None:
        for group in groups:
            identifier = self._string(group["id"]).replace("_", " ")
            records = self._records(group["range_study"])
            ranges = [
                self._integer(record["hopping_range_cells"]) for record in records
            ]
            axis.semilogy(
                ranges,
                [
                    self._real(record["smooth_withheld_eigenvalue_maximum_error"])
                    for record in records
                ],
                marker="o",
                label=f"{identifier}, smooth",
            )
            axis.semilogy(
                ranges,
                [
                    self._real(record["rough_withheld_eigenvalue_maximum_error"])
                    for record in records
                ],
                linestyle="--",
                label=f"{identifier}, rough",
            )
        axis.set_xlabel(r"block-hopping range $r_c/a$")
        axis.set_ylabel(r"withheld eigenvalue maximum error / $E_G$")
        axis.set_title("Composite finite-range hierarchy")
        axis.grid(True, which="both", alpha=0.3)
        axis.legend(fontsize="small")

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
    """Adapt command-line paths to the composite plotter."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("result", type=Path)
        parser.add_argument("--output", type=Path, required=True)
        args = parser.parse_args(argv)
        CompositeResultPlotter().execute(
            cast(Path, args.result).resolve(), cast(Path, args.output).resolve()
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
