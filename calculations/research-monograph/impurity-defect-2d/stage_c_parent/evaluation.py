"""Result provenance and complete numerical evaluation for Stage C."""

from __future__ import annotations

import concurrent.futures
import hashlib
import json
import multiprocessing
import os
import platform
import resource
import time
from pathlib import Path
from typing import cast

import numpy as np

from .model import (
    ComplexMatrix,
    JsonValue,
    MatrixKey,
    ParentControls,
    ParentFixture,
    StageCResultContext,
)
from .operator_construction import ParentMatrixConstructor
from .scheduling import ParentScheduleExecutor

STAGE_DIRECTORY = Path(__file__).resolve(strict=True).parent.parent
RUNNER_PATH = STAGE_DIRECTORY / "run_stage_c_parent.py"


class StageCResultProvenanceSerializer:
    """Serialize exact source, authority, implementation, and resource metadata."""

    __slots__ = ()

    @staticmethod
    def execute(context: StageCResultContext) -> dict[str, JsonValue]:
        runner = RUNNER_PATH.resolve(strict=True)
        stage_directory = runner.parent
        implementation_paths = (
            ("runner_cli", runner),
            ("record_model", stage_directory / "stage_c_parent/model.py"),
            ("record_deserializers", stage_directory / "stage_c_parent/records.py"),
            (
                "operator_construction",
                stage_directory / "stage_c_parent/operator_construction.py",
            ),
            ("model_fitting", stage_directory / "stage_c_parent/model_fitting.py"),
            ("schedule_executor", stage_directory / "stage_c_parent/scheduling.py"),
            ("result_evaluation", stage_directory / "stage_c_parent/evaluation.py"),
            (
                "execution_authorization",
                stage_directory / "stage_c_parent/authorization.py",
            ),
            ("retention", stage_directory / "stage_c_parent/retention.py"),
            ("result_context", stage_directory / "stage_c_parent/context.py"),
            ("protected_workflow", stage_directory / "stage_c_parent/workflows.py"),
            ("verifier_cli", stage_directory / "verify_stage_c_parent.py"),
            (
                "independent_verifier",
                stage_directory / "stage_c_parent_verification/verifier.py",
            ),
            ("plotter", stage_directory / "plot_stage_c_parent.py"),
            ("result_schema", stage_directory / "stage-c-result.schema.json"),
            (
                "execution_authorization_schema",
                stage_directory / "stage-c-execution-authorization.schema.json",
            ),
        )
        repository = (
            Path(context.repository_root)
            if context.repository_root is not None
            else None
        )
        implementation = [
            {
                "role": role,
                "path": (
                    path.relative_to(repository).as_posix()
                    if repository is not None and path.is_relative_to(repository)
                    else path.name
                ),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
            for role, path in implementation_paths
        ]
        authorization: JsonValue
        if context.authorization_id is None:
            authorization = None
        else:
            authorization = {
                "authorization_id": context.authorization_id,
                "authorization_path": context.authorization_path,
                "authorization_sha256": context.authorization_sha256,
                "checkpoint_path": context.checkpoint_path,
                "checkpoint_sha256": context.checkpoint_sha256,
                "human_response_verbatim": context.human_response_verbatim,
            }
        runtime: float | None = None
        peak_memory: int | None = None
        if context.started_at is not None:
            runtime = time.perf_counter() - context.started_at
            usage = max(
                resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            )
            peak_memory = int(usage if platform.system() == "Darwin" else usage * 1024)
        return {
            "source_mode": context.source_mode,
            "authorization": authorization,
            "repository": {
                "root": context.repository_root,
                "revision": context.repository_revision,
                "machine_identity": context.machine_identity,
                "native_artifact_root": context.native_artifact_root,
            },
            "operation_inventory": list(context.operation_inventory),
            "input_identities": [
                {"role": value.role, "path": value.path, "sha256": value.sha256}
                for value in context.input_identities
            ],
            "implementation_identities": cast(JsonValue, implementation),
            "retained_output_paths": {
                "attempt_record": context.attempt_record_path,
                "result": context.result_path,
                "verification_log": context.verification_log_path,
                "summary_svg": context.summary_svg_path,
                "report": context.report_path,
                "native_evidence_manifest": context.native_evidence_manifest_path,
                "checksum_catalog": context.checksum_catalog_path,
            },
            "resource_envelope": {
                "maximum_runtime_seconds": context.maximum_runtime_seconds,
                "maximum_peak_memory_gib": context.maximum_peak_memory_gib,
                "maximum_retained_output_mib": context.maximum_retained_output_mib,
                "network_access": False,
                "external_executables": [],
                "new_dependencies": [],
            },
            "attempt_policy": {
                "maximum_attempts": context.maximum_attempts,
                "retry_authorized": context.retry_authorized,
                "overwrite_existing": context.overwrite_existing,
            },
            "execution_observation": {
                "runtime_seconds": runtime,
                "peak_memory_bytes": peak_memory,
                "output_bytes": 0,
            },
        }


class AcceptedParentStageCEvaluator:
    """Compose two fresh schedules and evaluate the adopted contract."""

    __slots__ = ()

    def execute(
        self,
        controls: ParentControls,
        fixture: ParentFixture,
        design_sha256: str,
        context: StageCResultContext,
    ) -> dict[str, JsonValue]:
        schedules = (
            ("A_then_B", ("A_centered_uniform", "B_reduced_seam")),
            ("B_then_A", ("B_reduced_seam", "A_centered_uniform")),
        )
        process_context = multiprocessing.get_context("spawn")
        action = ParentScheduleExecutor()
        with (
            concurrent.futures.ProcessPoolExecutor(
                max_workers=1, mp_context=process_context
            ) as first_executor,
            concurrent.futures.ProcessPoolExecutor(
                max_workers=1, mp_context=process_context
            ) as second_executor,
        ):
            futures = (
                first_executor.submit(action.execute, controls, fixture, *schedules[0]),
                second_executor.submit(
                    action.execute, controls, fixture, *schedules[1]
                ),
            )
            schedule_results = [future.result() for future in futures]
        process_ids = {result.process_id for result in schedule_results}
        if len(process_ids) != 2 or os.getpid() in process_ids:
            raise RuntimeError(
                "Stage C parent schedules did not use distinct processes"
            )
        schedules_payload: list[dict[str, JsonValue]] = []
        matrices: dict[str, dict[MatrixKey, ComplexMatrix]] = {}
        for result in schedule_results:
            payload = cast(JsonValue, json.loads(result.payload_json))
            if not isinstance(payload, dict):
                raise TypeError("schedule payload must be a JSON object")
            schedules_payload.append(payload)
            matrices[result.schedule_id] = {
                key: np.frombuffer(value, dtype="<c16").reshape(
                    (controls.dimension, controls.dimension)
                )
                for key, value in result.recovered_matrices
            }
        schedules_payload.sort(key=lambda value: cast(str, value["schedule_id"]))
        schedule_comparisons: list[JsonValue] = []
        maximum_schedule = 0.0
        first = matrices["A_then_B"]
        second = matrices["B_then_A"]
        matrix_action = ParentMatrixConstructor()
        for key in sorted(first):
            residual = first[key] - second[key]
            maximum = matrix_action.maximum(residual)
            maximum_schedule = max(maximum_schedule, maximum)
            schedule_comparisons.append(
                {
                    "route": key[0],
                    "case_id": key[1],
                    "maximum_absolute": maximum,
                    "frobenius": float(np.linalg.norm(residual, ord="fro")),
                }
            )
        if len(schedule_comparisons) != controls.schedule_comparisons:
            raise ValueError("schedule-comparison inventory differs")
        summary, criteria = self._evaluate(
            controls, schedules_payload, maximum_schedule
        )
        return {
            "schema_version": 1,
            "result_id": context.result_id,
            "evidence_status": context.evidence_status,
            "accepted_parent_read": context.accepted_parent_read,
            "design_sha256": design_sha256,
            "fixture_sha256": fixture.fixture_sha256,
            "runner_sha256": hashlib.sha256(RUNNER_PATH.read_bytes()).hexdigest(),
            "provenance": StageCResultProvenanceSerializer.execute(context),
            "software_versions": {
                "python": platform.python_version(),
                "numpy": np.__version__,
            },
            "inventory": {
                "execution_schedules": 2,
                "route_evaluations": controls.route_evaluations,
                "bridge_records": controls.bridge_records,
                "model_fit_records": controls.model_fit_records,
                "schedule_comparisons": controls.schedule_comparisons,
            },
            "schedules": cast(JsonValue, schedules_payload),
            "schedule_comparisons": schedule_comparisons,
            "criteria": cast(JsonValue, criteria),
            "summary": summary,
        }

    def _evaluate(
        self,
        controls: ParentControls,
        schedules: list[dict[str, JsonValue]],
        maximum_schedule: float,
    ) -> tuple[dict[str, JsonValue], list[dict[str, JsonValue]]]:
        route_records = [
            cast(dict[str, JsonValue], record)
            for schedule in schedules
            for record in cast(list[JsonValue], schedule["route_records"])
        ]
        bridges = [
            cast(dict[str, JsonValue], record)
            for schedule in schedules
            for record in cast(list[JsonValue], schedule["bridge_records"])
        ]
        preprocessing = [
            cast(dict[str, JsonValue], schedule["preprocessing"])
            for schedule in schedules
        ]
        if len(route_records) != controls.route_evaluations:
            raise ValueError("route-evaluation inventory differs")
        if len(bridges) != controls.bridge_records:
            raise ValueError("bridge inventory differs")
        fit_count = sum(
            len(cast(list[JsonValue], record["fits"])) for record in route_records
        )
        if fit_count != controls.model_fit_records:
            raise ValueError("model-fit inventory differs")
        maximum_parent_hermiticity = max(
            cast(float, record["parent_hermiticity_maximum_absolute"])
            for record in route_records
        )
        maximum_defect_hermiticity = max(
            cast(float, record["defect_hermiticity_maximum_absolute"])
            for record in route_records
        )
        hopping_records = [
            cast(dict[str, JsonValue], value[name])
            for value in preprocessing
            for name in ("isotropic", "pretruncation", "compact", "axis_swapped")
        ]
        maximum_hopping_hermiticity = max(
            cast(float, record["hermiticity_maximum_absolute"])
            for record in hopping_records
        )
        isotropic_hopping_symmetry = max(
            cast(
                float,
                cast(dict[str, JsonValue], value["isotropic"])[
                    "symmetry_maximum_absolute"
                ],
            )
            for value in preprocessing
        )
        anisotropic_hopping_symmetry = max(
            cast(
                float,
                cast(dict[str, JsonValue], value[name])["symmetry_maximum_absolute"],
            )
            for value in preprocessing
            for name in ("pretruncation", "compact", "axis_swapped")
        )
        maximum_alignment = max(
            cast(float, record["alignment_unitarity_maximum_absolute"])
            for record in route_records
        )
        maximum_recovery = max(
            cast(float, record["recovery_maximum_absolute"]) for record in route_records
        )
        maximum_recovery_frobenius = max(
            cast(float, record["recovery_frobenius"]) for record in route_records
        )
        isotropic_covariance = max(
            cast(float, record["covariance_maximum_absolute"])
            for record in route_records
            if record["parent_family"] == "isotropic_D4"
        )
        anisotropic_covariance = max(
            cast(float, record["covariance_maximum_absolute"])
            for record in route_records
            if record["parent_family"] == "anisotropic_D2"
        )
        axis_swap_covariance = max(
            cast(float, record["covariance_maximum_absolute"])
            for record in route_records
            if record["parent_family"] == "anisotropic_axis_swap"
        )
        maximum_covariance = max(
            isotropic_covariance, anisotropic_covariance, axis_swap_covariance
        )
        maximum_bridge = max(
            cast(float, value)
            for record in bridges
            for key, value in record.items()
            if key.endswith("_maximum_absolute")
        )
        selected_fits: list[dict[str, JsonValue]] = []
        for record in route_records:
            selected = record["selected_model_class"]
            for fit_value in cast(list[JsonValue], record["fits"]):
                fit = cast(dict[str, JsonValue], fit_value)
                if fit["model_class"] == selected:
                    selected_fits.append(fit)
        if len(selected_fits) != controls.route_evaluations:
            raise ValueError("selected-fit inventory differs")
        selected_fit_maximum = max(
            cast(float, fit["residual_maximum_absolute"]) for fit in selected_fits
        )
        selected_fit_frobenius = max(
            cast(float, fit["residual_frobenius"]) for fit in selected_fits
        )
        selected_exterior = max(
            cast(
                float,
                cast(
                    dict[str, JsonValue],
                    cast(dict[str, JsonValue], fit["residual_shells"])["exterior"],
                )["maximum_absolute"],
            )
            for fit in selected_fits
        )
        exact_support_agreement = all(
            fit["exact_support_match"] is True for fit in selected_fits
        )
        selection_agreement = all(
            record["selected_model_class"] == record["expected_model_class"]
            for record in route_records
        )
        compact_digests = [
            cast(str, cast(dict[str, JsonValue], value["compact"])["sha256"])
            for value in preprocessing
        ]
        preprocessing_agreement = compact_digests[0] == compact_digests[1]
        adverse = cast(list[dict[str, JsonValue]], schedules[0]["adverse_controls"])
        adverse_values = {
            cast(str, record["control_id"]): record["value"] for record in adverse
        }
        adverse_pass = (
            adverse[0]["status"] == "DEFECT_2D.SITE_MAP_UNRESOLVED"
            and cast(float, adverse_values["omit_energy_reference_correction"]) >= 1.0
            and cast(float, adverse_values["directional_as_isotropic"]) >= 0.03
            and cast(float, adverse_values["nonlocal_as_directional"]) >= 0.03
            and cast(float, adverse_values["omit_hermitian_reverse"]) >= 0.03
            and cast(float, adverse_values["compare_raw_gauges_without_bridge"]) >= 0.01
            and cast(
                float,
                adverse_values["hold_generic_twist_fixed_under_quarter_turn"],
            )
            >= 1.0e-6
            and cast(float, adverse_values["claim_D4_for_anisotropic_parent"]) >= 1.0e-3
            and cast(float, adverse_values["axis_swap_defect_without_parent_swap"])
            >= 1.0e-3
            and adverse[9]["status"] == "DEFECT_2D.ROUTE_INDEPENDENCE_VIOLATION"
        )
        criteria: list[dict[str, JsonValue]] = [
            self._criterion(
                "hopping_and_matrix_hermiticity",
                max(
                    maximum_hopping_hermiticity,
                    maximum_parent_hermiticity,
                    maximum_defect_hermiticity,
                ),
                controls.criteria["hopping_hermiticity_maximum_absolute_EG"],
                "<=",
            ),
            self._criterion(
                "isotropic_D4_hopping_covariance",
                isotropic_hopping_symmetry,
                controls.criteria[
                    "isotropic_D4_hopping_covariance_maximum_absolute_EG"
                ],
                "<=",
            ),
            self._criterion(
                "anisotropic_D2_hopping_covariance",
                anisotropic_hopping_symmetry,
                controls.criteria[
                    "anisotropic_D2_hopping_covariance_maximum_absolute_EG"
                ],
                "<=",
            ),
            self._criterion(
                "alignment_unitarity",
                maximum_alignment,
                controls.criteria["alignment_unitarity_maximum_absolute"],
                "<=",
            ),
            self._criterion(
                "known_recovery_maximum",
                maximum_recovery,
                controls.criteria["known_recovery_maximum_absolute_EG"],
                "<=",
            ),
            self._criterion(
                "known_recovery_frobenius",
                maximum_recovery_frobenius,
                controls.criteria["known_recovery_frobenius_EG"],
                "<=",
            ),
            self._criterion(
                "isotropic_D4_covariance",
                isotropic_covariance,
                controls.criteria["symmetry_covariance_maximum_absolute_EG"],
                "<=",
            ),
            self._criterion(
                "anisotropic_D2_covariance",
                anisotropic_covariance,
                controls.criteria["symmetry_covariance_maximum_absolute_EG"],
                "<=",
            ),
            self._criterion(
                "axis_swap_covariance",
                axis_swap_covariance,
                controls.criteria["axis_swap_covariance_maximum_absolute_EG"],
                "<=",
            ),
            self._criterion(
                "gauge_bridge",
                maximum_bridge,
                controls.criteria["gauge_bridge_maximum_absolute_EG"],
                "<=",
            ),
            self._criterion(
                "selected_fit_maximum",
                selected_fit_maximum,
                controls.criteria["fit_maximum_absolute_EG"],
                "<=",
            ),
            self._criterion(
                "selected_fit_frobenius",
                selected_fit_frobenius,
                controls.criteria["fit_frobenius_EG"],
                "<=",
            ),
            self._criterion(
                "selected_radius_two_exterior",
                selected_exterior,
                controls.criteria["radius_two_exterior_maximum_absolute_EG"],
                "<=",
            ),
            {
                "criterion": "exact_support_and_first_model_class_selection",
                "value": 1.0
                if exact_support_agreement and selection_agreement
                else 0.0,
                "comparison": "==",
                "threshold": 1.0,
                "passed": exact_support_agreement and selection_agreement,
            },
            {
                "criterion": "schedule_preprocessing_agreement",
                "value": 1.0 if preprocessing_agreement else 0.0,
                "comparison": "==",
                "threshold": 1.0,
                "passed": preprocessing_agreement,
            },
            self._criterion(
                "schedule_invariance",
                maximum_schedule,
                controls.criteria["schedule_maximum_absolute"],
                "==",
            ),
            {
                "criterion": "adverse_controls_discriminate",
                "value": 1.0 if adverse_pass else 0.0,
                "comparison": "==",
                "threshold": 1.0,
                "passed": adverse_pass,
            },
        ]
        summary: dict[str, JsonValue] = {
            "maximum_hopping_parent_or_defect_hermiticity": max(
                maximum_hopping_hermiticity,
                maximum_parent_hermiticity,
                maximum_defect_hermiticity,
            ),
            "maximum_hopping_symmetry_absolute": max(
                isotropic_hopping_symmetry, anisotropic_hopping_symmetry
            ),
            "maximum_alignment_unitarity": maximum_alignment,
            "maximum_recovery_absolute": maximum_recovery,
            "maximum_recovery_frobenius": maximum_recovery_frobenius,
            "maximum_covariance_absolute": maximum_covariance,
            "maximum_bridge_absolute": maximum_bridge,
            "maximum_selected_fit_absolute": selected_fit_maximum,
            "maximum_selected_fit_frobenius": selected_fit_frobenius,
            "maximum_selected_exterior_absolute": selected_exterior,
            "maximum_schedule_absolute": maximum_schedule,
            "preprocessing_schedule_agreement": preprocessing_agreement,
            "model_selection_agreement": selection_agreement,
            "adverse_controls_passed": adverse_pass,
            "all_criteria_passed": all(
                cast(bool, criterion["passed"]) for criterion in criteria
            ),
        }
        return summary, criteria

    @staticmethod
    def _criterion(
        identifier: str, value: float, threshold: float, comparison: str
    ) -> dict[str, JsonValue]:
        if comparison == "<=":
            passed = value <= threshold
        elif comparison == "==":
            passed = value == threshold
        else:
            raise ValueError(f"unsupported comparison {comparison}")
        return {
            "criterion": identifier,
            "value": value,
            "comparison": comparison,
            "threshold": threshold,
            "passed": passed,
        }
