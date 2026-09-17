#!/usr/bin/env python3
"""Plot the bounded nonconverged Wannier90 comparison."""

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


class Wannier90ComparisonPlotter:
    """Render centers, spreads, range errors, and alignment diagnostics."""

    __slots__ = ()

    def execute(
        self, result_path: Path, composite_path: Path, output_path: Path
    ) -> None:
        result = self._mapping(
            cast(JsonValue, json.loads(result_path.read_text(encoding="utf-8")))
        )
        composite = self._mapping(
            cast(JsonValue, json.loads(composite_path.read_text(encoding="utf-8")))
        )
        groups = self._records(result["groups"])
        converged = all(
            self._boolean(group["convergence_criterion_satisfied"]) for group in groups
        )
        direct_groups = {
            self._string(group["id"]): group
            for group in self._records(composite["groups"])
        }
        figure, axes = plt.subplots(2, 2, figsize=(11.0, 8.0), constrained_layout=True)
        self._plot_centers(axes[0, 0], groups, converged)
        self._plot_spreads(axes[0, 1], groups, converged)
        self._plot_range_errors(axes[1, 0], groups, direct_groups)
        self._plot_diagnostics(axes[1, 1], groups)
        figure.suptitle(
            (
                "Wannier90 localization benchmark (converged)"
                if converged
                else "Wannier90 localization benchmark (not converged)"
            ),
            fontsize=14,
        )
        figure.savefig(output_path, dpi=180)
        plt.close(figure)

    def _plot_centers(
        self,
        axis: plt.Axes,
        groups: tuple[dict[str, JsonValue], ...],
        converged: bool,
    ) -> None:
        for index, group in enumerate(groups):
            direct = [
                self._real(value)
                for value in self._array(
                    group["direct_wilson_centers_by_phase_convention"]
                )
            ]
            wannier = [
                (self._real(self._array(value)[0]) + 0.5) % 1.0 - 0.5
                for value in self._array(group["centers_cell_coordinates"])
            ]
            axis.scatter(
                [index - 0.08] * len(direct),
                direct,
                marker="o",
                s=70,
                color="#4c78a8",
                label="direct Wilson" if index == 0 else None,
            )
            axis.scatter(
                [index + 0.08] * len(wannier),
                wannier,
                marker="s",
                s=70,
                color="#f58518",
                label=(
                    "Wannier90 converged"
                    if converged and index == 0
                    else "Wannier90 final iterate"
                    if index == 0
                    else None
                ),
            )
        axis.set_xticks(
            range(len(groups)),
            [self._string(group["id"]).replace("_", " ") for group in groups],
        )
        axis.set_ylabel("center / cell")
        axis.set_title("Wannier-center comparison")
        axis.grid(True, alpha=0.3)
        axis.legend(fontsize="small")

    def _plot_spreads(
        self,
        axis: plt.Axes,
        groups: tuple[dict[str, JsonValue], ...],
        converged: bool,
    ) -> None:
        positions = np.arange(len(groups), dtype=np.float64)
        width = 0.34
        for function_index in range(2):
            values = [
                self._real(self._array(group["spreads_cell_squared"])[function_index])
                for group in groups
            ]
            axis.bar(
                positions + (function_index - 0.5) * width,
                values,
                width,
                label=f"WF {function_index + 1}",
            )
        axis.set_xticks(
            positions,
            [self._string(group["id"]).replace("_", " ") for group in groups],
        )
        axis.set_yscale("log")
        axis.set_ylabel(r"spread / cell$^2$")
        axis.set_title(
            "Individual Wannier spreads"
            if converged
            else "Final-iterate Wannier spreads"
        )
        axis.grid(True, axis="y", which="both", alpha=0.3)
        axis.legend(fontsize="small")

    def _plot_range_errors(
        self,
        axis: plt.Axes,
        groups: tuple[dict[str, JsonValue], ...],
        direct_groups: dict[str, dict[str, JsonValue]],
    ) -> None:
        for group in groups:
            identifier = self._string(group["id"])
            display_name = identifier.replace("_", " ")
            records = self._records(group["range_study"])
            direct_records = self._records(direct_groups[identifier]["range_study"])
            ranges = [
                self._integer(record["hopping_range_cells"]) for record in records
            ]
            axis.semilogy(
                ranges,
                [
                    self._real(record["wannier90_training_eigenvalue_maximum_error"])
                    for record in records
                ],
                marker="s",
                linestyle="--",
                label=f"{display_name}, Wannier90",
            )
            axis.semilogy(
                ranges,
                [
                    self._real(record["smooth_withheld_eigenvalue_maximum_error"])
                    for record in direct_records
                ],
                marker="o",
                label=f"{display_name}, direct polar",
            )
        axis.set_xlabel(r"block-hopping range $r_c/a$")
        axis.set_ylabel(r"maximum eigenvalue error / $E_G$")
        axis.set_title("Finite-range accuracy")
        axis.grid(True, which="both", alpha=0.3)
        axis.legend(fontsize="small")

    def _plot_diagnostics(
        self, axis: plt.Axes, groups: tuple[dict[str, JsonValue], ...]
    ) -> None:
        labels: list[str] = []
        values: list[float] = []
        for group in groups:
            identifier = self._string(group["id"]).replace("_", " ")
            for short, key in (
                ("alignment", "pointwise_alignment_operator_maximum_frobenius_defect"),
                ("spectrum", "wannier90_represented_eigenvalue_maximum_defect"),
                ("serialized", "hr_training_eigenvalue_maximum_error"),
                ("center", "center_set_circular_maximum_defect"),
            ):
                labels.append(f"{identifier}\n{short}")
                values.append(self._real(group[key]))
        axis.bar(range(len(values)), values)
        axis.set_xticks(range(len(values)), labels, rotation=35, ha="right")
        axis.set_yscale("log")
        axis.set_ylabel("defect")
        axis.set_title("Residual diagnostic scales")
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
    def _boolean(value: JsonValue) -> bool:
        if not isinstance(value, bool):
            raise TypeError("value must be a Boolean")
        return value

    @staticmethod
    def _string(value: JsonValue) -> str:
        if not isinstance(value, str):
            raise TypeError("value must be a string")
        return value


class CommandAdapter:
    """Adapt retained result paths to the plotter."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("result", type=Path)
        parser.add_argument("--composite", type=Path, required=True)
        parser.add_argument("--output", type=Path, required=True)
        args = parser.parse_args(argv)
        Wannier90ComparisonPlotter().execute(
            cast(Path, args.result).resolve(),
            cast(Path, args.composite).resolve(),
            cast(Path, args.output).resolve(),
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
