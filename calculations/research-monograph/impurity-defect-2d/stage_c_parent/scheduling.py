"""Fresh-process schedule execution for accepted-parent Stage C."""

from __future__ import annotations

import json
import os
from typing import cast

import numpy as np

from .model import (
    ComplexMatrix,
    JsonValue,
    MatrixKey,
    ParentCase,
    ParentControls,
    ParentFixture,
    ParentHopping,
    ParentScheduleResult,
)
from .model_fitting import ParentModelFitter, RouteIndependenceGate
from .operator_construction import ParentHoppingConstructor, ParentMatrixConstructor


class ParentScheduleExecutor:
    """Execute one complete route order in one spawned process."""

    __slots__ = ()

    def execute(
        self,
        controls: ParentControls,
        fixture: ParentFixture,
        schedule_id: str,
        route_order: tuple[str, str],
    ) -> ParentScheduleResult:
        hopping = ParentHoppingConstructor()
        matrix = ParentMatrixConstructor()
        fitter = ParentModelFitter(matrix)
        anisotropic_full = hopping.anisotropic(fixture)
        anisotropic = hopping.compact(
            anisotropic_full, fixture.hopping_maximum_squared_radius
        )
        swapped = hopping.swapped(anisotropic)
        parents = {
            "isotropic_lambda_0p5_0p5_0": fixture.isotropic_hoppings,
            "anisotropic_lambda_0p3_0p7_0": anisotropic,
            "anisotropic_lambda_0p7_0p3_0": swapped,
        }
        preprocessing = self._preprocessing(
            controls, fixture, anisotropic_full, anisotropic, swapped
        )
        cases = self._cases(controls)
        attack = matrix.attack(controls)
        identity = np.eye(controls.dimension, dtype=np.complex128)
        route_records: list[dict[str, JsonValue]] = []
        matrices: dict[tuple[str, str, str], ComplexMatrix] = {}
        recovered_bytes: list[tuple[MatrixKey, bytes]] = []
        provenance_gate = RouteIndependenceGate()
        for route in route_order:
            provenance_gate.execute(route, "compact_parent_inputs")
            for case in cases:
                case_id = case.case_id
                base_twist = case.base_twist
                operation = case.operation
                transformed_twist_lift = matrix.transform_twist(base_twist, operation)
                transformed_twist = (
                    transformed_twist_lift
                    if route == "A_centered_uniform"
                    else matrix.reduce_twist(transformed_twist_lift)
                )
                source_twist = (
                    base_twist
                    if route == "A_centered_uniform"
                    else matrix.reduce_twist(base_twist)
                )
                source_parent_id = case.source_parent_id
                target_parent_id = case.target_parent_id
                source_terms = case.source_terms
                target_terms = tuple(
                    matrix.transform_bond(term, operation) for term in source_terms
                )
                source_parent = matrix.parent(
                    controls, parents[source_parent_id], source_twist, route
                )
                target_parent = matrix.parent(
                    controls, parents[target_parent_id], transformed_twist, route
                )
                source_defect = matrix.defect(
                    controls, source_terms, source_twist, route
                )
                target_defect = matrix.defect(
                    controls, target_terms, transformed_twist, route
                )
                source_full = source_parent + source_defect
                target_full = target_parent + target_defect
                permutation = matrix.permutation(controls, operation)
                if route == "A_centered_uniform":
                    covariance_residual = (
                        target_full - permutation @ source_full @ permutation.conj().T
                    )
                else:
                    source_gauge = matrix.gauge(controls, base_twist)
                    target_gauge = matrix.gauge(controls, transformed_twist_lift)
                    source_uniform = source_gauge.conj().T @ source_full @ source_gauge
                    target_uniform = target_gauge.conj().T @ target_full @ target_gauge
                    covariance_residual = (
                        target_uniform
                        - permutation @ source_uniform @ permutation.conj().T
                    )
                if route == "A_centered_uniform":
                    route_attack = attack
                else:
                    target_gauge = matrix.gauge(controls, transformed_twist_lift)
                    route_attack = target_gauge @ attack @ target_gauge.conj().T
                attacked = (
                    route_attack @ target_full @ route_attack.conj().T
                    + 0.137 * identity
                )
                aligned = (
                    route_attack.conj().T @ (attacked - 0.137 * identity) @ route_attack
                )
                recovered = aligned - target_parent
                recovery = recovered - target_defect
                fits: list[dict[str, JsonValue]] = []
                selected: str | None = None
                for model_class in controls.model_classes:
                    fit = fitter.execute(
                        controls,
                        recovered,
                        transformed_twist,
                        route,
                        operation,
                        model_class,
                    )
                    fits.append(fit)
                    if selected is None and fit["accepted"] is True:
                        selected = model_class
                record = {
                    "route": route,
                    "case_id": case_id,
                    "parent_family": case.parent_family,
                    "source_parent_id": source_parent_id,
                    "target_parent_id": target_parent_id,
                    "defect_id": case.defect_id,
                    "twist_id": case.twist_id,
                    "operation": operation.identifier,
                    "transformed_twist_lift": cast(
                        JsonValue, list(transformed_twist_lift)
                    ),
                    "comparison_twist": cast(JsonValue, list(transformed_twist)),
                    "parent_sha256": matrix.digest(target_parent),
                    "defect_sha256": matrix.digest(target_defect),
                    "full_sha256": matrix.digest(target_full),
                    "attacked_sha256": matrix.digest(attacked),
                    "recovered_sha256": matrix.digest(recovered),
                    "parent_hermiticity_maximum_absolute": matrix.maximum(
                        target_parent - target_parent.conj().T
                    ),
                    "defect_hermiticity_maximum_absolute": matrix.maximum(
                        target_defect - target_defect.conj().T
                    ),
                    "alignment_unitarity_maximum_absolute": matrix.maximum(
                        route_attack.conj().T @ route_attack - identity
                    ),
                    "recovery_maximum_absolute": matrix.maximum(recovery),
                    "recovery_frobenius": float(np.linalg.norm(recovery, ord="fro")),
                    "covariance_maximum_absolute": matrix.maximum(covariance_residual),
                    "covariance_frobenius": float(
                        np.linalg.norm(covariance_residual, ord="fro")
                    ),
                    "selected_model_class": selected,
                    "expected_model_class": case.expected_model_class,
                    "fits": cast(JsonValue, fits),
                }
                route_records.append(record)
                matrices[(route, case_id, "parent")] = target_parent
                matrices[(route, case_id, "defect")] = target_defect
                matrices[(route, case_id, "full")] = target_full
                matrices[(route, case_id, "attacked")] = attacked
                matrices[(route, case_id, "recovered")] = recovered
                recovered_bytes.append(
                    (
                        (route, case_id),
                        np.ascontiguousarray(recovered, dtype="<c16").tobytes(),
                    )
                )
        route_records.sort(key=self._record_key)
        bridge_records = self._bridges(controls, cases, matrices)
        adverse = self._adverse(
            controls, parents, route_records, matrix, fitter, attack
        )
        payload: dict[str, JsonValue] = {
            "schedule_id": schedule_id,
            "route_order": cast(JsonValue, list(route_order)),
            "fresh_spawned_process": True,
            "preprocessing": preprocessing,
            "route_records": cast(JsonValue, route_records),
            "bridge_records": cast(JsonValue, bridge_records),
            "adverse_controls": cast(JsonValue, adverse),
        }
        return ParentScheduleResult(
            schedule_id,
            os.getpid(),
            json.dumps(payload, sort_keys=True, separators=(",", ":")),
            tuple(sorted(recovered_bytes, key=lambda value: value[0])),
        )

    @staticmethod
    def _record_key(record: dict[str, JsonValue]) -> tuple[str, str]:
        return cast(str, record["case_id"]), cast(str, record["route"])

    def _preprocessing(
        self,
        controls: ParentControls,
        fixture: ParentFixture,
        full: tuple[ParentHopping, ...],
        compact: tuple[ParentHopping, ...],
        swapped: tuple[ParentHopping, ...],
    ) -> dict[str, JsonValue]:
        constructor = ParentHoppingConstructor()
        matrix = ParentMatrixConstructor()
        isotropic_metrics = constructor.validate(
            fixture.isotropic_hoppings, controls.d4
        )
        full_metrics = constructor.validate(full, controls.d2)
        compact_metrics = constructor.validate(compact, controls.d2)
        swapped_metrics = constructor.validate(swapped, controls.d2)
        truncation: list[JsonValue] = []
        for twist_id, twist in zip(("gamma", "generic"), controls.twists, strict=True):
            full_matrix = matrix.parent(controls, full, twist, "A_centered_uniform")
            compact_matrix = matrix.parent(
                controls, compact, twist, "A_centered_uniform"
            )
            residual = full_matrix - compact_matrix
            truncation.append(
                {
                    "twist_id": twist_id,
                    "maximum_absolute": matrix.maximum(residual),
                    "frobenius": float(np.linalg.norm(residual, ord="fro")),
                }
            )
        return {
            "fixture_sha256": fixture.fixture_sha256,
            "isotropic": isotropic_metrics,
            "pretruncation": full_metrics,
            "compact": compact_metrics,
            "axis_swapped": swapped_metrics,
            "truncation": truncation,
        }

    def _cases(self, controls: ParentControls) -> tuple[ParentCase, ...]:
        result: list[ParentCase] = []
        for defect_id, terms, expected in controls.defects:
            for twist_id, twist in zip(
                ("gamma", "generic"), controls.twists, strict=True
            ):
                for operation in controls.d4:
                    result.append(
                        ParentCase(
                            f"isotropic__{defect_id}__{twist_id}__"
                            f"{operation.identifier}",
                            "isotropic_D4",
                            "isotropic_lambda_0p5_0p5_0",
                            "isotropic_lambda_0p5_0p5_0",
                            defect_id,
                            terms,
                            expected,
                            twist_id,
                            twist,
                            operation,
                        )
                    )
                for operation in controls.d2:
                    result.append(
                        ParentCase(
                            f"anisotropic_D2__{defect_id}__{twist_id}__"
                            f"{operation.identifier}",
                            "anisotropic_D2",
                            "anisotropic_lambda_0p3_0p7_0",
                            "anisotropic_lambda_0p3_0p7_0",
                            defect_id,
                            terms,
                            expected,
                            twist_id,
                            twist,
                            operation,
                        )
                    )
                result.append(
                    ParentCase(
                        f"axis_swap__{defect_id}__{twist_id}__reflection_diagonal",
                        "anisotropic_axis_swap",
                        "anisotropic_lambda_0p3_0p7_0",
                        "anisotropic_lambda_0p7_0p3_0",
                        defect_id,
                        terms,
                        expected,
                        twist_id,
                        twist,
                        controls.axis_swap,
                    )
                )
        if len(result) != 52:
            raise ValueError("accepted-parent Stage C requires 52 cases per schedule")
        return tuple(result)

    def _bridges(
        self,
        controls: ParentControls,
        cases: tuple[ParentCase, ...],
        matrices: dict[tuple[str, str, str], ComplexMatrix],
    ) -> list[dict[str, JsonValue]]:
        matrix = ParentMatrixConstructor()
        result: list[dict[str, JsonValue]] = []
        for case in cases:
            case_id = case.case_id
            operation = case.operation
            base_twist = case.base_twist
            lift = matrix.transform_twist(base_twist, operation)
            gauge = matrix.gauge(controls, lift)
            record: dict[str, JsonValue] = {"case_id": case_id}
            for subject in ("parent", "defect", "full", "attacked", "recovered"):
                route_a = matrices[("A_centered_uniform", case_id, subject)]
                route_b = matrices[("B_reduced_seam", case_id, subject)]
                residual = route_b - gauge @ route_a @ gauge.conj().T
                record[f"{subject}_maximum_absolute"] = matrix.maximum(residual)
                record[f"{subject}_frobenius"] = float(
                    np.linalg.norm(residual, ord="fro")
                )
            result.append(record)
        return result

    def _adverse(
        self,
        controls: ParentControls,
        parents: dict[str, tuple[ParentHopping, ...]],
        route_records: list[dict[str, JsonValue]],
        matrix: ParentMatrixConstructor,
        fitter: ParentModelFitter,
        attack: ComplexMatrix,
    ) -> list[dict[str, JsonValue]]:
        gamma = controls.twists[0]
        generic = controls.twists[1]
        identity_operation = controls.d4[0]
        quarter = controls.d4[1]
        directional_terms = controls.defects[0][1]
        nonlocal_terms = controls.defects[1][1]
        directional = matrix.defect(
            controls, directional_terms, gamma, "A_centered_uniform"
        )
        isotropic_fit = fitter.execute(
            controls,
            directional,
            gamma,
            "A_centered_uniform",
            identity_operation,
            "onsite_plus_isotropic_nearest_neighbor",
        )
        nonlocal_matrix = matrix.defect(
            controls, nonlocal_terms, gamma, "A_centered_uniform"
        )
        directional_fit = fitter.execute(
            controls,
            nonlocal_matrix,
            gamma,
            "A_centered_uniform",
            identity_operation,
            "onsite_plus_directional_nearest_neighbor",
        )
        omitted = matrix.defect(
            controls,
            (directional_terms[0],),
            gamma,
            "A_centered_uniform",
            include_reverse=False,
        )
        route_a_defect = matrix.defect(
            controls, directional_terms, generic, "A_centered_uniform"
        )
        route_b_defect = matrix.defect(
            controls, directional_terms, generic, "B_reduced_seam"
        )
        isotropic_parent = parents["isotropic_lambda_0p5_0p5_0"]
        source_iso = matrix.parent(
            controls, isotropic_parent, generic, "A_centered_uniform"
        )
        rotated_lift = matrix.transform_twist(generic, quarter)
        fixed_twist_target = matrix.parent(
            controls, isotropic_parent, generic, "A_centered_uniform"
        )
        permutation = matrix.permutation(controls, quarter)
        fixed_twist = (
            fixed_twist_target - permutation @ source_iso @ permutation.conj().T
        )
        anisotropic_parent = parents["anisotropic_lambda_0p3_0p7_0"]
        source_anis = matrix.parent(
            controls, anisotropic_parent, generic, "A_centered_uniform"
        )
        invalid_d4_target = matrix.parent(
            controls, anisotropic_parent, rotated_lift, "A_centered_uniform"
        )
        invalid_d4 = (
            invalid_d4_target - permutation @ source_anis @ permutation.conj().T
        )
        swap = controls.axis_swap
        swap_permutation = matrix.permutation(controls, swap)
        swap_lift = matrix.transform_twist(generic, swap)
        unswapped_target = matrix.parent(
            controls, anisotropic_parent, swap_lift, "A_centered_uniform"
        )
        unswapped = (
            unswapped_target
            - swap_permutation @ source_anis @ swap_permutation.conj().T
        )
        identity = np.eye(controls.dimension, dtype=np.complex128)
        alignment_unitarity = matrix.maximum(attack.conj().T @ attack - identity)
        if (
            alignment_unitarity
            > controls.criteria["alignment_unitarity_maximum_absolute"]
        ):
            raise ValueError("authored attack is not unitary")
        route_b_records = [
            record for record in route_records if record["route"] == "B_reduced_seam"
        ]
        route_violation_status = "missing_failure"
        try:
            RouteIndependenceGate().execute(
                "B_reduced_seam", "A_centered_uniform_matrix"
            )
        except ValueError as error:
            route_violation_status = str(error)
        return [
            {
                "control_id": "prealignment_subtraction",
                "status": "DEFECT_2D.SITE_MAP_UNRESOLVED",
                "value": None,
            },
            {
                "control_id": "omit_energy_reference_correction",
                "status": "discriminating",
                "value": float(np.linalg.norm(0.137 * identity, ord="fro")),
            },
            {
                "control_id": "directional_as_isotropic",
                "status": "discriminating",
                "value": isotropic_fit["residual_frobenius"],
            },
            {
                "control_id": "nonlocal_as_directional",
                "status": "discriminating",
                "value": directional_fit["residual_frobenius"],
            },
            {
                "control_id": "omit_hermitian_reverse",
                "status": "discriminating",
                "value": matrix.maximum(omitted - omitted.conj().T),
            },
            {
                "control_id": "compare_raw_gauges_without_bridge",
                "status": "discriminating",
                "value": matrix.maximum(route_b_defect - route_a_defect),
            },
            {
                "control_id": "hold_generic_twist_fixed_under_quarter_turn",
                "status": "discriminating",
                "value": matrix.maximum(fixed_twist),
            },
            {
                "control_id": "claim_D4_for_anisotropic_parent",
                "status": "discriminating",
                "value": matrix.maximum(invalid_d4),
            },
            {
                "control_id": "axis_swap_defect_without_parent_swap",
                "status": "discriminating",
                "value": matrix.maximum(unswapped),
            },
            {
                "control_id": "construct_route_B_from_route_A",
                "status": route_violation_status,
                "value": float(len(route_b_records)),
            },
        ]
