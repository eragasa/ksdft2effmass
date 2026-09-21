"""Typed deterministic local-QE executor support for control-lifecycle evidence."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from ksdft2effmass.integration.quantum_espresso import (
    LocalQuantumEspressoArtifactSource,
    LocalQuantumEspressoAttemptWorkspaceName,
    LocalQuantumEspressoExecutionLimits,
    LocalQuantumEspressoExecutionPlan,
    LocalQuantumEspressoExecutionPreparationRequest,
    LocalQuantumEspressoExecutionPreparer,
    LocalQuantumEspressoExecutor,
    LocalQuantumEspressoPeakResidentBytesUnlimited,
    LocalQuantumEspressoPreparationImplementationIdentity,
    LocalQuantumEspressoProcessRunner,
    LocalQuantumEspressoStreamArtifactBindings,
    LocalQuantumEspressoSupportedExecutableBinding,
    QuantumEspressoArtifactDestination,
    QuantumEspressoCalculatorOutcomeResolver,
    QuantumEspressoDiagnosticCatalog,
    QuantumEspressoDiagnosticClassifier,
    QuantumEspressoDiagnosticReportIdentity,
    QuantumEspressoExecutableConfiguration,
    QuantumEspressoExecutableConfigurationIdentity,
    QuantumEspressoExecutableKind,
    QuantumEspressoExecutionInput,
    QuantumEspressoExecutionInputIdentity,
    QuantumEspressoFileArtifactContent,
    QuantumEspressoInputStager,
    QuantumEspressoNativeInputArtifact,
    QuantumEspressoNativeOutputCandidateSpecification,
    QuantumEspressoNativeOutputCollector,
    QuantumEspressoNativeOutputExtractionSpecification,
    QuantumEspressoNativeOutputRole,
    QuantumEspressoProgram,
    QuantumEspressoPseudopotentialArtifact,
    QuantumEspressoTerminalRecordIdentity,
    QuantumEspressoTerminalRecordPublisher,
    QuantumEspressoTerminalRecordSerializer,
    QuantumEspressoWorkspaceEntryType,
    QuantumEspressoWorkspaceSnapshotter,
)
from ksdft2effmass.workflows import (
    ArtifactContentIdentity,
    ArtifactIdentity,
    ResultObjectIdentity,
    SimulationDispatchObservationIdentity,
    TaskInvocationFailureIdentity,
)
from ksdft2effmass.workflows.control.lifecycle import SimulationDispatchControlRequest


@dataclass(frozen=True, slots=True)
class LocalQuantumEspressoExecutorScenarioFactory:
    """Construct one executor exactly correlated to a synthetic control request."""

    @staticmethod
    def content_identity(path: Path) -> ArtifactContentIdentity:
        """Return the complete SHA-256 identity of one maintained resource."""
        content = path.read_bytes()
        return ArtifactContentIdentity(
            "sha256", hashlib.sha256(content).hexdigest(), len(content)
        )

    @staticmethod
    def resource(relative_path: str) -> Path:
        """Return one maintained integration fixture resource path."""
        return (
            Path(__file__).parents[3]
            / "integration"
            / "quantum_espresso"
            / "resources"
            / "local_execution"
            / relative_path
        ).resolve()

    @classmethod
    def execute(
        cls,
        run_root: Path,
        request: SimulationDispatchControlRequest,
    ) -> LocalQuantumEspressoExecutor:
        """Return a complete deterministic fixture executor for one control request."""
        if not isinstance(run_root, Path):
            raise TypeError("run_root must be pathlib.Path")
        if type(request) is not SimulationDispatchControlRequest:
            raise TypeError("request must be SimulationDispatchControlRequest")
        preparation = request.preparation_request
        activation = preparation.activation
        authorization = preparation.authorization_request
        grant = authorization.grant
        executable = cls.resource("executable/fixture_pw.py")
        native = cls.resource("input/pw.in")
        pseudo = cls.resource("pseudo/Si.fixture.UPF")
        executable_content = cls.content_identity(executable)
        native_artifact = QuantumEspressoNativeInputArtifact(
            identity=ArtifactIdentity("artifact.input"),
            content=QuantumEspressoFileArtifactContent(cls.content_identity(native)),
            destination=QuantumEspressoArtifactDestination("input/pw.in"),
        )
        pseudo_artifact = QuantumEspressoPseudopotentialArtifact(
            identity=ArtifactIdentity("artifact.pseudo"),
            content=QuantumEspressoFileArtifactContent(cls.content_identity(pseudo)),
            destination=QuantumEspressoArtifactDestination("pseudo/Si.fixture.UPF"),
        )
        execution_input = QuantumEspressoExecutionInput(
            identity=QuantumEspressoExecutionInputIdentity("qe.control-fixture.input"),
            program=QuantumEspressoProgram.PW,
            native_input=native_artifact,
            pseudopotentials=(pseudo_artifact,),
            predecessor_native_state=(),
            task_definition_identity=activation.task_instance.definition_identity,
            task_instance_identity=activation.task_instance.identity,
            activation_identity=activation.identity,
            operation_identity=activation.operation_identity,
            attempt_identity=activation.attempt_identity,
            contract_version="qe-execution-input:1",
        )
        catalog = QuantumEspressoDiagnosticCatalog.fixture_pw_v1()
        configuration = QuantumEspressoExecutableConfiguration(
            identity=QuantumEspressoExecutableConfigurationIdentity(
                "qe.control-fixture.configuration"
            ),
            program=QuantumEspressoProgram.PW,
            executable_kind=QuantumEspressoExecutableKind.DETERMINISTIC_FIXTURE,
            executable_content_identity=executable_content,
            program_version="fixture-pw-v1",
            argument_suffix=("--fixture-empty-stderr",),
            environment_additions=(("OMP_NUM_THREADS", "1"),),
            classifier_identity=catalog.classifier_identity,
            contract_version="qe-executable-configuration:1",
        )
        preparation_request = LocalQuantumEspressoExecutionPreparationRequest(
            execution_input=execution_input,
            executable_configuration=configuration,
            executable_path=executable,
            executable_content_identity=executable_content,
            executable_destination=QuantumEspressoArtifactDestination(
                "integration/executable"
            ),
            authorized_run_root=run_root,
            attempt_workspace_name=LocalQuantumEspressoAttemptWorkspaceName(
                "attempt-001"
            ),
            artifact_sources=(
                LocalQuantumEspressoArtifactSource(native_artifact, native),
                LocalQuantumEspressoArtifactSource(pseudo_artifact, pseudo),
            ),
            limits=LocalQuantumEspressoExecutionLimits(
                wall_time_milliseconds=2_000,
                termination_grace_milliseconds=100,
                minimum_free_bytes=0,
                maximum_created_entry_count=100,
                maximum_created_total_bytes=1_000_000,
                peak_resident_bytes=LocalQuantumEspressoPeakResidentBytesUnlimited(),
            ),
            stdout_destination=QuantumEspressoArtifactDestination("streams/stdout"),
            stderr_destination=QuantumEspressoArtifactDestination("streams/stderr"),
            before_snapshot_destination=QuantumEspressoArtifactDestination(
                "records/before.snapshot"
            ),
            after_snapshot_destination=QuantumEspressoArtifactDestination(
                "records/after.snapshot"
            ),
            terminal_record_destination=QuantumEspressoArtifactDestination(
                "records/terminal.json"
            ),
            work_destination=QuantumEspressoArtifactDestination("work"),
            result_destination=QuantumEspressoArtifactDestination("results"),
            simulation_execution_request_identity=authorization.request_identity,
            scientific_executor_identity=grant.executor_identity,
            dispatch_destination_identity=grant.destination_identity,
            dispatch_resource_scope_identity=grant.resource_scope_identities[0],
            authorization_result_identity=authorization.result_identity,
        )
        candidates = (
            QuantumEspressoNativeOutputCandidateSpecification(
                artifact_identity=ArtifactIdentity("artifact.stderr"),
                role=QuantumEspressoNativeOutputRole.STDERR,
                relative_path=preparation_request.stderr_destination,
                entry_type=QuantumEspressoWorkspaceEntryType.REGULAR_FILE,
                required=True,
            ),
            QuantumEspressoNativeOutputCandidateSpecification(
                artifact_identity=ArtifactIdentity("artifact.stdout"),
                role=QuantumEspressoNativeOutputRole.STDOUT,
                relative_path=preparation_request.stdout_destination,
                entry_type=QuantumEspressoWorkspaceEntryType.REGULAR_FILE,
                required=True,
            ),
        )
        extraction = QuantumEspressoNativeOutputExtractionSpecification(
            identity="qe-control-fixture-extraction:1",
            executable_configuration_identity=configuration.identity,
            program=configuration.program,
            executable_kind=configuration.executable_kind,
            program_version=configuration.program_version,
            candidates=candidates,
        )
        plan = LocalQuantumEspressoExecutionPlan(
            preparation_request=preparation_request,
            extraction_specification=extraction,
            stream_artifacts=LocalQuantumEspressoStreamArtifactBindings(
                stdout_artifact_identity=ArtifactIdentity("artifact.stdout"),
                stderr_artifact_identity=ArtifactIdentity("artifact.stderr"),
            ),
            diagnostic_report_identity=QuantumEspressoDiagnosticReportIdentity(
                "diagnostic-report.control-fixture"
            ),
            result_object_identity=ResultObjectIdentity("result.qe.control-fixture"),
            terminal_record_identity=QuantumEspressoTerminalRecordIdentity(
                "terminal.qe.control-fixture"
            ),
            dispatch_observation_identity=SimulationDispatchObservationIdentity(
                "dispatch-observation.qe.control-fixture"
            ),
            dispatch_outcome_identity=request.dispatch_outcome_identity,
            task_failure_identity=TaskInvocationFailureIdentity(
                "failure.qe.control-fixture"
            ),
            workflow_run_identity=grant.workflow_run_identity,
            grant_identity=grant.authority_reference.grant_identity,
            grant_authority_reference=grant.authority_reference,
            obligation_identity=authorization.obligation_identity,
            claim_authorization_result_identity=(
                request.claim_authorization_request.result_identity
            ),
            dispatch_entry_identity=request.dispatch_entry_identity,
            dispatch_entry_revision_identity=request.dispatch_entry_revision_identity,
            input_result_reference_identities=(grant.input_result_reference_identities),
            input_artifact_entry_identities=grant.input_artifact_entry_identities,
            result_contract_version="qe-pw-result:1",
            diagnostic_claim_boundary=(
                "synthetic fixture diagnostics establish software behavior only",
            ),
        )
        snapshotter = QuantumEspressoWorkspaceSnapshotter("qe-snapshotter:1")
        binding = LocalQuantumEspressoSupportedExecutableBinding(
            executable_configuration_identity=configuration.identity,
            executable_content_identity=configuration.executable_content_identity,
            program=configuration.program,
            executable_kind=configuration.executable_kind,
            program_version=configuration.program_version,
            classifier_identity=configuration.classifier_identity,
        )
        return LocalQuantumEspressoExecutor(
            plan=plan,
            preparer=LocalQuantumEspressoExecutionPreparer(
                LocalQuantumEspressoPreparationImplementationIdentity(
                    "qe-control-fixture-preparer:1"
                ),
                (binding,),
            ),
            stager=QuantumEspressoInputStager("qe-input-stager:1"),
            process_runner=LocalQuantumEspressoProcessRunner(
                observer_version="qe-process-observer:1",
                snapshotter=snapshotter,
            ),
            classifier=QuantumEspressoDiagnosticClassifier(catalog),
            collector=QuantumEspressoNativeOutputCollector("qe-output-collector:1"),
            outcome_resolver=QuantumEspressoCalculatorOutcomeResolver(
                "qe-outcome-resolver:1"
            ),
            terminal_serializer=QuantumEspressoTerminalRecordSerializer(),
            terminal_publisher=QuantumEspressoTerminalRecordPublisher(
                "qe-terminal-publisher:1", snapshotter
            ),
        )
