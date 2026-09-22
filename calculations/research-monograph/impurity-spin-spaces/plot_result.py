#!/usr/bin/env python3
"""Plot the retained controlled spin-space embedding result."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import cast

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from matplotlib.gridspec import GridSpec

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type ComplexMatrix = npt.NDArray[np.complex128]


class SpinSpaceResultPlotter:
    """Render operator structure, scalar residuals, and spin-frame covariance."""

    __slots__ = ()

    def execute(self, result_path: Path, output_path: Path) -> None:
        result = self._mapping(
            cast(JsonValue, json.loads(result_path.read_text(encoding="utf-8"))),
            "result",
        )
        operators = self._mapping(result["operators"], "operators")
        checks = self._mapping(result["checks"], "checks")
        figure = plt.figure(figsize=(11.5, 7.2), constrained_layout=True)
        grid = GridSpec(2, 4, figure=figure, height_ratios=(1.0, 1.05))
        heatmap_axes = [figure.add_subplot(grid[0, index]) for index in range(4)]
        identifiers = (
            "spinless_impurity",
            "spin_degenerate_impurity",
            "collinear_impurity_orbital_major",
            "time_reversal_spinor_impurity",
        )
        titles = (
            r"Spinless $\Delta H_0$",
            r"Degenerate $\Delta H_0\otimes I_2$",
            "Collinear",
            "Spin-mixing",
        )
        matrices = [
            self._complex_matrix(
                self._mapping(operators[identifier], identifier)["matrix"], identifier
            )
            for identifier in identifiers
        ]
        maximum = max(float(np.max(np.abs(matrix))) for matrix in matrices)
        image = None
        for axis, matrix, title in zip(heatmap_axes, matrices, titles, strict=True):
            image = axis.imshow(
                np.abs(matrix),
                origin="lower",
                cmap="magma",
                vmin=0.0,
                vmax=maximum,
                interpolation="nearest",
            )
            axis.set_title(title, fontsize=10)
            axis.set_xlabel("basis index")
            axis.set_ylabel("basis index")
        if image is None:
            raise ValueError("operator heatmap set must be nonempty")
        figure.colorbar(
            image,
            ax=heatmap_axes,
            location="right",
            shrink=0.82,
            label=r"$|\Delta H_{ij}|$ / synthetic energy unit",
        )
        scalar_axis = figure.add_subplot(grid[1, :2])
        covariance_axis = figure.add_subplot(grid[1, 2:])
        self._plot_scalar_models(scalar_axis, checks)
        self._plot_covariance(covariance_axis, checks)
        figure.savefig(output_path, dpi=200)
        plt.close(figure)

    def _plot_scalar_models(self, axis: plt.Axes, checks: dict[str, JsonValue]) -> None:
        records = self._records(checks["scalar_model_class"], "scalar models")
        labels = [
            self._string(record["id"], "scalar id").replace("-", " ")
            for record in records
        ]
        residuals = [
            self._real(record["relative_frobenius_residual"], "relative residual")
            for record in records
        ]
        positions = np.arange(len(labels))
        colors = ["#4C78A8", "#E45756", "#72B7B2"]
        axis.bar(positions, residuals, color=colors)
        axis.set_xticks(positions, labels, rotation=12, ha="right")
        axis.set_ylabel("best scalar relative Frobenius residual")
        axis.set_title("Spin-independent model class")
        axis.grid(True, axis="y", alpha=0.3)
        for position, residual in zip(positions, residuals, strict=True):
            axis.text(
                float(position),
                residual + 0.012,
                f"{residual:.3f}",
                ha="center",
                va="bottom",
                fontsize=9,
            )
        axis.set_ylim(0.0, max(residuals) * 1.22)

    def _plot_covariance(self, axis: plt.Axes, checks: dict[str, JsonValue]) -> None:
        records = self._records(checks["spin_frame_covariance"], "covariance")
        labels = [
            self._string(record["id"], "rotation id").replace("-", " ")
            for record in records
        ]
        positions = np.arange(len(labels))
        unaligned = [
            self._real(record["unaligned_frobenius_defect"], "unaligned defect")
            for record in records
        ]
        aligned = [
            max(
                self._real(record["aligned_frobenius_defect"], "aligned defect"),
                1.0e-18,
            )
            for record in records
        ]
        eigenvalue = [
            max(
                self._real(
                    record["eigenvalue_maximum_absolute_defect"],
                    "eigenvalue defect",
                ),
                1.0e-18,
            )
            for record in records
        ]
        axis.semilogy(positions, unaligned, "o-", label="unaligned matrix defect")
        axis.semilogy(positions, aligned, "s-", label="after declared alignment")
        axis.semilogy(positions, eigenvalue, "^-", label="eigenvalue defect")
        axis.set_xticks(positions, labels, rotation=12, ha="right")
        axis.set_ylabel("absolute defect / synthetic energy unit")
        axis.set_title("Spin-frame covariance")
        axis.grid(True, which="both", alpha=0.3)
        axis.legend(fontsize="small")

    @staticmethod
    def _mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be a JSON object")
        return value

    def _records(self, value: JsonValue, name: str) -> tuple[dict[str, JsonValue], ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return tuple(self._mapping(item, name) for item in value)

    @staticmethod
    def _string(value: JsonValue, name: str) -> str:
        if not isinstance(value, str) or not value:
            raise TypeError(f"{name} must be a nonempty string")
        return value

    @staticmethod
    def _real(value: JsonValue, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be a JSON number")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    def _complex_matrix(self, value: JsonValue, name: str) -> ComplexMatrix:
        if not isinstance(value, list) or not value:
            raise TypeError(f"{name} must be a nonempty matrix")
        rows: list[list[complex]] = []
        for row in value:
            if not isinstance(row, list):
                raise TypeError(f"{name} rows must be JSON arrays")
            values: list[complex] = []
            for pair in row:
                if not isinstance(pair, list) or len(pair) != 2:
                    raise TypeError(f"{name} entries must be [real, imaginary]")
                values.append(
                    complex(
                        self._real(pair[0], name),
                        self._real(pair[1], name),
                    )
                )
            rows.append(values)
        return np.asarray(rows, dtype=np.complex128)


def main() -> None:
    """Adapt command-line paths into the owned plot action."""
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    SpinSpaceResultPlotter().execute(
        arguments.result.resolve(), arguments.output.resolve()
    )


if __name__ == "__main__":
    main()
