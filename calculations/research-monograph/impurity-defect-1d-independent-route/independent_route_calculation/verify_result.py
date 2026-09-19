"""Independently verify the retained real-space/Bloch-fiber comparison."""

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


LEGACY_RUNNER_SHA256 = (
    "9ec2c391e4b49d859abef52249d17699173b6e7844387b3eda47e016d487839c"
)


class IndependentRouteResultVerifier:
    """Rebuild both extraction paths without importing the experiment runner."""

    __slots__ = ()

    def execute(self, result_path: Path, root: Path) -> None:
        retained = self._load(result_path)
        if self._integer(retained["schema_version"], "schema_version") != 1:
            raise ValueError("unsupported result schema")
        if retained["evidence_status"] != "synthetic test data":
            raise ValueError("evidence status mismatch")
        provenance = self._mapping(retained["provenance"], "provenance")
        input_path = root / self._string(provenance["input_path"], "input path")
        script_path = root / self._string(provenance["script_path"], "script path")
        self._assert_text(
            self._sha256(input_path), provenance["input_sha256"], "input sha256"
        )
        recorded_script_sha256 = self._string(
            provenance["script_sha256"], "script sha256"
        )
        implementation_path_value = provenance.get("implementation_path")
        implementation_sha256_value = provenance.get("implementation_sha256")
        if implementation_path_value is None and implementation_sha256_value is None:
            self._assert_text(
                LEGACY_RUNNER_SHA256,
                recorded_script_sha256,
                "historical script sha256",
            )
        else:
            self._assert_text(
                self._sha256(script_path),
                recorded_script_sha256,
                "script sha256",
            )
            implementation_path = root / self._string(
                implementation_path_value, "implementation path"
            )
            self._assert_text(
                self._sha256(implementation_path),
                implementation_sha256_value,
                "implementation sha256",
            )
        source = self._load(input_path)
        sources = self._mapping(source["baseline_sources"], "sources")
        source_records = (
            (
                self._string(sources["input_path"], "baseline input path"),
                self._string(sources["input_sha256"], "baseline input sha"),
            ),
            (
                self._string(sources["result_path"], "baseline result path"),
                self._string(sources["result_sha256"], "baseline result sha"),
            ),
            (
                self._string(sources["composite_result_path"], "composite path"),
                self._string(sources["composite_result_sha256"], "composite sha"),
            ),
        )
        for path_text, digest in source_records:
            self._assert_text(self._sha256(root / path_text), digest, path_text)
        retained_sources = self._records(
            retained["source_identities"], "source identities"
        )
        retained_identity = {
            self._string(item["path"], "identity path"): self._string(
                item["sha256"], "identity sha"
            )
            for item in retained_sources
        }
        if retained_identity != dict(source_records):
            raise ValueError("source identity set mismatch")
        baseline_input = self._load(root / source_records[0][0])
        baseline_result = self._load(root / source_records[1][0])
        composite = self._load(root / source_records[2][0])
        route = self._mapping(source["route_contract"], "route")
        cell_count = self._integer(route["supercell_size"], "cell count")
        momentum = (
            self._real(route["reduced_momentum_times_supercell"], "momentum")
            / cell_count
        )
        hopping_range = self._integer(
            route["real_space_hopping_range_cells"], "hopping range"
        )
        group_id = self._string(route["composite_group_id"], "group id")
        hoppings = self._hoppings(composite, group_id, hopping_range)
        defects = self._defects(baseline_result, cell_count)
        alignment = self._mapping(baseline_input["alignment_control"], "alignment")
        shift = self._real(alignment["energy_reference_shift"], "energy shift")
        eigenspace_tolerance = self._real(
            source["eigenspace_tolerance"], "eigenspace tolerance"
        )
        control_ids = self._strings(source["control_ids"], "control ids")
        expected_nominal: list[dict[str, JsonValue]] = []
        for identifier in control_ids:
            spin_count, plant = defects[identifier]
            transform = self._transform(cell_count, momentum, spin_count, alignment, 0)
            real_pristine = self._real_space_host(
                hoppings, cell_count, momentum, spin_count
            )
            raw_candidate = transform.conj().T @ (
                real_pristine + plant
            ) @ transform + shift * np.eye(plant.shape[0])
            aligned_real = (
                transform
                @ (raw_candidate - shift * np.eye(plant.shape[0]))
                @ transform.conj().T
            )
            extracted_real = aligned_real - real_pristine
            folding, fiber_pristine = self._fiber_host(
                hoppings, cell_count, momentum, spin_count
            )
            candidate_to_fiber = folding.conj().T @ transform
            aligned_fiber = (
                candidate_to_fiber
                @ (raw_candidate - shift * np.eye(plant.shape[0]))
                @ candidate_to_fiber.conj().T
            )
            extracted_fiber = aligned_fiber - fiber_pristine
            expected_nominal.append(
                self._comparison_record(
                    identifier,
                    spin_count,
                    plant,
                    real_pristine,
                    aligned_real,
                    extracted_real,
                    folding,
                    fiber_pristine,
                    aligned_fiber,
                    extracted_fiber,
                    eigenspace_tolerance,
                )
            )
        self._assert_records(
            self._records(retained["nominal_controls"], "nominal controls"),
            tuple(expected_nominal),
        )
        self._verify_adversarial(
            source,
            retained,
            hoppings,
            defects,
            alignment,
            cell_count,
            momentum,
            shift,
        )
        self._verify_reconciliation(
            source,
            retained,
            hoppings,
            defects,
            alignment,
            cell_count,
            shift,
            eigenspace_tolerance,
        )
        contract = self._mapping(retained["route_contract"], "route contract")
        if "Neither route imports or calls the other route" not in self._string(
            contract["implementation_independence"], "independence"
        ):
            raise ValueError("implementation-independence statement is missing")
        limitations = retained["limitations"]
        if not isinstance(limitations, list) or len(limitations) != 4:
            raise ValueError("four limitations are required")

    def _verify_adversarial(
        self,
        source: dict[str, JsonValue],
        retained: dict[str, JsonValue],
        hoppings: tuple[tuple[int, ComplexMatrix], ...],
        defects: dict[str, tuple[int, ComplexMatrix]],
        alignment: dict[str, JsonValue],
        cell_count: int,
        momentum: float,
        shift: float,
    ) -> None:
        request = self._mapping(source["adversarial_controls"], "adversarial request")
        truncation_range = self._integer(
            request["truncation_mismatch_bloch_range_cells"], "truncation range"
        )
        domain_count = self._integer(
            request["domain_mismatch_fiber_count"], "domain count"
        )
        weight_amplitude = self._real(
            request["nonuniform_weight_amplitude"], "weight amplitude"
        )
        translation_delta = self._integer(
            request["alignment_translation_delta_cells"], "translation delta"
        )
        _, plant = defects["range-two-nonlocal"]
        transform = self._transform(cell_count, momentum, 1, alignment, 0)
        real_pristine = self._real_space_host(hoppings, cell_count, momentum, 1)
        raw_candidate = transform.conj().T @ (
            real_pristine + plant
        ) @ transform + shift * np.eye(plant.shape[0])
        aligned_real = (
            transform
            @ (raw_candidate - shift * np.eye(plant.shape[0]))
            @ transform.conj().T
        )
        extracted_real = aligned_real - real_pristine
        truncated = tuple(item for item in hoppings if abs(item[0]) <= truncation_range)
        folding, truncated_pristine = self._fiber_host(
            truncated, cell_count, momentum, 1
        )
        candidate_to_fiber = folding.conj().T @ transform
        aligned_truncated = (
            candidate_to_fiber
            @ (raw_candidate - shift * np.eye(plant.shape[0]))
            @ candidate_to_fiber.conj().T
        )
        extracted_truncated = aligned_truncated - truncated_pristine
        transformed_real_pristine = folding.conj().T @ real_pristine @ folding
        transformed_real_extracted = folding.conj().T @ extracted_real @ folding
        truncation_spectral_discrepancy = self._spectral_defect(
            folding.conj().T @ aligned_real @ folding,
            aligned_truncated,
        )
        expected: tuple[dict[str, JsonValue], ...] = (
            {
                "id": "hopping-truncation-mismatch",
                "status": "noncommuting",
                "issue_codes": ["INDEPENDENT_ROUTE.HOPPING_TRUNCATION_MISMATCH"],
                "real_space_hopping_range_cells": max(
                    abs(item[0]) for item in hoppings
                ),
                "bloch_fiber_hopping_range_cells": truncation_range,
                "truncation_operator_discrepancy": self._norm(
                    truncated_pristine - transformed_real_pristine
                ),
                "route_noncommutativity_frobenius": self._norm(
                    transformed_real_extracted - extracted_truncated
                ),
                "reconstructed_spectral_maximum_absolute_discrepancy": (
                    truncation_spectral_discrepancy
                ),
                "reconciliation_id": "hopping-common-parent-reconciliation",
            },
            {
                "id": "fiber-domain-mismatch",
                "status": "stopped",
                "issue_codes": ["INDEPENDENT_ROUTE.FIBER_DOMAIN_MISMATCH"],
                "real_space_cell_count": cell_count,
                "bloch_fiber_count": domain_count,
                "extracted_operator": None,
                "reconciliation_id": "fiber-domain-common-space-reconciliation",
            },
            {
                "id": "nonuniform-fiber-weights",
                "status": "stopped",
                "issue_codes": ["INDEPENDENT_ROUTE.QUADRATURE_WEIGHT_MISMATCH"],
                "nonuniform_weight_amplitude": weight_amplitude,
                "folding_map_unitarity_defect": self._weighted_unitarity_defect(
                    folding, cell_count, weight_amplitude
                ),
                "extracted_operator": None,
                "reconciliation_id": "nonuniform-weight-dual-map-reconciliation",
            },
            {
                "id": "unmatched-alignment-map",
                "status": "stopped",
                "issue_codes": ["INDEPENDENT_ROUTE.ALIGNMENT_MAP_MISMATCH"],
                "alignment_map_frobenius_discrepancy": self._norm(
                    transform
                    - self._transform(
                        cell_count,
                        momentum,
                        1,
                        alignment,
                        translation_delta,
                    )
                ),
                "extracted_operator": None,
                "reconciliation_id": "alignment-relative-map-reconciliation",
            },
        )
        self._assert_records(
            self._records(retained["adversarial_controls"], "adversarial result"),
            expected,
        )

    def _verify_reconciliation(
        self,
        source: dict[str, JsonValue],
        retained: dict[str, JsonValue],
        hoppings: tuple[tuple[int, ComplexMatrix], ...],
        defects: dict[str, tuple[int, ComplexMatrix]],
        alignment: dict[str, JsonValue],
        nominal_cell_count: int,
        shift: float,
        eigenspace_tolerance: float,
    ) -> None:
        request = self._mapping(
            source["reconciliation_controls"], "reconciliation request"
        )
        common_range = self._integer(
            request["common_hopping_range_cells"], "common hopping range"
        )
        common_count = self._integer(
            request["common_domain_cell_count"], "common domain"
        )
        weighted_rule = self._string(
            request["weighted_fiber_coordinate_rule"], "weighted rule"
        )
        alignment_rule = self._string(request["alignment_map_rule"], "alignment rule")
        route = self._mapping(source["route_contract"], "route")
        total_momentum = self._real(
            route["reduced_momentum_times_supercell"], "total momentum"
        )
        _, full_plant = defects["range-two-nonlocal"]
        common_dimension = 2 * common_count
        excluded_norm = self._norm(full_plant[common_dimension:, :]) + self._norm(
            full_plant[:, common_dimension:]
        )
        plant = np.asarray(
            full_plant[:common_dimension, :common_dimension], dtype=np.complex128
        )
        common_momentum = total_momentum / common_count
        common_transform = self._transform(
            common_count, common_momentum, 1, alignment, 0
        )
        common_pristine = self._real_space_host(
            hoppings, common_count, common_momentum, 1
        )
        common_raw = common_transform.conj().T @ (
            common_pristine + plant
        ) @ common_transform + shift * np.eye(common_dimension)
        common_aligned = (
            common_transform
            @ (common_raw - shift * np.eye(common_dimension))
            @ common_transform.conj().T
        )
        common_extracted = common_aligned - common_pristine
        common_folding, common_fiber_pristine = self._fiber_host(
            hoppings, common_count, common_momentum, 1
        )
        common_candidate_to_fiber = common_folding.conj().T @ common_transform
        common_fiber_aligned = (
            common_candidate_to_fiber
            @ (common_raw - shift * np.eye(common_dimension))
            @ common_candidate_to_fiber.conj().T
        )
        common_fiber_extracted = common_fiber_aligned - common_fiber_pristine
        domain_record = self._comparison_record(
            "range-two-nonlocal",
            1,
            plant,
            common_pristine,
            common_aligned,
            common_extracted,
            common_folding,
            common_fiber_pristine,
            common_fiber_aligned,
            common_fiber_extracted,
            eigenspace_tolerance,
        )
        domain_record["id"] = "fiber-domain-common-space-reconciliation"
        domain_record["control_class"] = "domain-reconciliation"
        domain_record["status"] = "reconciled"
        domain_record["reconciles_issue_code"] = (
            "INDEPENDENT_ROUTE.FIBER_DOMAIN_MISMATCH"
        )
        domain_record["nominal_real_space_cell_count"] = nominal_cell_count
        domain_record["common_cell_and_fiber_count"] = common_count
        domain_record["excluded_defect_norm"] = excluded_norm

        nominal_momentum = total_momentum / nominal_cell_count
        nominal_transform = self._transform(
            nominal_cell_count, nominal_momentum, 1, alignment, 0
        )
        nominal_pristine = self._real_space_host(
            hoppings, nominal_cell_count, nominal_momentum, 1
        )
        nominal_raw = nominal_transform.conj().T @ (
            nominal_pristine + full_plant
        ) @ nominal_transform + shift * np.eye(full_plant.shape[0])
        nominal_aligned = (
            nominal_transform
            @ (nominal_raw - shift * np.eye(full_plant.shape[0]))
            @ nominal_transform.conj().T
        )
        nominal_extracted = nominal_aligned - nominal_pristine
        folding, fiber_pristine = self._fiber_host(
            hoppings, nominal_cell_count, nominal_momentum, 1
        )
        candidate_to_fiber = folding.conj().T @ nominal_transform
        fiber_aligned = (
            candidate_to_fiber
            @ (nominal_raw - shift * np.eye(full_plant.shape[0]))
            @ candidate_to_fiber.conj().T
        )

        common_hoppings = tuple(
            item for item in hoppings if abs(item[0]) <= common_range
        )
        common_parent_pristine = self._real_space_host(
            common_hoppings, nominal_cell_count, nominal_momentum, 1
        )
        common_parent_raw = nominal_transform.conj().T @ (
            common_parent_pristine + full_plant
        ) @ nominal_transform + shift * np.eye(full_plant.shape[0])
        common_parent_aligned = (
            nominal_transform
            @ (common_parent_raw - shift * np.eye(full_plant.shape[0]))
            @ nominal_transform.conj().T
        )
        common_parent_extracted = common_parent_aligned - common_parent_pristine
        common_parent_folding, common_parent_fiber_pristine = self._fiber_host(
            common_hoppings, nominal_cell_count, nominal_momentum, 1
        )
        common_parent_candidate_to_fiber = (
            common_parent_folding.conj().T @ nominal_transform
        )
        common_parent_fiber_aligned = (
            common_parent_candidate_to_fiber
            @ (common_parent_raw - shift * np.eye(full_plant.shape[0]))
            @ common_parent_candidate_to_fiber.conj().T
        )
        common_parent_fiber_extracted = (
            common_parent_fiber_aligned - common_parent_fiber_pristine
        )
        parent_record = self._comparison_record(
            "range-two-nonlocal",
            1,
            full_plant,
            common_parent_pristine,
            common_parent_aligned,
            common_parent_extracted,
            common_parent_folding,
            common_parent_fiber_pristine,
            common_parent_fiber_aligned,
            common_parent_fiber_extracted,
            eigenspace_tolerance,
        )
        parent_record["id"] = "hopping-common-parent-reconciliation"
        parent_record["control_class"] = "truncation-reconciliation"
        parent_record["status"] = "reconciled"
        parent_record["reconciles_issue_code"] = (
            "INDEPENDENT_ROUTE.HOPPING_TRUNCATION_MISMATCH"
        )
        parent_record["nominal_hopping_range_cells"] = max(
            abs(item[0]) for item in hoppings
        )
        parent_record["common_hopping_range_cells"] = common_range
        parent_record["parent_change_from_nominal_frobenius"] = self._norm(
            common_parent_pristine - nominal_pristine
        )

        adversarial = self._mapping(
            source["adversarial_controls"], "adversarial request"
        )
        amplitude = self._real(
            adversarial["nonuniform_weight_amplitude"], "weight amplitude"
        )
        weights = 1.0 + amplitude * np.cos(
            2.0 * np.pi * np.arange(nominal_cell_count) / nominal_cell_count
        )
        repeated_sqrt = np.repeat(np.sqrt(weights), 2)
        scale = np.diag(repeated_sqrt)
        scale_inverse = np.diag(1.0 / repeated_sqrt)
        weighted_synthesis = folding @ scale
        weighted_inverse = scale_inverse @ folding.conj().T
        weighted_pristine = scale_inverse @ fiber_pristine @ scale
        weighted_physical = scale_inverse @ fiber_aligned @ scale
        weighted_extracted = weighted_physical - weighted_pristine
        transformed_real = weighted_inverse @ nominal_extracted @ weighted_synthesis
        weighted_target = weighted_inverse @ full_plant @ weighted_synthesis
        metric = weighted_synthesis.conj().T @ weighted_synthesis
        identity = np.eye(weighted_synthesis.shape[0])
        weight_record: dict[str, JsonValue] = {
            "id": "nonuniform-weight-dual-map-reconciliation",
            "control_class": "quadrature-reconciliation",
            "status": "reconciled",
            "issue_codes": [],
            "reconciles_issue_code": ("INDEPENDENT_ROUTE.QUADRATURE_WEIGHT_MISMATCH"),
            "coordinate_rule": weighted_rule,
            "dimension": weighted_synthesis.shape[0],
            "minimum_weight": float(np.min(weights)),
            "maximum_weight": float(np.max(weights)),
            "weighted_synthesis_unitarity_defect": self._norm(
                weighted_synthesis.conj().T @ weighted_synthesis - identity
            ),
            "explicit_inverse_defect": self._norm(
                weighted_inverse @ weighted_synthesis - identity
            ),
            "adjoint_inverse_discrepancy": self._norm(
                weighted_synthesis.conj().T - weighted_inverse
            ),
            "induced_metric_self_adjoint_defect": self._norm(
                weighted_physical.conj().T @ metric - metric @ weighted_physical
            ),
            "route_b_planted_recovery_defect": self._norm(
                weighted_extracted - weighted_target
            ),
            "route_noncommutativity_frobenius": self._norm(
                transformed_real - weighted_extracted
            ),
        }

        translation_delta = self._integer(
            adversarial["alignment_translation_delta_cells"], "translation delta"
        )
        altered_transform = self._transform(
            nominal_cell_count,
            nominal_momentum,
            1,
            alignment,
            translation_delta,
        )
        relative = nominal_transform @ altered_transform.conj().T
        altered_physical = (
            altered_transform
            @ (nominal_raw - shift * np.eye(full_plant.shape[0]))
            @ altered_transform.conj().T
        )
        altered_pristine = relative.conj().T @ nominal_pristine @ relative
        altered_extracted = altered_physical - altered_pristine
        reconciled = relative @ altered_extracted @ relative.conj().T
        reconciled_fiber = folding.conj().T @ reconciled @ folding
        real_fiber = folding.conj().T @ nominal_extracted @ folding
        alignment_record: dict[str, JsonValue] = {
            "id": "alignment-relative-map-reconciliation",
            "control_class": "alignment-reconciliation",
            "status": "reconciled",
            "issue_codes": [],
            "reconciles_issue_code": "INDEPENDENT_ROUTE.ALIGNMENT_MAP_MISMATCH",
            "coordinate_rule": alignment_rule,
            "dimension": full_plant.shape[0],
            "relative_map_unitarity_defect": self._norm(
                relative.conj().T @ relative - identity
            ),
            "reconciled_physical_operator_defect": self._norm(
                relative @ altered_physical @ relative.conj().T - nominal_aligned
            ),
            "route_b_planted_recovery_defect": self._norm(
                reconciled_fiber - folding.conj().T @ full_plant @ folding
            ),
            "route_noncommutativity_frobenius": self._norm(
                real_fiber - reconciled_fiber
            ),
        }
        self._assert_records(
            self._records(
                retained["reconciliation_controls"], "reconciliation controls"
            ),
            (parent_record, domain_record, weight_record, alignment_record),
        )

    def _comparison_record(
        self,
        identifier: str,
        spin_count: int,
        plant: ComplexMatrix,
        real_pristine: ComplexMatrix,
        aligned_real: ComplexMatrix,
        extracted_real: ComplexMatrix,
        folding: ComplexMatrix,
        fiber_pristine: ComplexMatrix,
        aligned_fiber: ComplexMatrix,
        extracted_fiber: ComplexMatrix,
        eigenspace_tolerance: float,
    ) -> dict[str, JsonValue]:
        real_pristine_fiber = folding.conj().T @ real_pristine @ folding
        real_extracted_fiber = folding.conj().T @ extracted_real @ folding
        target_fiber = folding.conj().T @ plant @ folding
        route_defect = self._norm(real_extracted_fiber - extracted_fiber)
        target_norm = self._norm(target_fiber)
        values_a, vectors_a = np.linalg.eigh(folding.conj().T @ aligned_real @ folding)
        values_b, vectors_b = np.linalg.eigh(aligned_fiber)
        lowest_dimension = int(
            np.sum(np.abs(values_b - values_b[0]) <= eigenspace_tolerance)
        )
        projector_a = (
            vectors_a[:, :lowest_dimension] @ vectors_a[:, :lowest_dimension].conj().T
        )
        projector_b = (
            vectors_b[:, :lowest_dimension] @ vectors_b[:, :lowest_dimension].conj().T
        )
        fidelity: float | None = None
        if lowest_dimension == 1:
            fidelity = float(
                np.clip(abs(np.vdot(vectors_a[:, 0], vectors_b[:, 0])) ** 2, 0.0, 1.0)
            )
        return {
            "id": identifier,
            "control_class": self._control_class(identifier),
            "spin_count": spin_count,
            "status": "commuting",
            "issue_codes": [],
            "dimension": plant.shape[0],
            "folding_map_unitarity_defect": self._norm(
                folding.conj().T @ folding - np.eye(folding.shape[1])
            ),
            "representation_frobenius_discrepancy": self._norm(
                real_pristine_fiber - fiber_pristine
            ),
            "alignment_frobenius_defect": self._norm(
                aligned_real - (real_pristine + plant)
            ),
            "route_a_planted_recovery_defect": self._norm(extracted_real - plant),
            "route_b_planted_recovery_defect": self._norm(
                extracted_fiber - target_fiber
            ),
            "route_noncommutativity_frobenius": route_defect,
            "route_relative_noncommutativity": (
                route_defect / target_norm if target_norm > 0.0 else 0.0
            ),
            "spectral_maximum_absolute_discrepancy": float(
                np.max(np.abs(values_a - values_b))
            ),
            "lowest_eigenspace_dimension": lowest_dimension,
            "lowest_eigenspace_projector_defect": self._norm(projector_a - projector_b),
            "lowest_state_fidelity": fidelity,
            "route_a_extracted_sha256": self._matrix_sha256(extracted_real),
            "route_b_extracted_sha256": self._matrix_sha256(extracted_fiber),
            "target_fiber_sha256": self._matrix_sha256(target_fiber),
        }

    def _hoppings(
        self, composite: dict[str, JsonValue], group_id: str, hopping_range: int
    ) -> tuple[tuple[int, ComplexMatrix], ...]:
        groups = self._records(composite["groups"], "groups")
        matches = [item for item in groups if item["id"] == group_id]
        if len(matches) != 1:
            raise ValueError("composite group mismatch")
        result: list[tuple[int, ComplexMatrix]] = []
        for record in self._records(matches[0]["smooth_hopping_blocks"], "hoppings"):
            displacement = self._integer(record["representative_cells"], "displacement")
            if abs(displacement) <= hopping_range:
                result.append(
                    (
                        displacement,
                        self._complex_matrix(record["matrix"], "hopping"),
                    )
                )
        return tuple(result)

    def _defects(
        self, baseline: dict[str, JsonValue], cell_count: int
    ) -> dict[str, tuple[int, ComplexMatrix]]:
        result: dict[str, tuple[int, ComplexMatrix]] = {}
        for record in self._records(
            baseline["extraction_controls"], "extraction controls"
        ):
            identifier = self._string(record["id"], "control id")
            spin_count = self._integer(record["spin_count"], "spin count")
            result[identifier] = (
                spin_count,
                self._compact(
                    record["compact_planted_blocks"],
                    cell_count,
                    2 * spin_count,
                ),
            )
        return result

    @staticmethod
    def _real_space_host(
        hoppings: tuple[tuple[int, ComplexMatrix], ...],
        cell_count: int,
        momentum: float,
        spin_count: int,
    ) -> ComplexMatrix:
        spinless = np.zeros((2 * cell_count, 2 * cell_count), dtype=np.complex128)
        for source in range(cell_count):
            for displacement, matrix in hoppings:
                raw = source + displacement
                target = raw % cell_count
                crossings = (raw - target) // cell_count
                spinless[
                    2 * source : 2 * source + 2,
                    2 * target : 2 * target + 2,
                ] += np.exp(2j * np.pi * momentum * cell_count * crossings) * matrix
        if spin_count == 1:
            return spinless
        return np.asarray(np.kron(spinless, np.eye(2)), dtype=np.complex128)

    @staticmethod
    def _fiber_host(
        hoppings: tuple[tuple[int, ComplexMatrix], ...],
        cell_count: int,
        momentum: float,
        spin_count: int,
    ) -> tuple[ComplexMatrix, ComplexMatrix]:
        folding_spinless = np.zeros(
            (2 * cell_count, 2 * cell_count), dtype=np.complex128
        )
        pristine_spinless = np.zeros_like(folding_spinless)
        for index in range(cell_count):
            primitive_momentum = (momentum + index / cell_count) % 1.0
            fiber = sum(
                (
                    np.exp(2j * np.pi * primitive_momentum * displacement) * matrix
                    for displacement, matrix in hoppings
                ),
                start=np.zeros((2, 2), dtype=np.complex128),
            )
            begin = 2 * index
            pristine_spinless[begin : begin + 2, begin : begin + 2] = fiber
            for site in range(cell_count):
                folding_spinless[
                    2 * site : 2 * site + 2,
                    begin : begin + 2,
                ] = (
                    np.exp(2j * np.pi * primitive_momentum * site)
                    / np.sqrt(cell_count)
                    * np.eye(2)
                )
        if spin_count == 1:
            return folding_spinless, pristine_spinless
        return (
            np.asarray(np.kron(folding_spinless, np.eye(2)), dtype=np.complex128),
            np.asarray(np.kron(pristine_spinless, np.eye(2)), dtype=np.complex128),
        )

    def _transform(
        self,
        cell_count: int,
        momentum: float,
        spin_count: int,
        settings: dict[str, JsonValue],
        translation_delta: int,
    ) -> ComplexMatrix:
        cells = self._integer(settings["translation_cells"], "translation")
        cells += translation_delta
        translation = np.zeros((cell_count, cell_count), dtype=np.complex128)
        for source in range(cell_count):
            raw = source + cells
            target = raw % cell_count
            crossings = (raw - target) // cell_count
            translation[target, source] = np.exp(
                2j * np.pi * momentum * cell_count * crossings
            )
        angle = self._real(settings["orbital_rotation_angle_radians"], "angle")
        rotation = np.asarray(
            [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]],
            dtype=np.complex128,
        )
        permutation_values = self._integers(
            settings["orbital_permutation"], "permutation"
        )
        permutation = np.eye(2)[np.asarray(permutation_values, dtype=np.int64)]
        phases = np.diag(
            np.exp(
                1j
                * np.asarray(self._reals(settings["orbital_phases_radians"], "phases"))
            )
        )
        reference_to_candidate = np.asarray(
            np.kron(translation, phases @ permutation @ rotation),
            dtype=np.complex128,
        )
        phase_step = self._real(settings["site_phase_step_radians"], "phase step")
        site_phases = np.asarray(
            [
                np.exp(1j * phase_step * (site + 0.5 * orbital))
                for site in range(cell_count)
                for orbital in range(2)
            ]
        )
        reference_to_candidate = np.diag(site_phases) @ reference_to_candidate
        if spin_count == 2:
            axis = np.asarray(self._reals(settings["spin_rotation_axis"], "axis"))
            axis /= np.linalg.norm(axis)
            spin_angle = self._real(
                settings["spin_rotation_angle_radians"], "spin angle"
            )
            pauli_x = np.asarray([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)
            pauli_y = np.asarray([[0.0, -1j], [1j, 0.0]], dtype=np.complex128)
            pauli_z = np.asarray([[1.0, 0.0], [0.0, -1.0]], dtype=np.complex128)
            generator = axis[0] * pauli_x + axis[1] * pauli_y + axis[2] * pauli_z
            spin_rotation = (
                np.cos(spin_angle / 2.0) * np.eye(2)
                - 1j * np.sin(spin_angle / 2.0) * generator
            )
            reference_to_candidate = np.asarray(
                np.kron(reference_to_candidate, spin_rotation),
                dtype=np.complex128,
            )
        return reference_to_candidate.conj().T

    def _compact(self, value: JsonValue, cells: int, block: int) -> ComplexMatrix:
        result = np.zeros((cells * block, cells * block), dtype=np.complex128)
        for record in self._records(value, "compact blocks"):
            row = self._integer(record["row_site"], "row")
            column = self._integer(record["column_site"], "column")
            result[
                block * row : block * (row + 1),
                block * column : block * (column + 1),
            ] = self._complex_matrix(record["matrix"], "compact block")
        return result

    @staticmethod
    def _weighted_unitarity_defect(
        folding: ComplexMatrix, cell_count: int, amplitude: float
    ) -> float:
        weights = 1.0 + amplitude * np.cos(
            2.0 * np.pi * np.arange(cell_count) / cell_count
        )
        weighted = folding @ np.diag(np.repeat(np.sqrt(weights), 2))
        return float(
            np.linalg.norm(weighted.conj().T @ weighted - np.eye(weighted.shape[1]))
        )

    @staticmethod
    def _control_class(identifier: str) -> str:
        if identifier == "null":
            return "null"
        if identifier in {"scalar-onsite", "orbital-onsite"}:
            return "local"
        if identifier in {"nearest-neighbor", "range-two-nonlocal"}:
            return "nonlocal"
        if identifier == "collinear-spin":
            return "collinear"
        if identifier == "spin-mixing":
            return "spin-mixing"
        raise ValueError("unknown control")

    @staticmethod
    def _spectral_defect(first: ComplexMatrix, second: ComplexMatrix) -> float:
        return float(
            np.max(np.abs(np.linalg.eigvalsh(first) - np.linalg.eigvalsh(second)))
        )

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

    def _assert_records(
        self,
        actual: tuple[dict[str, JsonValue], ...],
        expected: tuple[dict[str, JsonValue], ...],
    ) -> None:
        if len(actual) != len(expected):
            raise ValueError("record count mismatch")
        for retained, reconstructed in zip(actual, expected, strict=True):
            self._assert_record(retained, reconstructed)

    def _assert_record(
        self, actual: dict[str, JsonValue], expected: dict[str, JsonValue]
    ) -> None:
        if set(actual) != set(expected):
            raise ValueError("record field set mismatch")
        for key, expected_value in expected.items():
            actual_value = actual[key]
            if isinstance(expected_value, float):
                np.testing.assert_allclose(
                    self._real(actual_value, key),
                    expected_value,
                    rtol=5.0e-12,
                    atol=5.0e-14,
                )
            elif actual_value != expected_value:
                raise ValueError(f"record mismatch: {key}")

    @staticmethod
    def _load(path: Path) -> dict[str, JsonValue]:
        value = cast(JsonValue, json.loads(path.read_text(encoding="utf-8")))
        if not isinstance(value, dict):
            raise TypeError("JSON root must be an object")
        return value

    @staticmethod
    def _mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be an object")
        return value

    def _records(self, value: JsonValue, name: str) -> tuple[dict[str, JsonValue], ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be an array")
        return tuple(self._mapping(item, name) for item in value)

    @staticmethod
    def _string(value: JsonValue, name: str) -> str:
        if not isinstance(value, str) or not value:
            raise TypeError(f"{name} must be a nonempty string")
        return value

    def _strings(self, value: JsonValue, name: str) -> tuple[str, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be an array")
        return tuple(self._string(item, name) for item in value)

    @staticmethod
    def _integer(value: JsonValue, name: str) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an integer")
        return value

    def _integers(self, value: JsonValue, name: str) -> tuple[int, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be an array")
        return tuple(self._integer(item, name) for item in value)

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
            raise TypeError(f"{name} must be an array")
        return tuple(self._real(item, name) for item in value)

    def _complex_matrix(self, value: JsonValue, name: str) -> ComplexMatrix:
        if not isinstance(value, list) or not value:
            raise TypeError(f"{name} must be a nonempty matrix")
        rows: list[list[complex]] = []
        for row in value:
            if not isinstance(row, list):
                raise TypeError(f"{name} rows must be arrays")
            parsed: list[complex] = []
            for pair in row:
                if not isinstance(pair, list) or len(pair) != 2:
                    raise TypeError(f"{name} values must be complex pairs")
                parsed.append(
                    complex(self._real(pair[0], name), self._real(pair[1], name))
                )
            rows.append(parsed)
        return np.asarray(rows, dtype=np.complex128)

    def _assert_text(self, expected: str, actual: JsonValue, name: str) -> None:
        if self._string(actual, name) != expected:
            raise ValueError(f"{name} mismatch")

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()
