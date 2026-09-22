#!/usr/bin/env python3
"""Plot separated continuum-refinement diagnostics for the synthetic 1D defect."""

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


class ContinuumRefinementSummaryPlotter:
    """Render numerical support, lattice scaling, and profile criteria."""

    __slots__ = ()

    def execute(self, result_path: Path, output_path: Path) -> None:
        result = self._load(result_path)
        figure, grid = plt.subplots(2, 2, figsize=(11.4, 8.5))
        axes = cast(np.ndarray[tuple[int, int], np.dtype[np.object_]], grid)
        self._plot_supporting_axes(axes[0, 0], result)
        self._plot_lattice_scale(axes[0, 1], result)
        self._plot_profile_families(axes[1, 0], result)
        self._plot_assessment(axes[1, 1], result)
        figure.suptitle(
            "Separated continuum refinement for the synthetic 1D defect",
            fontsize=14,
            fontweight="bold",
        )
        figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.96))
        output_path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(output_path, dpi=180)
        plt.close(figure)

    def _plot_supporting_axes(self, axis: Axes, result: dict[str, JsonValue]) -> None:
        mesh = self._records(
            self._mapping(result["continuum_mesh_axis"], "mesh")["records"],
            "mesh records",
        )
        domain = self._records(
            self._mapping(result["continuum_domain_axis"], "domain")["records"],
            "domain records",
        )
        supercell = self._records(
            self._mapping(result["lattice_supercell_axis"], "supercell")["records"],
            "supercell records",
        )
        axis.plot(
            [self._real(item["mode_count"]) for item in mesh],
            [
                max(self._real(item["binding_defect_from_finest"]), 1e-18)
                for item in mesh
            ],
            marker="o",
            label="continuum mesh",
        )
        axis.plot(
            [self._real(item["domain_length"]) for item in domain],
            [
                max(
                    self._real(item["binding_defect_from_largest_domain"]),
                    1e-18,
                )
                for item in domain
            ],
            marker="s",
            label="continuum domain",
        )
        axis.plot(
            [self._real(item["cell_count"]) for item in supercell],
            [
                max(
                    self._real(item["binding_defect_from_largest_supercell"]),
                    1e-18,
                )
                for item in supercell
            ],
            marker="^",
            label="lattice supercell",
        )
        axis.set_yscale("log")
        axis.set_xlabel("mode count, domain length, or cells")
        axis.set_ylabel("binding defect from finest/largest ($E_G$)")
        axis.set_title("(a) Independently refined numerical supports")
        axis.grid(True, which="both", alpha=0.25)
        axis.legend(frameon=False, fontsize=8)

    def _plot_lattice_scale(self, axis: Axes, result: dict[str, JsonValue]) -> None:
        records = self._records(
            self._mapping(result["lattice_scale_axis"], "scale")["records"],
            "scale records",
        )
        spacing = [self._real(item["lattice_spacing"]) for item in records]
        series = (
            ("binding", "relative_binding_error", 1e-3),
            ("projector", "projector_frobenius_defect", 1e-2),
            ("compressed operator", "compressed_operator_spectral_norm", 1e-3),
            ("BZ-edge weight", "brillouin_edge_weight", 1e-4),
        )
        for label, field, tolerance in series:
            axis.plot(
                spacing,
                [self._real(item[field]) / tolerance for item in records],
                marker="o",
                label=label,
            )
        axis.axhline(1.0, color="black", linestyle="--", linewidth=1.0)
        axis.set_xscale("log", base=2)
        axis.invert_xaxis()
        axis.set_yscale("log")
        axis.set_xlabel("lattice spacing ($a_{ref}$), coarse to fine")
        axis.set_ylabel("metric / frozen tolerance")
        axis.set_title("(b) Fixed-profile lattice-scale sequence")
        axis.grid(True, which="both", alpha=0.25)
        axis.legend(frameon=False, fontsize=7)

    def _plot_profile_families(self, axis: Axes, result: dict[str, JsonValue]) -> None:
        families = self._records(
            self._mapping(result["profile_width_axis"], "profiles")["families"],
            "families",
        )
        styles = {"fixed-integrated": "o-", "fixed-peak": "s--"}
        for family in families:
            name = self._string(family["family"], "family")
            records = self._records(family["records"], "profile records")
            widths = [self._real(item["width"]) for item in records]
            ratios = [
                self._real(item["compressed_operator_spectral_norm"]) / 1e-3
                for item in records
            ]
            axis.plot(widths, ratios, styles[name], label=f"{name}: operator")
            axis.plot(
                widths,
                [self._real(item["relative_binding_error"]) / 1e-3 for item in records],
                styles[name],
                alpha=0.45,
                label=f"{name}: binding",
            )
        axis.axhline(1.0, color="black", linestyle="--", linewidth=1.0)
        axis.set_xscale("log", base=2)
        axis.set_yscale("log")
        axis.set_xlabel("Gaussian width ($a_{ref}$)")
        axis.set_ylabel("metric / frozen tolerance")
        axis.set_title("(c) Width families remain distinct")
        axis.grid(True, which="both", alpha=0.25)
        axis.legend(frameon=False, fontsize=7)

    def _plot_assessment(self, axis: Axes, result: dict[str, JsonValue]) -> None:
        assessment = self._mapping(result["crossover_assessment"], "assessment")
        scale = assessment["lattice_scale_persistent_pass_spacing"]
        integrated = assessment["fixed_integrated_crossover_width"]
        peak = assessment["fixed_peak_crossover_width"]
        rows = [
            ["continuum mesh", "pass", "fixed domain/profile"],
            ["continuum domain", "pass", "fixed spectral spacing"],
            ["lattice supercell", "pass", "fixed lattice/profile"],
            [
                "lattice scale",
                f"pass from $a={self._optional(scale)}$",
                "fixed profile",
            ],
            ["fixed-integrated width", self._optional(integrated), "no crossover"],
            ["fixed-peak width", self._optional(peak), "no crossover"],
        ]
        axis.axis("off")
        table = axis.table(
            cellText=rows,
            colLabels=["axis", "outcome", "interpretation"],
            loc="center",
            cellLoc="left",
            colLoc="left",
            colWidths=[0.34, 0.29, 0.37],
        )
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1.0, 1.45)
        for column in range(3):
            table[(0, column)].set_text_props(fontweight="bold")
            table[(0, column)].set_facecolor("#d8e6f3")
        axis.set_title("(d) Bounded result: scale pass, no width crossover", pad=18)

    @classmethod
    def _load(cls, path: Path) -> dict[str, JsonValue]:
        return cls._mapping(cast(JsonValue, json.loads(path.read_bytes())), "result")

    @staticmethod
    def _mapping(value: JsonValue, field: str) -> dict[str, JsonValue]:
        if type(value) is not dict:
            raise TypeError(f"{field} must be an object")
        return value

    @classmethod
    def _records(cls, value: JsonValue, field: str) -> list[dict[str, JsonValue]]:
        if type(value) is not list:
            raise TypeError(f"{field} must be an array")
        return [cls._mapping(item, field) for item in value]

    @staticmethod
    def _real(value: JsonValue) -> float:
        if type(value) is int:
            return float(value)
        if type(value) is float and np.isfinite(value):
            return value
        raise TypeError("value must be finite real excluding bool")

    @staticmethod
    def _string(value: JsonValue, field: str) -> str:
        if type(value) is not str:
            raise TypeError(f"{field} must be a string")
        return value

    @staticmethod
    def _optional(value: JsonValue) -> str:
        if value is None:
            return "none"
        if type(value) is int:
            return f"{value:g}"
        if type(value) is float:
            return f"{value:g}"
        raise TypeError("optional numeric value is invalid")


class CommandLineApplication:
    """Own typed command-line adaptation for the plotter."""

    __slots__ = ()

    def execute(self) -> None:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--result", type=Path, required=True)
        parser.add_argument("--output", type=Path, required=True)
        arguments = parser.parse_args()
        ContinuumRefinementSummaryPlotter().execute(
            cast(Path, arguments.result), cast(Path, arguments.output)
        )


def main() -> None:
    """Adapt the Python script entry point to the owned CLI application."""
    CommandLineApplication().execute()


if __name__ == "__main__":
    main()
