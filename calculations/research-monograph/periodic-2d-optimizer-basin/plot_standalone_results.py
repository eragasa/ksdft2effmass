#!/usr/bin/env python3
"""Plot the completed standalone optimizer-convergence study."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import cast

import matplotlib.pyplot as plt
import numpy as np
from execute_study import JsonValue


class StandaloneResultPlotter:
    """Render convergence, spread, holdout, and optimizer-control diagnostics."""

    __slots__ = ()

    def execute(self, result_path: Path, output_path: Path) -> None:
        result = self._mapping(
            cast(JsonValue, json.loads(result_path.read_text(encoding="utf-8")))
        )
        assessment = self._mapping(result["convergence_assessment"])
        fixed = [
            self._mapping(value)
            for value in self._array(assessment["fixed_embedding_mesh_sequence"])
        ]
        balanced = [
            self._mapping(value)
            for value in self._array(assessment["balanced_embedding_mesh_sequence"])
        ]
        groups = [self._mapping(value) for value in self._array(result["groups"])]
        figure, axes = plt.subplots(2, 3, figsize=(15.0, 8.5), constrained_layout=True)
        self._convergence_panel(axes[0, 0], fixed, balanced)
        self._spread_panel(axes[0, 1], fixed)
        self._holdout_panel(axes[0, 2], assessment)
        self._control_panel(axes[1, 0], assessment)
        self._basin_sensitivity_panel(axes[1, 1], groups)
        self._numerical_control_panel(axes[1, 2], groups)
        figure.suptitle(
            "Expanded periodic-2D optimizer and discretization study",
            fontsize=14,
        )
        figure.savefig(output_path, dpi=220)
        plt.close(figure)

    def _convergence_panel(
        self,
        axis: plt.Axes,
        fixed: list[dict[str, JsonValue]],
        balanced: list[dict[str, JsonValue]],
    ) -> None:
        mesh = [self._integer(value["reciprocal_mesh_size"]) for value in fixed]
        axis.plot(
            mesh,
            [
                self._real(value["effective_native_converged_fraction"])
                for value in fixed
            ],
            "o-",
            label=r"fixed $c=31$",
        )
        axis.plot(
            mesh,
            [
                self._real(value["effective_native_converged_fraction"])
                for value in balanced
            ],
            "s--",
            label=r"balanced $c=N$",
        )
        axis.axhline(0.75, color="black", linestyle=":", label="frozen minimum")
        axis.set_ylim(-0.03, 1.05)
        axis.set_xlabel(r"reciprocal mesh $N$")
        axis.set_ylabel("final converged-start fraction")
        axis.set_title("Native convergence after continuation")
        axis.grid(alpha=0.25)
        axis.legend(fontsize=8)

    def _spread_panel(self, axis: plt.Axes, fixed: list[dict[str, JsonValue]]) -> None:
        mesh = [self._integer(value["reciprocal_mesh_size"]) for value in fixed]
        omega_i = [
            self._real(
                self._mapping(value["best_observed_converged"])["omega_i_cell_squared"]
            )
            for value in fixed
        ]
        omega_tilde = [
            self._real(
                self._mapping(value["best_observed_converged"])[
                    "omega_tilde_cell_squared"
                ]
            )
            for value in fixed
        ]
        median_tilde = [
            self._real(
                self._mapping(value["median_across_converged"])[
                    "omega_tilde_cell_squared"
                ]
            )
            for value in fixed
        ]
        axis.plot(mesh, omega_i, "o-", label=r"best-start $\Omega_I$")
        axis.plot(mesh, omega_tilde, "s-", label=r"best $\widetilde\Omega$")
        axis.plot(mesh, median_tilde, "^--", label=r"median $\widetilde\Omega$")
        axis.set_xlabel(r"reciprocal mesh $N$")
        axis.set_ylabel(r"spread ($a^2$)")
        axis.set_title("Fixed-embedding spread components")
        axis.grid(alpha=0.25)
        axis.legend(fontsize=8)

    def _holdout_panel(self, axis: plt.Axes, assessment: dict[str, JsonValue]) -> None:
        holdout = self._mapping(assessment["fixed_embedding_holdout"])
        records = [self._mapping(value) for value in self._array(holdout["records"])]
        labels = [
            f"{self._string(value['summary'])} "
            + {
                "omega_i_cell_squared": r"$\Omega_I$",
                "omega_tilde_cell_squared": r"$\widetilde\Omega$",
                "radius_18_hopping_tail_energy_units": r"tail",
            }[self._string(value["metric"])]
            for value in records
        ]
        residuals = [
            100.0 * self._real(value["relative_residual"]) for value in records
        ]
        colors = [
            "#2b8cbe" if value["pass"] is True else "#d7301f" for value in records
        ]
        positions = np.arange(len(records))
        axis.bar(positions, residuals, color=colors)
        axis.axhline(1.0, color="black", linestyle=":", label="1% maximum")
        axis.set_xticks(positions, labels, rotation=30, ha="right")
        axis.set_ylabel(r"$N=31$ holdout residual (%)")
        axis.set_title(r"Fit $a+b/N^2$ on $N=15,19,23,27$")
        axis.grid(axis="y", alpha=0.25)
        axis.legend(fontsize=8)

    def _control_panel(self, axis: plt.Axes, assessment: dict[str, JsonValue]) -> None:
        controls = [
            self._mapping(value)
            for value in self._array(assessment["preconditioner_controls"])
        ]
        positions = np.arange(len(controls))
        width = 0.34
        baseline = [
            self._integer(value["baseline_final_converged_count"]) for value in controls
        ]
        disabled = [
            self._integer(value["control_final_converged_count"]) for value in controls
        ]
        axis.bar(positions - width / 2, baseline, width, label="preconditioned")
        axis.bar(positions + width / 2, disabled, width, label="preconditioner off")
        axis.set_xticks(positions, [r"fixed $c=31$", r"balanced $c=23$"])
        axis.set_ylim(0, 16.8)
        axis.set_ylabel("final converged starts of 16")
        axis.set_title(r"Optimizer control at $N=23,P=4$")
        axis.grid(axis="y", alpha=0.25)
        axis.legend(fontsize=8)

    def _basin_sensitivity_panel(
        self, axis: plt.Axes, groups: list[dict[str, JsonValue]]
    ) -> None:
        first = [
            self._mapping(value)
            for value in self._array(groups[0]["density_tolerance_sensitivity"])
        ]
        tolerances = [self._real(value["density_l2_tolerance"]) for value in first]
        pair_counts: list[int] = []
        best_occupancies: list[int] = []
        for tolerance in tolerances:
            records = [
                next(
                    self._mapping(value)
                    for value in self._array(group["density_tolerance_sensitivity"])
                    if self._real(self._mapping(value)["density_l2_tolerance"])
                    == tolerance
                )
                for group in groups
            ]
            pair_counts.append(
                sum(
                    self._integer(value["direct_matching_pair_count"])
                    for value in records
                )
            )
            best_occupancies.append(
                max(
                    self._integer(value["best_endpoint_direct_occupancy"])
                    for value in records
                )
            )
        axis.plot(tolerances, pair_counts, "o-", label="matching endpoint pairs")
        axis.axvline(1.0e-5, color="black", linestyle=":", label="frozen tolerance")
        axis.set_xscale("log")
        axis.set_xlabel(r"density $L^2$ tolerance")
        axis.set_ylabel("direct matching pairs across groups")
        axis.set_title("Post-hoc basin-threshold sensitivity")
        axis.grid(alpha=0.25)
        secondary = axis.twinx()
        secondary.plot(
            tolerances,
            best_occupancies,
            "s--",
            color="#d95f02",
            label="maximum best-endpoint occupancy",
        )
        secondary.set_ylim(0.8, 4.2)
        secondary.set_ylabel("best-endpoint direct occupancy")
        handles, labels = axis.get_legend_handles_labels()
        other_handles, other_labels = secondary.get_legend_handles_labels()
        axis.legend(handles + other_handles, labels + other_labels, fontsize=7)

    def _numerical_control_panel(
        self, axis: plt.Axes, groups: list[dict[str, JsonValue]]
    ) -> None:
        controls = [
            self._mapping(group["basin_post_hoc_numerical_controls"])
            for group in groups
        ]
        ratios = [
            max(
                self._real(value["maximum_center_set_periodic_distance_cell"])
                for value in controls
            )
            / 1.0e-3,
            max(self._real(value["maximum_density_l2_mismatch"]) for value in controls)
            / 1.0e-5,
        ]
        positions = np.arange(2)
        axis.bar(positions, ratios, color=("#7570b3", "#1b9e77"))
        axis.axhline(1.0, color="black", linestyle=":", label="frozen tolerance")
        axis.set_yscale("log")
        axis.set_xticks(positions, ("center", "density"))
        axis.set_ylabel("maximum mismatch / frozen tolerance")
        axis.set_title("Post-hoc exact-equivalence controls")
        axis.text(
            0.03,
            0.04,
            "performed after execution; protocol deviation retained",
            transform=axis.transAxes,
            fontsize=7,
        )
        axis.grid(axis="y", alpha=0.25)
        axis.legend(fontsize=7)

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
    """Adapt result and image paths to the plotter."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--result", type=Path, required=True)
        parser.add_argument("--output", type=Path, required=True)
        arguments = parser.parse_args(argv)
        StandaloneResultPlotter().execute(
            cast(Path, arguments.result).resolve(),
            cast(Path, arguments.output).resolve(),
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
