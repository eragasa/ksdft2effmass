"""Closed authorization decoding and fail-before-read validation for Stage C."""

from __future__ import annotations

import hashlib
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from .model import (
    ArtifactBinding,
    JsonValue,
    StageCAcceptedParentExecutionAuthorization,
)
from .records import ParentJsonReader

STAGE_DIRECTORY = Path(__file__).resolve(strict=True).parent.parent
RUNNER_PATH = STAGE_DIRECTORY / "run_stage_c_parent.py"
VERIFIER_PATH = STAGE_DIRECTORY / "verify_stage_c_parent.py"
PLOTTER_PATH = STAGE_DIRECTORY / "plot_stage_c_parent.py"
RESULT_SCHEMA_PATH = STAGE_DIRECTORY / "stage-c-result.schema.json"
AUTHORIZATION_SCHEMA_PATH = (
    STAGE_DIRECTORY / "stage-c-execution-authorization.schema.json"
)


class AcceptedParentStageCExecutionAuthorizationDeserializer:
    """Deserialize the exact closed future execution-authorization record."""

    __slots__ = ("_json",)

    _ARTIFACT_BINDINGS: ClassVar[tuple[tuple[str, str], ...]] = (
        (
            "accepted_parent_design",
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-accepted-parent-design.json",
        ),
        (
            "runner",
            "calculations/research-monograph/impurity-defect-2d/run_stage_c_parent.py",
        ),
        (
            "protected_workflow",
            "calculations/research-monograph/impurity-defect-2d/run_stage_c_parent.py",
        ),
        (
            "verifier",
            "calculations/research-monograph/impurity-defect-2d/"
            "verify_stage_c_parent.py",
        ),
        (
            "plotter",
            "calculations/research-monograph/impurity-defect-2d/plot_stage_c_parent.py",
        ),
        (
            "result_schema",
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-result.schema.json",
        ),
        (
            "execution_authorization_schema",
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-execution-authorization.schema.json",
        ),
        (
            "accepted_periodic_parent_input",
            "calculations/research-monograph/periodic-2d/input.json",
        ),
        (
            "accepted_periodic_parent_result",
            "calculations/research-monograph/periodic-2d/result.json",
        ),
        (
            "accepted_stage_a_prerequisite",
            "calculations/research-monograph/impurity-defect-2d/stage-a-result.json",
        ),
        (
            "accepted_stage_b_parent_and_route_evidence",
            "calculations/research-monograph/impurity-defect-2d/stage-b-result.json",
        ),
        (
            "accepted_execution_free_stage_c_contract",
            "calculations/research-monograph/impurity-defect-2d/stage-c-design.json",
        ),
    )
    OPERATION_INVENTORY: ClassVar[tuple[str, ...]] = (
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
    )

    def __init__(self) -> None:
        self._json = ParentJsonReader()

    def execute(self, path: Path) -> StageCAcceptedParentExecutionAuthorization:
        root = self._json.read(path)
        expected_keys = {
            "schema_version",
            "authorization_kind",
            "stage_id",
            "execution_authorized",
            "authorization_id",
            "checkpoint",
            "repository",
            "artifacts",
            "operation_inventory",
            "outputs",
            "resource_envelope",
            "attempt_policy",
        }
        if set(root) != expected_keys:
            raise ValueError("execution authorization field inventory differs")
        expected: dict[str, JsonValue] = {
            "schema_version": 1,
            "authorization_kind": "defect-2d-stage-c-accepted-parent-execution",
            "stage_id": "C_directional_and_nonlocal_model_classes",
            "execution_authorized": True,
        }
        for key, value in expected.items():
            if root.get(key) != value:
                raise ValueError(f"execution authorization field {key!r} differs")
        checkpoint = self._json.mapping(root["checkpoint"], "checkpoint")
        repository = self._json.mapping(root["repository"], "repository")
        outputs = self._json.mapping(root["outputs"], "outputs")
        resources = self._json.mapping(root["resource_envelope"], "resources")
        attempt = self._json.mapping(root["attempt_policy"], "attempt policy")
        artifact_records = self._json.records(root["artifacts"], "artifacts")
        operation_inventory = tuple(
            self._json.text(value, "operation")
            for value in self._json.array(
                root["operation_inventory"], "operation inventory"
            )
        )
        if operation_inventory != self.OPERATION_INVENTORY:
            raise ValueError("execution operation inventory differs")
        self._require_exact_keys(
            checkpoint,
            {"path", "sha256", "human_response_verbatim"},
            "checkpoint",
        )
        self._require_exact_keys(
            repository,
            {"root", "revision", "machine_identity", "native_artifact_root"},
            "repository",
        )
        self._require_exact_keys(
            outputs,
            {
                "attempt_record",
                "result",
                "verification_log",
                "summary_svg",
                "report",
                "native_evidence_manifest",
                "checksum_catalog",
            },
            "outputs",
        )
        self._require_exact_keys(
            resources,
            {
                "maximum_matrix_dimension",
                "maximum_execution_schedules",
                "maximum_route_evaluations",
                "maximum_bridge_records",
                "maximum_model_fit_records",
                "maximum_schedule_comparisons",
                "maximum_runtime_seconds",
                "maximum_peak_memory_gib",
                "maximum_retained_output_mib",
                "network_access",
                "external_executables",
                "new_dependencies",
            },
            "resource envelope",
        )
        self._require_exact_keys(
            attempt,
            {"maximum_attempts", "retry_authorized", "overwrite_existing"},
            "attempt policy",
        )
        for record in artifact_records:
            self._require_exact_keys(record, {"role", "path", "sha256"}, "artifact")
        artifacts = tuple(
            ArtifactBinding(
                self._json.text(record["role"], "artifact role"),
                self._json.text(record["path"], "artifact path"),
                self._sha256(record["sha256"], "artifact sha256"),
            )
            for record in artifact_records
        )
        if tuple((value.role, value.path) for value in artifacts) != (
            self._ARTIFACT_BINDINGS
        ):
            raise ValueError("execution authorization artifact bindings differ")
        external = tuple(
            self._json.text(value, "external executable")
            for value in self._json.array(
                resources["external_executables"], "external executables"
            )
        )
        dependencies = tuple(
            self._json.text(value, "new dependency")
            for value in self._json.array(resources["new_dependencies"], "dependencies")
        )
        return StageCAcceptedParentExecutionAuthorization(
            authorization_id=self._json.text(
                root["authorization_id"], "authorization_id"
            ),
            checkpoint_path=self._json.text(checkpoint["path"], "checkpoint path"),
            checkpoint_sha256=self._sha256(checkpoint["sha256"], "checkpoint sha256"),
            human_response_verbatim=self._json.text(
                checkpoint["human_response_verbatim"], "human response"
            ),
            repository_root=self._json.text(repository["root"], "repository root"),
            repository_revision=self._revision(repository["revision"]),
            machine_identity=self._json.text(
                repository["machine_identity"], "machine identity"
            ),
            native_artifact_root=self._json.text(
                repository["native_artifact_root"], "native artifact root"
            ),
            artifacts=artifacts,
            operation_inventory=operation_inventory,
            attempt_record_path=self._json.text(
                outputs["attempt_record"], "attempt record path"
            ),
            result_path=self._json.text(outputs["result"], "result path"),
            verification_log_path=self._json.text(
                outputs["verification_log"], "verification log path"
            ),
            summary_svg_path=self._json.text(
                outputs["summary_svg"], "summary SVG path"
            ),
            report_path=self._json.text(outputs["report"], "report path"),
            native_evidence_manifest_path=self._json.text(
                outputs["native_evidence_manifest"], "native manifest path"
            ),
            checksum_catalog_path=self._json.text(
                outputs["checksum_catalog"], "checksum catalog path"
            ),
            maximum_matrix_dimension=self._json.integer(
                resources["maximum_matrix_dimension"], "maximum matrix dimension"
            ),
            maximum_execution_schedules=self._json.integer(
                resources["maximum_execution_schedules"], "maximum schedules"
            ),
            maximum_route_evaluations=self._json.integer(
                resources["maximum_route_evaluations"], "maximum route evaluations"
            ),
            maximum_bridge_records=self._json.integer(
                resources["maximum_bridge_records"], "maximum bridge records"
            ),
            maximum_model_fit_records=self._json.integer(
                resources["maximum_model_fit_records"], "maximum model fits"
            ),
            maximum_schedule_comparisons=self._json.integer(
                resources["maximum_schedule_comparisons"],
                "maximum schedule comparisons",
            ),
            maximum_runtime_seconds=self._json.integer(
                resources["maximum_runtime_seconds"], "maximum runtime"
            ),
            maximum_peak_memory_gib=self._json.real(
                resources["maximum_peak_memory_gib"], "maximum memory"
            ),
            maximum_retained_output_mib=self._json.real(
                resources["maximum_retained_output_mib"], "maximum output"
            ),
            network_access=self._json.boolean(
                resources["network_access"], "network access"
            ),
            external_executables=external,
            new_dependencies=dependencies,
            maximum_attempts=self._json.integer(
                attempt["maximum_attempts"], "maximum attempts"
            ),
            retry_authorized=self._json.boolean(
                attempt["retry_authorized"], "retry authorized"
            ),
            overwrite_existing=self._json.boolean(
                attempt["overwrite_existing"], "overwrite existing"
            ),
        )

    @staticmethod
    def _require_exact_keys(
        value: dict[str, JsonValue], expected: set[str], label: str
    ) -> None:
        if set(value) != expected:
            raise ValueError(f"{label} must use the exact closed fields")

    def _revision(self, value: JsonValue) -> str:
        revision = self._json.text(value, "repository revision")
        if len(revision) not in (40, 64) or any(
            character not in "0123456789abcdef" for character in revision
        ):
            raise ValueError("repository revision is not a lowercase object ID")
        return revision

    def _sha256(self, value: JsonValue, name: str) -> str:
        digest = self._json.text(value, name)
        if len(digest) != 64 or any(
            character not in "0123456789abcdef" for character in digest
        ):
            raise ValueError(f"{name} is not lowercase SHA-256")
        return digest


