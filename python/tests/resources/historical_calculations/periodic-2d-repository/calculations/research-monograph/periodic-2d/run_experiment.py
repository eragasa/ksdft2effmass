#!/usr/bin/env python3
"""Run the controlled separable-to-coupled two-dimensional reduction exercise."""

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
type RealMatrix = npt.NDArray[np.float64]
type ComplexVector = npt.NDArray[np.complex128]
type ComplexMatrix = npt.NDArray[np.complex128]


@dataclass(frozen=True, slots=True)
class ExperimentInput:
    """Frozen dimensionless controls for the two-dimensional experiment."""

    experiment_id: str
    lattice_period: float
    reciprocal_vector: float
    reciprocal_energy: float
    lambda_x: float
    lambda_y: float
    anisotropic_lambda_x: float
    anisotropic_lambda_y: float
    anisotropic_lambda_xy: float
    coupling_sequence: tuple[float, ...]
    plane_wave_cutoffs: tuple[int, ...]
    plane_wave_reference_cutoff: int
    finite_difference_points: tuple[int, ...]
    parent_sample_momenta: tuple[tuple[float, float], ...]
    parent_coupling: float
    compared_band_count: int
    common_low_mode_cutoff: int
    reciprocal_mesh_size: int
    withheld_mesh_size: int
    shell_squared_radii: tuple[int, ...]
    effective_mass_step: float
    minimum_neighbor_overlap: float
    chern_integer_defect: float

    def __post_init__(self) -> None:
        if not self.experiment_id:
            raise ValueError("experiment_id must be nonempty")
        positive = (
            self.lattice_period,
            self.reciprocal_vector,
            self.reciprocal_energy,
            self.lambda_x,
            self.lambda_y,
            self.anisotropic_lambda_x,
            self.anisotropic_lambda_y,
            self.effective_mass_step,
            self.minimum_neighbor_overlap,
            self.chern_integer_defect,
        )
        if not all(np.isfinite(value) and value > 0.0 for value in positive):
            raise ValueError("positive controls must be finite and positive")
        if not np.isclose(
            self.lattice_period * self.reciprocal_vector,
            2.0 * np.pi,
            rtol=0.0,
            atol=2.0e-15,
        ):
            raise ValueError("lattice_period*reciprocal_vector must equal 2*pi")
        for values, name in (
            (self.coupling_sequence, "coupling_sequence"),
            (self.plane_wave_cutoffs, "plane_wave_cutoffs"),
            (self.finite_difference_points, "finite_difference_points"),
            (self.shell_squared_radii, "shell_squared_radii"),
        ):
            if not values or tuple(sorted(set(values))) != values:
                raise ValueError(f"{name} must be nonempty and strictly increasing")
        if self.coupling_sequence[0] != 0.0:
            raise ValueError("coupling_sequence must begin at the separable limit")
        if self.plane_wave_reference_cutoff <= self.plane_wave_cutoffs[-1]:
            raise ValueError("reference cutoff must exceed study cutoffs")
        if any(value < 1 for value in self.plane_wave_cutoffs):
            raise ValueError("plane-wave cutoffs must be positive")
        if any(value < 5 or value % 2 == 0 for value in self.finite_difference_points):
            raise ValueError("finite-difference sizes must be odd and at least five")
        if self.compared_band_count < 1:
            raise ValueError("compared_band_count must be positive")
        if self.common_low_mode_cutoff < 1:
            raise ValueError("common_low_mode_cutoff must be positive")
        if self.reciprocal_mesh_size < 5 or self.reciprocal_mesh_size % 2 == 0:
            raise ValueError("reciprocal mesh must be odd and at least five")
        if self.withheld_mesh_size <= self.reciprocal_mesh_size:
            raise ValueError("withheld mesh must be finer than the transform mesh")
        maximum_rep = self.reciprocal_mesh_size // 2
        if self.shell_squared_radii[-1] != 2 * maximum_rep * maximum_rep:
            raise ValueError("final shell must contain every mesh representative")
        if not 0.0 < self.minimum_neighbor_overlap < 1.0:
            raise ValueError("minimum_neighbor_overlap must lie in (0,1)")


