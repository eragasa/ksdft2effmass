#!/usr/bin/env python3
"""Plot the three-model topological benchmark."""

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


class TopologicalSummaryPlotter:
    """Render Wilson, Chern, gap, and curvature convergence diagnostics."""

    __slots__ = ("_result",)

    def __init__(self, payload: bytes) -> None:
        value = cast(JsonValue, json.loads(payload.decode("utf-8")))
        if not isinstance(value, dict):
            raise TypeError("result must be a mapping")
        self._result = value

    def execute(self) -> Figure:
        models_value = self._result["models"]
        if not isinstance(models_value, list):
            raise TypeError("models must be an array")
        labels = {
            "qi_wu_zhang": "Qi--Wu--Zhang",
            "hofstadter": "Hofstadter $1/3$",
            "haldane": "Haldane",
        }
        colors = {
            "qi_wu_zhang": "#0072B2",
            "hofstadter": "#D55E00",
            "haldane": "#009E73",
        }
        figure, axes = plt.subplots(2, 3, figsize=(12.0, 7.2), constrained_layout=True)
        for model_value in models_value:
            model = self._mapping(model_value)
            name = self._string(model["model"])
            cases = self._array(model["cases"])
            for case_value in cases:
                case = self._mapping(case_value)
                case_name = self._string(case["case"])
                final = self._mapping(case["final_mesh"])
                phases = np.asarray(self._reals(final["wilson_phases"]))
                coordinate = np.arange(phases.size, dtype=np.float64) / phases.size
                column = 0 if case_name == "topological" else 1
                axes[0, column].plot(
                    coordinate,
                    np.unwrap(phases) / (2.0 * np.pi),
                    color=colors[name],
                    label=labels[name],
                    linewidth=1.8,
                )
                convergence = self._array(case["convergence"])
                mesh = [
                    self._integer(self._mapping(item)["mesh_size"])
                    for item in convergence
                ]
                chern = [
                    self._real(self._mapping(item)["retained_chern"])
                    for item in convergence
                ]
                plaquette = [
                    self._real(self._mapping(item)["maximum_absolute_plaquette_phase"])
                    for item in convergence
                ]
                linestyle = "-" if case_name == "topological" else "--"
                axes[0, 2].plot(
                    mesh,
                    chern,
                    marker="o",
                    linestyle=linestyle,
                    color=colors[name],
                    label=f"{labels[name]}, {case_name}",
                )
                axes[1, 0].loglog(
                    mesh,
                    plaquette,
                    marker="o",
                    linestyle=linestyle,
                    color=colors[name],
                    label=f"{labels[name]}, {case_name}",
                )
        axes[0, 0].set_title("Topological Wilson flow")
        axes[0, 1].set_title("Trivial-control Wilson flow")
        for axis in axes[0, :2]:
            axis.set_xlabel("transverse fractional coordinate $v$")
            axis.set_ylabel("unwrapped phase / $2\\pi$")
            axis.grid(alpha=0.25)
        axes[0, 0].legend(fontsize=8)
        axes[0, 2].set_title("Chern convergence")
        axes[0, 2].set_xlabel("mesh size $N$")
        axes[0, 2].set_ylabel("retained-band Chern sum")
        axes[0, 2].grid(alpha=0.25)
        axes[0, 2].legend(fontsize=7)
        axes[1, 0].set_title("Plaquette-phase refinement")
        axes[1, 0].set_xlabel("mesh size $N$")
        axes[1, 0].set_ylabel("maximum $|\\phi_{\\mathrm{plaq}}|$")
        axes[1, 0].grid(alpha=0.25, which="both")

        model_names: list[str] = []
        topological_gaps: list[float] = []
        trivial_gaps: list[float] = []
        band_chern_labels: list[str] = []
        band_chern_values: list[float] = []
        for model_value in models_value:
            model = self._mapping(model_value)
            name = self._string(model["model"])
            model_names.append(labels[name])
            for case_value in self._array(model["cases"]):
                case = self._mapping(case_value)
                final = self._mapping(case["final_mesh"])
                case_name = self._string(case["case"])
                gap = self._real(final["minimum_retained_gap"])
                if case_name == "topological":
                    topological_gaps.append(gap)
                    for band, chern in enumerate(self._reals(final["band_cherns"])):
                        band_chern_labels.append(f"{labels[name]} b{band}")
                        band_chern_values.append(chern)
                else:
                    trivial_gaps.append(gap)
        positions = np.arange(len(model_names), dtype=np.float64)
        width = 0.36
        axes[1, 1].bar(
            positions - width / 2,
            topological_gaps,
            width,
            label="topological",
            color="#CC79A7",
        )
        axes[1, 1].bar(
            positions + width / 2,
            trivial_gaps,
            width,
            label="trivial",
            color="#56B4E9",
        )
        axes[1, 1].set_xticks(positions, model_names, rotation=18, ha="right")
        axes[1, 1].set_ylabel("minimum retained gap")
        axes[1, 1].set_title("Isolated-band controls")
        axes[1, 1].legend(fontsize=8)
        axes[1, 1].grid(axis="y", alpha=0.25)

        band_positions = np.arange(len(band_chern_labels), dtype=np.float64)
        axes[1, 2].bar(band_positions, band_chern_values, color="#E69F00")
        axes[1, 2].set_xticks(
            band_positions, band_chern_labels, rotation=40, ha="right", fontsize=7
        )
        axes[1, 2].set_ylabel("Chern sum")
        axes[1, 2].set_title("Topological-case band Chern integers")
        axes[1, 2].grid(axis="y", alpha=0.25)
        figure.suptitle(
            "Three distinct synthetic Chern-band obstruction benchmarks", fontsize=14
        )
        return figure

    def _mapping(self, value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("expected a mapping")
        return value

    def _array(self, value: JsonValue) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError("expected an array")
        return value

    def _string(self, value: JsonValue) -> str:
        if not isinstance(value, str):
            raise TypeError("expected a string")
        return value

    def _integer(self, value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("expected an integer")
        return value

    def _real(self, value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("expected a real number")
        return float(value)

    def _reals(self, value: JsonValue) -> list[float]:
        return [self._real(item) for item in self._array(value)]


def main() -> None:
    """CLI entry point required by the script boundary."""
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    figure = TopologicalSummaryPlotter(arguments.result.read_bytes()).execute()
    figure.savefig(arguments.output, dpi=220)
    plt.close(figure)


if __name__ == "__main__":
    main()
