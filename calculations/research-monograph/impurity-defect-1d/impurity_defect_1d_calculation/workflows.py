"""Defect-1D workflows ownership."""

from __future__ import annotations

import hashlib
import platform
from pathlib import Path

import numpy as np
import numpy.typing as npt

from .model import (
    AlignmentControl,
    ComplexMatrix,
    ComplexVector,
    DefectExerciseInput,
    ExtractionControl,
    JsonValue,
    ParentData,
    RealVector,
    RepresentedOperator,
    SupercellBasis,
)
from .operators import (
    OperatorCompatibilityAnalyzer,
)
from .records import (
    DefectResultSerializer,
)


class MatchedDefectExtractionExperiment:
    """Execute folding, extraction, finite-size, model, and observable controls."""

    __slots__ = ("_compatibility", "_serializer")

    def __init__(self) -> None:
        self._compatibility = OperatorCompatibilityAnalyzer()
        self._serializer = DefectResultSerializer()

    def execute(
        self,
        specification: DefectExerciseInput,
        parent: ParentData,
        input_path: Path,
        script_path: Path,
    ) -> bytes:
        folding = self._folding_control(specification, parent)
        extraction, model_hierarchy, stopping = self._extraction_controls(
            specification, parent
        )
        finite_size = self._finite_size_control(specification, parent)
        smoothness, smoothness_state = self._smoothness_control(specification, parent)
        metric_contrast = self._metric_contrast_control(specification, smoothness_state)
        repository_root = script_path.parents[3]
        payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": specification.experiment_id,
            "evidence_status": "synthetic test data",
            "calculation_status": "calculated synthetic numerical-verification result",
            "parent": {
                "period": parent.period,
                "composite_orbital_count": 2,
                "composite_hopping_range_cells": specification.parent.hopping_range,
                "source_identities": [
                    {"path": path, "sha256": digest}
                    for path, digest in parent.source_identities
                ],
                "role": (
                    "accepted periodic-1D represented parents reused as fixed "
                    "synthetic inputs"
                ),
            },
            "folding_control": folding,
            "extraction_controls": extraction,
            "model_class_hierarchy": model_hierarchy,
            "stopping_controls": stopping,
            "finite_size_control": finite_size,
            "smoothness_control": smoothness,
            "metric_contrast_control": metric_contrast,
            "error_accounting": {
                "parent_representation_and_reduction": (
                    "Inherited from the accepted periodic-1D records; this exercise "
                    "adds no parent-solver or parent-reduction validation."
                ),
                "folding_and_alignment": (
                    "Reported by map unitarity, folded block residuals, null "
                    "extraction, and planted-operator recovery defects."
                ),
                "finite_size": (
                    "Reported through defect-band width, center, bound-state count, "
                    "core restriction, exterior norm, and localization metrics."
                ),
                "model_optimization": (
                    "The frozen finite classes use closed-form orthogonal projections; "
                    "there is no iterative optimizer error."
                ),
                "model_class": (
                    "Reported by frozen classwise operator residuals and never "
                    "combined with extraction or optimization error."
                ),
                "observable": (
                    "Operator residual, binding-energy difference, bound-state count, "
                    "and state fidelity remain separate."
                ),
                "scientific_validation": "Not performed.",
                "uncertainty_quantification": "Not performed.",
            },
            "limitations": [
                "Every defect and comparison map is synthetic and known by "
                "construction.",
                "The periodic parents are accepted represented reductions, not "
                "material Hamiltonians.",
                "The parabolic comparator is band-limited on one fixed grid and "
                "does not establish a continuum crossover.",
                "No silicon, dopant, DFT, production Wannier, scientific-validation, "
                "or UQ claim is made.",
            ],
            "provenance": {
                "input_path": input_path.resolve()
                .relative_to(repository_root)
                .as_posix(),
                "input_sha256": self._sha256(input_path),
                "script_path": script_path.resolve()
                .relative_to(repository_root)
                .as_posix(),
                "script_sha256": self._sha256(script_path),
                "implementation_identities": [
                    {
                        "path": path.relative_to(repository_root).as_posix(),
                        "sha256": self._sha256(path),
                    }
                    for path in self._implementation_paths()
                ],
                "python_version": platform.python_version(),
                "numpy_version": np.__version__,
            },
        }
        return self._serializer.execute(payload)

    def _folding_control(
        self, specification: DefectExerciseInput, parent: ParentData
    ) -> list[JsonValue]:
        hoppings = self._composite_hoppings(parent)
        size = specification.folding.supercell_size
        records: list[JsonValue] = []
        for scaled_momentum in specification.folding.reduced_momentum_times_supercell:
            momentum = scaled_momentum / size
            supercell = self._supercell_hamiltonian(hoppings, size, momentum)
            folded_momenta = tuple(
                self._reduce_momentum(momentum + branch / size)
                for branch in range(size)
            )
            folding_map = self._folding_map(size, folded_momenta)
            target = np.zeros_like(supercell)
            for branch, primitive_momentum in enumerate(folded_momenta):
                target[
                    2 * branch : 2 * branch + 2,
                    2 * branch : 2 * branch + 2,
                ] = self._primitive_hamiltonian(hoppings, primitive_momentum)
            represented = folding_map.conj().T @ supercell @ folding_map
            block_mask = np.zeros_like(represented, dtype=bool)
            for branch in range(size):
                block_mask[
                    2 * branch : 2 * branch + 2,
                    2 * branch : 2 * branch + 2,
                ] = True
            records.append(
                {
                    "reduced_momentum": momentum,
                    "reduced_momentum_times_supercell": scaled_momentum,
                    "folded_primitive_momenta": list(folded_momenta),
                    "folding_map_sha256": self._matrix_sha256(folding_map),
                    "folding_map_unitarity_frobenius_defect": self._norm(
                        folding_map.conj().T @ folding_map - np.eye(2 * size)
                    ),
                    "folded_operator_frobenius_defect": self._norm(
                        represented - target
                    ),
                    "folded_off_block_frobenius_norm": self._norm(
                        np.where(block_mask, 0.0, represented)
                    ),
                    "eigenvalue_maximum_absolute_defect": self._eigenvalue_defect(
                        supercell, target
                    ),
                    "supercell_operator_sha256": self._matrix_sha256(supercell),
                    "folded_target_sha256": self._matrix_sha256(target),
                }
            )
        return records

    def _extraction_controls(
        self, specification: DefectExerciseInput, parent: ParentData
    ) -> tuple[list[JsonValue], list[JsonValue], list[JsonValue]]:
        control = specification.extraction
        size = control.supercell_size
        momentum = control.reduced_momentum_times_supercell / size
        hoppings = self._composite_hoppings(parent)
        pristine = self._supercell_hamiltonian(hoppings, size, momentum)
        spinless_basis = self._basis(size, 1, momentum, "canonical", "shared_zero")
        spin_basis = self._basis(size, 2, momentum, "canonical", "shared_zero")
        pristine_spin: ComplexMatrix = np.asarray(
            np.kron(pristine, np.eye(2, dtype=np.complex128)), dtype=np.complex128
        )
        defects = self._planted_defects(control, size)
        records: list[JsonValue] = []
        model_records: list[JsonValue] = []
        null = np.zeros_like(pristine)
        null_record = self._extraction_record(
            "null",
            pristine,
            null,
            spinless_basis,
            specification,
        )
        records.append(null_record)
        for identifier in (
            "scalar-onsite",
            "orbital-onsite",
            "nearest-neighbor",
            "range-two-nonlocal",
        ):
            defect = defects[identifier]
            record = self._extraction_record(
                identifier,
                pristine,
                defect,
                spinless_basis,
                specification,
            )
            records.append(record)
            model_records.append(
                self._spinless_model_hierarchy(identifier, defect, size, specification)
            )
        for identifier in ("collinear-spin", "spin-mixing"):
            defect = defects[identifier]
            record = self._extraction_record(
                identifier,
                pristine_spin,
                defect,
                spin_basis,
                specification,
            )
            records.append(record)
            model_records.append(
                self._spin_model_hierarchy(identifier, defect, size, specification)
            )
        stopping = self._stopping_controls(pristine, spinless_basis)
        return records, model_records, stopping

    def _extraction_record(
        self,
        identifier: str,
        pristine: ComplexMatrix,
        defect: ComplexMatrix,
        canonical_basis: SupercellBasis,
        specification: DefectExerciseInput,
    ) -> dict[str, JsonValue]:
        spin_count = canonical_basis.spin_count
        coordinate_map = self._alignment_map(
            canonical_basis.cell_count,
            canonical_basis.reduced_momentum,
            spin_count,
            specification.alignment,
        )
        shift = specification.alignment.energy_shift
        raw = coordinate_map @ (
            pristine + defect
        ) @ coordinate_map.conj().T + shift * np.eye(pristine.shape[0])
        aligned_hamiltonian = (
            coordinate_map.conj().T
            @ (raw - shift * np.eye(raw.shape[0]))
            @ coordinate_map
        )
        extracted = aligned_hamiltonian - pristine
        uncorrected = coordinate_map.conj().T @ raw @ coordinate_map - pristine
        raw_basis = SupercellBasis(
            state_space_id=canonical_basis.state_space_id,
            cell_count=canonical_basis.cell_count,
            orbital_count=canonical_basis.orbital_count,
            spin_count=canonical_basis.spin_count,
            reduced_momentum=canonical_basis.reduced_momentum,
            site_ordering="translated-cyclic",
            orbital_ordering="rotated-and-phased",
            spin_ordering=(
                "rotated-spin-frame" if spin_count == 2 else "not-applicable"
            ),
            coordinate_frame="scrambled-known-map",
            energy_unit=canonical_basis.energy_unit,
            energy_reference="shifted_raw_zero",
            geometry_id=canonical_basis.geometry_id,
            subspace_id=canonical_basis.subspace_id,
        )
        pristine_record = RepresentedOperator("pristine", canonical_basis, pristine)
        raw_record = RepresentedOperator("raw-defect", raw_basis, raw)
        compatibility = self._compatibility.execute(pristine_record, raw_record)
        core_projector = self._site_projector(
            canonical_basis.cell_count,
            canonical_basis.orbital_count * spin_count,
            (0,),
        )
        exterior = np.eye(pristine.shape[0]) - core_projector
        false_offset = uncorrected - defect
        return {
            "id": identifier,
            "spin_count": spin_count,
            "dimension": pristine.shape[0],
            "planted_operator_sha256": self._matrix_sha256(defect),
            "raw_operator_sha256": self._matrix_sha256(raw),
            "alignment_map_sha256": self._matrix_sha256(coordinate_map),
            "extracted_operator_sha256": self._matrix_sha256(extracted),
            "alignment_map_unitarity_frobenius_defect": self._norm(
                coordinate_map.conj().T @ coordinate_map - np.eye(pristine.shape[0])
            ),
            "direct_comparison_status": compatibility.status,
            "direct_comparison_issue_codes": list(compatibility.issue_codes),
            "raw_coordinate_difference_frobenius_not_interpreted": self._norm(
                raw - pristine
            ),
            "aligned_extraction_frobenius_defect": self._norm(extracted - defect),
            "aligned_extraction_maximum_absolute_defect": self._maximum(
                extracted - defect
            ),
            "extracted_hermiticity_maximum_absolute_residual": self._maximum(
                extracted - extracted.conj().T
            ),
            "declared_energy_reference_shift": shift,
            "uncorrected_false_offset_frobenius_norm": self._norm(false_offset),
            "uncorrected_false_offset_exterior_frobenius_norm": self._norm(
                exterior @ false_offset @ exterior
            ),
            "corrected_exterior_frobenius_norm": self._norm(
                exterior @ extracted @ exterior
            ),
            "corrected_cross_coupling_frobenius_norm": float(
                np.sqrt(
                    self._norm(core_projector @ extracted @ exterior) ** 2
                    + self._norm(exterior @ extracted @ core_projector) ** 2
                )
            ),
            "compact_planted_blocks": self._compact_blocks(
                defect,
                canonical_basis.cell_count,
                canonical_basis.orbital_count * spin_count,
            ),
            "alignment_parameters": {
                "translation_cells": specification.alignment.translation_cells,
                "orbital_permutation": list(
                    specification.alignment.orbital_permutation
                ),
                "orbital_rotation_angle_radians": (
                    specification.alignment.orbital_rotation_angle
                ),
                "orbital_phases_radians": list(specification.alignment.orbital_phases),
                "site_phase_step_radians": specification.alignment.site_phase_step,
                "spin_rotation_axis": list(specification.alignment.spin_axis),
                "spin_rotation_angle_radians": (
                    specification.alignment.spin_rotation_angle
                ),
            },
        }

    def _planted_defects(
        self, control: ExtractionControl, size: int
    ) -> dict[str, ComplexMatrix]:
        dimension = 2 * size
        scalar = np.zeros((dimension, dimension), dtype=np.complex128)
        scalar[:2, :2] = control.scalar_onsite_strength * np.eye(2)
        orbital = np.zeros_like(scalar)
        orbital[:2, :2] = np.asarray(control.orbital_onsite, dtype=np.complex128)
        nearest = np.zeros_like(scalar)
        nearest_block = np.asarray(control.nearest_neighbor, dtype=np.complex128)
        nearest[:2, 2:4] = nearest_block
        nearest[2:4, :2] = nearest_block.conj().T
        range_two = np.zeros_like(scalar)
        range_two_block = np.asarray(control.range_two, dtype=np.complex128)
        range_two[:2, 4:6] = range_two_block
        range_two[4:6, :2] = range_two_block.conj().T
        identity_spin = np.eye(2, dtype=np.complex128)
        pauli_x, pauli_y, pauli_z = self._pauli()
        collinear = np.zeros((2 * dimension, 2 * dimension), dtype=np.complex128)
        collinear[:4, :4] = np.kron(
            np.asarray(control.collinear_independent, dtype=np.complex128),
            identity_spin,
        ) + np.kron(
            np.asarray(control.collinear_splitting, dtype=np.complex128),
            pauli_z,
        )
        spin_mixing = np.zeros_like(collinear)
        spin_mixing[:4, :4] = np.kron(
            np.asarray(control.collinear_independent, dtype=np.complex128),
            identity_spin,
        )
        for block, pauli in zip(
            (control.spin_x, control.spin_y, control.spin_z),
            (pauli_x, pauli_y, pauli_z),
            strict=True,
        ):
            spin_mixing[:4, :4] += np.kron(
                np.asarray(block, dtype=np.complex128), pauli
            )
        return {
            "scalar-onsite": scalar,
            "orbital-onsite": orbital,
            "nearest-neighbor": nearest,
            "range-two-nonlocal": range_two,
            "collinear-spin": collinear,
            "spin-mixing": spin_mixing,
        }

    def _spinless_model_hierarchy(
        self,
        identifier: str,
        defect: ComplexMatrix,
        size: int,
        specification: DefectExerciseInput,
    ) -> dict[str, JsonValue]:
        central = defect[:2, :2]
        scalar = np.zeros_like(defect)
        scalar[:2, :2] = 0.5 * np.trace(central) * np.eye(2)
        orbital = np.zeros_like(defect)
        orbital[:2, :2] = central
        range_one = orbital.copy()
        range_two = orbital.copy()
        for site in range(1, size):
            distance = min(site, size - site)
            block = defect[:2, 2 * site : 2 * site + 2]
            reverse = defect[2 * site : 2 * site + 2, :2]
            if distance <= 1:
                range_one[:2, 2 * site : 2 * site + 2] = block
                range_one[2 * site : 2 * site + 2, :2] = reverse
            if distance <= 2:
                range_two[:2, 2 * site : 2 * site + 2] = block
                range_two[2 * site : 2 * site + 2, :2] = reverse
        classes = (
            ("scalar-onsite", scalar),
            ("orbital-onsite", orbital),
            ("range-1-nonlocal", range_one),
            ("range-2-nonlocal", range_two),
        )
        records: list[JsonValue] = []
        first_adequate: str | None = None
        for class_id, model in classes:
            residual = self._norm(defect - model)
            if first_adequate is None and residual <= specification.algebraic_tolerance:
                first_adequate = class_id
            records.append(
                {
                    "class_id": class_id,
                    "absolute_frobenius_residual": residual,
                    "relative_frobenius_residual": self._relative_norm(
                        defect - model, defect
                    ),
                    "model_operator_sha256": self._matrix_sha256(model),
                }
            )
        return {
            "defect_id": identifier,
            "hierarchy": records,
            "first_adequate_class": first_adequate,
        }

    def _spin_model_hierarchy(
        self,
        identifier: str,
        defect: ComplexMatrix,
        size: int,
        specification: DefectExerciseInput,
    ) -> dict[str, JsonValue]:
        block = defect[:4, :4].reshape(2, 2, 2, 2)
        pauli_x, pauli_y, pauli_z = self._pauli()
        identity = np.eye(2, dtype=np.complex128)
        spin_matrices = (identity, pauli_x, pauli_y, pauli_z)
        coefficients: list[ComplexMatrix] = []
        for spin_matrix in spin_matrices:
            coefficient = np.zeros((2, 2), dtype=np.complex128)
            for first in range(2):
                for second in range(2):
                    coefficient += (
                        0.5 * spin_matrix[second, first] * block[:, first, :, second]
                    )
            coefficients.append(coefficient)
        independent_block = np.kron(coefficients[0], identity)
        collinear_block = independent_block + np.kron(coefficients[3], pauli_z)
        spinor_block = sum(
            (
                np.kron(coefficient, spin_matrix)
                for coefficient, spin_matrix in zip(
                    coefficients, spin_matrices, strict=True
                )
            ),
            start=np.zeros((4, 4), dtype=np.complex128),
        )
        classes: list[tuple[str, ComplexMatrix]] = []
        for class_id, central_block in (
            ("spin-independent-onsite", independent_block),
            ("collinear-onsite", collinear_block),
            ("spinor-onsite", spinor_block),
        ):
            model = np.zeros((4 * size, 4 * size), dtype=np.complex128)
            model[:4, :4] = central_block
            classes.append((class_id, model))
        records: list[JsonValue] = []
        first_adequate: str | None = None
        for class_id, model in classes:
            residual = self._norm(defect - model)
            if first_adequate is None and residual <= specification.algebraic_tolerance:
                first_adequate = class_id
            records.append(
                {
                    "class_id": class_id,
                    "absolute_frobenius_residual": residual,
                    "relative_frobenius_residual": self._relative_norm(
                        defect - model, defect
                    ),
                    "model_operator_sha256": self._matrix_sha256(model),
                }
            )
        return {
            "defect_id": identifier,
            "hierarchy": records,
            "first_adequate_class": first_adequate,
        }

    def _stopping_controls(
        self, pristine: ComplexMatrix, canonical_basis: SupercellBasis
    ) -> list[JsonValue]:
        reference = RepresentedOperator("reference", canonical_basis, pristine)
        variants: tuple[tuple[str, SupercellBasis, ComplexMatrix], ...] = (
            (
                "unequal-retained-rank",
                self._basis_variant(canonical_basis, orbital_count=3),
                np.zeros(
                    (
                        canonical_basis.cell_count * 3,
                        canonical_basis.cell_count * 3,
                    ),
                    dtype=np.complex128,
                ),
            ),
            (
                "mismatched-spin-space",
                self._basis_variant(canonical_basis, spin_count=2),
                np.asarray(
                    np.kron(pristine, np.eye(2, dtype=np.complex128)),
                    dtype=np.complex128,
                ),
            ),
            (
                "incorrect-supercell-shape",
                self._basis_variant(canonical_basis, geometry_id="wrong-length"),
                pristine,
            ),
            (
                "lost-site-correspondence",
                self._basis_variant(canonical_basis, site_ordering="unknown-sites"),
                pristine,
            ),
            (
                "incompatible-retained-subspace",
                self._basis_variant(canonical_basis, subspace_id="orthogonal-subspace"),
                pristine,
            ),
            (
                "different-energy-reference",
                self._basis_variant(canonical_basis, energy_reference="unknown-zero"),
                pristine,
            ),
        )
        records: list[JsonValue] = []
        for identifier, basis, matrix in variants:
            candidate = RepresentedOperator(identifier, basis, matrix)
            result = self._compatibility.execute(reference, candidate)
            records.append(
                {
                    "id": identifier,
                    "status": result.status,
                    "issue_codes": list(result.issue_codes),
                    "residual": None,
                    "retained_subspace_minimum_singular_overlap": (
                        0.0 if identifier == "incompatible-retained-subspace" else None
                    ),
                    "retained_subspace_maximum_principal_angle_radians": (
                        float(np.pi / 2.0)
                        if identifier == "incompatible-retained-subspace"
                        else None
                    ),
                }
            )
        return records

    def _finite_size_control(
        self, specification: DefectExerciseInput, parent: ParentData
    ) -> dict[str, JsonValue]:
        control = specification.finite_size
        hoppings = self._composite_hoppings(parent)
        orbital_block = np.asarray(control.orbital_block, dtype=np.complex128)
        host_edge = self._host_edge(hoppings)
        reference_size = control.supercell_sizes[-1]
        reference_defect = self._gaussian_defect(
            reference_size,
            control.gaussian_width,
            control.gaussian_strength,
            orbital_block,
        )
        reference_core = self._core_restriction(
            reference_defect, reference_size, control.core_radius, 2
        )
        records: list[JsonValue] = []
        scaled_momenta = (
            np.arange(control.momentum_mesh_size, dtype=np.float64)
            - control.momentum_mesh_size // 2
        ) / control.momentum_mesh_size
        for size in control.supercell_sizes:
            defect = self._gaussian_defect(
                size,
                control.gaussian_width,
                control.gaussian_strength,
                orbital_block,
            )
            core = self._core_restriction(defect, size, control.core_radius, 2)
            core_projector = self._site_projector(
                size,
                2,
                tuple(
                    index
                    for index, coordinate in enumerate(self._coordinates(size))
                    if abs(coordinate) <= control.core_radius
                ),
            )
            exterior = np.eye(2 * size) - core_projector
            energies: list[float] = []
            for scaled_momentum in scaled_momenta:
                momentum = float(scaled_momentum) / size
                hamiltonian = (
                    self._supercell_hamiltonian(hoppings, size, momentum) + defect
                )
                energies.append(float(np.linalg.eigvalsh(hamiltonian)[0]))
            zero_hamiltonian = self._supercell_hamiltonian(hoppings, size, 0.0) + defect
            zero_values, zero_vectors = np.linalg.eigh(zero_hamiltonian)
            bound_count = int(
                np.sum(
                    zero_values < host_edge - specification.bound_threshold_tolerance
                )
            )
            probability = np.sum(
                np.abs(zero_vectors[:, 0].reshape(size, 2)) ** 2, axis=1
            )
            coordinates = self._coordinates(size).astype(np.float64)
            records.append(
                {
                    "supercell_size": size,
                    "defect_operator_sha256": self._matrix_sha256(defect),
                    "core_restriction_frobenius_defect_from_largest": self._norm(
                        core - reference_core
                    ),
                    "exterior_frobenius_norm": self._norm(exterior @ defect @ exterior),
                    "cross_coupling_frobenius_norm": float(
                        np.sqrt(
                            self._norm(core_projector @ defect @ exterior) ** 2
                            + self._norm(exterior @ defect @ core_projector) ** 2
                        )
                    ),
                    "host_lower_band_edge": host_edge,
                    "lowest_defect_band_center": float(np.mean(energies)),
                    "lowest_defect_band_minimum": min(energies),
                    "lowest_defect_band_maximum": max(energies),
                    "lowest_defect_band_width": float(np.ptp(energies)),
                    "center_binding_relative_to_host_edge": host_edge
                    - float(np.mean(energies)),
                    "bound_state_count_at_zero_momentum": bound_count,
                    "lowest_state_inverse_participation_ratio": float(
                        np.sum(probability**2)
                    ),
                    "lowest_state_core_probability": float(
                        np.sum(probability[np.abs(coordinates) <= control.core_radius])
                    ),
                    "lowest_state_rms_radius_cells": float(
                        np.sqrt(np.sum(probability * coordinates**2))
                    ),
                }
            )
        return {
            "profile": {
                "family": "fixed-peak Gaussian onsite",
                "width_cells": control.gaussian_width,
                "strength": control.gaussian_strength,
                "orbital_block": [list(row) for row in control.orbital_block],
                "core_radius_cells": control.core_radius,
            },
            "records": records,
        }

    def _smoothness_control(
        self, specification: DefectExerciseInput, parent: ParentData
    ) -> tuple[
        dict[str, JsonValue], tuple[ComplexMatrix, ComplexMatrix, float, RealVector]
    ]:
        control = specification.smoothness
        size = control.supercell_size
        representatives = np.asarray(
            [value[0] for value in parent.scalar_hoppings], dtype=np.int64
        )
        hoppings = np.asarray(
            [value[1] for value in parent.scalar_hoppings], dtype=np.complex128
        )
        coordinates = self._coordinates(size).astype(np.float64)
        momenta = np.fft.fftfreq(size)
        fourier = np.exp(
            2j * np.pi * np.outer(np.arange(size, dtype=np.float64), momenta)
        ) / np.sqrt(size)
        lattice_energies = np.asarray(
            [
                np.sum(hoppings * np.exp(2j * np.pi * momentum * representatives)).real
                for momentum in momenta
            ],
            dtype=np.float64,
        )
        edge = float(np.sum(hoppings).real)
        curvature = float(
            0.5 * np.sum(-np.square(2.0 * np.pi * representatives) * hoppings).real
        )
        if curvature <= 0.0:
            raise ValueError("accepted scalar parent must have positive edge curvature")
        continuum_energies = edge + curvature * np.square(momenta)
        lattice_parent = fourier @ np.diag(lattice_energies) @ fourier.conj().T
        continuum_parent = fourier @ np.diag(continuum_energies) @ fourier.conj().T
        families: list[JsonValue] = []
        contrast_profile = np.zeros(size, dtype=np.float64)
        for family in ("fixed-peak", "fixed-integrated"):
            records: list[JsonValue] = []
            for width in control.widths:
                gaussian = np.exp(-np.square(coordinates) / (2.0 * width**2))
                if family == "fixed-peak":
                    profile = control.fixed_peak_strength * gaussian
                else:
                    profile = (
                        control.fixed_integrated_strength
                        / (np.sqrt(2.0 * np.pi) * width)
                        * gaussian
                    )
                lattice_values, lattice_vectors = np.linalg.eigh(
                    lattice_parent + np.diag(profile)
                )
                continuum_values, continuum_vectors = np.linalg.eigh(
                    continuum_parent + np.diag(profile)
                )
                lattice_state = lattice_vectors[:, 0]
                continuum_state = continuum_vectors[:, 0]
                momentum_amplitudes = fourier.conj().T @ lattice_state
                records.append(
                    {
                        "width_cells": width,
                        "profile_peak_magnitude": float(np.max(np.abs(profile))),
                        "profile_discrete_integrated_magnitude": float(
                            abs(np.sum(profile))
                        ),
                        "lattice_binding_energy": edge - float(lattice_values[0]),
                        "parabolic_binding_energy": edge - float(continuum_values[0]),
                        "parabolic_minus_lattice_binding_error": float(
                            lattice_values[0] - continuum_values[0]
                        ),
                        "state_fidelity": float(
                            abs(np.vdot(lattice_state, continuum_state)) ** 2
                        ),
                        "lattice_bound_state_count": int(
                            np.sum(
                                lattice_values
                                < edge - specification.bound_threshold_tolerance
                            )
                        ),
                        "parabolic_bound_state_count": int(
                            np.sum(
                                continuum_values
                                < edge - specification.bound_threshold_tolerance
                            )
                        ),
                        "lattice_high_momentum_weight": float(
                            np.sum(
                                np.abs(momentum_amplitudes[np.abs(momenta) > 0.25]) ** 2
                            )
                        ),
                        "lattice_state_rms_radius_cells": self._state_rms_radius(
                            lattice_state, coordinates
                        ),
                        "parabolic_state_rms_radius_cells": self._state_rms_radius(
                            continuum_state, coordinates
                        ),
                    }
                )
                if (
                    family == specification.metric_contrast.profile_family
                    and width == specification.metric_contrast.width
                ):
                    contrast_profile = profile.copy()
            families.append({"family": family, "records": records})
        if not np.any(contrast_profile):
            raise ValueError("metric contrast profile was not selected by the scan")
        result: dict[str, JsonValue] = {
            "supercell_size": size,
            "parent_lower_edge": edge,
            "parabolic_curvature": curvature,
            "parabolic_mass_parameter_inverse_twice_curvature": (
                1.0 / (2.0 * curvature)
            ),
            "lattice_parent_sha256": self._matrix_sha256(lattice_parent),
            "parabolic_parent_sha256": self._matrix_sha256(continuum_parent),
            "families": families,
            "interpretation": (
                "The parabolic comparator improves with profile width in the "
                "retained scan, but one fixed band-limited grid does not establish "
                "a continuum crossover."
            ),
        }
        return result, (lattice_parent, continuum_parent, edge, contrast_profile)

    def _metric_contrast_control(
        self,
        specification: DefectExerciseInput,
        smoothness_state: tuple[ComplexMatrix, ComplexMatrix, float, RealVector],
    ) -> dict[str, JsonValue]:
        lattice_parent, _, edge, profile = smoothness_state
        reference_impurity = np.diag(profile).astype(np.complex128)
        reference_hamiltonian = lattice_parent + reference_impurity
        values, vectors = np.linalg.eigh(reference_hamiltonian)
        bound_count = int(
            np.sum(values < edge - specification.bound_threshold_tolerance)
        )
        if bound_count < 1 or bound_count >= values.size:
            raise ValueError("metric contrast requires bound and unbound states")
        bound_state = vectors[:, 0]
        reference_binding = edge - float(values[0])
        high_state = vectors[:, -1]
        large_strength = specification.metric_contrast.excited_residual_strength
        large_model = reference_impurity + large_strength * np.outer(
            high_state, high_state.conj()
        )
        large_values, large_vectors = np.linalg.eigh(lattice_parent + large_model)
        first_unbound = vectors[:, bound_count]
        spectral_gap = float(values[bound_count] - values[0])
        coupling = specification.metric_contrast.coupling_to_gap_ratio * spectral_gap
        small_model = reference_impurity + coupling * (
            np.outer(bound_state, first_unbound.conj())
            + np.outer(first_unbound, bound_state.conj())
        )
        small_values, small_vectors = np.linalg.eigh(lattice_parent + small_model)
        cases = (
            (
                "large-operator-residual-excited-sector",
                large_model,
                large_values,
                large_vectors,
            ),
            (
                "small-global-residual-bound-continuum-coupling",
                small_model,
                small_values,
                small_vectors,
            ),
        )
        records: list[JsonValue] = []
        for identifier, model, model_values, model_vectors in cases:
            residual = self._norm(model - reference_impurity)
            binding = edge - float(model_values[0])
            records.append(
                {
                    "id": identifier,
                    "operator_frobenius_residual": residual,
                    "operator_residual_relative_to_full_reference_hamiltonian": (
                        residual / self._norm(reference_hamiltonian)
                    ),
                    "binding_energy": binding,
                    "binding_energy_error": binding - reference_binding,
                    "lowest_state_fidelity": float(
                        abs(np.vdot(bound_state, model_vectors[:, 0])) ** 2
                    ),
                    "bound_state_count": int(
                        np.sum(
                            model_values
                            < edge - specification.bound_threshold_tolerance
                        )
                    ),
                    "model_operator_sha256": self._matrix_sha256(model),
                }
            )
        return {
            "reference": {
                "profile_family": specification.metric_contrast.profile_family,
                "width_cells": specification.metric_contrast.width,
                "binding_energy": reference_binding,
                "bound_state_count": bound_count,
                "impurity_operator_sha256": self._matrix_sha256(reference_impurity),
            },
            "construction": {
                "excited_state_residual_strength": large_strength,
                "bound_to_first_unbound_spectral_gap": spectral_gap,
                "bound_continuum_coupling": coupling,
                "coupling_to_gap_ratio": (
                    specification.metric_contrast.coupling_to_gap_ratio
                ),
            },
            "cases": records,
        }

    @staticmethod
    def _implementation_paths() -> tuple[Path, ...]:
        package = Path(__file__).resolve().parent
        return tuple(
            package / name
            for name in ("model.py", "records.py", "operators.py", "workflows.py")
        )

    @staticmethod
    def _composite_hoppings(
        parent: ParentData,
    ) -> tuple[tuple[int, ComplexMatrix], ...]:
        return tuple(
            (representative, np.asarray(matrix, dtype=np.complex128))
            for representative, matrix in parent.composite_hoppings
        )

    @staticmethod
    def _primitive_hamiltonian(
        hoppings: tuple[tuple[int, ComplexMatrix], ...], momentum: float
    ) -> ComplexMatrix:
        result = np.zeros((2, 2), dtype=np.complex128)
        for representative, block in hoppings:
            result += np.exp(2j * np.pi * momentum * representative) * block
        return result

    @staticmethod
    def _supercell_hamiltonian(
        hoppings: tuple[tuple[int, ComplexMatrix], ...],
        size: int,
        momentum: float,
    ) -> ComplexMatrix:
        result = np.zeros((2 * size, 2 * size), dtype=np.complex128)
        for source in range(size):
            for representative, block in hoppings:
                raw_target = source + representative
                target = raw_target % size
                crossings = (raw_target - target) // size
                phase = np.exp(2j * np.pi * momentum * size * crossings)
                result[
                    2 * source : 2 * source + 2,
                    2 * target : 2 * target + 2,
                ] += phase * block
        return result

    @staticmethod
    def _folding_map(size: int, momenta: tuple[float, ...]) -> ComplexMatrix:
        result = np.zeros((2 * size, 2 * size), dtype=np.complex128)
        identity = np.eye(2, dtype=np.complex128)
        for branch, momentum in enumerate(momenta):
            for site in range(size):
                result[
                    2 * site : 2 * site + 2,
                    2 * branch : 2 * branch + 2,
                ] = np.exp(2j * np.pi * momentum * site) / np.sqrt(size) * identity
        return result

    def _alignment_map(
        self,
        size: int,
        momentum: float,
        spin_count: int,
        control: AlignmentControl,
    ) -> ComplexMatrix:
        translation = np.zeros((size, size), dtype=np.complex128)
        for source in range(size):
            raw_target = source + control.translation_cells
            target = raw_target % size
            crossings = (raw_target - target) // size
            translation[target, source] = np.exp(
                2j * np.pi * momentum * size * crossings
            )
        cosine = np.cos(control.orbital_rotation_angle)
        sine = np.sin(control.orbital_rotation_angle)
        orbital_rotation = np.asarray(
            [[cosine, -sine], [sine, cosine]], dtype=np.complex128
        )
        orbital_phases = np.diag(np.exp(1j * np.asarray(control.orbital_phases)))
        orbital_permutation = np.eye(2, dtype=np.complex128)[
            np.asarray(control.orbital_permutation, dtype=np.int64)
        ]
        site_orbital: ComplexMatrix = np.asarray(
            np.kron(
                translation,
                orbital_phases @ orbital_permutation @ orbital_rotation,
            ),
            dtype=np.complex128,
        )
        phases = np.empty(2 * size, dtype=np.complex128)
        for site in range(size):
            for orbital in range(2):
                phases[2 * site + orbital] = np.exp(
                    1j * control.site_phase_step * (site + 0.5 * orbital)
                )
        site_orbital = np.diag(phases) @ site_orbital
        if spin_count == 1:
            return site_orbital
        axis = np.asarray(control.spin_axis, dtype=np.float64)
        axis /= np.linalg.norm(axis)
        pauli_x, pauli_y, pauli_z = self._pauli()
        generator = axis[0] * pauli_x + axis[1] * pauli_y + axis[2] * pauli_z
        spin_rotation = (
            np.cos(control.spin_rotation_angle / 2.0) * np.eye(2)
            - 1j * np.sin(control.spin_rotation_angle / 2.0) * generator
        )
        return np.asarray(np.kron(site_orbital, spin_rotation), dtype=np.complex128)

    @staticmethod
    def _basis(
        size: int,
        spin_count: int,
        momentum: float,
        frame: str,
        energy_reference: str,
    ) -> SupercellBasis:
        return SupercellBasis(
            state_space_id=(
                "low-pair-orbital-supercell"
                if spin_count == 1
                else "low-pair-orbital-supercell-x-spin-half"
            ),
            cell_count=size,
            orbital_count=2,
            spin_count=spin_count,
            reduced_momentum=momentum,
            site_ordering="canonical-cyclic-sites",
            orbital_ordering="low-pair-smooth-frame",
            spin_ordering=("not-applicable" if spin_count == 1 else "up-down-fast"),
            coordinate_frame=frame,
            energy_unit="E_G",
            energy_reference=energy_reference,
            geometry_id=f"one-dimensional-supercell-{size}",
            subspace_id="accepted-low-pair-composite",
        )

    @staticmethod
    def _basis_variant(
        basis: SupercellBasis,
        *,
        orbital_count: int | None = None,
        spin_count: int | None = None,
        geometry_id: str | None = None,
        site_ordering: str | None = None,
        subspace_id: str | None = None,
        energy_reference: str | None = None,
    ) -> SupercellBasis:
        return SupercellBasis(
            state_space_id=basis.state_space_id,
            cell_count=basis.cell_count,
            orbital_count=(
                basis.orbital_count if orbital_count is None else orbital_count
            ),
            spin_count=basis.spin_count if spin_count is None else spin_count,
            reduced_momentum=basis.reduced_momentum,
            site_ordering=(
                basis.site_ordering if site_ordering is None else site_ordering
            ),
            orbital_ordering=basis.orbital_ordering,
            spin_ordering=basis.spin_ordering,
            coordinate_frame=basis.coordinate_frame,
            energy_unit=basis.energy_unit,
            energy_reference=(
                basis.energy_reference if energy_reference is None else energy_reference
            ),
            geometry_id=basis.geometry_id if geometry_id is None else geometry_id,
            subspace_id=basis.subspace_id if subspace_id is None else subspace_id,
        )

    @staticmethod
    def _gaussian_defect(
        size: int, width: float, strength: float, orbital_block: ComplexMatrix
    ) -> ComplexMatrix:
        coordinates = MatchedDefectExtractionExperiment._coordinates(size)
        profile = strength * np.exp(-np.square(coordinates) / (2.0 * width**2))
        result = np.zeros((2 * size, 2 * size), dtype=np.complex128)
        for site, value in enumerate(profile):
            result[2 * site : 2 * site + 2, 2 * site : 2 * site + 2] = (
                value * orbital_block
            )
        return result

    @staticmethod
    def _coordinates(size: int) -> npt.NDArray[np.int64]:
        values = np.arange(size, dtype=np.int64)
        return np.where(values <= size // 2, values, values - size)

    @staticmethod
    def _site_projector(
        size: int, block_size: int, sites: tuple[int, ...]
    ) -> ComplexMatrix:
        result = np.zeros((size * block_size, size * block_size), dtype=np.complex128)
        for site in sites:
            begin = block_size * site
            result[begin : begin + block_size, begin : begin + block_size] = np.eye(
                block_size
            )
        return result

    @staticmethod
    def _core_restriction(
        matrix: ComplexMatrix, size: int, radius: int, block_size: int
    ) -> ComplexMatrix:
        coordinates = MatchedDefectExtractionExperiment._coordinates(size)
        ordered_sites = tuple(
            int(np.flatnonzero(coordinates == coordinate)[0])
            for coordinate in range(-radius, radius + 1)
        )
        indices = np.asarray(
            [
                block_size * site + internal
                for site in ordered_sites
                for internal in range(block_size)
            ],
            dtype=np.int64,
        )
        return matrix[np.ix_(indices, indices)]

    @staticmethod
    def _compact_blocks(
        matrix: ComplexMatrix, size: int, block_size: int
    ) -> list[JsonValue]:
        records: list[JsonValue] = []
        for first in range(size):
            for second in range(size):
                block = matrix[
                    block_size * first : block_size * (first + 1),
                    block_size * second : block_size * (second + 1),
                ]
                if np.any(block != 0.0):
                    records.append(
                        {
                            "row_site": first,
                            "column_site": second,
                            "matrix": (
                                MatchedDefectExtractionExperiment._complex_matrix_json(
                                    block
                                )
                            ),
                        }
                    )
        return records

    @staticmethod
    def _complex_matrix_json(matrix: ComplexMatrix) -> list[JsonValue]:
        return [
            [[float(value.real), float(value.imag)] for value in row] for row in matrix
        ]

    @staticmethod
    def _host_edge(
        hoppings: tuple[tuple[int, ComplexMatrix], ...],
    ) -> float:
        momenta = np.linspace(-0.5, 0.5, 4096, endpoint=False)
        return min(
            float(
                np.linalg.eigvalsh(
                    MatchedDefectExtractionExperiment._primitive_hamiltonian(
                        hoppings, momentum
                    )
                )[0]
            )
            for momentum in momenta
        )

    @staticmethod
    def _state_rms_radius(state: ComplexVector, coordinates: RealVector) -> float:
        probabilities = np.abs(state) ** 2
        return float(np.sqrt(np.sum(probabilities * np.square(coordinates))))

    @staticmethod
    def _reduce_momentum(momentum: float) -> float:
        return float((momentum + 0.5) % 1.0 - 0.5)

    @staticmethod
    def _pauli() -> tuple[ComplexMatrix, ComplexMatrix, ComplexMatrix]:
        return (
            np.asarray([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128),
            np.asarray([[0.0, -1j], [1j, 0.0]], dtype=np.complex128),
            np.asarray([[1.0, 0.0], [0.0, -1.0]], dtype=np.complex128),
        )

    @staticmethod
    def _relative_norm(difference: ComplexMatrix, reference: ComplexMatrix) -> float:
        scale = float(np.linalg.norm(reference))
        if scale == 0.0:
            return 0.0 if np.linalg.norm(difference) == 0.0 else float("inf")
        return float(np.linalg.norm(difference) / scale)

    @staticmethod
    def _matrix_sha256(matrix: ComplexMatrix) -> str:
        canonical = np.stack((matrix.real, matrix.imag), axis=-1).astype(
            "<f8", copy=True
        )
        canonical[canonical == 0.0] = 0.0
        return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()

    @staticmethod
    def _norm(matrix: ComplexMatrix) -> float:
        return float(np.linalg.norm(matrix))

    @staticmethod
    def _maximum(matrix: ComplexMatrix) -> float:
        return float(np.max(np.abs(matrix)))

    @staticmethod
    def _eigenvalue_defect(first: ComplexMatrix, second: ComplexMatrix) -> float:
        return float(
            np.max(np.abs(np.linalg.eigvalsh(first) - np.linalg.eigvalsh(second)))
        )

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()
