"""Final fail-closed assembly of one local QE ``pw.x`` Workflow result."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.workflows import ResultObjectIdentity

from ..contracts import (
    QeCalculatorFailedOutcome,
    QeCalculatorOutcome,
    QeCompletedOutcome,
    QeDiagnosticReport,
    QeDiagnosticUnresolvedOutcome,
    QeFileArtifactContent,
    QeOperationResultEvidence,
    QeProcessFailedOutcome,
    QeProgram,
    QePwResult,
)
from ..effects import (
    QeNativeOutputExtractionSpecification,
    QeNativeOutputManifest,
    QeNativeOutputRole,
    QePublishedTerminalRecord,
    QeTerminalRecord,
    QeTerminalStatus,
)
from ..execution import LocalQeResolvedDestinationRole
from ..execution_evidence import QePwEvidenceFailureCode, QePwPublishedEvidence


@dataclass(frozen=True, slots=True)
class QePwResultAssemblyIdentity:
    """Identify one exact ``pw.x`` Workflow-result assembly policy.

    Attributes
    ----------
    value
        Nonempty nominal policy identity.
    """

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("value must be a built-in str")
        if not self.value:
            raise ValueError("value must not be empty")


class _QePwResultAssemblyError(ValueError):
    """Carry one shared application failure code through assembly validation."""

    def __init__(self, code: QePwEvidenceFailureCode, condition: str) -> None:
        super().__init__(condition)
        self.code = code


@dataclass(frozen=True, slots=True, kw_only=True)
class QePwResultAssemblyFailure:
    """Retain one rejected ``pw.x`` Workflow-result assembly.

    Parameters
    ----------
    code
        Shared ``pw.x`` evidence failure code.
    assembly_identity
        Exact result-assembly policy identity.
    result_identity, result_contract_version
        Reserved Workflow result identity and expected result contract.
    observed_condition
        Sanitized nonempty mechanical mismatch description.
    """

    code: QePwEvidenceFailureCode
    assembly_identity: QePwResultAssemblyIdentity
    result_identity: ResultObjectIdentity
    result_contract_version: str
    execution_evidence: QePwPublishedEvidence
    diagnostic_report: QeDiagnosticReport
    extraction_specification: QeNativeOutputExtractionSpecification
    native_output_manifest: QeNativeOutputManifest
    calculator_outcome: QeCalculatorOutcome
    terminal_record: QeTerminalRecord
    published_terminal_record: QePublishedTerminalRecord
    observed_condition: str

    def __post_init__(self) -> None:
        expected = (
            (self.code, QePwEvidenceFailureCode, "code"),
            (
                self.assembly_identity,
                QePwResultAssemblyIdentity,
                "assembly_identity",
            ),
            (self.result_identity, ResultObjectIdentity, "result_identity"),
            (self.execution_evidence, QePwPublishedEvidence, "execution_evidence"),
            (self.diagnostic_report, QeDiagnosticReport, "diagnostic_report"),
            (
                self.extraction_specification,
                QeNativeOutputExtractionSpecification,
                "extraction_specification",
            ),
            (
                self.native_output_manifest,
                QeNativeOutputManifest,
                "native_output_manifest",
            ),
            (self.terminal_record, QeTerminalRecord, "terminal_record"),
            (
                self.published_terminal_record,
                QePublishedTerminalRecord,
                "published_terminal_record",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if type(self.calculator_outcome) not in (
            QeCompletedOutcome,
            QeCalculatorFailedOutcome,
            QeProcessFailedOutcome,
            QeDiagnosticUnresolvedOutcome,
        ):
            raise TypeError("calculator_outcome must be a closed QE outcome variant")
        if type(self.result_contract_version) is not str:
            raise TypeError("result_contract_version must be a built-in str")
        if not self.result_contract_version:
            raise ValueError("result_contract_version must not be empty")
        if type(self.observed_condition) is not str:
            raise TypeError("observed_condition must be a built-in str")
        if not self.observed_condition:
            raise ValueError("observed_condition must not be empty")


type QePwResultAssemblyResult = QePwResult | QePwResultAssemblyFailure


@dataclass(frozen=True, slots=True)
class QePwResultAssembler:
    """Validate terminal evidence and construct one Workflow-facing PW result.

    Parameters
    ----------
    identity
        Exact KSD result-assembly policy identity.

    Notes
    -----
    This action performs no filesystem access, process entry, retry, scientific
    interpretation, convergence decision, or acceptance.
    """

    identity: QePwResultAssemblyIdentity

    def __post_init__(self) -> None:
        if type(self.identity) is not QePwResultAssemblyIdentity:
            raise TypeError("identity must be QePwResultAssemblyIdentity")

    def execute(
        self,
        result_identity: ResultObjectIdentity,
        result_contract_version: str,
        execution_evidence: QePwPublishedEvidence,
        diagnostic_report: QeDiagnosticReport,
        extraction_specification: QeNativeOutputExtractionSpecification,
        native_output_manifest: QeNativeOutputManifest,
        calculator_outcome: QeCalculatorOutcome,
        terminal_record: QeTerminalRecord,
        published_terminal_record: QePublishedTerminalRecord,
    ) -> QePwResultAssemblyResult:
        """Return one exact ``QePwResult`` or typed assembly failure."""
        if type(result_identity) is not ResultObjectIdentity:
            raise TypeError("result_identity must be ResultObjectIdentity")
        if type(result_contract_version) is not str:
            raise TypeError("result_contract_version must be a built-in str")
        if not result_contract_version:
            raise ValueError("result_contract_version must not be empty")
        try:
            self._validate_sources(execution_evidence)
            self._validate_diagnostics(execution_evidence, diagnostic_report)
            self._validate_native_outputs(
                execution_evidence,
                extraction_specification,
                native_output_manifest,
            )
            self._validate_operation_evidence(
                execution_evidence,
                diagnostic_report,
                native_output_manifest,
                calculator_outcome,
                terminal_record,
            )
            self._validate_terminal(
                execution_evidence,
                diagnostic_report,
                native_output_manifest,
                calculator_outcome,
                terminal_record,
                published_terminal_record,
            )
            process = execution_evidence.captured_process.observation
            return QePwResult(
                identity=result_identity,
                execution_input=execution_evidence.prepared_execution.request.execution_input,
                process_observation=process,
                diagnostic_report=diagnostic_report,
                calculator_outcome=calculator_outcome,
                native_output_manifest_identity=native_output_manifest.identity,
                native_output_entry_identities=tuple(
                    sorted(
                        (entry.identity for entry in native_output_manifest.entries),
                        key=lambda value: value.value,
                    )
                ),
                execution_record_manifest_entry_identity=(
                    execution_evidence.publication_entry.identity
                ),
                execution_record_content_identity=execution_evidence.content_identity,
                execution_record_publication_snapshot_identity=(
                    execution_evidence.publication_snapshot.identity
                ),
                terminal_record_identity=terminal_record.identity,
                terminal_record_content_identity=(
                    published_terminal_record.record_artifact.content_identity
                ),
                contract_version=result_contract_version,
            )
        except _QePwResultAssemblyError as error:
            return QePwResultAssemblyFailure(
                code=error.code,
                assembly_identity=self.identity,
                result_identity=result_identity,
                result_contract_version=result_contract_version,
                execution_evidence=execution_evidence,
                diagnostic_report=diagnostic_report,
                extraction_specification=extraction_specification,
                native_output_manifest=native_output_manifest,
                calculator_outcome=calculator_outcome,
                terminal_record=terminal_record,
                published_terminal_record=published_terminal_record,
                observed_condition=str(error),
            )

    def _validate_sources(self, execution_evidence: QePwPublishedEvidence) -> None:
        prepared = execution_evidence.prepared_execution
        expected = tuple(
            sorted(
                (
                    source.artifact_identity
                    for source in prepared.request.external_artifact_sources
                ),
                key=lambda value: value.value,
            )
        )
        observed = tuple(
            value.artifact_identity for value in prepared.source_observations
        )
        predecessors = {
            value.identity
            for value in prepared.request.execution_input.predecessor_native_state
        }
        if (
            observed != expected
            or not predecessors.issubset(set(observed))
            or prepared.calculator_input_binding.execution_input
            is not prepared.request.execution_input
        ):
            raise _QePwResultAssemblyError(
                QePwEvidenceFailureCode.PREPARATION_CORRELATION_MISMATCH,
                "prepared source and predecessor correlations must remain exact",
            )

    def _validate_diagnostics(
        self,
        execution_evidence: QePwPublishedEvidence,
        diagnostic_report: QeDiagnosticReport,
    ) -> None:
        prepared = execution_evidence.prepared_execution
        process = execution_evidence.captured_process.observation
        configuration = prepared.request.executable_configuration
        if (
            configuration.program is not QeProgram.PW
            or diagnostic_report.executable_configuration_identity
            != configuration.identity
            or diagnostic_report.classifier_identity
            != configuration.classifier_identity
            or diagnostic_report.executable_kind is not configuration.executable_kind
            or diagnostic_report.program is not configuration.program
            or diagnostic_report.program_version != configuration.program_version
            or diagnostic_report.stdout_content_identity
            != process.stdout.content_identity
            or diagnostic_report.stderr_content_identity
            != process.stderr.content_identity
        ):
            raise _QePwResultAssemblyError(
                QePwEvidenceFailureCode.DIAGNOSTIC_CORRELATION_MISMATCH,
                "diagnostic report must identify the captured process",
            )

    def _validate_native_outputs(
        self,
        execution_evidence: QePwPublishedEvidence,
        extraction_specification: QeNativeOutputExtractionSpecification,
        native_output_manifest: QeNativeOutputManifest,
    ) -> None:
        prepared = execution_evidence.prepared_execution
        captured = execution_evidence.captured_process
        process = captured.observation
        configuration = prepared.request.executable_configuration
        if (
            extraction_specification.executable_configuration_identity
            != configuration.identity
            or extraction_specification.executable_kind
            is not configuration.executable_kind
            or extraction_specification.program is not configuration.program
            or extraction_specification.program_version != configuration.program_version
            or native_output_manifest.preparation_identity != prepared.identity
            or native_output_manifest.after_snapshot_identity
            != captured.after_snapshot.identity
            or native_output_manifest.extraction_specification_identity
            != extraction_specification.identity
        ):
            raise _QePwResultAssemblyError(
                QePwEvidenceFailureCode.NATIVE_OUTPUT_CORRELATION_MISMATCH,
                "native-output manifest must identify the preparation and snapshot",
            )
        stdout_entries = tuple(
            entry
            for entry in native_output_manifest.entries
            if entry.role is QeNativeOutputRole.STDOUT
        )
        stderr_entries = tuple(
            entry
            for entry in native_output_manifest.entries
            if entry.role is QeNativeOutputRole.STDERR
        )
        if len(stdout_entries) != 1 or len(stderr_entries) != 1:
            raise _QePwResultAssemblyError(
                QePwEvidenceFailureCode.NATIVE_OUTPUT_CORRELATION_MISMATCH,
                "native-output manifest must retain both streams",
            )
        stdout = stdout_entries[0]
        stderr = stderr_entries[0]
        if (
            type(stdout.content) is not QeFileArtifactContent
            or type(stderr.content) is not QeFileArtifactContent
            or stdout.artifact_identity != process.stdout.artifact_identity
            or stderr.artifact_identity != process.stderr.artifact_identity
            or stdout.content.content_identity != process.stdout.content_identity
            or stderr.content.content_identity != process.stderr.content_identity
        ):
            raise _QePwResultAssemblyError(
                QePwEvidenceFailureCode.NATIVE_OUTPUT_CORRELATION_MISMATCH,
                "native-output streams must match captured streams",
            )

    def _validate_operation_evidence(
        self,
        execution_evidence: QePwPublishedEvidence,
        diagnostic_report: QeDiagnosticReport,
        native_output_manifest: QeNativeOutputManifest,
        calculator_outcome: QeCalculatorOutcome,
        terminal_record: QeTerminalRecord,
    ) -> None:
        prepared = execution_evidence.prepared_execution
        process = execution_evidence.captured_process.observation
        try:
            QeOperationResultEvidence(
                execution_input=prepared.request.execution_input,
                process_observation=process,
                diagnostic_report=diagnostic_report,
                calculator_outcome=calculator_outcome,
                native_output_manifest_identity=native_output_manifest.identity,
                native_output_entry_identities=tuple(
                    sorted(
                        (entry.identity for entry in native_output_manifest.entries),
                        key=lambda value: value.value,
                    )
                ),
                terminal_record_identity=terminal_record.identity,
            )
        except ValueError as error:
            raise _QePwResultAssemblyError(
                QePwEvidenceFailureCode.OUTCOME_CORRELATION_MISMATCH,
                str(error),
            ) from error

    def _validate_terminal(
        self,
        execution_evidence: QePwPublishedEvidence,
        diagnostic_report: QeDiagnosticReport,
        native_output_manifest: QeNativeOutputManifest,
        calculator_outcome: QeCalculatorOutcome,
        terminal_record: QeTerminalRecord,
        published_terminal_record: QePublishedTerminalRecord,
    ) -> None:
        prepared = execution_evidence.prepared_execution
        captured = execution_evidence.captured_process
        process = captured.observation
        expected_status: QeTerminalStatus
        if type(calculator_outcome) is QeCompletedOutcome:
            expected_status = QeTerminalStatus.COMPLETED
        elif type(calculator_outcome) is QeCalculatorFailedOutcome:
            expected_status = QeTerminalStatus.CALCULATOR_FAILED
        elif type(calculator_outcome) is QeProcessFailedOutcome:
            expected_status = QeTerminalStatus.PROCESS_FAILED
        else:
            expected_status = QeTerminalStatus.DIAGNOSTIC_UNRESOLVED
        if (
            terminal_record.status is not expected_status
            or terminal_record.simulation_execution_request_identity
            != prepared.request.simulation_execution_request_identity
            or terminal_record.execution_input_identity
            != prepared.request.execution_input.identity
            or terminal_record.preparation_identity != prepared.identity
            or terminal_record.process_observation_identity != process.identity
            or terminal_record.stdout_artifact_identity
            != process.stdout.artifact_identity
            or terminal_record.stdout_content_identity
            != process.stdout.content_identity
            or terminal_record.stderr_artifact_identity
            != process.stderr.artifact_identity
            or terminal_record.stderr_content_identity
            != process.stderr.content_identity
            or terminal_record.before_snapshot_identity
            != captured.before_snapshot.identity
            or terminal_record.after_snapshot_identity
            != captured.after_snapshot.identity
            or terminal_record.execution_record_manifest_entry_identity
            != execution_evidence.publication_entry.identity
            or terminal_record.execution_record_content_identity
            != execution_evidence.content_identity
            or terminal_record.execution_record_publication_snapshot_identity
            != execution_evidence.publication_snapshot.identity
            or terminal_record.diagnostic_report_identity != diagnostic_report.identity
            or terminal_record.native_output_manifest_identity
            != native_output_manifest.identity
        ):
            raise _QePwResultAssemblyError(
                QePwEvidenceFailureCode.TERMINAL_CORRELATION_MISMATCH,
                "terminal record must reference every evidence owner",
            )
        destinations = tuple(
            value
            for value in prepared.resolved_destinations
            if value.role is LocalQeResolvedDestinationRole.TERMINAL_RECORD
        )
        if (
            len(destinations) != 1
            or published_terminal_record.record_artifact.record is not terminal_record
            or published_terminal_record.destination != destinations[0].absolute_path
        ):
            raise _QePwResultAssemblyError(
                QePwEvidenceFailureCode.TERMINAL_CORRELATION_MISMATCH,
                "terminal publication must retain the exact record and destination",
            )
