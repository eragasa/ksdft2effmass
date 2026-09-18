#!/usr/bin/env python3
"""Plot the independent-route synthetic benchmark."""

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


class IndependentRouteSummaryPlotter:
    """Render route, observable, and adversarial diagnostics."""

    __slots__ = ()

    def execute(self, result_path: Path, output_path: Path) -> None:
        result = self._load(result_path)
        figure, grid = plt.subplots(2, 2, figsize=(11.0, 8.2))
        axes = cast(np.ndarray[tuple[int, int], np.dtype[np.object_]], grid)
        self._plot_operator_errors(axes[0, 0], result)
        self._plot_observable_errors(axes[0, 1], result)
        self._plot_error_matrix(axes[1, 0], result)
        self._plot_adversarial(axes[1, 1], result)
        figure.suptitle(
            "Independent real-space and Bloch-fiber defect extraction",
            fontsize=14,
            fontweight="bold",
        )
        figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.96))
        output_path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(output_path, dpi=180)
        plt.close(figure)

    def _plot_operator_errors(self, axis: Axes, result: dict[str, JsonValue]) -> None:
        records = self._records(result["nominal_controls"], "nominal controls")
        labels = [self._short(self._string(item["id"], "id")) for item in records]
        x_values = np.arange(len(records))
        width = 0.25
        representation = [
            self._real(item["representation_frobenius_discrepancy"]) for item in records
        ]
        route = [
            self._real(item["route_noncommutativity_frobenius"]) for item in records
        ]
        recovery = [
            self._real(item["route_b_planted_recovery_defect"]) for item in records
        ]
        axis.bar(x_values - width, representation, width, label="representation")
        axis.bar(x_values, route, width, label="route")
        axis.bar(x_values + width, recovery, width, label="fiber recovery")
        axis.axhline(1.0e-11, color="black", linestyle="--", linewidth=1.0)
        axis.set_yscale("log")
        axis.set_xticks(x_values, labels, rotation=25, ha="right")
        axis.set_ylabel("Frobenius defect")
        axis.set_title("(a) Nominal operator agreement")
        axis.grid(True, axis="y", which="both", alpha=0.25)
        axis.legend(frameon=False, fontsize=8)

    def _plot_observable_errors(self, axis: Axes, result: dict[str, JsonValue]) -> None:
        records = self._records(result["nominal_controls"], "nominal controls")
        labels = [self._short(self._string(item["id"], "id")) for item in records]
        x_values = np.arange(len(records))
        width = 0.36
        spectral = [
            self._real(item["spectral_maximum_absolute_discrepancy"])
            for item in records
        ]
        projector = [
            self._real(item["lowest_eigenspace_projector_defect"]) for item in records
        ]
        axis.bar(x_values - width / 2.0, spectral, width, label="spectrum")
        axis.bar(x_values + width / 2.0, projector, width, label="lowest eigenspace")
        axis.axhline(1.0e-11, color="black", linestyle="--", linewidth=1.0)
        axis.set_yscale("log")
        axis.set_xticks(x_values, labels, rotation=25, ha="right")
        axis.set_ylabel("absolute discrepancy")
        axis.set_title("(b) Spectral and state diagnostics")
        axis.grid(True, axis="y", which="both", alpha=0.25)
        axis.legend(frameon=False, fontsize=8)

    def _plot_error_matrix(self, axis: Axes, result: dict[str, JsonValue]) -> None:
        records = self._records(result["nominal_controls"], "nominal controls")
        labels = [self._short(self._string(item["id"], "id")) for item in records]
        fields = (
            "folding_map_unitarity_defect",
            "representation_frobenius_discrepancy",
            "alignment_frobenius_defect",
            "route_a_planted_recovery_defect",
            "route_b_planted_recovery_defect",
            "route_noncommutativity_frobenius",
        )
        matrix = np.asarray(
            [
                [max(self._real(item[field]), 1.0e-18) for item in records]
                for field in fields
            ]
        )
        image = axis.imshow(np.log10(matrix), aspect="auto", cmap="viridis")
        axis.set_xticks(np.arange(len(labels)), labels, rotation=25, ha="right")
        axis.set_yticks(
            np.arange(len(fields)),
            [
                "unitarity",
                "representation",
                "alignment",
                "real recovery",
                "fiber recovery",
                "route",
            ],
        )
        axis.set_title("(c) Separated error ledger ($\\log_{10}$)")
        colorbar = axis.figure.colorbar(image, ax=axis, fraction=0.046, pad=0.04)
        colorbar.set_label("$\\log_{10}$ absolute defect")

    def _plot_adversarial(self, axis: Axes, result: dict[str, JsonValue]) -> None:
        records = self._records(result["adversarial_controls"], "adversarial controls")
        reconciled = self._records(
            result["reconciliation_controls"], "reconciliation controls"
        )
        reconciliation_status = {
            self._string(item["reconciles_issue_code"], "reconciled issue"): (
                self._string(item["status"], "reconciliation status")
            )
            for item in reconciled
        }
        rows: list[list[str]] = []
        for record in records:
            issues = record["issue_codes"]
            if not isinstance(issues, list) or len(issues) != 1:
                raise ValueError("adversarial control must have one issue")
            issue = self._string(issues[0], "issue")
            rows.append(
                [
                    self._short(self._string(record["id"], "id")),
                    self._string(record["status"], "status"),
                    reconciliation_status.get(issue, "not reconciled"),
                ]
            )
        axis.axis("off")
        table = axis.table(
            cellText=rows,
            colLabels=["contract", "raw result", "reconciled"],
            loc="center",
            cellLoc="left",
            colLoc="left",
            colWidths=[0.31, 0.27, 0.42],
        )
        table.auto_set_font_size(False)
        table.set_fontsize(7.8)
        table.scale(1.0, 1.55)
        for (row, _column), cell in table.get_celld().items():
            if row == 0:
                cell.set_facecolor("#d9e6f2")
                cell.set_text_props(fontweight="bold")
            elif row % 2 == 0:
                cell.set_facecolor("#f2f2f2")
        route_error = self._real(records[0]["route_noncommutativity_frobenius"])
        maximum_reconciled = max(
            self._real(item["route_noncommutativity_frobenius"]) for item in reconciled
        )
        axis.text(
            0.5,
            0.18,
            (
                f"Raw truncation mismatch: {route_error:.3e}\n"
                f"Maximum reconciled route defect: {maximum_reconciled:.3e}"
            ),
            transform=axis.transAxes,
            ha="center",
            fontsize=8.2,
        )
        axis.set_title("(d) Guarded mismatches and explicit reconciliation", pad=12)

    @staticmethod
    def _short(value: str) -> str:
        replacements = {
            "scalar-onsite": "scalar",
            "orbital-onsite": "orbital",
            "nearest-neighbor": "range 1",
            "range-two-nonlocal": "range 2",
            "collinear-spin": "collinear",
            "spin-mixing": "spin mix",
            "hopping-truncation-mismatch": "truncation",
            "fiber-domain-mismatch": "domain",
            "nonuniform-fiber-weights": "weights",
            "unmatched-alignment-map": "map",
        }
        return replacements.get(value, value)

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


def main() -> None:
    """Adapt retained result and output paths into the plotting action."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    IndependentRouteSummaryPlotter().execute(
        arguments.result.resolve(), arguments.output.resolve()
    )


if __name__ == "__main__":
    main()
