#!/usr/bin/env python3
"""Plot the synthetic blind-alignment benchmark summary."""

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


class BlindAlignmentSummaryPlotter:
    """Render retained map, extraction, spectral, and stopping diagnostics."""

    __slots__ = ()

    def execute(
        self, result_path: Path, output_path: Path, diagnostics_output_path: Path
    ) -> None:
        result = self._load(result_path)
        figure, grid = plt.subplots(2, 2, figsize=(11.0, 8.2))
        axes = cast(np.ndarray[tuple[int, int], np.dtype[np.object_]], grid)
        self._plot_noise(axes[0, 0], result)
        self._plot_exact(axes[0, 1], result)
        self._plot_gauge(axes[1, 0], result)
        self._plot_stops(axes[1, 1], result)
        figure.suptitle(
            "Synthetic blind alignment: inference, conditioning, and stopping",
            fontsize=14,
            fontweight="bold",
        )
        figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.96))
        output_path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(output_path, dpi=180)
        plt.close(figure)
        self._plot_diagnostics(result, diagnostics_output_path)

    def _plot_diagnostics(
        self, result: dict[str, JsonValue], output_path: Path
    ) -> None:
        diagnostic = self._mapping(
            result["debugging_diagnostics"], "debugging diagnostics"
        )
        figure, grid = plt.subplots(2, 2, figsize=(11.0, 8.2))
        axes = cast(np.ndarray[tuple[int, int], np.dtype[np.object_]], grid)
        self._plot_condition_boundary(axes[0, 0], diagnostic)
        self._plot_angle_boundary(axes[0, 1], diagnostic)
        self._plot_energy_boundary(axes[1, 0], diagnostic)
        self._plot_reconciliations(axes[1, 1], diagnostic)
        figure.suptitle(
            "Debugging the five structured alignment stops",
            fontsize=14,
            fontweight="bold",
        )
        figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.96))
        output_path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(output_path, dpi=180)
        plt.close(figure)

    def _plot_condition_boundary(
        self, axis: Axes, diagnostic: dict[str, JsonValue]
    ) -> None:
        records = self._records(
            diagnostic["conditioning_boundary"], "conditioning boundary"
        )
        passing = [item for item in records if item["status"] == "aligned_full"]
        stopped = [item for item in records if item["status"] == "stopped"]
        conditions = np.asarray(
            [self._real(item["anchor_condition_number"]) for item in passing]
        )
        map_error = np.asarray(
            [
                self._real(item["phase_quotiented_alignment_frobenius_defect"])
                for item in passing
            ]
        )
        extraction = np.asarray(
            [self._real(item["extraction_frobenius_defect"]) for item in passing]
        )
        axis.loglog(conditions, map_error, "o-", label="map defect")
        axis.loglog(conditions, extraction, "s-", label="extraction defect")
        if stopped:
            stop_conditions = np.asarray(
                [self._real(item["anchor_condition_number"]) for item in stopped]
            )
            axis.scatter(
                stop_conditions,
                np.full(stop_conditions.shape, 1.0e-8),
                marker="x",
                s=55,
                color="#c44e52",
                label="structured stop",
            )
        axis.axvline(1.0e6, color="black", linestyle="--", linewidth=1.0)
        axis.set_xlabel("anchor condition number")
        axis.set_ylabel("absolute defect")
        axis.set_title("(a) Conditioning boundary")
        axis.grid(True, which="both", alpha=0.25)
        axis.legend(frameon=False, fontsize=8)

    def _plot_angle_boundary(
        self, axis: Axes, diagnostic: dict[str, JsonValue]
    ) -> None:
        records = self._records(
            diagnostic["principal_angle_boundary"], "angle boundary"
        )
        angles = np.asarray(
            [self._real(item["requested_principal_angle_radians"]) for item in records]
        )
        accepted = np.asarray(
            [1.0 if item["status"] == "aligned_full" else 0.0 for item in records]
        )
        axis.step(angles, accepted, where="mid", color="#4c72b0")
        axis.scatter(
            angles[accepted > 0.5],
            accepted[accepted > 0.5],
            marker="o",
            color="#55a868",
            label="aligned",
        )
        axis.scatter(
            angles[accepted < 0.5],
            accepted[accepted < 0.5],
            marker="x",
            s=55,
            color="#c44e52",
            label="stopped",
        )
        axis.axvline(0.35, color="black", linestyle="--", linewidth=1.0)
        axis.set_yticks([0.0, 1.0], ["stop", "align"])
        axis.set_ylim(-0.15, 1.15)
        axis.set_xlabel("maximum principal angle (rad)")
        axis.set_title("(b) Retained-subspace boundary")
        axis.grid(True, axis="x", alpha=0.25)
        axis.legend(frameon=False, fontsize=8)

    def _plot_energy_boundary(
        self, axis: Axes, diagnostic: dict[str, JsonValue]
    ) -> None:
        records = self._records(diagnostic["energy_anchor_boundary"], "energy boundary")
        ranks = np.asarray(
            [
                self._integer(item["requested_energy_anchor_rank"], "energy rank")
                for item in records
            ]
        )
        accepted = np.asarray(
            [1.0 if item["status"] == "aligned_full" else 0.0 for item in records]
        )
        axis.step(ranks, accepted, where="mid", color="#4c72b0")
        axis.scatter(
            ranks[accepted > 0.5],
            accepted[accepted > 0.5],
            marker="o",
            color="#55a868",
            label="shift identified",
        )
        axis.scatter(
            ranks[accepted < 0.5],
            accepted[accepted < 0.5],
            marker="x",
            s=55,
            color="#c44e52",
            label="structured stop",
        )
        axis.axvline(3.5, color="black", linestyle="--", linewidth=1.0)
        axis.set_yticks([0.0, 1.0], ["stop", "align"])
        axis.set_ylim(-0.15, 1.15)
        axis.set_xlabel("exterior energy-anchor rank")
        axis.set_title("(c) Energy-reference boundary")
        axis.grid(True, axis="x", alpha=0.25)
        axis.legend(frameon=False, fontsize=8)

    def _plot_reconciliations(
        self, axis: Axes, diagnostic: dict[str, JsonValue]
    ) -> None:
        rank = self._mapping(diagnostic["rank_reconciliation"], "rank reconciliation")
        spin = self._mapping(diagnostic["spin_reconciliation"], "spin reconciliation")
        lifted = self._mapping(spin["lifted_alignment"], "lifted alignment")
        rows = [
            [
                "rank mismatch",
                "rectangular partial isometry",
                f"{self._real(rank['phase_quotiented_alignment_frobenius_defect']):.2e}",
                f"{self._real(rank['extraction_frobenius_defect']):.2e}",
            ],
            [
                "spin mismatch",
                "explicit spin lift",
                f"{self._real(lifted['phase_quotiented_alignment_frobenius_defect']):.2e}",
                f"{self._real(lifted['extraction_frobenius_defect']):.2e}",
            ],
        ]
        axis.axis("off")
        table = axis.table(
            cellText=rows,
            colLabels=["original stop", "declared resolution", "map", "extraction"],
            loc="center",
            cellLoc="left",
            colLoc="left",
            colWidths=[0.24, 0.38, 0.19, 0.19],
        )
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1.0, 1.7)
        for (row, _column), cell in table.get_celld().items():
            if row == 0:
                cell.set_facecolor("#d9e6f2")
                cell.set_text_props(fontweight="bold")
            elif row % 2 == 0:
                cell.set_facecolor("#f2f2f2")
        restriction = self._real(spin["spin_independent_restriction_residual"])
        axis.text(
            0.5,
            0.22,
            f"Spin-mixing restriction residual: {restriction:.3e}",
            transform=axis.transAxes,
            ha="center",
            fontsize=9,
        )
        axis.set_title("(d) Explicit rank and spin reconciliation", pad=12)

    def _plot_noise(self, axis: Axes, result: dict[str, JsonValue]) -> None:
        records = self._records(result["noise_sweep"], "noise sweep")
        noise = np.asarray(
            [
                max(self._real(item["unitary_noise_radians"]), 1.0e-16)
                for item in records
            ]
        )
        map_error = np.asarray(
            [
                self._real(item["phase_quotiented_alignment_frobenius_defect"])
                for item in records
            ]
        )
        extraction = np.asarray(
            [self._real(item["extraction_frobenius_defect"]) for item in records]
        )
        spectral = np.asarray(
            [
                self._real(item["active_spectral_maximum_absolute_defect"])
                for item in records
            ]
        )
        axis.loglog(noise, map_error, "o-", label="alignment map")
        axis.loglog(noise, extraction, "s-", label="extracted operator")
        axis.loglog(noise, spectral, "^-", label="active spectrum")
        axis.set_xlabel("authored unitary anchor noise (rad)")
        axis.set_ylabel("absolute defect")
        axis.set_title("(a) Noise response")
        axis.grid(True, which="both", alpha=0.25)
        axis.legend(frameon=False, fontsize=8)

    def _plot_exact(self, axis: Axes, result: dict[str, JsonValue]) -> None:
        records = self._records(result["exact_full_rank_cases"], "exact cases")
        labels = [self._string(item["id"], "exact id") for item in records]
        x_values = np.arange(len(records))
        width = 0.24
        map_error = [
            self._real(item["phase_quotiented_alignment_frobenius_defect"])
            for item in records
        ]
        extraction = [
            self._real(item["extraction_frobenius_defect"]) for item in records
        ]
        shift_error = [
            max(abs(self._real(item["energy_shift_error"])), 1.0e-18)
            for item in records
        ]
        axis.bar(x_values - width, map_error, width, label="map")
        axis.bar(x_values, extraction, width, label="extraction")
        axis.bar(x_values + width, shift_error, width, label="energy shift")
        axis.set_yscale("log")
        axis.set_xticks(x_values, labels)
        axis.set_ylabel("absolute defect")
        axis.set_title("(b) Exact full-rank controls")
        axis.grid(True, axis="y", which="both", alpha=0.25)
        axis.legend(frameon=False, fontsize=8)

    def _plot_gauge(self, axis: Axes, result: dict[str, JsonValue]) -> None:
        record = self._mapping(result["gauge_equivalent_case"], "gauge case")
        labels = ["full completion", "compressed operator", "partial map"]
        values = [
            self._real(record["full_completion_extraction_disagreement"]),
            self._real(record["compressed_completion_extraction_disagreement"]),
            self._real(record["partial_map_agreement_between_completions"]),
        ]
        colors = ["#c44e52", "#4c72b0", "#55a868"]
        axis.bar(labels, values, color=colors)
        axis.set_yscale("log")
        axis.set_ylabel("Frobenius disagreement")
        axis.set_title("(c) Gauge-equivalent partial alignment")
        axis.tick_params(axis="x", rotation=17)
        axis.grid(True, axis="y", which="both", alpha=0.25)
        identified = self._integer(record["identified_dimension"], "identified")
        total = self._integer(record["dimension"], "dimension")
        axis.text(
            0.98,
            0.95,
            f"identified sector: {identified}/{total}",
            transform=axis.transAxes,
            ha="right",
            va="top",
            fontsize=9,
        )

    def _plot_stops(self, axis: Axes, result: dict[str, JsonValue]) -> None:
        records = self._records(result["stopping_cases"], "stopping cases")
        axis.axis("off")
        rows: list[list[str]] = []
        for record in records:
            issues = record["issue_codes"]
            if not isinstance(issues, list) or len(issues) != 1:
                raise ValueError("each stopping case must have one issue")
            rows.append(
                [
                    self._string(record["id"], "stop id").replace("-", " "),
                    self._string(issues[0], "issue").removeprefix("BLIND_ALIGNMENT."),
                ]
            )
        table = axis.table(
            cellText=rows,
            colLabels=["control", "structured outcome"],
            loc="center",
            cellLoc="left",
            colLoc="left",
            colWidths=[0.50, 0.50],
        )
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1.0, 1.55)
        for (row, _column), cell in table.get_celld().items():
            if row == 0:
                cell.set_facecolor("#d9e6f2")
                cell.set_text_props(fontweight="bold")
            elif row % 2 == 0:
                cell.set_facecolor("#f2f2f2")
        axis.set_title("(d) Structured stopping controls", pad=12)

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
    def _real(value: JsonValue, name: str = "value") -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be numeric")
        return float(value)

    @staticmethod
    def _integer(value: JsonValue, name: str) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an integer")
        return value


def main() -> None:
    """Adapt result and output paths into the owned plotting action."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--diagnostics-output", type=Path, required=True)
    arguments = parser.parse_args()
    BlindAlignmentSummaryPlotter().execute(
        arguments.result.resolve(),
        arguments.output.resolve(),
        arguments.diagnostics_output.resolve(),
    )


if __name__ == "__main__":
    main()
