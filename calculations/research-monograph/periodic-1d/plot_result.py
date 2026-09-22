#!/usr/bin/env python3
"""Plot the retained isolated-band periodic-reduction result."""

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
type ComplexVector = npt.NDArray[np.complex128]


class PeriodicReductionResultPlotter:
    """Render parent convergence, bands, hoppings, and truncation errors."""

    __slots__ = ()

    def execute(self, result_path: Path, output_path: Path) -> None:
        result = self._mapping(
            cast(JsonValue, json.loads(result_path.read_text(encoding="utf-8")))
        )
        parent = self._mapping(result["parent_representation_verification"])
        reduction = self._mapping(result["isolated_band_reduction"])
        pw = self._records(parent["plane_wave_cutoff_study"])
        fd = self._records(parent["finite_difference_grid_study"])
        ranges = self._records(reduction["hopping_range_study"])
        momenta = np.asarray(self._reals(reduction["reciprocal_mesh"]))
        energies = np.asarray(self._reals(reduction["lowest_band_energies"]))
        representatives = np.asarray(
            self._integers(reduction["hopping_representatives_cells"])
        )
        hoppings = self._complexes(reduction["hopping_coefficients"])
        period = float(2.0 * np.pi)

        figure, axes = plt.subplots(2, 2, figsize=(11.0, 8.0), constrained_layout=True)
        axes[0, 0].semilogy(
            [self._integer(record["cutoff"]) for record in pw],
            [self._real(record["maximum_first_bands_absolute_error"]) for record in pw],
            marker="o",
            label="plane-wave cutoff",
        )
        axes[0, 0].semilogy(
            [self._integer(record["interior_cell_points"]) for record in fd],
            [self._real(record["maximum_first_bands_absolute_error"]) for record in fd],
            marker="s",
            label="finite-difference grid",
        )
        axes[0, 0].set_xlabel("cutoff P or grid points N")
        axes[0, 0].set_ylabel(r"maximum low-band error / $E_G$")
        axes[0, 0].set_title("Independent discretization convergence")
        axes[0, 0].legend()
        axes[0, 0].grid(True, which="both", alpha=0.3)

        axes[0, 1].plot(momenta, energies, color="black", label="represented band")
        for hopping_range in (1, 3):
            retained = np.abs(representatives) <= hopping_range
            model = (
                np.exp(
                    1j
                    * np.outer(
                        momenta,
                        representatives[retained] * period,
                    )
                )
                @ hoppings[retained]
            )
            axes[0, 1].plot(
                momenta,
                model.real,
                linestyle="--",
                label=rf"TB $r_c={hopping_range}$",
            )
        axes[0, 1].set_xlabel(r"$k/G$")
        axes[0, 1].set_ylabel(r"energy / $E_G$")
        axes[0, 1].set_title("Lowest band and finite-range approximations")
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)

        axes[1, 0].semilogy(
            np.abs(representatives), np.abs(hoppings), marker="o", linestyle="none"
        )
        axes[1, 0].set_xlabel(r"hopping distance $|R|/a$")
        axes[1, 0].set_ylabel(r"$|t(R)|/E_G$")
        axes[1, 0].set_title("Real-space hopping decay")
        axes[1, 0].grid(True, which="both", alpha=0.3)

        range_values = [
            self._integer(record["hopping_range_cells"]) for record in ranges
        ]
        axes[1, 1].semilogy(
            range_values,
            [
                self._real(record["training_root_mean_square_error"])
                for record in ranges
            ],
            marker="o",
            label="training RMS",
        )
        axes[1, 1].semilogy(
            range_values,
            [
                self._real(record["withheld_root_mean_square_error"])
                for record in ranges
            ],
            marker="s",
            label="withheld RMS",
        )
        axes[1, 1].set_xlabel(r"hopping range $r_c/a$")
        axes[1, 1].set_ylabel(r"energy error / $E_G$")
        axes[1, 1].set_title("Finite-range error")
        axes[1, 1].legend()
        axes[1, 1].grid(True, which="both", alpha=0.3)
        figure.savefig(output_path, dpi=180)
        plt.close(figure)

    @staticmethod
    def _mapping(value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("value must be a JSON object")
        return value

    @staticmethod
    def _records(value: JsonValue) -> tuple[dict[str, JsonValue], ...]:
        if not isinstance(value, list):
            raise TypeError("value must be a JSON array")
        records: list[dict[str, JsonValue]] = []
        for item in value:
            if not isinstance(item, dict):
                raise TypeError("array entries must be JSON objects")
            records.append(item)
        return tuple(records)

    @staticmethod
    def _real(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("value must be a number")
        return float(value)

    @staticmethod
    def _integer(value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("value must be an integer")
        return value

    def _reals(self, value: JsonValue) -> tuple[float, ...]:
        if not isinstance(value, list):
            raise TypeError("value must be an array")
        return tuple(self._real(item) for item in value)

    def _integers(self, value: JsonValue) -> tuple[int, ...]:
        if not isinstance(value, list):
            raise TypeError("value must be an array")
        return tuple(self._integer(item) for item in value)

    def _complexes(self, value: JsonValue) -> ComplexVector:
        if not isinstance(value, list):
            raise TypeError("value must be an array")
        entries: list[complex] = []
        for pair in value:
            if not isinstance(pair, list) or len(pair) != 2:
                raise TypeError("complex entries must be pairs")
            entries.append(complex(self._real(pair[0]), self._real(pair[1])))
        return np.asarray(entries, dtype=np.complex128)


class CommandAdapter:
    """Adapt command-line paths to the owned plotter."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("result", type=Path)
        parser.add_argument("--output", type=Path, required=True)
        args = parser.parse_args(argv)
        PeriodicReductionResultPlotter().execute(
            cast(Path, args.result).resolve(), cast(Path, args.output).resolve()
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
