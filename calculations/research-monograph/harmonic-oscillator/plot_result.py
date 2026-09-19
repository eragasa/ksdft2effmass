#!/usr/bin/env python3
"""Plot the retained Appendix E harmonic-oscillator comparison."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import cast

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type RealMatrix = npt.NDArray[np.float64]


class HarmonicOscillatorResultPlotter:
    """Render convergence, map-quality, and operator-difference graphics."""

    __slots__ = ()

    def execute(
        self, result_path: Path, summary_path: Path, heatmap_path: Path
    ) -> None:
        payload = self.mapping(
            cast(JsonValue, json.loads(result_path.read_text(encoding="utf-8"))),
            "result",
        )
        cases_value = payload["cases"]
        if not isinstance(cases_value, list):
            raise TypeError("cases must be a JSON array")
        cases = tuple(self.mapping(value, "case") for value in cases_value)
        boxes = sorted({self.real(case["box_half_width"]) for case in cases})
        spacings = sorted(
            {self.real(case["grid_spacing"]) for case in cases}, reverse=True
        )
        retained_dimensions = sorted(
            {self.integer(case["retained_dimension"]) for case in cases}
        )

        figure, axes = plt.subplots(2, 2, figsize=(11.0, 8.0), constrained_layout=True)
        finest_spacing = spacings[-1]
        for retained in retained_dimensions:
            values = [
                self.diagnostic(
                    cases,
                    box,
                    finest_spacing,
                    retained,
                    "relative_discrepancy_frobenius",
                )
                for box in boxes
            ]
            axes[0, 0].semilogy(boxes, values, marker="o", label=f"K={retained}")
        axes[0, 0].set_xlabel(r"box half-width $b=X/\ell$")
        axes[0, 0].set_ylabel(r"relative Frobenius discrepancy $\delta_F$")
        axes[0, 0].set_title(rf"Box expansion at $\eta={finest_spacing:g}$")
        axes[0, 0].legend()
        axes[0, 0].grid(True, which="both", alpha=0.3)

        widest_box = boxes[-1]
        for retained in retained_dimensions:
            values = [
                self.diagnostic(
                    cases,
                    widest_box,
                    spacing,
                    retained,
                    "relative_discrepancy_frobenius",
                )
                for spacing in spacings
            ]
            axes[0, 1].loglog(spacings, values, marker="o", label=f"K={retained}")
        axes[0, 1].invert_xaxis()
        axes[0, 1].set_xlabel(r"grid spacing $\eta=\Delta x/\ell$")
        axes[0, 1].set_ylabel(r"relative Frobenius discrepancy $\delta_F$")
        axes[0, 1].set_title(f"Spatial refinement at $b={widest_box:g}$")
        axes[0, 1].legend()
        axes[0, 1].grid(True, which="both", alpha=0.3)

        largest_retained = retained_dimensions[-1]
        diagonal = [
            self.diagnostic(
                cases,
                widest_box,
                spacing,
                largest_retained,
                "diagonal_discrepancy_frobenius",
            )
            for spacing in spacings
        ]
        off_diagonal = [
            self.diagnostic(
                cases,
                widest_box,
                spacing,
                largest_retained,
                "off_diagonal_discrepancy_frobenius",
            )
            for spacing in spacings
        ]
        axes[1, 0].loglog(spacings, diagonal, marker="o", label="diagonal")
        axes[1, 0].loglog(spacings, off_diagonal, marker="s", label="off-diagonal")
        axes[1, 0].invert_xaxis()
        axes[1, 0].set_xlabel(r"grid spacing $\eta$")
        axes[1, 0].set_ylabel(r"absolute discrepancy / $\hbar\omega$")
        axes[1, 0].set_title(
            f"Discrepancy split at $b={widest_box:g}$, K={largest_retained}"
        )
        axes[1, 0].legend()
        axes[1, 0].grid(True, which="both", alpha=0.3)

        for retained in retained_dimensions:
            gram_values = [
                self.diagnostic(
                    cases, box, finest_spacing, retained, "gram_deviation_frobenius"
                )
                for box in boxes
            ]
            axes[1, 1].semilogy(boxes, gram_values, marker="o", label=f"K={retained}")
        axes[1, 1].set_xlabel(r"box half-width $b$")
        axes[1, 1].set_ylabel(r"sampled-state Gram deviation $\|G-I\|_F$")
        axes[1, 1].set_title(rf"Map quality at $\eta={finest_spacing:g}$")
        axes[1, 1].legend()
        axes[1, 1].grid(True, which="both", alpha=0.3)
        figure.savefig(summary_path, dpi=180)
        plt.close(figure)

        selected = self.case(cases, widest_box, finest_spacing, largest_retained)
        operators = self.mapping(
            selected["operators_in_common_coordinates"], "operators"
        )
        difference = self.matrix(
            operators["finite_box_minus_ladder"], "finite_box_minus_ladder"
        )
        heatmap, axis = plt.subplots(figsize=(6.4, 5.3), constrained_layout=True)
        scale = float(np.max(np.abs(difference)))
        image = axis.imshow(
            difference,
            cmap="coolwarm",
            vmin=-scale,
            vmax=scale,
            origin="lower",
        )
        axis.set_xlabel("number-state column")
        axis.set_ylabel("number-state row")
        axis.set_title(
            rf"$(A_{{X,h}}^{{(K)}}-H_{{lad}}^{{(K)}})/(\hbar\omega)$, "
            rf"$b={widest_box:g}$, $\eta={finest_spacing:g}$, $K={largest_retained}$"
        )
        heatmap.colorbar(image, ax=axis, label="dimensionless matrix entry")
        heatmap.savefig(heatmap_path, dpi=180)
        plt.close(heatmap)

    def diagnostic(
        self,
        cases: tuple[dict[str, JsonValue], ...],
        box: float,
        spacing: float,
        retained: int,
        name: str,
    ) -> float:
        """Return one named diagnostic from an exactly selected comparison case."""
        case = self.case(cases, box, spacing, retained)
        diagnostics = self.mapping(case["diagnostics"], "diagnostics")
        return self.real(diagnostics[name])

    def case(
        self,
        cases: tuple[dict[str, JsonValue], ...],
        box: float,
        spacing: float,
        retained: int,
    ) -> dict[str, JsonValue]:
        """Return the unique case matching box, spacing, and retained dimension."""
        matches = tuple(
            case
            for case in cases
            if self.real(case["box_half_width"]) == box
            and self.real(case["grid_spacing"]) == spacing
            and self.integer(case["retained_dimension"]) == retained
        )
        if len(matches) != 1:
            raise ValueError("expected one matching comparison case")
        return matches[0]

    @staticmethod
    def mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        """Return ``value`` as a JSON object or raise ``TypeError``."""
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be a JSON object")
        return value

    @staticmethod
    def real(value: JsonValue) -> float:
        """Return ``value`` as a finite float, excluding Boolean values."""
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("value must be a JSON number")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError("value must be finite")
        return result

    @staticmethod
    def integer(value: JsonValue) -> int:
        """Return ``value`` as an integer, excluding Boolean values."""
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("value must be a JSON integer")
        return value

    @staticmethod
    def matrix(value: JsonValue, name: str) -> RealMatrix:
        """Return ``value`` as a finite two-dimensional binary64 matrix."""
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        matrix = np.asarray(value, dtype=np.float64)
        if matrix.ndim != 2 or not np.all(np.isfinite(matrix)):
            raise ValueError(f"{name} must be a finite matrix")
        return matrix


def main() -> None:
    """Adapt command-line paths to the public result plotter."""
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--summary-output", type=Path, required=True)
    parser.add_argument("--heatmap-output", type=Path, required=True)
    args = parser.parse_args()
    HarmonicOscillatorResultPlotter().execute(
        cast(Path, args.result).resolve(),
        cast(Path, args.summary_output).resolve(),
        cast(Path, args.heatmap_output).resolve(),
    )


if __name__ == "__main__":
    main()