@dataclass(frozen=True, slots=True)
class StageCOperationPaths:
    """Own canonical retained paths for one complete protected operation."""

    attempt_record: Path
    result: Path
    verification_log: Path
    summary_svg: Path
    report: Path
    native_evidence_manifest: Path
    checksum_catalog: Path

    @classmethod
    def authored(cls, directory: Path) -> StageCOperationPaths:
        """Return the complete authored-sandbox retained path inventory."""

        return cls(
            directory / "stage-c-accepted-parent-attempt.jsonl",
            directory / "stage-c-accepted-parent-result.json",
            directory / "stage-c-accepted-parent-verification.log",
            directory / "stage-c-accepted-parent-summary.svg",
            directory / "stage-c-accepted-parent-report.md",
            directory / "stage-c-accepted-parent-native-evidence-manifest.json",
            directory / "stage-c-accepted-parent-SHA256SUMS",
        )

    def produced_outputs(self) -> tuple[tuple[str, Path], ...]:
        """Return outputs covered by the finalized checksum catalog."""

        return (
            ("result", self.result),
            ("verification_log", self.verification_log),
            ("summary_svg", self.summary_svg),
            ("report", self.report),
            ("native_evidence_manifest", self.native_evidence_manifest),
        )


@dataclass(frozen=True, slots=True)
class ValidatedStageCExecution:
    """Carry validated authority, canonical artifacts, and retained paths."""

    authorization: StageCAcceptedParentExecutionAuthorization
    authorization_path: Path
    artifact_paths: tuple[tuple[str, Path], ...]
    outputs: StageCOperationPaths


