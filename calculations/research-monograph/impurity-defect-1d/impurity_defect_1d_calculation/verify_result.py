"""Independently verify the retained one-dimensional defect result."""

from __future__ import annotations

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
type ComplexVector = npt.NDArray[np.complex128]
type RealVector = npt.NDArray[np.float64]

LEGACY_RUNNER_SHA256 = (
    "ba373a8ccdc87c265040f240a057d63afa73bfacb0d4ca2f58e8e7311612e7ba"
)


class DefectResultVerifier:
    """Reconstruct retained controls without importing the calculation runner."""

    __slots__ = ()

    def execute(self, result_path: Path, repository_root: Path) -> None:
        result = self._load(result_path, "result")
        if self._integer(result["schema_version"], "schema_version") != 1:
            raise ValueError("unsupported result schema version")
        if result["evidence_status"] != "synthetic test data":
            raise ValueError("result evidence status mismatch")
        if (
            result["calculation_status"]
            != "calculated synthetic numerical-verification result"
        ):
            raise ValueError("result calculation status mismatch")
        provenance = self._mapping(result["provenance"], "provenance")
        input_path = repository_root / self._string(
            provenance["input_path"], "input_path"
        )
        script_path = repository_root / self._string(
            provenance["script_path"], "script_path"
        )
        self._assert_text(
            self._sha256(input_path), provenance["input_sha256"], "input sha256"
        )
        recorded_script_sha256 = self._string(
            provenance["script_sha256"], "script sha256"
        )
        implementation_identities = provenance.get("implementation_identities")
        if implementation_identities is None:
            self._assert_text(
                LEGACY_RUNNER_SHA256,
                recorded_script_sha256,
                "historical script sha256",
            )
        else:
            if (
                not isinstance(implementation_identities, list)
                or len(implementation_identities) != 4
            ):
                raise ValueError("four implementation identities are required")
            self._assert_text(
                self._sha256(script_path),
                recorded_script_sha256,
                "script sha256",
            )
            for value in implementation_identities:
                identity = self._mapping(value, "implementation identity")
                implementation_path = repository_root / self._string(
                    identity["path"], "implementation path"
                )
                self._assert_text(
                    self._sha256(implementation_path),
                    identity["sha256"],
                    "implementation sha256",
                )
        source = self._load(input_path, "input")
        tolerance = self._real(source["algebraic_tolerance"], "tolerance")
        threshold = self._real(source["bound_state_threshold_tolerance"], "threshold")
        composite, scalar = self._load_parents(source, result, repository_root)
        self._verify_folding(source, result, composite, tolerance)
        self._verify_extraction(source, result, composite, tolerance)
        self._verify_stops(result)
        self._verify_finite_size(source, result, composite, threshold)
        smoothness_state = self._verify_smoothness(source, result, scalar, threshold)
        self._verify_metric_contrast(source, result, smoothness_state, threshold)
        limitations = result["limitations"]
        if not isinstance(limitations, list) or len(limitations) != 4:
            raise ValueError("four explicit limitations are required")

    def _load_parents(
        self,
        source: dict[str, JsonValue],
        result: dict[str, JsonValue],
        repository_root: Path,
    ) -> tuple[tuple[tuple[int, ComplexMatrix], ...], tuple[tuple[int, complex], ...]]:
        parent_source = self._mapping(source["parent_sources"], "parent_sources")
        isolated_path = repository_root / self._string(
            parent_source["isolated_band_result_path"], "isolated path"
        )
        composite_path = repository_root / self._string(
            parent_source["composite_result_path"], "composite path"
        )
        isolated_digest = self._string(
            parent_source["isolated_band_result_sha256"], "isolated sha256"
        )
        composite_digest = self._string(
            parent_source["composite_result_sha256"], "composite sha256"
        )
        self._assert_text(self._sha256(isolated_path), isolated_digest, "isolated")
        self._assert_text(self._sha256(composite_path), composite_digest, "composite")
        retained_parent = self._mapping(result["parent"], "retained parent")
        identities = self._records(
            retained_parent["source_identities"], "source identities"
        )
        retained = {
            self._string(item["path"], "source path"): self._string(
                item["sha256"], "source sha256"
            )
            for item in identities
        }
        expected = {
            isolated_path.relative_to(repository_root).as_posix(): isolated_digest,
            composite_path.relative_to(repository_root).as_posix(): composite_digest,
        }
        if retained != expected:
            raise ValueError("retained parent identities do not match input")
        isolated = self._load(isolated_path, "isolated parent")
        reduction = self._mapping(
            isolated["isolated_band_reduction"], "isolated reduction"
        )
        representatives = self._integers(
            reduction["hopping_representatives_cells"], "scalar representatives"
        )
        scalar_values = self._complexes(
            reduction["hopping_coefficients"], "scalar values"
        )
        scalar = tuple(sorted(zip(representatives, scalar_values, strict=True)))
        composite_payload = self._load(composite_path, "composite parent")
        group_id = self._string(parent_source["composite_group_id"], "group id")
        groups = self._records(composite_payload["groups"], "groups")
        groups_by_id = {
            self._string(group["id"], "group id"): group for group in groups
        }
        group = groups_by_id[group_id]
        hopping_range = self._integer(
            parent_source["parent_hopping_range_cells"], "hopping range"
        )
        blocks: list[tuple[int, ComplexMatrix]] = []
        for record in self._records(
            group["smooth_hopping_blocks"], "smooth hopping blocks"
        ):
            representative = self._integer(
                record["representative_cells"], "representative"
            )
            if abs(representative) <= hopping_range:
                blocks.append(
                    (
                        representative,
                        self._complex_matrix(record["matrix"], "hopping matrix"),
                    )
                )
        blocks.sort(key=lambda item: item[0])
        if tuple(item[0] for item in blocks) != tuple(
            range(-hopping_range, hopping_range + 1)
        ):
            raise ValueError("parent composite range is incomplete")
        return tuple(blocks), scalar

    def _verify_folding(
        self,
        source: dict[str, JsonValue],
        result: dict[str, JsonValue],
        hoppings: tuple[tuple[int, ComplexMatrix], ...],
        tolerance: float,
    ) -> None:
        control = self._mapping(source["folding_control"], "folding control")
        size = self._integer(control["supercell_size"], "folding size")
        scaled_values = self._reals(
            control["reduced_momentum_times_supercell"], "folding momenta"
        )
        records = self._records(result["folding_control"], "folding records")
        if len(records) != len(scaled_values):
            raise ValueError("folding record count mismatch")
        for record, scaled in zip(records, scaled_values, strict=True):
            momentum = scaled / size
            primitive_momenta = tuple(
                self._reduce(momentum + branch / size) for branch in range(size)
            )
            transform = np.zeros((2 * size, 2 * size), dtype=np.complex128)
            for site in range(size):
                for branch, primitive_momentum in enumerate(primitive_momenta):
                    phase = np.exp(2j * np.pi * primitive_momentum * site) / np.sqrt(
                        size
                    )
                    transform[
                        2 * site : 2 * site + 2,
                        2 * branch : 2 * branch + 2,
                    ] = phase * np.eye(2)
            supercell = self._supercell(hoppings, size, momentum)
            target = np.zeros_like(supercell)
            for branch, primitive_momentum in enumerate(primitive_momenta):
                target[
                    2 * branch : 2 * branch + 2,
                    2 * branch : 2 * branch + 2,
                ] = self._primitive(hoppings, primitive_momentum)
            represented = transform.conj().T @ supercell @ transform
            mask = np.zeros_like(represented, dtype=bool)
            for branch in range(size):
                mask[2 * branch : 2 * branch + 2, 2 * branch : 2 * branch + 2] = True
            self._assert_close(record, "reduced_momentum", momentum)
            self._assert_vector(
                record["folded_primitive_momenta"], primitive_momenta, "folded momenta"
            )
            self._assert_text(
                self._digest(transform), record["folding_map_sha256"], "folding map"
            )
            self._assert_text(
                self._digest(supercell),
                record["supercell_operator_sha256"],
                "folded supercell",
            )
            self._assert_text(
                self._digest(target), record["folded_target_sha256"], "folded target"
            )
            self._assert_close(
                record,
                "folding_map_unitarity_frobenius_defect",
                self._norm(transform.conj().T @ transform - np.eye(2 * size)),
            )
            self._assert_close(
                record,
                "folded_operator_frobenius_defect",
                self._norm(represented - target),
            )
            self._assert_close(
                record,
                "folded_off_block_frobenius_norm",
                self._norm(np.where(mask, 0.0, represented)),
            )
            self._assert_close(
                record,
                "eigenvalue_maximum_absolute_defect",
                float(
                    np.max(
                        np.abs(
                            np.linalg.eigvalsh(supercell) - np.linalg.eigvalsh(target)
                        )
                    )
                ),
            )
            if (
                self._real(
                    record["folded_operator_frobenius_defect"], "folding residual"
                )
                > tolerance
            ):
                raise ValueError("folding residual exceeds algebraic tolerance")

    def _verify_extraction(
        self,
        source: dict[str, JsonValue],
        result: dict[str, JsonValue],
        hoppings: tuple[tuple[int, ComplexMatrix], ...],
        tolerance: float,
    ) -> None:
        control = self._mapping(source["extraction_control"], "extraction control")
        alignment = self._mapping(source["alignment_control"], "alignment control")
        size = self._integer(control["supercell_size"], "extraction size")
        momentum = (
            self._real(
                control["reduced_momentum_times_supercell"], "extraction momentum"
            )
            / size
        )
        pristine = self._supercell(hoppings, size, momentum)
        defects = self._defects(control, size)
        records = {
            self._string(record["id"], "extraction id"): record
            for record in self._records(
                result["extraction_controls"], "extraction records"
            )
        }
        expected_ids = {
            "null",
            "scalar-onsite",
            "orbital-onsite",
            "nearest-neighbor",
            "range-two-nonlocal",
            "collinear-spin",
            "spin-mixing",
        }
        if set(records) != expected_ids:
            raise ValueError("extraction case set mismatch")
        shift = self._real(alignment["energy_reference_shift"], "energy shift")
        for identifier in sorted(expected_ids):
            spin_count = 2 if identifier in {"collinear-spin", "spin-mixing"} else 1
            host = (
                np.asarray(np.kron(pristine, np.eye(2)), dtype=np.complex128)
                if spin_count == 2
                else pristine
            )
            defect = defects[identifier]
            coordinate_map = self._alignment(size, momentum, spin_count, alignment)
            raw = coordinate_map @ (
                host + defect
            ) @ coordinate_map.conj().T + shift * np.eye(host.shape[0])
            aligned = (
                coordinate_map.conj().T
                @ (raw - shift * np.eye(raw.shape[0]))
                @ coordinate_map
            )
            extracted = aligned - host
            wrong = coordinate_map.conj().T @ raw @ coordinate_map - host
            false_offset = wrong - defect
            projector = np.zeros_like(host)
            block_size = 2 * spin_count
            projector[:block_size, :block_size] = np.eye(block_size)
            exterior = np.eye(host.shape[0]) - projector
            record = records[identifier]
            self._assert_text(
                self._digest(defect), record["planted_operator_sha256"], "planted"
            )
            self._assert_text(self._digest(raw), record["raw_operator_sha256"], "raw")
            self._assert_text(
                self._digest(coordinate_map),
                record["alignment_map_sha256"],
                "alignment map",
            )
            self._assert_text(
                self._digest(extracted),
                record["extracted_operator_sha256"],
                "extracted",
            )
            expected_issues = {
                "DEFECT.COMPATIBILITY.COORDINATE_FRAME",
                "DEFECT.COMPATIBILITY.ENERGY_REFERENCE",
                "DEFECT.COMPATIBILITY.ORBITAL_ORDER",
                "DEFECT.COMPATIBILITY.SITE_ORDER",
            }
            if spin_count == 2:
                expected_issues.add("DEFECT.COMPATIBILITY.SPIN_ORDER")
            issue_values = record["direct_comparison_issue_codes"]
            if (
                not isinstance(issue_values, list)
                or set(issue_values) != expected_issues
            ):
                raise ValueError(f"{identifier}: direct comparison issues mismatch")
            if record["direct_comparison_status"] != "stopped":
                raise ValueError(f"{identifier}: raw comparison must stop")
            expected_scalars = {
                "alignment_map_unitarity_frobenius_defect": self._norm(
                    coordinate_map.conj().T @ coordinate_map - np.eye(host.shape[0])
                ),
                "raw_coordinate_difference_frobenius_not_interpreted": self._norm(
                    raw - host
                ),
                "aligned_extraction_frobenius_defect": self._norm(extracted - defect),
                "aligned_extraction_maximum_absolute_defect": self._maximum(
                    extracted - defect
                ),
                "extracted_hermiticity_maximum_absolute_residual": self._maximum(
                    extracted - extracted.conj().T
                ),
                "uncorrected_false_offset_frobenius_norm": self._norm(false_offset),
                "uncorrected_false_offset_exterior_frobenius_norm": self._norm(
                    exterior @ false_offset @ exterior
                ),
                "corrected_exterior_frobenius_norm": self._norm(
                    exterior @ extracted @ exterior
                ),
                "corrected_cross_coupling_frobenius_norm": float(
                    np.sqrt(
                        self._norm(projector @ extracted @ exterior) ** 2
                        + self._norm(exterior @ extracted @ projector) ** 2
                    )
                ),
            }
            for field, expected in expected_scalars.items():
                self._assert_close(record, field, expected)
            compact = self._rebuild_compact(
                record["compact_planted_blocks"], size, block_size
            )
            np.testing.assert_allclose(compact, defect, rtol=0.0, atol=0.0)
            if (
                self._real(
                    record["aligned_extraction_frobenius_defect"], "extraction residual"
                )
                > tolerance
            ):
                raise ValueError(f"{identifier}: extraction residual exceeds tolerance")
        self._verify_model_hierarchy(source, result, defects)

    def _verify_model_hierarchy(
        self,
        source: dict[str, JsonValue],
        result: dict[str, JsonValue],
        defects: dict[str, ComplexMatrix],
    ) -> None:
        control = self._mapping(source["extraction_control"], "extraction control")
        size = self._integer(control["supercell_size"], "extraction size")
        records = {
            self._string(item["defect_id"], "model defect id"): item
            for item in self._records(
                result["model_class_hierarchy"], "model hierarchy"
            )
        }
        expected_first = {
            "scalar-onsite": "scalar-onsite",
            "orbital-onsite": "orbital-onsite",
            "nearest-neighbor": "range-1-nonlocal",
            "range-two-nonlocal": "range-2-nonlocal",
            "collinear-spin": "collinear-onsite",
            "spin-mixing": "spinor-onsite",
        }
        if set(records) != set(expected_first):
            raise ValueError("model hierarchy case set mismatch")
        for identifier, first_class in expected_first.items():
            record = records[identifier]
            self._assert_text(
                first_class, record["first_adequate_class"], "first class"
            )
            defect = defects[identifier]
            models = self._models(identifier, defect, size)
            retained_classes = self._records(record["hierarchy"], "class hierarchy")
            if len(retained_classes) != len(models):
                raise ValueError(f"{identifier}: model class count mismatch")
            for retained, (class_id, model) in zip(
                retained_classes, models, strict=True
            ):
                self._assert_text(class_id, retained["class_id"], "class id")
                residual = self._norm(defect - model)
                relative = (
                    0.0 if self._norm(defect) == 0.0 else residual / self._norm(defect)
                )
                self._assert_close(retained, "absolute_frobenius_residual", residual)
                self._assert_close(retained, "relative_frobenius_residual", relative)
                self._assert_text(
                    self._digest(model),
                    retained["model_operator_sha256"],
                    "model digest",
                )

    def _verify_stops(self, result: dict[str, JsonValue]) -> None:
        expected = {
            "unequal-retained-rank": {
                "DEFECT.COMPATIBILITY.DIMENSION",
                "DEFECT.COMPATIBILITY.ORBITAL_COUNT",
            },
            "mismatched-spin-space": {
                "DEFECT.COMPATIBILITY.DIMENSION",
                "DEFECT.COMPATIBILITY.SPIN_COUNT",
            },
            "incorrect-supercell-shape": {"DEFECT.COMPATIBILITY.GEOMETRY"},
            "lost-site-correspondence": {"DEFECT.COMPATIBILITY.SITE_ORDER"},
            "incompatible-retained-subspace": {"DEFECT.COMPATIBILITY.SUBSPACE"},
            "different-energy-reference": {"DEFECT.COMPATIBILITY.ENERGY_REFERENCE"},
        }
        records = self._records(result["stopping_controls"], "stopping controls")
        if len(records) != len(expected):
            raise ValueError("stopping-control count mismatch")
        for record in records:
            identifier = self._string(record["id"], "stop id")
            issues = record["issue_codes"]
            if (
                identifier not in expected
                or not isinstance(issues, list)
                or set(issues) != expected[identifier]
                or record["status"] != "stopped"
                or record["residual"] is not None
            ):
                raise ValueError(f"invalid stopping control: {identifier}")
            singular_overlap = record["retained_subspace_minimum_singular_overlap"]
            principal_angle = record[
                "retained_subspace_maximum_principal_angle_radians"
            ]
            if identifier == "incompatible-retained-subspace":
                np.testing.assert_allclose(
                    self._real(singular_overlap, "singular overlap"), 0.0
                )
                np.testing.assert_allclose(
                    self._real(principal_angle, "principal angle"), np.pi / 2.0
                )
            elif singular_overlap is not None or principal_angle is not None:
                raise ValueError(f"unexpected subspace diagnostics: {identifier}")

    def _verify_finite_size(
        self,
        source: dict[str, JsonValue],
        result: dict[str, JsonValue],
        hoppings: tuple[tuple[int, ComplexMatrix], ...],
        threshold: float,
    ) -> None:
        control = self._mapping(source["finite_size_control"], "finite control")
        retained = self._mapping(result["finite_size_control"], "finite result")
        records = self._records(retained["records"], "finite records")
        sizes = self._integers(control["supercell_sizes"], "finite sizes")
        if len(records) != len(sizes):
            raise ValueError("finite-size record count mismatch")
        width = self._real(control["gaussian_width_cells"], "Gaussian width")
        strength = self._real(control["gaussian_strength"], "Gaussian strength")
        orbital = self._real_matrix(control["orbital_block"], "finite orbital")
        radius = self._integer(control["core_radius_cells"], "core radius")
        mesh_size = self._integer(control["reduced_momentum_mesh_size"], "mesh size")
        host_edge = min(
            float(np.linalg.eigvalsh(self._primitive(hoppings, momentum))[0])
            for momentum in np.linspace(-0.5, 0.5, 4096, endpoint=False)
        )
        reference = self._gaussian(sizes[-1], width, strength, orbital)
        reference_core = self._core(reference, sizes[-1], radius, 2)
        scaled_momenta = (
            np.arange(mesh_size, dtype=np.float64) - mesh_size // 2
        ) / mesh_size
        for record, size in zip(records, sizes, strict=True):
            defect = self._gaussian(size, width, strength, orbital)
            core = self._core(defect, size, radius, 2)
            coordinates = self._coordinates(size).astype(np.float64)
            sites = tuple(
                int(index) for index in np.flatnonzero(np.abs(coordinates) <= radius)
            )
            projector = self._projector(size, 2, sites)
            exterior = np.eye(2 * size) - projector
            energies = np.asarray(
                [
                    np.linalg.eigvalsh(
                        self._supercell(hoppings, size, float(scaled) / size) + defect
                    )[0]
                    for scaled in scaled_momenta
                ],
                dtype=np.float64,
            )
            values, vectors = np.linalg.eigh(
                self._supercell(hoppings, size, 0.0) + defect
            )
            probability = np.sum(np.abs(vectors[:, 0].reshape(size, 2)) ** 2, axis=1)
            expected = {
                "core_restriction_frobenius_defect_from_largest": self._norm(
                    core - reference_core
                ),
                "exterior_frobenius_norm": self._norm(exterior @ defect @ exterior),
                "cross_coupling_frobenius_norm": float(
                    np.sqrt(
                        self._norm(projector @ defect @ exterior) ** 2
                        + self._norm(exterior @ defect @ projector) ** 2
                    )
                ),
                "host_lower_band_edge": host_edge,
                "lowest_defect_band_center": float(np.mean(energies)),
                "lowest_defect_band_minimum": float(np.min(energies)),
                "lowest_defect_band_maximum": float(np.max(energies)),
                "lowest_defect_band_width": float(np.ptp(energies)),
                "center_binding_relative_to_host_edge": host_edge
                - float(np.mean(energies)),
                "lowest_state_inverse_participation_ratio": float(
                    np.sum(probability**2)
                ),
                "lowest_state_core_probability": float(
                    np.sum(probability[np.abs(coordinates) <= radius])
                ),
                "lowest_state_rms_radius_cells": float(
                    np.sqrt(np.sum(probability * coordinates**2))
                ),
            }
            if self._integer(record["supercell_size"], "finite size") != size:
                raise ValueError("finite-size sequence mismatch")
            self._assert_text(
                self._digest(defect),
                record["defect_operator_sha256"],
                "finite defect",
            )
            for field, value in expected.items():
                self._assert_close(record, field, value)
            count = int(np.sum(values < host_edge - threshold))
            if (
                self._integer(
                    record["bound_state_count_at_zero_momentum"], "bound count"
                )
                != count
            ):
                raise ValueError("finite-size bound-state count mismatch")

    def _verify_smoothness(
        self,
        source: dict[str, JsonValue],
        result: dict[str, JsonValue],
        scalar_hoppings: tuple[tuple[int, complex], ...],
        threshold: float,
    ) -> tuple[ComplexMatrix, float, RealVector]:
        control = self._mapping(source["smoothness_control"], "smoothness control")
        retained = self._mapping(result["smoothness_control"], "smoothness result")
        size = self._integer(control["supercell_size"], "smoothness size")
        widths = self._reals(control["widths_cells"], "smoothness widths")
        representatives = np.asarray(
            [item[0] for item in scalar_hoppings], dtype=np.int64
        )
        hopping_values = np.asarray(
            [item[1] for item in scalar_hoppings], dtype=np.complex128
        )
        coordinates = self._coordinates(size).astype(np.float64)
        momenta = np.fft.fftfreq(size)
        transform = np.exp(
            2j * np.pi * np.outer(np.arange(size, dtype=np.float64), momenta)
        ) / np.sqrt(size)
        lattice_energies = np.asarray(
            [
                np.sum(
                    hopping_values * np.exp(2j * np.pi * momentum * representatives)
                ).real
                for momentum in momenta
            ]
        )
        edge = float(np.sum(hopping_values).real)
        curvature = float(
            -0.5
            * np.sum(np.square(2.0 * np.pi * representatives) * hopping_values).real
        )
        continuum_energies = edge + curvature * momenta**2
        lattice_parent = transform @ np.diag(lattice_energies) @ transform.conj().T
        continuum_parent = transform @ np.diag(continuum_energies) @ transform.conj().T
        self._assert_close(retained, "parent_lower_edge", edge)
        self._assert_close(retained, "parabolic_curvature", curvature)
        self._assert_close(
            retained,
            "parabolic_mass_parameter_inverse_twice_curvature",
            1.0 / (2.0 * curvature),
        )
        self._assert_text(
            self._digest(lattice_parent),
            retained["lattice_parent_sha256"],
            "lattice parent",
        )
        self._assert_text(
            self._digest(continuum_parent),
            retained["parabolic_parent_sha256"],
            "parabolic parent",
        )
        families = self._records(retained["families"], "smoothness families")
        if len(families) != 2:
            raise ValueError("smoothness family count mismatch")
        contrast_family = self._mapping(
            source["metric_contrast_control"], "metric contrast"
        )
        selected_family = self._string(
            contrast_family["profile_family"], "contrast family"
        )
        selected_width = self._real(contrast_family["width_cells"], "contrast width")
        selected_profile = np.zeros(size, dtype=np.float64)
        for family_record, family in zip(
            families, ("fixed-peak", "fixed-integrated"), strict=True
        ):
            self._assert_text(family, family_record["family"], "family")
            records = self._records(family_record["records"], "smoothness records")
            if len(records) != len(widths):
                raise ValueError("smoothness record count mismatch")
            for record, width in zip(records, widths, strict=True):
                gaussian = np.exp(-(coordinates**2) / (2.0 * width**2))
                if family == "fixed-peak":
                    profile = (
                        self._real(control["fixed_peak_strength"], "fixed peak")
                        * gaussian
                    )
                else:
                    profile = (
                        self._real(
                            control["fixed_integrated_strength"], "fixed integrated"
                        )
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
                momentum_amplitudes = transform.conj().T @ lattice_state
                expected = {
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
                    "lattice_high_momentum_weight": float(
                        np.sum(np.abs(momentum_amplitudes[np.abs(momenta) > 0.25]) ** 2)
                    ),
                    "lattice_state_rms_radius_cells": self._rms(
                        lattice_state, coordinates
                    ),
                    "parabolic_state_rms_radius_cells": self._rms(
                        continuum_state, coordinates
                    ),
                }
                for field, value in expected.items():
                    self._assert_close(record, field, value)
                counts = (
                    int(np.sum(lattice_values < edge - threshold)),
                    int(np.sum(continuum_values < edge - threshold)),
                )
                retained_counts = (
                    self._integer(
                        record["lattice_bound_state_count"], "lattice bound count"
                    ),
                    self._integer(
                        record["parabolic_bound_state_count"],
                        "parabolic bound count",
                    ),
                )
                if counts != retained_counts:
                    raise ValueError("smoothness bound-state count mismatch")
                if family == selected_family and width == selected_width:
                    selected_profile = profile.copy()
        if not np.any(selected_profile):
            raise ValueError("metric-contrast profile missing")
        return lattice_parent, edge, selected_profile

    def _verify_metric_contrast(
        self,
        source: dict[str, JsonValue],
        result: dict[str, JsonValue],
        state: tuple[ComplexMatrix, float, RealVector],
        threshold: float,
    ) -> None:
        lattice_parent, edge, profile = state
        control = self._mapping(
            source["metric_contrast_control"], "metric contrast control"
        )
        retained = self._mapping(
            result["metric_contrast_control"], "metric contrast result"
        )
        impurity = np.diag(profile).astype(np.complex128)
        hamiltonian = lattice_parent + impurity
        values, vectors = np.linalg.eigh(hamiltonian)
        count = int(np.sum(values < edge - threshold))
        bound_state = vectors[:, 0]
        first_unbound = vectors[:, count]
        gap = float(values[count] - values[0])
        large_strength = self._real(
            control["excited_state_residual_strength"], "large strength"
        )
        ratio = self._real(
            control["bound_continuum_coupling_to_gap_ratio"], "coupling ratio"
        )
        large = impurity + large_strength * np.outer(
            vectors[:, -1], vectors[:, -1].conj()
        )
        coupling = ratio * gap
        small = impurity + coupling * (
            np.outer(bound_state, first_unbound.conj())
            + np.outer(first_unbound, bound_state.conj())
        )
        models = (
            ("large-operator-residual-excited-sector", large),
            ("small-global-residual-bound-continuum-coupling", small),
        )
        cases = self._records(retained["cases"], "metric cases")
        if len(cases) != len(models):
            raise ValueError("metric-contrast case count mismatch")
        binding = edge - float(values[0])
        reference = self._mapping(retained["reference"], "contrast reference")
        self._assert_close(reference, "binding_energy", binding)
        if self._integer(reference["bound_state_count"], "reference count") != count:
            raise ValueError("metric-contrast reference count mismatch")
        self._assert_text(
            self._digest(impurity),
            reference["impurity_operator_sha256"],
            "contrast impurity",
        )
        construction = self._mapping(retained["construction"], "construction")
        self._assert_close(construction, "bound_to_first_unbound_spectral_gap", gap)
        self._assert_close(construction, "bound_continuum_coupling", coupling)
        for record, (identifier, model) in zip(cases, models, strict=True):
            self._assert_text(identifier, record["id"], "contrast case")
            model_values, model_vectors = np.linalg.eigh(lattice_parent + model)
            residual = self._norm(model - impurity)
            model_binding = edge - float(model_values[0])
            expected = {
                "operator_frobenius_residual": residual,
                "operator_residual_relative_to_full_reference_hamiltonian": (
                    residual / self._norm(hamiltonian)
                ),
                "binding_energy": model_binding,
                "binding_energy_error": model_binding - binding,
                "lowest_state_fidelity": float(
                    abs(np.vdot(bound_state, model_vectors[:, 0])) ** 2
                ),
            }
            for field, value in expected.items():
                self._assert_close(record, field, value)
            model_count = int(np.sum(model_values < edge - threshold))
            if self._integer(record["bound_state_count"], "model count") != model_count:
                raise ValueError("metric-contrast bound-state count mismatch")
            self._assert_text(
                self._digest(model),
                record["model_operator_sha256"],
                "contrast model",
            )

    def _defects(
        self, control: dict[str, JsonValue], size: int
    ) -> dict[str, ComplexMatrix]:
        dimension = 2 * size
        zero = np.zeros((dimension, dimension), dtype=np.complex128)
        scalar = zero.copy()
        scalar[:2, :2] = self._real(
            control["scalar_onsite_strength"], "scalar onsite"
        ) * np.eye(2)
        orbital = zero.copy()
        orbital[:2, :2] = self._real_matrix(
            control["orbital_onsite_block"], "orbital onsite"
        )
        nearest = zero.copy()
        nearest_block = self._real_matrix(
            control["nearest_neighbor_block"], "nearest block"
        )
        nearest[:2, 2:4] = nearest_block
        nearest[2:4, :2] = nearest_block.T
        range_two = zero.copy()
        range_block = self._real_matrix(control["range_two_block"], "range block")
        range_two[:2, 4:6] = range_block
        range_two[4:6, :2] = range_block.T
        identity, pauli_x, pauli_y, pauli_z = self._spin_basis()
        independent = self._real_matrix(
            control["collinear_spin_independent_block"], "spin independent"
        )
        splitting = self._real_matrix(
            control["collinear_splitting_block"], "spin splitting"
        )
        collinear = np.zeros((2 * dimension, 2 * dimension), dtype=np.complex128)
        collinear[:4, :4] = np.kron(independent, identity) + np.kron(splitting, pauli_z)
        spinor = np.zeros_like(collinear)
        spinor[:4, :4] = np.kron(independent, identity)
        for key, pauli in (
            ("spin_mixing_x_block", pauli_x),
            ("spin_mixing_y_block", pauli_y),
            ("spin_mixing_z_block", pauli_z),
        ):
            spinor[:4, :4] += np.kron(self._real_matrix(control[key], key), pauli)
        return {
            "null": zero,
            "scalar-onsite": scalar,
            "orbital-onsite": orbital,
            "nearest-neighbor": nearest,
            "range-two-nonlocal": range_two,
            "collinear-spin": collinear,
            "spin-mixing": spinor,
        }

    def _models(
        self, identifier: str, defect: ComplexMatrix, size: int
    ) -> tuple[tuple[str, ComplexMatrix], ...]:
        if identifier in {"collinear-spin", "spin-mixing"}:
            block = defect[:4, :4].reshape(2, 2, 2, 2)
            identity, pauli_x, pauli_y, pauli_z = self._spin_basis()
            spin_basis = (identity, pauli_x, pauli_y, pauli_z)
            coefficients: list[ComplexMatrix] = []
            for spin_matrix in spin_basis:
                coefficient = np.zeros((2, 2), dtype=np.complex128)
                for first in range(2):
                    for second in range(2):
                        coefficient += (
                            0.5
                            * spin_matrix[second, first]
                            * block[:, first, :, second]
                        )
                coefficients.append(coefficient)
            central_blocks = (
                ("spin-independent-onsite", np.kron(coefficients[0], identity)),
                (
                    "collinear-onsite",
                    np.kron(coefficients[0], identity)
                    + np.kron(coefficients[3], pauli_z),
                ),
                (
                    "spinor-onsite",
                    sum(
                        (
                            np.kron(coefficient, spin_matrix)
                            for coefficient, spin_matrix in zip(
                                coefficients, spin_basis, strict=True
                            )
                        ),
                        start=np.zeros((4, 4), dtype=np.complex128),
                    ),
                ),
            )
            models: list[tuple[str, ComplexMatrix]] = []
            for class_id, central in central_blocks:
                model = np.zeros_like(defect)
                model[:4, :4] = central
                models.append((class_id, model))
            return tuple(models)
        central = defect[:2, :2]
        scalar = np.zeros_like(defect)
        scalar[:2, :2] = 0.5 * np.trace(central) * np.eye(2)
        orbital = np.zeros_like(defect)
        orbital[:2, :2] = central
        range_one = orbital.copy()
        range_two = orbital.copy()
        for site in range(1, size):
            distance = min(site, size - site)
            if distance <= 1:
                range_one[:2, 2 * site : 2 * site + 2] = defect[
                    :2, 2 * site : 2 * site + 2
                ]
                range_one[2 * site : 2 * site + 2, :2] = defect[
                    2 * site : 2 * site + 2, :2
                ]
            if distance <= 2:
                range_two[:2, 2 * site : 2 * site + 2] = defect[
                    :2, 2 * site : 2 * site + 2
                ]
                range_two[2 * site : 2 * site + 2, :2] = defect[
                    2 * site : 2 * site + 2, :2
                ]
        return (
            ("scalar-onsite", scalar),
            ("orbital-onsite", orbital),
            ("range-1-nonlocal", range_one),
            ("range-2-nonlocal", range_two),
        )

    def _alignment(
        self,
        size: int,
        momentum: float,
        spin_count: int,
        control: dict[str, JsonValue],
    ) -> ComplexMatrix:
        shift = self._integer(control["translation_cells"], "translation")
        translation = np.zeros((size, size), dtype=np.complex128)
        for source in range(size):
            raw_target = source + shift
            target = raw_target % size
            crossings = (raw_target - target) // size
            translation[target, source] = np.exp(
                2j * np.pi * momentum * size * crossings
            )
        angle = self._real(control["orbital_rotation_angle_radians"], "orbital angle")
        rotation = np.asarray(
            [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]],
            dtype=np.complex128,
        )
        permutation_values = self._integers(
            control["orbital_permutation"], "orbital permutation"
        )
        if tuple(sorted(permutation_values)) != (0, 1):
            raise ValueError("orbital permutation is invalid")
        permutation = np.eye(2, dtype=np.complex128)[
            np.asarray(permutation_values, dtype=np.int64)
        ]
        phase_values = np.asarray(
            self._reals(control["orbital_phases_radians"], "orbital phases")
        )
        phases = np.diag(np.exp(1j * phase_values))
        site_orbital = np.asarray(
            np.kron(translation, phases @ permutation @ rotation),
            dtype=np.complex128,
        )
        step = self._real(control["site_phase_step_radians"], "site phase")
        diagonal = np.asarray(
            [
                np.exp(1j * step * (site + 0.5 * orbital))
                for site in range(size)
                for orbital in range(2)
            ],
            dtype=np.complex128,
        )
        site_orbital = np.diag(diagonal) @ site_orbital
        if spin_count == 1:
            return site_orbital
        axis = np.asarray(
            self._reals(control["spin_rotation_axis"], "spin axis"),
            dtype=np.float64,
        )
        axis /= np.linalg.norm(axis)
        spin_angle = self._real(control["spin_rotation_angle_radians"], "spin angle")
        identity, pauli_x, pauli_y, pauli_z = self._spin_basis()
        generator = axis[0] * pauli_x + axis[1] * pauli_y + axis[2] * pauli_z
        spin_rotation = (
            np.cos(spin_angle / 2.0) * identity
            - 1j * np.sin(spin_angle / 2.0) * generator
        )
        return np.asarray(np.kron(site_orbital, spin_rotation), dtype=np.complex128)

    def _rebuild_compact(
        self, value: JsonValue, size: int, block_size: int
    ) -> ComplexMatrix:
        result = np.zeros((size * block_size, size * block_size), dtype=np.complex128)
        for record in self._records(value, "compact blocks"):
            row = self._integer(record["row_site"], "row site")
            column = self._integer(record["column_site"], "column site")
            result[
                block_size * row : block_size * (row + 1),
                block_size * column : block_size * (column + 1),
            ] = self._complex_matrix(record["matrix"], "compact matrix")
        return result

    @staticmethod
    def _primitive(
        hoppings: tuple[tuple[int, ComplexMatrix], ...], momentum: float
    ) -> ComplexMatrix:
        result = np.zeros((2, 2), dtype=np.complex128)
        for representative, block in hoppings:
            result += np.exp(2j * np.pi * momentum * representative) * block
        return result

    @staticmethod
    def _supercell(
        hoppings: tuple[tuple[int, ComplexMatrix], ...], size: int, momentum: float
    ) -> ComplexMatrix:
        result = np.zeros((2 * size, 2 * size), dtype=np.complex128)
        for first in range(size):
            for representative, block in hoppings:
                raw_second = first + representative
                second = raw_second % size
                crossings = (raw_second - second) // size
                phase = np.exp(2j * np.pi * momentum * size * crossings)
                result[
                    2 * first : 2 * first + 2,
                    2 * second : 2 * second + 2,
                ] += phase * block
        return result

    @staticmethod
    def _gaussian(
        size: int, width: float, strength: float, orbital: ComplexMatrix
    ) -> ComplexMatrix:
        coordinates = DefectResultVerifier._coordinates(size)
        profile = strength * np.exp(-(coordinates**2) / (2.0 * width**2))
        result = np.zeros((2 * size, 2 * size), dtype=np.complex128)
        for site, value in enumerate(profile):
            result[2 * site : 2 * site + 2, 2 * site : 2 * site + 2] = value * orbital
        return result

    @staticmethod
    def _coordinates(size: int) -> npt.NDArray[np.int64]:
        indices = np.arange(size, dtype=np.int64)
        return np.where(indices <= size // 2, indices, indices - size)

    @staticmethod
    def _projector(size: int, block_size: int, sites: tuple[int, ...]) -> ComplexMatrix:
        result = np.zeros((size * block_size, size * block_size), dtype=np.complex128)
        for site in sites:
            result[
                block_size * site : block_size * (site + 1),
                block_size * site : block_size * (site + 1),
            ] = np.eye(block_size)
        return result

    @staticmethod
    def _core(
        matrix: ComplexMatrix, size: int, radius: int, block_size: int
    ) -> ComplexMatrix:
        coordinates = DefectResultVerifier._coordinates(size)
        sites = tuple(
            int(np.flatnonzero(coordinates == coordinate)[0])
            for coordinate in range(-radius, radius + 1)
        )
        indices = np.asarray(
            [
                block_size * site + internal
                for site in sites
                for internal in range(block_size)
            ],
            dtype=np.int64,
        )
        return matrix[np.ix_(indices, indices)]

    @staticmethod
    def _spin_basis() -> tuple[
        ComplexMatrix, ComplexMatrix, ComplexMatrix, ComplexMatrix
    ]:
        return (
            np.eye(2, dtype=np.complex128),
            np.asarray([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128),
            np.asarray([[0.0, -1j], [1j, 0.0]], dtype=np.complex128),
            np.asarray([[1.0, 0.0], [0.0, -1.0]], dtype=np.complex128),
        )

    @staticmethod
    def _rms(state: ComplexVector, coordinates: RealVector) -> float:
        return float(np.sqrt(np.sum(np.abs(state) ** 2 * coordinates**2)))

    @staticmethod
    def _reduce(momentum: float) -> float:
        return float((momentum + 0.5) % 1.0 - 0.5)

    @staticmethod
    def _digest(matrix: ComplexMatrix) -> str:
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
    def _mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be a JSON object")
        return value

    def _records(self, value: JsonValue, name: str) -> tuple[dict[str, JsonValue], ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return tuple(self._mapping(item, name) for item in value)

    @staticmethod
    def _string(value: JsonValue, name: str) -> str:
        if not isinstance(value, str) or not value:
            raise TypeError(f"{name} must be a nonempty string")
        return value

    @staticmethod
    def _integer(value: JsonValue, name: str) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an integer")
        return value

    @staticmethod
    def _real(value: JsonValue, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be numeric")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    def _reals(self, value: JsonValue, name: str) -> tuple[float, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return tuple(self._real(item, name) for item in value)

    def _integers(self, value: JsonValue, name: str) -> tuple[int, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return tuple(self._integer(item, name) for item in value)

    def _complexes(self, value: JsonValue, name: str) -> tuple[complex, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        result: list[complex] = []
        for item in value:
            if not isinstance(item, list) or len(item) != 2:
                raise TypeError(f"{name} entries must be complex pairs")
            result.append(complex(self._real(item[0], name), self._real(item[1], name)))
        return tuple(result)

    def _real_matrix(self, value: JsonValue, name: str) -> ComplexMatrix:
        if not isinstance(value, list) or not value:
            raise TypeError(f"{name} must be a nonempty matrix")
        rows: list[list[float]] = []
        for row in value:
            if not isinstance(row, list):
                raise TypeError(f"{name} rows must be arrays")
            rows.append([self._real(item, name) for item in row])
        return np.asarray(rows, dtype=np.complex128)

    def _complex_matrix(self, value: JsonValue, name: str) -> ComplexMatrix:
        if not isinstance(value, list) or not value:
            raise TypeError(f"{name} must be a nonempty matrix")
        return np.asarray(
            [list(self._complexes(row, name)) for row in value],
            dtype=np.complex128,
        )

    @staticmethod
    def _load(path: Path, name: str) -> dict[str, JsonValue]:
        value = cast(JsonValue, json.loads(path.read_text(encoding="utf-8")))
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be a JSON object")
        return value

    def _assert_close(
        self, record: dict[str, JsonValue], field: str, expected: float
    ) -> None:
        actual = self._real(record[field], field)
        np.testing.assert_allclose(actual, expected, rtol=5.0e-13, atol=5.0e-14)

    def _assert_vector(
        self, value: JsonValue, expected: tuple[float, ...], name: str
    ) -> None:
        np.testing.assert_allclose(
            np.asarray(self._reals(value, name)),
            np.asarray(expected),
            rtol=0.0,
            atol=5.0e-15,
        )

    def _assert_text(self, expected: str, value: JsonValue, name: str) -> None:
        if self._string(value, name) != expected:
            raise ValueError(f"{name} mismatch")

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()
