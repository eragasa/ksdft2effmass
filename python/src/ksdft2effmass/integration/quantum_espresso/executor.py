"""Authorized one-attempt orchestration for local Quantum ESPRESSO execution.

The Workflow dispatch adapter enters this ActionObject only after claim-phase
reauthorization and a successful dispatch-entry compare-and-swap.  This module
independently rechecks the complete executor-bound correlation before any workspace
mutation.  It performs no authority issuance, retry, resolution, scientific
acceptance, or executor discovery.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import final

from projectkoios.simulations.calculator.input import CalculatorInputRecord

from ksdft2effmass.workflows import (
    ArtifactManifestEntryIdentity,
    DispatchOutcomeKind,
    ExecutionGrantIdentity,
    ObligationIdentity,
    ResultObjectIdentity,
    ResultObjectReferenceIdentity,
    ScientificExecutionAuthorityReference,
    ScientificExecutorIdentity,
    SimulationDispatchEffectRequest,
    SimulationDispatchEntryIdentity,
    SimulationDispatchObservationIdentity,
    SimulationDispatchOutcome,
    SimulationDispatchOutcomeIdentity,
    SimulationExecutionAuthorizationResultIdentity,
    TaskInvocationFailure,
    TaskInvocationFailureIdentity,
    WorkflowRunIdentity,
    WorkflowRunRevisionIdentity,
)

from .calculator_input import (
    QeCalculatorInputAdmission,
    QeCalculatorInputAdmissionFailure,
    QeCalculatorInputAdmissionPolicyIdentity,
    QeCalculatorInputBinding,
)
from .contracts import (
    QeCalculatorFailedOutcome,
    QeCalculatorOutcome,
    QeCompletedOutcome,
    QeDiagnosticReport,
    QeDiagnosticReportIdentity,
    QeDiagnosticUnresolvedOutcome,
    QeProcessFailedOutcome,
    QeProgram,
    QePwResult,
    QeTerminalRecordIdentity,
)
from .diagnostics import (
    QeDiagnosticClassificationRequest,
    QeDiagnosticClassifier,
)
from .effects import (
    QeInputStager,
    QeNativeOutputCollectionFailure,
    QeNativeOutputCollector,
    QeNativeOutputExtractionSpecification,
    QeNativeOutputManifest,
    QePublishedTerminalRecord,
    QeStagedExecution,
    QeStagingFailure,
    QeTerminalPublicationFailure,
    QeTerminalRecord,
    QeTerminalRecordArtifact,
    QeTerminalRecordPublisher,
    QeTerminalRecordSerializer,
    QeTerminalStatus,
)
from .execution import (
    LocalQeExecutionPreparationRequest,
    LocalQeExecutionPreparer,
    LocalQePreparationFailure,
    LocalQePreparedExecution,
)
from .execution_evidence import (
    QePwEvidenceAdapter,
    QePwEvidencePublisher,
    QePwObservation,
    QePwObservationFailure,
    QePwPublicationFailure,
    QePwPublishedEvidence,
)
from .outcomes import QeCalculatorOutcomeResolver
from .process import (
    LocalQeCapturedProcess,
    LocalQeProcessFailure,
    LocalQeProcessFailureDisposition,
    LocalQeProcessRunner,
    LocalQeStreamArtifactBindings,
)
from .results import QePwResultAssembler, QePwResultAssemblyFailure


@dataclass(frozen=True, slots=True, kw_only=True)
class LocalQeExecutionPlan:
    """Bind one exact Workflow dispatch to caller-supplied QE result identities.

    Parameters
    ----------
    preparation_request
        Read-only local preparation input whose authority correlations are rechecked
        when the Workflow effect request arrives.
    calculator_input
        Exact immutable provider input instance admitted against the preparation
        request before any filesystem mutation or process entry.
    calculator_input_admission_policy_identity
        Exact KSD admission policy applied to the provider and Workflow correlation.
    extraction_specification, stream_artifacts
        Exact native-output candidates and distinct stdout/stderr artifact bindings.
    diagnostic_report_identity, result_object_identity, terminal_record_identity
        Caller-supplied immutable identities for the produced integration records.
    dispatch_observation_identity, dispatch_outcome_identity, task_failure_identity
        Caller-supplied Workflow envelope identities for every closed dispatch branch.
    workflow_run_identity, grant_identity, grant_authority_reference
        Expected Workflow run and exact versioned authority reference.
    obligation_identity, claim_authorization_result_identity
        Expected one-dispatch obligation and immediate claim authorization.
    dispatch_entry_identity, dispatch_entry_revision_identity
        Expected durable dispatch-entry state and committed revision.
    input_result_reference_identities, input_artifact_entry_identities
        Expected canonical Workflow input correlations.
    result_contract_version
        Nonempty contract identity for the program-specific ResultObject.
    diagnostic_claim_boundary
        Nonempty statements limiting what classified fixture or QE text establishes.

    Notes
    -----
    The plan conveys expected correlation and deterministic integration choices. It is
    neither an execution grant nor a reusable calculator configuration.
    """

    preparation_request: LocalQeExecutionPreparationRequest
    calculator_input: CalculatorInputRecord
    calculator_input_admission_policy_identity: QeCalculatorInputAdmissionPolicyIdentity
    extraction_specification: QeNativeOutputExtractionSpecification
    stream_artifacts: LocalQeStreamArtifactBindings
    diagnostic_report_identity: QeDiagnosticReportIdentity
    result_object_identity: ResultObjectIdentity
    terminal_record_identity: QeTerminalRecordIdentity
    dispatch_observation_identity: SimulationDispatchObservationIdentity
    dispatch_outcome_identity: SimulationDispatchOutcomeIdentity
    task_failure_identity: TaskInvocationFailureIdentity
    workflow_run_identity: WorkflowRunIdentity
    grant_identity: ExecutionGrantIdentity
    grant_authority_reference: ScientificExecutionAuthorityReference
    obligation_identity: ObligationIdentity
    claim_authorization_result_identity: SimulationExecutionAuthorizationResultIdentity
    dispatch_entry_identity: SimulationDispatchEntryIdentity
    dispatch_entry_revision_identity: WorkflowRunRevisionIdentity
    input_result_reference_identities: tuple[ResultObjectReferenceIdentity, ...]
    input_artifact_entry_identities: tuple[ArtifactManifestEntryIdentity, ...]
    result_contract_version: str
    diagnostic_claim_boundary: tuple[str, ...]

    def __post_init__(self) -> None:
        expected = (
            (
                self.preparation_request,
                LocalQeExecutionPreparationRequest,
                "preparation_request",
            ),
            (
                self.calculator_input,
                CalculatorInputRecord,
                "calculator_input",
            ),
            (
                self.calculator_input_admission_policy_identity,
                QeCalculatorInputAdmissionPolicyIdentity,
                "calculator_input_admission_policy_identity",
            ),
            (
                self.extraction_specification,
                QeNativeOutputExtractionSpecification,
                "extraction_specification",
            ),
            (
                self.stream_artifacts,
                LocalQeStreamArtifactBindings,
                "stream_artifacts",
            ),
            (
                self.diagnostic_report_identity,
                QeDiagnosticReportIdentity,
                "diagnostic_report_identity",
            ),
            (
                self.result_object_identity,
                ResultObjectIdentity,
                "result_object_identity",
            ),
            (
                self.terminal_record_identity,
                QeTerminalRecordIdentity,
                "terminal_record_identity",
            ),
            (
                self.dispatch_observation_identity,
                SimulationDispatchObservationIdentity,
                "dispatch_observation_identity",
            ),
            (
                self.dispatch_outcome_identity,
                SimulationDispatchOutcomeIdentity,
                "dispatch_outcome_identity",
            ),
            (
                self.task_failure_identity,
                TaskInvocationFailureIdentity,
                "task_failure_identity",
            ),
            (self.workflow_run_identity, WorkflowRunIdentity, "workflow_run_identity"),
            (self.grant_identity, ExecutionGrantIdentity, "grant_identity"),
            (
                self.grant_authority_reference,
                ScientificExecutionAuthorityReference,
                "grant_authority_reference",
            ),
            (self.obligation_identity, ObligationIdentity, "obligation_identity"),
            (
                self.claim_authorization_result_identity,
                SimulationExecutionAuthorizationResultIdentity,
                "claim_authorization_result_identity",
            ),
            (
                self.dispatch_entry_identity,
                SimulationDispatchEntryIdentity,
                "dispatch_entry_identity",
            ),
            (
                self.dispatch_entry_revision_identity,
                WorkflowRunRevisionIdentity,
                "dispatch_entry_revision_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        collections = (
            (
                self.input_result_reference_identities,
                ResultObjectReferenceIdentity,
                "input_result_reference_identities",
            ),
            (
                self.input_artifact_entry_identities,
                ArtifactManifestEntryIdentity,
                "input_artifact_entry_identities",
            ),
        )
        for values, member_type, name in collections:
            if type(values) is not tuple or any(
                type(value) is not member_type for value in values
            ):
                raise TypeError(f"{name} must contain {member_type.__name__} values")
            if values != tuple(sorted(values, key=lambda value: value.value)) or len(
                set(values)
            ) != len(values):
                raise ValueError(f"{name} must be unique and lexically sorted")
        if self.grant_authority_reference.grant_identity != self.grant_identity:
            raise ValueError("grant identity must agree with its authority reference")
        if type(self.result_contract_version) is not str:
            raise TypeError("result_contract_version must be a built-in str")
        if self.result_contract_version != "qe-pw-result:2":
            raise ValueError("result_contract_version must be qe-pw-result:2")
        boundary = self.diagnostic_claim_boundary
        if type(boundary) is not tuple or any(
            type(value) is not str for value in boundary
        ):
            raise TypeError(
                "diagnostic_claim_boundary must contain built-in str values"
            )
        if not boundary or any(not value for value in boundary):
            raise ValueError("diagnostic_claim_boundary must contain nonempty strings")
        request = self.preparation_request
        specification = self.extraction_specification
        configuration = request.executable_configuration
        if configuration.program is not QeProgram.PW:
            raise ValueError("local QE execution plan supports pw.x only")
        if (
            specification.executable_configuration_identity != configuration.identity
            or specification.program is not configuration.program
            or specification.executable_kind is not configuration.executable_kind
            or specification.program_version != configuration.program_version
        ):
            raise ValueError(
                "extraction specification must match executable configuration"
            )
        by_role = {
            candidate.role.value: candidate for candidate in specification.candidates
        }
        stdout = by_role.get("stdout")
        stderr = by_role.get("stderr")
        if (
            stdout is None
            or stderr is None
            or stdout.artifact_identity
            != self.stream_artifacts.stdout_artifact_identity
            or stderr.artifact_identity
            != self.stream_artifacts.stderr_artifact_identity
            or stdout.relative_path != request.stdout_destination
            or stderr.relative_path != request.stderr_destination
        ):
            raise ValueError("stream bindings must match extraction and preparation")


@dataclass(frozen=True, slots=True)
@final
class LocalQeExecutor:
    """Execute one authorized local QE attempt and adapt it to Workflow dispatch.

    Parameters
    ----------
    plan
        Exact one-attempt execution plan and expected Workflow correlations.
    preparer, stager, process_runner
        ActionObjects owning read-only preparation, no-replace staging, and at-most-
        once process entry with closed capture.
    evidence_adapter, evidence_publisher, result_assembler
        Provider observation adaptation, verified no-replace record publication, and
        fail-closed assembly of the Workflow-facing result.
    classifier, collector, outcome_resolver
        ActionObjects owning exact-stream diagnostics, candidate collection, and
        fail-closed calculator outcome resolution.
    terminal_serializer, terminal_publisher
        ActionObjects owning private canonical terminal bytes and atomic no-replace
        publication.

    Notes
    -----
    Workflow authority issuance, claim, dispatch-entry compare-and-swap, retry,
    resolution, and scientific acceptance remain outside this ActionObject.
    """

    plan: LocalQeExecutionPlan
    preparer: LocalQeExecutionPreparer
    stager: QeInputStager
    process_runner: LocalQeProcessRunner
    evidence_adapter: QePwEvidenceAdapter
    evidence_publisher: QePwEvidencePublisher
    result_assembler: QePwResultAssembler
    classifier: QeDiagnosticClassifier
    collector: QeNativeOutputCollector
    outcome_resolver: QeCalculatorOutcomeResolver
    terminal_serializer: QeTerminalRecordSerializer
    terminal_publisher: QeTerminalRecordPublisher

    def __post_init__(self) -> None:
        expected = (
            (self.plan, LocalQeExecutionPlan, "plan"),
            (self.preparer, LocalQeExecutionPreparer, "preparer"),
            (self.stager, QeInputStager, "stager"),
            (self.process_runner, LocalQeProcessRunner, "process_runner"),
            (
                self.evidence_adapter,
                QePwEvidenceAdapter,
                "evidence_adapter",
            ),
            (
                self.evidence_publisher,
                QePwEvidencePublisher,
                "evidence_publisher",
            ),
            (
                self.result_assembler,
                QePwResultAssembler,
                "result_assembler",
            ),
            (self.classifier, QeDiagnosticClassifier, "classifier"),
            (self.collector, QeNativeOutputCollector, "collector"),
            (
                self.outcome_resolver,
                QeCalculatorOutcomeResolver,
                "outcome_resolver",
            ),
            (
                self.terminal_serializer,
                QeTerminalRecordSerializer,
                "terminal_serializer",
            ),
            (
                self.terminal_publisher,
                QeTerminalRecordPublisher,
                "terminal_publisher",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        catalog = self.classifier.catalog
        configuration = self.plan.preparation_request.executable_configuration
        if (
            configuration.program is not QeProgram.PW
            or catalog.classifier_identity != configuration.classifier_identity
            or catalog.program is not configuration.program
            or catalog.executable_kind is not configuration.executable_kind
            or catalog.program_version != configuration.program_version
        ):
            raise ValueError(
                "classifier catalog must match the execution configuration"
            )

    @property
    def executor_identity(self) -> ScientificExecutorIdentity:
        """Return the exact Workflow executor identity accepted by this instance."""
        return self.plan.preparation_request.scientific_executor_identity

    def execute(
        self, request: SimulationDispatchEffectRequest
    ) -> SimulationDispatchOutcome:
        """Perform at most one process invocation after exact correlation checks."""
        if type(request) is not SimulationDispatchEffectRequest:
            raise TypeError("request must be SimulationDispatchEffectRequest")
        mismatch: str | None = self._correlation_mismatch(request)
        if mismatch is not None:
            return self._rejected(
                request, "authorization_correlation_mismatch", mismatch
            )

        input_binding: QeCalculatorInputBinding | QeCalculatorInputAdmissionFailure = (
            QeCalculatorInputAdmission(
                self.plan.calculator_input_admission_policy_identity
            ).execute(
                self.plan.calculator_input,
                self.plan.preparation_request.execution_input,
            )
        )
        if type(input_binding) is QeCalculatorInputAdmissionFailure:
            return self._rejected(
                request,
                "calculator_input_admission_failed",
                f"provider calculator input was rejected: {input_binding.code.value}",
            )
        if type(input_binding) is not QeCalculatorInputBinding:
            raise TypeError("calculator input admission returned an unsupported result")

        preparation: LocalQePreparedExecution | LocalQePreparationFailure = (
            self.preparer.execute(self.plan.preparation_request, input_binding)
        )
        if type(preparation) is LocalQePreparationFailure:
            return self._rejected(
                request,
                "preparation_failed",
                f"local QE preparation failed: {preparation.code.value}",
            )
        if type(preparation) is not LocalQePreparedExecution:
            raise TypeError("local QE preparation returned an unsupported result")
        staging: QeStagedExecution | QeStagingFailure = self.stager.execute(
            preparation, input_binding
        )
        if type(staging) is QeStagingFailure:
            return self._rejected(
                request,
                "staging_failed",
                f"local QE staging failed: {staging.code.value}",
            )
        if type(staging) is not QeStagedExecution:
            raise TypeError("local QE staging returned an unsupported result")
        process: LocalQeCapturedProcess | LocalQeProcessFailure = (
            self.process_runner.execute(
                preparation, staging, self.plan.stream_artifacts
            )
        )
        if type(process) is LocalQeProcessFailure:
            if process.disposition is LocalQeProcessFailureDisposition.REJECTED:
                return self._rejected(
                    request,
                    "process_entry_rejected",
                    f"local QE process entry failed: {process.code.value}",
                )
            return self._indeterminate(
                request,
                (
                    self.plan.dispatch_entry_identity.value,
                    preparation.identity.value,
                    staging.identity.value,
                    "qe-process-failure:" + process.code.value,
                ),
            )
        if type(process) is not LocalQeCapturedProcess:
            raise TypeError("local QE process runner returned an unsupported result")
        observation_binding: QePwObservation | QePwObservationFailure = (
            self.evidence_adapter.execute(preparation, process)
        )
        if type(observation_binding) is QePwObservationFailure:
            return self._indeterminate(
                request,
                (
                    process.observation.identity.value,
                    "qe-execution-evidence-adaptation-failure:"
                    + observation_binding.code.value,
                ),
            )
        if type(observation_binding) is not QePwObservation:
            raise TypeError(
                "QE execution evidence adapter returned an unsupported result"
            )
        execution_evidence: QePwPublishedEvidence | QePwPublicationFailure = (
            self.evidence_publisher.execute(observation_binding)
        )
        if type(execution_evidence) is QePwPublicationFailure:
            return self._indeterminate(
                request,
                (
                    process.observation.identity.value,
                    "qe-execution-record-publication-failure:"
                    + execution_evidence.code.value,
                ),
            )
        if type(execution_evidence) is not QePwPublishedEvidence:
            raise TypeError(
                "QE execution record publisher returned an unsupported result"
            )

        report: QeDiagnosticReport = self.classifier.execute(
            QeDiagnosticClassificationRequest(
                report_identity=self.plan.diagnostic_report_identity,
                configuration=self.plan.preparation_request.executable_configuration,
                stdout=process.stdout_bytes,
                stderr=process.stderr_bytes,
                stdout_content_identity=process.observation.stdout.content_identity,
                stderr_content_identity=process.observation.stderr.content_identity,
                claim_boundary=self.plan.diagnostic_claim_boundary,
            )
        )
        collection: QeNativeOutputManifest | QeNativeOutputCollectionFailure = (
            self.collector.execute(
                process.after_snapshot, self.plan.extraction_specification
            )
        )
        if type(collection) is QeNativeOutputCollectionFailure:
            return self._indeterminate(
                request,
                (
                    process.observation.identity.value,
                    process.after_snapshot.identity.value,
                    "qe-output-collection-failure:" + collection.code.value,
                ),
            )
        if type(collection) is not QeNativeOutputManifest:
            raise TypeError("QE output collection returned an unsupported result")
        outcome: QeCalculatorOutcome = self.outcome_resolver.execute(
            process.observation,
            report,
            collection,
            self.plan.extraction_specification,
        )
        terminal: QeTerminalRecord = QeTerminalRecord(
            identity=self.plan.terminal_record_identity,
            status=self._terminal_status(outcome),
            simulation_execution_request_identity=(
                self.plan.preparation_request.simulation_execution_request_identity
            ),
            execution_input_identity=(
                self.plan.preparation_request.execution_input.identity
            ),
            preparation_identity=preparation.identity,
            process_observation_identity=process.observation.identity,
            stdout_artifact_identity=process.observation.stdout.artifact_identity,
            stdout_content_identity=process.observation.stdout.content_identity,
            stderr_artifact_identity=process.observation.stderr.artifact_identity,
            stderr_content_identity=process.observation.stderr.content_identity,
            before_snapshot_identity=process.before_snapshot.identity,
            after_snapshot_identity=process.after_snapshot.identity,
            execution_record_manifest_entry_identity=(
                execution_evidence.publication_entry.identity
            ),
            execution_record_content_identity=execution_evidence.content_identity,
            execution_record_publication_snapshot_identity=(
                execution_evidence.publication_snapshot.identity
            ),
            diagnostic_report_identity=report.identity,
            native_output_manifest_identity=collection.identity,
        )
        terminal_artifact: QeTerminalRecordArtifact = self.terminal_serializer.execute(
            terminal
        )
        publication: QePublishedTerminalRecord | QeTerminalPublicationFailure = (
            self.terminal_publisher.execute(preparation, terminal_artifact)
        )
        if type(publication) is QeTerminalPublicationFailure:
            return self._indeterminate(
                request,
                (
                    process.observation.identity.value,
                    collection.identity.value,
                    terminal.identity.value,
                    "qe-terminal-publication-failure:" + publication.code.value,
                ),
            )
        if type(publication) is not QePublishedTerminalRecord:
            raise TypeError("QE terminal publication returned an unsupported result")
        result: QePwResult | QePwResultAssemblyFailure = self.result_assembler.execute(
            self.plan.result_object_identity,
            self.plan.result_contract_version,
            execution_evidence,
            report,
            self.plan.extraction_specification,
            collection,
            outcome,
            terminal,
            publication,
        )
        if type(result) is QePwResultAssemblyFailure:
            return self._indeterminate(
                request,
                (
                    process.observation.identity.value,
                    terminal.identity.value,
                    "qe-pw-result-assembly-failure:" + result.code.value,
                ),
            )
        if type(result) is not QePwResult:
            raise TypeError("QE result assembler returned an unsupported result")
        return self._confirmed(request, result, collection)

    def _correlation_mismatch(
        self, request: SimulationDispatchEffectRequest
    ) -> str | None:
        plan = self.plan
        preparation = plan.preparation_request
        execution_input = preparation.execution_input
        execution_request = request.execution_request
        correlation = execution_request.correlation
        obligation = execution_request.obligation
        claim = request.claim_authorization.request
        entry = request.dispatch_entry_receipt
        expected_resources = (preparation.dispatch_resource_scope_identity,)
        if (
            correlation.request_identity
            != preparation.simulation_execution_request_identity
        ):
            return "simulation request identity differs from the prepared request"
        if correlation.workflow_run_identity != plan.workflow_run_identity:
            return "workflow run identity differs from the execution plan"
        if (
            correlation.task_instance_identity != execution_input.task_instance_identity
            or correlation.activation_identity != execution_input.activation_identity
            or correlation.operation_identity != execution_input.operation_identity
            or correlation.attempt_identity != execution_input.attempt_identity
            or claim.task_definition_identity
            != execution_input.task_definition_identity
        ):
            return "Task or attempt identities differ from the QE execution input"
        if (
            correlation.executor_identity != preparation.scientific_executor_identity
            or correlation.executor_identity != self.executor_identity
        ):
            return "executor identity differs from the local QE executor"
        if (
            obligation.destination_identity != preparation.dispatch_destination_identity
            or claim.destination_identity != preparation.dispatch_destination_identity
        ):
            return "dispatch destination differs from the prepared destination"
        if (
            obligation.resource_scope_identities != expected_resources
            or claim.resource_scope_identities != expected_resources
        ):
            return "dispatch resources differ from the prepared resource scope"
        if (
            execution_request.preparation_authorization.identity
            != preparation.authorization_result_identity
            or correlation.authorization_result_identity
            != preparation.authorization_result_identity
        ):
            return "preparation authorization identity differs from the prepared value"
        if (
            correlation.grant_identity != plan.grant_identity
            or claim.grant.authority_reference != plan.grant_authority_reference
            or request.claim_authorization.identity
            != plan.claim_authorization_result_identity
            or correlation.obligation_identity != plan.obligation_identity
            or entry.dispatch_entry_identity != plan.dispatch_entry_identity
            or entry.committed_revision_identity
            != plan.dispatch_entry_revision_identity
        ):
            return (
                "grant, claim authorization, obligation, or dispatch-entry "
                "identity differs from the plan"
            )
        if (
            request.outcome_identity != plan.dispatch_outcome_identity
            or request.outcome_identity
            != request.dispatch_entry_receipt.outcome_identity
        ):
            return "dispatch outcome identity differs from the execution plan"
        if (
            correlation.input_result_reference_identities
            != plan.input_result_reference_identities
            or correlation.input_artifact_entry_identities
            != plan.input_artifact_entry_identities
        ):
            return "Workflow input identities differ from the execution plan"
        return None

    def _confirmed(
        self,
        request: SimulationDispatchEffectRequest,
        result: QePwResult,
        manifest: QeNativeOutputManifest,
    ) -> SimulationDispatchOutcome:
        values = request.execution_request.correlation
        return SimulationDispatchOutcome(
            identity=request.outcome_identity,
            observation_identity=self.plan.dispatch_observation_identity,
            request_identity=values.request_identity,
            workflow_run_identity=values.workflow_run_identity,
            task_instance_identity=values.task_instance_identity,
            activation_identity=values.activation_identity,
            operation_identity=values.operation_identity,
            attempt_identity=values.attempt_identity,
            executor_identity=values.executor_identity,
            obligation_identity=values.obligation_identity,
            grant_identity=values.grant_identity,
            kind=DispatchOutcomeKind.CONFIRMED,
            result=result,
            native_output_manifest_identity=manifest.identity,
            native_output_manifest_entry_identities=tuple(
                sorted(
                    (entry.identity for entry in manifest.entries),
                    key=lambda value: value.value,
                )
            ),
        )

    def _rejected(
        self,
        request: SimulationDispatchEffectRequest,
        code: str,
        diagnostic: str,
    ) -> SimulationDispatchOutcome:
        values = request.execution_request.correlation
        return SimulationDispatchOutcome(
            identity=request.outcome_identity,
            observation_identity=self.plan.dispatch_observation_identity,
            request_identity=values.request_identity,
            workflow_run_identity=values.workflow_run_identity,
            task_instance_identity=values.task_instance_identity,
            activation_identity=values.activation_identity,
            operation_identity=values.operation_identity,
            attempt_identity=values.attempt_identity,
            executor_identity=values.executor_identity,
            obligation_identity=values.obligation_identity,
            grant_identity=values.grant_identity,
            kind=DispatchOutcomeKind.REJECTED,
            failure=TaskInvocationFailure(
                identity=self.plan.task_failure_identity,
                code="quantum_espresso." + code,
                operation_phase="local_quantum_espresso_execution",
                diagnostic=diagnostic,
                retryable=None,
                claim_boundary=(
                    "this failure establishes no successful calculator invocation",
                    "retry eligibility and resolution remain Workflow-owned",
                ),
            ),
        )

    def _indeterminate(
        self,
        request: SimulationDispatchEffectRequest,
        reconciliation_identities: tuple[str, ...],
    ) -> SimulationDispatchOutcome:
        values = request.execution_request.correlation
        return SimulationDispatchOutcome(
            identity=request.outcome_identity,
            observation_identity=self.plan.dispatch_observation_identity,
            request_identity=values.request_identity,
            workflow_run_identity=values.workflow_run_identity,
            task_instance_identity=values.task_instance_identity,
            activation_identity=values.activation_identity,
            operation_identity=values.operation_identity,
            attempt_identity=values.attempt_identity,
            executor_identity=values.executor_identity,
            obligation_identity=values.obligation_identity,
            grant_identity=values.grant_identity,
            kind=DispatchOutcomeKind.INDETERMINATE,
            reconciliation_identity_values=tuple(
                sorted(set(reconciliation_identities))
            ),
        )

    @staticmethod
    def _terminal_status(
        outcome: QeCalculatorOutcome,
    ) -> QeTerminalStatus:
        if type(outcome) is QeCompletedOutcome:
            return QeTerminalStatus.COMPLETED
        if type(outcome) is QeCalculatorFailedOutcome:
            return QeTerminalStatus.CALCULATOR_FAILED
        if type(outcome) is QeProcessFailedOutcome:
            return QeTerminalStatus.PROCESS_FAILED
        if type(outcome) is QeDiagnosticUnresolvedOutcome:
            return QeTerminalStatus.DIAGNOSTIC_UNRESOLVED
        raise TypeError("outcome must be a closed QE calculator outcome")
