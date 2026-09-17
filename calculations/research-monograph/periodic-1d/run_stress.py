#!/usr/bin/env python3
"""Stress-test assumptions behind the isolated-band periodic reduction."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt
from scipy.linalg import eigh  # type: ignore[import-untyped]

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type RealVector = npt.NDArray[np.float64]
type ComplexVector = npt.NDArray[np.complex128]
type ComplexMatrix = npt.NDArray[np.complex128]


@dataclass(frozen=True, slots=True)
class PotentialShape:
    """Represent a finite real Fourier-series modification of the potential."""

    identifier: str
    constant: float
    cosine_coefficients: tuple[float, ...]
    sine_coefficients: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class StressInput:
    """Represent bounded adversarial parameter and route perturbations."""

    experiment_id: str
    potential_strengths: tuple[float, ...]
    plane_wave_cutoffs: tuple[int, ...]
    plane_wave_reference_cutoff: int
    finite_difference_points: tuple[int, ...]
    compared_band_count: int
    stress_band_indices: tuple[int, ...]
    potential_shapes: tuple[PotentialShape, ...]
    reciprocal_mesh_sizes: tuple[int, ...]
    hopping_range_cells: int
    withheld_mesh_size: int
    isolation_gap_threshold: float
    route_stress_potential_strength: float
    route_stress_mesh_size: int
    route_stress_hopping_range_cells: int


class StressInputDeserializer:
    """Deserialize the closed version-1 stress input."""

    __slots__ = ()

    def execute(self, payload: bytes) -> StressInput:
        value = cast(JsonValue, json.loads(payload.decode("utf-8")))
        if not isinstance(value, dict):
            raise TypeError("stress input must be a JSON object")
        if value["schema_version"] != 1:
            raise ValueError("unsupported stress input schema version")
        if value["evidence_status"] != "illustrative numerical stress test":
            raise ValueError("unexpected stress-test evidence status")
        result = StressInput(
            experiment_id=self._string(value["experiment_id"]),
            potential_strengths=self._reals(value["potential_strengths"]),
            plane_wave_cutoffs=self._integers(value["plane_wave_cutoffs"]),
            plane_wave_reference_cutoff=self._integer(
                value["plane_wave_reference_cutoff"]
            ),
            finite_difference_points=self._integers(
                value["finite_difference_points"]
            ),
            compared_band_count=self._integer(value["compared_band_count"]),
            stress_band_indices=self._integers(value["stress_band_indices"]),
            potential_shapes=self._potential_shapes(value["potential_shapes"]),
            reciprocal_mesh_sizes=self._integers(value["reciprocal_mesh_sizes"]),
            hopping_range_cells=self._integer(value["hopping_range_cells"]),
            withheld_mesh_size=self._integer(value["withheld_mesh_size"]),
            isolation_gap_threshold=self._real(value["isolation_gap_threshold"]),
            route_stress_potential_strength=self._real(
                value["route_stress_potential_strength"]
            ),
            route_stress_mesh_size=self._integer(value["route_stress_mesh_size"]),
            route_stress_hopping_range_cells=self._integer(
                value["route_stress_hopping_range_cells"]
            ),
        )
        if tuple(sorted(set(result.potential_strengths))) != result.potential_strengths:
            raise ValueError("potential strengths must be strictly increasing")
        if result.potential_strengths[0] != 0.0:
            raise ValueError("stress suite must include the gap-closing free limit")
        if result.plane_wave_reference_cutoff <= result.plane_wave_cutoffs[-1]:
            raise ValueError("reference cutoff must exceed study cutoffs")
        if 2 * result.plane_wave_cutoffs[0] + 1 < result.compared_band_count:
            raise ValueError("smallest plane-wave basis cannot hold compared bands")
        if (
            not result.stress_band_indices
            or result.stress_band_indices[-1] >= result.compared_band_count
        ):
            raise ValueError("stress band indices must lie within compared bands")
        if any(size % 2 != 0 for size in result.reciprocal_mesh_sizes):
            raise ValueError("reciprocal mesh sizes must be even")
        return result

    @staticmethod
    def _string(value: JsonValue) -> str:
        if not isinstance(value, str) or not value:
            raise TypeError("value must be a nonempty string")
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
            raise TypeError("value must be an array")
        return tuple(self._real(item) for item in value)

    def _integers(self, value: JsonValue) -> tuple[int, ...]:
        if not isinstance(value, list):
            raise TypeError("value must be an array")
        return tuple(self._integer(item) for item in value)

    def _potential_shapes(self, value: JsonValue) -> tuple[PotentialShape, ...]:
        if not isinstance(value, list):
            raise TypeError("potential_shapes must be an array")
        shapes: list[PotentialShape] = []
        for item in value:
            if not isinstance(item, dict):
                raise TypeError("potential shape must be an object")
            cosine = self._reals(item["cosine_coefficients"])
            sine = self._reals(item["sine_coefficients"])
            if len(cosine) != len(sine) or not cosine:
                raise ValueError("potential harmonic arrays must be nonempty and equal")
            shapes.append(
                PotentialShape(
                    identifier=self._string(item["id"]),
                    constant=self._real(item["constant"]),
                    cosine_coefficients=cosine,
                    sine_coefficients=sine,
                )
            )
        if len({shape.identifier for shape in shapes}) != len(shapes):
            raise ValueError("potential shape identifiers must be unique")
        return tuple(shapes)


class PeriodicReductionStressExperiment:
    """Challenge isolation, convergence, sampling, gauge, and route assumptions."""

    __slots__ = ()
    _PERIOD = 2.0 * np.pi

    def execute(
        self, stress: StressInput, input_path: Path, script_path: Path
    ) -> bytes:
        repository_root = script_path.parents[3]
        payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": stress.experiment_id,
            "evidence_status": "illustrative numerical stress test",
            "calculation_status": "calculated illustrative result",
            "potential_amplitude_stress": self._potential_stress(stress),
            "potential_shape_stress": self._potential_shape_stress(stress),
            "mesh_band_and_isolation_stress": self._mesh_stress(stress),
            "gauge_covariance_stress": self._gauge_stress(stress),
            "route_assumption_stress": self._route_stress(stress),
            "provenance": {
                "input_path": input_path.relative_to(repository_root).as_posix(),
                "input_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
                "script_path": script_path.relative_to(repository_root).as_posix(),
                "script_sha256": hashlib.sha256(script_path.read_bytes()).hexdigest(),
                "python_version": platform.python_version(),
                "numpy_version": np.__version__,
                "floating_point": "IEEE-754 binary64",
            },
            "claim_boundary": (
                "Adversarial numerical verification of the frozen cosine-model "
                "workflow; not material validation or uncertainty quantification."
            ),
        }
        serialized = json.dumps(
            payload, indent=2, sort_keys=True, allow_nan=False
        )
        return (serialized + "\n").encode("utf-8")

    def _potential_stress(self, stress: StressInput) -> list[JsonValue]:
        sample_momenta = (-0.5, -0.25, 0.0, 0.25, 0.5)
        records: list[JsonValue] = []
        for strength in stress.potential_strengths:
            reference = np.asarray(
                [
                    self._pw_eigensystem(
                        momentum, strength, stress.plane_wave_reference_cutoff
                    )[0][: stress.compared_band_count]
                    for momentum in sample_momenta
                ]
            )
            cutoff_records: list[JsonValue] = []
            for cutoff in stress.plane_wave_cutoffs:
                values = np.asarray(
                    [
                        self._pw_eigensystem(momentum, strength, cutoff)[0][
                            : stress.compared_band_count
                        ]
                        for momentum in sample_momenta
                    ]
                )
                cutoff_records.append(
                    {
                        "cutoff": cutoff,
                        "maximum_low_band_error": float(
                            np.max(np.abs(values - reference))
                        ),
                    }
                )
            fd_records: list[JsonValue] = []
            for points in stress.finite_difference_points:
                values = np.asarray(
                    [
                        self._fd_energies(
                            momentum,
                            self._cosine_shape(strength),
                            points,
                            stress.compared_band_count,
                        )
                        for momentum in sample_momenta
                    ]
                )
                fd_records.append(
                    {
                        "points": points,
                        "maximum_low_band_error": float(
                            np.max(np.abs(values - reference))
                        ),
                    }
                )
            boundary = self._pw_eigensystem(
                0.5, strength, stress.plane_wave_reference_cutoff
            )[0]
            positive = np.asarray(
                [
                    self._pw_eigensystem(
                        momentum,
                        strength,
                        stress.plane_wave_cutoffs[-1],
                    )[0][: stress.compared_band_count]
                    for momentum in sample_momenta
                ]
            )
            negative = np.asarray(
                [
                    self._pw_eigensystem(
                        momentum,
                        -strength,
                        stress.plane_wave_cutoffs[-1],
                    )[0][: stress.compared_band_count]
                    for momentum in sample_momenta
                ]
            )
            gap = float(boundary[1] - boundary[0])
            records.append(
                {
                    "potential_strength": strength,
                    "zone_boundary_gap": gap,
                    "isolated_band_status": (
                        "pass"
                        if gap > stress.isolation_gap_threshold
                        else "failed_gap_closure"
                    ),
                    "potential_sign_invariance_maximum_error": float(
                        np.max(np.abs(positive - negative))
                    ),
                    "plane_wave_cutoff_study": cutoff_records,
                    "finite_difference_grid_study": fd_records,
                }
            )
        return records

    def _potential_shape_stress(self, stress: StressInput) -> dict[str, JsonValue]:
        sample_momenta = np.linspace(-0.5, 0.5, 33)
        baseline_energies: RealVector | None = None
        translated_energies: RealVector | None = None
        shifted_energies: RealVector | None = None
        records: list[JsonValue] = []
        for shape in stress.potential_shapes:
            reference = np.asarray(
                [
                    self._shape_pw_eigensystem(
                        momentum, shape, stress.plane_wave_reference_cutoff
                    )[0][: stress.compared_band_count]
                    for momentum in sample_momenta
                ]
            )
            finite_difference = np.asarray(
                [
                    self._fd_energies(
                        momentum,
                        shape,
                        stress.finite_difference_points[-1],
                        stress.compared_band_count,
                    )
                    for momentum in sample_momenta
                ]
            )
            gaps = self._minimum_band_gaps(reference)
            records.append(
                {
                    "id": shape.identifier,
                    "minimum_adjacent_gaps": [float(value) for value in gaps],
                    "finest_grid_maximum_band_error": float(
                        np.max(np.abs(finite_difference - reference))
                    ),
                    "time_reversal_energy_residual": float(
                        np.max(np.abs(reference - reference[::-1]))
                    ),
                }
            )
            flat = reference.reshape(-1)
            if shape.identifier == "baseline_cosine":
                baseline_energies = flat
            elif shape.identifier == "translated_cosine":
                translated_energies = flat
            elif shape.identifier == "constant_shifted_cosine":
                shifted_energies = flat
        if (
            baseline_energies is None
            or translated_energies is None
            or shifted_energies is None
        ):
            raise ValueError("required covariance-control potential shapes are missing")
        return {
            "cases": records,
            "translation_isospectral_maximum_error": float(
                np.max(np.abs(translated_energies - baseline_energies))
            ),
            "constant_shift_covariance_maximum_error": float(
                np.max(np.abs((shifted_energies - 0.2) - baseline_energies))
            ),
        }

    def _mesh_stress(self, stress: StressInput) -> list[JsonValue]:
        records: list[JsonValue] = []
        withheld_momenta = np.linspace(-0.5, 0.5, stress.withheld_mesh_size)
        required_band_count = max(stress.stress_band_indices) + 2
        for strength in stress.potential_strengths:
            shape = self._cosine_shape(strength)
            withheld_bands = np.asarray(
                [
                    self._shape_pw_eigensystem(
                        momentum, shape, stress.plane_wave_cutoffs[-1]
                    )[0][:required_band_count]
                    for momentum in withheld_momenta
                ]
            )
            for mesh_size in stress.reciprocal_mesh_sizes:
                momenta, band_energies, band_states = self._bands_mesh(
                    shape,
                    stress.plane_wave_cutoffs[-1],
                    mesh_size,
                    required_band_count,
                )
                minimum_gaps = self._minimum_band_gaps(band_energies)
                representatives = np.arange(-mesh_size // 2, mesh_size // 2)
                retained = np.abs(representatives) <= stress.hopping_range_cells
                for band_index in stress.stress_band_indices:
                    energies = band_energies[:, band_index]
                    states = band_states[:, band_index, :]
                    overlap_minimum = self._minimum_sewn_overlap(states)
                    hoppings = (
                        np.exp(
                            -1j
                            * np.outer(representatives * self._PERIOD, momenta)
                        )
                        @ energies
                        / mesh_size
                    )
                    withheld_model = (
                        np.exp(
                            1j
                            * np.outer(
                                withheld_momenta,
                                representatives[retained] * self._PERIOD,
                            )
                        )
                        @ hoppings[retained]
                    ).real
                    reconstruction = (
                        np.exp(
                            1j
                            * np.outer(momenta, representatives * self._PERIOD)
                        )
                        @ hoppings
                    )
                    gap = float(minimum_gaps[band_index])
                    records.append(
                        {
                            "potential_strength": strength,
                            "band_index": band_index,
                            "mesh_size": mesh_size,
                            "minimum_adjacent_gap": gap,
                            "isolation_applicable": (
                                gap > stress.isolation_gap_threshold
                            ),
                            "minimum_sewn_neighbor_overlap": overlap_minimum,
                            "full_reconstruction_maximum_error": float(
                                np.max(np.abs(reconstruction.real - energies))
                            ),
                            "fixed_range_withheld_maximum_error": float(
                                np.max(
                                    np.abs(
                                        withheld_bands[:, band_index]
                                        - withheld_model
                                    )
                                )
                            ),
                        }
                    )
        return records

    def _gauge_stress(self, stress: StressInput) -> dict[str, JsonValue]:
        strength = stress.route_stress_potential_strength
        mesh_size = stress.route_stress_mesh_size
        _, _, all_states = self._bands_mesh(
            self._cosine_shape(strength),
            stress.plane_wave_cutoffs[-1],
            mesh_size,
            1,
        )
        states = all_states[:, 0, :]
        phases = np.exp(
            1j
            * (
                0.7 * np.sin(np.arange(mesh_size, dtype=np.float64))
                + 0.3 * np.cos(3.0 * np.arange(mesh_size, dtype=np.float64))
            )
        )
        transformed = states * phases[:, None]
        transported_a, holonomy_a = self._parallel_transport(states)
        transported_b, holonomy_b = self._parallel_transport(transformed)
        overlap = np.vdot(transported_a[0], transported_b[0])
        transported_b *= np.exp(-1j * np.angle(overlap))
        frame_defect = float(
            np.max(np.linalg.norm(transported_a - transported_b, axis=1))
        )
        projector_defect = float(
            np.max(
                [
                    np.linalg.norm(
                        np.outer(state, state.conj())
                        - np.outer(changed, changed.conj()),
                        ord="fro",
                    )
                    for state, changed in zip(states, transformed, strict=True)
                ]
            )
        )
        return {
            "potential_strength": strength,
            "mesh_size": mesh_size,
            "random_phase_projector_maximum_frobenius_defect": projector_defect,
            "parallel_transport_frame_maximum_aligned_defect": frame_defect,
            "closure_holonomy_difference_modulo_2pi": float(
                abs(np.angle(np.exp(1j * (holonomy_a - holonomy_b))))
            ),
        }

    def _route_stress(self, stress: StressInput) -> dict[str, JsonValue]:
        strength = stress.route_stress_potential_strength
        mesh_size = stress.route_stress_mesh_size
        hopping_range = stress.route_stress_hopping_range_cells
        momenta, all_energies, _ = self._bands_mesh(
            self._cosine_shape(strength),
            stress.plane_wave_cutoffs[-1],
            mesh_size,
            1,
        )
        energies = all_energies[:, 0]
        representatives = np.arange(-mesh_size // 2, mesh_size // 2)
        hoppings = (
            np.exp(-1j * np.outer(representatives * self._PERIOD, momenta))
            @ energies
            / mesh_size
        )
        retained = np.abs(representatives) <= hopping_range
        retained_representatives = representatives[retained]
        mediated = hoppings[retained]
        design = np.exp(
            1j * np.outer(momenta, retained_representatives * self._PERIOD)
        )
        uniform = np.linalg.lstsq(design, energies, rcond=None)[0]
        weights = 1.0 + 4.0 * np.exp(-np.square(momenta / 0.15))
        weighted = np.linalg.lstsq(
            np.sqrt(weights)[:, None] * design,
            np.sqrt(weights) * energies,
            rcond=None,
        )[0]
        training = np.abs(momenta) <= 0.3
        incomplete = np.linalg.lstsq(
            design[training], energies[training], rcond=None
        )[0]
        comparison_momenta = np.linspace(-0.5, 0.5, 257)
        comparison_design = np.exp(
            1j
            * np.outer(
                comparison_momenta,
                retained_representatives * self._PERIOD,
            )
        )
        return {
            "potential_strength": strength,
            "mesh_size": mesh_size,
            "hopping_range_cells": hopping_range,
            "uniform_complete_coefficient_defect": float(
                np.linalg.norm(uniform - mediated)
            ),
            "nonuniform_weight_coefficient_defect": float(
                np.linalg.norm(weighted - mediated)
            ),
            "incomplete_training_coefficient_defect": float(
                np.linalg.norm(incomplete - mediated)
            ),
            "nonuniform_weight_comparison_l2_defect": float(
                np.linalg.norm(comparison_design @ (weighted - mediated))
            ),
            "incomplete_training_comparison_l2_defect": float(
                np.linalg.norm(comparison_design @ (incomplete - mediated))
            ),
        }

    @staticmethod
    def _cosine_shape(strength: float) -> PotentialShape:
        return PotentialShape(
            identifier="amplitude_sweep",
            constant=0.0,
            cosine_coefficients=(strength,),
            sine_coefficients=(0.0,),
        )

    def _pw_eigensystem(
        self, momentum: float, strength: float, cutoff: int
    ) -> tuple[RealVector, ComplexMatrix]:
        return self._shape_pw_eigensystem(
            momentum, self._cosine_shape(strength), cutoff
        )

    @staticmethod
    def _shape_pw_eigensystem(
        momentum: float, shape: PotentialShape, cutoff: int
    ) -> tuple[RealVector, ComplexMatrix]:
        indices = np.arange(-cutoff, cutoff + 1, dtype=np.float64)
        dimension = 2 * cutoff + 1
        matrix = np.diag(
            np.square(momentum + indices) + shape.constant
        ).astype(np.complex128)
        for harmonic, (cosine, sine) in enumerate(
            zip(
                shape.cosine_coefficients,
                shape.sine_coefficients,
                strict=True,
            ),
            start=1,
        ):
            diagonal_size = dimension - harmonic
            matrix += np.diag(
                np.full(diagonal_size, 0.5 * (cosine + 1j * sine)),
                harmonic,
            )
            matrix += np.diag(
                np.full(diagonal_size, 0.5 * (cosine - 1j * sine)),
                -harmonic,
            )
        return np.linalg.eigh(matrix)

    def _bands_mesh(
        self,
        shape: PotentialShape,
        cutoff: int,
        mesh_size: int,
        band_count: int,
    ) -> tuple[RealVector, npt.NDArray[np.float64], npt.NDArray[np.complex128]]:
        momenta = -0.5 + np.arange(mesh_size, dtype=np.float64) / mesh_size
        energies = np.empty((mesh_size, band_count), dtype=np.float64)
        states = np.empty(
            (mesh_size, band_count, 2 * cutoff + 1), dtype=np.complex128
        )
        for index, momentum in enumerate(momenta):
            values, vectors = self._shape_pw_eigensystem(momentum, shape, cutoff)
            energies[index] = values[:band_count]
            states[index] = vectors[:, :band_count].T
        return momenta, energies, states

    @staticmethod
    def _minimum_band_gaps(energies: npt.NDArray[np.float64]) -> RealVector:
        band_count = energies.shape[1]
        gaps = np.empty(band_count, dtype=np.float64)
        for band_index in range(band_count):
            candidates: list[float] = []
            if band_index > 0:
                candidates.append(
                    float(np.min(energies[:, band_index] - energies[:, band_index - 1]))
                )
            if band_index + 1 < band_count:
                candidates.append(
                    float(np.min(energies[:, band_index + 1] - energies[:, band_index]))
                )
            gaps[band_index] = min(candidates)
        return gaps

    @staticmethod
    def _minimum_sewn_overlap(states: ComplexMatrix) -> float:
        values = [
            abs(np.vdot(states[index], states[index + 1]))
            for index in range(states.shape[0] - 1)
        ]
        sewn_first = np.zeros_like(states[0])
        sewn_first[:-1] = states[0][1:]
        values.append(abs(np.vdot(states[-1], sewn_first)))
        return float(min(values))

    @staticmethod
    def _parallel_transport(states_input: ComplexMatrix) -> tuple[ComplexMatrix, float]:
        states = states_input.copy()
        for index in range(states.shape[0] - 1):
            overlap = np.vdot(states[index], states[index + 1])
            if abs(overlap) <= 1.0e-14:
                raise ValueError("parallel transport failed on a vanishing overlap")
            states[index + 1] *= np.exp(-1j * np.angle(overlap))
        sewn_first = np.zeros_like(states[0])
        sewn_first[:-1] = states[0][1:]
        closure = np.vdot(states[-1], sewn_first)
        if abs(closure) <= 1.0e-14:
            raise ValueError("parallel transport closure failed")
        holonomy = float(np.angle(closure))
        states *= np.exp(
            1j
            * holonomy
            * np.arange(states.shape[0], dtype=np.float64)[:, None]
            / states.shape[0]
        )
        return states, holonomy

    @classmethod
    def _fd_energies(
        cls, momentum: float, shape: PotentialShape, points: int, bands: int
    ) -> RealVector:
        spacing = cls._PERIOD / points
        kinetic = 1.0 / (spacing * spacing)
        coordinates = spacing * np.arange(points, dtype=np.float64)
        potential = np.full(points, shape.constant, dtype=np.float64)
        for harmonic, (cosine, sine) in enumerate(
            zip(
                shape.cosine_coefficients,
                shape.sine_coefficients,
                strict=True,
            ),
            start=1,
        ):
            potential += cosine * np.cos(harmonic * coordinates)
            potential += sine * np.sin(harmonic * coordinates)
        matrix = np.diag(2.0 * kinetic + potential).astype(np.complex128)
        off_diagonal = np.full(points - 1, -kinetic)
        matrix += np.diag(off_diagonal, 1) + np.diag(off_diagonal, -1)
        matrix[0, -1] = -kinetic * np.exp(-1j * momentum * cls._PERIOD)
        matrix[-1, 0] = np.conjugate(matrix[0, -1])
        return cast(
            RealVector,
            eigh(
                matrix,
                subset_by_index=(0, bands - 1),
                eigvals_only=True,
                check_finite=False,
            ),
        )


class CommandAdapter:
    """Adapt command-line paths to the stress experiment."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--input", type=Path, required=True)
        parser.add_argument("--output", type=Path, required=True)
        args = parser.parse_args(argv)
        input_path = cast(Path, args.input).resolve()
        output_path = cast(Path, args.output).resolve()
        script_path = Path(__file__).resolve()
        stress = StressInputDeserializer().execute(input_path.read_bytes())
        output_path.write_bytes(
            PeriodicReductionStressExperiment().execute(
                stress, input_path, script_path
            )
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