class ExperimentInputDeserializer:
    """Deserialize the closed version-1 experiment input."""

    __slots__ = ()

    def execute(self, payload: bytes) -> ExperimentInput:
        value = cast(JsonValue, json.loads(payload.decode("utf-8")))
        root = self._mapping(value, "input")
        if self._integer(root["schema_version"], "schema_version") != 1:
            raise ValueError("unsupported input schema version")
        if root["evidence_status"] != "illustrative numerical experiment":
            raise ValueError("unexpected evidence status")
        convention = self._mapping(
            root["dimensionless_convention"], "dimensionless_convention"
        )
        isotropic = self._mapping(root["isotropic_potential"], "isotropic_potential")
        anisotropic = self._mapping(root["anisotropic_control"], "anisotropic_control")
        topology = self._mapping(root["topology_tolerances"], "topology_tolerances")
        momentum_value = root["parent_sample_momenta"]
        if not isinstance(momentum_value, list):
            raise TypeError("parent_sample_momenta must be an array")
        momenta: list[tuple[float, float]] = []
        for item in momentum_value:
            if not isinstance(item, list) or len(item) != 2:
                raise TypeError("each parent momentum must have two entries")
            momenta.append((self._real(item[0], "kx"), self._real(item[1], "ky")))
        return ExperimentInput(
            experiment_id=self._string(root["experiment_id"], "experiment_id"),
            lattice_period=self._real(convention["lattice_period"], "lattice_period"),
            reciprocal_vector=self._real(
                convention["reciprocal_vector"], "reciprocal_vector"
            ),
            reciprocal_energy=self._real(
                convention["reciprocal_energy"], "reciprocal_energy"
            ),
            lambda_x=self._real(isotropic["lambda_x"], "lambda_x"),
            lambda_y=self._real(isotropic["lambda_y"], "lambda_y"),
            anisotropic_lambda_x=self._real(
                anisotropic["lambda_x"], "anisotropic lambda_x"
            ),
            anisotropic_lambda_y=self._real(
                anisotropic["lambda_y"], "anisotropic lambda_y"
            ),
            anisotropic_lambda_xy=self._real(
                anisotropic["lambda_xy"], "anisotropic lambda_xy"
            ),
            coupling_sequence=self._reals(
                root["coupling_sequence"], "coupling_sequence"
            ),
            plane_wave_cutoffs=self._integers(
                root["plane_wave_cutoffs"], "plane_wave_cutoffs"
            ),
            plane_wave_reference_cutoff=self._integer(
                root["plane_wave_reference_cutoff"], "plane_wave_reference_cutoff"
            ),
            finite_difference_points=self._integers(
                root["finite_difference_points"], "finite_difference_points"
            ),
            parent_sample_momenta=tuple(momenta),
            parent_coupling=self._real(root["parent_coupling"], "parent_coupling"),
            compared_band_count=self._integer(
                root["compared_band_count"], "compared_band_count"
            ),
            common_low_mode_cutoff=self._integer(
                root["common_low_mode_cutoff"], "common_low_mode_cutoff"
            ),
            reciprocal_mesh_size=self._integer(
                root["reciprocal_mesh_size"], "reciprocal_mesh_size"
            ),
            withheld_mesh_size=self._integer(
                root["withheld_mesh_size"], "withheld_mesh_size"
            ),
            shell_squared_radii=self._integers(
                root["hopping_shell_squared_radii"],
                "hopping_shell_squared_radii",
            ),
            effective_mass_step=self._real(
                root["effective_mass_step"], "effective_mass_step"
            ),
            minimum_neighbor_overlap=self._real(
                topology["minimum_neighbor_overlap"], "minimum_neighbor_overlap"
            ),
            chern_integer_defect=self._real(
                topology["chern_integer_defect"], "chern_integer_defect"
            ),
        )

    @staticmethod
    def _mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be an object")
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
            raise TypeError(f"{name} must be an array")
        return tuple(self._real(item, name) for item in value)

    def _integers(self, value: JsonValue, name: str) -> tuple[int, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be an array")
        return tuple(self._integer(item, name) for item in value)


class Periodic2DExperiment:
    """Execute represented-parent, subspace, topology, and reduction checks."""

    __slots__ = ()

    def execute(
        self, experiment: ExperimentInput, input_path: Path, script_path: Path
    ) -> bytes:
        parent = self._parent_verification(experiment)
        separable = self._separable_verification(experiment)
        continuation = [
            self._coupling_case(experiment, coupling)
            for coupling in experiment.coupling_sequence
        ]
        anisotropy = self._anisotropy_control(experiment)
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
                "brillouin_zone": "-G/2 <= k_i < G/2",
                "plane_wave_order": "p outer, q inner, each increasing",
                "finite_difference_order": "x outer, y inner, each increasing",
                "energy_reference": "common dimensionless parent Hamiltonian zero",
                "spin_convention": "spinless scalar",
            },
            "parent_representation_verification": parent,
            "separable_reference": separable,
            "coupling_continuation": continuation,
            "anisotropy_control": anisotropy,
            "error_accounting": {
                "one_dimensional_reference": "exact represented Kronecker identities",
                "plane_wave_cutoff": "independent cutoff sequence against P=5",
                "real_space_grid": "centered second-order Bloch finite differences",
                "reciprocal_mesh": "15x15 transform mesh and 31x31 withheld mesh",
                "degeneracy": "rank-two projector, not individual eigenvector labels",
                "gauge_and_topology": (
                    "sewn neighbor links, Wilson phases, plaquette phases, "
                    "and Chern sum"
                ),
                "hopping_shell": "frozen squared-radius point-group shells",
                "fit_route": (
                    "equal-weight complete-mesh least squares versus mediated "
                    "Fourier truncation"
                ),
                "effective_mass": "fixed centered Hessian stencil",
                "coupling": "lambda_xy varied alone over the frozen sequence",
            },
            "structured_stops": {
                "neighbor_overlap_below_threshold": (
                    "PERIODIC_2D.SUBSPACE_OVERLAP_TOO_SMALL"
                ),
                "chern_not_integer_within_tolerance": (
                    "PERIODIC_2D.CHERN_NOT_QUANTIZED"
                ),
                "represented_operator_metadata_mismatch": (
                    "PERIODIC_2D.REPRESENTATION_MISMATCH"
                ),
            },
            "provenance": {
                "input_path": input_path.relative_to(repository_root).as_posix(),
                "input_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
                "script_path": script_path.relative_to(repository_root).as_posix(),
                "script_sha256": hashlib.sha256(script_path.read_bytes()).hexdigest(),
                "python_version": platform.python_version(),
                "numpy_version": np.__version__,
                "scipy_algorithm": (
                    "scipy.linalg.eigh for finite-difference low spectra"
                ),
                "floating_point": "IEEE-754 binary64",
            },
            "limitations": [
                (
                    "The finite plane-wave and finite-difference representations "
                    "are numerical approximations of the declared synthetic parent."
                ),
                (
                    "Gauge, topology, hopping, and route studies retain only the "
                    "lowest isolated scalar band."
                ),
                (
                    "This direct scalar stage does not invoke Wannier90; external "
                    "localization is evaluated only in the separately authorized "
                    "rank-three extension."
                ),
                (
                    "The real scalar family is topologically trivial by construction "
                    "and does not test a Chern-band obstruction."
                ),
                (
                    "The calculation is numerical verification, not material "
                    "validation, transferability evidence, or uncertainty "
                    "quantification."
                ),
            ],
        }
        return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")

    def _parent_verification(self, experiment: ExperimentInput) -> dict[str, JsonValue]:
        reference = experiment.plane_wave_reference_cutoff
        cutoff_records: list[JsonValue] = []
        for cutoff in experiment.plane_wave_cutoffs:
            maximum = 0.0
            for kx, ky in experiment.parent_sample_momenta:
                expected = self._pw_eigensystem(
                    kx,
                    ky,
                    experiment.lambda_x,
                    experiment.lambda_y,
                    experiment.parent_coupling,
                    reference,
                    vectors=False,
                )[0][: experiment.compared_band_count]
                observed = self._pw_eigensystem(
                    kx,
                    ky,
                    experiment.lambda_x,
                    experiment.lambda_y,
                    experiment.parent_coupling,
                    cutoff,
                    vectors=False,
                )[0][: experiment.compared_band_count]
                maximum = max(maximum, float(np.max(np.abs(observed - expected))))
            cutoff_records.append(
                {
                    "cutoff": cutoff,
                    "represented_dimension": (2 * cutoff + 1) ** 2,
                    "maximum_low_band_absolute_error": maximum,
                }
            )

        fd_records: list[JsonValue] = []
        for points in experiment.finite_difference_points:
            spectral_maximum = 0.0
            operator_maximum = 0.0
            for kx, ky in experiment.parent_sample_momenta:
                reference_values = self._pw_eigensystem(
                    kx,
                    ky,
                    experiment.lambda_x,
                    experiment.lambda_y,
                    experiment.parent_coupling,
                    reference,
                    vectors=False,
                )[0][: experiment.compared_band_count]
                matrix = self._fd_matrix(
                    kx,
                    ky,
                    experiment.lambda_x,
                    experiment.lambda_y,
                    experiment.parent_coupling,
                    points,
                    experiment.lattice_period,
                )
                values = eigh(
                    matrix,
                    subset_by_index=[0, experiment.compared_band_count - 1],
                    eigvals_only=True,
                    check_finite=True,
                    driver="evr",
                )
                spectral_maximum = max(
                    spectral_maximum,
                    float(np.max(np.abs(values - reference_values))),
                )
                transported = self._transport_fd_to_low_modes(
                    matrix,
                    kx,
                    ky,
                    points,
                    experiment.common_low_mode_cutoff,
                    experiment.lattice_period,
                )
                common = self._pw_matrix(
                    kx,
                    ky,
                    experiment.lambda_x,
                    experiment.lambda_y,
                    experiment.parent_coupling,
                    experiment.common_low_mode_cutoff,
                )
                operator_maximum = max(
                    operator_maximum,
                    float(np.linalg.norm(transported - common)),
                )
            fd_records.append(
                {
                    "points_per_direction": points,
                    "represented_dimension": points * points,
                    "maximum_low_band_absolute_error": spectral_maximum,
                    "maximum_common_low_mode_frobenius_error": operator_maximum,
                }
            )
        return {
            "comparison_case": {
                "lambda_x": experiment.lambda_x,
                "lambda_y": experiment.lambda_y,
                "lambda_xy": experiment.parent_coupling,
            },
            "plane_wave_reference_cutoff": reference,
            "plane_wave_cutoff_study": cutoff_records,
            "finite_difference_grid_study": fd_records,
            "comparison_precondition": (
                "finite operators share units, geometry, energy zero, spinless "
                "convention, Bloch momentum, and explicit Fourier alignment before "
                "subtraction"
            ),
        }

    def _separable_verification(
        self, experiment: ExperimentInput
    ) -> dict[str, JsonValue]:
        cutoff = experiment.plane_wave_cutoffs[-1]
        matrix_defect = 0.0
        energy_defect = 0.0
        for kx, ky in experiment.parent_sample_momenta:
            direct = self._pw_matrix(
                kx, ky, experiment.lambda_x, experiment.lambda_y, 0.0, cutoff
            )
            hx = self._pw_1d_matrix(kx, experiment.lambda_x, cutoff)
            hy = self._pw_1d_matrix(ky, experiment.lambda_y, cutoff)
            size = hx.shape[0]
            product = np.kron(hx, np.eye(size)) + np.kron(np.eye(size), hy)
            matrix_defect = max(matrix_defect, float(np.linalg.norm(direct - product)))
            direct_values = np.linalg.eigvalsh(direct)
            x_values = np.linalg.eigvalsh(hx)
            y_values = np.linalg.eigvalsh(hy)
            expected = np.sort((x_values[:, None] + y_values[None, :]).ravel())
            energy_defect = max(
                energy_defect,
                float(np.max(np.abs(direct_values - expected))),
            )

        hx = self._pw_1d_matrix(0.0, experiment.lambda_x, cutoff)
        x_values, x_vectors = np.linalg.eigh(hx)
        direct = self._pw_matrix(
            0.0, 0.0, experiment.lambda_x, experiment.lambda_y, 0.0, cutoff
        )
        values, vectors = np.linalg.eigh(direct)
        target = x_values[0] + x_values[1]
        selected = np.argsort(np.abs(values - target))[:2]
        direct_cluster = vectors[:, selected]
        product_cluster = np.column_stack(
            (
                np.kron(x_vectors[:, 0], x_vectors[:, 1]),
                np.kron(x_vectors[:, 1], x_vectors[:, 0]),
            )
        )
        projector_defect = float(
            np.linalg.norm(
                direct_cluster @ direct_cluster.conj().T
                - product_cluster @ product_cluster.conj().T
            )
        )
        hadamard = np.asarray([[1.0, 1.0], [1.0, -1.0]]) / np.sqrt(2.0)
        rotated = product_cluster @ hadamard
        individual_overlap = np.abs(product_cluster.conj().T @ rotated)
        attacked_projector_defect = float(
            np.linalg.norm(
                product_cluster @ product_cluster.conj().T - rotated @ rotated.conj().T
            )
        )
        return {
            "plane_wave_cutoff": cutoff,
            "maximum_kronecker_sum_matrix_frobenius_defect": matrix_defect,
            "maximum_full_spectrum_product_sum_defect": energy_defect,
            "gamma_degenerate_cluster": {
                "target_energy": float(target),
                "rank": 2,
                "projector_frobenius_defect": projector_defect,
                "controlled_basis_rotation_minimum_individual_overlap": float(
                    np.min(individual_overlap)
                ),
                "controlled_basis_rotation_projector_defect": attacked_projector_defect,
                "interpretation": (
                    "individual vectors are gauge dependent; the complete rank-two "
                    "projector is stable"
                ),
            },
        }

    def _coupling_case(
        self, experiment: ExperimentInput, coupling: float
    ) -> dict[str, JsonValue]:
        cutoff = experiment.plane_wave_cutoffs[-2]
        mesh = self._mesh(experiment.reciprocal_mesh_size)
        size = mesh.size
        energies = np.empty((size, size), dtype=np.float64)
        vectors = np.empty((size, size, (2 * cutoff + 1) ** 2), dtype=np.complex128)
        gap_minimum = np.inf
        separability_maximum = 0.0
        x_energies = {
            float(k): np.linalg.eigvalsh(
                self._pw_1d_matrix(float(k), experiment.lambda_x, cutoff)
            )[0]
            for k in mesh
        }
        y_energies = {
            float(k): np.linalg.eigvalsh(
                self._pw_1d_matrix(float(k), experiment.lambda_y, cutoff)
            )[0]
            for k in mesh
        }
        for ix, kx in enumerate(mesh):
            for iy, ky in enumerate(mesh):
                values, state = self._pw_eigensystem(
                    float(kx),
                    float(ky),
                    experiment.lambda_x,
                    experiment.lambda_y,
                    coupling,
                    cutoff,
                    vectors=True,
                )
                energies[ix, iy] = values[0]
                vectors[ix, iy] = state[:, 0]
                gap_minimum = min(gap_minimum, float(values[1] - values[0]))
                separability_maximum = max(
                    separability_maximum,
                    abs(
                        float(values[0]) - x_energies[float(kx)] - y_energies[float(ky)]
                    ),
                )
        topology = self._topology(vectors, cutoff)
        attacked = vectors.copy()
        for ix in range(size):
            for iy in range(size):
                attacked[ix, iy] *= np.exp(
                    1j * (0.37 * ix + 0.23 * iy + 0.11 * ix * iy)
                )
        attacked_topology = self._topology(attacked, cutoff)
        topology["gauge_attack_chern_difference"] = abs(
            cast(float, topology["chern_number"])
            - cast(float, attacked_topology["chern_number"])
        )
        topology["gauge_attack_maximum_wilson_phase_difference"] = max(
            self._phase_sequence_defect(
                cast(list[JsonValue], topology["wilson_loop_x_phases"]),
                cast(list[JsonValue], attacked_topology["wilson_loop_x_phases"]),
            ),
            self._phase_sequence_defect(
                cast(list[JsonValue], topology["wilson_loop_y_phases"]),
                cast(list[JsonValue], attacked_topology["wilson_loop_y_phases"]),
            ),
        )
        if (
            cast(float, topology["minimum_neighbor_overlap"])
            < experiment.minimum_neighbor_overlap
        ):
            raise RuntimeError("PERIODIC_2D.SUBSPACE_OVERLAP_TOO_SMALL")
        chern = cast(float, topology["chern_number"])
        if abs(chern - round(chern)) > experiment.chern_integer_defect:
            raise RuntimeError("PERIODIC_2D.CHERN_NOT_QUANTIZED")

        hopping_records, hoppings = self._hopping_study(
            experiment, coupling, mesh, energies
        )
        mixed_mask = np.asarray(
            [rx != 0 and ry != 0 for rx, ry in self._representatives(size)]
        )
        hopping_values = np.asarray(list(hoppings.values()))
        mixed_norm = float(np.linalg.norm(hopping_values[mixed_mask]))
        total_nonlocal = float(
            np.linalg.norm(
                np.asarray(
                    [
                        value
                        for (rx, ry), value in hoppings.items()
                        if rx != 0 or ry != 0
                    ]
                )
            )
        )
        mass = self._effective_mass_tensor(
            experiment.lambda_x,
            experiment.lambda_y,
            coupling,
            cutoff,
            experiment.effective_mass_step,
        )
        symmetry = self._symmetry_residuals(mesh, energies, square=True)
        return {
            "lambda_xy": coupling,
            "plane_wave_cutoff": cutoff,
            "reciprocal_mesh": mesh.tolist(),
            "lowest_band_energies": energies.tolist(),
            "minimum_isolation_gap": gap_minimum,
            "maximum_lowest_band_separability_residual": separability_maximum,
            "symmetry_residuals": symmetry,
            "topology_and_gauge": topology,
            "effective_mass": mass,
            "mixed_direction_hopping_l2_norm": mixed_norm,
            "mixed_to_total_nonlocal_hopping_ratio": (
                0.0 if total_nonlocal == 0.0 else mixed_norm / total_nonlocal
            ),
            "hopping_coefficients": [
                {
                    "rx": rx,
                    "ry": ry,
                    "real": float(value.real),
                    "imag": float(value.imag),
                    "magnitude": float(abs(value)),
                }
                for (rx, ry), value in hoppings.items()
            ],
            "shell_study": hopping_records,
        }

    def _anisotropy_control(self, experiment: ExperimentInput) -> dict[str, JsonValue]:
        cutoff = experiment.plane_wave_cutoffs[-2]
        mesh = self._mesh(experiment.reciprocal_mesh_size)
        energies = np.asarray(
            [
                [
                    self._pw_eigensystem(
                        float(kx),
                        float(ky),
                        experiment.anisotropic_lambda_x,
                        experiment.anisotropic_lambda_y,
                        experiment.anisotropic_lambda_xy,
                        cutoff,
                        vectors=False,
                    )[0][0]
                    for ky in mesh
                ]
                for kx in mesh
            ]
        )
        return {
            "lambda_x": experiment.anisotropic_lambda_x,
            "lambda_y": experiment.anisotropic_lambda_y,
            "lambda_xy": experiment.anisotropic_lambda_xy,
            "symmetry_residuals": self._symmetry_residuals(
                mesh, energies, square=False
            ),
            "effective_mass": self._effective_mass_tensor(
                experiment.anisotropic_lambda_x,
                experiment.anisotropic_lambda_y,
                experiment.anisotropic_lambda_xy,
                cutoff,
                experiment.effective_mass_step,
            ),
        }

    def _hopping_study(
        self,
        experiment: ExperimentInput,
        coupling: float,
        mesh: RealVector,
        energies: RealMatrix,
    ) -> tuple[list[JsonValue], dict[tuple[int, int], complex]]:
        reps = self._representatives(mesh.size)
        points = np.asarray([(kx, ky) for kx in mesh for ky in mesh])
        flat_energies = energies.ravel()
        inverse = np.exp(
            -2j
            * np.pi
            * np.asarray(
                [kx * rx + ky * ry for rx, ry in reps for kx, ky in points]
            ).reshape(len(reps), len(points))
        )
        coefficients = inverse @ flat_energies / len(points)
        hoppings = {
            rep: complex(value) for rep, value in zip(reps, coefficients, strict=True)
        }
        full_design = np.exp(
            2j
            * np.pi
            * np.asarray(
                [kx * rx + ky * ry for kx, ky in points for rx, ry in reps]
            ).reshape(len(points), len(reps))
        )
        full_reconstruction = full_design @ coefficients
        withheld_mesh = self._mesh(experiment.withheld_mesh_size)
        withheld_points = np.asarray(
            [(kx, ky) for kx in withheld_mesh for ky in withheld_mesh]
        )
        cutoff = experiment.plane_wave_cutoffs[-2]
        withheld_parent = np.asarray(
            [
                self._pw_eigensystem(
                    float(kx),
                    float(ky),
                    experiment.lambda_x,
                    experiment.lambda_y,
                    coupling,
                    cutoff,
                    vectors=False,
                )[0][0]
                for kx, ky in withheld_points
            ]
        )
        records: list[JsonValue] = []
        for squared_radius in experiment.shell_squared_radii:
            retained = np.asarray(
                [rx * rx + ry * ry <= squared_radius for rx, ry in reps]
            )
            design = full_design[:, retained]
            mediated_coefficients = coefficients[retained]
            mediated = design @ mediated_coefficients
            direct_coefficients = np.linalg.lstsq(design, flat_energies, rcond=None)[0]
            residual = flat_energies - mediated.real
            omitted = float(np.linalg.norm(coefficients[~retained]))
            withheld_design = np.exp(
                2j
                * np.pi
                * np.asarray(
                    [
                        kx * rx + ky * ry
                        for kx, ky in withheld_points
                        for (rx, ry), keep in zip(reps, retained, strict=True)
                        if keep
                    ]
                ).reshape(len(withheld_points), int(np.sum(retained)))
            )
            withheld_residual = (
                withheld_parent - (withheld_design @ mediated_coefficients).real
            )
            records.append(
                {
                    "maximum_squared_radius": squared_radius,
                    "retained_coefficient_count": int(np.sum(retained)),
                    "omitted_hopping_l2_norm": omitted,
                    "training_root_mean_square_error": float(
                        np.sqrt(np.mean(np.square(residual)))
                    ),
                    "training_maximum_absolute_error": float(np.max(np.abs(residual))),
                    "withheld_root_mean_square_error": float(
                        np.sqrt(np.mean(np.square(withheld_residual)))
                    ),
                    "withheld_maximum_absolute_error": float(
                        np.max(np.abs(withheld_residual))
                    ),
                    "parseval_absolute_residual": abs(
                        float(np.sum(np.square(residual)))
                        - len(points) * omitted * omitted
                    ),
                    "direct_mediated_coefficient_l2_defect": float(
                        np.linalg.norm(direct_coefficients - mediated_coefficients)
                    ),
                }
            )
        records[-1]["full_mesh_reconstruction_maximum_absolute_error"] = float(
            np.max(np.abs(full_reconstruction.real - flat_energies))
        )
        records[-1]["full_mesh_reconstruction_maximum_imaginary"] = float(
            np.max(np.abs(full_reconstruction.imag))
        )
        return records, hoppings

    def _topology(
        self, vectors: npt.NDArray[np.complex128], cutoff: int
    ) -> dict[str, JsonValue]:
        size = vectors.shape[0]
        ux = np.empty((size, size), dtype=np.complex128)
        uy = np.empty((size, size), dtype=np.complex128)
        overlap_minimum = np.inf
        for ix in range(size):
            for iy in range(size):
                current = vectors[ix, iy]
                target_x = (
                    vectors[ix + 1, iy]
                    if ix + 1 < size
                    else self._sew(vectors[0, iy], cutoff, 1, 0)
                )
                target_y = (
                    vectors[ix, iy + 1]
                    if iy + 1 < size
                    else self._sew(vectors[ix, 0], cutoff, 0, 1)
                )
                overlap_x = np.vdot(current, target_x)
                overlap_y = np.vdot(current, target_y)
                overlap_minimum = min(
                    overlap_minimum, float(abs(overlap_x)), float(abs(overlap_y))
                )
                if overlap_x == 0.0 or overlap_y == 0.0:
                    raise RuntimeError("PERIODIC_2D.SUBSPACE_OVERLAP_TOO_SMALL")
                ux[ix, iy] = overlap_x / abs(overlap_x)
                uy[ix, iy] = overlap_y / abs(overlap_y)
        plaquettes = np.empty((size, size), dtype=np.float64)
        for ix in range(size):
            for iy in range(size):
                plaquettes[ix, iy] = np.angle(
                    ux[ix, iy]
                    * uy[(ix + 1) % size, iy]
                    * np.conj(ux[ix, (iy + 1) % size])
                    * np.conj(uy[ix, iy])
                )
        wilson_x = [float(np.angle(np.prod(ux[:, iy]))) for iy in range(size)]
        wilson_y = [float(np.angle(np.prod(uy[ix, :]))) for ix in range(size)]
        chern = float(np.sum(plaquettes) / (2.0 * np.pi))
        return {
            "minimum_neighbor_overlap": overlap_minimum,
            "wilson_loop_x_phases": wilson_x,
            "wilson_loop_y_phases": wilson_y,
            "maximum_absolute_plaquette_phase": float(np.max(np.abs(plaquettes))),
            "chern_number": chern,
            "chern_integer_defect": abs(chern - round(chern)),
        }

    @staticmethod
    def _phase_sequence_defect(
        first: list[JsonValue], second: list[JsonValue]
    ) -> float:
        values_first = np.asarray([float(cast(float, value)) for value in first])
        values_second = np.asarray([float(cast(float, value)) for value in second])
        return float(
            np.max(np.abs(np.angle(np.exp(1j * (values_first - values_second)))))
        )

    @staticmethod
    def _sew(
        vector: ComplexVector, cutoff: int, shift_x: int, shift_y: int
    ) -> ComplexVector:
        size = 2 * cutoff + 1
        source = vector.reshape((size, size))
        result = np.zeros_like(source)
        if shift_x == 1 and shift_y == 0:
            result[:-1, :] = source[1:, :]
        elif shift_x == 0 and shift_y == 1:
            result[:, :-1] = source[:, 1:]
        else:
            raise ValueError("only positive unit sewing shifts are supported")
        return result.ravel()

    def _symmetry_residuals(
        self, mesh: RealVector, energies: RealMatrix, *, square: bool
    ) -> dict[str, JsonValue]:
        lookup = {round(float(value), 14): index for index, value in enumerate(mesh)}
        time_reversal = 0.0
        reflection_x = 0.0
        reflection_y = 0.0
        rotation = 0.0
        for ix, kx in enumerate(mesh):
            for iy, ky in enumerate(mesh):
                nix = lookup[round(float(-kx), 14)]
                niy = lookup[round(float(-ky), 14)]
                time_reversal = max(
                    time_reversal, abs(float(energies[ix, iy] - energies[nix, niy]))
                )
                reflection_x = max(
                    reflection_x, abs(float(energies[ix, iy] - energies[nix, iy]))
                )
                reflection_y = max(
                    reflection_y, abs(float(energies[ix, iy] - energies[ix, niy]))
                )
                rotated_x = lookup[round(float(-ky), 14)]
                rotated_y = lookup[round(float(kx), 14)]
                rotation = max(
                    rotation,
                    abs(float(energies[ix, iy] - energies[rotated_x, rotated_y])),
                )
        return {
            "time_reversal_maximum_absolute_energy": time_reversal,
            "reflection_x_maximum_absolute_energy": reflection_x,
            "reflection_y_maximum_absolute_energy": reflection_y,
            "c4_rotation_maximum_absolute_energy": rotation,
            "c4_expected": square,
        }

    def _effective_mass_tensor(
        self,
        lambda_x: float,
        lambda_y: float,
        lambda_xy: float,
        cutoff: int,
        step: float,
    ) -> dict[str, JsonValue]:
        def energy(kx: float, ky: float) -> float:
            return float(
                self._pw_eigensystem(
                    kx,
                    ky,
                    lambda_x,
                    lambda_y,
                    lambda_xy,
                    cutoff,
                    vectors=False,
                )[0][0]
            )

        origin = energy(0.0, 0.0)
        dxx = (energy(step, 0.0) - 2.0 * origin + energy(-step, 0.0)) / (step * step)
        dyy = (energy(0.0, step) - 2.0 * origin + energy(0.0, -step)) / (step * step)
        dxy = (
            energy(step, step)
            - energy(step, -step)
            - energy(-step, step)
            + energy(-step, -step)
        ) / (4.0 * step * step)
        hessian = np.asarray([[dxx, dxy], [dxy, dyy]])
        inverse_mass_relative_bare = hessian / 2.0
        mass_relative_bare = np.linalg.inv(inverse_mass_relative_bare)
        return {
            "step_in_reciprocal_vector_units": step,
            "energy_hessian_in_EG_over_G2": hessian.tolist(),
            "inverse_mass_tensor_relative_to_bare_inverse_mass": (
                inverse_mass_relative_bare.tolist()
            ),
            "mass_tensor_relative_to_bare_mass": mass_relative_bare.tolist(),
            "principal_masses_relative_to_bare_mass": np.linalg.eigvalsh(
                mass_relative_bare
            ).tolist(),
        }

    @staticmethod
    def _mesh(size: int) -> RealVector:
        half = size // 2
        return np.arange(-half, half + 1, dtype=np.float64) / size

    @staticmethod
    def _representatives(size: int) -> tuple[tuple[int, int], ...]:
        half = size // 2
        return tuple(
            (rx, ry) for rx in range(-half, half + 1) for ry in range(-half, half + 1)
        )

    @staticmethod
    def _pw_1d_matrix(k: float, strength: float, cutoff: int) -> ComplexMatrix:
        indices = np.arange(-cutoff, cutoff + 1, dtype=np.float64)
        matrix = np.diag(np.square(k + indices)).astype(np.complex128)
        coupling = strength / 2.0
        matrix += np.diag(np.full(2 * cutoff, coupling), 1)
        matrix += np.diag(np.full(2 * cutoff, coupling), -1)
        return matrix

    @staticmethod
    def _pw_matrix(
        kx: float,
        ky: float,
        lambda_x: float,
        lambda_y: float,
        lambda_xy: float,
        cutoff: int,
    ) -> ComplexMatrix:
        pairs = tuple(
            (p, q)
            for p in range(-cutoff, cutoff + 1)
            for q in range(-cutoff, cutoff + 1)
        )
        lookup = {pair: index for index, pair in enumerate(pairs)}
        matrix = np.zeros((len(pairs), len(pairs)), dtype=np.complex128)
        for index, (p, q) in enumerate(pairs):
            matrix[index, index] = (kx + p) ** 2 + (ky + q) ** 2
            for dp in (-1, 1):
                target = lookup.get((p + dp, q))
                if target is not None:
                    matrix[index, target] += lambda_x / 2.0
            for dq in (-1, 1):
                target = lookup.get((p, q + dq))
                if target is not None:
                    matrix[index, target] += lambda_y / 2.0
            for dp in (-1, 1):
                for dq in (-1, 1):
                    target = lookup.get((p + dp, q + dq))
                    if target is not None:
                        matrix[index, target] += lambda_xy / 4.0
        return matrix

    def _pw_eigensystem(
        self,
        kx: float,
        ky: float,
        lambda_x: float,
        lambda_y: float,
        lambda_xy: float,
        cutoff: int,
        *,
        vectors: bool,
    ) -> tuple[RealVector, ComplexMatrix]:
        matrix = self._pw_matrix(kx, ky, lambda_x, lambda_y, lambda_xy, cutoff)
        if vectors:
            values, states = np.linalg.eigh(matrix)
            return values, states
        return np.linalg.eigvalsh(matrix), np.empty((0, 0), dtype=np.complex128)

    @staticmethod
    def _fd_1d_matrix(k: float, points: int, period: float) -> ComplexMatrix:
        spacing = period / points
        matrix = np.diag(np.full(points, 2.0 / (spacing * spacing))).astype(
            np.complex128
        )
        off_diagonal = -1.0 / (spacing * spacing)
        matrix += np.diag(np.full(points - 1, off_diagonal), 1)
        matrix += np.diag(np.full(points - 1, off_diagonal), -1)
        matrix[0, -1] = off_diagonal * np.exp(-1j * k * period)
        matrix[-1, 0] = off_diagonal * np.exp(1j * k * period)
        return matrix

    def _fd_matrix(
        self,
        kx: float,
        ky: float,
        lambda_x: float,
        lambda_y: float,
        lambda_xy: float,
        points: int,
        period: float,
    ) -> ComplexMatrix:
        tx = self._fd_1d_matrix(kx, points, period)
        ty = self._fd_1d_matrix(ky, points, period)
        identity = np.eye(points)
        matrix = np.kron(tx, identity) + np.kron(identity, ty)
        coordinate = np.arange(points, dtype=np.float64) * period / points
        potential = (
            lambda_x * np.cos(coordinate)[:, None]
            + lambda_y * np.cos(coordinate)[None, :]
            + lambda_xy * np.cos(coordinate)[:, None] * np.cos(coordinate)[None, :]
        )
        matrix += np.diag(potential.ravel())
        return matrix

    @staticmethod
    def _transport_fd_to_low_modes(
        matrix: ComplexMatrix,
        kx: float,
        ky: float,
        points: int,
        low_cutoff: int,
        period: float,
    ) -> ComplexMatrix:
        coordinate = np.arange(points, dtype=np.float64) * period / points
        x, y = np.meshgrid(coordinate, coordinate, indexing="ij")
        columns = []
        for p in range(-low_cutoff, low_cutoff + 1):
            for q in range(-low_cutoff, low_cutoff + 1):
                columns.append(
                    np.exp(1j * ((kx + p) * x + (ky + q) * y)).ravel() / points
                )
        transform = np.column_stack(columns)
        return transform.conj().T @ matrix @ transform


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    experiment = ExperimentInputDeserializer().execute(arguments.input.read_bytes())
    output = Periodic2DExperiment().execute(
        experiment, arguments.input.resolve(), Path(__file__).resolve()
    )
    arguments.output.write_bytes(output)


if __name__ == "__main__":
    main()
