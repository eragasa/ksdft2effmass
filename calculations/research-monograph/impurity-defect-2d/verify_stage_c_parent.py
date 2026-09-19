#!/usr/bin/env python3
"""Independently verify authored-fixture accepted-parent Stage C behavior."""

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

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type ComplexMatrix = npt.NDArray[np.complex128]
type IntPair = tuple[int, int]
type FloatPair = tuple[float, float]
type IntMatrix2 = tuple[tuple[int, int], tuple[int, int]]


@dataclass(frozen=True, slots=True)
class VerificationCase:
    """Represent one independently decoded case."""

    family: str
    defect_id: str
    twist_id: str
    operation_id: str


class VerificationJsonReader:
    """Decode closed JSON values without runner types."""

    __slots__ = ()

    @staticmethod
    def mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be an object")
        return value

    @staticmethod
    def array(value: JsonValue, name: str) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be an array")
        return value

    @staticmethod
    def text(value: JsonValue, name: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"{name} must be a string")
        return value

    @staticmethod
    def real(value: JsonValue, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be real")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    @staticmethod
    def boolean(value: JsonValue, name: str) -> bool:
        if not isinstance(value, bool):
            raise TypeError(f"{name} must be boolean")
        return value

    @staticmethod
    def integer(value: JsonValue, name: str) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be integer")
        return value


class IndependentStageCParentVerifier:
    """Reconstruct parents, defects, fits, bridges, and controls independently."""

    __slots__ = ("_json", "_nx", "_ny", "_dimension")

    def __init__(self) -> None:
        self._json = VerificationJsonReader()
        self._nx = 8
        self._ny = 8
        self._dimension = 64

    def execute(
        self, design_path: Path, fixture_path: Path, result_path: Path
    ) -> dict[str, JsonValue]:
        design_bytes = design_path.read_bytes()
        fixture_bytes = fixture_path.read_bytes()
        result = self._json.mapping(
            cast(JsonValue, json.loads(result_path.read_bytes())), "result"
        )
        if result.get("accepted_parent_read") is not False:
            raise ValueError("result does not declare execution-free operation")
        if result.get("evidence_status") not in (
            "authored synthetic execution-free software-verification behavior; "
            "not accepted-parent evidence",
            "authored synthetic complete-operation software-verification behavior; "
            "not accepted-parent evidence",
        ):
            raise ValueError("unexpected result evidence status")
        design_sha256 = hashlib.sha256(design_bytes).hexdigest()
        if design_sha256 != (
            "e5103eb95300095d46280fce5539b3e0a168c8c7b41f2f2473d1b3d2d8a48706"
        ):
            raise ValueError("verification design identity is not human-adopted")
        if result.get("design_sha256") != design_sha256:
            raise ValueError("result design identity differs")
        runner_path = Path(__file__).with_name("run_stage_c_parent.py")
        if (
            result.get("runner_sha256")
            != hashlib.sha256(runner_path.read_bytes()).hexdigest()
        ):
            raise ValueError("result runner identity differs")
        design = self._json.mapping(cast(JsonValue, json.loads(design_bytes)), "design")
        fixture = self._json.mapping(
            cast(JsonValue, json.loads(fixture_bytes)), "fixture"
        )
        if fixture.get("accepted_parent") is not False:
            raise ValueError("independent verification forbids accepted-parent fixture")
        fixture_id = fixture.get("fixture_id")
        if fixture_id == (
            "research-monograph.impurity-defect-2d.stage-c.accepted-parent."
            "authored-fixture.v1"
        ):
            source_digest = hashlib.sha256(fixture_bytes).hexdigest()
            source_mode = "authored_parent_fixture"
            parents = self._parents(fixture)
            expected_identity_records: tuple[dict[str, JsonValue], ...] = (
                {
                    "role": "authored_parent_fixture",
                    "path": fixture_path.resolve(strict=True)
                    .relative_to(Path.cwd().resolve(strict=True))
                    .as_posix(),
                    "sha256": source_digest,
                },
            )
        elif fixture_id == (
            "research-monograph.impurity-defect-2d.stage-c.accepted-parent."
            "adapter-authored-fixture.v1"
        ):
            source_digest, parents = self._adapter_parents(fixture)
            source_mode = "authored_accepted_parent_adapter_fixture"
            roles = (
                "accepted_periodic_parent_input",
                "accepted_periodic_parent_result",
                "accepted_stage_a_prerequisite",
                "accepted_stage_b_parent_and_route_evidence",
                "accepted_execution_free_stage_c_contract",
            )
            sources = self._json.mapping(fixture["sources"], "adapter sources")
            expected_identity_records = tuple(
                {
                    "role": role,
                    "path": f"embedded://{role}",
                    "sha256": hashlib.sha256(
                        json.dumps(
                            self._json.mapping(sources[role], role),
                            sort_keys=True,
                            separators=(",", ":"),
                            allow_nan=False,
                        ).encode("utf-8")
                    ).hexdigest(),
                }
                for role in roles
            )
        else:
            raise ValueError("unexpected independent-verification fixture")
        if result.get("fixture_sha256") != source_digest:
            raise ValueError("result source identity differs")
        provenance = self._json.mapping(result["provenance"], "provenance")
        observed_source_mode = provenance.get("source_mode")
        allowed_source_modes = (
            (source_mode, "authored_complete_operation_fixture")
            if source_mode == "authored_accepted_parent_adapter_fixture"
            else (source_mode,)
        )
        if observed_source_mode not in allowed_source_modes:
            raise ValueError("result source mode differs")
        identities = self._json.array(
            provenance["input_identities"], "input identities"
        )
        identity_records = tuple(
            self._json.mapping(value, "input identity") for value in identities
        )
        if identity_records != expected_identity_records:
            raise ValueError("result input-identity inventory differs")
        return self._verify(design, result, parents, False)

    def execute_accepted(
        self, authorization_path: Path, repository_root: Path, result_path: Path
    ) -> dict[str, JsonValue]:
        """Independently bind and verify one separately authorized parent result."""

        root = repository_root.resolve(strict=True)
        if not repository_root.is_absolute() or root != repository_root:
            raise ValueError("verification repository root must be canonical")
        authorization_file = self._inside(root, authorization_path)
        if authorization_file.relative_to(root).as_posix() != (
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-accepted-parent-execution-authorization.json"
        ):
            raise ValueError("verification authorization path differs")
        authorization = self._read(authorization_file, "authorization")
        if authorization.get("authorization_id") != (
            "research-monograph.impurity-defect-2d.stage-c."
            "accepted-parent-execution.hc17.v1"
        ):
            raise ValueError("verification authorization identity differs")
        if authorization.get("authorization_kind") != (
            "defect-2d-stage-c-accepted-parent-execution"
        ) or authorization.get("execution_authorized") is not True:
            raise ValueError("verification authorization is not executable Stage C")
        repository = self._json.mapping(
            authorization["repository"], "authorization repository"
        )
        if repository.get("root") != (
            "/Users/eugene/worktrees/ksdft2effmass-calculations"
        ) or repository.get("root") != str(root):
            raise ValueError("verification repository binding differs")
        if repository.get("revision") != (
            "9def2718ee763faf2060eb692739600485de5c72"
        ) or repository.get("revision") != self._repository_revision(root):
            raise ValueError("verification repository revision differs")
        if repository.get("machine_identity") != "minerva" or (
            repository.get("machine_identity") != platform.node()
        ):
            raise ValueError("verification machine binding differs")
        native_root_value = repository.get("native_artifact_root")
        if native_root_value != "/Users/eugene/projects/ksdft2effmass":
            raise ValueError("verification native artifact root differs")
        native_root = Path(native_root_value).resolve(strict=True)
        if str(native_root) != native_root_value:
            raise ValueError("verification native artifact root is not canonical")
        checkpoint_binding = self._json.mapping(
            authorization["checkpoint"], "checkpoint binding"
        )
        if checkpoint_binding.get("path") != (
            ".pi/checkpoints/research-monograph-impurity-defect-2d-"
            "stage-c-accepted-parent-execution.json"
        ):
            raise ValueError("verification checkpoint path differs")
        checkpoint = self._bound(root, checkpoint_binding["path"], "checkpoint")
        if self._digest(checkpoint) != checkpoint_binding.get("sha256"):
            raise ValueError("verification checkpoint identity differs")
        checkpoint_record = self._read(checkpoint, "checkpoint")
        if checkpoint_record.get("normalized_decision") != (
            "AUTHORIZE_ONE_ACCEPTED_PARENT_STAGE_C_EXECUTION"
        ):
            raise ValueError("verification checkpoint does not authorize Stage C")
        if checkpoint_record.get("human_response") != checkpoint_binding.get(
            "human_response_verbatim"
        ):
            raise ValueError("verification checkpoint response differs")
        artifact_values = self._json.array(
            authorization["artifacts"], "authorization artifacts"
        )
        bindings = tuple(
            self._json.mapping(value, "artifact binding")
            for value in artifact_values
        )
        roles = tuple(
            self._json.text(value["role"], "artifact role") for value in bindings
        )
        expected_roles = (
            "accepted_parent_design",
            "runner",
            "protected_workflow",
            "verifier",
            "plotter",
            "result_schema",
            "execution_authorization_schema",
            "accepted_periodic_parent_input",
            "accepted_periodic_parent_result",
            "accepted_stage_a_prerequisite",
            "accepted_stage_b_parent_and_route_evidence",
            "accepted_execution_free_stage_c_contract",
        )
        expected_paths = (
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-accepted-parent-design.json",
            "calculations/research-monograph/impurity-defect-2d/"
            "run_stage_c_parent.py",
            "calculations/research-monograph/impurity-defect-2d/"
            "run_stage_c_parent.py",
            "calculations/research-monograph/impurity-defect-2d/"
            "verify_stage_c_parent.py",
            "calculations/research-monograph/impurity-defect-2d/"
            "plot_stage_c_parent.py",
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-result.schema.json",
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-execution-authorization.schema.json",
            "calculations/research-monograph/periodic-2d/input.json",
            "calculations/research-monograph/periodic-2d/result.json",
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-a-result.json",
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-b-result.json",
            "calculations/research-monograph/impurity-defect-2d/stage-c-design.json",
        )
        represented_paths = tuple(
            self._json.text(value["path"], "artifact path") for value in bindings
        )
        if roles != expected_roles or represented_paths != expected_paths:
            raise ValueError("verification artifact bindings differ")
        paths: dict[str, Path] = {}
        digests: dict[str, str] = {}
        for binding in bindings:
            role = self._json.text(binding["role"], "artifact role")
            path = self._bound(root, binding["path"], role)
            digest = self._json.text(binding["sha256"], "artifact sha256")
            if self._digest(path) != digest:
                raise ValueError(f"verification artifact identity differs for {role}")
            paths[role] = path
            digests[role] = digest
        if paths["verifier"] != Path(__file__).resolve(strict=True):
            raise ValueError("authorization verifier path differs")
        operation_inventory = tuple(
            self._json.text(value, "operation")
            for value in self._json.array(
                authorization["operation_inventory"], "operation inventory"
            )
        )
        if operation_inventory != (
            "validate_authority",
            "consume_attempt",
            "validate_accepted_input_identities",
            "evaluate_stage_c",
            "serialize_result",
            "independently_verify_result",
            "render_summary_svg",
            "write_report",
            "write_native_evidence_manifest",
            "write_checksum_catalog",
            "finalize_attempt",
        ):
            raise ValueError("verification operation inventory differs")
        outputs = self._json.mapping(authorization["outputs"], "outputs")
        if outputs != {
            "attempt_record": (
                "calculations/research-monograph/impurity-defect-2d/"
                "stage-c-accepted-parent-attempt.jsonl"
            ),
            "result": (
                "calculations/research-monograph/impurity-defect-2d/"
                "stage-c-accepted-parent-result.json"
            ),
            "verification_log": (
                "calculations/research-monograph/impurity-defect-2d/"
                "stage-c-accepted-parent-verification.log"
            ),
            "summary_svg": (
                "calculations/research-monograph/impurity-defect-2d/"
                "stage-c-accepted-parent-summary.svg"
            ),
            "report": (
                "calculations/research-monograph/impurity-defect-2d/"
                "stage-c-accepted-parent-report.md"
            ),
            "native_evidence_manifest": (
                "calculations/research-monograph/impurity-defect-2d/"
                "stage-c-accepted-parent-native-evidence-manifest.json"
            ),
            "checksum_catalog": (
                "calculations/research-monograph/impurity-defect-2d/"
                "stage-c-accepted-parent-SHA256SUMS"
            ),
        }:
            raise ValueError("verification output bindings differ")
        attempt = self._json.mapping(
            authorization["attempt_policy"], "attempt policy"
        )
        if attempt != {
            "maximum_attempts": 1,
            "retry_authorized": False,
            "overwrite_existing": False,
        }:
            raise ValueError("verification attempt policy differs")
        expected_result = self._bound_output(root, outputs["result"], "result")
        result_file = self._inside(root, result_path)
        if result_file != expected_result:
            raise ValueError("verification result path differs")
        design_bytes = paths["accepted_parent_design"].read_bytes()
        design = self._json.mapping(cast(JsonValue, json.loads(design_bytes)), "design")
        result = self._read(result_file, "result")
        if result.get("accepted_parent_read") is not True:
            raise ValueError("result does not declare accepted-parent operation")
        if result.get("evidence_status") != (
            "calculated result from one explicitly authorized accepted-parent "
            "Stage C execution; numerical-verification evidence only, not "
            "material or scientific-validation evidence"
        ):
            raise ValueError("verification result evidence status differs")
        if result.get("design_sha256") != hashlib.sha256(design_bytes).hexdigest():
            raise ValueError("verification result design identity differs")
        if result.get("runner_sha256") != digests["runner"]:
            raise ValueError("verification result runner identity differs")
        data_roles = expected_roles[7:]
        source_digest = hashlib.sha256(
            "".join(digests[role] for role in data_roles).encode("ascii")
        ).hexdigest()
        if result.get("fixture_sha256") != source_digest:
            raise ValueError("verification accepted source identity differs")
        sources = {
            role: cast(JsonValue, self._read(paths[role], role)) for role in data_roles
        }
        _, parents = self._adapter_parents(
            {"sources": cast(JsonValue, sources)}
        )
        provenance = self._json.mapping(result["provenance"], "provenance")
        if provenance.get("source_mode") != "accepted_parent_execution":
            raise ValueError("verification result source mode differs")
        result_operations = tuple(
            self._json.text(value, "result operation")
            for value in self._json.array(
                provenance["operation_inventory"], "result operation inventory"
            )
        )
        if result_operations != operation_inventory:
            raise ValueError("verification result operation inventory differs")
        result_repository = self._json.mapping(
            provenance["repository"], "result repository"
        )
        if result_repository != repository:
            raise ValueError("verification result repository provenance differs")
        retained_outputs = self._json.mapping(
            provenance["retained_output_paths"], "result retained outputs"
        )
        if retained_outputs != outputs:
            raise ValueError("verification result retained outputs differ")
        result_attempt = self._json.mapping(
            provenance["attempt_policy"], "result attempt policy"
        )
        if result_attempt != attempt:
            raise ValueError("verification result attempt policy differs")
        result_identities = tuple(
            self._json.mapping(value, "result input identity")
            for value in self._json.array(
                provenance["input_identities"], "result input identities"
            )
        )
        expected_result_identities = tuple(
            {
                "role": role,
                "path": self._json.text(binding["path"], "artifact path"),
                "sha256": digests[role],
            }
            for role, binding in zip(data_roles, bindings[7:], strict=True)
        )
        if result_identities != expected_result_identities:
            raise ValueError("verification result input provenance differs")
        result_authorization = self._json.mapping(
            provenance["authorization"], "result authorization"
        )
        if result_authorization.get("authorization_sha256") != self._digest(
            authorization_file
        ):
            raise ValueError("result authorization identity differs")
        return self._verify(design, result, parents, True)

    def _verify(
        self,
        design: dict[str, JsonValue],
        result: dict[str, JsonValue],
        parents: dict[str, dict[IntPair, complex]],
        accepted_parent_read: bool,
    ) -> dict[str, JsonValue]:
        operations = self._operations()
        defects, expected_models = self._defects(design)
        twists = self._twists(design)
        schedules = self._json.array(result["schedules"], "schedules")
        if len(schedules) != 2:
            raise ValueError("two schedules required")
        maximum_difference = 0.0
        reconstructed_records = 0
        reconstructed_fits = 0
        schedule_signatures: list[str] = []
        schedule_preprocessing: list[str] = []
        for schedule_value in schedules:
            schedule = self._json.mapping(schedule_value, "schedule")
            schedule_records = self._json.array(
                schedule["route_records"], "route records"
            )
            if len(schedule_records) != 104:
                raise ValueError("each schedule must retain 104 route records")
            schedule_signature: list[JsonValue] = []
            for record_value in schedule_records:
                record = self._json.mapping(record_value, "route record")
                case = self._parse_case(self._json.text(record["case_id"], "case_id"))
                route = self._json.text(record["route"], "route")
                operation = operations[case.operation_id]
                base_twist = twists[case.twist_id]
                lifted = self._transform_twist(base_twist, operation)
                comparison_twist = (
                    lifted if route == "A_centered_uniform" else self._reduce(lifted)
                )
                source_parent_id, target_parent_id = self._parent_ids(case.family)
                transformed_terms = tuple(
                    self._transform_bond(term, operation)
                    for term in defects[case.defect_id]
                )
                target_parent = self._matrix(
                    parents[target_parent_id], comparison_twist, route
                )
                target_defect = self._defect(
                    transformed_terms, comparison_twist, route, True
                )
                target_full = target_parent + target_defect
                recovered = self._recover_independently(
                    target_full, target_parent, lifted, route
                )
                recovery = recovered - target_defect
                maximum_difference = max(
                    maximum_difference,
                    self._difference(
                        record,
                        "parent_hermiticity_maximum_absolute",
                        self._maximum(target_parent - target_parent.conj().T),
                    ),
                    self._difference(
                        record,
                        "defect_hermiticity_maximum_absolute",
                        self._maximum(target_defect - target_defect.conj().T),
                    ),
                    self._difference(
                        record,
                        "recovery_maximum_absolute",
                        self._maximum(recovery),
                    ),
                    self._difference(
                        record,
                        "recovery_frobenius",
                        float(np.linalg.norm(recovery, ord="fro")),
                    ),
                )
                source_twist = (
                    base_twist
                    if route == "A_centered_uniform"
                    else self._reduce(base_twist)
                )
                source_parent = self._matrix(
                    parents[source_parent_id], source_twist, route
                )
                source_defect = self._defect(
                    defects[case.defect_id], source_twist, route, True
                )
                covariance = self._covariance(
                    source_parent + source_defect,
                    target_full,
                    operation,
                    base_twist,
                    lifted,
                    route,
                )
                maximum_difference = max(
                    maximum_difference,
                    self._difference(
                        record,
                        "covariance_maximum_absolute",
                        self._maximum(covariance),
                    ),
                    self._difference(
                        record,
                        "covariance_frobenius",
                        float(np.linalg.norm(covariance, ord="fro")),
                    ),
                )
                fit_records = self._json.array(record["fits"], "fits")
                if len(fit_records) != 5:
                    raise ValueError("every route record requires five fits")
                selected: str | None = None
                for fit_value in fit_records:
                    fit = self._json.mapping(fit_value, "fit")
                    model_class = self._json.text(fit["model_class"], "model class")
                    fit_metrics = self._fit(
                        recovered,
                        comparison_twist,
                        route,
                        operation,
                        model_class,
                    )
                    for key in (
                        "residual_maximum_absolute",
                        "residual_frobenius",
                        "residual_spectral",
                        "core_exterior_coupling_frobenius",
                    ):
                        maximum_difference = max(
                            maximum_difference,
                            self._difference(fit, key, cast(float, fit_metrics[key])),
                        )
                    if (
                        fit["target_support_sha256"]
                        != fit_metrics["target_support_sha256"]
                    ):
                        raise ValueError("independent target support differs")
                    if (
                        fit["fitted_support_sha256"]
                        != fit_metrics["fitted_support_sha256"]
                    ):
                        raise ValueError("independent fitted support differs")
                    exact_support = (
                        fit_metrics["target_support_sha256"]
                        == fit_metrics["fitted_support_sha256"]
                    )
                    if fit["exact_support_match"] is not exact_support:
                        raise ValueError("retained exact-support disposition differs")
                    accepted = (
                        cast(float, fit_metrics["residual_maximum_absolute"]) <= 1.0e-10
                        and cast(float, fit_metrics["residual_frobenius"]) <= 1.0e-10
                        and cast(float, fit_metrics["exterior_maximum_absolute"])
                        <= 1.0e-10
                        and exact_support
                    )
                    if self._json.boolean(fit["accepted"], "accepted") != accepted:
                        raise ValueError("independent fit acceptance differs")
                    if selected is None and accepted:
                        selected = model_class
                    reconstructed_fits += 1
                if record["selected_model_class"] != selected:
                    raise ValueError("independent first accepted model differs")
                if selected != expected_models[case.defect_id]:
                    raise ValueError("authored expected model identity differs")
                schedule_signature.append(
                    {
                        "case_id": case.family
                        + case.defect_id
                        + case.twist_id
                        + case.operation_id,
                        "route": route,
                        "selected": selected,
                    }
                )
                reconstructed_records += 1
            schedule_signatures.append(
                hashlib.sha256(
                    json.dumps(
                        schedule_signature, sort_keys=True, separators=(",", ":")
                    ).encode()
                ).hexdigest()
            )
            preprocessing = self._json.mapping(
                schedule["preprocessing"], "preprocessing"
            )
            compact = self._json.mapping(preprocessing["compact"], "compact")
            schedule_preprocessing.append(
                self._json.text(compact["sha256"], "compact sha256")
            )
            maximum_difference = max(
                maximum_difference,
                self._verify_bridges(schedule, parents, defects, operations, twists),
                self._verify_adverse(schedule),
            )
        if schedule_signatures[0] != schedule_signatures[1]:
            raise ValueError("independent schedule signatures differ")
        if schedule_preprocessing[0] != schedule_preprocessing[1]:
            raise ValueError("anisotropic preprocessing differs between schedules")
        comparisons = self._json.array(
            result["schedule_comparisons"], "schedule comparisons"
        )
        if len(comparisons) != 104:
            raise ValueError("104 schedule comparisons required")
        for comparison_value in comparisons:
            comparison = self._json.mapping(comparison_value, "comparison")
            if self._json.real(comparison["maximum_absolute"], "maximum") != 0.0:
                raise ValueError("authored schedule comparison is not exact")
            if self._json.real(comparison["frobenius"], "frobenius") != 0.0:
                raise ValueError("authored schedule Frobenius comparison is not exact")
        if reconstructed_records != 208 or reconstructed_fits != 1040:
            raise ValueError("independent reconstruction inventory differs")
        if maximum_difference > 2.0e-12:
            raise ValueError(
                "maximum independent scalar difference "
                f"{maximum_difference} exceeds 2e-12"
            )
        summary = self._json.mapping(result["summary"], "summary")
        if summary.get("all_criteria_passed") is not True:
            raise ValueError("runner criteria did not all pass")
        return {
            "verification": "PASS",
            "reconstructed_route_records": reconstructed_records,
            "reconstructed_model_fits": reconstructed_fits,
            "maximum_independent_scalar_difference": maximum_difference,
            "runner_imported": False,
            "normal_equations_used": False,
            "accepted_parent_read": accepted_parent_read,
        }

    def _parents(
        self, fixture: dict[str, JsonValue]
    ) -> dict[str, dict[IntPair, complex]]:
        isotropic_record = self._json.mapping(
            fixture["isotropic_parent"], "isotropic parent"
        )
        isotropic: dict[IntPair, complex] = {}
        for value in self._json.array(isotropic_record["hoppings"], "hoppings"):
            record = self._json.mapping(value, "hopping")
            displacement = (
                int(self._json.real(record["rx"], "rx")),
                int(self._json.real(record["ry"], "ry")),
            )
            isotropic[displacement] = complex(
                self._json.real(record["real"], "real"),
                self._json.real(record["imag"], "imag"),
            )
        anisotropic_record = self._json.mapping(
            fixture["anisotropic_parent"], "anisotropic parent"
        )
        energy_rows = self._json.array(anisotropic_record["band_energies"], "energies")
        energies = np.asarray(
            [
                [
                    self._json.real(value, "energy")
                    for value in self._json.array(row, "row")
                ]
                for row in energy_rows
            ],
            dtype=np.float64,
        )
        coefficients = np.fft.ifft2(energies)
        anisotropic: dict[IntPair, complex] = {}
        for rx in range(-7, 8):
            for ry in range(-7, 8):
                if rx * rx + ry * ry <= 18:
                    anisotropic[(rx, ry)] = complex(coefficients[rx % 15, ry % 15])
        swapped = {(ry, rx): value for (rx, ry), value in anisotropic.items()}
        if len(isotropic) != 61 or len(anisotropic) != 61 or len(swapped) != 61:
            raise ValueError("independent parent inventory differs")
        return {
            "isotropic_lambda_0p5_0p5_0": isotropic,
            "anisotropic_lambda_0p3_0p7_0": anisotropic,
            "anisotropic_lambda_0p7_0p3_0": swapped,
        }

    def _adapter_parents(
        self, fixture: dict[str, JsonValue]
    ) -> tuple[str, dict[str, dict[IntPair, complex]]]:
        sources = self._json.mapping(fixture["sources"], "adapter sources")
        roles = (
            "accepted_periodic_parent_input",
            "accepted_periodic_parent_result",
            "accepted_stage_a_prerequisite",
            "accepted_stage_b_parent_and_route_evidence",
            "accepted_execution_free_stage_c_contract",
        )
        records = tuple(self._json.mapping(sources[role], role) for role in roles)
        digests = tuple(
            hashlib.sha256(
                json.dumps(
                    record, sort_keys=True, separators=(",", ":"), allow_nan=False
                ).encode("utf-8")
            ).hexdigest()
            for record in records
        )
        source_digest = hashlib.sha256("".join(digests).encode("ascii")).hexdigest()
        periodic_input, periodic_result, stage_a, stage_b, stage_c = records
        anisotropic = self._json.mapping(
            periodic_input["anisotropic_control"], "anisotropic input"
        )
        anisotropic_result = self._json.mapping(
            periodic_result["anisotropy_control"], "anisotropic result"
        )
        parameters = tuple(
            self._json.real(anisotropic[name], name)
            for name in ("lambda_x", "lambda_y", "lambda_xy")
        )
        result_parameters = tuple(
            self._json.real(anisotropic_result[name], name)
            for name in ("lambda_x", "lambda_y", "lambda_xy")
        )
        if parameters != (0.3, 0.7, 0.0) or result_parameters != parameters:
            raise ValueError("independent adapter anisotropy differs")
        if stage_a.get("stage_id") != "A_null_and_folding":
            raise ValueError("independent Stage A identity differs")
        if stage_b.get("stage_id") != "B_scalar_onsite_and_D4_multiroute":
            raise ValueError("independent Stage B identity differs")
        if stage_c.get("design_id") != (
            "research-monograph.impurity-defect-2d.stage-c.execution-free.v1"
        ):
            raise ValueError("independent Stage C contract differs")
        isotropic: dict[IntPair, complex] = {}
        for value in self._json.array(stage_b["input_hoppings"], "input hoppings"):
            record = self._json.mapping(value, "hopping")
            displacement = (
                self._json.integer(record["rx"], "rx"),
                self._json.integer(record["ry"], "ry"),
            )
            isotropic[displacement] = complex(
                self._json.real(record["real"], "real"),
                self._json.real(record["imag"], "imag"),
            )
        cutoff = self._json.integer(
            periodic_input["plane_wave_reference_cutoff"], "cutoff"
        )
        mesh = self._json.integer(periodic_input["reciprocal_mesh_size"], "mesh")
        if cutoff != 5 or mesh != 15:
            raise ValueError("independent adapter discretization differs")
        momenta = np.fft.fftfreq(mesh)
        x_energies = np.asarray(
            [self._lowest_band(float(k), parameters[0], cutoff) for k in momenta]
        )
        y_energies = np.asarray(
            [self._lowest_band(float(k), parameters[1], cutoff) for k in momenta]
        )
        coefficients = np.fft.ifft2(x_energies[:, None] + y_energies[None, :])
        compact: dict[IntPair, complex] = {}
        for rx in range(-7, 8):
            for ry in range(-7, 8):
                if rx * rx + ry * ry <= 18:
                    compact[(rx, ry)] = complex(coefficients[rx % 15, ry % 15])
        swapped = {(ry, rx): value for (rx, ry), value in compact.items()}
        if len(isotropic) != 61 or len(compact) != 61 or len(swapped) != 61:
            raise ValueError("independent adapter inventory differs")
        return source_digest, {
            "isotropic_lambda_0p5_0p5_0": isotropic,
            "anisotropic_lambda_0p3_0p7_0": compact,
            "anisotropic_lambda_0p7_0p3_0": swapped,
        }

    @staticmethod
    def _lowest_band(momentum: float, strength: float, cutoff: int) -> float:
        indices = np.arange(-cutoff, cutoff + 1, dtype=np.float64)
        matrix = np.diag(np.square(momentum + indices))
        matrix += np.diag(np.full(2 * cutoff, strength / 2.0), 1)
        matrix += np.diag(np.full(2 * cutoff, strength / 2.0), -1)
        return float(np.linalg.eigvalsh(matrix)[0])

    def _defects(
        self, design: dict[str, JsonValue]
    ) -> tuple[dict[str, tuple[tuple[IntPair, float], ...]], dict[str, str]]:
        defects: dict[str, tuple[tuple[IntPair, float], ...]] = {}
        expected: dict[str, str] = {}
        for value in self._json.array(design["planted_defects"], "defects"):
            record = self._json.mapping(value, "defect")
            identifier = self._json.text(record["defect_id"], "defect id")
            terms: list[tuple[IntPair, float]] = []
            for term_value in self._json.array(record["terms"], "terms"):
                term = self._json.mapping(term_value, "term")
                displacement_values = self._json.array(
                    term["displacement"], "displacement"
                )
                terms.append(
                    (
                        (
                            int(self._json.real(displacement_values[0], "dx")),
                            int(self._json.real(displacement_values[1], "dy")),
                        ),
                        self._json.real(term["change"], "change"),
                    )
                )
            defects[identifier] = tuple(terms)
            expected[identifier] = self._json.text(
                record["expected_first_accepted_model_class"], "expected model"
            )
        return defects, expected

    def _twists(self, design: dict[str, JsonValue]) -> dict[str, FloatPair]:
        space = self._json.mapping(design["represented_space"], "represented space")
        values = self._json.array(space["twist_lifts_turns"], "twists")
        if len(values) != 2:
            raise ValueError("independent verifier requires two twists")
        result: list[FloatPair] = []
        for value in values:
            pair = self._json.array(value, "twist")
            if len(pair) != 2:
                raise ValueError("twist must contain two components")
            result.append(
                (
                    self._json.real(pair[0], "twist x"),
                    self._json.real(pair[1], "twist y"),
                )
            )
        return {"gamma": result[0], "generic": result[1]}

    @staticmethod
    def _operations() -> dict[str, IntMatrix2]:
        return {
            "identity": ((1, 0), (0, 1)),
            "quarter_turn": ((0, -1), (1, 0)),
            "half_turn": ((-1, 0), (0, -1)),
            "three_quarter_turn": ((0, 1), (-1, 0)),
            "reflection_x": ((1, 0), (0, -1)),
            "reflection_y": ((-1, 0), (0, 1)),
            "reflection_diagonal": ((0, 1), (1, 0)),
            "reflection_antidiagonal": ((0, -1), (-1, 0)),
        }

    @staticmethod
    def _parse_case(identifier: str) -> VerificationCase:
        fields = identifier.split("__")
        if len(fields) != 4:
            raise ValueError(f"invalid case identity {identifier}")
        return VerificationCase(*fields)

    @staticmethod
    def _parent_ids(family: str) -> tuple[str, str]:
        if family == "isotropic":
            return "isotropic_lambda_0p5_0p5_0", "isotropic_lambda_0p5_0p5_0"
        if family == "anisotropic_D2":
            return "anisotropic_lambda_0p3_0p7_0", "anisotropic_lambda_0p3_0p7_0"
        if family == "axis_swap":
            return "anisotropic_lambda_0p3_0p7_0", "anisotropic_lambda_0p7_0p3_0"
        raise ValueError(f"unsupported parent family {family}")

    def _matrix(
        self, hoppings: dict[IntPair, complex], twist: FloatPair, route: str
    ) -> ComplexMatrix:
        result = np.zeros((self._dimension, self._dimension), dtype=np.complex128)
        for x in range(self._nx):
            for y in range(self._ny):
                row = self._index((x, y))
                for (dx, dy), value in hoppings.items():
                    target = x + dx, y + dy
                    column = self._index(target)
                    phase = self._phase((x, y), (dx, dy), twist, route)
                    result[row, column] += value * phase
        return result

    def _defect(
        self,
        terms: tuple[tuple[IntPair, float], ...],
        twist: FloatPair,
        route: str,
        reverse: bool,
    ) -> ComplexMatrix:
        result = np.zeros((self._dimension, self._dimension), dtype=np.complex128)
        for displacement, value in terms:
            row = self._index((0, 0))
            column = self._index(displacement)
            phase = self._phase((0, 0), displacement, twist, route)
            result[row, column] += value * phase
            if reverse:
                result[column, row] += value * phase.conjugate()
        return result

    def _phase(
        self,
        start: IntPair,
        displacement: IntPair,
        twist: FloatPair,
        route: str,
    ) -> complex:
        if route == "A_centered_uniform":
            return complex(
                np.exp(
                    2.0j
                    * np.pi
                    * (
                        twist[0] * displacement[0] / self._nx
                        + twist[1] * displacement[1] / self._ny
                    )
                )
            )
        if route == "B_reduced_seam":
            qx, _ = divmod(start[0] + displacement[0], self._nx)
            qy, _ = divmod(start[1] + displacement[1], self._ny)
            return complex(np.exp(2.0j * np.pi * (qx * twist[0] + qy * twist[1])))
        raise ValueError(f"unsupported route {route}")

    def _recover_independently(
        self,
        full: ComplexMatrix,
        parent: ComplexMatrix,
        lifted_twist: FloatPair,
        route: str,
    ) -> ComplexMatrix:
        attack = self._attack()
        if route == "B_reduced_seam":
            gauge = self._gauge(lifted_twist)
            attack = gauge @ attack @ gauge.conj().T
        identity = np.eye(self._dimension, dtype=np.complex128)
        attacked = attack @ full @ attack.conj().T + 0.137 * identity
        aligned = attack.conj().T @ (attacked - 0.137 * identity) @ attack
        return np.asarray(aligned - parent, dtype=np.complex128)

    def _covariance(
        self,
        source: ComplexMatrix,
        target: ComplexMatrix,
        operation: IntMatrix2,
        base_twist: FloatPair,
        lifted_twist: FloatPair,
        route: str,
    ) -> ComplexMatrix:
        permutation = self._permutation(operation)
        if route == "A_centered_uniform":
            return np.asarray(
                target - permutation @ source @ permutation.conj().T,
                dtype=np.complex128,
            )
        source_uniform = (
            self._gauge(base_twist).conj().T @ source @ self._gauge(base_twist)
        )
        target_uniform = (
            self._gauge(lifted_twist).conj().T @ target @ self._gauge(lifted_twist)
        )
        return np.asarray(
            target_uniform - permutation @ source_uniform @ permutation.conj().T,
            dtype=np.complex128,
        )

    def _fit(
        self,
        target: ComplexMatrix,
        twist: FloatPair,
        route: str,
        operation: IntMatrix2,
        model_class: str,
    ) -> dict[str, float | str]:
        basis = self._basis(twist, route, operation, model_class)
        columns = np.column_stack(
            [
                np.concatenate((value.real.ravel(), value.imag.ravel()))
                for value in basis
            ]
        )
        vector = np.concatenate((target.real.ravel(), target.imag.ravel()))
        orthogonal, triangular = np.linalg.qr(columns, mode="reduced")
        coefficients = np.linalg.solve(triangular, orthogonal.T @ vector)
        fitted = np.zeros_like(target)
        for coefficient, value in zip(coefficients, basis, strict=True):
            fitted += float(coefficient) * value
        residual = target - fitted
        return {
            "residual_maximum_absolute": self._maximum(residual),
            "residual_frobenius": float(np.linalg.norm(residual, ord="fro")),
            "residual_spectral": float(np.linalg.norm(residual, ord=2)),
            "core_exterior_coupling_frobenius": self._core_exterior(residual),
            "exterior_maximum_absolute": self._exterior_maximum(residual),
            "target_support_sha256": self._support_digest(target),
            "fitted_support_sha256": self._support_digest(fitted),
        }

    def _basis(
        self, twist: FloatPair, route: str, operation: IntMatrix2, model_class: str
    ) -> tuple[ComplexMatrix, ...]:
        onsite = self._onsite((0, 0))
        x_onsite = self._onsite(self._transform_pair((1, 0), operation))
        y_onsite = self._onsite(self._transform_pair((0, 1), operation))
        x = self._defect(
            ((self._transform_pair((1, 0), operation), 1.0),), twist, route, True
        )
        y = self._defect(
            ((self._transform_pair((0, 1), operation), 1.0),), twist, route, True
        )
        diagonal = self._defect(
            ((self._transform_pair((1, 1), operation), 1.0),), twist, route, True
        )
        if model_class == "point_scalar_onsite":
            return (onsite,)
        if model_class == "finite_support_diagonal_onsite":
            return onsite, x_onsite, y_onsite
        if model_class == "onsite_plus_isotropic_nearest_neighbor":
            return onsite, x + y
        if model_class == "onsite_plus_directional_nearest_neighbor":
            return onsite, x, y
        if model_class == "finite_range_nonlocal_radius_two":
            return onsite, x, y, diagonal
        raise ValueError(f"unsupported model class {model_class}")

    def _verify_bridges(
        self,
        schedule: dict[str, JsonValue],
        parents: dict[str, dict[IntPair, complex]],
        defects: dict[str, tuple[tuple[IntPair, float], ...]],
        operations: dict[str, IntMatrix2],
        twists: dict[str, FloatPair],
    ) -> float:
        maximum_difference = 0.0
        bridges = self._json.array(schedule["bridge_records"], "bridges")
        if len(bridges) != 52:
            raise ValueError("52 bridge records required per schedule")
        for bridge_value in bridges:
            bridge = self._json.mapping(bridge_value, "bridge")
            case = self._parse_case(self._json.text(bridge["case_id"], "case id"))
            operation = operations[case.operation_id]
            lifted = self._transform_twist(twists[case.twist_id], operation)
            reduced = self._reduce(lifted)
            _, target_parent_id = self._parent_ids(case.family)
            transformed_terms = tuple(
                self._transform_bond(term, operation)
                for term in defects[case.defect_id]
            )
            parent_a = self._matrix(
                parents[target_parent_id], lifted, "A_centered_uniform"
            )
            parent_b = self._matrix(
                parents[target_parent_id], reduced, "B_reduced_seam"
            )
            defect_a = self._defect(
                transformed_terms, lifted, "A_centered_uniform", True
            )
            defect_b = self._defect(transformed_terms, reduced, "B_reduced_seam", True)
            gauge = self._gauge(lifted)
            for subject, route_a, route_b in (
                ("parent", parent_a, parent_b),
                ("defect", defect_a, defect_b),
                ("full", parent_a + defect_a, parent_b + defect_b),
            ):
                residual = route_b - gauge @ route_a @ gauge.conj().T
                maximum_difference = max(
                    maximum_difference,
                    self._difference(
                        bridge, f"{subject}_maximum_absolute", self._maximum(residual)
                    ),
                    self._difference(
                        bridge,
                        f"{subject}_frobenius",
                        float(np.linalg.norm(residual, ord="fro")),
                    ),
                )
            for subject in ("attacked", "recovered"):
                retained = self._json.real(
                    bridge[f"{subject}_maximum_absolute"], subject
                )
                if retained > 1.0e-10:
                    raise ValueError(f"retained {subject} bridge exceeds criterion")
        return maximum_difference

    def _verify_adverse(self, schedule: dict[str, JsonValue]) -> float:
        records = [
            self._json.mapping(value, "adverse")
            for value in self._json.array(schedule["adverse_controls"], "adverse")
        ]
        values = {
            self._json.text(value["control_id"], "id"): value for value in records
        }
        floors = {
            "omit_energy_reference_correction": 1.0,
            "directional_as_isotropic": 0.03,
            "nonlocal_as_directional": 0.03,
            "omit_hermitian_reverse": 0.03,
            "compare_raw_gauges_without_bridge": 0.01,
            "hold_generic_twist_fixed_under_quarter_turn": 1.0e-6,
            "claim_D4_for_anisotropic_parent": 1.0e-3,
            "axis_swap_defect_without_parent_swap": 1.0e-3,
        }
        for identifier, floor in floors.items():
            value = self._json.real(values[identifier]["value"], identifier)
            if value < floor:
                raise ValueError(f"adverse control {identifier} did not discriminate")
        if values["prealignment_subtraction"].get("status") != (
            "DEFECT_2D.SITE_MAP_UNRESOLVED"
        ):
            raise ValueError("prealignment control did not fail closed")
        if values["construct_route_B_from_route_A"].get("status") != (
            "DEFECT_2D.ROUTE_INDEPENDENCE_VIOLATION"
        ):
            raise ValueError("route-provenance control did not fail closed")
        return 0.0

    def _core_indices(self) -> tuple[list[int], list[int]]:
        core: list[int] = []
        for index in range(self._dimension):
            x, y = divmod(index, self._ny)
            if max(min(x, self._nx - x), min(y, self._ny - y)) <= 2:
                core.append(index)
        exterior = [index for index in range(self._dimension) if index not in core]
        return core, exterior

    def _core_exterior(self, matrix: ComplexMatrix) -> float:
        core, exterior = self._core_indices()
        return float(
            np.sqrt(
                np.linalg.norm(matrix[np.ix_(core, exterior)], ord="fro") ** 2
                + np.linalg.norm(matrix[np.ix_(exterior, core)], ord="fro") ** 2
            )
        )

    def _exterior_maximum(self, matrix: ComplexMatrix) -> float:
        _, exterior = self._core_indices()
        if not exterior:
            return 0.0
        exterior_block = matrix[np.ix_(exterior, exterior)]
        core, _ = self._core_indices()
        cross = np.concatenate(
            (
                matrix[np.ix_(core, exterior)].ravel(),
                matrix[np.ix_(exterior, core)].ravel(),
                exterior_block.ravel(),
            )
        )
        return float(np.max(np.abs(cross), initial=0.0))

    def _attack(self) -> ComplexMatrix:
        operation = self._operations()["reflection_antidiagonal"]
        permutation = np.zeros((self._dimension, self._dimension), dtype=np.complex128)
        for x in range(self._nx):
            for y in range(self._ny):
                target = self._transform_pair((x, y), operation)
                translated = target[0] + 2, target[1] + 3
                permutation[self._index(translated), self._index((x, y))] = 1.0
        phases = np.asarray(
            [
                np.exp(1.0j * (0.137 * x - 0.191 * y))
                for x in range(self._nx)
                for y in range(self._ny)
            ],
            dtype=np.complex128,
        )
        return np.asarray(permutation @ np.diag(phases), dtype=np.complex128)

    def _permutation(self, operation: IntMatrix2) -> ComplexMatrix:
        result = np.zeros((self._dimension, self._dimension), dtype=np.complex128)
        for x in range(self._nx):
            for y in range(self._ny):
                result[
                    self._index(self._transform_pair((x, y), operation)),
                    self._index((x, y)),
                ] = 1.0
        return result

    def _gauge(self, twist: FloatPair) -> ComplexMatrix:
        phases = [
            np.exp(2.0j * np.pi * (x * twist[0] / self._nx + y * twist[1] / self._ny))
            for x in range(self._nx)
            for y in range(self._ny)
        ]
        return np.asarray(np.diag(phases), dtype=np.complex128)

    def _onsite(self, site: IntPair) -> ComplexMatrix:
        result = np.zeros((self._dimension, self._dimension), dtype=np.complex128)
        index = self._index(site)
        result[index, index] = 1.0
        return result

    def _index(self, site: IntPair) -> int:
        return (site[0] % self._nx) * self._ny + (site[1] % self._ny)

    @staticmethod
    def _transform_pair(value: IntPair, operation: IntMatrix2) -> IntPair:
        return (
            operation[0][0] * value[0] + operation[0][1] * value[1],
            operation[1][0] * value[0] + operation[1][1] * value[1],
        )

    @classmethod
    def _transform_bond(
        cls, term: tuple[IntPair, float], operation: IntMatrix2
    ) -> tuple[IntPair, float]:
        return cls._transform_pair(term[0], operation), term[1]

    @staticmethod
    def _transform_twist(value: FloatPair, operation: IntMatrix2) -> FloatPair:
        return (
            operation[0][0] * value[0] + operation[0][1] * value[1],
            operation[1][0] * value[0] + operation[1][1] * value[1],
        )

    @staticmethod
    def _reduce(value: FloatPair) -> FloatPair:
        return value[0] % 1.0, value[1] % 1.0

    @staticmethod
    def _maximum(matrix: ComplexMatrix) -> float:
        return float(np.max(np.abs(matrix), initial=0.0))

    @staticmethod
    def _support_digest(matrix: ComplexMatrix) -> str:
        support = np.argwhere(np.abs(matrix) > 1.0e-12)
        return hashlib.sha256(
            np.ascontiguousarray(support, dtype="<i8").tobytes()
        ).hexdigest()

    def _difference(
        self, record: dict[str, JsonValue], key: str, expected: float
    ) -> float:
        return abs(self._json.real(record[key], key) - expected)

    def _read(self, path: Path, name: str) -> dict[str, JsonValue]:
        return self._json.mapping(
            cast(JsonValue, json.loads(path.read_text(encoding="utf-8"))), name
        )

    @staticmethod
    def _repository_revision(root: Path) -> str:
        marker = root / ".git"
        if marker.is_file():
            text = marker.read_text().strip()
            if not text.startswith("gitdir: "):
                raise ValueError("verification repository gitdir marker differs")
            represented = Path(text.removeprefix("gitdir: "))
            git_directory = (
                represented if represented.is_absolute() else root / represented
            ).resolve(strict=True)
        elif marker.is_dir():
            git_directory = marker.resolve(strict=True)
        else:
            raise ValueError("verification repository Git metadata is absent")
        head = (git_directory / "HEAD").read_text().strip()
        if not head.startswith("ref: "):
            return IndependentStageCParentVerifier._object_id(head)
        reference = head.removeprefix("ref: ")
        common_marker = git_directory / "commondir"
        common_directory = (
            (git_directory / common_marker.read_text().strip()).resolve(strict=True)
            if common_marker.is_file()
            else git_directory
        )
        for directory in (git_directory, common_directory):
            candidate = directory / reference
            if candidate.is_file():
                return IndependentStageCParentVerifier._object_id(
                    candidate.read_text().strip()
                )
        packed = common_directory / "packed-refs"
        if packed.is_file():
            for line in packed.read_text().splitlines():
                if not line or line.startswith(("#", "^")):
                    continue
                object_id, represented_reference = line.split(" ", maxsplit=1)
                if represented_reference == reference:
                    return IndependentStageCParentVerifier._object_id(object_id)
        raise ValueError("verification repository HEAD reference is unresolved")

    @staticmethod
    def _object_id(value: str) -> str:
        if len(value) not in (40, 64) or any(
            character not in "0123456789abcdef" for character in value
        ):
            raise ValueError("verification repository HEAD object ID differs")
        return value

    @staticmethod
    def _inside(root: Path, represented: Path) -> Path:
        candidate = represented if represented.is_absolute() else root / represented
        result = candidate.resolve(strict=True)
        if not result.is_relative_to(root):
            raise ValueError("verification path escapes repository root")
        return result

    def _bound(self, root: Path, value: JsonValue, name: str) -> Path:
        represented = self._json.text(value, name)
        path = Path(represented)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"{name} must be canonical repository-relative")
        result = (root / path).resolve(strict=True)
        if result.relative_to(root).as_posix() != represented:
            raise ValueError(f"{name} is not canonical")
        return result

    def _bound_output(self, root: Path, value: JsonValue, name: str) -> Path:
        represented = self._json.text(value, name)
        path = Path(represented)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"{name} must be canonical repository-relative")
        result = (root / path).parent.resolve(strict=True) / path.name
        if not result.is_relative_to(root):
            raise ValueError(f"{name} escapes repository root")
        if result.relative_to(root).as_posix() != represented:
            raise ValueError(f"{name} is not canonical")
        return result

    @staticmethod
    def _digest(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    """Adapt argparse inputs into the independent verification action."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--accepted-parent-design", type=Path)
    fixtures = parser.add_mutually_exclusive_group()
    fixtures.add_argument("--authored-parent-fixture", type=Path)
    fixtures.add_argument("--authored-adapter-fixture", type=Path)
    parser.add_argument("--execution-authorization", type=Path)
    parser.add_argument("--repository-root", type=Path)
    parser.add_argument("--result", type=Path, required=True)
    arguments = parser.parse_args()
    fixture = (
        arguments.authored_parent_fixture
        if arguments.authored_parent_fixture is not None
        else arguments.authored_adapter_fixture
    )
    authored_mode = fixture is not None or arguments.accepted_parent_design is not None
    accepted_mode = (
        arguments.execution_authorization is not None
        or arguments.repository_root is not None
    )
    if authored_mode == accepted_mode:
        parser.error("select exactly one authored or accepted verification mode")
    verifier = IndependentStageCParentVerifier()
    if authored_mode:
        if fixture is None or arguments.accepted_parent_design is None:
            parser.error("authored verification requires design and fixture")
        report = verifier.execute(
            arguments.accepted_parent_design,
            fixture,
            arguments.result,
        )
    else:
        if (
            arguments.execution_authorization is None
            or arguments.repository_root is None
        ):
            parser.error("accepted verification requires authorization and root")
        report = verifier.execute_accepted(
            arguments.execution_authorization,
            arguments.repository_root,
            arguments.result,
        )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