class AcceptedParentStageCAuthorityValidator:
    """Validate complete authority before semantic accepted-parent reads."""

    __slots__ = ("_deserializer", "_json")

    DATA_ROLES: ClassVar[frozenset[str]] = frozenset(
        {
            "accepted_periodic_parent_input",
            "accepted_periodic_parent_result",
            "accepted_stage_a_prerequisite",
            "accepted_stage_b_parent_and_route_evidence",
            "accepted_execution_free_stage_c_contract",
        }
    )

    def __init__(self) -> None:
        self._deserializer = AcceptedParentStageCExecutionAuthorizationDeserializer()
        self._json = ParentJsonReader()

    def execute(
        self,
        design_path: Path,
        authorization_path: Path,
        repository_root: Path,
        output_path: Path,
    ) -> ValidatedStageCExecution:
        root = repository_root.resolve(strict=True)
        if not repository_root.is_absolute() or root != repository_root:
            raise ValueError("repository root must be canonical and absolute")
        authorization_file = self._existing(root, authorization_path)
        if authorization_file.relative_to(root).as_posix() != (
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-accepted-parent-execution-authorization.json"
        ):
            raise ValueError("execution authorization path differs")
        authorization = self._deserializer.execute(authorization_file)
        if authorization.authorization_id != (
            "research-monograph.impurity-defect-2d.stage-c."
            "accepted-parent-execution.hc17.v1"
        ):
            raise ValueError("execution authorization identity differs")
        if authorization.checkpoint_path != (
            ".pi/checkpoints/research-monograph-impurity-defect-2d-"
            "stage-c-accepted-parent-execution.json"
        ):
            raise ValueError("execution checkpoint path differs")
        if authorization.repository_root != (
            "/Users/eugene/worktrees/ksdft2effmass-calculations"
        ) or authorization.repository_root != str(root):
            raise ValueError("authorization repository root differs")
        if authorization.repository_revision != (
            "9def2718ee763faf2060eb692739600485de5c72"
        ) or authorization.repository_revision != self.repository_revision(root):
            raise ValueError("authorization repository revision differs")
        if authorization.machine_identity != "minerva" or (
            authorization.machine_identity != platform.node()
        ):
            raise ValueError("authorization machine identity differs")
        if authorization.native_artifact_root != (
            "/Users/eugene/projects/ksdft2effmass"
        ):
            raise ValueError("authorization native artifact root differs")
        native_root = Path(authorization.native_artifact_root).resolve(strict=True)
        if str(native_root) != authorization.native_artifact_root:
            raise ValueError("native artifact root must be canonical and existing")
        self._validate_resources(authorization)
        actual_outputs = (
            authorization.attempt_record_path,
            authorization.result_path,
            authorization.verification_log_path,
            authorization.summary_svg_path,
            authorization.report_path,
            authorization.native_evidence_manifest_path,
            authorization.checksum_catalog_path,
        )
        expected_outputs = (
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-accepted-parent-attempt.jsonl",
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-accepted-parent-result.json",
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-accepted-parent-verification.log",
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-accepted-parent-summary.svg",
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-accepted-parent-report.md",
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-accepted-parent-native-evidence-manifest.json",
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-accepted-parent-SHA256SUMS",
        )
        if actual_outputs != expected_outputs:
            raise ValueError("authorization retained output paths differ")
        resolved_outputs = tuple(
            self._bound_output(root, represented) for represented in actual_outputs
        )
        outputs = StageCOperationPaths(*resolved_outputs)
        actual_output = self._output(root, output_path)
        if actual_output != outputs.result:
            raise ValueError("authorization result path differs")
        for retained in resolved_outputs:
            if retained.exists():
                raise FileExistsError(
                    f"refusing consumed or existing output {retained}"
                )
        bindings = {value.role: value for value in authorization.artifacts}
        implementation_paths = {
            "accepted_parent_design": self._existing(root, design_path),
            "runner": RUNNER_PATH.resolve(strict=True),
            "protected_workflow": RUNNER_PATH.resolve(strict=True),
            "verifier": VERIFIER_PATH.resolve(strict=True),
            "plotter": PLOTTER_PATH.resolve(strict=True),
            "result_schema": RESULT_SCHEMA_PATH.resolve(strict=True),
            "execution_authorization_schema": AUTHORIZATION_SCHEMA_PATH.resolve(
                strict=True
            ),
        }
        artifact_paths: list[tuple[str, Path]] = []
        for role, path in implementation_paths.items():
            binding = bindings[role]
            self._validate_binding(root, binding, path)
            artifact_paths.append((role, path))
        checkpoint = self._bound_existing(root, authorization.checkpoint_path)
        if hashlib.sha256(checkpoint.read_bytes()).hexdigest() != (
            authorization.checkpoint_sha256
        ):
            raise ValueError("execution checkpoint identity differs")
        checkpoint_record = self._json.read(checkpoint)
        if checkpoint_record.get("status") != "resolved":
            raise ValueError("execution checkpoint is not resolved")
        if checkpoint_record.get("task_id") != (
            "research-monograph.exercises.impurity.defect-2d"
        ):
            raise ValueError("execution checkpoint task differs")
        if checkpoint_record.get("normalized_decision") != (
            "AUTHORIZE_ONE_ACCEPTED_PARENT_STAGE_C_EXECUTION"
        ):
            raise ValueError("checkpoint does not authorize accepted-parent Stage C")
        if checkpoint_record.get("human_response") != (
            authorization.human_response_verbatim
        ):
            raise ValueError("execution checkpoint response differs")
        artifact_paths.append(("checkpoint", checkpoint))
        for binding in authorization.artifacts:
            if binding.role in self.DATA_ROLES:
                artifact_paths.append(
                    (binding.role, self._bound_existing(root, binding.path))
                )
        return ValidatedStageCExecution(
            authorization, authorization_file, tuple(artifact_paths), outputs
        )

    @staticmethod
    def validate_accepted_input_identities(
        execution: ValidatedStageCExecution,
    ) -> None:
        bindings = {value.role: value for value in execution.authorization.artifacts}
        for role, path in execution.artifact_paths:
            if role not in AcceptedParentStageCAuthorityValidator.DATA_ROLES:
                continue
            if hashlib.sha256(path.read_bytes()).hexdigest() != bindings[role].sha256:
                raise ValueError(f"accepted input identity differs for {role}")

    @staticmethod
    def path(execution: ValidatedStageCExecution, role: str) -> Path:
        matches = tuple(
            path for found, path in execution.artifact_paths if found == role
        )
        if len(matches) != 1:
            raise ValueError(f"validated artifact {role!r} is not unique")
        return matches[0]

    def _validate_resources(
        self, authorization: StageCAcceptedParentExecutionAuthorization
    ) -> None:
        exact = (
            authorization.maximum_matrix_dimension,
            authorization.maximum_execution_schedules,
            authorization.maximum_route_evaluations,
            authorization.maximum_bridge_records,
            authorization.maximum_model_fit_records,
            authorization.maximum_schedule_comparisons,
        )
        if exact != (64, 2, 208, 104, 1040, 104):
            raise ValueError("authorization operation scale differs")
        if not 0 < authorization.maximum_runtime_seconds <= 600:
            raise ValueError("authorization runtime exceeds the design")
        if not 0.0 < authorization.maximum_peak_memory_gib <= 2.0:
            raise ValueError("authorization memory exceeds the design")
        if not 0.0 < authorization.maximum_retained_output_mib <= 20.0:
            raise ValueError("authorization output exceeds the design")
        if authorization.network_access:
            raise ValueError("network access is not authorized")
        if authorization.external_executables:
            raise ValueError("external executables are not authorized")
        if authorization.new_dependencies:
            raise ValueError("new dependencies are not authorized")
        if authorization.maximum_attempts != 1:
            raise ValueError("authorization must bind exactly one attempt")
        if authorization.retry_authorized:
            raise ValueError("retry is not authorized")
        if authorization.overwrite_existing:
            raise ValueError("overwrite is not authorized")

    def _validate_binding(
        self, root: Path, binding: ArtifactBinding, actual: Path
    ) -> None:
        if self._bound_existing(root, binding.path) != actual:
            raise ValueError(f"authorization path differs for {binding.role}")
        if hashlib.sha256(actual.read_bytes()).hexdigest() != binding.sha256:
            raise ValueError(f"authorization identity differs for {binding.role}")

    @staticmethod
    def repository_revision(root: Path) -> str:
        marker = root / ".git"
        if marker.is_file():
            text = marker.read_text().strip()
            prefix = "gitdir: "
            if not text.startswith(prefix):
                raise ValueError("repository gitdir marker differs")
            represented = Path(text.removeprefix(prefix))
            git_directory = (
                represented if represented.is_absolute() else root / represented
            ).resolve(strict=True)
        elif marker.is_dir():
            git_directory = marker.resolve(strict=True)
        else:
            raise ValueError("repository Git metadata is absent")
        head = (git_directory / "HEAD").read_text().strip()
        if not head.startswith("ref: "):
            return AcceptedParentStageCAuthorityValidator._object_id(head)
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
                return AcceptedParentStageCAuthorityValidator._object_id(
                    candidate.read_text().strip()
                )
        packed = common_directory / "packed-refs"
        if packed.is_file():
            for line in packed.read_text().splitlines():
                if not line or line.startswith(("#", "^")):
                    continue
                object_id, represented_reference = line.split(" ", maxsplit=1)
                if represented_reference == reference:
                    return AcceptedParentStageCAuthorityValidator._object_id(object_id)
        raise ValueError("repository HEAD reference is unresolved")

    @staticmethod
    def _object_id(value: str) -> str:
        if len(value) not in (40, 64) or any(
            character not in "0123456789abcdef" for character in value
        ):
            raise ValueError("repository HEAD is not a lowercase object ID")
        return value

    @staticmethod
    def _existing(root: Path, represented: Path) -> Path:
        candidate = represented if represented.is_absolute() else root / represented
        result = candidate.resolve(strict=True)
        if not result.is_relative_to(root):
            raise ValueError("path escapes repository root")
        return result

    @staticmethod
    def _output(root: Path, represented: Path) -> Path:
        candidate = represented if represented.is_absolute() else root / represented
        result = candidate.parent.resolve(strict=True) / candidate.name
        if not result.is_relative_to(root):
            raise ValueError("output escapes repository root")
        return result

    @staticmethod
    def _bound_existing(root: Path, represented: str) -> Path:
        path = Path(represented)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("bound path must be canonical repository-relative")
        result = (root / path).resolve(strict=True)
        if result.relative_to(root).as_posix() != represented:
            raise ValueError("bound path is not canonical")
        return result

    @staticmethod
    def _bound_output(root: Path, represented: str) -> Path:
        path = Path(represented)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("bound output must be canonical repository-relative")
        result = (root / path).parent.resolve(strict=True) / path.name
        if not result.is_relative_to(root):
            raise ValueError("bound output escapes repository root")
        if result.relative_to(root).as_posix() != represented:
            raise ValueError("bound output is not canonical")
        return result
