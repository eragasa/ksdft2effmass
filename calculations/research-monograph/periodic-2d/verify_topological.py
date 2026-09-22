#!/usr/bin/env python3
"""Independently verify the three topological-model calculations."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type ComplexMatrix = npt.NDArray[np.complex128]
type ComplexProjectors = npt.NDArray[np.complex128]
type RealVector = npt.NDArray[np.float64]


class TopologicalResultVerifier:
    """Rebuild spectra and topology through projector Bargmann invariants."""

    __slots__ = ("_input", "_result")

    def __init__(self, input_payload: bytes, result_payload: bytes) -> None:
        self._input = self._mapping(
            cast(JsonValue, json.loads(input_payload.decode("utf-8")))
        )
        self._result = self._mapping(
            cast(JsonValue, json.loads(result_payload.decode("utf-8")))
        )

    def execute(self, input_path: Path, runner_path: Path) -> None:
        if self._integer(self._result["schema_version"]) != 1:
            raise ValueError("unsupported result schema")
        if self._result["evidence_status"] != "illustrative numerical experiment":
            raise ValueError("unexpected evidence status")
        provenance = self._mapping(self._result["provenance"])
        self._equal(
            self._string(provenance["input_sha256"]),
            hashlib.sha256(input_path.read_bytes()).hexdigest(),
            "input content identity",
        )
        self._equal(
            self._string(provenance["runner_sha256"]),
            hashlib.sha256(runner_path.read_bytes()).hexdigest(),
            "runner content identity",
        )
        input_models = self._mapping(self._input["models"])
        tolerance_values = self._mapping(self._input["acceptance_tolerances"])
        invariant_tolerance = self._real(
            tolerance_values["gauge_attack_invariant_defect"]
        )
        model_values = self._array(self._result["models"])
        expected_names = ("qi_wu_zhang", "hofstadter", "haldane")
        self._equal(len(model_values), len(expected_names), "model count")
        for model_value, expected_name in zip(
            model_values, expected_names, strict=True
        ):
            model = self._mapping(model_value)
            model_name = self._string(model["model"])
            self._equal(model_name, expected_name, "model order")
            model_input = self._mapping(input_models[model_name])
            cases = self._array(model["cases"])
            self._equal(len(cases), 2, f"{model_name} case count")
            for case_value, expected_case in zip(
                cases, ("topological", "trivial"), strict=True
            ):
                case = self._mapping(case_value)
                case_name = self._string(case["case"])
                self._equal(case_name, expected_case, f"{model_name} case order")
                parameter = self._real(case["parameter_value"])
                convergence = self._array(case["convergence"])
                for record_value in convergence:
                    record = self._mapping(record_value)
                    mesh_size = self._integer(record["mesh_size"])
                    rebuilt = self._analyze(
                        model_name, model_input, parameter, mesh_size
                    )
                    self._close(
                        self._real(record["minimum_retained_gap"]),
                        rebuilt["minimum_retained_gap"],
                        2.0e-12,
                        f"{model_name} {case_name} gap N={mesh_size}",
                    )
                    self._close(
                        self._real(record["retained_chern"]),
                        rebuilt["retained_chern"],
                        2.0e-12,
                        f"{model_name} {case_name} Chern N={mesh_size}",
                    )
                    self._equal(
                        self._integer(record["wilson_winding"]),
                        rebuilt["wilson_winding"],
                        f"{model_name} {case_name} winding N={mesh_size}",
                    )
                final = self._mapping(case["final_mesh"])
                final_mesh = self._integer(final["mesh_size"])
                rebuilt = self._analyze(model_name, model_input, parameter, final_mesh)
                band_cherns = self._reals(final["band_cherns"])
                self._equal(
                    len(band_cherns),
                    len(rebuilt["band_cherns"]),
                    f"{model_name} band count",
                )
                for band, (recorded, reconstructed) in enumerate(
                    zip(band_cherns, rebuilt["band_cherns"], strict=True)
                ):
                    self._close(
                        recorded,
                        reconstructed,
                        2.0e-12,
                        f"{model_name} {case_name} band {band} Chern",
                    )
                recorded_phases = np.asarray(
                    self._reals(final["wilson_phases"]), dtype=np.float64
                )
                rebuilt_phases = np.asarray(rebuilt["wilson_phases"], dtype=np.float64)
                phase_defect = float(
                    np.max(
                        np.abs(
                            np.angle(np.exp(1j * (recorded_phases - rebuilt_phases)))
                        )
                    )
                )
                if phase_defect > 3.0e-11:
                    raise AssertionError(
                        f"{model_name} {case_name} Wilson phase defect: {phase_defect}"
                    )
                self._close(
                    self._real(final["projector_periodicity_defect"]),
                    rebuilt["projector_periodicity_defect"],
                    3.0e-12,
                    f"{model_name} {case_name} projector periodicity",
                )
                if self._real(final["gauge_attack_chern_defect"]) > invariant_tolerance:
                    raise AssertionError(f"{model_name} gauge-attacked Chern changed")
                if (
                    self._real(final["gauge_attack_wilson_phase_defect"])
                    > invariant_tolerance
                ):
                    raise AssertionError(
                        f"{model_name} gauge-attacked Wilson loop changed"
                    )
                topological = case_name == "topological"
                chern_integer = int(round(rebuilt["retained_chern"]))
                winding = rebuilt["wilson_winding"]
                if topological and (abs(chern_integer) != 1 or abs(winding) != 1):
                    raise AssertionError(f"{model_name} obstruction was not detected")
                if not topological and (chern_integer != 0 or winding != 0):
                    raise AssertionError(f"{model_name} trivial control is nontrivial")
                if not self._boolean(case["acceptance_passed"]):
                    raise AssertionError(f"{model_name} {case_name} did not pass")
        if not self._boolean(self._result["all_acceptance_checks_passed"]):
            raise AssertionError("aggregate acceptance flag is false")

    def analyze_case(
        self,
        model_name: str,
        model_input: dict[str, JsonValue],
        parameter: float,
        mesh_size: int,
    ) -> dict[str, float | int | list[float]]:
        """Reconstruct one case through projector Bargmann invariants."""
        return self._analyze(model_name, model_input, parameter, mesh_size)

    def _analyze(
        self,
        model_name: str,
        model_input: dict[str, JsonValue],
        parameter: float,
        mesh_size: int,
    ) -> dict[str, float | int | list[float]]:
        dimension = 3 if model_name == "hofstadter" else 2
        energies = np.empty((mesh_size, mesh_size, dimension), dtype=np.float64)
        projectors = np.empty(
            (dimension, mesh_size, mesh_size, dimension, dimension),
            dtype=np.complex128,
        )
        for i in range(mesh_size):
            for j in range(mesh_size):
                matrix = self._hamiltonian(
                    model_name, model_input, parameter, i / mesh_size, j / mesh_size
                )
                values, vectors = np.linalg.eigh(matrix)
                energies[i, j] = values
                for band in range(dimension):
                    state = vectors[:, band]
                    projectors[band, i, j] = np.outer(state, np.conj(state))
        band_cherns: list[float] = []
        retained_phases: RealVector | None = None
        for band in range(dimension):
            plaquette_sum = 0.0
            for i in range(mesh_size):
                for j in range(mesh_size):
                    loop = np.trace(
                        projectors[band, i, j]
                        @ projectors[band, (i + 1) % mesh_size, j]
                        @ projectors[band, (i + 1) % mesh_size, (j + 1) % mesh_size]
                        @ projectors[band, i, (j + 1) % mesh_size]
                    )
                    plaquette_sum += float(np.angle(loop))
            band_cherns.append(plaquette_sum / (2.0 * np.pi))
            if band == 0:
                phases = np.empty(mesh_size, dtype=np.float64)
                for j in range(mesh_size):
                    product = np.eye(dimension, dtype=np.complex128)
                    for i in range(mesh_size):
                        product = product @ projectors[band, i, j]
                    product = product @ projectors[band, 0, j]
                    phases[j] = np.angle(np.trace(product))
                retained_phases = phases
        if retained_phases is None:
            raise RuntimeError("retained Wilson phases were not constructed")
        closed = np.concatenate((retained_phases, retained_phases[:1]))
        unwrapped = np.unwrap(closed)
        winding = int(round(float((unwrapped[-1] - unwrapped[0]) / (2.0 * np.pi))))
        periodicity_defect = 0.0
        for index in range(mesh_size):
            coordinate = index / mesh_size
            for left_coordinates, right_coordinates in (
                ((0.0, coordinate), (1.0, coordinate)),
                ((coordinate, 0.0), (coordinate, 1.0)),
            ):
                _, left = np.linalg.eigh(
                    self._hamiltonian(
                        model_name,
                        model_input,
                        parameter,
                        left_coordinates[0],
                        left_coordinates[1],
                    )
                )
                _, right = np.linalg.eigh(
                    self._hamiltonian(
                        model_name,
                        model_input,
                        parameter,
                        right_coordinates[0],
                        right_coordinates[1],
                    )
                )
                left_projector = np.outer(left[:, 0], np.conj(left[:, 0]))
                right_projector = np.outer(right[:, 0], np.conj(right[:, 0]))
                periodicity_defect = max(
                    periodicity_defect,
                    float(np.linalg.norm(left_projector - right_projector, ord=2)),
                )
        return {
            "minimum_retained_gap": float(
                np.min(energies[:, :, 1] - energies[:, :, 0])
            ),
            "band_cherns": band_cherns,
            "retained_chern": band_cherns[0],
            "wilson_phases": retained_phases.tolist(),
            "wilson_winding": winding,
            "projector_periodicity_defect": periodicity_defect,
        }

    def _hamiltonian(
        self,
        model_name: str,
        model_input: dict[str, JsonValue],
        parameter: float,
        u: float,
        v: float,
    ) -> ComplexMatrix:
        x = 2.0 * np.pi * u
        y = 2.0 * np.pi * v
        if model_name == "qi_wu_zhang":
            dx = np.sin(x)
            dy = np.sin(y)
            dz = parameter + np.cos(x) + np.cos(y)
            return np.asarray(
                [[dz, dx - 1j * dy], [dx + 1j * dy, -dz]],
                dtype=np.complex128,
            )
        if model_name == "hofstadter":
            numerator = self._integer(model_input["flux_numerator"])
            denominator = self._integer(model_input["flux_denominator"])
            hopping = self._real(model_input["hopping"])
            matrix = np.zeros((denominator, denominator), dtype=np.complex128)
            for orbital in range(denominator):
                matrix[orbital, orbital] = -2.0 * hopping * np.cos(
                    y + 2.0 * np.pi * numerator * orbital / denominator
                ) + parameter * np.cos(2.0 * np.pi * orbital / denominator)
            for orbital in range(denominator - 1):
                matrix[orbital, orbital + 1] = -hopping
                matrix[orbital + 1, orbital] = -hopping
            matrix[denominator - 1, 0] = -hopping * np.exp(1j * x)
            matrix[0, denominator - 1] = np.conj(matrix[denominator - 1, 0])
            return matrix
        if model_name == "haldane":
            nearest = self._real(model_input["nearest_hopping"])
            next_nearest = self._real(model_input["next_nearest_hopping"])
            phase = self._real(model_input["phase"])
            coupling = nearest * (1.0 + np.exp(1j * x) + np.exp(1j * y))
            mass = parameter - 2.0 * next_nearest * np.sin(phase) * (
                np.sin(x) - np.sin(y) + np.sin(y - x)
            )
            shift = (
                2.0
                * next_nearest
                * np.cos(phase)
                * (np.cos(x) + np.cos(y) + np.cos(y - x))
            )
            return np.asarray(
                [
                    [shift + mass, coupling],
                    [np.conj(coupling), shift - mass],
                ],
                dtype=np.complex128,
            )
        raise ValueError(f"unsupported model: {model_name}")

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

    def _boolean(self, value: JsonValue) -> bool:
        if not isinstance(value, bool):
            raise TypeError("expected a boolean")
        return value

    def _integer(self, value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("expected an integer")
        return value

    def _real(self, value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("expected a real number")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError("expected a finite real number")
        return result

    def _reals(self, value: JsonValue) -> list[float]:
        return [self._real(item) for item in self._array(value)]

    def _close(
        self, actual: float, expected: float, tolerance: float, label: str
    ) -> None:
        if abs(actual - expected) > tolerance:
            raise AssertionError(
                f"{label}: actual={actual:.16e}, expected={expected:.16e}"
            )

    def _equal(self, actual: str | int, expected: str | int, label: str) -> None:
        if actual != expected:
            raise AssertionError(f"{label}: actual={actual!r}, expected={expected!r}")


def main() -> None:
    """CLI entry point required by the script boundary."""
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    arguments = parser.parse_args()
    input_path = arguments.result.with_name("topological-input.json")
    runner_path = arguments.result.with_name("run_topological.py")
    TopologicalResultVerifier(
        input_path.read_bytes(), arguments.result.read_bytes()
    ).execute(input_path, runner_path)
    print("periodic_2d_topological_verification=PASS")


if __name__ == "__main__":
    main()
