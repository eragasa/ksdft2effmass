#!/usr/bin/env python3
"""Plot the finite-rank analytical-oracle diagnostics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import cast

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


class AnalyticalOracleSummaryPlotter:
    """Render spectral, state, finite-size, and special-control evidence."""

    __slots__ = ()

    def execute(self, result_path: Path, output_path: Path) -> None:
        result = self._load(result_path)
        figure, grid = plt.subplots(2, 2, figsize=(11.0, 8.2))
        axes = cast(np.ndarray[tuple[int, int], np.dtype[np.object_]], grid)
        self._plot_energy_error(axes[0, 0], result)
        self._plot_binding(axes[0, 1], result)
        self._plot_state_error(axes[1, 0], result)
        self._plot_special_controls(axes[1, 1], result)
        figure.suptitle(
            "Finite-rank resolvent oracle for synthetic 1D bound states",
            fontsize=14,
            fontweight="bold",
        )
        figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.96))
        output_path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(output_path, dpi=180)
        plt.close(figure)

    def _plot_energy_error(self, axis: Axes, result: dict[str, JsonValue]) -> None:
        records = self._records(result["rank_one_sweep"], "sweep")
        for magnitude in self._magnitudes(records):
            selected = self._for_magnitude(records, magnitude)
            axis.plot(
                [self._integer(item["cell_count"], "cell count") for item in selected],
                [
                    max(self._real(item["energy_absolute_discrepancy"]), 1.0e-18)
                    for item in selected
                ],
                marker="o",
                label=f"g={magnitude:g}",
            )
        axis.axhline(1.0e-11, color="black", linestyle="--", linewidth=1.0)
        axis.set_yscale("log")
        axis.set_xlabel("supercell cells")
        axis.set_ylabel("absolute energy discrepancy ($E_G$)")
        axis.set_title("(a) Resolvent root versus eigensolve")
        axis.grid(True, which="both", alpha=0.25)
        axis.legend(frameon=False, fontsize=8)

    def _plot_binding(self, axis: Axes, result: dict[str, JsonValue]) -> None:
        records = self._records(result["rank_one_sweep"], "sweep")
        for magnitude in self._magnitudes(records):
            selected = self._for_magnitude(records, magnitude)
            axis.plot(
                [self._integer(item["cell_count"], "cell count") for item in selected],
                [self._real(item["binding_below_host_edge"]) for item in selected],
                marker="o",
                label=f"g={magnitude:g}",
            )
        axis.set_yscale("log")
        axis.set_xlabel("supercell cells")
        axis.set_ylabel("binding below finite-host edge ($E_G$)")
        axis.set_title("(b) Finite-size sequence (not a continuum limit)")
        axis.grid(True, which="both", alpha=0.25)
        axis.legend(frameon=False, fontsize=8)

    def _plot_state_error(self, axis: Axes, result: dict[str, JsonValue]) -> None:
        records = self._records(result["rank_one_sweep"], "sweep")
        for magnitude in self._magnitudes(records):
            selected = self._for_magnitude(records, magnitude)
            axis.plot(
                [self._integer(item["cell_count"], "cell count") for item in selected],
                [
                    max(self._real(item["projector_frobenius_defect"]), 1.0e-18)
                    for item in selected
                ],
                marker="o",
                label=f"g={magnitude:g}",
            )
        axis.axhline(1.0e-9, color="black", linestyle="--", linewidth=1.0)
        axis.set_yscale("log")
        axis.set_xlabel("supercell cells")
        axis.set_ylabel("projector Frobenius defect")
        axis.set_title("(c) Bound-state subspace agreement")
        axis.grid(True, which="both", alpha=0.25)
        axis.legend(frameon=False, fontsize=8)

    def _plot_special_controls(self, axis: Axes, result: dict[str, JsonValue]) -> None:
        controls = self._mapping(result["special_controls"], "special controls")
        rows = [
            ["zero coupling", self._status(controls, "threshold"), "0 below edge"],
            ["repulsive", self._status(controls, "repulsive"), "0 below edge"],
            ["spin-degenerate", self._status(controls, "spin_degenerate"), "rank 2"],
            ["unequal rank", self._status(controls, "unequal_rank"), "structured stop"],
        ]
        axis.axis("off")
        table = axis.table(
            cellText=rows,
            colLabels=["control", "outcome", "comparison"],
            loc="center",
            cellLoc="left",
            colLoc="left",
            colWidths=[0.30, 0.43, 0.27],
        )
        table.auto_set_font_size(False)
        table.set_fontsize(8.0)
        table.scale(1.0, 1.6)
        for (row, _column), cell in table.get_celld().items():
            if row == 0:
                cell.set_facecolor("#d9e6f2")
                cell.set_text_props(fontweight="bold")
            elif row % 2 == 0:
                cell.set_facecolor("#f2f2f2")
        degenerate = self._mapping(controls["spin_degenerate"], "degenerate")
        axis.text(
            0.5,
            0.17,
            (
                "Rank-2 projector defect: "
                f"{self._real(degenerate['projector_frobenius_defect']):.3e}"
            ),
            transform=axis.transAxes,
            ha="center",
            fontsize=8.5,
        )
        axis.set_title("(d) Threshold, no-state, and rank controls", pad=12)

    def _status(self, controls: dict[str, JsonValue], key: str) -> str:
        record = self._mapping(controls[key], key)
        self._string(record["status"], "status")
        labels = {
            "threshold": "threshold",
            "repulsive": "no lower bound state",
            "spin_degenerate": "oracle agreement",
            "unequal_rank": "stopped",
        }
        if key not in labels:
            raise ValueError("unknown special control")
        return labels[key]

    def _magnitudes(
        self, records: tuple[dict[str, JsonValue], ...]
    ) -> tuple[float, ...]:
        return tuple(
            sorted({self._real(item["attractive_magnitude"]) for item in records})
        )

    def _for_magnitude(
        self, records: tuple[dict[str, JsonValue], ...], magnitude: float
    ) -> tuple[dict[str, JsonValue], ...]:
        return tuple(
            item
            for item in records
            if self._real(item["attractive_magnitude"]) == magnitude
        )

    @staticmethod
    def _load(path: Path) -> dict[str, JsonValue]:
        value = cast(JsonValue, json.loads(path.read_text(encoding="utf-8")))
        if not isinstance(value, dict):
            raise TypeError("result root must be an object")
        return value

    @staticmethod
    def _mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be an object")
        return value

    def _records(self, value: JsonValue, name: str) -> tuple[dict[str, JsonValue], ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be an array")
        return tuple(self._mapping(item, name) for item in value)

    @staticmethod
    def _string(value: JsonValue, name: str) -> str:
        if not isinstance(value, str) or not value:
            raise TypeError(f"{name} must be a nonempty string")
        return value

    @staticmethod
    def _integer(value: JsonValue, name: str) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an integer")
        return value

    @staticmethod
    def _real(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("value must be numeric")
        return float(value)


def main() -> None:
    """Adapt retained result and output paths into the plotting action."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    AnalyticalOracleSummaryPlotter().execute(
        arguments.result.resolve(), arguments.output.resolve()
    )


if __name__ == "__main__":
    main()
