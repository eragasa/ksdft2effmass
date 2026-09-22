#!/usr/bin/env python3
"""Plot the retained one-dimensional defect-extraction summary."""

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


class DefectSummaryPlotter:
    """Render six diagnostics without changing retained numerical evidence."""

    __slots__ = ()

    def execute(self, result_path: Path, output_path: Path) -> None:
        root = self._mapping(
            cast(JsonValue, json.loads(result_path.read_text(encoding="utf-8"))),
            "result",
        )
        figure, axes = plt.subplots(2, 3, figsize=(15.0, 8.8))
        self._plot_algebraic(axes[0, 0], root)
        self._plot_models(axes[0, 1], root)
        self._plot_finite_size(axes[0, 2], root)
        self._plot_binding(axes[1, 0], root)
        self._plot_wavefunctions(axes[1, 1], root)
        self._plot_metric_contrast(axes[1, 2], root)
        figure.suptitle(
            "Matched synthetic pristine–defect extraction: separate diagnostics",
            fontsize=15,
        )
        figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.965))
        figure.savefig(output_path, dpi=180)
        plt.close(figure)

    def _plot_algebraic(self, axis: Axes, root: dict[str, JsonValue]) -> None:
        folding = self._records(root["folding_control"], "folding")
        extraction = self._records(root["extraction_controls"], "extraction")
        labels = ["fold −", "fold 0", "fold +"] + [
            self._short(self._string(item["id"], "extraction id"))
            for item in extraction
        ]
        values = [
            self._real(item["folded_operator_frobenius_defect"], "fold defect")
            for item in folding
        ] + [
            self._real(item["aligned_extraction_frobenius_defect"], "extraction defect")
            for item in extraction
        ]
        axis.bar(np.arange(len(values)), np.maximum(values, 1.0e-18), color="#326a8f")
        axis.axhline(1.0e-11, color="#a33a2b", linestyle="--", label="tolerance")
        axis.set_yscale("log")
        axis.set_xticks(np.arange(len(labels)), labels, rotation=58, ha="right")
        axis.set_ylabel("Frobenius defect")
        axis.set_title("(a) Folding and aligned recovery")
        axis.legend(frameon=False, fontsize=8)
        axis.grid(axis="y", alpha=0.25)

    def _plot_models(self, axis: Axes, root: dict[str, JsonValue]) -> None:
        hierarchy = self._records(root["model_class_hierarchy"], "model hierarchy")
        rows: list[list[float]] = []
        row_labels: list[str] = []
        for record in hierarchy:
            classes = self._records(record["hierarchy"], "classes")
            values = [
                self._real(item["relative_frobenius_residual"], "model residual")
                for item in classes
            ]
            rows.append(values + [np.nan] * (4 - len(values)))
            row_labels.append(self._short(self._string(record["defect_id"], "defect")))
        matrix = np.asarray(rows, dtype=np.float64)
        image = axis.imshow(
            np.ma.masked_invalid(matrix),
            aspect="auto",
            cmap="magma_r",
            vmin=0.0,
            vmax=1.0,
        )
        axis.set_xticks(
            np.arange(4), ["scalar", "orbital/collinear", "range 1/spinor", "range 2"]
        )
        axis.tick_params(axis="x", rotation=48)
        axis.set_yticks(np.arange(len(row_labels)), row_labels)
        for row in range(matrix.shape[0]):
            for column in range(matrix.shape[1]):
                if np.isfinite(matrix[row, column]):
                    axis.text(
                        column,
                        row,
                        f"{matrix[row, column]:.2f}",
                        ha="center",
                        va="center",
                        fontsize=7,
                        color="black" if matrix[row, column] < 0.5 else "white",
                    )
        axis.set_title("(b) Frozen model-class residuals")
        colorbar = axis.figure.colorbar(image, ax=axis, fraction=0.046, pad=0.03)
        colorbar.set_label("relative operator residual")

    def _plot_finite_size(self, axis: Axes, root: dict[str, JsonValue]) -> None:
        finite = self._mapping(root["finite_size_control"], "finite size")
        records = self._records(finite["records"], "finite records")
        sizes = np.asarray(
            [self._integer(item["supercell_size"], "size") for item in records]
        )
        widths = np.asarray(
            [
                self._real(item["lowest_defect_band_width"], "band width")
                for item in records
            ]
        )
        centers = np.asarray(
            [
                self._real(item["center_binding_relative_to_host_edge"], "binding")
                for item in records
            ]
        )
        line = axis.semilogy(sizes, widths, "o-", color="#7c3b91", label="band width")
        axis.set_xlabel("supercell size $N$")
        axis.set_ylabel("defect-band width ($E_G$)", color="#7c3b91")
        axis.tick_params(axis="y", labelcolor="#7c3b91")
        axis.grid(alpha=0.25)
        twin = axis.twinx()
        drift = np.abs(centers - centers[-1])
        second = twin.semilogy(
            sizes,
            np.maximum(drift, 1.0e-18),
            "s--",
            color="#d17c22",
            label="binding drift",
        )
        twin.set_ylabel("binding drift from $N=48$ ($E_G$)", color="#d17c22")
        twin.tick_params(axis="y", labelcolor="#d17c22")
        axis.set_title("(c) Periodic-image convergence")
        axis.legend(line + second, ["band width", "binding drift"], frameon=False)

    def _plot_binding(self, axis: Axes, root: dict[str, JsonValue]) -> None:
        smoothness = self._mapping(root["smoothness_control"], "smoothness")
        families = self._records(smoothness["families"], "families")
        for family, color, marker in zip(
            families, ("#26734d", "#b24a3b"), ("o", "s"), strict=True
        ):
            records = self._records(family["records"], "smooth records")
            widths = np.asarray(
                [self._real(item["width_cells"], "width") for item in records]
            )
            errors = np.asarray(
                [
                    abs(
                        self._real(
                            item["parabolic_minus_lattice_binding_error"],
                            "binding error",
                        )
                    )
                    for item in records
                ]
            )
            axis.loglog(
                widths,
                errors,
                marker=marker,
                color=color,
                label=self._string(family["family"], "family"),
            )
        axis.set_xlabel(r"Gaussian width $\sigma/a$")
        axis.set_ylabel("$|E_b^{par}-E_b^{lat}|$ ($E_G$)")
        axis.set_title("(d) Parabolic binding discrepancy")
        axis.legend(frameon=False)
        axis.grid(alpha=0.25, which="both")

    def _plot_wavefunctions(self, axis: Axes, root: dict[str, JsonValue]) -> None:
        smoothness = self._mapping(root["smoothness_control"], "smoothness")
        families = self._records(smoothness["families"], "families")
        for family, color, marker in zip(
            families, ("#26734d", "#b24a3b"), ("o", "s"), strict=True
        ):
            records = self._records(family["records"], "smooth records")
            widths = np.asarray(
                [self._real(item["width_cells"], "width") for item in records]
            )
            infidelities = np.asarray(
                [
                    1.0 - self._real(item["state_fidelity"], "fidelity")
                    for item in records
                ]
            )
            high_momentum = np.asarray(
                [
                    self._real(item["lattice_high_momentum_weight"], "high k")
                    for item in records
                ]
            )
            label = self._string(family["family"], "family")
            axis.loglog(
                widths,
                np.maximum(infidelities, 1.0e-18),
                marker=marker,
                color=color,
                label=f"{label}: $1-F$",
            )
            axis.loglog(
                widths,
                np.maximum(high_momentum, 1.0e-18),
                marker=marker,
                linestyle="--",
                color=color,
                label=f"{label}: high-$k$",
            )
        axis.set_xlabel(r"Gaussian width $\sigma/a$")
        axis.set_ylabel("weight or infidelity")
        axis.set_title("(e) Wavefunction and momentum diagnostics")
        axis.legend(frameon=False, fontsize=7)
        axis.grid(alpha=0.25, which="both")

    def _plot_metric_contrast(self, axis: Axes, root: dict[str, JsonValue]) -> None:
        contrast = self._mapping(root["metric_contrast_control"], "contrast")
        cases = self._records(contrast["cases"], "contrast cases")
        colors = ("#4c72b0", "#c44e52")
        for record, color in zip(cases, colors, strict=True):
            residual = self._real(
                record["operator_residual_relative_to_full_reference_hamiltonian"],
                "operator residual",
            )
            binding = abs(self._real(record["binding_energy_error"], "binding error"))
            infidelity = 1.0 - self._real(
                record["lowest_state_fidelity"], "state fidelity"
            )
            short = (
                "excited sector"
                if self._string(record["id"], "case").startswith("large")
                else "bound–continuum"
            )
            axis.scatter(
                residual,
                max(binding, 1.0e-18),
                s=70,
                marker="o",
                color=color,
                label=rf"$|\Delta E_b|$: {short}",
            )
            axis.scatter(
                residual,
                max(infidelity, 1.0e-18),
                s=70,
                marker="^",
                color=color,
                label=f"$1-F$: {short}",
            )
        axis.set_xscale("log")
        axis.set_yscale("log")
        axis.set_xlabel("relative global operator residual")
        axis.set_ylabel("observable error")
        axis.set_title("(f) Operator norm is not an observable oracle")
        axis.legend(frameon=False, fontsize=7)
        axis.grid(alpha=0.25, which="both")

    @staticmethod
    def _short(identifier: str) -> str:
        names = {
            "scalar-onsite": "scalar",
            "orbital-onsite": "orbital",
            "nearest-neighbor": "range 1",
            "range-two-nonlocal": "range 2",
            "collinear-spin": "collinear",
            "spin-mixing": "spin mix",
            "null": "null",
        }
        return names.get(identifier, identifier)

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
    def _integer(value: JsonValue, name: str) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an integer")
        return value

    @staticmethod
    def _real(value: JsonValue, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be numeric")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result


def main() -> None:
    """Adapt command-line paths into the plot action."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    DefectSummaryPlotter().execute(
        arguments.result.resolve(), arguments.output.resolve()
    )


if __name__ == "__main__":
    main()
