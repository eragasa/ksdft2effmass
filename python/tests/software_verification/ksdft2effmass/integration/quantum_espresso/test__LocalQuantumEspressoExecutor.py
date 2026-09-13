r"""Software verification of ``LocalQuantumEspressoExecutor``.

Evidence profile: routine

Bounded artifact scope: ``LocalQuantumEspressoExecutionPlan`` and
``LocalQuantumEspressoExecutor`` composition over deterministic fixture resources.

Facet and represented meaning

The artifact verifies exact Workflow effect-request correlation, one-attempt local
fixture execution, immutable QE ResultObjects, and confirmed, rejected, and
indeterminate Workflow dispatch adaptation.

Intrinsic and cross-object scope

Tests cover a completed fixture, diagnostic calculator failure, process timeout,
pre-effect Task and dispatch-entry correlation rejection, post-effect collection and
terminal-publication uncertainty, and terminal no-replace behavior. Lower-level
component behavior remains owned by its focused test modules.

VVUQ and scientific exclusions

All maintained resources are synthetic test data. These tests invoke only the
fixture executable, never Quantum ESPRESSO, and establish no calculator compatibility,
numerical verification, scientific validation, uncertainty quantification, production
readiness, or human acceptance.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from ksdft2effmass.integration.quantum_espresso import (
    LocalQuantumEspressoExecutionPlan,
    LocalQuantumEspressoExecutor,
    LocalQuantumEspressoProcessRunner,
    LocalQuantumEspressoStreamArtifactBindings,
    QuantumEspressoCalculatorFailedOutcome,
    QuantumEspressoCalculatorOutcomeResolver,
    QuantumEspressoCompletedOutcome,
    QuantumEspressoDiagnosticCatalog,
    QuantumEspressoDiagnosticClassifier,
    QuantumEspressoDiagnosticReportIdentity,
    QuantumEspressoInputStager,
    QuantumEspressoNativeOutputCandidateSpecification,
    QuantumEspressoNativeOutputCollector,
    QuantumEspressoNativeOutputExtractionSpecification,
    QuantumEspressoNativeOutputRole,
    QuantumEspressoProcessFailedOutcome,
    QuantumEspressoProcessFailureKind,
    QuantumEspressoPwResult,
    QuantumEspressoTerminalRecordIdentity,
    QuantumEspressoTerminalRecordPublisher,
    QuantumEspressoTerminalRecordSerializer,
    QuantumEspressoWorkspaceEntryType,
    QuantumEspressoWorkspaceSnapshotter,
)
from ksdft2effmass.workflows import (
    ArtifactIdentity,
    DispatchOutcomeKind,
    ResultObjectIdentity,
    SimulationDispatchEffect,
    SimulationDispatchEffectRequest,
    SimulationDispatchObservationIdentity,
    SimulationExecutionAuthorizer,
    TaskDefinitionIdentity,
    TaskInvocationFailureIdentity,
    WorkflowRunRevisionIdentity,
)

from . import test__quantum_espresso_local_execution as local_execution
from .resources.executor_scenarios import ControlScenarioFactory

pytestmark = pytest.mark.software_verification
SUT = LocalQuantumEspressoExecutor


class TestLocalQuantumEspressoExecutor:
    """Own end-to-end software evidence for the authorized local QE executor."""

    @staticmethod
    def reject_hard_link(
        source: Path,
        destination: Path,
        *,
        follow_symlinks: bool = True,
    ) -> None:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        del source, destination, follow_symlinks
        raise OSError("synthetic terminal publication failure")

    @classmethod
    def executor_and_request(
        cls,
        run_root: Path,
        *,
        fixture_mode: str = "--fixture-empty-stderr",
        task_definition_identity: str = "task.simulation.one",
        require_missing_native_result: bool = False,
        workspace_name: str = "attempt-001",
        wall_time_milliseconds: int = 2_000,
    ) -> tuple[LocalQuantumEspressoExecutor, SimulationDispatchEffectRequest]:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        dispatch = ControlScenarioFactory.dispatch_request()
        authorization = SimulationExecutionAuthorizer.execute(
            dispatch.claim_authorization_request
        )
        effect_request = SimulationDispatchEffectRequest(
            execution_request=dispatch.execution_request,
            claim_authorization=authorization,
            claimed_reservation=dispatch.claimed_reservation,
            claim_commit_receipt=dispatch.claim_commit_receipt,
            dispatch_entry_receipt=(
                ControlScenarioFactory.dispatch_entry_receipt(dispatch)
            ),
            outcome_identity=dispatch.outcome_identity,
        )
        correlation = effect_request.execution_request.correlation
        obligation = effect_request.execution_request.obligation
        base = local_execution.TestLocalQuantumEspressoExecutionPreparer.request(
            run_root,
            argument_suffix=(fixture_mode,),
            workspace_name=workspace_name,
            wall_time_milliseconds=wall_time_milliseconds,
            termination_grace_milliseconds=50,
        )
        execution_input = replace(
            base.execution_input,
            task_definition_identity=TaskDefinitionIdentity(task_definition_identity),
            task_instance_identity=correlation.task_instance_identity,
            activation_identity=correlation.activation_identity,
            operation_identity=correlation.operation_identity,
            attempt_identity=correlation.attempt_identity,
        )
        preparation_request = replace(
            base,
            execution_input=execution_input,
            simulation_execution_request_identity=correlation.request_identity,
            scientific_executor_identity=correlation.executor_identity,
            dispatch_destination_identity=obligation.destination_identity,
            dispatch_resource_scope_identity=obligation.resource_scope_identities[0],
            authorization_result_identity=(
                effect_request.execution_request.preparation_authorization.identity
            ),
        )
        candidates = [
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
        ]
        if require_missing_native_result:
            candidates.append(
                QuantumEspressoNativeOutputCandidateSpecification(
                    artifact_identity=ArtifactIdentity("artifact.native-result"),
                    role=QuantumEspressoNativeOutputRole.NATIVE_RESULT,
                    relative_path=preparation_request.result_destination,
                    entry_type=QuantumEspressoWorkspaceEntryType.DIRECTORY,
                    required=True,
                )
            )
        extraction = QuantumEspressoNativeOutputExtractionSpecification(
            identity="fixture-extraction:1",
            executable_configuration_identity=(
                preparation_request.executable_configuration.identity
            ),
            program=preparation_request.executable_configuration.program,
            executable_kind=(
                preparation_request.executable_configuration.executable_kind
            ),
            program_version=preparation_request.executable_configuration.program_version,
            candidates=tuple(
                sorted(candidates, key=lambda value: value.artifact_identity.value)
            ),
        )
        streams = LocalQuantumEspressoStreamArtifactBindings(
            stdout_artifact_identity=ArtifactIdentity("artifact.stdout"),
            stderr_artifact_identity=ArtifactIdentity("artifact.stderr"),
        )
        plan = LocalQuantumEspressoExecutionPlan(
            preparation_request=preparation_request,
            extraction_specification=extraction,
            stream_artifacts=streams,
            diagnostic_report_identity=QuantumEspressoDiagnosticReportIdentity(
                "diagnostic-report.one"
            ),
            result_object_identity=ResultObjectIdentity("result.qe.one"),
            terminal_record_identity=QuantumEspressoTerminalRecordIdentity(
                "terminal.qe.one"
            ),
            dispatch_observation_identity=SimulationDispatchObservationIdentity(
                "dispatch-observation.qe.one"
            ),
            dispatch_outcome_identity=effect_request.outcome_identity,
            task_failure_identity=TaskInvocationFailureIdentity("failure.qe.one"),
            workflow_run_identity=correlation.workflow_run_identity,
            grant_identity=correlation.grant_identity,
            grant_authority_reference=(
                effect_request.claim_authorization.request.grant.authority_reference
            ),
            obligation_identity=correlation.obligation_identity,
            claim_authorization_result_identity=effect_request.claim_authorization.identity,
            dispatch_entry_identity=(
                effect_request.dispatch_entry_receipt.dispatch_entry_identity
            ),
            dispatch_entry_revision_identity=(
                effect_request.dispatch_entry_receipt.committed_revision_identity
            ),
            input_result_reference_identities=(
                correlation.input_result_reference_identities
            ),
            input_artifact_entry_identities=correlation.input_artifact_entry_identities,
            result_contract_version="qe-pw-result:1",
            diagnostic_claim_boundary=(
                "synthetic fixture diagnostics establish software behavior only",
            ),
        )
        snapshotter = QuantumEspressoWorkspaceSnapshotter("qe-snapshotter:1")
        executor = SUT(
            plan=plan,
            preparer=local_execution.TestLocalQuantumEspressoExecutionPreparer.preparer(),
            stager=QuantumEspressoInputStager("qe-input-stager:1"),
            process_runner=LocalQuantumEspressoProcessRunner(
                observer_version="qe-process-observer:1",
                snapshotter=snapshotter,
            ),
            classifier=QuantumEspressoDiagnosticClassifier(
                QuantumEspressoDiagnosticCatalog.fixture_pw_v1()
            ),
            collector=QuantumEspressoNativeOutputCollector("qe-output-collector:1"),
            outcome_resolver=QuantumEspressoCalculatorOutcomeResolver(
                "qe-outcome-resolver:1"
            ),
            terminal_serializer=QuantumEspressoTerminalRecordSerializer(),
            terminal_publisher=QuantumEspressoTerminalRecordPublisher(
                "qe-terminal-publisher:1", snapshotter
            ),
        )
        return executor, effect_request

    def test_method__execute__completed_fixture_returns_confirmed_immutable_pw_result(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-QE-EXECUTOR-001

        Requirement: One exactly authorized and completed fixture attempt composes
        staging, capture, diagnostics, collection, outcome resolution, and terminal
        publication into a confirmed operation-specific ResultObject.

        Acceptance: The outcome is confirmed, its QE outcome is completed, exact
        manifest identities agree, and the terminal record exists without a retry.
        """
        executor, request = self.executor_and_request(tmp_path.resolve())

        outcome = executor.execute(request)

        assert isinstance(executor, SimulationDispatchEffect)
        assert outcome.kind is DispatchOutcomeKind.CONFIRMED
        assert type(outcome.result) is QuantumEspressoPwResult
        calculator_outcome = outcome.result.evidence.calculator_outcome
        assert type(calculator_outcome) is QuantumEspressoCompletedOutcome
        assert calculator_outcome.completion_marker_identities
        assert (
            outcome.native_output_manifest_identity
            == outcome.result.evidence.native_output_manifest_identity
        )
        terminal = tmp_path / "attempt-001" / "records" / "terminal.json"
        assert terminal.is_file()
        assert not hasattr(outcome.result, "retry")

    def test_method__execute__fatal_fixture_confirms_calculator_failure_result(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-QE-EXECUTOR-002

        Requirement: A determinately captured fatal calculator diagnostic is an
        immutable operation result rather than dispatch rejection.

        Acceptance: The dispatch is confirmed with calculator-failed evidence.
        """
        executor, request = self.executor_and_request(
            tmp_path.resolve(), fixture_mode="--fixture-calculator-fail"
        )

        outcome = executor.execute(request)

        assert outcome.kind is DispatchOutcomeKind.CONFIRMED
        assert type(outcome.result) is QuantumEspressoPwResult
        assert type(outcome.result.evidence.calculator_outcome) is (
            QuantumEspressoCalculatorFailedOutcome
        )

    def test_method__execute__timeout_confirms_process_failure_result(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-QE-EXECUTOR-003

        Requirement: A closed timeout lifecycle with exact captures remains a
        determinate calculator operation result.

        Acceptance: The dispatch is confirmed with timeout process-failure evidence.
        """
        executor, request = self.executor_and_request(
            tmp_path.resolve(),
            fixture_mode="--fixture-timeout",
            wall_time_milliseconds=20,
        )

        outcome = executor.execute(request)

        assert outcome.kind is DispatchOutcomeKind.CONFIRMED
        assert type(outcome.result) is QuantumEspressoPwResult
        calculator_outcome = outcome.result.evidence.calculator_outcome
        assert type(calculator_outcome) is QuantumEspressoProcessFailedOutcome
        assert calculator_outcome.reason is QuantumEspressoProcessFailureKind.TIMEOUT

    def test_method__execute__task_identity_mismatch_rejects_before_mutation(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-QE-EXECUTOR-004

        Requirement: The concrete executor independently checks exact Task and
        authorization correlation before local effects.

        Acceptance: Mismatched Task definition is rejected and creates no workspace.
        """
        executor, request = self.executor_and_request(
            tmp_path.resolve(), task_definition_identity="task.definition.mismatch"
        )

        outcome = executor.execute(request)

        assert outcome.kind is DispatchOutcomeKind.REJECTED
        assert outcome.failure is not None
        assert (
            outcome.failure.code
            == "quantum_espresso.authorization_correlation_mismatch"
        )
        assert tuple(tmp_path.iterdir()) == ()

    def test_method__execute__dispatch_entry_revision_mismatch_rejects_before_mutation(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-QE-EXECUTOR-005

        Requirement: Executor-boundary admission retains the exact committed
        dispatch-entry revision rather than checking only the executor name.

        Acceptance: A mismatched planned entry revision is rejected before workspace
        mutation or process entry.
        """
        executor, request = self.executor_and_request(tmp_path.resolve())
        mismatched = replace(
            executor,
            plan=replace(
                executor.plan,
                dispatch_entry_revision_identity=WorkflowRunRevisionIdentity(
                    "revision.dispatch-mismatch"
                ),
            ),
        )

        outcome = mismatched.execute(request)

        assert outcome.kind is DispatchOutcomeKind.REJECTED
        assert outcome.failure is not None
        assert tuple(tmp_path.iterdir()) == ()

    def test_method__execute__post_process_collection_failure_is_indeterminate(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-QE-EXECUTOR-006

        Requirement: Failure to close required native output after process entry does
        not become a rejected or successful operation.

        Acceptance: The dispatch is indeterminate with reconciliation identities and
        no terminal result.
        """
        executor, request = self.executor_and_request(
            tmp_path.resolve(), require_missing_native_result=True
        )

        outcome = executor.execute(request)

        assert outcome.kind is DispatchOutcomeKind.INDETERMINATE
        assert outcome.reconciliation_identity_values
        assert outcome.result is None
        assert not (tmp_path / "attempt-001" / "records" / "terminal.json").exists()

    def test_method__execute__terminal_publication_failure_is_indeterminate(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Evidence ID: SV-QE-EXECUTOR-007

        Requirement: Failure to atomically publish terminal evidence after process
        entry cannot become a confirmed result or a pre-effect rejection.

        Acceptance: A deterministic hard-link failure produces an indeterminate
        dispatch with no result and no published terminal destination.
        """
        executor, request = self.executor_and_request(tmp_path.resolve())
        monkeypatch.setattr(
            QuantumEspressoTerminalRecordPublisher,
            "_link",
            staticmethod(self.reject_hard_link),
        )

        outcome = executor.execute(request)

        assert outcome.kind is DispatchOutcomeKind.INDETERMINATE
        assert outcome.result is None
        assert any(
            value.startswith("qe-terminal-publication-failure:")
            for value in outcome.reconciliation_identity_values
        )
        assert not (tmp_path / "attempt-001" / "records" / "terminal.json").exists()

    def test_method__execute__preexisting_terminal_rejects_without_replacement(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-QE-EXECUTOR-008

        Requirement: An existing attempt workspace and terminal are never replaced;
        retries require fresh Workflow and workspace identities.

        Acceptance: The single attempted dispatch is rejected before staging and the
        preexisting terminal bytes remain unchanged.
        """
        executor, request = self.executor_and_request(tmp_path.resolve())
        terminal = tmp_path / "attempt-001" / "records" / "terminal.json"
        terminal.parent.mkdir(parents=True)
        terminal.write_bytes(b"preexisting terminal\n")
        before = terminal.read_bytes()

        outcome = executor.execute(request)

        assert outcome.kind is DispatchOutcomeKind.REJECTED
        assert outcome.failure is not None
        assert outcome.failure.code == "quantum_espresso.preparation_failed"
        assert terminal.read_bytes() == before
