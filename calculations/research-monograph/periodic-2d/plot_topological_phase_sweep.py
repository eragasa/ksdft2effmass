#!/usr/bin/env python3
"""Plot the three non-DFT topological parameter sweeps."""

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


class TopologicalPhaseSweepPlotter:
    """Render gaps and retained Chern sectors without combining model units."""

    __slots__ = ("_result", "_input")

    def __init__(self, result_payload: bytes, input_payload: bytes) -> None:
        self._result = self._mapping(
            cast(JsonValue, json.loads(result_payload.decode("utf-8")))
        )
        self._input = self._mapping(
            cast(JsonValue, json.loads(input_payload.decode("utf-8")))
        )

    def execute(self) -> Figure:
        figure, axes = plt.subplots(1, 3, figsize=(12.0, 3.9), constrained_layout=True)
        input_models = self._mapping(self._input["models"])
        titles = {
            "qi_wu_zhang": "Qi--Wu--Zhang",
            "hofstadter": "Hofstadter flux 1/3",
            "haldane": "Haldane",
        }
        for axis, model_value in zip(
            axes, self._array(self._result["models"]), strict=True
        ):
            model = self._mapping(model_value)
            name = self._string(model["model"])
            samples = [self._mapping(value) for value in self._array(model["samples"])]
            parameters = np.array([self._real(value["parameter"]) for value in samples])
            gaps = np.array(
                [self._real(value["minimum_retained_gap"]) for value in samples]
            )
            cherns = np.array(
                [self._integer(value["retained_chern_integer"]) for value in samples]
            )
            axis.plot(parameters, gaps, "o-", markersize=2.5, color="#0072B2")
            axis.set_xlabel(self._string(model["parameter_name"]))
            axis.set_ylabel("minimum retained gap", color="#0072B2")
            axis.tick_params(axis="y", labelcolor="#0072B2")
            axis.grid(alpha=0.25)
            twin = axis.twinx()
            twin.step(parameters, cherns, where="mid", color="#D55E00")
            twin.set_ylabel("retained Chern integer", color="#D55E00")
            twin.tick_params(axis="y", labelcolor="#D55E00")
            twin.set_yticks((-1, 0, 1))
            specification = self._mapping(input_models[name])
            for boundary in self._boundaries(name, specification):
                axis.axvline(boundary, color="black", linestyle=":", linewidth=0.9)
            axis.set_title(titles[name])
        figure.suptitle("Separate synthetic topological phase sweeps")
        return figure

    def _boundaries(
        self, model_name: str, specification: dict[str, JsonValue]
    ) -> tuple[float, ...]:
        if model_name == "qi_wu_zhang":
            return self._reals(specification["analytic_boundaries"])
        if model_name == "haldane":
            value = self._real(specification["analytic_boundary_magnitude"])
            return (-value, value)
        return tuple()

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

    def _reals(self, value: JsonValue) -> tuple[float, ...]:
        return tuple(self._real(item) for item in self._array(value))


def main() -> None:
    """CLI entry point required by the plotting-script boundary."""
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    result_path = cast(Path, arguments.result).resolve()
    input_path = cast(Path, arguments.input).resolve()
    output_path = cast(Path, arguments.output).resolve()
    figure = TopologicalPhaseSweepPlotter(
        result_path.read_bytes(), input_path.read_bytes()
    ).execute()
    figure.savefig(output_path, dpi=220)
    plt.close(figure)


if __name__ == "__main__":
    main()
