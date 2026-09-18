#!/usr/bin/env python3
"""Plot the bounded non-DFT Wannier90 study."""

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


class Wannier90StudyPlotter:
    """Render convergence and auxiliary-embedding sensitivity."""

    __slots__ = ("_result",)

    def __init__(self, payload: bytes) -> None:
        value = cast(JsonValue, json.loads(payload.decode("utf-8")))
        self._result = self._mapping(value)

    def execute(self) -> Figure:
        reference = self._mapping(self._result["reference_case"])
        cases = [self._mapping(value) for value in self._array(self._result["cases"])]
        records = [reference, *cases]
        labels = ["ref", "N=11", "N=19", "P=2", "P=4", "c=12", "c=18"]
        summaries = [self._mapping(record["summary"]) for record in records]
        native = np.array(
            [
                self._real(value["native_total_spread_cell_squared"])
                for value in summaries
            ]
        )
        common = np.array(
            [
                self._real(value["common_wannier90_total_spread_cell_squared"])
                for value in summaries
            ]
        )
        ratios = np.array(
            [
                self._real(value["common_wannier90_to_direct_ratio"])
                for value in summaries
            ]
        )
        tails = np.array(
            [
                self._real(value["radius_50_hopping_tail_energy_units"])
                for value in summaries
            ]
        )
        iterations = np.array(
            [self._integer(value["iterations"]) for value in summaries]
        )
        center_defects = np.array(
            [
                0.0,
                *[
                    self._real(
                        self._mapping(record["difference_from_reference"])[
                            "common_center_set_maximum_periodic_distance"
                        ]
                    )
                    for record in cases
                ],
            ]
        )
        positions = np.arange(len(records), dtype=float)
        figure, axes = plt.subplots(2, 2, figsize=(10.5, 7.4), constrained_layout=True)
        width = 0.38
        axes[0, 0].bar(positions - width / 2, native, width, label="native Berry-link")
        axes[0, 0].bar(
            positions + width / 2, common, width, label="common finite-supercell"
        )
        axes[0, 0].set_ylabel("total spread / cell$^2$")
        axes[0, 0].set_title("Estimator-resolved spread")
        axes[0, 0].legend(fontsize=8)
        axes[0, 1].plot(positions, ratios, "o-", color="#0072B2")
        axes[0, 1].set_ylabel("common Wannier90/direct ratio")
        axes[0, 1].set_title("Localization ratio")
        positive_tails = np.where(tails > 0.0, tails, np.nan)
        axes[1, 0].semilogy(positions, positive_tails, "s-", color="#D55E00")
        axes[1, 0].scatter(
            positions[tails == 0.0],
            np.full(np.sum(tails == 0.0), 1e-7),
            marker="v",
            color="#D55E00",
        )
        axes[1, 0].set_ylabel("radius-50 hopping tail / $E_G$")
        axes[1, 0].set_title("Finite-mesh hopping tail")
        axes[1, 1].plot(
            positions, center_defects, "o-", color="#009E73", label="center-set defect"
        )
        axes[1, 1].set_ylabel("periodic center-set distance")
        twin = axes[1, 1].twinx()
        twin.plot(positions, iterations, "s--", color="#CC79A7", label="iterations")
        twin.set_ylabel("Wannier90 iterations")
        axes[1, 1].set_title("Center sensitivity and iterations")
        for axis in axes.ravel():
            axis.set_xticks(positions, labels, rotation=35, ha="right")
            axis.grid(alpha=0.25)
        figure.suptitle("Periodic-2D bounded non-DFT Wannier90 study")
        return figure

    def _mapping(self, value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("expected a mapping")
        return value

    def _array(self, value: JsonValue) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError("expected an array")
        return value

    def _real(self, value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("expected a real number")
        return float(value)

    def _integer(self, value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("expected an integer")
        return value


def main() -> None:
    """CLI entry point required by the plotting-script boundary."""
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    result_path = cast(Path, arguments.result).resolve()
    output_path = cast(Path, arguments.output).resolve()
    figure = Wannier90StudyPlotter(result_path.read_bytes()).execute()
    figure.savefig(output_path, dpi=220)
    plt.close(figure)


if __name__ == "__main__":
    main()
