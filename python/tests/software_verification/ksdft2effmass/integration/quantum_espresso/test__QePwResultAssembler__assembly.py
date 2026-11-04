"""Software verification of final ``pw.x`` Workflow-result assembly."""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path

import pytest

from ksdft2effmass.integration.quantum_espresso import (
    LocalQeCapturedProcess,
    LocalQePreparedExecution,
    QeCalculatorInputAdmission,
    QeCalculatorInputBinding,
    QeCalculatorOutcome,
    QeDiagnosticClassificationRequest,
    QeDiagnosticReport,
    QeNativeOutputExtractionSpecification,
    QeNativeOutputManifest,
    QeProcessFailedOutcome,
    QeProcessFailureKind,
    QePublishedTerminalRecord,
    QePwEvidenceFailureCode,
    QePwObservation,
    QePwPublishedEvidence,
    QePwResult,
    QePwResultAssembler,
    QePwResultAssemblyFailure,
    QeStagedExecution,
    QeTerminalRecord,
    QeTerminalRecordArtifact,
    QeTerminalStatus,
)
from ksdft2effmass.workflows import (
    ArtifactContentIdentity,
    ArtifactManifestIdentity,
    ResultObjectIdentity,
)

from .test__LocalQeExecutor__execution import (
    TestLocalQeExecutor as _ExecutorScenario,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


@dataclass(frozen=True, slots=True)
class _AssemblyScenario:
    """Retain exact successful inputs for one result-assembly test."""

    evidence: QePwPublishedEvidence
    report: QeDiagnosticReport
    extraction_specification: QeNativeOutputExtractionSpecification
    manifest: QeNativeOutputManifest
    outcome: QeCalculatorOutcome
    terminal: QeTerminalRecord
    terminal_artifact: QeTerminalRecordArtifact
    publication: QePublishedTerminalRecord
    result_identity: ResultObjectIdentity
    result_contract_version: str


class TestQePwResultAssembler:
    """Assemble one exact ``pw.x`` result or return a shared failure code."""

    def test_execute_returns_exact_pw_result(self, tmp_path: Path) -> None:
        scenario, assembler = self._scenario(tmp_path.resolve())

        result = assembler.execute(
            scenario.result_identity,
            scenario.result_contract_version,
            scenario.evidence,
            scenario.report,
            scenario.extraction_specification,
            scenario.manifest,
            scenario.outcome,
            scenario.terminal,
            scenario.publication,
        )

        assert type(result) is QePwResult
        assert result.identity == scenario.result_identity
        assert result.diagnostic_report is scenario.report
        assert result.native_output_manifest_identity == scenario.manifest.identity
        assert (
            result.execution_record_content_identity
            == scenario.evidence.content_identity
        )
        assert (
            result.terminal_record_content_identity
            == scenario.terminal_artifact.content_identity
        )

    def test_execute_rejects_diagnostic_correlation_mismatch(
        self, tmp_path: Path
    ) -> None:
        scenario, assembler = self._scenario(tmp_path.resolve())
        report = replace(
            scenario.report,
            executable_configuration_identity=replace(
                scenario.report.executable_configuration_identity,
                value="different-configuration",
            ),
        )

        result = assembler.execute(
            scenario.result_identity,
            scenario.result_contract_version,
            scenario.evidence,
            report,
            scenario.extraction_specification,
            scenario.manifest,
            scenario.outcome,
            scenario.terminal,
            scenario.publication,
        )

        assert type(result) is QePwResultAssemblyFailure
        assert result.code is (QePwEvidenceFailureCode.DIAGNOSTIC_CORRELATION_MISMATCH)

    def test_execute_rejects_native_output_snapshot_mismatch(
        self, tmp_path: Path
    ) -> None:
        scenario, assembler = self._scenario(tmp_path.resolve())
        manifest = replace(
            scenario.manifest,
            after_snapshot_identity=ArtifactManifestIdentity("different-snapshot"),
        )

        result = assembler.execute(
            scenario.result_identity,
            scenario.result_contract_version,
            scenario.evidence,
            scenario.report,
            scenario.extraction_specification,
            manifest,
            scenario.outcome,
            scenario.terminal,
            scenario.publication,
        )

        assert type(result) is QePwResultAssemblyFailure
        assert result.code is (
            QePwEvidenceFailureCode.NATIVE_OUTPUT_CORRELATION_MISMATCH
        )

    def test_execute_rejects_outcome_correlation_mismatch(self, tmp_path: Path) -> None:
        scenario, assembler = self._scenario(tmp_path.resolve())
        outcome = QeProcessFailedOutcome(QeProcessFailureKind.NONZERO_EXIT)

        result = assembler.execute(
            scenario.result_identity,
            scenario.result_contract_version,
            scenario.evidence,
            scenario.report,
            scenario.extraction_specification,
            scenario.manifest,
            outcome,
            scenario.terminal,
            scenario.publication,
        )

        assert type(result) is QePwResultAssemblyFailure
        assert result.code is QePwEvidenceFailureCode.OUTCOME_CORRELATION_MISMATCH

    def test_execute_rejects_terminal_execution_record_mismatch(
        self, tmp_path: Path
    ) -> None:
        scenario, assembler = self._scenario(tmp_path.resolve())
        terminal = replace(
            scenario.terminal,
            execution_record_content_identity=ArtifactContentIdentity(
                "sha256", "f" * 64, 1
            ),
        )

        result = assembler.execute(
            scenario.result_identity,
            scenario.result_contract_version,
            scenario.evidence,
            scenario.report,
            scenario.extraction_specification,
            scenario.manifest,
            scenario.outcome,
            terminal,
            scenario.publication,
        )

        assert type(result) is QePwResultAssemblyFailure
        assert result.code is QePwEvidenceFailureCode.TERMINAL_CORRELATION_MISMATCH

    def test_execute_rejects_missing_predecessor_source_correlation(
        self, tmp_path: Path
    ) -> None:
        scenario, assembler = self._scenario(
            tmp_path.resolve(), include_predecessor=True
        )
        prepared = scenario.evidence.prepared_execution
        incomplete_prepared = replace(
            prepared,
            source_observations=tuple(
                value
                for value in prepared.source_observations
                if value.artifact_identity.value != "artifact.state"
            ),
        )
        observation = replace(
            scenario.evidence.observation_binding,
            prepared_execution=incomplete_prepared,
        )
        evidence = replace(scenario.evidence, observation_binding=observation)

        result = assembler.execute(
            scenario.result_identity,
            scenario.result_contract_version,
            evidence,
            scenario.report,
            scenario.extraction_specification,
            scenario.manifest,
            scenario.outcome,
            scenario.terminal,
            scenario.publication,
        )

        assert type(result) is QePwResultAssemblyFailure
        assert result.code is (QePwEvidenceFailureCode.PREPARATION_CORRELATION_MISMATCH)

    def _scenario(
        self, root: Path, *, include_predecessor: bool = False
    ) -> tuple[_AssemblyScenario, QePwResultAssembler]:
        executor, _request = _ExecutorScenario.executor_and_request(
            root, include_predecessor=include_predecessor
        )
        plan = executor.plan
        input_binding = QeCalculatorInputAdmission(
            plan.calculator_input_admission_policy_identity
        ).execute(plan.calculator_input, plan.preparation_request.execution_input)
        assert type(input_binding) is QeCalculatorInputBinding
        prepared = executor.preparer.execute(plan.preparation_request, input_binding)
        assert type(prepared) is LocalQePreparedExecution
        staged = executor.stager.execute(prepared, input_binding)
        assert type(staged) is QeStagedExecution
        process = executor.process_runner.execute(
            prepared, staged, plan.stream_artifacts
        )
        assert type(process) is LocalQeCapturedProcess
        observation = executor.evidence_adapter.execute(prepared, process)
        assert type(observation) is QePwObservation
        evidence = executor.evidence_publisher.execute(observation)
        assert type(evidence) is QePwPublishedEvidence
        report = executor.classifier.execute(
            QeDiagnosticClassificationRequest(
                report_identity=plan.diagnostic_report_identity,
                configuration=plan.preparation_request.executable_configuration,
                stdout=process.stdout_bytes,
                stderr=process.stderr_bytes,
                stdout_content_identity=process.observation.stdout.content_identity,
                stderr_content_identity=process.observation.stderr.content_identity,
                claim_boundary=plan.diagnostic_claim_boundary,
            )
        )
        manifest = executor.collector.execute(
            process.after_snapshot, plan.extraction_specification
        )
        assert type(manifest) is QeNativeOutputManifest
        outcome = executor.outcome_resolver.execute(
            process.observation,
            report,
            manifest,
            plan.extraction_specification,
        )
        terminal = QeTerminalRecord(
            identity=plan.terminal_record_identity,
            status=QeTerminalStatus.COMPLETED,
            simulation_execution_request_identity=(
                plan.preparation_request.simulation_execution_request_identity
            ),
            execution_input_identity=plan.preparation_request.execution_input.identity,
            preparation_identity=prepared.identity,
            process_observation_identity=process.observation.identity,
            stdout_artifact_identity=process.observation.stdout.artifact_identity,
            stdout_content_identity=process.observation.stdout.content_identity,
            stderr_artifact_identity=process.observation.stderr.artifact_identity,
            stderr_content_identity=process.observation.stderr.content_identity,
            before_snapshot_identity=process.before_snapshot.identity,
            after_snapshot_identity=process.after_snapshot.identity,
            execution_record_manifest_entry_identity=evidence.publication_entry.identity,
            execution_record_content_identity=evidence.content_identity,
            execution_record_publication_snapshot_identity=(
                evidence.publication_snapshot.identity
            ),
            diagnostic_report_identity=report.identity,
            native_output_manifest_identity=manifest.identity,
        )
        terminal_artifact = executor.terminal_serializer.execute(terminal)
        publication = executor.terminal_publisher.execute(prepared, terminal_artifact)
        assert type(publication) is QePublishedTerminalRecord
        return (
            _AssemblyScenario(
                evidence=evidence,
                report=report,
                extraction_specification=plan.extraction_specification,
                manifest=manifest,
                outcome=outcome,
                terminal=terminal,
                terminal_artifact=terminal_artifact,
                publication=publication,
                result_identity=plan.result_object_identity,
                result_contract_version=plan.result_contract_version,
            ),
            executor.result_assembler,
        )
