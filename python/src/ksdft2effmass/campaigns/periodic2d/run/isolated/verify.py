#!/usr/bin/env python3
"""Independently verify the retained two-dimensional periodic-reduction result."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt
from scipy.linalg import eigh  # type: ignore[import-untyped]

from ...model.retained import Periodic2DIsolatedBandCampaignModel

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type RealVector = npt.NDArray[np.float64]
type RealMatrix = npt.NDArray[np.float64]
type ComplexVector = npt.NDArray[np.complex128]
type ComplexMatrix = npt.NDArray[np.complex128]


@dataclass(frozen=True, slots=True)
class Periodic2DIsolatedBandCampaignVerificationRequest:
    """Request independent verification of one isolated retained campaign."""

    model: Periodic2DIsolatedBandCampaignModel
    repository_root: Path

    def __post_init__(self) -> None:
        """Validate exact model ownership and an absolute repository root."""
        if type(self.model) is not Periodic2DIsolatedBandCampaignModel:
            raise TypeError("model must be Periodic2DIsolatedBandCampaignModel")
        if not isinstance(self.repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        if not self.repository_root.is_absolute():
            raise ValueError("repository_root must be absolute")


@dataclass(frozen=True, slots=True)
class Periodic2DIsolatedBandCampaignVerificationResult:
    """Report source, structural, numerical, and aggregate verification channels."""

    source_authentication_passed: bool
    structural_contract_passed: bool
    numerical_reconstruction_passed: bool
    coupling_case_count: int
    retained_result_sha256: str
    maximum_reconstructed_energy_defect: float
    maximum_reconstructed_hopping_defect: float

    @property
    def passes(self) -> bool:
        """Return the aggregate bounded verification disposition."""
        return (
            self.source_authentication_passed
            and self.structural_contract_passed
            and self.numerical_reconstruction_passed
        )


class Periodic2DIsolatedBandCampaignVerifier:
    """Independently reconstruct operators, topology, and reductions."""

    __slots__ = ()

    def execute(
        self, request: Periodic2DIsolatedBandCampaignVerificationRequest
    ) -> Periodic2DIsolatedBandCampaignVerificationResult:
        """Authenticate retained sources and reconstruct numerical channels."""
        if type(request) is not Periodic2DIsolatedBandCampaignVerificationRequest:
            raise TypeError(
                "request must be Periodic2DIsolatedBandCampaignVerificationRequest"
            )
        result = self._mapping(
            cast(JsonValue, json.loads(request.model.result_payload)), "result"
        )
        self._require(result["schema_version"] == 1, "schema version mismatch")
        self._require(
            result["evidence_status"] == "illustrative numerical experiment",
            "evidence status mismatch",
        )
        self._require(
            result["calculation_status"] == "calculated illustrative result",
            "calculation status mismatch",
        )
        provenance = self._mapping(result["provenance"], "provenance")
        input_hash = hashlib.sha256(request.model.input_payload).hexdigest()
        self._require(
            input_hash == provenance["input_sha256"], "input identity mismatch"
        )
        script_path = request.repository_root / self._string(provenance["script_path"])
        self._require(
            hashlib.sha256(script_path.read_bytes()).hexdigest()
            == provenance["script_sha256"],
            "script identity mismatch",
        )
        source = self._mapping(
            cast(JsonValue, json.loads(request.model.input_payload)), "input"
        )
        isotropic = self._mapping(source["isotropic_potential"], "isotropic")
        lx = self._real(isotropic["lambda_x"])
        ly = self._real(isotropic["lambda_y"])
        cutoffs = self._integers(source["plane_wave_cutoffs"])
        reference = self._integer(source["plane_wave_reference_cutoff"])
        parent_coupling = self._real(source["parent_coupling"])
        compared = self._integer(source["compared_band_count"])
        low_cutoff = self._integer(source["common_low_mode_cutoff"])
        period = self._real(
            self._mapping(source["dimensionless_convention"], "convention")[
                "lattice_period"
            ]
        )
        sample_momenta = self._pairs(source["parent_sample_momenta"])
        self._verify_parent(
            self._mapping(result["parent_representation_verification"], "parent"),
            lx,
            ly,
            parent_coupling,
            cutoffs,
            reference,
            self._integers(source["finite_difference_points"]),
            sample_momenta,
            compared,
            low_cutoff,
            period,
        )
        self._verify_separable(
            self._mapping(result["separable_reference"], "separable"),
            lx,
            ly,
            cutoffs[-1],
            sample_momenta,
        )
        mesh_size = self._integer(source["reciprocal_mesh_size"])
        withheld_size = self._integer(source["withheld_mesh_size"])
        shells = self._integers(source["hopping_shell_squared_radii"])
        mass_step = self._real(source["effective_mass_step"])
        continuation = self._records(result["coupling_continuation"])
        couplings = self._reals(source["coupling_sequence"])
        self._require(
            len(continuation) == len(couplings), "coupling inventory mismatch"
        )
        maximum_energy_defect = 0.0
        maximum_hopping_defect = 0.0
        for record, coupling in zip(continuation, couplings, strict=True):
            energy_defect, hopping_defect = self._verify_coupling_case(
                record,
                lx,
                ly,
                coupling,
                cutoffs[-2],
                mesh_size,
                withheld_size,
                shells,
                mass_step,
            )
            maximum_energy_defect = max(maximum_energy_defect, energy_defect)
            maximum_hopping_defect = max(maximum_hopping_defect, hopping_defect)
        self._verify_anisotropy(
            self._mapping(result["anisotropy_control"], "anisotropy"),
            cutoffs[-2],
            mesh_size,
            mass_step,
        )
        limitations = result["limitations"]
        self._require(
            isinstance(limitations, list) and len(limitations) == 5,
            "limitations contract mismatch",
        )
        return Periodic2DIsolatedBandCampaignVerificationResult(
            source_authentication_passed=True,
            structural_contract_passed=True,
            numerical_reconstruction_passed=True,
            coupling_case_count=len(continuation),
            retained_result_sha256=hashlib.sha256(
                request.model.result_payload
            ).hexdigest(),
            maximum_reconstructed_energy_defect=maximum_energy_defect,
            maximum_reconstructed_hopping_defect=maximum_hopping_defect,
        )

    def _verify_parent(
        self,
        parent: dict[str, JsonValue],
        lx: float,
        ly: float,
        coupling: float,
        cutoffs: tuple[int, ...],
        reference: int,
        fd_sizes: tuple[int, ...],
        momenta: tuple[tuple[float, float], ...],
        compared: int,
        low_cutoff: int,
        period: float,
    ) -> None:
        cutoff_records = self._records(parent["plane_wave_cutoff_study"])
        self._require(
            len(cutoff_records) == len(cutoffs),
            "independent verification condition failed",
        )
        cutoff_errors: list[float] = []
        for record, cutoff in zip(cutoff_records, cutoffs, strict=True):
            maximum = 0.0
            for kx, ky in momenta:
                expected = np.linalg.eigvalsh(
                    self._plane_wave(kx, ky, lx, ly, coupling, reference)
                )[:compared]
                observed = np.linalg.eigvalsh(
                    self._plane_wave(kx, ky, lx, ly, coupling, cutoff)
                )[:compared]
                maximum = max(maximum, float(np.max(np.abs(observed - expected))))
            np.testing.assert_allclose(
                self._real(record["maximum_low_band_absolute_error"]),
                maximum,
                rtol=0.0,
                atol=2.0e-14,
            )
            cutoff_errors.append(maximum)
        self._require(
            np.all(np.diff(cutoff_errors) < 0.0),
            "independent verification condition failed",
        )
        self._require(
            cutoff_errors[-1] < 1e-09, "independent verification condition failed"
        )

        fd_records = self._records(parent["finite_difference_grid_study"])
        self._require(
            len(fd_records) == len(fd_sizes),
            "independent verification condition failed",
        )
        spectral_errors: list[float] = []
        operator_errors: list[float] = []
        for record, points in zip(fd_records, fd_sizes, strict=True):
            spectral = 0.0
            operator = 0.0
            for kx, ky in momenta:
                expected = np.linalg.eigvalsh(
                    self._plane_wave(kx, ky, lx, ly, coupling, reference)
                )[:compared]
                finite = self._finite_difference(
                    kx, ky, lx, ly, coupling, points, period
                )
                values = eigh(
                    finite,
                    subset_by_index=[0, compared - 1],
                    eigvals_only=True,
                    driver="evr",
                )
                spectral = max(spectral, float(np.max(np.abs(values - expected))))
                basis = self._sampled_plane_waves(kx, ky, points, low_cutoff, period)
                transported = basis.conj().T @ finite @ basis
                common = self._plane_wave(kx, ky, lx, ly, coupling, low_cutoff)
                operator = max(operator, float(np.linalg.norm(transported - common)))
            np.testing.assert_allclose(
                self._real(record["maximum_low_band_absolute_error"]),
                spectral,
                rtol=0.0,
                atol=2.0e-13,
            )
            np.testing.assert_allclose(
                self._real(record["maximum_common_low_mode_frobenius_error"]),
                operator,
                rtol=0.0,
                atol=2.0e-13,
            )
            spectral_errors.append(spectral)
            operator_errors.append(operator)
        self._require(
            np.all(np.diff(spectral_errors) < 0.0),
            "independent verification condition failed",
        )
        self._require(
            np.all(np.diff(operator_errors) < 0.0),
            "independent verification condition failed",
        )

    def _verify_separable(
        self,
        record: dict[str, JsonValue],
        lx: float,
        ly: float,
        cutoff: int,
        momenta: tuple[tuple[float, float], ...],
    ) -> None:
        matrix_defect = 0.0
        spectrum_defect = 0.0
        for kx, ky in momenta:
            hx = self._one_dimensional(kx, lx, cutoff)
            hy = self._one_dimensional(ky, ly, cutoff)
            size = hx.shape[0]
            expected_matrix = np.kron(hx, np.eye(size)) + np.kron(np.eye(size), hy)
            direct = self._plane_wave(kx, ky, lx, ly, 0.0, cutoff)
            matrix_defect = max(
                matrix_defect, float(np.linalg.norm(direct - expected_matrix))
            )
            expected_values = np.sort(
                (
                    np.linalg.eigvalsh(hx)[:, None] + np.linalg.eigvalsh(hy)[None, :]
                ).ravel()
            )
            spectrum_defect = max(
                spectrum_defect,
                float(np.max(np.abs(np.linalg.eigvalsh(direct) - expected_values))),
            )
        np.testing.assert_allclose(
            self._real(record["maximum_kronecker_sum_matrix_frobenius_defect"]),
            matrix_defect,
            atol=1.0e-15,
        )
        np.testing.assert_allclose(
            self._real(record["maximum_full_spectrum_product_sum_defect"]),
            spectrum_defect,
            atol=2.0e-14,
        )
        cluster = self._mapping(record["gamma_degenerate_cluster"], "cluster")
        self._require(
            self._integer(cluster["rank"]) == 2,
            "independent verification condition failed",
        )
        self._require(
            self._real(cluster["projector_frobenius_defect"]) < 2e-13,
            "independent verification condition failed",
        )
        np.testing.assert_allclose(
            self._real(cluster["controlled_basis_rotation_minimum_individual_overlap"]),
            1.0 / np.sqrt(2.0),
            atol=2.0e-15,
        )
        self._require(
            self._real(cluster["controlled_basis_rotation_projector_defect"]) < 1e-14,
            "independent verification condition failed",
        )

    def _verify_coupling_case(
        self,
        record: dict[str, JsonValue],
        lx: float,
        ly: float,
        coupling: float,
        cutoff: int,
        mesh_size: int,
        withheld_size: int,
        shells: tuple[int, ...],
        mass_step: float,
    ) -> tuple[float, float]:
        np.testing.assert_allclose(self._real(record["lambda_xy"]), coupling)
        mesh = self._mesh(mesh_size)
        stored = np.asarray(self._matrix_reals(record["lowest_band_energies"]))
        reconstructed = np.empty_like(stored)
        vectors = np.empty((mesh_size, mesh_size, (2 * cutoff + 1) ** 2), complex)
        minimum_gap = np.inf
        separability = 0.0
        x_values = {
            float(k): np.linalg.eigvalsh(self._one_dimensional(float(k), lx, cutoff))[0]
            for k in mesh
        }
        y_values = {
            float(k): np.linalg.eigvalsh(self._one_dimensional(float(k), ly, cutoff))[0]
            for k in mesh
        }
        for ix, kx in enumerate(mesh):
            for iy, ky in enumerate(mesh):
                values, states = np.linalg.eigh(
                    self._plane_wave(float(kx), float(ky), lx, ly, coupling, cutoff)
                )
                reconstructed[ix, iy] = values[0]
                vectors[ix, iy] = states[:, 0]
                minimum_gap = min(minimum_gap, float(values[1] - values[0]))
                separability = max(
                    separability,
                    abs(float(values[0]) - x_values[float(kx)] - y_values[float(ky)]),
                )
        energy_defect = float(np.max(np.abs(stored - reconstructed)))
        self._require(
            energy_defect < 2e-14, "independent verification condition failed"
        )
        np.testing.assert_allclose(
            self._real(record["minimum_isolation_gap"]), minimum_gap, atol=2.0e-14
        )
        np.testing.assert_allclose(
            self._real(record["maximum_lowest_band_separability_residual"]),
            separability,
            atol=2.0e-14,
        )
        topology = self._topology(vectors, cutoff)
        observed_topology = self._mapping(record["topology_and_gauge"], "topology")
        np.testing.assert_allclose(
            self._real(observed_topology["minimum_neighbor_overlap"]),
            topology[0],
            atol=2.0e-14,
        )
        np.testing.assert_allclose(
            self._real(observed_topology["chern_number"]), topology[1], atol=1.0e-13
        )
        self._require(
            abs(topology[1]) < 1e-12, "independent verification condition failed"
        )
        self._require(
            self._real(observed_topology["gauge_attack_chern_difference"]) < 1e-12,
            "independent verification condition failed",
        )
        self._require(
            self._real(
                observed_topology["gauge_attack_maximum_wilson_phase_difference"]
            )
            < 2e-12,
            "independent verification condition failed",
        )
        hopping_defect = self._verify_hoppings(
            record,
            reconstructed,
            mesh,
            lx,
            ly,
            coupling,
            cutoff,
            withheld_size,
            shells,
        )
        observed_mass = self._mapping(record["effective_mass"], "effective_mass")
        expected_mass = self._mass_tensor(lx, ly, coupling, cutoff, mass_step)
        np.testing.assert_allclose(
            np.asarray(
                self._matrix_reals(observed_mass["mass_tensor_relative_to_bare_mass"])
            ),
            expected_mass,
            rtol=0.0,
            atol=2.0e-10,
        )
        symmetry = self._mapping(record["symmetry_residuals"], "symmetry")
        self._require(
            self._real(symmetry["time_reversal_maximum_absolute_energy"]) < 5e-13,
            "independent verification condition failed",
        )
        self._require(
            self._real(symmetry["c4_rotation_maximum_absolute_energy"]) < 5e-13,
            "independent verification condition failed",
        )
        return energy_defect, hopping_defect

    def _verify_hoppings(
        self,
        record: dict[str, JsonValue],
        energies: RealMatrix,
        mesh: RealVector,
        lx: float,
        ly: float,
        coupling: float,
        cutoff: int,
        withheld_size: int,
        shells: tuple[int, ...],
    ) -> float:
        reps = self._representatives(mesh.size)
        points = np.asarray([(kx, ky) for kx in mesh for ky in mesh])
        phase = np.exp(
            -2j
            * np.pi
            * np.asarray([[kx * rx + ky * ry for kx, ky in points] for rx, ry in reps])
        )
        coefficients = phase @ energies.ravel() / points.shape[0]
        stored_records = self._records(record["hopping_coefficients"])
        stored = np.asarray(
            [
                self._real(item["real"]) + 1j * self._real(item["imag"])
                for item in stored_records
            ]
        )
        maximum_defect = float(np.max(np.abs(coefficients - stored)))
        self._require(
            maximum_defect < 2e-14, "independent verification condition failed"
        )
        design = np.exp(
            2j
            * np.pi
            * np.asarray([[kx * rx + ky * ry for rx, ry in reps] for kx, ky in points])
        )
        withheld_mesh = self._mesh(withheld_size)
        withheld_points = np.asarray(
            [(kx, ky) for kx in withheld_mesh for ky in withheld_mesh]
        )
        withheld_parent = np.asarray(
            [
                np.linalg.eigvalsh(
                    self._plane_wave(float(kx), float(ky), lx, ly, coupling, cutoff)
                )[0]
                for kx, ky in withheld_points
            ]
        )
        shell_records = self._records(record["shell_study"])
        self._require(
            len(shell_records) == len(shells),
            "independent verification condition failed",
        )
        previous_omitted = np.inf
        for observed, radius in zip(shell_records, shells, strict=True):
            retained = np.asarray(
                [rx * rx + ry * ry <= radius for rx, ry in reps], dtype=np.bool_
            )
            fit = design[:, retained]
            mediated = fit @ coefficients[retained]
            residual = energies.ravel() - mediated.real
            omitted = float(np.linalg.norm(coefficients[~retained]))
            np.testing.assert_allclose(
                self._real(observed["omitted_hopping_l2_norm"]), omitted, atol=2.0e-14
            )
            np.testing.assert_allclose(
                self._real(observed["training_root_mean_square_error"]),
                np.sqrt(np.mean(np.square(residual))),
                atol=2.0e-14,
            )
            direct = np.linalg.lstsq(fit, energies.ravel(), rcond=None)[0]
            np.testing.assert_allclose(
                self._real(observed["direct_mediated_coefficient_l2_defect"]),
                np.linalg.norm(direct - coefficients[retained]),
                atol=2.0e-14,
            )
            withheld_design = np.exp(
                2j
                * np.pi
                * np.asarray(
                    [
                        [
                            kx * rx + ky * ry
                            for (rx, ry), keep in zip(reps, retained, strict=True)
                            if keep
                        ]
                        for kx, ky in withheld_points
                    ]
                )
            )
            withheld_residual = (
                withheld_parent - (withheld_design @ coefficients[retained]).real
            )
            np.testing.assert_allclose(
                self._real(observed["withheld_root_mean_square_error"]),
                np.sqrt(np.mean(np.square(withheld_residual))),
                atol=2.0e-14,
            )
            self._require(
                omitted <= previous_omitted + 2e-14,
                "independent verification condition failed",
            )
            previous_omitted = omitted
        self._require(
            self._real(
                shell_records[-1]["full_mesh_reconstruction_maximum_absolute_error"]
            )
            < 2e-13,
            "independent verification condition failed",
        )
        return maximum_defect

    def _verify_anisotropy(
        self,
        record: dict[str, JsonValue],
        cutoff: int,
        mesh_size: int,
        step: float,
    ) -> None:
        lx = self._real(record["lambda_x"])
        ly = self._real(record["lambda_y"])
        coupling = self._real(record["lambda_xy"])
        observed = self._mapping(record["effective_mass"], "effective_mass")
        expected = self._mass_tensor(lx, ly, coupling, cutoff, step)
        np.testing.assert_allclose(
            np.asarray(
                self._matrix_reals(observed["mass_tensor_relative_to_bare_mass"])
            ),
            expected,
            atol=2.0e-10,
        )
        symmetry = self._mapping(record["symmetry_residuals"], "symmetry")
        self._require(
            symmetry["c4_expected"] is False,
            "independent verification condition failed",
        )
        self._require(
            self._real(symmetry["c4_rotation_maximum_absolute_energy"]) > 0.001,
            "independent verification condition failed",
        )
        self._require(
            self._real(symmetry["time_reversal_maximum_absolute_energy"]) < 5e-13,
            "independent verification condition failed",
        )
        self._require(mesh_size >= 5, "independent verification condition failed")

    def _topology(
        self, vectors: npt.NDArray[np.complex128], cutoff: int
    ) -> tuple[float, float]:
        size = vectors.shape[0]
        links_x = np.empty((size, size), complex)
        links_y = np.empty((size, size), complex)
        minimum = np.inf
        dimension = 2 * cutoff + 1
        for ix in range(size):
            for iy in range(size):
                current = vectors[ix, iy]
                if ix + 1 < size:
                    right = vectors[ix + 1, iy]
                else:
                    source = vectors[0, iy].reshape(dimension, dimension)
                    sewn = np.zeros_like(source)
                    sewn[:-1, :] = source[1:, :]
                    right = sewn.ravel()
                if iy + 1 < size:
                    up = vectors[ix, iy + 1]
                else:
                    source = vectors[ix, 0].reshape(dimension, dimension)
                    sewn = np.zeros_like(source)
                    sewn[:, :-1] = source[:, 1:]
                    up = sewn.ravel()
                ox = np.vdot(current, right)
                oy = np.vdot(current, up)
                minimum = min(minimum, float(abs(ox)), float(abs(oy)))
                links_x[ix, iy] = ox / abs(ox)
                links_y[ix, iy] = oy / abs(oy)
        total = 0.0
        for ix in range(size):
            for iy in range(size):
                total += np.angle(
                    links_x[ix, iy]
                    * links_y[(ix + 1) % size, iy]
                    / links_x[ix, (iy + 1) % size]
                    / links_y[ix, iy]
                )
        return minimum, float(total / (2.0 * np.pi))

    def _mass_tensor(
        self,
        lx: float,
        ly: float,
        coupling: float,
        cutoff: int,
        step: float,
    ) -> RealMatrix:
        def energy(kx: float, ky: float) -> float:
            """Return the independently reconstructed lowest energy."""
            return float(
                np.linalg.eigvalsh(self._plane_wave(kx, ky, lx, ly, coupling, cutoff))[
                    0
                ]
            )

        origin = energy(0.0, 0.0)
        dxx = (energy(step, 0.0) - 2.0 * origin + energy(-step, 0.0)) / step**2
        dyy = (energy(0.0, step) - 2.0 * origin + energy(0.0, -step)) / step**2
        dxy = (
            energy(step, step)
            - energy(step, -step)
            - energy(-step, step)
            + energy(-step, -step)
        ) / (4.0 * step**2)
        return np.linalg.inv(np.asarray([[dxx, dxy], [dxy, dyy]]) / 2.0)

    @staticmethod
    def _plane_wave(
        kx: float,
        ky: float,
        lx: float,
        ly: float,
        coupling: float,
        cutoff: int,
    ) -> ComplexMatrix:
        indices = np.arange(-cutoff, cutoff + 1)
        p, q = np.meshgrid(indices, indices, indexing="ij")
        flat_p = p.ravel()
        flat_q = q.ravel()
        delta_p = flat_p[:, None] - flat_p[None, :]
        delta_q = flat_q[:, None] - flat_q[None, :]
        matrix: ComplexMatrix = np.asarray(
            np.diag((kx + flat_p) ** 2 + (ky + flat_q) ** 2),
            dtype=np.complex128,
        )
        matrix += (lx / 2.0) * ((np.abs(delta_p) == 1) & (delta_q == 0))
        matrix += (ly / 2.0) * ((delta_p == 0) & (np.abs(delta_q) == 1))
        matrix += (coupling / 4.0) * ((np.abs(delta_p) == 1) & (np.abs(delta_q) == 1))
        return matrix

    @staticmethod
    def _one_dimensional(k: float, strength: float, cutoff: int) -> ComplexMatrix:
        indices = np.arange(-cutoff, cutoff + 1)
        delta = indices[:, None] - indices[None, :]
        return np.asarray(
            np.diag((k + indices) ** 2) + (strength / 2.0) * (np.abs(delta) == 1),
            dtype=np.complex128,
        )

    @staticmethod
    def _finite_difference(
        kx: float,
        ky: float,
        lx: float,
        ly: float,
        coupling: float,
        points: int,
        period: float,
    ) -> ComplexMatrix:
        spacing = period / points
        dimension = points * points
        matrix = np.zeros((dimension, dimension), complex)
        coordinate = np.arange(points) * spacing
        for ix in range(points):
            for iy in range(points):
                row = ix * points + iy
                matrix[row, row] = (
                    4.0 / spacing**2
                    + lx * np.cos(coordinate[ix])
                    + ly * np.cos(coordinate[iy])
                    + coupling * np.cos(coordinate[ix]) * np.cos(coordinate[iy])
                )
                for dx, dy, phase in (
                    (1, 0, np.exp(1j * kx * period) if ix == points - 1 else 1.0),
                    (-1, 0, np.exp(-1j * kx * period) if ix == 0 else 1.0),
                    (0, 1, np.exp(1j * ky * period) if iy == points - 1 else 1.0),
                    (0, -1, np.exp(-1j * ky * period) if iy == 0 else 1.0),
                ):
                    column = ((ix + dx) % points) * points + ((iy + dy) % points)
                    matrix[row, column] = -phase / spacing**2
        return matrix

    @staticmethod
    def _sampled_plane_waves(
        kx: float, ky: float, points: int, cutoff: int, period: float
    ) -> ComplexMatrix:
        coordinate = np.arange(points) * period / points
        columns: list[ComplexVector] = []
        for p in range(-cutoff, cutoff + 1):
            for q in range(-cutoff, cutoff + 1):
                values = np.empty(points * points, complex)
                for ix, x in enumerate(coordinate):
                    for iy, y in enumerate(coordinate):
                        values[ix * points + iy] = (
                            np.exp(1j * ((kx + p) * x + (ky + q) * y)) / points
                        )
                columns.append(values)
        return np.column_stack(columns)

    @staticmethod
    def _mesh(size: int) -> RealVector:
        half = size // 2
        return np.arange(-half, half + 1, dtype=float) / size

    @staticmethod
    def _representatives(size: int) -> tuple[tuple[int, int], ...]:
        half = size // 2
        return tuple(
            (rx, ry) for rx in range(-half, half + 1) for ry in range(-half, half + 1)
        )

    @staticmethod
    def _require(condition: bool | np.bool_, message: str) -> None:
        if not bool(condition):
            raise ValueError(message)

    @staticmethod
    def _mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be an object")
        return value

    def _records(self, value: JsonValue) -> tuple[dict[str, JsonValue], ...]:
        if not isinstance(value, list):
            raise TypeError("value must be an array")
        return tuple(self._mapping(item, "record") for item in value)

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

    @staticmethod
    def _string(value: JsonValue) -> str:
        if not isinstance(value, str) or not value:
            raise TypeError("value must be a nonempty string")
        return value

    def _reals(self, value: JsonValue) -> tuple[float, ...]:
        if not isinstance(value, list):
            raise TypeError("value must be an array")
        return tuple(self._real(item) for item in value)

    def _integers(self, value: JsonValue) -> tuple[int, ...]:
        if not isinstance(value, list):
            raise TypeError("value must be an array")
        return tuple(self._integer(item) for item in value)

    def _pairs(self, value: JsonValue) -> tuple[tuple[float, float], ...]:
        if not isinstance(value, list):
            raise TypeError("value must be an array")
        result: list[tuple[float, float]] = []
        for item in value:
            if not isinstance(item, list) or len(item) != 2:
                raise TypeError("pair must have two values")
            result.append((self._real(item[0]), self._real(item[1])))
        return tuple(result)

    def _matrix_reals(self, value: JsonValue) -> list[list[float]]:
        if not isinstance(value, list):
            raise TypeError("matrix must be an array")
        rows: list[list[float]] = []
        for row in value:
            if not isinstance(row, list):
                raise TypeError("matrix row must be an array")
            rows.append([self._real(item) for item in row])
        return rows
