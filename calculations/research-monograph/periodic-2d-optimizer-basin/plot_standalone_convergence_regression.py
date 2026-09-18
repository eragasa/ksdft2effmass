#!/usr/bin/env python3
"""Plot the post-hoc censored convergence-iteration regression."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import cast

import matplotlib.pyplot as plt
import numpy as np
from execute_study import JsonValue


class CensoredConvergenceRegressionPlotter:
    """Render category time ratios and selected convergence curves."""

    __slots__ = ()

    def execute(self, result_path: Path, output_path: Path) -> None:
        result = self._mapping(
            cast(JsonValue, json.loads(result_path.read_text(encoding="utf-8")))
        )
        estimates = [
            self._mapping(value) for value in self._array(result["category_estimates"])
        ]
        figure, axes = plt.subplots(1, 2, figsize=(13.5, 7.5), constrained_layout=True)
        self._forest_panel(axes[0], estimates)
        self._probability_panel(axes[1], estimates)
        figure.suptitle(
            "Post-hoc right-censored regression of native convergence iterations",
            fontsize=14,
        )
        figure.savefig(output_path, dpi=220)
        plt.close(figure)

    def _forest_panel(
        self, axis: plt.Axes, estimates: list[dict[str, JsonValue]]
    ) -> None:
        positions = np.arange(len(estimates))
        ratios = np.asarray(
            [self._real(value["time_ratio"]) for value in estimates], dtype=float
        )
        intervals = np.asarray(
            [
                self._reals(value["time_ratio_95_percent_interval"])
                for value in estimates
            ],
            dtype=float,
        )
        lower = ratios - intervals[:, 0]
        upper = intervals[:, 1] - ratios
        censored = np.asarray(
            [self._integer(value["right_censored_count"]) for value in estimates],
            dtype=float,
        )
        colors = plt.colormaps["viridis"](censored / 16.0)
        axis.errorbar(
            ratios,
            positions,
            xerr=np.vstack((lower, upper)),
            fmt="none",
            ecolor="#555555",
            elinewidth=1.0,
            capsize=2.5,
        )
        axis.scatter(ratios, positions, c=colors, s=44, zorder=3)
        axis.axvline(1.0, color="black", linestyle=":", label="fixed $N=23$ reference")
        axis.set_xscale("log")
        axis.set_yticks(
            positions,
            [self._string(value["label"]) for value in estimates],
        )
        axis.invert_yaxis()
        axis.set_xlabel(
            "adjusted convergence-time ratio (exploratory 95% model interval)"
        )
        axis.set_title("Configuration effects adjusted for deterministic start")
        axis.grid(axis="x", alpha=0.25)
        axis.legend(fontsize=8, loc="lower right")
        colorbar = axis.figure.colorbar(
            plt.cm.ScalarMappable(cmap="viridis", norm=plt.Normalize(0, 16)),
            ax=axis,
            location="bottom",
            fraction=0.05,
            pad=0.10,
            aspect=35,
        )
        colorbar.set_label("right-censored trajectories of 16")

    def _probability_panel(
        self, axis: plt.Axes, estimates: list[dict[str, JsonValue]]
    ) -> None:
        selected_labels = {
            r"fixed $N=11$",
            r"fixed $N=23$",
            r"fixed $N=27$",
            r"fixed $N=31$",
            r"fixed $N=23$, preconditioner off",
        }
        for estimate in estimates:
            label = self._string(estimate["label"])
            if label not in selected_labels:
                continue
            records = [
                self._mapping(value)
                for value in self._array(estimate["predicted_convergence_probability"])
            ]
            axis.plot(
                [self._integer(value["iterations"]) for value in records],
                [self._real(value["probability"]) for value in records],
                "o-",
                label=label,
            )
        axis.axvline(5000, color="black", linestyle=":", label="initial limit")
        axis.axvline(20000, color="#666666", linestyle="--", label="final limit")
        axis.set_xscale("log")
        axis.set_ylim(-0.02, 1.02)
        axis.set_xlabel("cumulative optimizer iterations")
        axis.set_ylabel("modelled probability of native convergence")
        axis.set_title("Selected adjusted convergence curves")
        axis.grid(alpha=0.25)
        axis.legend(fontsize=8, loc="upper left")
        axis.text(
            0.03,
            0.08,
            "Exploratory log-normal AFT model; nonconverged endpoints "
            "are right-censored",
            transform=axis.transAxes,
            fontsize=8,
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

    def _reals(self, value: JsonValue) -> list[float]:
        return [self._real(item) for item in self._array(value)]


class CommandAdapter:
    """Adapt regression-result and image paths to the plotter."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--result", type=Path, required=True)
        parser.add_argument("--output", type=Path, required=True)
        arguments = parser.parse_args(argv)
        CensoredConvergenceRegressionPlotter().execute(
            cast(Path, arguments.result).resolve(),
            cast(Path, arguments.output).resolve(),
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
