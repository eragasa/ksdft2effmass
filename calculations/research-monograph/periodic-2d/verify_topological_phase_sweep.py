#!/usr/bin/env python3
"""Verify topological phase sweeps through projector Bargmann invariants."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import cast

from verify_topological import JsonValue, TopologicalResultVerifier


class TopologicalPhaseSweepVerifier:
    """Independently reconstruct every retained phase-sweep sample."""

    __slots__ = ()

    def execute(self, result_path: Path) -> None:
        result = self._load(result_path)
        if self._integer(result["schema_version"]) != 1:
            raise ValueError("unsupported sweep result schema")
        if result["all_acceptance_checks_passed"] is not True:
            raise AssertionError("phase-sweep acceptance did not pass")
        input_path = result_path.with_name("topological-phase-sweep-input.json")
        runner_path = result_path.with_name("run_topological_phase_sweep.py")
        provenance = self._mapping(result["provenance"])
        self._identity(input_path, self._string(provenance["input_sha256"]), "input")
        self._identity(runner_path, self._string(provenance["runner_sha256"]), "runner")
        controls = self._load(input_path)
        mesh_size = self._integer(controls["mesh_size"])
        model_inputs = self._mapping(controls["models"])
        tolerance = self._real(
            self._mapping(controls["acceptance"])["chern_integer_defect"]
        )
        records = {
            self._string(self._mapping(value)["model"]): self._mapping(value)
            for value in self._array(result["models"])
        }
        if set(records) != {"qi_wu_zhang", "hofstadter", "haldane"}:
            raise AssertionError("unexpected sweep model identities")
        independent = TopologicalResultVerifier(b"{}", b"{}")
        for model_name, record in records.items():
            model_input = self._mapping(model_inputs[model_name])
            parameters = self._expected_parameters(model_input)
            samples = [self._mapping(value) for value in self._array(record["samples"])]
            if len(parameters) != len(samples):
                raise AssertionError(f"{model_name} sample count mismatch")
            for parameter, sample in zip(parameters, samples, strict=True):
                self._close(
                    self._real(sample["parameter"]),
                    parameter,
                    2.0e-15,
                    f"{model_name} parameter",
                )
                rebuilt = independent.analyze_case(
                    model_name, model_input, parameter, mesh_size
                )
                self._close(
                    self._real(sample["minimum_retained_gap"]),
                    self._real_value(rebuilt["minimum_retained_gap"]),
                    3.0e-13,
                    f"{model_name} gap",
                )
                self._close(
                    self._real(sample["retained_chern"]),
                    self._real_value(rebuilt["retained_chern"]),
                    3.0e-13,
                    f"{model_name} retained Chern",
                )
                recorded_cherns = self._reals(sample["band_cherns"])
                rebuilt_cherns = self._float_tuple(rebuilt["band_cherns"])
                if len(recorded_cherns) != len(rebuilt_cherns):
                    raise AssertionError(f"{model_name} band count mismatch")
                for recorded, rebuilt_value in zip(
                    recorded_cherns, rebuilt_cherns, strict=True
                ):
                    self._close(
                        recorded,
                        rebuilt_value,
                        3.0e-13,
                        f"{model_name} band Chern",
                    )
                if self._real(sample["retained_chern_integer_defect"]) >= tolerance:
                    raise AssertionError(f"{model_name} noninteger Chern sample")
                expected = self._analytic_expected(model_name, parameter, model_input)
                if expected != sample["analytic_expected_retained_chern"]:
                    raise AssertionError(f"{model_name} analytic expectation mismatch")

    def _expected_parameters(
        self, model_input: dict[str, JsonValue]
    ) -> tuple[float, ...]:
        start = self._real(model_input["start"])
        stop = self._real(model_input["stop"])
        count = self._integer(model_input["count"])
        if count < 2:
            raise ValueError("sweep count must be at least two")
        step = (stop - start) / (count - 1)
        return tuple(start + step * index for index in range(count))

    def _analytic_expected(
        self, model_name: str, parameter: float, model_input: dict[str, JsonValue]
    ) -> int | None:
        if model_name == "qi_wu_zhang":
            if parameter in (-2.0, 0.0, 2.0):
                return None
            if -2.0 < parameter < 0.0:
                return -1
            if 0.0 < parameter < 2.0:
                return 1
            return 0
        if model_name == "haldane":
            boundary = self._real(model_input["analytic_boundary_magnitude"])
            if abs(abs(parameter) - boundary) < 1.0e-14:
                return None
            return -1 if abs(parameter) < boundary else 0
        return None

    def _load(self, path: Path) -> dict[str, JsonValue]:
        value = cast(JsonValue, json.loads(path.read_text(encoding="utf-8")))
        return self._mapping(value)

    def _identity(self, path: Path, expected: str, label: str) -> None:
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError(
                f"{label} identity mismatch: actual={actual}, expected={expected}"
            )

    def _mapping(self, value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("expected a mapping")
        return value

    def _array(self, value: JsonValue) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError("expected an array")
        return value

    def _string(self, value: JsonValue) -> str:
        if not isinstance(value, str):
            raise TypeError("expected a string")
        return value

    def _integer(self, value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("expected an integer")
        return value

    def _real(self, value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("expected a real number")
        return float(value)

    def _reals(self, value: JsonValue) -> tuple[float, ...]:
        return tuple(self._real(item) for item in self._array(value))

    def _real_value(self, value: float | int | list[float]) -> float:
        if isinstance(value, list):
            raise TypeError("expected a scalar numerical result")
        return float(value)

    def _float_tuple(self, value: float | int | list[float]) -> tuple[float, ...]:
        if not isinstance(value, list):
            raise TypeError("expected a numerical result array")
        return tuple(float(item) for item in value)

    def _close(
        self, actual: float, expected: float, tolerance: float, label: str
    ) -> None:
        if abs(actual - expected) > tolerance:
            raise AssertionError(
                f"{label}: actual={actual:.16e}, expected={expected:.16e}"
            )


def main() -> None:
    """CLI entry point required by the script boundary."""
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    arguments = parser.parse_args()
    TopologicalPhaseSweepVerifier().execute(cast(Path, arguments.result).resolve())
    print("periodic_2d_topological_phase_sweep_verification=PASS")


if __name__ == "__main__":
    main()
