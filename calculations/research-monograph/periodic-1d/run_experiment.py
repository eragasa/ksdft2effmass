#!/usr/bin/env python3
"""Run the isolated-band slice of the Appendix G periodic reduction exercise."""

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
from scipy.special import mathieu_a, mathieu_b  # type: ignore[import-untyped]

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type RealVector = npt.NDArray[np.float64]
type ComplexVector = npt.NDArray[np.complex128]
type ComplexMatrix = npt.NDArray[np.complex128]


@dataclass(frozen=True, slots=True)
class ExperimentInput:
    """Represent the frozen dimensionless isolated-band experiment."""

    experiment_id: str
    lattice_period: float
    reciprocal_vector: float
    reciprocal_energy: float
    potential_strength: float
    plane_wave_cutoffs: tuple[int, ...]
    plane_wave_reference_cutoff: int
    finite_difference_points: tuple[int, ...]
    parent_sample_momenta: tuple[float, ...]
    compared_band_count: int
    common_low_mode_cutoff: int
    reciprocal_mesh_size: int
    hopping_ranges: tuple[int, ...]
    withheld_mesh_size: int
    weak_potential_strengths: tuple[float, ...]

    def __post_init__(self) -> None:
        if not self.experiment_id:
            raise ValueError("experiment_id must be nonempty")
        positive_reals = (
            self.lattice_period,
            self.reciprocal_vector,
            self.reciprocal_energy,
            self.potential_strength,
        )
        if not all(np.isfinite(value) and value > 0.0 for value in positive_reals):
            raise ValueError("dimensionless scales and potential must be positive")
        if not np.isclose(
            self.lattice_period * self.reciprocal_vector,
            2.0 * np.pi,
            rtol=0.0,
            atol=2.0e-15,
        ):
            raise ValueError("lattice_period*reciprocal_vector must equal 2*pi")
        integer_sequences = (
            self.plane_wave_cutoffs,
            self.finite_difference_points,
            self.hopping_ranges,
        )
        if any(not values for values in integer_sequences):
            raise ValueError("refinement and hopping sequences must be nonempty")
        if tuple(sorted(set(self.plane_wave_cutoffs))) != self.plane_wave_cutoffs:
            raise ValueError("plane_wave_cutoffs must be strictly increasing")
        if tuple(sorted(set(self.finite_difference_points))) != (
            self.finite_difference_points
        ):
            raise ValueError("finite_difference_points must be strictly increasing")
        if tuple(sorted(set(self.hopping_ranges))) != self.hopping_ranges:
            raise ValueError("hopping_ranges must be strictly increasing")
        if any(
            points < 2 or points % 2 == 0 for points in self.finite_difference_points
        ):
            raise ValueError("finite_difference_points must be odd and at least three")
        if self.plane_wave_reference_cutoff <= self.plane_wave_cutoffs[-1]:
            raise ValueError("reference cutoff must exceed every study cutoff")
        if self.compared_band_count < 1:
            raise ValueError("compared_band_count must be positive")
        if self.common_low_mode_cutoff < 1:
            raise ValueError("common_low_mode_cutoff must be positive")
        if self.reciprocal_mesh_size < 2 or self.reciprocal_mesh_size % 2 != 0:
            raise ValueError("reciprocal_mesh_size must be positive and even")
        if self.hopping_ranges[-1] >= self.reciprocal_mesh_size // 2:
            raise ValueError("hopping ranges must be below the Nyquist representative")
        if self.withheld_mesh_size < 3:
            raise ValueError("withheld_mesh_size must be at least three")


