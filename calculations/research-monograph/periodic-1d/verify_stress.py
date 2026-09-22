#!/usr/bin/env python3
"""Independently verify the retained periodic-reduction stress result."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import cast

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


class StressResultVerifier:
    """Verify adversarial conclusions without rerunning the eigensolvers."""

    __slots__ = ()

    def execute(self, result_path: Path) -> None:
        payload = cast(JsonValue, json.loads(result_path.read_text()))
        root = self._mapping(payload)
        if root["schema_version"] != 1:
            raise ValueError("unexpected stress result schema version")
        if root["evidence_status"] != "illustrative numerical stress test":
            raise ValueError("unexpected stress result status")
        self._verify_provenance(result_path, self._mapping(root["provenance"]))
        self._verify_amplitudes(self._array(root["potential_amplitude_stress"]))
        self._verify_shapes(self._mapping(root["potential_shape_stress"]))
        self._verify_mesh(self._array(root["mesh_band_and_isolation_stress"]))
        self._verify_gauge(self._mapping(root["gauge_covariance_stress"]))
        self._verify_routes(self._mapping(root["route_assumption_stress"]))

    def _verify_provenance(
        self, result_path: Path, provenance: dict[str, JsonValue]
    ) -> None:
        repository_root = result_path.parents[3]
        for prefix in ("input", "script"):
            relative_path = self._string(provenance[f"{prefix}_path"])
            expected = self._string(provenance[f"{prefix}_sha256"])
            observed = hashlib.sha256(
                (repository_root / relative_path).read_bytes()
            ).hexdigest()
            if observed != expected:
                raise ValueError(f"{prefix} identity mismatch")

    def _verify_amplitudes(self, values: list[JsonValue]) -> None:
        records = [self._mapping(value) for value in values]
        if len(records) != 7:
            raise ValueError("unexpected amplitude stress count")
        for index, record in enumerate(records):
            strength = self._number(record["potential_strength"])
            status = self._string(record["isolated_band_status"])
            gap = self._number(record["zone_boundary_gap"])
            if index == 0:
                if strength != 0.0 or status != "failed_gap_closure" or gap != 0.0:
                    raise ValueError("free-limit gap closure was not detected")
            elif status != "pass" or gap <= 0.0:
                raise ValueError("nonzero cosine amplitude lost lowest-band isolation")
            if self._number(record["potential_sign_invariance_maximum_error"]) > 1e-12:
                raise ValueError("potential-sign translation covariance failed")
            plane_wave = [
                self._mapping(item)
                for item in self._array(record["plane_wave_cutoff_study"])
            ]
            if self._number(plane_wave[-1]["maximum_low_band_error"]) > 1e-11:
                raise ValueError("finest plane-wave stress cutoff is unresolved")
            finite_difference = [
                self._mapping(item)
                for item in self._array(record["finite_difference_grid_study"])
            ]
            errors = [
                self._number(item["maximum_low_band_error"])
                for item in finite_difference
            ]
            pairs = zip(errors, errors[1:], strict=False)
            if any(later >= earlier for earlier, later in pairs):
                raise ValueError("finite-difference stress refinement is not monotone")

    def _verify_shapes(self, value: dict[str, JsonValue]) -> None:
        if self._number(value["translation_isospectral_maximum_error"]) > 1e-12:
            raise ValueError("translated-potential isospectral control failed")
        if self._number(value["constant_shift_covariance_maximum_error"]) > 1e-12:
            raise ValueError("constant energy-shift covariance failed")
        cases = [self._mapping(item) for item in self._array(value["cases"])]
        identifiers = {self._string(case["id"]) for case in cases}
        required = {
            "baseline_cosine",
            "translated_cosine",
            "constant_shifted_cosine",
            "second_harmonic_cosine",
            "inversion_broken",
            "three_harmonic",
        }
        if identifiers != required:
            raise ValueError("potential-shape stress cases are incomplete")
        for case in cases:
            if self._number(case["time_reversal_energy_residual"]) > 1e-12:
                raise ValueError("real-potential time-reversal energy symmetry failed")
            gaps = [
                self._number(item)
                for item in self._array(case["minimum_adjacent_gaps"])
            ]
            if len(gaps) != 8 or any(gap < 0.0 for gap in gaps):
                raise ValueError("invalid higher-band gap record")

    def _verify_mesh(self, values: list[JsonValue]) -> None:
        records = [self._mapping(value) for value in values]
        expected_count = 7 * 5 * 6
        if len(records) != expected_count:
            raise ValueError("unexpected mesh-band stress record count")
        for record in records:
            if self._number(record["full_reconstruction_maximum_error"]) > 1e-11:
                raise ValueError("complete hopping reconstruction failed")
        free_records = [
            record
            for record in records
            if self._number(record["potential_strength"]) == 0.0
        ]
        if any(
            self._boolean(record["isolation_applicable"])
            for record in free_records
        ):
            raise ValueError("free-limit degeneracies were treated as isolated")
        baseline_finest = {
            self._integer(record["band_index"]): record
            for record in records
            if self._number(record["potential_strength"]) == 0.5
            and self._integer(record["mesh_size"]) == 128
        }
        if set(baseline_finest) != {0, 1, 2, 3, 5, 7}:
            raise ValueError("higher-band baseline coverage is incomplete")
        if self._boolean(baseline_finest[7]["isolation_applicable"]):
            raise ValueError("near-degenerate eighth band was treated as isolated")
        lowest_error = self._number(
            baseline_finest[0]["fixed_range_withheld_maximum_error"]
        )
        highest_error = self._number(
            baseline_finest[7]["fixed_range_withheld_maximum_error"]
        )
        if highest_error <= 100.0 * lowest_error:
            raise ValueError("higher-band finite-range stress did not expose failure")

    def _verify_gauge(self, value: dict[str, JsonValue]) -> None:
        for key in (
            "random_phase_projector_maximum_frobenius_defect",
            "parallel_transport_frame_maximum_aligned_defect",
            "closure_holonomy_difference_modulo_2pi",
        ):
            if self._number(value[key]) > 1e-12:
                raise ValueError(f"gauge covariance failed for {key}")

    def _verify_routes(self, value: dict[str, JsonValue]) -> None:
        if self._number(value["uniform_complete_coefficient_defect"]) > 1e-12:
            raise ValueError("ideal route-equivalence control failed")
        weighted = self._number(value["nonuniform_weight_coefficient_defect"])
        incomplete = self._number(value["incomplete_training_coefficient_defect"])
        if weighted <= 1e-8 or incomplete <= 1e-5:
            raise ValueError("route-assumption perturbations did not break equivalence")

    @staticmethod
    def _mapping(value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("expected JSON object")
        return value

    @staticmethod
    def _array(value: JsonValue) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError("expected JSON array")
        return value

    @staticmethod
    def _string(value: JsonValue) -> str:
        if not isinstance(value, str):
            raise TypeError("expected string")
        return value

    @staticmethod
    def _number(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("expected number")
        return float(value)

    @staticmethod
    def _integer(value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("expected integer")
        return value

    @staticmethod
    def _boolean(value: JsonValue) -> bool:
        if not isinstance(value, bool):
            raise TypeError("expected boolean")
        return value


class CommandAdapter:
    """Adapt one result path to the independent verifier."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("result", type=Path)
        args = parser.parse_args(argv)
        StressResultVerifier().execute(cast(Path, args.result).resolve())
        print("periodic-1d adversarial stress result: PASS")
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
