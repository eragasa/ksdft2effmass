"""Manifest-driven project composition over Quantum ESPRESSO integration owners.

The public request names one exact JSON manifest. ``QuantumEspressoPlanner`` decodes
that manifest into integration-owned immutable records and ActionObjects, returning a
``QuantumEspressoExecution`` composition. QE syntax, staging, process control, stream
capture, and workspace observation remain owned by
:mod:`ksdft2effmass.integration.quantum_espresso`.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import cast

from ksdft2effmass.integration.quantum_espresso import (
    LocalQuantumEspressoArtifactSource,
    LocalQuantumEspressoExecutionLimits,
    LocalQuantumEspressoExecutionPlan,
    LocalQuantumEspressoExecutionPreparationRequest,
    LocalQuantumEspressoPeakResidentBytesUnlimited,
    LocalQuantumEspressoStreamArtifactBindings,
    QuantumEspressoArtifactDestination,
    QuantumEspressoDiagnosticClassifierIdentity,
    QuantumEspressoDiagnosticReportIdentity,
    QuantumEspressoExecutableConfiguration,
    QuantumEspressoExecutableConfigurationIdentity,
    QuantumEspressoExecutableKind,
    QuantumEspressoExecutionInput,
    QuantumEspressoExecutionInputIdentity,
    QuantumEspressoFileArtifactContent,
    QuantumEspressoNativeInputArtifact,
    QuantumEspressoNativeOutputCandidateSpecification,
    QuantumEspressoNativeOutputExtractionSpecification,
    QuantumEspressoNativeOutputRole,
    QuantumEspressoProgram,
    QuantumEspressoPseudopotentialArtifact,
    QuantumEspressoTerminalRecordIdentity,
    QuantumEspressoWorkspaceEntryType,
)
from ksdft2effmass.workflows import (
    ArtifactContentIdentity,
    ArtifactIdentity,
    ArtifactManifestEntryIdentity,
    AttemptIdentity,
    DispatchDestinationIdentity,
    DispatchResourceScopeIdentity,
    ExecutionGrantIdentity,
    ExecutionGrantRevisionIdentity,
    ObligationIdentity,
    OperationIdentity,
    ResultObjectIdentity,
    ResultObjectReferenceIdentity,
    ScientificExecutionAuthorityReference,
    ScientificExecutionAuthoritySnapshotIdentity,
    ScientificExecutionAuthorityStateIdentity,
    ScientificExecutorIdentity,
    SimulationDispatchEntryIdentity,
    SimulationDispatchObservationIdentity,
    SimulationDispatchOutcomeIdentity,
    SimulationExecutionAuthorizationResultIdentity,
    SimulationExecutionRequestIdentity,
    TaskActivationIdentity,
    TaskDefinitionIdentity,
    TaskInstanceIdentity,
    TaskInvocationFailureIdentity,
    WorkflowRunIdentity,
    WorkflowRunRevisionIdentity,
)

from .execution import (
    QuantumEspressoBundledExampleExecutionPlan,
    QuantumEspressoBundledExampleExecutionWorkflow,
)
from .run_identity import QuantumEspressoBundledExampleRunIdentity

_EXECUTION_MANIFEST_SCHEMA_IDENTITY = (
    "quantum-espresso-execution-manifest:v2.20260921T155105Z"
)

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoExecutionRequest:
    """Name one exact manifest supplying the complete simulation composition.

    Parameters
    ----------
    manifest_path
        Absolute path to a nonsymlink regular JSON manifest. The manifest owns run,
        source, destination, resource, environment, and correlation values. This
        request performs no file access or execution.
    """

    manifest_path: Path

    def __post_init__(self) -> None:
        if not isinstance(self.manifest_path, Path):
            raise TypeError("manifest_path must be pathlib.Path")
        if not self.manifest_path.is_absolute():
            raise ValueError("manifest_path must be absolute")


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoExecution:
    """Bind project correlation and local effect plans to a blocked direct Workflow."""

    plan: QuantumEspressoBundledExampleExecutionPlan
    local_execution_plan: LocalQuantumEspressoExecutionPlan
    workflow: QuantumEspressoBundledExampleExecutionWorkflow

    def __post_init__(self) -> None:
        if type(self.plan) is not QuantumEspressoBundledExampleExecutionPlan:
            raise TypeError("plan must be QuantumEspressoBundledExampleExecutionPlan")
        if type(self.local_execution_plan) is not LocalQuantumEspressoExecutionPlan:
            raise TypeError(
                "local_execution_plan must be LocalQuantumEspressoExecutionPlan"
            )
        if type(self.workflow) is not QuantumEspressoBundledExampleExecutionWorkflow:
            raise TypeError(
                "workflow must be QuantumEspressoBundledExampleExecutionWorkflow"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoExecutionManifest:
    """Represent one completely decoded dated schema-v2 composition."""

    schema_identity: str
    run_identity: QuantumEspressoBundledExampleRunIdentity
    development_decision_id: str
    authority_reference: ScientificExecutionAuthorityReference
    external_runs_root: Path
    execution_input: QuantumEspressoExecutionInput
    executable_configuration: QuantumEspressoExecutableConfiguration
    executable_path: Path
    executable_destination: QuantumEspressoArtifactDestination
    artifact_sources: tuple[LocalQuantumEspressoArtifactSource, ...]
    limits: LocalQuantumEspressoExecutionLimits
    stdout_destination: QuantumEspressoArtifactDestination
    stderr_destination: QuantumEspressoArtifactDestination
    before_snapshot_destination: QuantumEspressoArtifactDestination
    after_snapshot_destination: QuantumEspressoArtifactDestination
    terminal_record_destination: QuantumEspressoArtifactDestination
    work_destination: QuantumEspressoArtifactDestination
    result_destination: QuantumEspressoArtifactDestination
    simulation_execution_request_identity: SimulationExecutionRequestIdentity
    scientific_executor_identity: ScientificExecutorIdentity
    dispatch_destination_identity: DispatchDestinationIdentity
    dispatch_resource_scope_identity: DispatchResourceScopeIdentity
    authorization_result_identity: SimulationExecutionAuthorizationResultIdentity
    stream_artifacts: LocalQuantumEspressoStreamArtifactBindings
    extraction_specification: QuantumEspressoNativeOutputExtractionSpecification
    diagnostic_report_identity: QuantumEspressoDiagnosticReportIdentity
    result_object_identity: ResultObjectIdentity
    terminal_record_identity: QuantumEspressoTerminalRecordIdentity
    dispatch_observation_identity: SimulationDispatchObservationIdentity
    dispatch_outcome_identity: SimulationDispatchOutcomeIdentity
    task_failure_identity: TaskInvocationFailureIdentity
    workflow_run_identity: WorkflowRunIdentity
    obligation_identity: ObligationIdentity
    claim_authorization_result_identity: SimulationExecutionAuthorizationResultIdentity
    dispatch_entry_identity: SimulationDispatchEntryIdentity
    dispatch_entry_revision_identity: WorkflowRunRevisionIdentity
    input_result_reference_identities: tuple[ResultObjectReferenceIdentity, ...]
    input_artifact_entry_identities: tuple[ArtifactManifestEntryIdentity, ...]
    result_contract_version: str
    diagnostic_claim_boundary: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class QuantumEspressoExecutionManifestSerializer:
    """Decode the closed schema-v2 JSON manifest into typed integration records."""

    def deserialize(self, payload: bytes) -> QuantumEspressoExecutionManifest:
        """Decode exact UTF-8 JSON bytes and reject unknown or malformed fields."""
        if type(payload) is not bytes:
            raise TypeError("payload must be built-in bytes")
        try:
            decoded: object = json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("manifest must contain valid UTF-8 JSON") from exc
        root = self._object(self._json_value(decoded), "manifest")
        self._keys(
            root,
            {
                "schema_version",
                "schema_identity",
                "run",
                "authority",
                "sources",
                "execution",
                "dispatch",
                "native_outputs",
            },
            "manifest",
        )
        if self._integer(root, "schema_version", "manifest") != 2:
            raise ValueError("manifest schema_version must equal 2")
        schema_identity = self._string(root, "schema_identity", "manifest")
        if schema_identity != _EXECUTION_MANIFEST_SCHEMA_IDENTITY:
            raise ValueError(
                "manifest schema_identity must equal "
                f"{_EXECUTION_MANIFEST_SCHEMA_IDENTITY!r}"
            )
        run = self._object(root["run"], "run")
        self._keys(
            run,
            {"task_id", "release", "workspace_created_at", "external_runs_root"},
            "run",
        )
        try:
            created_at = datetime.fromisoformat(
                self._string(run, "workspace_created_at", "run").replace("Z", "+00:00")
            )
        except ValueError as exc:
            raise ValueError("run.workspace_created_at must be ISO-8601 text") from exc
        run_identity = QuantumEspressoBundledExampleRunIdentity(
            task_id=self._string(run, "task_id", "run"),
            release=self._string(run, "release", "run"),
            workspace_created_at=created_at,
        )
        external_runs_root = self._absolute_path(
            self._string(run, "external_runs_root", "run"),
            "run.external_runs_root",
        )
        authority = self._object(root["authority"], "authority")
        self._keys(
            authority,
            {
                "development_decision_id",
                "grant_identity",
                "grant_revision_identity",
                "snapshot_identity",
                "state_identity",
            },
            "authority",
        )
        development_decision_id = self._string(
            authority, "development_decision_id", "authority"
        )
        authority_reference = ScientificExecutionAuthorityReference(
            grant_identity=ExecutionGrantIdentity(
                self._string(authority, "grant_identity", "authority")
            ),
            grant_revision_identity=ExecutionGrantRevisionIdentity(
                self._string(authority, "grant_revision_identity", "authority")
            ),
            snapshot_identity=ScientificExecutionAuthoritySnapshotIdentity(
                self._string(authority, "snapshot_identity", "authority")
            ),
            state_identity=ScientificExecutionAuthorityStateIdentity(
                self._string(authority, "state_identity", "authority")
            ),
        )
        sources = self._object(root["sources"], "sources")
        self._keys(
            sources, {"executable", "native_input", "pseudopotentials"}, "sources"
        )
        executable = self._source(sources["executable"], "sources.executable")
        native = self._artifact_source(
            sources["native_input"], "sources.native_input", native=True
        )
        pseudo_values = self._array(sources["pseudopotentials"], "pseudopotentials")
        if not pseudo_values:
            raise ValueError("sources.pseudopotentials must not be empty")
        pseudos = tuple(
            self._artifact_source(
                value, f"sources.pseudopotentials[{index}]", native=False
            )
            for index, value in enumerate(pseudo_values)
        )
        artifacts = (native[0], *(value[0] for value in pseudos))
        artifact_sources = tuple(
            sorted(
                (native[1], *(value[1] for value in pseudos)),
                key=lambda value: value.artifact.identity.value,
            )
        )
        execution = self._object(root["execution"], "execution")
        self._keys(
            execution,
            {
                "identities",
                "program",
                "executable_kind",
                "program_version",
                "argument_suffix",
                "environment_additions",
                "limits",
                "destinations",
                "contract_versions",
            },
            "execution",
        )
        identities = self._object(execution["identities"], "execution.identities")
        identity_names = {
            "execution_input",
            "task_instance",
            "activation",
            "operation",
            "attempt",
            "executable_configuration",
            "classifier",
            "simulation_execution_request",
            "scientific_executor",
            "dispatch_destination",
            "dispatch_resource_scope",
            "authorization_result",
            "stdout_artifact",
            "stderr_artifact",
        }
        self._keys(identities, identity_names, "execution.identities")
        program = QuantumEspressoProgram(
            self._string(execution, "program", "execution")
        )
        executable_kind = QuantumEspressoExecutableKind(
            self._string(execution, "executable_kind", "execution")
        )
        execution_input = QuantumEspressoExecutionInput(
            identity=QuantumEspressoExecutionInputIdentity(
                self._string(identities, "execution_input", "execution.identities")
            ),
            program=program,
            native_input=cast(QuantumEspressoNativeInputArtifact, artifacts[0]),
            pseudopotentials=tuple(
                cast(QuantumEspressoPseudopotentialArtifact, value)
                for value in artifacts[1:]
            ),
            predecessor_native_state=(),
            task_definition_identity=TaskDefinitionIdentity(run_identity.task_id),
            task_instance_identity=TaskInstanceIdentity(
                self._string(identities, "task_instance", "execution.identities")
            ),
            activation_identity=TaskActivationIdentity(
                self._string(identities, "activation", "execution.identities")
            ),
            operation_identity=OperationIdentity(
                self._string(identities, "operation", "execution.identities")
            ),
            attempt_identity=AttemptIdentity(
                self._string(identities, "attempt", "execution.identities")
            ),
            contract_version=self._string(
                self._object(execution["contract_versions"], "contract_versions"),
                "execution_input",
                "contract_versions",
            ),
        )
        configuration = QuantumEspressoExecutableConfiguration(
            identity=QuantumEspressoExecutableConfigurationIdentity(
                self._string(
                    identities, "executable_configuration", "execution.identities"
                )
            ),
            program=program,
            executable_kind=executable_kind,
            executable_content_identity=executable[1],
            program_version=self._string(execution, "program_version", "execution"),
            argument_suffix=tuple(
                self._string_value(value, "execution.argument_suffix")
                for value in self._array(
                    execution["argument_suffix"], "execution.argument_suffix"
                )
            ),
            environment_additions=self._environment_additions(
                execution["environment_additions"]
            ),
            classifier_identity=QuantumEspressoDiagnosticClassifierIdentity(
                self._string(identities, "classifier", "execution.identities")
            ),
            contract_version=self._string(
                self._object(execution["contract_versions"], "contract_versions"),
                "executable_configuration",
                "contract_versions",
            ),
        )
        limits = self._limits(execution["limits"])
        destinations = self._object(execution["destinations"], "execution.destinations")
        destination_names = {
            "executable",
            "stdout",
            "stderr",
            "before_snapshot",
            "after_snapshot",
            "terminal_record",
            "work",
            "result",
        }
        self._keys(destinations, destination_names, "execution.destinations")
        dispatch = self._object(root["dispatch"], "dispatch")
        self._keys(
            dispatch,
            {
                "workflow_run",
                "obligation",
                "claim_authorization_result",
                "dispatch_entry",
                "dispatch_entry_revision",
                "dispatch_outcome",
                "dispatch_observation",
                "task_failure",
                "diagnostic_report",
                "result_object",
                "terminal_record",
                "input_result_references",
                "input_artifact_entries",
                "result_contract_version",
                "diagnostic_claim_boundary",
            },
            "dispatch",
        )
        input_result_reference_identities = tuple(
            ResultObjectReferenceIdentity(
                self._string_value(value, "dispatch.input_result_references")
            )
            for value in self._array(
                dispatch["input_result_references"],
                "dispatch.input_result_references",
            )
        )
        input_artifact_entry_identities = tuple(
            ArtifactManifestEntryIdentity(
                self._string_value(value, "dispatch.input_artifact_entries")
            )
            for value in self._array(
                dispatch["input_artifact_entries"],
                "dispatch.input_artifact_entries",
            )
        )
        diagnostic_claim_boundary = tuple(
            self._string_value(value, "dispatch.diagnostic_claim_boundary")
            for value in self._array(
                dispatch["diagnostic_claim_boundary"],
                "dispatch.diagnostic_claim_boundary",
            )
        )
        native_outputs = self._object(root["native_outputs"], "native_outputs")
        self._keys(native_outputs, {"identity", "candidates"}, "native_outputs")
        candidates = tuple(
            sorted(
                (
                    self._output_candidate(value, index)
                    for index, value in enumerate(
                        self._array(
                            native_outputs["candidates"],
                            "native_outputs.candidates",
                        )
                    )
                ),
                key=lambda value: value.artifact_identity.value,
            )
        )
        extraction_specification = QuantumEspressoNativeOutputExtractionSpecification(
            identity=self._string(native_outputs, "identity", "native_outputs"),
            executable_configuration_identity=configuration.identity,
            program=configuration.program,
            executable_kind=configuration.executable_kind,
            program_version=configuration.program_version,
            candidates=candidates,
        )
        return QuantumEspressoExecutionManifest(
            schema_identity=schema_identity,
            run_identity=run_identity,
            development_decision_id=development_decision_id,
            authority_reference=authority_reference,
            external_runs_root=external_runs_root,
            execution_input=execution_input,
            executable_configuration=configuration,
            executable_path=executable[0],
            executable_destination=self._destination(destinations, "executable"),
            artifact_sources=artifact_sources,
            limits=limits,
            stdout_destination=self._destination(destinations, "stdout"),
            stderr_destination=self._destination(destinations, "stderr"),
            before_snapshot_destination=self._destination(
                destinations, "before_snapshot"
            ),
            after_snapshot_destination=self._destination(
                destinations, "after_snapshot"
            ),
            terminal_record_destination=self._destination(
                destinations, "terminal_record"
            ),
            work_destination=self._destination(destinations, "work"),
            result_destination=self._destination(destinations, "result"),
            simulation_execution_request_identity=SimulationExecutionRequestIdentity(
                self._string(
                    identities,
                    "simulation_execution_request",
                    "execution.identities",
                )
            ),
            scientific_executor_identity=ScientificExecutorIdentity(
                self._string(identities, "scientific_executor", "execution.identities")
            ),
            dispatch_destination_identity=DispatchDestinationIdentity(
                self._string(identities, "dispatch_destination", "execution.identities")
            ),
            dispatch_resource_scope_identity=DispatchResourceScopeIdentity(
                self._string(
                    identities, "dispatch_resource_scope", "execution.identities"
                )
            ),
            authorization_result_identity=(
                SimulationExecutionAuthorizationResultIdentity(
                    self._string(
                        identities, "authorization_result", "execution.identities"
                    )
                )
            ),
            stream_artifacts=LocalQuantumEspressoStreamArtifactBindings(
                stdout_artifact_identity=ArtifactIdentity(
                    self._string(identities, "stdout_artifact", "execution.identities")
                ),
                stderr_artifact_identity=ArtifactIdentity(
                    self._string(identities, "stderr_artifact", "execution.identities")
                ),
            ),
            extraction_specification=extraction_specification,
            diagnostic_report_identity=QuantumEspressoDiagnosticReportIdentity(
                self._string(dispatch, "diagnostic_report", "dispatch")
            ),
            result_object_identity=ResultObjectIdentity(
                self._string(dispatch, "result_object", "dispatch")
            ),
            terminal_record_identity=QuantumEspressoTerminalRecordIdentity(
                self._string(dispatch, "terminal_record", "dispatch")
            ),
            dispatch_observation_identity=SimulationDispatchObservationIdentity(
                self._string(dispatch, "dispatch_observation", "dispatch")
            ),
            dispatch_outcome_identity=SimulationDispatchOutcomeIdentity(
                self._string(dispatch, "dispatch_outcome", "dispatch")
            ),
            task_failure_identity=TaskInvocationFailureIdentity(
                self._string(dispatch, "task_failure", "dispatch")
            ),
            workflow_run_identity=WorkflowRunIdentity(
                self._string(dispatch, "workflow_run", "dispatch")
            ),
            obligation_identity=ObligationIdentity(
                self._string(dispatch, "obligation", "dispatch")
            ),
            claim_authorization_result_identity=(
                SimulationExecutionAuthorizationResultIdentity(
                    self._string(dispatch, "claim_authorization_result", "dispatch")
                )
            ),
            dispatch_entry_identity=SimulationDispatchEntryIdentity(
                self._string(dispatch, "dispatch_entry", "dispatch")
            ),
            dispatch_entry_revision_identity=WorkflowRunRevisionIdentity(
                self._string(dispatch, "dispatch_entry_revision", "dispatch")
            ),
            input_result_reference_identities=input_result_reference_identities,
            input_artifact_entry_identities=input_artifact_entry_identities,
            result_contract_version=self._string(
                dispatch, "result_contract_version", "dispatch"
            ),
            diagnostic_claim_boundary=diagnostic_claim_boundary,
        )

    def _output_candidate(
        self, value: JsonValue, index: int
    ) -> QuantumEspressoNativeOutputCandidateSpecification:
        context = f"native_outputs.candidates[{index}]"
        candidate = self._object(value, context)
        self._keys(
            candidate,
            {"artifact_identity", "role", "relative_path", "entry_type", "required"},
            context,
        )
        try:
            role = QuantumEspressoNativeOutputRole(
                self._string(candidate, "role", context)
            )
            entry_type = QuantumEspressoWorkspaceEntryType(
                self._string(candidate, "entry_type", context)
            )
        except ValueError as exc:
            raise ValueError(f"{context} contains an unsupported enum value") from exc
        return QuantumEspressoNativeOutputCandidateSpecification(
            artifact_identity=ArtifactIdentity(
                self._string(candidate, "artifact_identity", context)
            ),
            role=role,
            relative_path=QuantumEspressoArtifactDestination(
                self._string(candidate, "relative_path", context)
            ),
            entry_type=entry_type,
            required=self._boolean(candidate, "required", context),
        )

    def _source(
        self, value: JsonValue, context: str
    ) -> tuple[Path, ArtifactContentIdentity]:
        source = self._object(value, context)
        self._keys(source, {"path", "sha256", "byte_count"}, context)
        return (
            self._absolute_path(self._string(source, "path", context), context),
            ArtifactContentIdentity(
                "sha256",
                self._string(source, "sha256", context),
                self._integer(source, "byte_count", context),
            ),
        )

    def _artifact_source(
        self, value: JsonValue, context: str, *, native: bool
    ) -> tuple[
        QuantumEspressoNativeInputArtifact | QuantumEspressoPseudopotentialArtifact,
        LocalQuantumEspressoArtifactSource,
    ]:
        source = self._object(value, context)
        self._keys(
            source,
            {"identity", "destination", "path", "sha256", "byte_count"},
            context,
        )
        path, content_identity = self._source(
            {
                "path": source["path"],
                "sha256": source["sha256"],
                "byte_count": source["byte_count"],
            },
            context,
        )
        artifact_identity = ArtifactIdentity(self._string(source, "identity", context))
        content = QuantumEspressoFileArtifactContent(content_identity)
        destination = QuantumEspressoArtifactDestination(
            self._string(source, "destination", context)
        )
        artifact: (
            QuantumEspressoNativeInputArtifact | QuantumEspressoPseudopotentialArtifact
        )
        if native:
            artifact = QuantumEspressoNativeInputArtifact(
                identity=artifact_identity,
                content=content,
                destination=destination,
            )
        else:
            artifact = QuantumEspressoPseudopotentialArtifact(
                identity=artifact_identity,
                content=content,
                destination=destination,
            )
        return artifact, LocalQuantumEspressoArtifactSource(artifact, path)

    def _limits(self, value: JsonValue) -> LocalQuantumEspressoExecutionLimits:
        limits = self._object(value, "execution.limits")
        keys = {
            "wall_time_milliseconds",
            "termination_grace_milliseconds",
            "minimum_free_bytes",
            "maximum_created_entry_count",
            "maximum_created_total_bytes",
            "peak_resident_bytes",
        }
        self._keys(limits, keys, "execution.limits")
        if limits["peak_resident_bytes"] is not None:
            raise ValueError("execution.limits.peak_resident_bytes must be null")
        return LocalQuantumEspressoExecutionLimits(
            wall_time_milliseconds=self._integer(
                limits, "wall_time_milliseconds", "execution.limits"
            ),
            termination_grace_milliseconds=self._integer(
                limits, "termination_grace_milliseconds", "execution.limits"
            ),
            minimum_free_bytes=self._integer(
                limits, "minimum_free_bytes", "execution.limits"
            ),
            maximum_created_entry_count=self._integer(
                limits, "maximum_created_entry_count", "execution.limits"
            ),
            maximum_created_total_bytes=self._integer(
                limits, "maximum_created_total_bytes", "execution.limits"
            ),
            peak_resident_bytes=LocalQuantumEspressoPeakResidentBytesUnlimited(),
        )

    def _environment_additions(self, value: JsonValue) -> tuple[tuple[str, str], ...]:
        additions = []
        for index, item in enumerate(
            self._array(value, "execution.environment_additions")
        ):
            pair = self._array(item, f"environment_additions[{index}]")
            if len(pair) != 2:
                raise ValueError("each environment addition must contain two strings")
            additions.append(
                (
                    self._string_value(pair[0], "environment addition key"),
                    self._string_value(pair[1], "environment addition value"),
                )
            )
        return tuple(additions)

    def _destination(
        self, values: JsonObject, name: str
    ) -> QuantumEspressoArtifactDestination:
        return QuantumEspressoArtifactDestination(
            self._string(values, name, "execution.destinations")
        )

    @classmethod
    def _json_value(cls, value: object) -> JsonValue:
        if value is None or isinstance(value, bool | int | float | str):
            return value
        if type(value) is list:
            return [cls._json_value(item) for item in cast(list[object], value)]
        if type(value) is dict:
            result: JsonObject = {}
            for key, item in cast(dict[object, object], value).items():
                if type(key) is not str:
                    raise TypeError("JSON object keys must be strings")
                result[key] = cls._json_value(item)
            return result
        raise TypeError("manifest contains a value outside the JSON domain")

    @staticmethod
    def _object(value: JsonValue, context: str) -> JsonObject:
        if type(value) is not dict:
            raise TypeError(f"{context} must be a JSON object")
        return value

    @staticmethod
    def _array(value: JsonValue, context: str) -> list[JsonValue]:
        if type(value) is not list:
            raise TypeError(f"{context} must be a JSON array")
        return value

    @staticmethod
    def _keys(value: JsonObject, expected: set[str], context: str) -> None:
        if set(value) != expected:
            raise ValueError(f"{context} must contain exactly {sorted(expected)!r}")

    @staticmethod
    def _string(value: JsonObject, key: str, context: str) -> str:
        return QuantumEspressoExecutionManifestSerializer._string_value(
            value[key], f"{context}.{key}"
        )

    @staticmethod
    def _string_value(value: JsonValue, context: str) -> str:
        if type(value) is not str or not value:
            raise TypeError(f"{context} must be a nonempty string")
        return value

    @staticmethod
    def _boolean(value: JsonObject, key: str, context: str) -> bool:
        result = value[key]
        if type(result) is not bool:
            raise TypeError(f"{context}.{key} must be a built-in bool")
        return result

    @staticmethod
    def _integer(value: JsonObject, key: str, context: str) -> int:
        result = value[key]
        if type(result) is not int:
            raise TypeError(f"{context}.{key} must be a built-in integer")
        return result

    @staticmethod
    def _absolute_path(value: str, context: str) -> Path:
        path = Path(value)
        if not path.is_absolute():
            raise ValueError(f"{context} path must be absolute")
        return path


@dataclass(frozen=True, slots=True)
class QuantumEspressoPlanner:
    """Construct an integration-backed execution entirely from one JSON manifest."""

    serializer: QuantumEspressoExecutionManifestSerializer = (
        QuantumEspressoExecutionManifestSerializer()
    )

    def __post_init__(self) -> None:
        if type(self.serializer) is not QuantumEspressoExecutionManifestSerializer:
            raise TypeError(
                "serializer must be QuantumEspressoExecutionManifestSerializer"
            )

    def execute(
        self, request: QuantumEspressoExecutionRequest
    ) -> QuantumEspressoExecution:
        """Read one exact manifest and return a nonexecuting composition."""
        if type(request) is not QuantumEspressoExecutionRequest:
            raise TypeError("request must be QuantumEspressoExecutionRequest")
        path = request.manifest_path
        if path.is_symlink() or not path.is_file():
            raise ValueError("manifest_path must name a nonsymlink regular file")
        manifest = self.serializer.deserialize(path.read_bytes())
        preparation_request = LocalQuantumEspressoExecutionPreparationRequest(
            execution_input=manifest.execution_input,
            executable_configuration=manifest.executable_configuration,
            executable_path=manifest.executable_path,
            executable_content_identity=(
                manifest.executable_configuration.executable_content_identity
            ),
            executable_destination=manifest.executable_destination,
            authorized_run_root=manifest.external_runs_root.joinpath(
                *manifest.run_identity.relative_parent_path.parts
            ),
            attempt_workspace_name=manifest.run_identity.attempt_workspace_name,
            artifact_sources=manifest.artifact_sources,
            limits=manifest.limits,
            stdout_destination=manifest.stdout_destination,
            stderr_destination=manifest.stderr_destination,
            before_snapshot_destination=manifest.before_snapshot_destination,
            after_snapshot_destination=manifest.after_snapshot_destination,
            terminal_record_destination=manifest.terminal_record_destination,
            work_destination=manifest.work_destination,
            result_destination=manifest.result_destination,
            simulation_execution_request_identity=(
                manifest.simulation_execution_request_identity
            ),
            scientific_executor_identity=manifest.scientific_executor_identity,
            dispatch_destination_identity=manifest.dispatch_destination_identity,
            dispatch_resource_scope_identity=(
                manifest.dispatch_resource_scope_identity
            ),
            authorization_result_identity=manifest.authorization_result_identity,
        )
        plan = QuantumEspressoBundledExampleExecutionPlan(
            manifest_schema_identity=manifest.schema_identity,
            run_identity=manifest.run_identity,
            development_decision_id=manifest.development_decision_id,
            authority_reference=manifest.authority_reference,
            external_runs_root=manifest.external_runs_root,
            preparation_request=preparation_request,
            stream_artifacts=manifest.stream_artifacts,
        )
        local_execution_plan = LocalQuantumEspressoExecutionPlan(
            preparation_request=preparation_request,
            extraction_specification=manifest.extraction_specification,
            stream_artifacts=manifest.stream_artifacts,
            diagnostic_report_identity=manifest.diagnostic_report_identity,
            result_object_identity=manifest.result_object_identity,
            terminal_record_identity=manifest.terminal_record_identity,
            dispatch_observation_identity=manifest.dispatch_observation_identity,
            dispatch_outcome_identity=manifest.dispatch_outcome_identity,
            task_failure_identity=manifest.task_failure_identity,
            workflow_run_identity=manifest.workflow_run_identity,
            grant_identity=manifest.authority_reference.grant_identity,
            grant_authority_reference=manifest.authority_reference,
            obligation_identity=manifest.obligation_identity,
            claim_authorization_result_identity=(
                manifest.claim_authorization_result_identity
            ),
            dispatch_entry_identity=manifest.dispatch_entry_identity,
            dispatch_entry_revision_identity=(
                manifest.dispatch_entry_revision_identity
            ),
            input_result_reference_identities=(
                manifest.input_result_reference_identities
            ),
            input_artifact_entry_identities=manifest.input_artifact_entry_identities,
            result_contract_version=manifest.result_contract_version,
            diagnostic_claim_boundary=manifest.diagnostic_claim_boundary,
        )
        workflow = QuantumEspressoBundledExampleExecutionWorkflow()
        return QuantumEspressoExecution(
            plan=plan,
            local_execution_plan=local_execution_plan,
            workflow=workflow,
        )
