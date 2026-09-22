#!/usr/bin/env python3
"""Verify the retained isolated-band periodic-reduction result."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt
from scipy.special import mathieu_a, mathieu_b  # type: ignore[import-untyped]

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type RealVector = npt.NDArray[np.float64]
type ComplexVector = npt.NDArray[np.complex128]
type ComplexMatrix = npt.NDArray[np.complex128]


class PeriodicReductionResultVerifier:
    """Verify analytical limits, transforms, route agreement, and provenance."""

    __slots__ = ()

    def execute(self, result_path: Path, repository_root: Path) -> None:
        result = self._mapping(
            cast(JsonValue, json.loads(result_path.read_text(encoding="utf-8"))),
            "result",
        )
        assert result["schema_version"] == 1
        assert result["evidence_status"] == "illustrative numerical experiment"
        assert result["calculation_status"] == "calculated illustrative result"
        provenance = self._mapping(result["provenance"], "provenance")
        input_path = repository_root / self._string(provenance["input_path"])
        script_path = repository_root / self._string(provenance["script_path"])
        assert (
            hashlib.sha256(input_path.read_bytes()).hexdigest()
            == provenance["input_sha256"]
        )
        assert (
            hashlib.sha256(script_path.read_bytes()).hexdigest()
            == provenance["script_sha256"]
        )
        input_record = self._mapping(
            cast(JsonValue, json.loads(input_path.read_text(encoding="utf-8"))),
            "input",
        )
        potential = self._real(input_record["potential_strength"])
        cutoff = self._integers(input_record["plane_wave_cutoffs"])[-1]
        mesh_size = self._integer(input_record["reciprocal_mesh_size"])
        period = self._real(
            self._mapping(
                input_record["dimensionless_convention"], "dimensionless_convention"
            )["lattice_period"]
        )

        parent = self._mapping(result["parent_representation_verification"], "parent")
        self._verify_parent(parent, potential)
        reduction = self._mapping(result["isolated_band_reduction"], "reduction")
        self._verify_reduction(
            reduction,
            potential,
            cutoff,
            mesh_size,
            period,
            self._integer(input_record["withheld_mesh_size"]),
        )
        limitations = result["limitations"]
        assert isinstance(limitations, list) and len(limitations) == 4

    def _verify_parent(self, parent: dict[str, JsonValue], potential: float) -> None:
        pw_records = self._records(parent["plane_wave_cutoff_study"])
        pw_errors = np.asarray(
            [
                self._real(record["maximum_first_bands_absolute_error"])
                for record in pw_records
            ]
        )
        assert pw_errors[0] > 1.0e-8
        assert np.min(pw_errors[1:]) < 1.0e-12

        fd_records = self._records(parent["finite_difference_grid_study"])
        fd_errors = np.asarray(
            [
                self._real(record["maximum_first_bands_absolute_error"])
                for record in fd_records
            ]
        )
        assert np.all(np.diff(fd_errors) < 0.0)
        fd_orders = np.log(fd_errors[:-1] / fd_errors[1:]) / np.log(
            np.asarray(
                [
                    self._integer(fd_records[index + 1]["interior_cell_points"])
                    / self._integer(fd_records[index]["interior_cell_points"])
                    for index in range(len(fd_records) - 1)
                ]
            )
        )
        assert np.min(fd_orders) > 1.9

        low_records = self._records(parent["common_low_mode_operator_study"])
        low_errors = np.asarray(
            [
                self._real(record["maximum_low_mode_operator_frobenius_error"])
                for record in low_records
            ]
        )
        assert np.all(np.diff(low_errors) < 0.0)
        assert low_errors[-1] < 1.0e-2

        symmetry = self._mapping(parent["symmetry_residuals"], "symmetry")
        assert self._real(symmetry["inversion_maximum_absolute_energy"]) < 1.0e-12
        assert (
            self._real(symmetry["potential_sign_translation_maximum_absolute_energy"])
            < 1.0e-12
        )

        references = self._mapping(parent["mathieu_references"], "mathieu")
        q = 2.0 * potential
        np.testing.assert_allclose(
            self._real(references["zone_center_lowest"]),
            mathieu_a(0, q) / 4.0,
            rtol=0.0,
            atol=1.0e-15,
        )
        boundary = np.asarray(self._reals(references["zone_boundary_lowest_two"]))
        expected_boundary = np.sort(
            np.asarray([mathieu_a(1, q), mathieu_b(1, q)]) / 4.0
        )
        np.testing.assert_allclose(boundary, expected_boundary, atol=1.0e-15)
        assert self._real(references["plane_wave_zone_center_absolute_error"]) < 1.0e-12
        assert (
            self._real(references["plane_wave_zone_boundary_maximum_absolute_error"])
            < 1.0e-12
        )

        gap_records = self._records(parent["weak_potential_gap_study"])
        for record in gap_records:
            strength = self._real(record["potential_strength"])
            gap = self._real(record["zone_boundary_gap"])
            relative = self._real(record["relative_deviation_from_leading_gap"])
            np.testing.assert_allclose(relative, abs(gap - strength) / strength)
            assert relative < 3.0e-3

    def _verify_reduction(
        self,
        reduction: dict[str, JsonValue],
        potential: float,
        cutoff: int,
        mesh_size: int,
        period: float,
        withheld_size: int,
    ) -> None:
        momenta = np.asarray(self._reals(reduction["reciprocal_mesh"]))
        energies = np.asarray(self._reals(reduction["lowest_band_energies"]))
        representatives = np.asarray(
            self._integers(reduction["hopping_representatives_cells"]), dtype=np.int64
        )
        hoppings = self._complexes(reduction["hopping_coefficients"])
        assert (
            momenta.shape == energies.shape == representatives.shape == hoppings.shape
        )
        assert momenta.size == mesh_size
        expected_energies = np.asarray(
            [self._pw_energies(momentum, potential, cutoff)[0] for momentum in momenta]
        )
        np.testing.assert_allclose(energies, expected_energies, atol=1.0e-14)
        expected_hoppings = (
            np.exp(-1j * np.outer(representatives * period, momenta))
            @ energies
            / mesh_size
        )
        np.testing.assert_allclose(hoppings, expected_hoppings, atol=1.0e-14)
        reconstruction = (
            np.exp(1j * np.outer(momenta, representatives * period)) @ hoppings
        )
        observed_reconstruction = self._real(
            reduction["full_mesh_reconstruction_maximum_absolute_error"]
        )
        np.testing.assert_allclose(
            observed_reconstruction,
            np.max(np.abs(reconstruction.real - energies)),
            atol=1.0e-16,
        )
        assert observed_reconstruction < 1.0e-12
        assert self._real(reduction["hopping_maximum_imaginary"]) < 1.0e-12
        assert self._real(reduction["neighbor_overlap_minimum_magnitude"]) > 0.99

        localization = self._mapping(
            reduction["wannier_localization"], "wannier_localization"
        )
        np.testing.assert_allclose(
            self._real(localization["quadrature_norm"]), 1.0, atol=1.0e-12
        )
        center = self._real(localization["center_over_period"])
        assert -0.5 <= center < 0.5 or np.isclose(center, 0.5)
        assert self._real(localization["spread_over_period_squared"]) > 0.0
        assert len(self._string(localization["profile_density_content_sha256"])) == 64

        withheld_momenta = np.linspace(-0.5, 0.5, withheld_size)
        withheld_parent = np.asarray(
            [
                self._pw_energies(momentum, potential, cutoff)[0]
                for momentum in withheld_momenta
            ]
        )
        range_records = self._records(reduction["hopping_range_study"])
        previous_omitted = np.inf
        for record in range_records:
            hopping_range = self._integer(record["hopping_range_cells"])
            retained = np.abs(representatives) <= hopping_range
            omitted = float(np.linalg.norm(hoppings[~retained]))
            np.testing.assert_allclose(
                self._real(record["omitted_hopping_l2_norm"]), omitted, atol=1.0e-15
            )
            assert omitted < previous_omitted
            previous_omitted = omitted
            design = np.exp(1j * np.outer(momenta, representatives[retained] * period))
            mediated = design @ hoppings[retained]
            residual = energies - mediated.real
            np.testing.assert_allclose(
                self._real(record["training_root_mean_square_error"]),
                np.sqrt(np.mean(np.square(residual))),
                atol=1.0e-15,
            )
            parseval = abs(
                float(np.sum(np.square(residual))) - mesh_size * omitted * omitted
            )
            np.testing.assert_allclose(
                self._real(record["parseval_absolute_residual"]),
                parseval,
                atol=1.0e-18,
            )
            direct = np.linalg.lstsq(design, energies, rcond=None)[0]
            assert np.linalg.norm(direct - hoppings[retained]) < 1.0e-12
            withheld_design = np.exp(
                1j * np.outer(withheld_momenta, representatives[retained] * period)
            )
            withheld_error = (
                withheld_parent - (withheld_design @ hoppings[retained]).real
            )
            np.testing.assert_allclose(
                self._real(record["withheld_root_mean_square_error"]),
                np.sqrt(np.mean(np.square(withheld_error))),
                atol=1.0e-15,
            )
        assert self._real(range_records[-1]["withheld_maximum_absolute_error"]) < 1.0e-7

    @staticmethod
    def _pw_energies(momentum: float, potential: float, cutoff: int) -> RealVector:
        indices = np.arange(-cutoff, cutoff + 1, dtype=np.float64)
        matrix = np.diag(np.square(momentum + indices))
        coupling = 0.5 * potential
        matrix += np.diag(np.full(2 * cutoff, coupling), 1)
        matrix += np.diag(np.full(2 * cutoff, coupling), -1)
        return np.linalg.eigvalsh(matrix)

    @staticmethod
    def _mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be a JSON object")
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
    def _string(value: JsonValue) -> str:
        if not isinstance(value, str):
            raise TypeError("value must be a string")
        return value

    @staticmethod
    def _real(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("value must be a number")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError("value must be finite")
        return result

    @staticmethod
    def _integer(value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("value must be an integer")
        return value

    def _reals(self, value: JsonValue) -> tuple[float, ...]:
        if not isinstance(value, list):
            raise TypeError("value must be a JSON array")
        return tuple(self._real(item) for item in value)

    def _integers(self, value: JsonValue) -> tuple[int, ...]:
        if not isinstance(value, list):
            raise TypeError("value must be a JSON array")
        return tuple(self._integer(item) for item in value)

    def _complexes(self, value: JsonValue) -> ComplexVector:
        if not isinstance(value, list):
            raise TypeError("complex vector must be a JSON array")
        result: list[complex] = []
        for pair in value:
            if not isinstance(pair, list) or len(pair) != 2:
                raise TypeError("complex entries must be [real, imaginary]")
            result.append(complex(self._real(pair[0]), self._real(pair[1])))
        return np.asarray(result, dtype=np.complex128)


class CommandAdapter:
    """Adapt command-line paths to the owned verifier."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("result", type=Path)
        args = parser.parse_args(argv)
        PeriodicReductionResultVerifier().execute(
            cast(Path, args.result).resolve(), Path(__file__).resolve().parents[3]
        )
        print("periodic-1d isolated-band result: PASS")
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
