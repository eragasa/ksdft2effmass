#!/usr/bin/env python3
"""Run three separately represented two-dimensional topological benchmarks."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type ComplexMatrix = npt.NDArray[np.complex128]
type ComplexFrames = npt.NDArray[np.complex128]
type RealMatrix = npt.NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class TopologicalInput:
    """Frozen controls for the three-model topological benchmark."""

    experiment_id: str
    mesh_sizes: tuple[int, ...]
    qwz_topological_mass: float
    qwz_trivial_mass: float
    hof_flux_numerator: int
    hof_flux_denominator: int
    hof_hopping: float
    hof_topological_amplitude: float
    hof_trivial_amplitude: float
    haldane_nearest_hopping: float
    haldane_next_nearest_hopping: float
    haldane_phase: float
    haldane_topological_mass: float
    haldane_trivial_mass: float
    chern_integer_defect: float
    gauge_attack_invariant_defect: float
    minimum_gap: float

    def __post_init__(self) -> None:
        if not self.experiment_id:
            raise ValueError("experiment_id must be nonempty")
        if tuple(sorted(set(self.mesh_sizes))) != self.mesh_sizes:
            raise ValueError("mesh sizes must be strictly increasing")
        if any(size < 9 or size % 2 == 0 for size in self.mesh_sizes):
            raise ValueError("mesh sizes must be odd and at least nine")
        if self.hof_flux_denominator != 3 or self.hof_flux_numerator != 1:
            raise ValueError("version 1 freezes Hofstadter flux to 1/3")
        positive = (
            self.hof_hopping,
            self.haldane_nearest_hopping,
            self.haldane_next_nearest_hopping,
            self.chern_integer_defect,
            self.gauge_attack_invariant_defect,
            self.minimum_gap,
        )
        if any(not np.isfinite(value) or value <= 0.0 for value in positive):
            raise ValueError("positive controls must be finite")


class TopologicalInputDeserializer:
    """Deserialize the closed three-model input record."""

    __slots__ = ()

    def execute(self, payload: bytes) -> TopologicalInput:
        root = self._mapping(cast(JsonValue, json.loads(payload.decode("utf-8"))))
        if self._integer(root["schema_version"]) != 1:
            raise ValueError("unsupported schema version")
        if root["evidence_status"] != "illustrative numerical experiment":
            raise ValueError("unexpected evidence status")
        models = self._mapping(root["models"])
        qwz = self._mapping(models["qi_wu_zhang"])
        hof = self._mapping(models["hofstadter"])
        haldane = self._mapping(models["haldane"])
        tolerances = self._mapping(root["acceptance_tolerances"])
        for model in (qwz, hof, haldane):
            if self._integer(model["retained_band"]) != 0:
                raise ValueError("version 1 retains the lowest band")
        return TopologicalInput(
            experiment_id=self._string(root["experiment_id"]),
            mesh_sizes=self._integers(root["mesh_sizes"]),
            qwz_topological_mass=self._real(qwz["topological_mass"]),
            qwz_trivial_mass=self._real(qwz["trivial_mass"]),
            hof_flux_numerator=self._integer(hof["flux_numerator"]),
            hof_flux_denominator=self._integer(hof["flux_denominator"]),
            hof_hopping=self._real(hof["hopping"]),
            hof_topological_amplitude=self._real(
                hof["topological_superlattice_amplitude"]
            ),
            hof_trivial_amplitude=self._real(hof["trivial_superlattice_amplitude"]),
            haldane_nearest_hopping=self._real(haldane["nearest_hopping"]),
            haldane_next_nearest_hopping=self._real(haldane["next_nearest_hopping"]),
            haldane_phase=self._real(haldane["phase"]),
            haldane_topological_mass=self._real(haldane["topological_sublattice_mass"]),
            haldane_trivial_mass=self._real(haldane["trivial_sublattice_mass"]),
            chern_integer_defect=self._real(tolerances["chern_integer_defect"]),
            gauge_attack_invariant_defect=self._real(
                tolerances["gauge_attack_invariant_defect"]
            ),
            minimum_gap=self._real(tolerances["minimum_gap"]),
        )

    def _mapping(self, value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("expected a mapping")
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
        result = float(value)
        if not np.isfinite(result):
            raise ValueError("real values must be finite")
        return result

    def _integers(self, value: JsonValue) -> tuple[int, ...]:
        if not isinstance(value, list):
            raise TypeError("expected an integer array")
        return tuple(self._integer(item) for item in value)


class ThreeModelTopologicalExperiment:
    """Evaluate QWZ, Hofstadter, and Haldane without conflating their spaces."""

    __slots__ = ("_controls",)

    def __init__(self, controls: TopologicalInput) -> None:
        self._controls = controls

    def execute(self, input_path: Path, runner_path: Path) -> dict[str, JsonValue]:
        model_records: list[JsonValue] = []
        specifications = (
            (
                "qi_wu_zhang",
                2,
                self._controls.qwz_topological_mass,
                self._controls.qwz_trivial_mass,
                "mass",
            ),
            (
                "hofstadter",
                self._controls.hof_flux_denominator,
                self._controls.hof_topological_amplitude,
                self._controls.hof_trivial_amplitude,
                "superlattice_amplitude",
            ),
            (
                "haldane",
                2,
                self._controls.haldane_topological_mass,
                self._controls.haldane_trivial_mass,
                "sublattice_mass",
            ),
        )
        all_pass = True
        for (
            model_name,
            dimension,
            topological_value,
            trivial_value,
            parameter,
        ) in specifications:
            cases: list[JsonValue] = []
            for case_name, value in (
                ("topological", topological_value),
                ("trivial", trivial_value),
            ):
                convergence: list[JsonValue] = []
                final: dict[str, JsonValue] | None = None
                for mesh_size in self._controls.mesh_sizes:
                    analysis = self._analyze(model_name, value, mesh_size, dimension)
                    convergence.append(
                        {
                            "mesh_size": mesh_size,
                            "minimum_retained_gap": analysis["minimum_retained_gap"],
                            "retained_chern": analysis["retained_chern"],
                            "retained_chern_integer_defect": analysis[
                                "retained_chern_integer_defect"
                            ],
                            "maximum_absolute_plaquette_phase": analysis[
                                "maximum_absolute_plaquette_phase"
                            ],
                            "wilson_winding": analysis["wilson_winding"],
                        }
                    )
                    final = analysis
                if final is None:
                    raise RuntimeError("at least one mesh is required")
                expected_nonzero = case_name == "topological"
                if float(final["minimum_retained_gap"]) <= self._controls.minimum_gap:
                    raise RuntimeError("TOPOLOGICAL.GAP_CLOSED")
                if (
                    float(final["retained_chern_integer_defect"])
                    >= self._controls.chern_integer_defect
                ):
                    raise RuntimeError("TOPOLOGICAL.CHERN_NOT_QUANTIZED")
                if (
                    float(final["gauge_attack_chern_defect"])
                    >= self._controls.gauge_attack_invariant_defect
                    or float(final["gauge_attack_wilson_phase_defect"])
                    >= self._controls.gauge_attack_invariant_defect
                ):
                    raise RuntimeError("TOPOLOGICAL.GAUGE_INVARIANCE_FAILED")
                chern_integer = int(final["retained_chern_integer"])
                wilson_winding = int(final["wilson_winding"])
                case_pass = (
                    (abs(chern_integer) == 1 and abs(wilson_winding) == 1)
                    if expected_nonzero
                    else (chern_integer == 0 and wilson_winding == 0)
                )
                if not case_pass:
                    raise RuntimeError("TOPOLOGICAL.OBSTRUCTION_MISMATCH")
                all_pass = all_pass and case_pass
                cases.append(
                    {
                        "case": case_name,
                        "parameter_name": parameter,
                        "parameter_value": value,
                        "convergence": convergence,
                        "final_mesh": final,
                        "acceptance_passed": case_pass,
                    }
                )
            model_records.append(
                {
                    "model": model_name,
                    "hilbert_dimension_per_k": dimension,
                    "brillouin_coordinates": (
                        "fractional torus coordinates (u,v) in [0,1)^2"
                    ),
                    "cases": cases,
                }
            )
        return {
            "schema_version": 1,
            "experiment_id": self._controls.experiment_id,
            "evidence_status": "illustrative numerical experiment",
            "generated_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
            "provenance": {
                "input_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
                "runner_sha256": hashlib.sha256(runner_path.read_bytes()).hexdigest(),
                "python_version": platform.python_version(),
                "numpy_version": np.__version__,
            },
            "models": model_records,
            "interpretation": {
                "obstruction_test": (
                    "A nonzero retained-band Chern integer together with matching "
                    "Wilson-loop winding is the numerical obstruction diagnostic."
                ),
                "separate_spaces": (
                    "The three model errors are not combined and no model is "
                    "identified with the scalar cosine parent."
                ),
                "claim_boundary": (
                    "The result is synthetic numerical verification, not a material "
                    "calculation, scientific validation, or a general localization "
                    "theorem."
                ),
            },
            "all_acceptance_checks_passed": all_pass,
        }

    def _analyze(
        self, model_name: str, parameter: float, mesh_size: int, dimension: int
    ) -> dict[str, JsonValue]:
        energies = np.empty((mesh_size, mesh_size, dimension), dtype=np.float64)
        frames = np.empty(
            (mesh_size, mesh_size, dimension, dimension), dtype=np.complex128
        )
        for i in range(mesh_size):
            for j in range(mesh_size):
                matrix = self._hamiltonian(
                    model_name, i / mesh_size, j / mesh_size, parameter
                )
                values, vectors = np.linalg.eigh(matrix)
                energies[i, j] = values
                frames[i, j] = vectors
        minimum_gap = float(np.min(energies[:, :, 1] - energies[:, :, 0]))
        band_cherns: list[float] = []
        band_integer_defects: list[float] = []
        retained_plaquettes: RealMatrix | None = None
        retained_links_x: ComplexMatrix | None = None
        for band in range(dimension):
            links_x, links_y = self._links(frames[:, :, :, band])
            plaquettes = self._plaquette_phases(links_x, links_y)
            chern = float(np.sum(plaquettes) / (2.0 * np.pi))
            band_cherns.append(chern)
            band_integer_defects.append(abs(chern - round(chern)))
            if band == 0:
                retained_plaquettes = plaquettes
                retained_links_x = links_x
        if retained_plaquettes is None or retained_links_x is None:
            raise RuntimeError("retained-band links were not built")
        retained_chern = band_cherns[0]
        wilson_phases = self._wilson_phases(retained_links_x)
        wilson_winding = self._winding(wilson_phases)

        attacked = frames[:, :, :, 0].copy()
        for i in range(mesh_size):
            for j in range(mesh_size):
                phase = 0.37 * np.sin(4.0 * np.pi * i / mesh_size)
                phase += 0.29 * np.cos(6.0 * np.pi * j / mesh_size)
                phase += 0.13 * np.sin(2.0 * np.pi * (i + 2 * j) / mesh_size)
                attacked[i, j] *= np.exp(1j * phase)
        attacked_x, attacked_y = self._links(attacked)
        attacked_plaquettes = self._plaquette_phases(attacked_x, attacked_y)
        attacked_chern = float(np.sum(attacked_plaquettes) / (2.0 * np.pi))
        attacked_wilson = self._wilson_phases(attacked_x)
        wilson_defect = float(
            np.max(np.abs(np.angle(np.exp(1j * (wilson_phases - attacked_wilson)))))
        )
        projector_periodicity_defect = self._projector_periodicity_defect(
            model_name, parameter, mesh_size
        )
        return {
            "mesh_size": mesh_size,
            "minimum_retained_gap": minimum_gap,
            "band_cherns": band_cherns,
            "band_chern_integer_defects": band_integer_defects,
            "sum_band_cherns": float(sum(band_cherns)),
            "retained_chern": retained_chern,
            "retained_chern_integer": int(round(retained_chern)),
            "retained_chern_integer_defect": abs(
                retained_chern - round(retained_chern)
            ),
            "maximum_absolute_plaquette_phase": float(
                np.max(np.abs(retained_plaquettes))
            ),
            "wilson_phases": wilson_phases.tolist(),
            "wilson_winding": wilson_winding,
            "gauge_attack_chern_defect": abs(attacked_chern - retained_chern),
            "gauge_attack_wilson_phase_defect": wilson_defect,
            "projector_periodicity_defect": projector_periodicity_defect,
            "obstruction_detected": abs(int(round(retained_chern))) == 1
            and abs(wilson_winding) == 1,
        }

    def _hamiltonian(
        self, model_name: str, u: float, v: float, parameter: float
    ) -> ComplexMatrix:
        if model_name == "qi_wu_zhang":
            x = 2.0 * np.pi * u
            y = 2.0 * np.pi * v
            dx = np.sin(x)
            dy = np.sin(y)
            dz = parameter + np.cos(x) + np.cos(y)
            return np.array(
                [[dz, dx - 1j * dy], [dx + 1j * dy, -dz]],
                dtype=np.complex128,
            )
        if model_name == "hofstadter":
            q = self._controls.hof_flux_denominator
            p = self._controls.hof_flux_numerator
            hopping = self._controls.hof_hopping
            matrix = np.zeros((q, q), dtype=np.complex128)
            theta_x = 2.0 * np.pi * u
            ky = 2.0 * np.pi * v
            for orbital in range(q):
                matrix[orbital, orbital] = -2.0 * hopping * np.cos(
                    ky + 2.0 * np.pi * p * orbital / q
                ) + parameter * np.cos(2.0 * np.pi * orbital / q)
            for orbital in range(q - 1):
                matrix[orbital, orbital + 1] = -hopping
                matrix[orbital + 1, orbital] = -hopping
            matrix[q - 1, 0] = -hopping * np.exp(1j * theta_x)
            matrix[0, q - 1] = np.conj(matrix[q - 1, 0])
            return matrix
        if model_name == "haldane":
            x = 2.0 * np.pi * u
            y = 2.0 * np.pi * v
            nearest = self._controls.haldane_nearest_hopping
            next_nearest = self._controls.haldane_next_nearest_hopping
            phase = self._controls.haldane_phase
            off_diagonal = nearest * (1.0 + np.exp(1j * x) + np.exp(1j * y))
            signed_sines = np.sin(x) - np.sin(y) + np.sin(y - x)
            diagonal = parameter - 2.0 * next_nearest * np.sin(phase) * signed_sines
            identity = (
                2.0
                * next_nearest
                * np.cos(phase)
                * (np.cos(x) + np.cos(y) + np.cos(y - x))
            )
            return np.array(
                [
                    [identity + diagonal, off_diagonal],
                    [np.conj(off_diagonal), identity - diagonal],
                ],
                dtype=np.complex128,
            )
        raise ValueError(f"unsupported model: {model_name}")

    def _links(self, states: ComplexFrames) -> tuple[ComplexMatrix, ComplexMatrix]:
        size = states.shape[0]
        links_x = np.empty((size, size), dtype=np.complex128)
        links_y = np.empty((size, size), dtype=np.complex128)
        for i in range(size):
            for j in range(size):
                overlap_x = np.vdot(states[i, j], states[(i + 1) % size, j])
                overlap_y = np.vdot(states[i, j], states[i, (j + 1) % size])
                if abs(overlap_x) < 1.0e-12 or abs(overlap_y) < 1.0e-12:
                    raise RuntimeError("TOPOLOGICAL.NEIGHBOR_OVERLAP_TOO_SMALL")
                links_x[i, j] = overlap_x / abs(overlap_x)
                links_y[i, j] = overlap_y / abs(overlap_y)
        return links_x, links_y

    def _plaquette_phases(
        self, links_x: ComplexMatrix, links_y: ComplexMatrix
    ) -> RealMatrix:
        size = links_x.shape[0]
        phases = np.empty((size, size), dtype=np.float64)
        for i in range(size):
            for j in range(size):
                loop = (
                    links_x[i, j]
                    * links_y[(i + 1) % size, j]
                    * np.conj(links_x[i, (j + 1) % size])
                    * np.conj(links_y[i, j])
                )
                phases[i, j] = np.angle(loop)
        return phases

    def _wilson_phases(self, links_x: ComplexMatrix) -> npt.NDArray[np.float64]:
        return np.angle(np.prod(links_x, axis=0)).astype(np.float64)

    def _winding(self, phases: npt.NDArray[np.float64]) -> int:
        closed = np.concatenate((phases, phases[:1]))
        unwrapped = np.unwrap(closed)
        return int(round(float((unwrapped[-1] - unwrapped[0]) / (2.0 * np.pi))))

    def _projector_periodicity_defect(
        self, model_name: str, parameter: float, mesh_size: int
    ) -> float:
        defect = 0.0
        for index in range(mesh_size):
            coordinate = index / mesh_size
            for first, second in (
                ((0.0, coordinate), (1.0, coordinate)),
                ((coordinate, 0.0), (coordinate, 1.0)),
            ):
                _, left_vectors = np.linalg.eigh(
                    self._hamiltonian(model_name, first[0], first[1], parameter)
                )
                _, right_vectors = np.linalg.eigh(
                    self._hamiltonian(model_name, second[0], second[1], parameter)
                )
                left = np.outer(left_vectors[:, 0], np.conj(left_vectors[:, 0]))
                right = np.outer(right_vectors[:, 0], np.conj(right_vectors[:, 0]))
                defect = max(defect, float(np.linalg.norm(left - right, ord=2)))
        return defect


class TopologicalResultSerializer:
    """Serialize a closed JSON-compatible result."""

    __slots__ = ()

    def execute(self, result: dict[str, JsonValue]) -> bytes:
        return (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> None:
    """CLI entry point required by the script boundary."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    controls = TopologicalInputDeserializer().execute(arguments.input.read_bytes())
    result = ThreeModelTopologicalExperiment(controls).execute(
        arguments.input, Path(__file__)
    )
    arguments.output.write_bytes(TopologicalResultSerializer().execute(result))


if __name__ == "__main__":
    main()