class ExperimentInputDeserializer:
    """Deserialize the closed version-1 input record."""

    __slots__ = ()

    def execute(self, payload: bytes) -> ExperimentInput:
        value = cast(JsonValue, json.loads(payload.decode("utf-8")))
        root = self._mapping(value, "input")
        constants = self._mapping(
            root["dimensionless_convention"], "dimensionless_convention"
        )
        if self._integer(root["schema_version"], "schema_version") != 1:
            raise ValueError("unsupported input schema version")
        if root["evidence_status"] != "illustrative numerical experiment":
            raise ValueError("evidence_status must identify an illustrative experiment")
        return ExperimentInput(
            experiment_id=self._string(root["experiment_id"], "experiment_id"),
            lattice_period=self._real(constants["lattice_period"], "lattice_period"),
            reciprocal_vector=self._real(
                constants["reciprocal_vector"], "reciprocal_vector"
            ),
            reciprocal_energy=self._real(
                constants["reciprocal_energy"], "reciprocal_energy"
            ),
            potential_strength=self._real(
                root["potential_strength"], "potential_strength"
            ),
            plane_wave_cutoffs=self._integers(
                root["plane_wave_cutoffs"], "plane_wave_cutoffs"
            ),
            plane_wave_reference_cutoff=self._integer(
                root["plane_wave_reference_cutoff"],
                "plane_wave_reference_cutoff",
            ),
            finite_difference_points=self._integers(
                root["finite_difference_points"], "finite_difference_points"
            ),
            parent_sample_momenta=self._reals(
                root["parent_sample_momenta"], "parent_sample_momenta"
            ),
            compared_band_count=self._integer(
                root["compared_band_count"], "compared_band_count"
            ),
            common_low_mode_cutoff=self._integer(
                root["common_low_mode_cutoff"], "common_low_mode_cutoff"
            ),
            reciprocal_mesh_size=self._integer(
                root["reciprocal_mesh_size"], "reciprocal_mesh_size"
            ),
            hopping_ranges=self._integers(root["hopping_ranges"], "hopping_ranges"),
            withheld_mesh_size=self._integer(
                root["withheld_mesh_size"], "withheld_mesh_size"
            ),
            weak_potential_strengths=self._reals(
                root["weak_potential_strengths"], "weak_potential_strengths"
            ),
        )

    @staticmethod
    def _mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be a JSON object")
        return value

    @staticmethod
    def _string(value: JsonValue, name: str) -> str:
        if not isinstance(value, str) or not value:
            raise TypeError(f"{name} must be a nonempty string")
        return value

    @staticmethod
    def _real(value: JsonValue, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be a JSON number")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    @staticmethod
    def _integer(value: JsonValue, name: str) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be a JSON integer")
        return value

    def _reals(self, value: JsonValue, name: str) -> tuple[float, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return tuple(self._real(item, name) for item in value)

    def _integers(self, value: JsonValue, name: str) -> tuple[int, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return tuple(self._integer(item, name) for item in value)


class PeriodicReductionExperiment:
    """Execute parent verification, localization, and isolated-band reduction."""

    __slots__ = ()

    def execute(
        self, experiment: ExperimentInput, input_path: Path, script_path: Path
    ) -> bytes:
        parent = self._parent_verification(experiment)
        reduction = self._isolated_band_reduction(experiment)
        repository_root = script_path.parents[3]
        payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": experiment.experiment_id,
            "evidence_status": "illustrative numerical experiment",
            "calculation_status": "calculated illustrative result",
            "dimensionless_convention": {
                "lattice_period": experiment.lattice_period,
                "reciprocal_vector": experiment.reciprocal_vector,
                "reciprocal_energy": experiment.reciprocal_energy,
                "brillouin_zone": "-G/2 <= k < G/2",
                "plane_wave_order": "increasing reciprocal index n",
            },
            "parent_representation_verification": parent,
            "isolated_band_reduction": reduction,
            "error_accounting": {
                "parent_representation": (
                    "separate plane-wave-cutoff and finite-difference-grid studies"
                ),
                "reciprocal_sampling": (
                    "fixed 64-point transform mesh and independent 257-point "
                    "withheld mesh"
                ),
                "retained_subspace": "lowest isolated band only in this slice",
                "gauge_localization": (
                    "parallel transport, closure holonomy, map overlaps, and "
                    "profile moments"
                ),
                "hopping_truncation": (
                    "reported separately for each retained real-space range"
                ),
                "fit_route": (
                    "direct and Fourier-mediated coefficients compared on the "
                    "same complete uniform mesh"
                ),
                "observable_extraction": (
                    "bandwidth, zone-boundary gap, and zone-center curvature"
                ),
            },
            "provenance": {
                "input_path": input_path.relative_to(repository_root).as_posix(),
                "input_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
                "script_path": script_path.relative_to(repository_root).as_posix(),
                "script_sha256": hashlib.sha256(script_path.read_bytes()).hexdigest(),
                "python_version": platform.python_version(),
                "numpy_version": np.__version__,
                "scipy_algorithms": (
                    "scipy.linalg.eigh and scipy.special Mathieu values"
                ),
                "floating_point": "IEEE-754 binary64",
            },
            "limitations": [
                (
                    "This slice treats one isolated band and does not complete the "
                    "composite-band gauge study."
                ),
                (
                    "Wannier90 was not executed; direct parallel transport is the "
                    "only localization route calculated here."
                ),
                (
                    "Finite-grid and plane-wave agreement is numerical verification "
                    "of the cosine model, not material validation."
                ),
                (
                    "The tight-binding hierarchy approximates the represented band "
                    "dispersion, not the scalar cosine potential."
                ),
            ],
        }
        return (
            json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
        ).encode("utf-8")

    def _parent_verification(self, experiment: ExperimentInput) -> dict[str, JsonValue]:
        momenta = np.asarray(experiment.parent_sample_momenta, dtype=np.float64)
        reference = np.asarray(
            [
                self._pw_eigensystem(
                    momentum,
                    experiment.potential_strength,
                    experiment.plane_wave_reference_cutoff,
                )[0][: experiment.compared_band_count]
                for momentum in momenta
            ]
        )
        pw_records: list[JsonValue] = []
        for cutoff in experiment.plane_wave_cutoffs:
            energies = np.asarray(
                [
                    self._pw_eigensystem(
                        momentum, experiment.potential_strength, cutoff
                    )[0][: experiment.compared_band_count]
                    for momentum in momenta
                ]
            )
            pw_records.append(
                {
                    "cutoff": cutoff,
                    "maximum_first_bands_absolute_error": float(
                        np.max(np.abs(energies - reference))
                    ),
                }
            )
        fd_records: list[JsonValue] = []
        low_mode_records: list[JsonValue] = []
        for points in experiment.finite_difference_points:
            energies = np.asarray(
                [
                    self._fd_energies(
                        momentum,
                        experiment.potential_strength,
                        points,
                        experiment.compared_band_count,
                        experiment.lattice_period,
                    )
                    for momentum in momenta
                ]
            )
            fd_records.append(
                {
                    "interior_cell_points": points,
                    "grid_spacing_over_period": 1.0 / points,
                    "maximum_first_bands_absolute_error": float(
                        np.max(np.abs(energies - reference))
                    ),
                }
            )
            low_mode_records.append(
                {
                    "interior_cell_points": points,
                    "low_mode_cutoff": experiment.common_low_mode_cutoff,
                    "maximum_low_mode_operator_frobenius_error": max(
                        self._low_mode_operator_error(
                            momentum,
                            experiment.potential_strength,
                            points,
                            experiment.common_low_mode_cutoff,
                            experiment.lattice_period,
                        )
                        for momentum in momenta
                    ),
                }
            )
        symmetry_mesh = np.linspace(-0.5, 0.5, 41)
        positive = np.asarray(
            [
                self._pw_eigensystem(
                    momentum,
                    experiment.potential_strength,
                    experiment.plane_wave_cutoffs[-1],
                )[0][: experiment.compared_band_count]
                for momentum in symmetry_mesh
            ]
        )
        reflected = np.asarray(
            [
                self._pw_eigensystem(
                    -momentum,
                    experiment.potential_strength,
                    experiment.plane_wave_cutoffs[-1],
                )[0][: experiment.compared_band_count]
                for momentum in symmetry_mesh
            ]
        )
        negative = np.asarray(
            [
                self._pw_eigensystem(
                    momentum,
                    -experiment.potential_strength,
                    experiment.plane_wave_cutoffs[-1],
                )[0][: experiment.compared_band_count]
                for momentum in symmetry_mesh
            ]
        )
        weak_gap_records: list[JsonValue] = []
        for strength in experiment.weak_potential_strengths:
            energies = self._pw_eigensystem(
                0.5, strength, experiment.plane_wave_reference_cutoff
            )[0]
            gap = float(energies[1] - energies[0])
            weak_gap_records.append(
                {
                    "potential_strength": strength,
                    "zone_boundary_gap": gap,
                    "leading_perturbative_gap": strength,
                    "relative_deviation_from_leading_gap": abs(gap - strength)
                    / strength,
                }
            )
        q = 2.0 * experiment.potential_strength
        zone_center_reference = float(mathieu_a(0, q) / 4.0)
        boundary_references = sorted(
            (float(mathieu_a(1, q) / 4.0), float(mathieu_b(1, q) / 4.0))
        )
        return {
            "plane_wave_cutoff_study": pw_records,
            "finite_difference_grid_study": fd_records,
            "common_low_mode_operator_study": low_mode_records,
            "symmetry_residuals": {
                "inversion_maximum_absolute_energy": float(
                    np.max(np.abs(positive - reflected))
                ),
                "potential_sign_translation_maximum_absolute_energy": float(
                    np.max(np.abs(positive - negative))
                ),
            },
            "weak_potential_gap_study": weak_gap_records,
            "mathieu_references": {
                "q_convention": "q=2*V0/E_G and E/E_G=A/4",
                "zone_center_lowest": zone_center_reference,
                "zone_boundary_lowest_two": cast(list[JsonValue], boundary_references),
                "plane_wave_zone_center_absolute_error": abs(
                    float(
                        self._pw_eigensystem(
                            0.0,
                            experiment.potential_strength,
                            experiment.plane_wave_reference_cutoff,
                        )[0][0]
                    )
                    - zone_center_reference
                ),
                "plane_wave_zone_boundary_maximum_absolute_error": float(
                    np.max(
                        np.abs(
                            self._pw_eigensystem(
                                0.5,
                                experiment.potential_strength,
                                experiment.plane_wave_reference_cutoff,
                            )[0][:2]
                            - np.asarray(boundary_references)
                        )
                    )
                ),
            },
        }

    def _isolated_band_reduction(
        self, experiment: ExperimentInput
    ) -> dict[str, JsonValue]:
        mesh_size = experiment.reciprocal_mesh_size
        momenta = -0.5 + np.arange(mesh_size, dtype=np.float64) / mesh_size
        cutoff = experiment.plane_wave_cutoffs[-1]
        energies = np.empty(mesh_size, dtype=np.float64)
        states = np.empty((mesh_size, 2 * cutoff + 1), dtype=np.complex128)
        for index, momentum in enumerate(momenta):
            values, vectors = self._pw_eigensystem(
                momentum, experiment.potential_strength, cutoff
            )
            energies[index] = values[0]
            states[index] = vectors[:, 0]
        gauge_states, overlap_magnitudes, holonomy = self._parallel_transport(states)
        localization = self._localization_diagnostics(
            gauge_states, momenta, experiment.lattice_period
        )
        representatives = np.arange(-mesh_size // 2, mesh_size // 2, dtype=np.int64)
        phase = np.exp(
            -1j
            * np.outer(
                representatives * experiment.lattice_period,
                momenta,
            )
        )
        hoppings = phase @ energies / mesh_size
        reconstruction = (
            np.exp(
                1j
                * np.outer(
                    momenta,
                    representatives * experiment.lattice_period,
                )
            )
            @ hoppings
        )
        withheld_momenta = np.linspace(-0.5, 0.5, experiment.withheld_mesh_size)
        withheld_parent = np.asarray(
            [
                self._pw_eigensystem(momentum, experiment.potential_strength, cutoff)[
                    0
                ][0]
                for momentum in withheld_momenta
            ]
        )
        range_records: list[JsonValue] = []
        for hopping_range in experiment.hopping_ranges:
            retained = np.abs(representatives) <= hopping_range
            mediated_coefficients = hoppings[retained]
            retained_representatives = representatives[retained]
            training_design = np.exp(
                1j
                * np.outer(
                    momenta,
                    retained_representatives * experiment.lattice_period,
                )
            )
            mediated_training = training_design @ mediated_coefficients
            direct_coefficients = np.linalg.lstsq(
                training_design, energies, rcond=None
            )[0]
            direct_training = training_design @ direct_coefficients
            withheld_design = np.exp(
                1j
                * np.outer(
                    withheld_momenta,
                    retained_representatives * experiment.lattice_period,
                )
            )
            mediated_withheld = withheld_design @ mediated_coefficients
            omitted_norm = float(np.linalg.norm(hoppings[~retained]))
            training_residual = energies - mediated_training.real
            parseval_left = float(np.sum(np.square(training_residual)))
            parseval_right = float(mesh_size * omitted_norm * omitted_norm)
            curvature = float(
                -np.sum(
                    np.square(retained_representatives * experiment.lattice_period)
                    * mediated_coefficients
                ).real
            )
            range_records.append(
                {
                    "hopping_range_cells": hopping_range,
                    "retained_coefficient_count": int(np.count_nonzero(retained)),
                    "omitted_hopping_l2_norm": omitted_norm,
                    "training_root_mean_square_error": float(
                        np.sqrt(np.mean(np.square(training_residual)))
                    ),
                    "withheld_root_mean_square_error": float(
                        np.sqrt(
                            np.mean(np.square(withheld_parent - mediated_withheld.real))
                        )
                    ),
                    "training_maximum_absolute_error": float(
                        np.max(np.abs(training_residual))
                    ),
                    "withheld_maximum_absolute_error": float(
                        np.max(np.abs(withheld_parent - mediated_withheld.real))
                    ),
                    "parseval_absolute_residual": abs(parseval_left - parseval_right),
                    "direct_mediated_coefficient_l2_defect": float(
                        np.linalg.norm(direct_coefficients - mediated_coefficients)
                    ),
                    "direct_mediated_training_l2_defect": float(
                        np.linalg.norm(direct_training - mediated_training)
                    ),
                    "bandwidth_error": abs(
                        float(np.ptp(mediated_withheld.real))
                        - float(np.ptp(withheld_parent))
                    ),
                    "zone_center_curvature": curvature,
                }
            )
        dk = 1.0e-3
        center_values = np.asarray(
            [
                self._pw_eigensystem(momentum, experiment.potential_strength, cutoff)[
                    0
                ][0]
                for momentum in (-dk, 0.0, dk)
            ]
        )
        parent_curvature = float(
            (center_values[0] - 2.0 * center_values[1] + center_values[2]) / (dk * dk)
        )
        boundary_values = self._pw_eigensystem(
            0.5, experiment.potential_strength, cutoff
        )[0]
        return {
            "reciprocal_mesh": cast(list[JsonValue], momenta.tolist()),
            "lowest_band_energies": cast(list[JsonValue], energies.tolist()),
            "neighbor_overlap_minimum_magnitude": float(np.min(overlap_magnitudes)),
            "neighbor_overlap_maximum_magnitude": float(np.max(overlap_magnitudes)),
            "closure_holonomy_phase": holonomy,
            "wannier_localization": localization,
            "hopping_representatives_cells": cast(
                list[JsonValue], representatives.tolist()
            ),
            "hopping_coefficients": self._complex_vector(cast(ComplexVector, hoppings)),
            "full_mesh_reconstruction_maximum_absolute_error": float(
                np.max(np.abs(reconstruction.real - energies))
            ),
            "full_mesh_reconstruction_maximum_imaginary": float(
                np.max(np.abs(reconstruction.imag))
            ),
            "hopping_maximum_imaginary": float(np.max(np.abs(hoppings.imag))),
            "parent_observables": {
                "bandwidth": float(np.ptp(withheld_parent)),
                "zone_boundary_gap": float(boundary_values[1] - boundary_values[0]),
                "zone_center_curvature": parent_curvature,
            },
            "hopping_range_study": range_records,
        }

    def _localization_diagnostics(
        self,
        states: ComplexMatrix,
        momenta: RealVector,
        lattice_period: float,
    ) -> dict[str, JsonValue]:
        mesh_size, basis_size = states.shape
        cutoff = (basis_size - 1) // 2
        samples_per_cell = 32
        points = mesh_size * samples_per_cell
        coordinates = np.linspace(
            -0.5 * mesh_size * lattice_period,
            0.5 * mesh_size * lattice_period,
            points,
            endpoint=False,
        )
        cell_coordinates = np.mod(coordinates, lattice_period)
        reciprocal_indices = np.arange(-cutoff, cutoff + 1, dtype=np.float64)
        cell_basis = np.exp(
            1j * np.outer(cell_coordinates, reciprocal_indices)
        ) / np.sqrt(lattice_period)
        periodic_parts = cell_basis @ states.T
        bloch_states = periodic_parts * np.exp(1j * np.outer(coordinates, momenta))
        wannier = np.sum(bloch_states, axis=1) / mesh_size
        spacing = coordinates[1] - coordinates[0]
        norm = float(spacing * np.sum(np.square(np.abs(wannier))))
        density = np.square(np.abs(wannier)) / norm
        center = float(spacing * np.sum(coordinates * density))
        spread = float(spacing * np.sum(np.square(coordinates - center) * density))
        canonical_density = np.asarray(density, dtype="<f8", order="C")
        return {
            "profile_definition": (
                "Born-von Karman inverse Bloch transform of the periodic "
                "parallel-transport gauge"
            ),
            "profile_sample_count": points,
            "profile_density_content_sha256": hashlib.sha256(
                canonical_density.tobytes(order="C")
            ).hexdigest(),
            "profile_density_content_encoding": (
                "IEEE-754 binary64 little-endian row-major"
            ),
            "quadrature_norm": norm,
            "center_over_period": center / lattice_period,
            "spread_over_period_squared": spread / (lattice_period * lattice_period),
        }

    @staticmethod
    def _parallel_transport(
        input_states: ComplexMatrix,
    ) -> tuple[ComplexMatrix, RealVector, float]:
        states = input_states.copy()
        mesh_size = states.shape[0]
        overlap_magnitudes = np.empty(mesh_size, dtype=np.float64)
        for index in range(mesh_size - 1):
            overlap = np.vdot(states[index], states[index + 1])
            if abs(overlap) <= 1.0e-12:
                raise ValueError(
                    "neighbor overlap is too small for isolated-band transport"
                )
            states[index + 1] *= np.exp(-1j * np.angle(overlap))
            overlap_magnitudes[index] = abs(overlap)
        sewn_first = np.zeros_like(states[0])
        sewn_first[:-1] = states[0][1:]
        closure = np.vdot(states[-1], sewn_first)
        if abs(closure) <= 1.0e-12:
            raise ValueError("closure overlap is too small")
        overlap_magnitudes[-1] = abs(closure)
        holonomy = float(np.angle(closure))
        phases = np.exp(
            1j * holonomy * np.arange(mesh_size, dtype=np.float64) / mesh_size
        )
        states *= phases[:, None]
        return states, overlap_magnitudes, holonomy

    @staticmethod
    def _pw_eigensystem(
        momentum: float, potential_strength: float, cutoff: int
    ) -> tuple[RealVector, ComplexMatrix]:
        indices = np.arange(-cutoff, cutoff + 1, dtype=np.float64)
        matrix = np.diag(np.square(momentum + indices)).astype(np.complex128)
        coupling = 0.5 * potential_strength
        matrix += np.diag(np.full(2 * cutoff, coupling), 1)
        matrix += np.diag(np.full(2 * cutoff, coupling), -1)
        values, vectors = np.linalg.eigh(matrix)
        return values, vectors

    @staticmethod
    def _fd_energies(
        momentum: float,
        potential_strength: float,
        points: int,
        band_count: int,
        lattice_period: float,
    ) -> RealVector:
        spacing = lattice_period / points
        kinetic = 1.0 / (spacing * spacing)
        coordinates = spacing * np.arange(points, dtype=np.float64)
        diagonal = 2.0 * kinetic + potential_strength * np.cos(coordinates)
        matrix = np.diag(diagonal).astype(np.complex128)
        off_diagonal = np.full(points - 1, -kinetic)
        matrix += np.diag(off_diagonal, 1) + np.diag(off_diagonal, -1)
        matrix[0, -1] = -kinetic * np.exp(-1j * momentum * lattice_period)
        matrix[-1, 0] = np.conjugate(matrix[0, -1])
        return cast(
            RealVector,
            eigh(
                matrix,
                subset_by_index=(0, band_count - 1),
                eigvals_only=True,
                check_finite=False,
            ),
        )

    @staticmethod
    def _low_mode_operator_error(
        momentum: float,
        potential_strength: float,
        points: int,
        low_mode_cutoff: int,
        lattice_period: float,
    ) -> float:
        spacing = lattice_period / points
        kinetic = 1.0 / (spacing * spacing)
        coordinates = spacing * np.arange(points, dtype=np.float64)
        diagonal = 2.0 * kinetic + potential_strength * np.cos(coordinates)
        matrix = np.diag(diagonal).astype(np.complex128)
        off_diagonal = np.full(points - 1, -kinetic)
        matrix += np.diag(off_diagonal, 1) + np.diag(off_diagonal, -1)
        matrix[0, -1] = -kinetic * np.exp(-1j * momentum * lattice_period)
        matrix[-1, 0] = np.conjugate(matrix[0, -1])
        indices = np.arange(-low_mode_cutoff, low_mode_cutoff + 1)
        transform = np.exp(
            1j
            * np.outer(
                coordinates,
                momentum + indices.astype(np.float64),
            )
        ) / np.sqrt(points)
        transported = transform.conj().T @ matrix @ transform
        pw_indices = indices.astype(np.float64)
        plane_wave = np.diag(np.square(momentum + pw_indices)).astype(np.complex128)
        coupling = 0.5 * potential_strength
        plane_wave += np.diag(np.full(2 * low_mode_cutoff, coupling), 1)
        plane_wave += np.diag(np.full(2 * low_mode_cutoff, coupling), -1)
        return float(np.linalg.norm(transported - plane_wave, ord="fro"))

    @staticmethod
    def _complex_vector(values: ComplexVector) -> list[JsonValue]:
        return [
            cast(list[JsonValue], [float(value.real), float(value.imag)])
            for value in values
        ]


class CommandAdapter:
    """Adapt command-line paths to the owned experiment."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--input", type=Path, required=True)
        parser.add_argument("--output", type=Path, required=True)
        args = parser.parse_args(argv)
        input_path = cast(Path, args.input).resolve()
        output_path = cast(Path, args.output).resolve()
        script_path = Path(__file__).resolve()
        experiment = ExperimentInputDeserializer().execute(input_path.read_bytes())
        output_path.write_bytes(
            PeriodicReductionExperiment().execute(experiment, input_path, script_path)
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
