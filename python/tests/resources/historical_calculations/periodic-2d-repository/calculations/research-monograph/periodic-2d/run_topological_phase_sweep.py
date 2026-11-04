#!/usr/bin/env python3
"""Run non-DFT parameter sweeps for the three topological controls."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type ComplexMatrix = npt.NDArray[np.complex128]


class TopologicalPhaseSweep:
    """Evaluate gaps and lattice Chern sums along declared parameter axes."""

    __slots__ = ("_root", "_mesh")

    def __init__(self, payload: bytes) -> None:
        self._root = self._mapping(cast(JsonValue, json.loads(payload.decode())))
        if self._integer(self._root["schema_version"]) != 1:
            raise ValueError("unsupported sweep schema")
        self._mesh = self._integer(self._root["mesh_size"])
        if self._mesh < 9 or self._mesh % 2 == 0:
            raise ValueError("mesh must be odd and at least nine")

    def execute(self, input_path: Path, runner_path: Path) -> dict[str, JsonValue]:
        models = self._mapping(self._root["models"])
        tolerances = self._mapping(self._root["acceptance"])
        exclusion = self._real(tolerances["analytic_boundary_exclusion_width"])
        integer_tolerance = self._real(tolerances["chern_integer_defect"])
        endpoint_gap = self._real(tolerances["minimum_endpoint_gap"])
        records: list[JsonValue] = []
        all_passed = True
        for model_name in ("qi_wu_zhang", "hofstadter", "haldane"):
            specification = self._mapping(models[model_name])
            parameters = np.linspace(
                self._real(specification["start"]),
                self._real(specification["stop"]),
                self._integer(specification["count"]),
            )
            samples: list[JsonValue] = []
            for parameter in parameters:
                analysis = self._analyze(model_name, float(parameter), specification)
                expected = self._expected(model_name, float(parameter), specification)
                distance = self._boundary_distance(
                    model_name, float(parameter), specification
                )
                rounded = int(round(analysis["retained_chern"]))
                sample_passed = analysis[
                    "retained_chern_integer_defect"
                ] < integer_tolerance and (
                    expected is None or distance <= exclusion or rounded == expected
                )
                all_passed = all_passed and sample_passed
                samples.append(
                    {
                        "parameter": float(parameter),
                        "minimum_retained_gap": analysis["minimum_retained_gap"],
                        "analytic_boundary_gap": self._analytic_gap(
                            model_name, float(parameter), specification
                        ),
                        "retained_chern": analysis["retained_chern"],
                        "retained_chern_integer": rounded,
                        "retained_chern_integer_defect": analysis[
                            "retained_chern_integer_defect"
                        ],
                        "band_cherns": analysis["band_cherns"],
                        "analytic_expected_retained_chern": expected,
                        "analytic_boundary_distance": distance,
                        "acceptance_passed": sample_passed,
                    }
                )
            first_gap = self._real(self._mapping(samples[0])["minimum_retained_gap"])
            last_gap = self._real(self._mapping(samples[-1])["minimum_retained_gap"])
            endpoints_passed = first_gap > endpoint_gap and last_gap > endpoint_gap
            all_passed = all_passed and endpoints_passed
            records.append(
                {
                    "model": model_name,
                    "parameter_name": self._string(specification["parameter_name"]),
                    "samples": samples,
                    "chern_change_brackets": self._change_brackets(samples),
                    "minimum_sampled_gap": min(
                        self._real(self._mapping(value)["minimum_retained_gap"])
                        for value in samples
                    ),
                    "endpoint_gaps_passed": endpoints_passed,
                }
            )
        return {
            "schema_version": 1,
            "experiment_id": self._string(self._root["experiment_id"]),
            "evidence_status": "illustrative numerical experiment",
            "generated_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
            "authorization_checkpoint": "RM-PERIODIC-2D-NONDFT-STUDY-HC06",
            "provenance": {
                "input_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
                "runner_sha256": hashlib.sha256(runner_path.read_bytes()).hexdigest(),
                "python_version": platform.python_version(),
                "numpy_version": np.__version__,
            },
            "mesh_size": self._mesh,
            "models": records,
            "all_acceptance_checks_passed": all_passed,
            "claim_boundary": (
                "These sweeps are synthetic numerical verification of declared "
                "finite Bloch models, not material phase diagrams or scientific "
                "validation."
            ),
        }

    def _analyze(
        self, model_name: str, parameter: float, specification: dict[str, JsonValue]
    ) -> dict[str, JsonValue]:
        dimension = 3 if model_name == "hofstadter" else 2
        frames = np.empty(
            (self._mesh, self._mesh, dimension, dimension), dtype=np.complex128
        )
        energies = np.empty((self._mesh, self._mesh, dimension), dtype=float)
        for i in range(self._mesh):
            for j in range(self._mesh):
                matrix = self._hamiltonian(
                    model_name, i / self._mesh, j / self._mesh, parameter, specification
                )
                values, vectors = np.linalg.eigh(matrix)
                energies[i, j] = values
                frames[i, j] = vectors
        cherns: list[float] = []
        for band in range(dimension):
            states = frames[:, :, :, band]
            overlap_x = np.sum(states.conj() * np.roll(states, -1, axis=0), axis=2)
            overlap_y = np.sum(states.conj() * np.roll(states, -1, axis=1), axis=2)
            links_x = overlap_x / np.abs(overlap_x)
            links_y = overlap_y / np.abs(overlap_y)
            plaquette = np.angle(
                links_x
                * np.roll(links_y, -1, axis=0)
                * np.roll(links_x.conj(), -1, axis=1)
                * links_y.conj()
            )
            cherns.append(float(np.sum(plaquette) / (2.0 * np.pi)))
        retained = cherns[0]
        return {
            "minimum_retained_gap": float(
                np.min(energies[:, :, 1] - energies[:, :, 0])
            ),
            "retained_chern": retained,
            "retained_chern_integer_defect": abs(retained - round(retained)),
            "band_cherns": cherns,
        }

    def _hamiltonian(
        self,
        model_name: str,
        u: float,
        v: float,
        parameter: float,
        specification: dict[str, JsonValue],
    ) -> ComplexMatrix:
        x = 2.0 * np.pi * u
        y = 2.0 * np.pi * v
        if model_name == "qi_wu_zhang":
            dz = parameter + np.cos(x) + np.cos(y)
            return np.array(
                [
                    [dz, np.sin(x) - 1j * np.sin(y)],
                    [np.sin(x) + 1j * np.sin(y), -dz],
                ],
                dtype=np.complex128,
            )
        if model_name == "hofstadter":
            q = self._integer(specification["flux_denominator"])
            p = self._integer(specification["flux_numerator"])
            hopping = self._real(specification["hopping"])
            matrix = np.zeros((q, q), dtype=np.complex128)
            for orbital in range(q):
                matrix[orbital, orbital] = -2.0 * hopping * np.cos(
                    y + 2.0 * np.pi * p * orbital / q
                ) + parameter * np.cos(2.0 * np.pi * orbital / q)
            for orbital in range(q - 1):
                matrix[orbital, orbital + 1] = -hopping
                matrix[orbital + 1, orbital] = -hopping
            matrix[q - 1, 0] = -hopping * np.exp(1j * x)
            matrix[0, q - 1] = np.conj(matrix[q - 1, 0])
            return matrix
        nearest = self._real(specification["nearest_hopping"])
        next_nearest = self._real(specification["next_nearest_hopping"])
        phase = self._real(specification["phase"])
        off_diagonal = nearest * (1.0 + np.exp(1j * x) + np.exp(1j * y))
        signed_sines = np.sin(x) - np.sin(y) + np.sin(y - x)
        diagonal = parameter - 2.0 * next_nearest * np.sin(phase) * signed_sines
        identity = (
            2.0 * next_nearest * np.cos(phase) * (np.cos(x) + np.cos(y) + np.cos(y - x))
        )
        return np.array(
            [
                [identity + diagonal, off_diagonal],
                [np.conj(off_diagonal), identity - diagonal],
            ],
            dtype=np.complex128,
        )

    def _expected(
        self, model_name: str, parameter: float, specification: dict[str, JsonValue]
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
            boundary = self._real(specification["analytic_boundary_magnitude"])
            if abs(abs(parameter) - boundary) < 1.0e-14:
                return None
            return -1 if abs(parameter) < boundary else 0
        return None

    def _boundary_distance(
        self, model_name: str, parameter: float, specification: dict[str, JsonValue]
    ) -> float:
        if model_name == "qi_wu_zhang":
            boundaries = self._reals(specification["analytic_boundaries"])
            return min(abs(parameter - boundary) for boundary in boundaries)
        if model_name == "haldane":
            boundary = self._real(specification["analytic_boundary_magnitude"])
            return min(abs(parameter - boundary), abs(parameter + boundary))
        return float("inf")

    def _analytic_gap(
        self, model_name: str, parameter: float, specification: dict[str, JsonValue]
    ) -> float | None:
        if model_name == "qi_wu_zhang":
            return 2.0 * min(abs(parameter + 2.0), abs(parameter), abs(parameter - 2.0))
        if model_name == "haldane":
            boundary = self._real(specification["analytic_boundary_magnitude"])
            return 2.0 * min(abs(parameter - boundary), abs(parameter + boundary))
        return None

    def _change_brackets(self, samples: list[JsonValue]) -> list[JsonValue]:
        brackets: list[JsonValue] = []
        for left_value, right_value in zip(samples, samples[1:], strict=False):
            left = self._mapping(left_value)
            right = self._mapping(right_value)
            if left["retained_chern_integer"] != right["retained_chern_integer"]:
                brackets.append(
                    {
                        "left_parameter": left["parameter"],
                        "right_parameter": right["parameter"],
                        "left_chern": left["retained_chern_integer"],
                        "right_chern": right["retained_chern_integer"],
                    }
                )
        return brackets

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


def main() -> None:
    """CLI entry point required by the script boundary."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    input_path = cast(Path, arguments.input).resolve()
    output_path = cast(Path, arguments.output).resolve()
    result = TopologicalPhaseSweep(input_path.read_bytes()).execute(
        input_path, Path(__file__).resolve()
    )
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
